from flask import Blueprint, render_template, jsonify
from utils.data_loader import DataLoader


template_blueprint = Blueprint('template', __name__)

data_loader = DataLoader('data/Travel.csv')
data = data_loader.pre_process_travel_data(data_loader.data)

@template_blueprint.route('/')
def index():
    return jsonify({
        'message': 'g9_optimizeprice API',
        'success': True,
        'version': '1.0.0',
        'endpoints': [
            '/gui',
            '/demo',
            '/pricing/company',
            '/pricing/customer',
            '/pricing/cost'
        ],
        'documentation': '/docs',
    })

@template_blueprint.route('/gui')
def gui():
    return render_template('index.html')

@template_blueprint.route('/demo')
def ga_demo():
    return render_template('demo/ga_demo.html')

@template_blueprint.route('/pricing/company')
def pricing_for_company():
    return render_template('pricing/company_pricing.html')

@template_blueprint.route('/pricing/customer')
def pricing_for_customer():
    return render_template('pricing/customer_pricing.html')

@template_blueprint.route('/pricing/cost')
def pricing_cost():
    return render_template('pricing/cost_calculation.html')