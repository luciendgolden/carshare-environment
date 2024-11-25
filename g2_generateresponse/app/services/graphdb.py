"""
Includes all functions for GraphDB interactions, 
such as creating repositories, executing SPARQL queries, 
and processing RDF data. 
"""

import os
import time
import requests
from flask import current_app
import logging
from requests_toolbelt.multipart.encoder import MultipartEncoder
from app.utils import get_resource_path
from openai import OpenAI

logger = logging.getLogger(__name__)

last_request_time = 0
min_interval = 1

def get_openai_client(api_key):
    return OpenAI(api_key=api_key)

def get_config_values():
    config = {
        'graphdb_url': current_app.config['GRAPHDB_URL'],
        'repository_id': current_app.config['GRAPHDB_REPOSITORY'],
        'sparql_endpoint': f"{current_app.config['GRAPHDB_URL']}/repositories/{current_app.config['GRAPHDB_REPOSITORY']}",
        'llama_endpoint': current_app.config.get("LLAMA_ENDPOINT"),
        'llama_chat_endpoint': f"{current_app.config.get('LLAMA_ENDPOINT')}/v1/chat/completions",
        'openai_endpoint': current_app.config.get("OPENAI_ENDPOINT"),
        'openai_api_key': current_app.config.get("OPENAI_API_KEY"),
        'llama_key': current_app.config.get("LLAMA_API_KEY"),
    }
    config['openai_client'] = get_openai_client(config['openai_api_key'])  # Create OpenAI client
    return config

def repo_exists():
    config = get_config_values()
    resp = requests.get(f"{config['graphdb_url']}/repositories")
    return resp.ok and config['repository_id'] in resp.text


def create_repo():
    config = get_config_values()
    config_path = get_resource_path('config.ttl')
    
    if not config_path:
        raise FileNotFoundError("Repository configuration file not found.")

    multipart_encoder = MultipartEncoder(fields={'config': (config_path, open(config_path, 'rb'), 'text/turtle')})
    headers = {'Content-Type': multipart_encoder.content_type}
    response = requests.post(f"{config['graphdb_url']}/rest/repositories/", data=multipart_encoder, headers=headers)
    return handle_response(response)

def preload_rdf(file_name):
    config = get_config_values()
    file_path = get_resource_path(file_name)
    if not file_path:
        current_app.logger.info(f"File {file_name} not found.")
        return False

    with open(file_path, 'rb') as file:
        headers = {'Content-Type': 'text/turtle'}
        response = requests.post(f"{config['graphdb_url']}/repositories/{config['repository_id']}/statements", data=file, headers=headers)
    return handle_response(response)


def handle_response(response, expect_json=False):
    if response.status_code in [200, 201, 204]:
        try:
            content = response.json() if expect_json else response.text
            return {'success': True, 'message': 'Operation successful', 'data': content}
        except ValueError:
            return {'success': True, 'message': 'Operation successful but no JSON content', 'data': None} if expect_json else {'success': True, 'message': 'Operation successful'}
    else:
        current_app.logger.error(f"Operation failed: {response.status_code}, {response.text}")
        return {'success': False, 'message': 'Operation failed', 'error': response.text, 'status_code': response.status_code}

# Executes a SPARQL query on the GraphDB and returns the results.
def execute_sparql_query(query, headers=None, expect_json=False):
    config = get_config_values()
    
    data = {
        "query": query,
    }

    if headers is None:
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/sparql-results+json"
        }

    current_app.logger.debug(f"execute_sparql_query SPARQL Query: {query}")
    current_app.logger.debug(f"execute_sparql_query Headers: {headers}")
    current_app.logger.debug(f"execute_sparql_query Endpoint: {config['sparql_endpoint']}")

    response = requests.post(f"{config['sparql_endpoint']}", headers=headers, data=data)

    response_dict = handle_response(response, expect_json=expect_json)
    
    if response_dict['success']:
        current_app.logger.debug(f"Successfully executed SPARQL query.")

    return response_dict

def execute_sparql_update(statement, headers=None):
    config = get_config_values()
    
    current_app.logger.debug(f"execute_sparql_update")
    current_app.logger.debug(f"{statement}")
    
    if headers is None:
        headers = {
            "Content-Type": "application/sparql-update",
            "Accept": "application/sparql-results+json"
        }

    response = requests.post(f"{config['sparql_endpoint']}/statements", headers=headers, data=statement)
    
    response_dict = handle_response(response)
    
    if response_dict['success']:
        current_app.logger.debug(f"Successfully executed SPARQL update.")

    return response_dict

# Limits the rdf that is being sent to GPT and returns only rdfs related to the given user_id.
# Was introduced to deal with "Token limit reached" error from GPT, due to large amount of rdfs being sent in a single GPT call.
def get_rdf_for_user(user_id):
    query = f"""
    PREFIX carshare: <http://example.org/carshare#> 
    SELECT * WHERE {{
        ?client carshare:clientID "{user_id}" .
        ?client ?p ?o .
    }}
    """
    return execute_sparql_query(query, headers={"Accept": "*/*"})

# Limits the rdf that is being sent to GPT and returns only relevant rdfs, without all the unnecessary Property, Type rdfs from the graphDB.
# Was introduced to deal with "Token limit reached" error from GPT, due to large amount of rdfs being sent in a single GPT call.
def get_relevant_rdf():
    query = """
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    CONSTRUCT { ?s ?p ?o . } WHERE {
        ?s ?p ?o .
        FILTER (!strstarts(str(?p), str(rdf:)) && !strstarts(str(?p), str(rdfs:)) && !strstarts(str(?p), str(owl:)))
    }
    """
    return execute_sparql_query(query, headers={"Accept": "*/*"})


def filter_out_blank_nodes(data):
    """Filters out RDF triples containing blank nodes from the provided data.

    Args:
    - data (dict): The RDF data as a SPARQL query response.

    Returns:
    - dict: Filtered RDF data without blank nodes.
    """
    if not data or 'results' not in data or 'bindings' not in data['results']:
        current_app.logger.debug("No RDF data or unexpected format.")
        return data

    filtered_data = {"head": data["head"], "results": {"bindings": []}}
    for result in data['results']['bindings']:
        # Check for blank nodes in triple components and skip those triples
        if all(value.get('type') != 'bnode' for value in result.values()):
            filtered_data['results']['bindings'].append(result)
    return filtered_data

def uri_to_readable(uri):
    """Converts URI to a more readable format by extracting the last part."""
    # Extract the last part of the URI after the # or the last /, whichever is found last.
    return uri.split('#')[-1].split('/')[-1]

def prepare_rdf_for_llm(data):
    """Converts RDF data into a format suitable for LLM summarization.

    This function dynamically constructs sentences from SPARQL response bindings,
    creating meaningful RDF triples as strings for LLM processing.

    Args:
    - data (dict): Filtered RDF data without blank nodes, from a SPARQL response.

    Returns:
    - str: A string representation of RDF triples for LLM processing.
    """
    triples = []
    for binding in data.get('results', {}).get('bindings', []):
        # Construct a triple (s, p, o) for each binding, making URIs readable
        triple_parts = []
        for var in sorted(binding.keys()):
            value = binding[var]['value']
            if binding[var]['type'] == 'uri':
                readable_value = uri_to_readable(value)
            else:
                readable_value = value
            triple_parts.append(readable_value)
        
        if len(triple_parts) == 3:
            triples.append(f"- ({triple_parts[0]}, {triple_parts[1]}, {triple_parts[2]})")

    rdf_summary = '\n'.join(triples)
    return rdf_summary

def flatten_rdf_data(data):
    """
    Converts RDF data into a structured format for easier processing by LLM.

    Args:
    - data (dict): RDF data from a SPARQL query.

    Returns:
    - list: A list of dictionaries representing the RDF triples.
    """
    flattened_data = []
    for binding in data.get('results', {}).get('bindings', []):
        entry = {}
        for var, value_dict in binding.items():
            value = value_dict['value']
            if value_dict['type'] == 'uri':
                entry[var] = uri_to_readable(value)
            else:
                entry[var] = value
        flattened_data.append(entry)
    return flattened_data

def structure_for_llm(flattened_data):
    """
    Organizes flattened RDF data into a structured JSON format for LLM summarization.

    Args:
    - flattened_data (list): A list of flattened RDF entries.

    Returns:
    - dict: A structured representation of the data.
    """
    structured_data = {}
    for entry in flattened_data:
        for key, value in entry.items():
            if key not in structured_data:
                structured_data[key] = []
            structured_data[key].append(value)
    
    return structured_data

def llm_summarize_data_in_nl(data):
    config = get_config_values()
    client = config['openai_client']
    
    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": """
                    You will be given data and your job is to GENERATE A SHORT HUMAN READABLE SUMMARY. 
                    The response should be written such that it sounds like YOU are presenting it to the user.
                    """
                },
                {
                    "role": "user",
                    "content": f"data={data}"
                }
            ]
        )

        current_app.logger.debug(f"Generated LLM Message: {completion.choices[0].message}")
        
        summary = completion.choices[0].message.content
        
        return summary
    except Exception as e:
        current_app.logger.error(f"Failed to generate summary from LLM: {e}")
        return None


def llm_sparql_from_question(question, rdf_domain):
    config = get_config_values()
    client = config['openai_client']
    
    try:
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": """
                    You will be given a RDF domain wrapped in <D></D> (THE ONLY SOURCE OF TRUTH YOU USE).
                    Given a user question in <Q></Q>, you must GENERATE A SPARQL QUERY for the question using the provided RDF domain.
                    The user ID will be provided as a literal value in double quotes (e.g., "user-id-string").
                    Make sure to use correct SPARQL syntax and ensure that all values are properly enclosed in double quotes.
                    RETURN ONLY THE SPARQL QUERY AS A RESPONSE IN RAW TEXT, NOTHING ELSE.
                    Example: SELECT ?paymentMethod WHERE {
                    ?client <http://example.org/carshare#clientID> "user-id-string" .
                    ?client <http://example.org/carshare#paymentMethod> ?paymentMethod .
                    }
                    """
                },
                {
                    "role": "user",
                    "content": f"<D>{rdf_domain}</D><Q>{question}</Q>"
                }
            ])

        query = completion.choices[0].message.content
        current_app.logger.debug(f"llm_sparql_from_question: {completion.choices[0].message}")
        
        # Filter ```sparql``` or ```SPARQL``` code block from the response
        if "```sparql" in query:
            query = query.split("```sparql")[1].split("```")[0].strip()
        elif "```SPARQL" in query:
            query = query.split("```SPARQL")[1].split("```")[0].strip()
        
        return query
    except Exception as e:
        current_app.logger.error(f"Failed to generate SPARQL query from LLM: {e}")
        return None
