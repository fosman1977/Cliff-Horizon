"""
Configuration and Constants for Weather Derivative Simulator

This module contains all configuration parameters, constants, and default values
used throughout the simulator.
"""

from dataclasses import dataclass
from typing import Optional
import os


# ============================================================================
# DATA SOURCE CONFIGURATION
# ============================================================================

DATA_SOURCE_GPM_IMERG_LATE = "GPM_IMERG_Late_v07"
DATA_SOURCE_GPM_IMERG_FINAL = "GPM_IMERG_Final_v07"

# NASA Earthdata Configuration
NASA_EARTHDATA_URL = "https://gpm1.gesdisc.eosdis.nasa.gov/data/GPM_L3/GPM_3IMERGHHL.07/"

# Default data source priority
DATA_SOURCE_PRIORITY = [
    DATA_SOURCE_GPM_IMERG_LATE,
    DATA_SOURCE_GPM_IMERG_FINAL
]

# ============================================================================
# HISTORICAL DATA CONFIGURATION
# ============================================================================

DEFAULT_HISTORICAL_START_YEAR = 2015
DEFAULT_HISTORICAL_END_YEAR = 2024
MINIMUM_HISTORICAL_YEARS = 5  # Minimum years needed for reliable analysis

# ============================================================================
# GEOGRAPHIC CONFIGURATION
# ============================================================================

DEFAULT_GRID_RADIUS_KM = 10.0  # Default radius for spatial averaging
MIN_LATITUDE = -60.0  # GPM IMERG coverage limit
MAX_LATITUDE = 60.0
MIN_LONGITUDE = -180.0
MAX_LONGITUDE = 180.0

# ============================================================================
# PRODUCT STRUCTURE DEFAULTS
# ============================================================================

DEFAULT_RAINFALL_THRESHOLD_MM = 25.0  # Default threshold for "rainy day"
DEFAULT_SETTLEMENT_DAYS = 30  # Days after period end for settlement

# Risk limits
MAX_NOTIONAL_PER_CONTRACT = 500000  # USD - internal risk limit
MIN_PREMIUM_AMOUNT = 1000  # USD - minimum viable premium

# ============================================================================
# PRICING MODEL DEFAULTS
# ============================================================================

# Risk loadings (as decimals, not percentages)
DEFAULT_VOLATILITY_LOADING = 0.15  # 15%
DEFAULT_BASIS_RISK_LOADING = 0.05  # 5%
DEFAULT_PROFIT_MARGIN = 0.20  # 20%
DEFAULT_OPERATIONAL_COST = 1000.0  # USD per contract
DEFAULT_COST_OF_CAPITAL = 0.12  # 12% per annum

# Capital requirement multipliers
CAPITAL_VAR_MULTIPLIER = 1.5  # 1.5 Ã— VaR_99
CAPITAL_EXPECTED_LOSS_MULTIPLIER = 2.0  # 2.0 Ã— Expected Loss
CAPITAL_NOTIONAL_FLOOR = 0.10  # 10% of maximum possible loss

# ============================================================================
# MONTE CARLO SIMULATION DEFAULTS
# ============================================================================

DEFAULT_N_SIMULATIONS = 10000
DEFAULT_RANDOM_SEED = 42
DEFAULT_SIMULATION_METHOD = "hybrid"  # "bootstrap", "parametric", or "hybrid"
DEFAULT_BOOTSTRAP_WEIGHT = 0.5  # 50/50 split for hybrid method

# Confidence levels for risk metrics
CONFIDENCE_LEVELS = {
    'var_90': 0.90,
    'var_95': 0.95,
    'var_99': 0.99,
}

# ============================================================================
# DISTRIBUTION FITTING CONFIGURATION
# ============================================================================

CANDIDATE_DISTRIBUTIONS = [
    'poisson',
    'negative_binomial',
    'empirical'
]

# Thresholds for distribution selection
VARIANCE_MEAN_RATIO_THRESHOLD = 1.2  # If > 1.2, prefer Negative Binomial over Poisson
MIN_SAMPLE_SIZE_PARAMETRIC = 20  # Minimum samples for parametric fitting

# Goodness-of-fit test
GOF_SIGNIFICANCE_LEVEL = 0.05  # 5% significance level for Ï‡Â² or KS test

# ============================================================================
# VALIDATION THRESHOLDS
# ============================================================================

# Premium validation
MAX_PREMIUM_TO_NOTIONAL_RATIO = 0.5  # Premium should be < 50% of notional
MIN_EXPECTED_LOSS_RATIO = 0.40  # 40%
MAX_EXPECTED_LOSS_RATIO = 0.80  # 80%

# Risk metric validation
MIN_REQUIRED_CAPITAL_TO_EXPECTED_LOSS = 2.0  # Capital â‰¥ 2Ã— expected loss

# ============================================================================
# OUTPUT CONFIGURATION
# ============================================================================

OUTPUT_DIR = "output"
REPORTS_DIR = os.path.join(OUTPUT_DIR, "reports")
EXCEL_DIR = os.path.join(OUTPUT_DIR, "excel")
TEMP_DIR = os.path.join(OUTPUT_DIR, "temp")

# Report formatting
DECIMAL_PLACES_CURRENCY = 2
DECIMAL_PLACES_PERCENTAGE = 1
DECIMAL_PLACES_PROBABILITY = 3

# ============================================================================
# DATABASE CONFIGURATION
# ============================================================================

# PostgreSQL with PostGIS (to be configured by user)
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "weather_derivatives")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# ============================================================================
# REVENUE PROJECTION CONFIGURATION
# ============================================================================

# Growth scenarios (number of contracts per year)
GROWTH_SCENARIOS = {
    'conservative': [5, 15, 30, 50, 80, 100, 120],
    'base_case': [5, 30, 80, 150, 200, 250, 300],
    'bull_case': [5, 40, 120, 200, 300, 400, 500]
}

# Average premium per contract by year
AVG_PREMIUM_BY_YEAR = {
    1: 20000,
    2: 22000,
    3: 25000,
    4: 28000,
    5: 30000
}

# Target loss ratios by year (improving with diversification)
TARGET_LOSS_RATIOS = {
    1: 0.70,
    2: 0.65,
    3: 0.60,
    4: 0.58,
    5: 0.55
}

# Operating costs by year (USD)
OPERATING_COSTS = {
    'personnel': [200000, 300000, 400000, 500000, 600000, 700000, 800000],
    'technology': [50000, 50000, 75000, 100000, 150000, 200000, 250000],
    'legal_compliance': [75000, 25000, 30000, 40000, 50000, 60000, 70000],
    'marketing_bd': [30000, 40000, 50000, 75000, 100000, 125000, 150000],
    'office_admin': [45000, 35000, 45000, 60000, 80000, 100000, 120000]
}

# Singapore corporate tax rate
SINGAPORE_TAX_RATE = 0.17  # 17%

# ============================================================================
# LOGGING CONFIGURATION
# ============================================================================

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_FILE = "weather_derivative_simulator.log"


# ============================================================================
# DATA CLASSES FOR TYPE SAFETY
# ============================================================================

@dataclass
class ContractSpecification:
    """User-input contract terms"""
    location_lat: float
    location_lon: float
    location_name: str
    observation_month: int  # 1-12
    observation_year: int
    rainfall_threshold_mm: float
    strike_rainy_days: int
    payout_rate_per_day: float
    maximum_payout_days: int
    grid_radius_km: float = DEFAULT_GRID_RADIUS_KM
    settlement_days: int = DEFAULT_SETTLEMENT_DAYS
    
    def __post_init__(self):
        """Validate contract parameters"""
        if not MIN_LATITUDE <= self.location_lat <= MAX_LATITUDE:
            raise ValueError(f"Latitude must be between {MIN_LATITUDE} and {MAX_LATITUDE}")
        if not MIN_LONGITUDE <= self.location_lon <= MAX_LONGITUDE:
            raise ValueError(f"Longitude must be between {MIN_LONGITUDE} and {MAX_LONGITUDE}")
        if not 1 <= self.observation_month <= 12:
            raise ValueError("Month must be between 1 and 12")
        if self.observation_year < 2025:
            raise ValueError("Observation year must be 2025 or later")
        if self.strike_rainy_days < 0:
            raise ValueError("Strike days cannot be negative")
        if self.maximum_payout_days < 0:
            raise ValueError("Maximum payout days cannot be negative")
        if self.payout_rate_per_day <= 0:
            raise ValueError("Payout rate must be positive")
        
        # Check notional limit
        max_payout = self.maximum_payout_days * self.payout_rate_per_day
        if max_payout > MAX_NOTIONAL_PER_CONTRACT:
            raise ValueError(f"Maximum payout (${max_payout:,.0f}) exceeds limit (${MAX_NOTIONAL_PER_CONTRACT:,.0f})")
    
    @property
    def maximum_payout(self) -> float:
        """Calculate maximum possible payout"""
        return self.maximum_payout_days * self.payout_rate_per_day


@dataclass
class PricingParameters:
    """Pricing model parameters"""
    volatility_loading: float = DEFAULT_VOLATILITY_LOADING
    basis_risk_loading: float = DEFAULT_BASIS_RISK_LOADING
    profit_margin: float = DEFAULT_PROFIT_MARGIN
    operational_cost: float = DEFAULT_OPERATIONAL_COST
    cost_of_capital: float = DEFAULT_COST_OF_CAPITAL
    
    def __post_init__(self):
        """Validate pricing parameters"""
        if not 0 <= self.volatility_loading <= 1:
            raise ValueError("Volatility loading must be between 0 and 1")
        if not 0 <= self.basis_risk_loading <= 1:
            raise ValueError("Basis risk loading must be between 0 and 1")
        if not 0 <= self.profit_margin <= 1:
            raise ValueError("Profit margin must be between 0 and 1")
        if self.operational_cost < 0:
            raise ValueError("Operational cost cannot be negative")
        if not 0 <= self.cost_of_capital <= 1:
            raise ValueError("Cost of capital must be between 0 and 1")


@dataclass
class SimulationParameters:
    """Monte Carlo simulation parameters"""
    n_simulations: int = DEFAULT_N_SIMULATIONS
    random_seed: int = DEFAULT_RANDOM_SEED
    method: str = DEFAULT_SIMULATION_METHOD
    bootstrap_weight: float = DEFAULT_BOOTSTRAP_WEIGHT
    
    def __post_init__(self):
        """Validate simulation parameters"""
        if self.n_simulations < 1000:
            raise ValueError("Number of simulations must be at least 1000")
        if self.n_simulations > 100000:
            raise ValueError("Number of simulations cannot exceed 100,000")
        if self.method not in ['bootstrap', 'parametric', 'hybrid']:
            raise ValueError("Method must be 'bootstrap', 'parametric', or 'hybrid'")
        if not 0 <= self.bootstrap_weight <= 1:
            raise ValueError("Bootstrap weight must be between 0 and 1")


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def get_days_in_month(month: int, year: int) -> int:
    """Get number of days in a given month"""
    import calendar
    return calendar.monthrange(year, month)[1]


def validate_contract(contract: ContractSpecification) -> tuple[bool, Optional[str]]:
    """
    Validate contract specification
    
    Returns:
        (is_valid, error_message)
    """
    # Check if strike is feasible for month
    days_in_month = get_days_in_month(contract.observation_month, contract.observation_year)
    
    if contract.strike_rainy_days > days_in_month:
        return False, f"Strike ({contract.strike_rainy_days}) exceeds days in month ({days_in_month})"
    
    if contract.strike_rainy_days + contract.maximum_payout_days > days_in_month:
        return False, f"Strike + max payout days ({contract.strike_rainy_days + contract.maximum_payout_days}) exceeds days in month ({days_in_month})"
    
    return True, None


# ============================================================================
# VERSION INFO
# ============================================================================

__version__ = "1.0.0"
__author__ = "Cliff Horizon Pte. Ltd."
__date__ = "2025-11-18"
