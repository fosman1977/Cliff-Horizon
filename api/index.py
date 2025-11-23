"""
Weather Derivative Simulator API
Serverless API endpoint for Vercel deployment
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import sys
import os

# Add parent directory to path to import simulator modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    """API root endpoint"""
    return jsonify({
        'name': 'Weather Derivative Simulator API',
        'version': '1.0.0',
        'status': 'active',
        'endpoints': {
            '/': 'API information',
            '/api/health': 'Health check',
            '/api/price': 'Price a weather derivative contract (POST)',
            '/api/info': 'Get simulator information'
        }
    })

@app.route('/api/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'Weather Derivative Simulator API is running'
    })

@app.route('/api/info')
def info():
    """Get simulator information"""
    return jsonify({
        'name': 'Weather Derivative Simulator',
        'description': 'Professional-grade pricing engine for rainfall-based derivatives',
        'company': 'Cliff Horizon Pte. Ltd.',
        'version': '1.0.0',
        'phase': 'Phase 1 - Production Ready',
        'features': [
            'Distribution Fitting (Poisson, Negative Binomial, Empirical)',
            'Monte Carlo Simulation (10,000+ scenarios)',
            'Risk Metrics (VaR, CVaR, Trigger Frequency)',
            'Complete Pricing Engine',
            'Capital Requirement Calculation'
        ],
        'technology': ['Python', 'NumPy', 'SciPy', 'Pandas']
    })

@app.route('/api/price', methods=['POST'])
def price_contract():
    """
    Price a weather derivative contract

    Expected POST body:
    {
        "contract": {
            "location_name": "Bankot, India",
            "observation_month": 10,
            "observation_year": 2025,
            "rainfall_threshold_mm": 25.0,
            "strike_rainy_days": 11,
            "payout_rate_per_day": 14000,
            "maximum_payout_days": 7
        },
        "historical_data": [7, 10, 9, 12, 8, 14, 9, 11, 8, 10]
    }
    """
    try:
        # Import simulator modules
        from simulator import WeatherDerivativeSimulator
        from config import ContractSpecification
        import numpy as np

        data = request.get_json()

        if not data:
            return jsonify({'error': 'No data provided'}), 400

        # Extract contract and historical data
        contract_data = data.get('contract', {})
        historical_data = data.get('historical_data', [])

        if not contract_data or not historical_data:
            return jsonify({'error': 'Missing contract or historical_data'}), 400

        # Create contract specification
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

        # Convert historical data to numpy array
        historical_array = np.array(historical_data)

        # Create simulator and price contract
        simulator = WeatherDerivativeSimulator()
        results = simulator.price_contract(contract, historical_array)

        # Return results
        return jsonify({
            'success': True,
            'results': results,
            'summary': simulator.generate_summary()
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# For local development
if __name__ == '__main__':
    app.run(debug=True, port=5000)
