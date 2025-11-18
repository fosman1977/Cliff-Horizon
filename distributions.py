"""
Distribution Fitting Module

Fits probability distributions to historical rainy day counts.
Supports Poisson, Negative Binomial, and Empirical distributions.
"""

import numpy as np
from scipy import stats
from scipy.optimize import minimize
from typing import Dict, Tuple, Optional, List
from dataclasses import dataclass
import warnings

from src.config import (
    CANDIDATE_DISTRIBUTIONS,
    VARIANCE_MEAN_RATIO_THRESHOLD,
    MIN_SAMPLE_SIZE_PARAMETRIC,
    GOF_SIGNIFICANCE_LEVEL
)


@dataclass
class DistributionFit:
    """Results of distribution fitting"""
    distribution_type: str
    parameters: Dict[str, float]
    aic: float
    bic: float
    log_likelihood: float
    gof_statistic: float
    gof_pvalue: float
    is_good_fit: bool
    
    def pmf(self, k: int) -> float:
        """Probability mass function"""
        if self.distribution_type == 'poisson':
            return stats.poisson.pmf(k, mu=self.parameters['lambda'])
        elif self.distribution_type == 'negative_binomial':
            return stats.nbinom.pmf(k, n=self.parameters['n'], p=self.parameters['p'])
        elif self.distribution_type == 'empirical':
            # Return empirical probability
            return self.parameters.get(f'p_{k}', 0.0)
        else:
            raise ValueError(f"Unknown distribution: {self.distribution_type}")
    
    def cdf(self, k: int) -> float:
        """Cumulative distribution function"""
        if self.distribution_type == 'poisson':
            return stats.poisson.cdf(k, mu=self.parameters['lambda'])
        elif self.distribution_type == 'negative_binomial':
            return stats.nbinom.cdf(k, n=self.parameters['n'], p=self.parameters['p'])
        elif self.distribution_type == 'empirical':
            # Cumulative sum of empirical probabilities up to k
            cum_prob = 0.0
            for i in range(k + 1):
                cum_prob += self.parameters.get(f'p_{i}', 0.0)
            return cum_prob
        else:
            raise ValueError(f"Unknown distribution: {self.distribution_type}")
    
    def ppf(self, q: float) -> int:
        """Percent point function (inverse CDF)"""
        if self.distribution_type == 'poisson':
            return int(stats.poisson.ppf(q, mu=self.parameters['lambda']))
        elif self.distribution_type == 'negative_binomial':
            return int(stats.nbinom.ppf(q, n=self.parameters['n'], p=self.parameters['p']))
        elif self.distribution_type == 'empirical':
            # Find the smallest k where CDF(k) >= q
            for k in range(100):  # Reasonable upper limit
                if self.cdf(k) >= q:
                    return k
            return 99  # Fallback
        else:
            raise ValueError(f"Unknown distribution: {self.distribution_type}")
    
    def rvs(self, size: int = 1, random_state: Optional[int] = None) -> np.ndarray:
        """Generate random variates"""
        if self.distribution_type == 'poisson':
            return np.random.RandomState(random_state).poisson(
                lam=self.parameters['lambda'], size=size
            )
        elif self.distribution_type == 'negative_binomial':
            return np.random.RandomState(random_state).negative_binomial(
                n=self.parameters['n'], p=self.parameters['p'], size=size
            )
        elif self.distribution_type == 'empirical':
            # Sample from empirical distribution
            values = []
            probabilities = []
            for key, value in self.parameters.items():
                if key.startswith('p_'):
                    k = int(key.split('_')[1])
                    values.append(k)
                    probabilities.append(value)
            
            if not values:
                raise ValueError("Empirical distribution has no probabilities")
            
            # Normalize probabilities
            probabilities = np.array(probabilities)
            probabilities = probabilities / probabilities.sum()
            
            return np.random.RandomState(random_state).choice(
                values, size=size, p=probabilities
            )
        else:
            raise ValueError(f"Unknown distribution: {self.distribution_type}")
    
    def mean(self) -> float:
        """Expected value"""
        if self.distribution_type == 'poisson':
            return self.parameters['lambda']
        elif self.distribution_type == 'negative_binomial':
            n = self.parameters['n']
            p = self.parameters['p']
            return n * (1 - p) / p
        elif self.distribution_type == 'empirical':
            mean_val = 0.0
            for key, prob in self.parameters.items():
                if key.startswith('p_'):
                    k = int(key.split('_')[1])
                    mean_val += k * prob
            return mean_val
        else:
            raise ValueError(f"Unknown distribution: {self.distribution_type}")
    
    def variance(self) -> float:
        """Variance"""
        if self.distribution_type == 'poisson':
            return self.parameters['lambda']
        elif self.distribution_type == 'negative_binomial':
            n = self.parameters['n']
            p = self.parameters['p']
            return n * (1 - p) / (p ** 2)
        elif self.distribution_type == 'empirical':
            mean_val = self.mean()
            variance_val = 0.0
            for key, prob in self.parameters.items():
                if key.startswith('p_'):
                    k = int(key.split('_')[1])
                    variance_val += ((k - mean_val) ** 2) * prob
            return variance_val
        else:
            raise ValueError(f"Unknown distribution: {self.distribution_type}")


class DistributionFitter:
    """Fits probability distributions to rainy day count data"""
    
    def __init__(self, data: np.ndarray):
        """
        Initialize fitter with historical rainy day counts
        
        Parameters:
        -----------
        data : np.ndarray
            Array of historical rainy day counts
        """
        self.data = np.array(data, dtype=int)
        self.n_samples = len(self.data)
        self.mean = np.mean(self.data)
        self.variance = np.var(self.data, ddof=1)  # Sample variance
        self.std = np.std(self.data, ddof=1)
        
        # Validate data
        if self.n_samples < 5:
            raise ValueError("Need at least 5 data points for distribution fitting")
        if np.any(self.data < 0):
            raise ValueError("Data contains negative values")
    
    def fit_poisson(self) -> DistributionFit:
        """Fit Poisson distribution"""
        # MLE for Poisson: Î» = sample mean
        lambda_mle = self.mean
        
        # Log-likelihood
        log_likelihood = np.sum(stats.poisson.logpmf(self.data, mu=lambda_mle))
        
        # AIC and BIC (1 parameter)
        k_params = 1
        aic = 2 * k_params - 2 * log_likelihood
        bic = k_params * np.log(self.n_samples) - 2 * log_likelihood
        
        # Goodness-of-fit test (Chi-squared)
        gof_stat, gof_pval = self._chi_squared_test(
            lambda k: stats.poisson.pmf(k, mu=lambda_mle)
        )
        
        return DistributionFit(
            distribution_type='poisson',
            parameters={'lambda': lambda_mle},
            aic=aic,
            bic=bic,
            log_likelihood=log_likelihood,
            gof_statistic=gof_stat,
            gof_pvalue=gof_pval,
            is_good_fit=(gof_pval > GOF_SIGNIFICANCE_LEVEL)
        )
    
    def fit_negative_binomial(self) -> DistributionFit:
        """Fit Negative Binomial distribution"""
        # Method of moments for initial guess
        if self.variance <= self.mean:
            # Variance not greater than mean, fall back to Poisson-like parameters
            p_init = 0.5
            n_init = self.mean
        else:
            p_init = self.mean / self.variance
            n_init = (self.mean ** 2) / (self.variance - self.mean)
        
        # MLE optimization
        def neg_log_likelihood(params):
            n, p = params
            if n <= 0 or p <= 0 or p >= 1:
                return np.inf
            try:
                ll = np.sum(stats.nbinom.logpmf(self.data, n=n, p=p))
                return -ll
            except:
                return np.inf
        
        # Optimize
        result = minimize(
            neg_log_likelihood,
            x0=[n_init, p_init],
            bounds=[(0.1, 1000), (0.01, 0.99)],
            method='L-BFGS-B'
        )
        
        if not result.success:
            warnings.warn("Negative Binomial optimization did not converge")
        
        n_mle, p_mle = result.x
        log_likelihood = -result.fun
        
        # AIC and BIC (2 parameters)
        k_params = 2
        aic = 2 * k_params - 2 * log_likelihood
        bic = k_params * np.log(self.n_samples) - 2 * log_likelihood
        
        # Goodness-of-fit test
        gof_stat, gof_pval = self._chi_squared_test(
            lambda k: stats.nbinom.pmf(k, n=n_mle, p=p_mle)
        )
        
        return DistributionFit(
            distribution_type='negative_binomial',
            parameters={'n': n_mle, 'p': p_mle},
            aic=aic,
            bic=bic,
            log_likelihood=log_likelihood,
            gof_statistic=gof_stat,
            gof_pvalue=gof_pval,
            is_good_fit=(gof_pval > GOF_SIGNIFICANCE_LEVEL)
        )
    
    def fit_empirical(self) -> DistributionFit:
        """Fit empirical distribution (non-parametric)"""
        # Count frequencies
        unique_values, counts = np.unique(self.data, return_counts=True)
        probabilities = counts / self.n_samples
        
        # Store as parameters
        parameters = {}
        for val, prob in zip(unique_values, probabilities):
            parameters[f'p_{val}'] = float(prob)
        
        # Log-likelihood
        log_likelihood = np.sum(np.log(counts / self.n_samples) * counts)
        
        # AIC and BIC (n_unique parameters)
        k_params = len(unique_values)
        aic = 2 * k_params - 2 * log_likelihood
        bic = k_params * np.log(self.n_samples) - 2 * log_likelihood
        
        # Goodness-of-fit (perfect fit by definition)
        gof_stat = 0.0
        gof_pval = 1.0
        
        return DistributionFit(
            distribution_type='empirical',
            parameters=parameters,
            aic=aic,
            bic=bic,
            log_likelihood=log_likelihood,
            gof_statistic=gof_stat,
            gof_pvalue=gof_pval,
            is_good_fit=True
        )
    
    def _chi_squared_test(self, pmf_func) -> Tuple[float, float]:
        """
        Perform Chi-squared goodness-of-fit test
        
        Returns:
            (chi2_statistic, p_value)
        """
        # Bin the data
        min_val = int(self.data.min())
        max_val = int(self.data.max())
        
        # Observed frequencies
        observed = np.zeros(max_val - min_val + 1)
        for val in self.data:
            observed[val - min_val] += 1
        
        # Expected frequencies
        expected = np.zeros(max_val - min_val + 1)
        for i, k in enumerate(range(min_val, max_val + 1)):
            expected[i] = pmf_func(k) * self.n_samples
        
        # Combine bins with expected < 5
        observed_combined = []
        expected_combined = []
        
        current_obs = 0
        current_exp = 0
        
        for obs, exp in zip(observed, expected):
            current_obs += obs
            current_exp += exp
            
            if current_exp >= 5:
                observed_combined.append(current_obs)
                expected_combined.append(current_exp)
                current_obs = 0
                current_exp = 0
        
        # Add remaining
        if current_obs > 0:
            if len(observed_combined) > 0:
                observed_combined[-1] += current_obs
                expected_combined[-1] += current_exp
            else:
                observed_combined.append(current_obs)
                expected_combined.append(current_exp)
        
        observed_combined = np.array(observed_combined)
        expected_combined = np.array(expected_combined)
        
        # Chi-squared statistic
        chi2_stat = np.sum((observed_combined - expected_combined) ** 2 / expected_combined)
        
        # Degrees of freedom (bins - 1 - number of estimated parameters)
        # For Poisson: 1 parameter, for NegBin: 2 parameters
        if 'lambda' in str(pmf_func):
            df = len(observed_combined) - 1 - 1
        else:
            df = len(observed_combined) - 1 - 2
        
        df = max(df, 1)  # Ensure at least 1 degree of freedom
        
        # P-value
        p_value = 1 - stats.chi2.cdf(chi2_stat, df)
        
        return chi2_stat, p_value
    
    def select_best_distribution(self) -> DistributionFit:
        """
        Select the best distribution using AIC/BIC and heuristics
        
        Returns:
            Best fitting DistributionFit object
        """
        fits = []
        
        # Always fit empirical
        fits.append(self.fit_empirical())
        
        # Fit parametric distributions if sample size is sufficient
        if self.n_samples >= MIN_SAMPLE_SIZE_PARAMETRIC:
            try:
                fits.append(self.fit_poisson())
            except Exception as e:
                warnings.warn(f"Poisson fitting failed: {e}")
            
            try:
                fits.append(self.fit_negative_binomial())
            except Exception as e:
                warnings.warn(f"Negative Binomial fitting failed: {e}")
        
        # Selection heuristics
        variance_mean_ratio = self.variance / self.mean if self.mean > 0 else float('inf')
        
        # If variance â‰ˆ mean, prefer Poisson
        # If variance > mean, prefer Negative Binomial
        # If small sample, prefer Empirical
        
        if self.n_samples < MIN_SAMPLE_SIZE_PARAMETRIC:
            # Use empirical for small samples
            best_fit = [f for f in fits if f.distribution_type == 'empirical'][0]
        else:
            # Use AIC for model selection among parametric
            parametric_fits = [f for f in fits if f.distribution_type != 'empirical']
            
            if parametric_fits:
                # Select best parametric fit by AIC
                best_parametric = min(parametric_fits, key=lambda f: f.aic)
                
                # Check if it's a good fit
                if best_parametric.is_good_fit:
                    best_fit = best_parametric
                else:
                    # Fall back to empirical if parametric doesn't fit well
                    best_fit = [f for f in fits if f.distribution_type == 'empirical'][0]
            else:
                best_fit = [f for f in fits if f.distribution_type == 'empirical'][0]
        
        return best_fit


def fit_distribution(data: np.ndarray, method: str = 'auto') -> DistributionFit:
    """
    Fit a probability distribution to rainy day count data
    
    Parameters:
    -----------
    data : np.ndarray
        Historical rainy day counts
    method : str
        'auto', 'poisson', 'negative_binomial', or 'empirical'
    
    Returns:
    --------
    DistributionFit object
    """
    fitter = DistributionFitter(data)
    
    if method == 'auto':
        return fitter.select_best_distribution()
    elif method == 'poisson':
        return fitter.fit_poisson()
    elif method == 'negative_binomial':
        return fitter.fit_negative_binomial()
    elif method == 'empirical':
        return fitter.fit_empirical()
    else:
        raise ValueError(f"Unknown method: {method}")
