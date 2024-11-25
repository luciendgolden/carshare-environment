from flask import Blueprint, jsonify, current_app, request, Response

import requests

db_operations_blueprint = Blueprint('database_operations', __name__)

# This method allows to add additional rdfs to the domain knowledge, making it dynamically extendable.
@db_operations_blueprint.route('/add', methods=['POST'])
def populate_db():
    graphdb_url = current_app.config['GRAPHDB_URL']
    repository_id = current_app.config['GRAPHDB_REPOSITORY']
    
    try:
        rdf_data = request.get_data(as_text=True)
        headers = {'Content-Type': 'text/turtle'}
        response = requests.post(f"{graphdb_url}/repositories/{repository_id}/statements", data=rdf_data, headers=headers)
        
        if response.status_code in [200, 201, 204]:
            return jsonify({'success': True, 'message': 'Repository populated successfully'})
        else:
            return jsonify({'success': False, 'message': 'Error while populating repository', 'error': response.text})
    
    except Exception as e:
        return jsonify({'success': False, 'message': 'Internal server error', 'error': str(e)}), 500

# This method will erase the existing rdfs from the graphDB
@db_operations_blueprint.route('/erase', methods=['POST'])
def erase_db():
    graphdb_url = current_app.config['GRAPHDB_URL']
    repository_id = current_app.config['GRAPHDB_REPOSITORY']
    
    try:
        statement = "DELETE {?s ?p ?o .} WHERE {?s ?p ?o .}"
        response = requests.post(f"{graphdb_url}/repositories/{repository_id}/statements?update={statement}")
        
        if response.status_code in [200, 201, 204]:
            return jsonify({'success': True, 'message': 'Repository is empty'})
        else:
            return jsonify({'success': False, 'message': 'Error while erasing data from repository', 'error': response.text})
    
    except Exception as e:
        return jsonify({'success': False, 'message': 'Internal server error', 'error': str(e)}), 500

# This method allows executing different GraphDB statements
@db_operations_blueprint.route('/sparql', methods=['POST'])
def send_sparql():
    graphdb_url = current_app.config['GRAPHDB_URL']
    repository_id = current_app.config['GRAPHDB_REPOSITORY']

    try:
        query = request.values.get("q")
        statement = request.values.get("u")

        if query is not None:
            response = requests.post(
                f"{graphdb_url}/repositories/{repository_id}",
                data={'query': query},
                headers={
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Accept": "application/sparql-results+json"
                }
            )
        elif statement is not None:
            response = requests.post(
                f"{graphdb_url}/repositories/{repository_id}/statements",
                data=statement,
                headers={
                    "Content-Type": "application/sparql-update",
                    "Accept": "application/sparql-results+json"
                }
            )
        else:
            current_app.logger.warning("Neither 'u' (update) nor 'q' (query) provided in the request.")
            return jsonify({'success': False, 'message': 'No SPARQL statement or query provided'}), 400

        return Response(
            response.content, 
            status=response.status_code, 
            content_type=response.headers.get('Content-Type')
        )

    except requests.exceptions.RequestException as e:
        current_app.logger.error(f"RequestException occurred: {e}")
        return jsonify({'success': False, 'message': 'Failed to connect to GraphDB', 'error': str(e)}), 502

    except Exception as e:
        current_app.logger.error(f"Unexpected error: {e}")
        return jsonify({'success': False, 'message': 'Internal server error', 'error': str(e)}), 500