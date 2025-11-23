"""
Pricing Engine for Weather Derivatives

This module implements the pricing logic for weather derivative contracts.
"""

import numpy as np
from dataclasses import dataclass
from typing import Dict, Optional
from config import (
    ContractSpecification,
    PricingParameters,
    CAPITAL_VAR_MULTIPLIER,
    DEFAULT_SETTLEMENT_DAYS
)
from distributions import DistributionFit


@dataclass
class PricingResults:
    """Results from pricing calculation"""
    expected_payout: float
    variance_payout: float
    std_payout: float
    pure_premium: float
    volatility_charge: float
    basis_risk_charge: float
    technical_premium: float
    capital_required: float
    capital_charge: float
    operational_cost: float
    profit_amount: float
    gross_premium: float
    premium_as_pct_notional: float
    expected_loss_ratio: float

    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            'expected_payout': self.expected_payout,
            'variance_payout': self.variance_payout,
            'std_payout': self.std_payout,
            'pure_premium': self.pure_premium,
            'volatility_charge': self.volatility_charge,
            'basis_risk_charge': self.basis_risk_charge,
            'technical_premium': self.technical_premium,
            'capital_required': self.capital_required,
            'capital_charge': self.capital_charge,
            'operational_cost': self.operational_cost,
            'profit_amount': self.profit_amount,
            'gross_premium': self.gross_premium,
            'premium_as_pct_notional': self.premium_as_pct_notional,
            'expected_loss_ratio': self.expected_loss_ratio
        }


class PricingEngine:
    """
    Pricing engine for weather derivative contracts

    Calculates premiums using actuarial principles:
    1. Expected payout (pure premium)
    2. Risk loadings (volatility, basis risk)
    3. Capital requirements (VaR-based)
    4. Profit margin
    """

    def __init__(
        self,
        contract: ContractSpecification,
        distribution: DistributionFit,
        params: PricingParameters
    ):
        """
        Initialize pricing engine

        Parameters:
        -----------
        contract : ContractSpecification
            Contract terms
        distribution : DistributionFit
            Fitted probability distribution
        params : PricingParameters
            Pricing parameters
        """
        self.contract = contract
        self.distribution = distribution
        self.params = params

    def calculate_expected_payout(self) -> tuple[float, float, float]:
        """
        Calculate expected payout and variance

        Returns:
        --------
        expected_payout : float
            Expected payout amount
        variance : float
            Variance of payout
        std_dev : float
            Standard deviation of payout
        """
        strike = self.contract.strike_rainy_days
        max_days = self.contract.maximum_payout_days
        payout_rate = self.contract.payout_rate_per_day

        # Calculate expected payout by summing over all possible outcomes
        expected_payout = 0.0
        expected_payout_sq = 0.0

        # For each possible rainy day count
        for days in range(strike + 1, strike + max_days + 1):
            excess_days = days - strike
            capped_excess = min(excess_days, max_days)
            payout = capped_excess * payout_rate
            prob = self.distribution.pmf(days)

            expected_payout += payout * prob
            expected_payout_sq += (payout ** 2) * prob

        # For days exceeding strike + max_days (full payout)
        prob_extreme = 1 - self.distribution.cdf(strike + max_days)
        max_payout = max_days * payout_rate
        expected_payout += max_payout * prob_extreme
        expected_payout_sq += (max_payout ** 2) * prob_extreme

        # Calculate variance
        variance = expected_payout_sq - (expected_payout ** 2)
        variance = max(0, variance)  # Ensure non-negative
        std_dev = np.sqrt(variance)

        return expected_payout, variance, std_dev

    def calculate_premium(self, var_99: Optional[float] = None) -> PricingResults:
        """
        Calculate gross premium

        Parameters:
        -----------
        var_99 : float, optional
            99% Value at Risk from simulation (if available)

        Returns:
        --------
        results : PricingResults
            Complete pricing breakdown
        """
        # Calculate expected payout
        expected_payout, variance, std_dev = self.calculate_expected_payout()

        # Pure premium (expected payout)
        pure_premium = expected_payout

        # Volatility charge (based on standard deviation)
        volatility_charge = self.params.volatility_loading * std_dev

        # Basis risk charge (systematic risk)
        basis_risk_charge = self.params.basis_risk_loading * pure_premium

        # Technical premium
        technical_premium = pure_premium + volatility_charge + basis_risk_charge

        # Capital requirement (based on VaR)
        if var_99 is not None:
            capital_required = CAPITAL_VAR_MULTIPLIER * var_99
        else:
            # Estimate using 2.33 * std_dev (99% for normal distribution)
            capital_required = CAPITAL_VAR_MULTIPLIER * 2.33 * std_dev

        # Capital charge (cost of holding capital)
        # Prorated for contract period (assuming ~1 month)
        time_fraction = (DEFAULT_SETTLEMENT_DAYS + 30) / 365
        capital_charge = self.params.cost_of_capital * capital_required * time_fraction

        # Operational cost
        operational_cost = self.params.operational_cost

        # Subtotal before profit
        subtotal = technical_premium + capital_charge + operational_cost

        # Profit margin
        profit_amount = self.params.profit_margin * subtotal

        # Gross premium
        gross_premium = subtotal + profit_amount

        # Additional metrics
        max_payout = self.contract.maximum_payout
        premium_as_pct_notional = (gross_premium / max_payout * 100) if max_payout > 0 else 0
        expected_loss_ratio = (expected_payout / gross_premium * 100) if gross_premium > 0 else 0

        return PricingResults(
            expected_payout=expected_payout,
            variance_payout=variance,
            std_payout=std_dev,
            pure_premium=pure_premium,
            volatility_charge=volatility_charge,
            basis_risk_charge=basis_risk_charge,
            technical_premium=technical_premium,
            capital_required=capital_required,
            capital_charge=capital_charge,
            operational_cost=operational_cost,
            profit_amount=profit_amount,
            gross_premium=gross_premium,
            premium_as_pct_notional=premium_as_pct_notional,
            expected_loss_ratio=expected_loss_ratio
        )


def calculate_break_even_trigger_rate(
    contract: ContractSpecification,
    distribution: DistributionFit,
    premium: float
) -> float:
    """
    Calculate the trigger frequency at which contract breaks even

    Parameters:
    -----------
    contract : ContractSpecification
        Contract terms
    premium : float
        Quoted premium
    distribution : DistributionFit
        Fitted distribution

    Returns:
    --------
    trigger_rate : float
        Break-even trigger frequency (probability)
    """
    # Simplified: trigger rate where expected payout equals premium
    trigger_prob = 1 - distribution.cdf(contract.strike_rainy_days)
    return trigger_prob
