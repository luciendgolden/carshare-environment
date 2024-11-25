from flask import Blueprint, jsonify, request, current_app

from app.services.graphdb import (
    execute_sparql_query, 
    get_rdf_for_user, 
    llm_summarize_data_in_nl,
    execute_sparql_update,
    flatten_rdf_data,
    structure_for_llm,
    get_relevant_rdf, 
    llm_sparql_from_question, 
    filter_out_blank_nodes
)

request_management_blueprint = Blueprint('request_management', __name__)

@request_management_blueprint.route('/from/nlp', methods=['POST'])
def question():
    """
    This method allows to ask question from the rdf store
    and receive semi-structured data in response.
    """
    requestBody = request.get_json()
    question = requestBody.get('question')
    user_id = requestBody.get('userId')
    
    current_app.logger.debug(f"/from/nlp Request body: {requestBody}")

    if user_id is None:
        response = get_relevant_rdf()
    else:
        question += ". for the user with id - " + f'"{user_id}"'
        response = get_rdf_for_user(user_id)
        
    current_app.logger.debug(f"/from/nlp Question: {question}")
    current_app.logger.debug(f"/from/nlp Response: {response}")

    if not response.get('success'):
        # Handle failure to get RDF data
        current_app.logger.error("Failed to get RDF data.")
        return jsonify({'error': 'Failed to get RDF data', 'details': response.get('message')}), 500

    # LLM SPARQL query from the question and the RDF data
    query = llm_sparql_from_question(question, response['data'])
    current_app.logger.debug(f"Generated SPARQL query: {query}")
    
    if query is None:
        return jsonify({'error': 'Failed to form a query'}), 500

    # Determine if it's a query or update
    first_keyword = query.split()[0].upper()

    if first_keyword in ["SELECT", "ASK", "CONSTRUCT", "DESCRIBE"]:
        sparql_data_response = execute_sparql_query(query, expect_json=True)
    elif first_keyword in ["INSERT", "DELETE", "LOAD", "CLEAR", "CREATE", "DROP", "COPY", "MOVE", "ADD"]:
        sparql_data_response = execute_sparql_update(query)
    else:
        return jsonify({'error': 'Invalid SPARQL operation'}), 400

    if not sparql_data_response.get('success'):
        return jsonify({'error': 'Failed to execute SPARQL operation', 'details': sparql_data_response.get('message'), 'response': sparql_data_response.get('error')}), 500

    # Handle the response for queries
    if first_keyword in ["SELECT", "ASK", "CONSTRUCT", "DESCRIBE"]:
        filtered_data = filter_out_blank_nodes(sparql_data_response['data'])
        current_app.logger.debug(f"Filtered data: {filtered_data}")
    
        flattened_data = flatten_rdf_data(filtered_data)
        structured_data = structure_for_llm(flattened_data)
    
        summary = llm_summarize_data_in_nl(structured_data)

        return jsonify({'success': True, 'data': structured_data, 'summary': summary}), 200
    else:
        # If it's an update, simply return the success response
        return jsonify({'success': True, 'summary': 'SPARQL update executed successfully'}), 200

"""
Receives a JSON object and sends it to the LLM in order to generate a human-readable summary.
"""
@request_management_blueprint.route('/from/json', methods=['POST'])
def from_json():
    requestBody = request.get_json()
    current_app.logger.debug(f"/from/json Request body: {requestBody}")

    summary = llm_summarize_data_in_nl(requestBody)
    current_app.logger.debug(f"/from/json Summary: {summary}")

    return jsonify({'success': True, 'summary': summary}), 200