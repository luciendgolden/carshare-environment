import os

class Config:
    GRAPHDB_REPOSITORY = os.getenv('GRAPHDB_REPOSITORY', 'CMKEws23_Integration')
    GRAPHDB_URL = os.getenv('GRAPHDB_URL', 'http://localhost:7200')
    OPENAI_ENDPOINT = os.getenv('OPENAI_ENDPOINT', 'https://api.openai.com')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', 'your-local-openai-key')
    LLAMA_ENDPOINT = os.getenv('LLAMA_ENDPOINT', 'http://llama_cpp:8080')
    LLAMA_API_KEY = os.getenv('LLAMA_API_KEY', 'your-local-llama-key')