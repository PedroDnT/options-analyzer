"""
AI Assistant for ETH Options Analysis
Intelligent analysis and recommendations using LLM
"""

import openai
import json
import logging
from typing import Dict, List, Optional
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ETHOptionsAIAssistant:
    def __init__(self):
        """Initialize the AI assistant with OpenAI client"""
        # OpenAI client is automatically configured via environment variables
        self.client = openai.OpenAI()
        
    def analyze_market_conditions(self, market_data: Dict, analysis_results: Dict) -> str:
        """Generate intelligent market analysis using LLM"""
        
        prompt = f"""
        You are an expert quantitative analyst specializing in cryptocurrency options. Analyze the current ETH options market conditions and provide insights.

        Current Market Data:
        - ETH Price: ${market_data.get('eth_price', 'N/A')}
        - ETH Implied Volatility: {market_data.get('eth_iv_deribit', 'N/A')}%
        - ETH Realized Volatility (30D): {market_data.get('eth_rv_30d', 'N/A')}%
        - VIX: {market_data.get('vix', 'N/A')}
        - BTC Realized Volatility (7D): {market_data.get('btc_rv_7d', 'N/A')}%

        Analysis Results:
        - Volatility Risk Premium: {analysis_results.get('current_metrics', {}).get('vrp', 'N/A')}%
        - IV Rank: {analysis_results.get('current_metrics', {}).get('estimated_ivr', 'N/A')}
        - Put-Call Skew: {analysis_results.get('skew_analysis', {}).get('put_call_skew', 'N/A')}%
        - Volatility Regime: {analysis_results.get('regime_analysis', {}).get('crypto_regime', 'N/A')}
        - Monte Carlo Expected IV (30D): {analysis_results.get('forward_projections', {}).get('mc_mean', 'N/A')}%

        Provide a concise but comprehensive analysis covering:
        1. Current market regime assessment
        2. Key opportunities and risks
        3. Cross-asset implications
        4. Forward-looking outlook

        Keep the response professional and actionable, suitable for institutional traders.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert quantitative analyst specializing in cryptocurrency options trading."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=800,
                temperature=0.3
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Error generating AI analysis: {e}")
            return "AI analysis temporarily unavailable. Please refer to quantitative metrics for trading decisions."
    
    def generate_position_commentary(self, positions: List[Dict], market_data: Dict) -> Dict:
        """Generate intelligent commentary for each trading position"""
        
        commentaries = {}
        
        for position in positions:
            prompt = f"""
            Analyze this ETH options trading position and provide intelligent commentary:

            Position: {position['position_type']}
            Strategy: {position['strategy']}
            Strikes: {position['strikes']}
            Priority: {position['priority']}
            Win Probability: {position.get('win_probability', 'N/A')}
            Entry Criteria Met: {position['entry_criteria_met']}

            Current Market Context:
            - ETH Price: ${market_data.get('eth_price', 'N/A')}
            - Current IV: {market_data.get('eth_iv_deribit', 'N/A')}%

            Provide a brief (2-3 sentences) commentary on:
            1. Why this position makes sense in current market conditions
            2. Key risks to monitor
            3. Optimal timing for execution

            Be concise and actionable.
            """
            
            try:
                response = self.client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You are an expert options trader providing position analysis."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=200,
                    temperature=0.3
                )
                
                commentaries[position['position_type']] = response.choices[0].message.content
                
            except Exception as e:
                logger.error(f"Error generating position commentary: {e}")
                commentaries[position['position_type']] = "Commentary temporarily unavailable."
        
        return commentaries
    
    def generate_risk_assessment(self, analysis_results: Dict, market_data: Dict) -> str:
        """Generate intelligent risk assessment"""
        
        prompt = f"""
        Provide a risk assessment for ETH options trading based on current market conditions:

        Key Metrics:
        - IV Rank: {analysis_results.get('current_metrics', {}).get('estimated_ivr', 'N/A')}
        - Volatility Risk Premium: {analysis_results.get('current_metrics', {}).get('vrp', 'N/A')}%
        - Regime: {analysis_results.get('regime_analysis', {}).get('crypto_regime', 'N/A')}
        - Cross-asset divergence: {analysis_results.get('regime_analysis', {}).get('regime_divergence', 'N/A')}
        - ETH/VIX Ratio: {analysis_results.get('cross_asset', {}).get('eth_vix_ratio', 'N/A')}

        Assess the following risk factors:
        1. Volatility expansion risk
        2. Liquidity risk in ETH options
        3. Regime transition probability
        4. Cross-asset contagion risk
        5. Model risk and limitations

        Provide specific risk management recommendations.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a risk management expert for cryptocurrency derivatives."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=600,
                temperature=0.3
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Error generating risk assessment: {e}")
            return "Risk assessment temporarily unavailable. Please apply standard risk management protocols."
    
    def answer_user_question(self, question: str, market_data: Dict, analysis_results: Dict) -> str:
        """Answer user questions about the analysis"""
        
        context = f"""
        Current ETH Options Market Context:
        - ETH Price: ${market_data.get('eth_price', 'N/A')}
        - Implied Volatility: {market_data.get('eth_iv_deribit', 'N/A')}%
        - Realized Volatility: {market_data.get('eth_rv_30d', 'N/A')}%
        - VRP: {analysis_results.get('current_metrics', {}).get('vrp', 'N/A')}%
        - IV Rank: {analysis_results.get('current_metrics', {}).get('estimated_ivr', 'N/A')}
        - Regime: {analysis_results.get('regime_analysis', {}).get('crypto_regime', 'N/A')}
        """
        
        prompt = f"""
        You are an expert ETH options analyst. Answer the user's question based on the current market analysis.

        {context}

        User Question: {question}

        Provide a clear, accurate answer based on the market data and analysis. If the question requires information not available in the context, explain what additional data would be needed.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert cryptocurrency options analyst providing accurate, data-driven answers."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=400,
                temperature=0.3
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Error answering user question: {e}")
            return "I'm unable to process your question at the moment. Please try again later."
    
    def generate_executive_summary(self, analysis_results: Dict, market_data: Dict) -> str:
        """Generate executive summary of the analysis"""
        
        prompt = f"""
        Generate a concise executive summary for institutional traders based on this ETH options analysis:

        Assessment: {analysis_results.get('assessment', {}).get('overall_assessment', 'N/A')}
        VRP: {analysis_results.get('current_metrics', {}).get('vrp', 'N/A')}%
        Top Opportunity: {analysis_results.get('assessment', {}).get('top_opportunity', 'N/A')}
        Regime: {analysis_results.get('regime_analysis', {}).get('crypto_regime', 'N/A')}
        
        Forward Outlook:
        - Expected IV (30D): {analysis_results.get('forward_projections', {}).get('mc_mean', 'N/A')}%
        - 5th Percentile: {analysis_results.get('forward_projections', {}).get('mc_5th_percentile', 'N/A')}%
        - 95th Percentile: {analysis_results.get('forward_projections', {}).get('mc_95th_percentile', 'N/A')}%

        Provide a 3-4 sentence executive summary highlighting:
        1. Current market assessment
        2. Top trading opportunity
        3. Key risk factors
        4. Recommended action
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are writing an executive summary for institutional cryptocurrency traders."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                temperature=0.3
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Error generating executive summary: {e}")
            return "Executive summary temporarily unavailable."

