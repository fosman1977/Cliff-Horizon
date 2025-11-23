# Deployment Guide

## Current Deployment: Static Website

This project is currently deployed as a **static website** showcasing the Weather Derivative Simulator project.

### What's Deployed

- **Landing Page** (`index.html`): Professional website with project information, features, and installation instructions
- **GitHub Repository Link**: Direct access to the source code
- **Documentation Links**: README and technical documentation

### What's NOT Deployed (Yet)

- **Python API**: The REST API is not currently deployed due to Vercel serverless function complexity
- **Real-time Pricing**: API endpoints for contract pricing

## Why Static Only?

The Python codebase is a **library/CLI tool** designed to run locally with full NumPy/SciPy dependencies. Deploying the API as a serverless function on Vercel presents challenges:

1. **Large Dependencies**: NumPy and SciPy add significant build time and size
2. **Cold Start Performance**: Scientific computing libraries have slow cold starts
3. **Complexity**: WSGI adapter configuration for Flask on serverless

## How to Use the Simulator

### Local Installation

```bash
# Clone the repository
git clone https://github.com/fosman1977/Cliff-Horizon.git
cd Cliff-Horizon

# Install dependencies
pip install -r requirements.txt

# Run examples
python example.py
```

### Python Usage

```python
from simulator import WeatherDerivativeSimulator
from config import ContractSpecification
import numpy as np

# Create simulator
sim = WeatherDerivativeSimulator()

# Define contract
contract = ContractSpecification(
    location_lat=17.895,
    location_lon=73.052,
    location_name="Bankot, India",
    observation_month=10,
    observation_year=2025,
    rainfall_threshold_mm=25.0,
    strike_rainy_days=11,
    payout_rate_per_day=14000,
    maximum_payout_days=7
)

# Historical data (10 years)
historical_data = np.array([7, 10, 9, 12, 8, 14, 9, 11, 8, 10])

# Price the contract
results = sim.price_contract(contract, historical_data)
print(sim.generate_summary())
```

## Future: Adding API Deployment

If you want to deploy the API in the future, consider these options:

### Option 1: Different Platform
- **Heroku**: Better for Python apps with heavy dependencies
- **AWS Lambda with Layers**: Pre-build NumPy/SciPy as layers
- **Google Cloud Run**: Container-based deployment
- **Railway**: Simple Python deployment

### Option 2: Lightweight API
Create a simplified API version:
- Pre-compute common scenarios
- Cache results
- Use lighter-weight libraries
- Implement request queuing

### Option 3: Separate API Service
- Deploy API separately from static site
- Use CORS to connect them
- API on platform suited for Python (Heroku, Railway)
- Static site on Vercel

## Current File Structure

```
Cliff-Horizon/
├── index.html              # Deployed landing page
├── vercel.json            # Simple static config
├── requirements.txt        # For local installation
├── .gitignore
│
├── config.py              # Core configuration
├── simulator.py           # Main simulator
├── distributions.py       # Distribution fitting
├── pricing.py             # Pricing engine
├── monte_carlo.py         # Monte Carlo simulation
├── example.py             # Usage examples
│
└── Documentation/
    ├── README.md
    ├── BUILD_SUMMARY.md
    └── ...
```

## Deployment Commands

### Current Deployment (Static)
Vercel automatically deploys from your Git repository. Just push changes:

```bash
git add .
git commit -m "Your changes"
git push
```

### Manual Deploy
```bash
vercel --prod
```

## Summary

✅ **Landing page deployed successfully**
✅ **Full Python simulator code available for download**
✅ **Easy local installation and usage**
❌ **API not deployed** (by design - use locally instead)

For most use cases, running the simulator locally is the recommended approach. It provides:
- Full control over parameters
- No API rate limits
- Faster execution
- Access to all features
- Better debugging

---

**Questions?** See the main README.md or contact Cliff Horizon Pte. Ltd.
