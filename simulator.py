"""
Weather Derivative Simulator - Main Class

This is the main interface for pricing and analyzing weather derivative contracts.
"""

import numpy as np
from typing import Dict, Optional, Tuple
from datetime import datetime
import warnings

from config import (
    ContractSpecification,
    PricingParameters,
    SimulationParameters,
    validate_contract
)
from distributions import fit_distribution, DistributionFit
from pricing import PricingEngine, PricingResults, calculate_break_even_trigger_rate
from monte_carlo import MonteCarloSimulator, SimulationResults


class WeatherDerivativeSimulator:
    """
    Main simulator class for weather derivative pricing and analysis
    
    This class orchestrates the entire pricing workflow:
    1. Accepts contract specification
    2. Analyzes historical data
    3. Fits probability distributions
    4. Calculates premiums
    5. Runs Monte Carlo simulations
    6. Generates risk metrics
    """
    
    def __init__(self):
        """Initialize simulator"""
        self.version = "1.0.0"
        self.pricing_date = datetime.now()
        
        # Results storage
        self.contract: Optional[ContractSpecification] = None
        self.historical_data: Optional[np.ndarray] = None
        self.distribution: Optional[DistributionFit] = None
        self.pricing_results: Optional[PricingResults] = None
        self.simulation_results: Optional[SimulationResults] = None
    
    def set_contract(self, contract: ContractSpecification) -> bool:
        """
        Set contract specification
        
        Parameters:
        -----------
        contract : ContractSpecification
            Contract terms
        
        Returns:
        --------
        success : bool
            True if contract is valid
        """
        # Validate contract
        is_valid, error_msg = validate_contract(contract)
        if not is_valid:
            raise ValueError(f"Invalid contract: {error_msg}")
        
        self.contract = contract
        return True
    
    def set_historical_data(self, rainy_day_counts: np.ndarray) -> Dict[str, float]:
        """
        Set historical rainy day count data
        
        Parameters:
        -----------
        rainy_day_counts : np.ndarray
            Array of historical rainy day counts for the observation month
        
        Returns:
        --------
        statistics : dict
            Summary statistics of historical data
        """
        self.historical_data = np.array(rainy_day_counts, dtype=int)
        
        # Validate
        if len(self.historical_data) < 5:
            warnings.warn("Less than 5 years of historical data - results may be unreliable")
        
        # Calculate statistics
        statistics = {
            'n_years': len(self.historical_data),
            'mean_rainy_days': float(np.mean(self.historical_data)),
            'std_rainy_days': float(np.std(self.historical_data, ddof=1)),
            'min_rainy_days': int(np.min(self.historical_data)),
            'max_rainy_days': int(np.max(self.historical_data)),
            'median_rainy_days': float(np.median(self.historical_data))
        }
        
        # Calculate historical trigger frequency
        if self.contract is not None:
            historical_triggers = np.sum(
                self.historical_data > self.contract.strike_rainy_days
            )
            statistics['historical_trigger_frequency'] = float(
                historical_triggers / len(self.historical_data)
            )
        
        return statistics
    
    def fit_distribution(self, method: str = 'auto') -> DistributionFit:
        """
        Fit probability distribution to historical data
        
        Parameters:
        -----------
        method : str
            'auto', 'poisson', 'negative_binomial', or 'empirical'
        
        Returns:
        --------
        distribution : DistributionFit
            Fitted distribution
        """
        if self.historical_data is None:
            raise ValueError("Historical data not set. Call set_historical_data() first.")
        
        self.distribution = fit_distribution(self.historical_data, method=method)
        return self.distribution
    
    def calculate_premium(
        self,
        pricing_params: Optional[PricingParameters] = None
    ) -> PricingResults:
        """
        Calculate premium for the contract
        
        Parameters:
        -----------
        pricing_params : PricingParameters, optional
            Pricing parameters (uses defaults if not provided)
        
        Returns:
        --------
        pricing_results : PricingResults
            Detailed pricing breakdown
        """
        if self.contract is None:
            raise ValueError("Contract not set. Call set_contract() first.")
        if self.distribution is None:
            raise ValueError("Distribution not fitted. Call fit_distribution() first.")
        
        # Use default parameters if not provided
        if pricing_params is None:
            pricing_params = PricingParameters()
        
        # Create pricing engine
        engine = PricingEngine(self.contract, self.distribution, pricing_params)
        
        # Calculate premium (without VaR initially)
        self.pricing_results = engine.calculate_premium(var_99=None)
        
        return self.pricing_results
    
    def run_simulation(
        self,
        sim_params: Optional[SimulationParameters] = None
    ) -> SimulationResults:
        """
        Run Monte Carlo simulation
        
        Parameters:
        -----------
        sim_params : SimulationParameters, optional
            Simulation parameters (uses defaults if not provided)
        
        Returns:
        --------
        simulation_results : SimulationResults
            Simulation results including VaR, CVaR, etc.
        """
        if self.contract is None:
            raise ValueError("Contract not set. Call set_contract() first.")
        if self.distribution is None:
            raise ValueError("Distribution not fitted. Call fit_distribution() first.")
        
        # Use default parameters if not provided
        if sim_params is None:
            sim_params = SimulationParameters()
        
        # Create simulator
        simulator = MonteCarloSimulator(
            self.contract,
            self.distribution,
            self.historical_data,
            sim_params
        )
        
        # Run simulation
        self.simulation_results = simulator.run()
        
        # Recalculate premium with actual VaR from simulation
        if self.pricing_results is not None:
            pricing_params = PricingParameters()  # Use defaults
            engine = PricingEngine(self.contract, self.distribution, pricing_params)
            self.pricing_results = engine.calculate_premium(
                var_99=self.simulation_results.var_99
            )
        
        return self.simulation_results
    
    def price_contract(
        self,
        contract: ContractSpecification,
        historical_data: np.ndarray,
        pricing_params: Optional[PricingParameters] = None,
        sim_params: Optional[SimulationParameters] = None,
        distribution_method: str = 'auto'
    ) -> Dict:
        """
        Complete pricing workflow in one call
        
        Parameters:
        -----------
        contract : ContractSpecification
            Contract terms
        historical_data : np.ndarray
            Historical rainy day counts
        pricing_params : PricingParameters, optional
            Pricing parameters
        sim_params : SimulationParameters, optional
            Simulation parameters
        distribution_method : str
            Distribution fitting method
        
        Returns:
        --------
        results : dict
            Complete pricing and risk analysis results
        """
        # Execute workflow
        self.set_contract(contract)
        hist_stats = self.set_historical_data(historical_data)
        distribution = self.fit_distribution(method=distribution_method)
        pricing = self.calculate_premium(pricing_params)
        simulation = self.run_simulation(sim_params)
        
        # Calculate break-even
        break_even_rate = calculate_break_even_trigger_rate(
            contract, distribution, pricing.gross_premium
        )
        
        # Compile results
        results = {
            'contract': {
                'location': contract.location_name,
                'latitude': contract.location_lat,
                'longitude': contract.longitude,
                'observation_month': contract.observation_month,
                'observation_year': contract.observation_year,
                'rainfall_threshold_mm': contract.rainfall_threshold_mm,
                'strike_rainy_days': contract.strike_rainy_days,
                'payout_rate_per_day': contract.payout_rate_per_day,
                'maximum_payout_days': contract.maximum_payout_days,
                'maximum_payout': contract.maximum_payout
            },
            'historical_analysis': hist_stats,
            'distribution': {
                'type': distribution.distribution_type,
                'parameters': distribution.parameters,
                'mean': distribution.mean(),
                'variance': distribution.variance(),
                'is_good_fit': distribution.is_good_fit,
                'gof_pvalue': distribution.gof_pvalue
            },
            'pricing': pricing.to_dict(),
            'simulation': simulation.to_dict(),
            'profitability': {
                'expected_profit': pricing.gross_premium - pricing.expected_payout,
                'expected_roe': (
                    (pricing.gross_premium - pricing.expected_payout) / 
                    pricing.capital_required * 100
                ) if pricing.capital_required > 0 else 0,
                'break_even_trigger_rate': break_even_rate
            },
            'metadata': {
                'pricing_date': self.pricing_date.isoformat(),
                'simulator_version': self.version,
                'distribution_method': distribution_method
            }
        }
        
        return results
    
    def generate_summary(self) -> str:
        """
        Generate a text summary of pricing results
        
        Returns:
        --------
        summary : str
            Formatted text summary
        """
        if self.contract is None or self.pricing_results is None:
            return "No pricing results available. Run price_contract() first."
        
        summary = f"""
{'=' * 65}
WEATHER DERIVATIVE PRICING SUMMARY
{'=' * 65}

Contract Details:
  Location:              {self.contract.location_name}
  Coordinates:           ({self.contract.location_lat:.3f}Â°N, {self.contract.location_lon:.3f}Â°E)
  Observation Period:    {self.contract.observation_month}/{self.contract.observation_year}
  Rainfall Threshold:    {self.contract.rainfall_threshold_mm} mm/day
  Strike Level:          {self.contract.strike_rainy_days} rainy days
  Payout Rate:           ${self.contract.payout_rate_per_day:,.0f} per excess day
  Maximum Payout Days:   {self.contract.maximum_payout_days} days
  Maximum Payout:        ${self.contract.maximum_payout:,.0f}

"""
        
        if self.historical_data is not None:
            summary += f"""Historical Analysis ({len(self.historical_data)} years):
  Mean Rainy Days:       {np.mean(self.historical_data):.1f} days
  Std Dev:               {np.std(self.historical_data, ddof=1):.1f} days
  Historical Range:      {np.min(self.historical_data)} - {np.max(self.historical_data)} days
  Trigger Frequency:     {np.sum(self.historical_data > self.contract.strike_rainy_days) / len(self.historical_data) * 100:.1f}%
"""
        
        if self.distribution is not None:
            summary += f"""  Fitted Distribution:   {self.distribution.distribution_type}
  Distribution Mean:     {self.distribution.mean():.1f} days

"""
        
        p = self.pricing_results
        summary += f"""Pricing Results:
  Pure Premium:          ${p.pure_premium:,.2f}
  Volatility Loading:    ${p.volatility_charge:,.2f}
  Basis Risk Loading:    ${p.basis_risk_charge:,.2f}
  Technical Premium:     ${p.technical_premium:,.2f}
  Capital Charge:        ${p.capital_charge:,.2f}
  Operational Cost:      ${p.operational_cost:,.2f}
  Profit Margin:         ${p.profit_amount:,.2f}
  ---------------------
  QUOTED PREMIUM:        ${p.gross_premium:,.2f}
  
  Premium as % Notional: {p.premium_as_pct_notional:.1f}%
  Expected Loss Ratio:   {p.expected_loss_ratio:.1f}%

"""
        
        if self.simulation_results is not None:
            s = self.simulation_results
            summary += f"""Risk Metrics (from {s.n_simulations:,} simulations):
  Expected Payout:       ${s.mean_payout:,.2f}
  Standard Deviation:    ${s.std_payout:,.2f}
  Trigger Frequency:     {s.trigger_frequency * 100:.1f}%
  Value at Risk (95%):   ${s.var_95:,.0f}
  Value at Risk (99%):   ${s.var_99:,.0f}
  CVaR (99%):            ${s.cvar_99:,.0f}
  Required Capital:      ${p.capital_required:,.0f}

"""
        
        profit = p.gross_premium - p.expected_payout
        roe = (profit / p.capital_required * 100) if p.capital_required > 0 else 0
        
        summary += f"""Profitability:
  Expected Profit:       ${profit:,.2f}
  Expected ROE:          {roe:.1f}%

{'=' * 65}
"""
        
        return summary


def create_example_contract() -> ContractSpecification:
    """Create an example contract for testing"""
    return ContractSpecification(
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


def create_example_historical_data() -> np.ndarray:
    """Create example historical data for testing"""
    # Simulated October rainy days for Bankot (2015-2024)
    return np.array([7, 10, 9, 12, 8, 14, 9, 11, 8, 10])
