# Weather Derivative Simulator

A comprehensive Python-based pricing engine for weather derivatives with focus on rainfall-based contracts for the construction industry.

## 🎯 Overview

This simulator provides professional-grade pricing and risk analysis for weather derivative contracts. It's designed specifically for Cliff Horizon's weather intelligence services, enabling accurate pricing of parametric weather insurance products.

## ✨ Features

- **Distribution Fitting**: Automatic selection between Poisson, Negative Binomial, and Empirical distributions
- **Monte Carlo Simulation**: 10,000+ scenario analysis with bootstrap, parametric, and hybrid methods
- **Risk Metrics**: VaR, CVaR, trigger frequency, and capital requirements
- **Pricing Engine**: Complete premium calculation with risk loadings and capital charges
- **Professional Output**: Formatted summaries and detailed breakdowns

## 🚀 Quick Start

### Installation

```bash
# Install dependencies
pip install numpy scipy pandas

# Run examples
python example.py
```

### Basic Usage

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

# Display results
print(sim.generate_summary())
```

## 📁 Project Structure

```
├── config.py              # Configuration and data structures
├── distributions.py       # Distribution fitting module
├── simulator.py          # Main pricing engine
├── example.py            # Usage examples
├── BUILD_SUMMARY.md      # Development summary
└── Documentation/
    ├── Weather_Derivative_Product_Design.md
    ├── Weather_Derivatives_Implementation_Plan.docx
    └── Weather_Derivatives_Regulatory_Analysis_Summary.md
```

## 📊 What It Calculates

- **Pure Premium**: Expected payout based on historical data
- **Risk Loadings**: Volatility and basis risk adjustments
- **Capital Requirements**: VaR-based capital allocation
- **Gross Premium**: Final quoted price including profit margin
- **Risk Metrics**: VaR (90%, 95%, 99%), CVaR, trigger frequency
- **Profitability**: Expected ROE and break-even analysis

## 🧪 Testing

```bash
python example.py
```

Expected runtime: ~10-15 seconds for all examples

## 📈 Roadmap

### ✅ Phase 1 - Core Simulator (Complete)
- Distribution fitting
- Pricing engine
- Monte Carlo simulation
- Risk metrics

### 🚧 Phase 2 - Data & Reporting (Planned)
- GPM IMERG data integration
- Excel/PDF report generation
- PostgreSQL database
- Automated data pipeline

### 🔮 Phase 3 - Portfolio Management (Planned)
- Multi-contract aggregation
- Correlation modelling
- Revenue projections
- Scenario analysis

### 🌐 Phase 4 - Web Interface (Future)
- REST API
- Web dashboard
- Interactive visualisations

## 📝 Documentation

- **[Product Design](Weather_Derivative_Product_Design.md)** - Contract structure and ISDA documentation
- **[Implementation Plan](Weather_Derivatives_Implementation_Plan.docx)** - 4-stage development roadmap
- **[Regulatory Analysis](Weather_Derivatives_Regulatory_Analysis_Summary.md)** - Compliance framework
- **[Build Summary](BUILD_SUMMARY.md)** - Development details and technical specs

## 🔧 Configuration

Edit `config.py` to customise:

```python
# Risk parameters
DEFAULT_VOLATILITY_LOADING = 0.15
DEFAULT_BASIS_RISK_LOADING = 0.05
CAPITAL_VAR_MULTIPLIER = 1.5

# Simulation parameters
DEFAULT_N_SIMULATIONS = 10000
DEFAULT_VAR_CONFIDENCE_LEVELS = [0.90, 0.95, 0.99]
```

## 📦 Dependencies

- Python 3.8+
- NumPy
- SciPy
- Pandas

## 🏢 About

Developed for **Cliff Horizon Pte. Ltd.** - A Singapore-based weather intelligence services company providing weather analytics to construction companies globally.

## 📄 License

Proprietary - © 2025 Cliff Horizon Pte. Ltd.

## 🤝 Contributing

This is a private project for Cliff Horizon's internal use.

## 📧 Contact

For questions or support, contact Cliff Horizon Pte. Ltd.

---

**Version**: 1.0.0  
**Status**: Production Ready (Phase 1)  
**Last Updated**: November 2025
