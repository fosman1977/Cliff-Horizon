"""
Example Usage of Weather Derivative Simulator

This script demonstrates how to use the simulator to price a contract.
"""

import numpy as np
from simulator import WeatherDerivativeSimulator, create_example_contract, create_example_historical_data
from config import ContractSpecification, PricingParameters, SimulationParameters


def example_basic_pricing():
    """Example 1: Basic pricing workflow"""
    print("=" * 70)
    print("EXAMPLE 1: Basic Pricing Workflow")
    print("=" * 70)
    
    # Create simulator
    sim = WeatherDerivativeSimulator()
    
    # Define contract
    contract = create_example_contract()
    
    # Historical data (October rainy days for Bankot, 2015-2024)
    historical_data = create_example_historical_data()
    
    # Price the contract (one-line call)
    results = sim.price_contract(
        contract=contract,
        historical_data=historical_data
    )
    
    # Print summary
    print(sim.generate_summary())
    
    return results


def example_custom_parameters():
    """Example 2: Custom pricing parameters"""
    print("\n" + "=" * 70)
    print("EXAMPLE 2: Custom Pricing Parameters")
    print("=" * 70)
    
    sim = WeatherDerivativeSimulator()
    
    # Custom contract
    contract = ContractSpecification(
        location_lat=19.076,  # Mumbai
        location_lon=72.877,
        location_name="Mumbai, India",
        observation_month=7,  # July (monsoon)
        observation_year=2025,
        rainfall_threshold_mm=30.0,  # Higher threshold
        strike_rainy_days=15,
        payout_rate_per_day=10000,
        maximum_payout_days=10
    )
    
    # Simulated historical data for Mumbai July
    historical_data = np.array([18, 20, 17, 22, 19, 21, 18, 20, 17, 19])
    
    # Custom pricing parameters (more conservative)
    pricing_params = PricingParameters(
        volatility_loading=0.20,  # 20% instead of default 15%
        basis_risk_loading=0.07,  # 7% instead of default 5%
        profit_margin=0.25,  # 25% instead of default 20%
        cost_of_capital=0.15  # 15% instead of default 12%
    )
    
    # Custom simulation parameters
    sim_params = SimulationParameters(
        n_simulations=20000,  # More simulations for precision
        method='hybrid',
        bootstrap_weight=0.6  # 60% bootstrap, 40% parametric
    )
    
    # Price with custom parameters
    results = sim.price_contract(
        contract=contract,
        historical_data=historical_data,
        pricing_params=pricing_params,
        sim_params=sim_params
    )
    
    print(sim.generate_summary())
    
    # Show impact of conservative parameters
    print(f"\nImpact of Conservative Parameters:")
    print(f"  Higher loadings increased premium by: {pricing_params.volatility_loading * 100:.0f}% + {pricing_params.basis_risk_loading * 100:.0f}%")
    print(f"  Expected Loss Ratio: {results['pricing']['expected_loss_ratio']:.1f}%")
    print(f"  (Lower loss ratio = more conservative pricing)")
    
    return results


def example_step_by_step():
    """Example 3: Step-by-step workflow with detailed inspection"""
    print("\n" + "=" * 70)
    print("EXAMPLE 3: Step-by-Step Workflow")
    print("=" * 70)
    
    sim = WeatherDerivativeSimulator()
    
    # Step 1: Set contract
    print("\n[Step 1] Setting contract...")
    contract = create_example_contract()
    sim.set_contract(contract)
    print(f"âœ“ Contract set for {contract.location_name}")
    
    # Step 2: Load historical data
    print("\n[Step 2] Loading historical data...")
    historical_data = create_example_historical_data()
    hist_stats = sim.set_historical_data(historical_data)
    print(f"âœ“ Loaded {hist_stats['n_years']} years of data")
    print(f"  Mean: {hist_stats['mean_rainy_days']:.1f} days")
    print(f"  Range: {hist_stats['min_rainy_days']}-{hist_stats['max_rainy_days']} days")
    print(f"  Historical trigger frequency: {hist_stats.get('historical_trigger_frequency', 0) * 100:.1f}%")
    
    # Step 3: Fit distribution
    print("\n[Step 3] Fitting probability distribution...")
    distribution = sim.fit_distribution(method='auto')
    print(f"âœ“ Selected: {distribution.distribution_type}")
    print(f"  Parameters: {distribution.parameters}")
    print(f"  Expected rainy days: {distribution.mean():.2f}")
    print(f"  Goodness of fit p-value: {distribution.gof_pvalue:.3f}")
    if distribution.is_good_fit:
        print(f"  âœ“ Distribution fits well (p > 0.05)")
    else:
        print(f"  âš  Distribution may not fit well (p < 0.05)")
    
    # Step 4: Calculate premium
    print("\n[Step 4] Calculating premium...")
    pricing = sim.calculate_premium()
    print(f"âœ“ Premium calculated: ${pricing.gross_premium:,.2f}")
    print(f"\n  Breakdown:")
    for component, value in pricing.pricing_breakdown.items():
        print(f"    {component:.<30} ${value:>10,.2f}")
    
    # Step 5: Run simulation
    print("\n[Step 5] Running Monte Carlo simulation...")
    simulation = sim.run_simulation()
    print(f"âœ“ Completed {simulation.n_simulations:,} simulations")
    print(f"\n  Risk Metrics:")
    print(f"    Mean payout:.................. ${simulation.mean_payout:>10,.2f}")
    print(f"    Std Dev:...................... ${simulation.std_payout:>10,.2f}")
    print(f"    VaR (95%):.................... ${simulation.var_95:>10,.2f}")
    print(f"    VaR (99%):.................... ${simulation.var_99:>10,.2f}")
    print(f"    CVaR (99%):................... ${simulation.cvar_99:>10,.2f}")
    print(f"    Trigger frequency:............ {simulation.trigger_frequency * 100:>9.1f}%")
    
    # Step 6: Analyze profitability
    print("\n[Step 6] Profitability Analysis...")
    expected_profit = pricing.gross_premium - pricing.expected_payout
    roe = (expected_profit / pricing.capital_required * 100) if pricing.capital_required > 0 else 0
    print(f"  Premium:...................... ${pricing.gross_premium:>10,.2f}")
    print(f"  Expected payout:.............. ${pricing.expected_payout:>10,.2f}")
    print(f"  Expected profit:.............. ${expected_profit:>10,.2f}")
    print(f"  Required capital:............. ${pricing.capital_required:>10,.2f}")
    print(f"  Expected ROE:................. {roe:>9.1f}%")
    
    print("\n" + "=" * 70)
    print("âœ“ Complete pricing analysis finished!")
    print("=" * 70)


def example_comparison():
    """Example 4: Compare different strike levels"""
    print("\n" + "=" * 70)
    print("EXAMPLE 4: Comparing Different Strike Levels")
    print("=" * 70)
    
    historical_data = create_example_historical_data()
    
    # Base contract
    base_contract = create_example_contract()
    
    # Try different strikes
    strikes = [9, 10, 11, 12, 13]
    
    print(f"\n{'Strike':>6} | {'Premium':>10} | {'Loss Ratio':>11} | {'Exp. ROE':>9} | {'Trigger %':>10}")
    print("-" * 70)
    
    for strike in strikes:
        contract = ContractSpecification(
            location_lat=base_contract.location_lat,
            location_lon=base_contract.location_lon,
            location_name=base_contract.location_name,
            observation_month=base_contract.observation_month,
            observation_year=base_contract.observation_year,
            rainfall_threshold_mm=base_contract.rainfall_threshold_mm,
            strike_rainy_days=strike,
            payout_rate_per_day=base_contract.payout_rate_per_day,
            maximum_payout_days=base_contract.maximum_payout_days
        )
        
        sim = WeatherDerivativeSimulator()
        results = sim.price_contract(contract, historical_data)
        
        print(f"{strike:>6} | ${results['pricing']['gross_premium']:>9,.0f} | "
              f"{results['pricing']['expected_loss_ratio']:>10.1f}% | "
              f"{results['profitability']['expected_roe']:>8.1f}% | "
              f"{results['simulation']['trigger_frequency'] * 100:>9.1f}%")
    
    print("\nInsights:")
    print("  â€¢ Lower strike = Higher trigger probability = Higher premium")
    print("  â€¢ Higher strike = Lower trigger probability = Lower premium")
    print("  â€¢ Optimal strike balances client need with pricing attractiveness")


if __name__ == "__main__":
    print("\n")
    print("â•”" + "=" * 68 + "â•—")
    print("â•‘" + " " * 15 + "WEATHER DERIVATIVE SIMULATOR" + " " * 25 + "â•‘")
    print("â•‘" + " " * 20 + "Example Demonstrations" + " " * 26 + "â•‘")
    print("â•š" + "=" * 68 + "â•")
    
    # Run examples
    try:
        # Example 1: Basic usage
        example_basic_pricing()
        
        # Example 2: Custom parameters
        example_custom_parameters()
        
        # Example 3: Step-by-step
        example_step_by_step()
        
        # Example 4: Comparison
        example_comparison()
        
        print("\n" + "=" * 70)
        print("All examples completed successfully!")
        print("=" * 70)
        
    except Exception as e:
        print(f"\nâŒ Error: {e}")
        import traceback
        traceback.print_exc()
