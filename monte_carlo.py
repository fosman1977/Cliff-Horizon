"""
Monte Carlo Simulation for Weather Derivatives

This module implements Monte Carlo simulation for risk analysis.
"""

import numpy as np
from dataclasses import dataclass
from typing import Dict
from config import ContractSpecification, SimulationParameters
from distributions import DistributionFit


@dataclass
class SimulationResults:
    """Results from Monte Carlo simulation"""
    n_simulations: int
    simulated_rainy_days: np.ndarray
    simulated_payouts: np.ndarray
    mean_payout: float
    std_payout: float
    min_payout: float
    max_payout: float
    trigger_frequency: float
    var_90: float
    var_95: float
    var_99: float
    cvar_90: float
    cvar_95: float
    cvar_99: float
    percentiles: Dict[int, float]

    def to_dict(self) -> Dict:
        """Convert to dictionary (excluding large arrays)"""
        return {
            'n_simulations': self.n_simulations,
            'mean_payout': self.mean_payout,
            'std_payout': self.std_payout,
            'min_payout': self.min_payout,
            'max_payout': self.max_payout,
            'trigger_frequency': self.trigger_frequency,
            'var_90': self.var_90,
            'var_95': self.var_95,
            'var_99': self.var_99,
            'cvar_90': self.cvar_90,
            'cvar_95': self.cvar_95,
            'cvar_99': self.cvar_99,
            'percentiles': self.percentiles
        }


class MonteCarloSimulator:
    """
    Monte Carlo simulator for weather derivatives

    Implements three simulation methods:
    1. Bootstrap: Resampling from historical data
    2. Parametric: Sampling from fitted distribution
    3. Hybrid: Mixture of bootstrap and parametric
    """

    def __init__(
        self,
        contract: ContractSpecification,
        distribution: DistributionFit,
        historical_data: np.ndarray,
        params: SimulationParameters
    ):
        """
        Initialize Monte Carlo simulator

        Parameters:
        -----------
        contract : ContractSpecification
            Contract terms
        distribution : DistributionFit
            Fitted probability distribution
        historical_data : np.ndarray
            Historical rainy day counts
        params : SimulationParameters
            Simulation parameters
        """
        self.contract = contract
        self.distribution = distribution
        self.historical_data = historical_data
        self.params = params

        # Set random seed for reproducibility
        np.random.seed(params.random_seed)

    def simulate_rainy_days(self) -> np.ndarray:
        """
        Simulate rainy day counts using selected method

        Returns:
        --------
        simulated_days : np.ndarray
            Array of simulated rainy day counts
        """
        n = self.params.n_simulations

        if self.params.method == 'bootstrap':
            # Bootstrap: resample from historical data
            simulated = np.random.choice(
                self.historical_data,
                size=n,
                replace=True
            )

        elif self.params.method == 'parametric':
            # Parametric: sample from fitted distribution
            simulated = self.distribution.rvs(size=n)

        elif self.params.method == 'hybrid':
            # Hybrid: mix of bootstrap and parametric
            n_bootstrap = int(n * self.params.bootstrap_weight)
            n_parametric = n - n_bootstrap

            bootstrap_sample = np.random.choice(
                self.historical_data,
                size=n_bootstrap,
                replace=True
            )
            parametric_sample = self.distribution.rvs(size=n_parametric)

            simulated = np.concatenate([bootstrap_sample, parametric_sample])
            np.random.shuffle(simulated)

        else:
            raise ValueError(f"Unknown simulation method: {self.params.method}")

        return simulated.astype(int)

    def calculate_payout(self, rainy_days: np.ndarray) -> np.ndarray:
        """
        Calculate payouts for simulated rainy day counts

        Parameters:
        -----------
        rainy_days : np.ndarray
            Array of rainy day counts

        Returns:
        --------
        payouts : np.ndarray
            Array of corresponding payouts
        """
        strike = self.contract.strike_rainy_days
        max_days = self.contract.maximum_payout_days
        rate = self.contract.payout_rate_per_day

        # Calculate excess days
        excess_days = np.maximum(rainy_days - strike, 0)

        # Cap at maximum payout days
        capped_excess = np.minimum(excess_days, max_days)

        # Calculate payouts
        payouts = capped_excess * rate

        return payouts

    def calculate_var_cvar(
        self,
        payouts: np.ndarray,
        confidence_levels: list = [0.90, 0.95, 0.99]
    ) -> Dict:
        """
        Calculate Value at Risk (VaR) and Conditional VaR (CVaR)

        Parameters:
        -----------
        payouts : np.ndarray
            Array of simulated payouts
        confidence_levels : list
            List of confidence levels

        Returns:
        --------
        risk_metrics : dict
            Dictionary of VaR and CVaR values
        """
        risk_metrics = {}

        for level in confidence_levels:
            # VaR: percentile of loss distribution
            var = np.percentile(payouts, level * 100)
            risk_metrics[f'var_{int(level * 100)}'] = var

            # CVaR: expected loss given loss exceeds VaR
            excess_losses = payouts[payouts >= var]
            cvar = np.mean(excess_losses) if len(excess_losses) > 0 else var
            risk_metrics[f'cvar_{int(level * 100)}'] = cvar

        return risk_metrics

    def run(self) -> SimulationResults:
        """
        Run Monte Carlo simulation

        Returns:
        --------
        results : SimulationResults
            Complete simulation results
        """
        # Simulate rainy days
        simulated_rainy_days = self.simulate_rainy_days()

        # Calculate payouts
        simulated_payouts = self.calculate_payout(simulated_rainy_days)

        # Calculate statistics
        mean_payout = float(np.mean(simulated_payouts))
        std_payout = float(np.std(simulated_payouts))
        min_payout = float(np.min(simulated_payouts))
        max_payout = float(np.max(simulated_payouts))

        # Trigger frequency (proportion of scenarios with payout > 0)
        trigger_frequency = float(np.mean(simulated_payouts > 0))

        # Calculate VaR and CVaR
        risk_metrics = self.calculate_var_cvar(simulated_payouts)

        # Calculate percentiles
        percentile_levels = [10, 25, 50, 75, 90, 95, 99]
        percentiles = {
            p: float(np.percentile(simulated_payouts, p))
            for p in percentile_levels
        }

        return SimulationResults(
            n_simulations=self.params.n_simulations,
            simulated_rainy_days=simulated_rainy_days,
            simulated_payouts=simulated_payouts,
            mean_payout=mean_payout,
            std_payout=std_payout,
            min_payout=min_payout,
            max_payout=max_payout,
            trigger_frequency=trigger_frequency,
            var_90=risk_metrics['var_90'],
            var_95=risk_metrics['var_95'],
            var_99=risk_metrics['var_99'],
            cvar_90=risk_metrics['cvar_90'],
            cvar_95=risk_metrics['cvar_95'],
            cvar_99=risk_metrics['cvar_99'],
            percentiles=percentiles
        )
