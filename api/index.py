"""
Weather Derivative Simulator API
Vercel Serverless Function
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = Flask(__name__)
CORS(app)

@app.route('/')
@app.route('/api')
def home():
    """API root endpoint"""
    return jsonify({
        'name': 'Weather Derivative Simulator API',
        'version': '1.0.0',
        'status': 'active',
        'endpoints': {
            '/api': 'API information',
            '/api/health': 'Health check',
            '/api/info': 'Simulator details',
            '/api/price': 'Price contract (POST)'
        }
    })

@app.route('/api/health')
def health():
    """Health check"""
    return jsonify({
        'status': 'healthy',
        'message': 'Weather Derivative Simulator API is running'
    })

@app.route('/api/info')
def info():
    """Simulator information"""
    return jsonify({
        'name': 'Weather Derivative Simulator',
        'description': 'Professional-grade pricing engine for rainfall-based derivatives',
        'company': 'Cliff Horizon Pte. Ltd.',
        'version': '1.0.0',
        'features': [
            'Distribution Fitting (Poisson, Negative Binomial, Empirical)',
            'Monte Carlo Simulation (10,000+ scenarios)',
            'Risk Metrics (VaR, CVaR, Trigger Frequency)',
            'Complete Pricing Engine',
            'Capital Requirement Calculation'
        ]
    })

@app.route('/api/price', methods=['POST'])
def price_contract():
    """Price a weather derivative contract"""
    try:
        from simulator import WeatherDerivativeSimulator
        from config import ContractSpecification
        import numpy as np

        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        contract_data = data.get('contract', {})
        historical_data = data.get('historical_data', [])

        if not contract_data or not historical_data:
            return jsonify({'error': 'Missing contract or historical_data'}), 400

        # Create contract
        contract = ContractSpecification(
            location_lat=contract_data.get('location_lat', 0.0),
            location_lon=contract_data.get('location_lon', 0.0),
            location_name=contract_data.get('location_name', 'Unknown'),
            observation_month=contract_data.get('observation_month'),
            observation_year=contract_data.get('observation_year', 2025),
            rainfall_threshold_mm=contract_data.get('rainfall_threshold_mm'),
            strike_rainy_days=contract_data.get('strike_rainy_days'),
            payout_rate_per_day=contract_data.get('payout_rate_per_day'),
            maximum_payout_days=contract_data.get('maximum_payout_days')
        )

        # Price contract
        simulator = WeatherDerivativeSimulator()
        results = simulator.price_contract(contract, np.array(historical_data))

        return jsonify({
            'success': True,
            'results': results
        })

    except Exception as e:
        import traceback
        return jsonify({
            'success': False,
            'error': str(e),
            'trace': traceback.format_exc()
        }), 500

# Export for Vercel
handler = app
