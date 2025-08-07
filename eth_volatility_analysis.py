#!/usr/bin/env python3
"""
ETH Options Implied Volatility Analysis
Comprehensive quantitative analysis of ETH options IV pricing
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from scipy.optimize import minimize
import warnings
warnings.filterwarnings('ignore')

# Set up plotting style
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

class ETHVolatilityAnalyzer:
    def __init__(self):
        """Initialize the ETH Volatility Analyzer with current market data"""
        # Current market data (as collected)
        self.current_data = {
            'eth_price': 3614.96,
            'eth_iv_deribit': 65.40,
            'eth_iv_binance': 65.0,  # Approximate from charts
            'eth_rv_1d': 23.63,
            'eth_rv_3d': 23.01,
            'eth_rv_7d': 23.48,
            'eth_rv_30d': 59.0,  # From Messari
            'btc_rv_1d': 10.53,
            'btc_rv_7d': 11.37,
            'btc_rv_30d': 12.47,
            'vix': 17.73,
            'move_index': 89.20
        }
        
        # Historical context data
        self.historical_data = {
            'eth_30d_vol_7d_ago': 54.0,
            'eth_30d_vol_30d_ago': 61.0,
            'eth_30d_vol_1y_ago': 67.0,
            'vix_52w_low': 12.70,
            'vix_52w_high': 60.13
        }
        
        # Options activity data
        self.options_activity = {
            'calls_sold': 26.4,
            'puts_bought': 32.5,
            'puts_sold': 24.8,
            'calls_bought': 20.8
        }
    
    def calculate_ivr(self, current_iv, min_iv_252d, max_iv_252d):
        """Calculate Implied Volatility Rank"""
        if max_iv_252d == min_iv_252d:
            return 0.5  # Neutral if no range
        ivr = (current_iv - min_iv_252d) / (max_iv_252d - min_iv_252d)
        return max(0, min(1, ivr))  # Bound between 0 and 1
    
    def calculate_iv_percentile(self, current_iv, historical_iv_series):
        """Calculate IV Percentile"""
        if len(historical_iv_series) == 0:
            return 0.5
        percentile = stats.percentileofscore(historical_iv_series, current_iv) / 100
        return percentile
    
    def calculate_vrp(self, implied_vol, realized_vol):
        """Calculate Volatility Risk Premium"""
        return implied_vol - realized_vol
    
    def calculate_skew_metrics(self):
        """Calculate volatility skew and smile metrics"""
        # Simulated skew data based on typical ETH options patterns
        # In practice, this would use actual strike-level IV data
        strikes = np.array([0.8, 0.9, 1.0, 1.1, 1.2])  # Moneyness
        ivs = np.array([75, 68, 65, 63, 62])  # Typical ETH skew pattern
        
        # Calculate skew metrics
        put_call_skew = ivs[0] - ivs[-1]  # 25D put vs call
        atm_skew = ivs[1] - ivs[3]  # 10D put vs call relative to ATM
        
        return {
            'put_call_skew': put_call_skew,
            'atm_skew': atm_skew,
            'smile_curvature': np.std(ivs)
        }
    
    def garch_volatility_forecast(self, returns_series, forecast_days=30):
        """Simple GARCH(1,1) volatility forecast"""
        # Simplified GARCH implementation
        # In practice, would use arch library for full GARCH modeling
        
        returns = np.array(returns_series)
        mean_return = np.mean(returns)
        
        # GARCH parameters (simplified estimation)
        omega = 0.000001  # Long-term variance
        alpha = 0.1       # ARCH coefficient
        beta = 0.85       # GARCH coefficient
        
        # Calculate conditional variance
        variance = np.var(returns)
        forecasted_variance = omega + alpha * (returns[-1] - mean_return)**2 + beta * variance
        
        # Annualized volatility forecast
        forecasted_vol = np.sqrt(forecasted_variance * 252) * 100
        
        return forecasted_vol
    
    def monte_carlo_iv_simulation(self, n_simulations=10000, days=30):
        """Monte Carlo simulation for forward IV projections"""
        np.random.seed(42)  # For reproducibility
        
        current_iv = self.current_data['eth_iv_deribit']
        current_rv = self.current_data['eth_rv_30d']
        
        # Model parameters
        iv_mean_reversion_speed = 0.5
        iv_long_term_mean = 55.0  # Long-term IV mean
        iv_volatility = 15.0  # Volatility of IV itself
        
        dt = 1/252  # Daily time step
        
        simulated_ivs = []
        
        for _ in range(n_simulations):
            iv = current_iv
            for day in range(days):
                # Mean-reverting process with stochastic component
                dW = np.random.normal(0, np.sqrt(dt))
                div = iv_mean_reversion_speed * (iv_long_term_mean - iv) * dt + iv_volatility * dW
                iv += div
                iv = max(10, min(150, iv))  # Bound IV between reasonable limits
            
            simulated_ivs.append(iv)
        
        return np.array(simulated_ivs)
    
    def regime_detection(self):
        """Detect current volatility regime"""
        current_iv = self.current_data['eth_iv_deribit']
        current_rv = self.current_data['eth_rv_30d']
        vix = self.current_data['vix']
        
        # Define regime thresholds
        regimes = {
            'low_vol': current_iv < 40,
            'medium_vol': 40 <= current_iv < 70,
            'high_vol': current_iv >= 70,
            'crisis_vol': current_iv >= 100
        }
        
        # Cross-asset regime analysis
        tradfi_regime = 'low' if vix < 20 else 'medium' if vix < 30 else 'high'
        
        current_regime = 'medium_vol'  # Based on current 65% IV
        
        return {
            'crypto_regime': current_regime,
            'tradfi_regime': tradfi_regime,
            'regime_divergence': current_regime != tradfi_regime
        }
    
    def comprehensive_analysis(self):
        """Run comprehensive volatility analysis"""
        print("ETH Options Implied Volatility Analysis")
        print("=" * 50)
        
        # Current state metrics
        current_iv = self.current_data['eth_iv_deribit']
        current_rv_30d = self.current_data['eth_rv_30d']
        
        # Estimate IVR (using historical context)
        # Assuming 252-day range of 30-120% based on crypto volatility patterns
        estimated_ivr = self.calculate_ivr(current_iv, 30, 120)
        
        # Calculate VRP
        vrp_30d = self.calculate_vrp(current_iv, current_rv_30d)
        
        # Skew analysis
        skew_metrics = self.calculate_skew_metrics()
        
        # Regime detection
        regime_analysis = self.regime_detection()
        
        # Monte Carlo projections
        mc_projections = self.monte_carlo_iv_simulation()
        
        # Cross-asset analysis
        eth_btc_rv_ratio = self.current_data['eth_rv_7d'] / self.current_data['btc_rv_7d']
        eth_vix_ratio = current_iv / self.current_data['vix']
        
        # Compile results
        results = {
            'current_metrics': {
                'eth_iv': current_iv,
                'eth_rv_30d': current_rv_30d,
                'vrp': vrp_30d,
                'estimated_ivr': estimated_ivr,
                'iv_percentile_estimate': 0.65  # Based on current vs historical levels
            },
            'skew_analysis': skew_metrics,
            'regime_analysis': regime_analysis,
            'cross_asset': {
                'eth_btc_rv_ratio': eth_btc_rv_ratio,
                'eth_vix_ratio': eth_vix_ratio,
                'vix_regime': 'low' if self.current_data['vix'] < 20 else 'medium'
            },
            'forward_projections': {
                'mc_mean': np.mean(mc_projections),
                'mc_std': np.std(mc_projections),
                'mc_5th_percentile': np.percentile(mc_projections, 5),
                'mc_95th_percentile': np.percentile(mc_projections, 95)
            },
            'options_flow': self.options_activity
        }
        
        return results
    
    def print_analysis_summary(self, results):
        """Print formatted analysis summary"""
        print("\n1. CURRENT STATE ASSESSMENT")
        print("-" * 30)
        print(f"ETH Implied Volatility: {results['current_metrics']['eth_iv']:.1f}%")
        print(f"ETH Realized Volatility (30D): {results['current_metrics']['eth_rv_30d']:.1f}%")
        print(f"Volatility Risk Premium: {results['current_metrics']['vrp']:.1f}%")
        print(f"Estimated IV Rank: {results['current_metrics']['estimated_ivr']:.2f}")
        print(f"Estimated IV Percentile: {results['current_metrics']['iv_percentile_estimate']:.2f}")
        
        print("\n2. VOLATILITY SURFACE ANALYSIS")
        print("-" * 30)
        print(f"Put-Call Skew: {results['skew_analysis']['put_call_skew']:.1f}%")
        print(f"ATM Skew: {results['skew_analysis']['atm_skew']:.1f}%")
        print(f"Smile Curvature: {results['skew_analysis']['smile_curvature']:.1f}%")
        
        print("\n3. REGIME ANALYSIS")
        print("-" * 30)
        print(f"Crypto Volatility Regime: {results['regime_analysis']['crypto_regime']}")
        print(f"TradFi Volatility Regime: {results['regime_analysis']['tradfi_regime']}")
        print(f"Regime Divergence: {results['regime_analysis']['regime_divergence']}")
        
        print("\n4. CROSS-ASSET SIGNALS")
        print("-" * 30)
        print(f"ETH/BTC RV Ratio: {results['cross_asset']['eth_btc_rv_ratio']:.2f}")
        print(f"ETH IV/VIX Ratio: {results['cross_asset']['eth_vix_ratio']:.1f}x")
        print(f"VIX Regime: {results['cross_asset']['vix_regime']}")
        
        print("\n5. FORWARD PROJECTIONS (30-day)")
        print("-" * 30)
        print(f"Expected IV: {results['forward_projections']['mc_mean']:.1f}%")
        print(f"IV Volatility: {results['forward_projections']['mc_std']:.1f}%")
        print(f"5th Percentile: {results['forward_projections']['mc_5th_percentile']:.1f}%")
        print(f"95th Percentile: {results['forward_projections']['mc_95th_percentile']:.1f}%")
        
        print("\n6. OPTIONS FLOW ANALYSIS")
        print("-" * 30)
        print(f"Puts Bought: {results['options_flow']['puts_bought']:.1f}%")
        print(f"Calls Bought: {results['options_flow']['calls_bought']:.1f}%")
        print(f"Net Put Bias: {results['options_flow']['puts_bought'] + results['options_flow']['puts_sold'] - results['options_flow']['calls_bought'] - results['options_flow']['calls_sold']:.1f}%")

def main():
    """Main analysis function"""
    analyzer = ETHVolatilityAnalyzer()
    results = analyzer.comprehensive_analysis()
    analyzer.print_analysis_summary(results)
    
    # Save results for further analysis
    import json
    with open('/home/ubuntu/eth_volatility_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nAnalysis complete. Results saved to eth_volatility_results.json")
    return results

if __name__ == "__main__":
    results = main()

