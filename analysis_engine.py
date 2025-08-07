"""
ETH Options Analysis Engine
Comprehensive quantitative analysis replicating the full research report
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import json
import logging
from scipy import stats
from scipy.optimize import minimize

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ETHOptionsAnalyzer:
    def __init__(self):
        """Initialize the analyzer with default parameters"""
        self.long_term_iv_mean = 55.0
        self.mean_reversion_speed = 0.5
        self.iv_volatility = 15.0
        
    def calculate_ivr(self, current_iv: float, historical_ivs: List[float]) -> float:
        """Calculate Implied Volatility Rank"""
        if not historical_ivs or len(historical_ivs) < 2:
            # Use estimated range if no historical data
            min_iv, max_iv = 30.0, 120.0
        else:
            min_iv = min(historical_ivs)
            max_iv = max(historical_ivs)
        
        if max_iv == min_iv:
            return 0.5
        
        ivr = (current_iv - min_iv) / (max_iv - min_iv)
        return max(0, min(1, ivr))
    
    def calculate_iv_percentile(self, current_iv: float, historical_ivs: List[float]) -> float:
        """Calculate IV Percentile"""
        if not historical_ivs:
            return 0.5
        
        percentile = stats.percentileofscore(historical_ivs, current_iv) / 100
        return percentile
    
    def calculate_vrp(self, implied_vol: float, realized_vol: float) -> float:
        """Calculate Volatility Risk Premium"""
        if implied_vol is None or realized_vol is None:
            return None
        return implied_vol - realized_vol
    
    def calculate_skew_metrics(self, current_iv: float) -> Dict:
        """Calculate volatility skew metrics (simulated based on typical patterns)"""
        # In production, this would use actual strike-level IV data
        # Simulating typical ETH skew patterns
        
        # ETH typically shows put skew
        put_call_skew = 13.0  # 25D put vs call
        atm_skew = 5.0        # 10D put vs call relative to ATM
        smile_curvature = 4.7  # Standard deviation across strikes
        
        return {
            'put_call_skew': put_call_skew,
            'atm_skew': atm_skew,
            'smile_curvature': smile_curvature
        }
    
    def monte_carlo_iv_simulation(self, current_iv: float, n_simulations: int = 10000, days: int = 30) -> Dict:
        """Monte Carlo simulation for forward IV projections"""
        np.random.seed(42)  # For reproducibility
        
        dt = 1/252  # Daily time step
        simulated_ivs = []
        
        for _ in range(n_simulations):
            iv = current_iv
            for day in range(days):
                # Mean-reverting process with stochastic component
                dW = np.random.normal(0, np.sqrt(dt))
                div = self.mean_reversion_speed * (self.long_term_iv_mean - iv) * dt + self.iv_volatility * dW
                iv += div
                iv = max(10, min(150, iv))  # Bound IV between reasonable limits
            
            simulated_ivs.append(iv)
        
        simulated_ivs = np.array(simulated_ivs)
        
        return {
            'mc_mean': np.mean(simulated_ivs),
            'mc_std': np.std(simulated_ivs),
            'mc_5th_percentile': np.percentile(simulated_ivs, 5),
            'mc_95th_percentile': np.percentile(simulated_ivs, 95),
            'mc_median': np.median(simulated_ivs),
            'mc_distribution': simulated_ivs.tolist()[:1000]  # Sample for frontend
        }
    
    def detect_volatility_regime(self, current_iv: float, vix: float) -> Dict:
        """Detect current volatility regime"""
        # Crypto regime classification
        if current_iv < 40:
            crypto_regime = 'low_vol'
        elif current_iv < 70:
            crypto_regime = 'medium_vol'
        elif current_iv < 100:
            crypto_regime = 'high_vol'
        else:
            crypto_regime = 'crisis_vol'
        
        # TradFi regime classification
        if vix < 20:
            tradfi_regime = 'low'
        elif vix < 30:
            tradfi_regime = 'medium'
        else:
            tradfi_regime = 'high'
        
        regime_divergence = crypto_regime != tradfi_regime
        
        return {
            'crypto_regime': crypto_regime,
            'tradfi_regime': tradfi_regime,
            'regime_divergence': regime_divergence
        }
    
    def calculate_cross_asset_signals(self, data: Dict) -> Dict:
        """Calculate cross-asset volatility signals"""
        eth_rv_7d = data.get('eth_rv_7d', 0)
        btc_rv_7d = data.get('btc_rv_7d', 0)
        eth_iv = data.get('eth_iv_deribit', 0)
        vix = data.get('vix', 0)
        
        # Calculate ratios
        eth_btc_rv_ratio = eth_rv_7d / btc_rv_7d if btc_rv_7d > 0 else None
        eth_vix_ratio = eth_iv / vix if vix > 0 else None
        
        return {
            'eth_btc_rv_ratio': eth_btc_rv_ratio,
            'eth_vix_ratio': eth_vix_ratio,
            'vix_regime': 'low' if vix < 20 else 'medium' if vix < 30 else 'high'
        }
    
    def generate_trading_positions(self, analysis_results: Dict, market_data: Dict) -> List[Dict]:
        """Generate specific trading position recommendations"""
        positions = []
        
        current_iv = analysis_results.get('current_metrics', {}).get('eth_iv', 0)
        vrp = analysis_results.get('current_metrics', {}).get('vrp', 0)
        skew = analysis_results.get('skew_analysis', {}).get('put_call_skew', 0)
        ivr = analysis_results.get('current_metrics', {}).get('estimated_ivr', 0)
        eth_price = market_data.get('eth_price', 3600)
        
        # Position 1: Short Put Spread (High Priority)
        if vrp > 3 and skew > 8 and ivr > 0.3:
            positions.append({
                'position_type': 'Short Put Spread',
                'strategy': 'Monetize elevated put skew and positive VRP',
                'strikes': f'SELL ${eth_price * 0.94:.0f} Put / BUY ${eth_price * 0.89:.0f} Put',
                'expiry': '31 DTE',
                'net_credit_debit': 50.0,
                'max_risk': 150.0,
                'max_profit': 50.0,
                'win_probability': 0.75,
                'priority': 'HIGH',
                'entry_criteria_met': True,
                'position_details': {
                    'sell_strike': eth_price * 0.94,
                    'buy_strike': eth_price * 0.89,
                    'breakeven': eth_price * 0.94 - 50,
                    'sizing': '10-30 spreads',
                    'rationale': f'VRP: {vrp:.1f}%, Skew: {skew:.1f}%, IVR: {ivr:.2f}'
                }
            })
        
        # Position 2: Short Straddle (Medium Priority)
        if vrp > 5 and ivr > 0.35:
            positions.append({
                'position_type': 'Short Straddle',
                'strategy': 'Capture volatility risk premium with delta-neutral exposure',
                'strikes': f'SELL ${eth_price:.0f} Call & Put',
                'expiry': '31 DTE',
                'net_credit_debit': 200.0,
                'max_risk': None,  # Undefined risk
                'max_profit': 200.0,
                'win_probability': 0.60,
                'priority': 'MEDIUM',
                'entry_criteria_met': vrp > 5 and current_iv > 60,
                'position_details': {
                    'strike': eth_price,
                    'breakevens': [eth_price - 200, eth_price + 200],
                    'sizing': '1-5 straddles',
                    'rationale': f'VRP: {vrp:.1f}%, IV: {current_iv:.1f}%'
                }
            })
        
        # Position 3: Calendar Spread (Lower Priority)
        positions.append({
            'position_type': 'Calendar Spread',
            'strategy': 'Exploit term structure backwardation',
            'strikes': f'SELL 14 DTE / BUY 31 DTE ${eth_price:.0f} Call',
            'expiry': '14/31 DTE',
            'net_credit_debit': -30.0,
            'max_risk': 30.0,
            'max_profit': 60.0,
            'win_probability': 0.55,
            'priority': 'LOW',
            'entry_criteria_met': True,
            'position_details': {
                'strike': eth_price,
                'sizing': '5-25 calendars',
                'rationale': 'Term structure backwardation'
            }
        })
        
        # Position 4: Protective Puts (Hedge)
        positions.append({
            'position_type': 'Protective Put',
            'strategy': 'Portfolio protection given bearish options flow',
            'strikes': f'BUY ${eth_price * 0.89:.0f} Put',
            'expiry': '45 DTE',
            'net_credit_debit': -95.0,
            'max_risk': 95.0,
            'max_profit': None,  # Protection value
            'win_probability': None,
            'priority': 'HEDGE',
            'entry_criteria_met': True,
            'position_details': {
                'strike': eth_price * 0.89,
                'protection_level': '11% below current price',
                'sizing': '1 put per 1 ETH held',
                'rationale': 'Bearish options flow protection'
            }
        })
        
        return positions
    
    def comprehensive_analysis(self, market_data: Dict, historical_data: Optional[List] = None) -> Dict:
        """Run comprehensive volatility analysis"""
        logger.info("Starting comprehensive ETH options analysis...")
        
        # Extract key metrics
        current_iv = market_data.get('eth_iv_deribit', 65.4)
        current_rv_30d = market_data.get('eth_rv_30d', 59.0)
        vix = market_data.get('vix', 17.73)
        
        # Calculate core metrics
        vrp = self.calculate_vrp(current_iv, current_rv_30d)
        
        # Estimate IVR and percentile (would use historical data in production)
        historical_ivs = [45, 50, 55, 60, 65, 70, 75, 80, 85, 90]  # Simulated
        estimated_ivr = self.calculate_ivr(current_iv, historical_ivs)
        iv_percentile = self.calculate_iv_percentile(current_iv, historical_ivs)
        
        # Skew analysis
        skew_metrics = self.calculate_skew_metrics(current_iv)
        
        # Regime detection
        regime_analysis = self.detect_volatility_regime(current_iv, vix)
        
        # Monte Carlo projections
        mc_projections = self.monte_carlo_iv_simulation(current_iv)
        
        # Cross-asset analysis
        cross_asset = self.calculate_cross_asset_signals(market_data)
        
        # Compile results
        results = {
            'timestamp': datetime.utcnow().isoformat(),
            'current_metrics': {
                'eth_iv': current_iv,
                'eth_rv_30d': current_rv_30d,
                'vrp': vrp,
                'estimated_ivr': estimated_ivr,
                'iv_percentile': iv_percentile
            },
            'skew_analysis': skew_metrics,
            'regime_analysis': regime_analysis,
            'cross_asset': cross_asset,
            'forward_projections': mc_projections,
            'options_flow': {
                'puts_bought': market_data.get('puts_bought', 32.5),
                'calls_bought': market_data.get('calls_bought', 20.8),
                'net_put_bias': market_data.get('net_put_bias', 10.1)
            }
        }
        
        # Generate trading positions
        trading_positions = self.generate_trading_positions(results, market_data)
        results['trading_positions'] = trading_positions
        
        # Add assessment summary
        results['assessment'] = self._generate_assessment_summary(results)
        
        logger.info("Comprehensive analysis completed")
        return results
    
    def _generate_assessment_summary(self, results: Dict) -> Dict:
        """Generate high-level assessment summary"""
        current_iv = results['current_metrics']['eth_iv']
        vrp = results['current_metrics']['vrp']
        ivr = results['current_metrics']['estimated_ivr']
        
        # Overall assessment
        if ivr > 0.7:
            iv_assessment = "EXPENSIVE"
        elif ivr > 0.4:
            iv_assessment = "MODERATELY EXPENSIVE"
        elif ivr > 0.2:
            iv_assessment = "FAIR VALUE"
        else:
            iv_assessment = "CHEAP"
        
        # VRP assessment
        if vrp > 15:
            vrp_assessment = "VERY HIGH PREMIUM"
        elif vrp > 8:
            vrp_assessment = "HIGH PREMIUM"
        elif vrp > 3:
            vrp_assessment = "MODERATE PREMIUM"
        elif vrp > -3:
            vrp_assessment = "FAIR PREMIUM"
        else:
            vrp_assessment = "NEGATIVE PREMIUM"
        
        # Trading recommendation
        high_priority_positions = [p for p in results['trading_positions'] if p['priority'] == 'HIGH']
        
        return {
            'overall_assessment': iv_assessment,
            'vrp_assessment': vrp_assessment,
            'regime': results['regime_analysis']['crypto_regime'],
            'top_opportunity': high_priority_positions[0]['position_type'] if high_priority_positions else None,
            'risk_level': 'MODERATE',
            'confidence': 'HIGH' if ivr > 0.3 and abs(vrp) > 3 else 'MEDIUM'
        }

