from dotenv import load_dotenv
import os


# Load the .env file
load_dotenv()

from flask import Flask, render_template, send_from_directory
from controllers import pricing_blueprint, template_blueprint
from dotenv import load_dotenv
from flasgger import Swagger, swag_from, LazyString, LazyJSONEncoder


app = Flask(__name__)
swagger = Swagger(app)
app.register_blueprint(pricing_blueprint, url_prefix='/api')
app.register_blueprint(template_blueprint)

@app.route('/docs')
def swagger_ui():
    return render_template('swagger_ui.html')

@app.route('/spec')
def get_spec():
    return send_from_directory(app.root_path, 'swagger.yaml')

if __name__ == '__main__':
    app.run(debug=True)
