"""
ETH Options Analysis API Routes with Input Validation
"""

from flask import Blueprint, request, jsonify
from marshmallow import Schema, fields, validate, ValidationError
import logging
from datetime import datetime
import os

# Import our modules
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from data_collector import ETHDataCollector
from analysis_engine import ETHOptionsAnalyzer
from ai_assistant import ETHOptionsAIAssistant
from src.models.eth_data import ETHMarketData, ETHAnalysisResults, TradingPositions, db

logger = logging.getLogger(__name__)

eth_bp = Blueprint('eth', __name__)

# Input validation schemas
class AIChatSchema(Schema):
    question = fields.Str(required=True, validate=validate.Length(min=1, max=1000))

class AnalysisRequestSchema(Schema):
    use_cached_data = fields.Bool(load_default=False)
    include_ai_insights = fields.Bool(load_default=True)

@eth_bp.route('/market-data', methods=['GET'])
def get_market_data():
    """Get current ETH market data"""
    try:
        collector = ETHDataCollector()
        
        # Get fresh data
        market_data = collector.collect_all_data()
        
        # Store in database
        db_entry = ETHMarketData(
            eth_price=market_data.get('eth_price'),
            eth_iv_deribit=market_data.get('eth_iv_deribit'),
            eth_iv_binance=market_data.get('eth_iv_binance'),
            eth_rv_1d=market_data.get('eth_rv_1d'),
            eth_rv_7d=market_data.get('eth_rv_7d'),
            eth_rv_30d=market_data.get('eth_rv_30d'),
            btc_rv_7d=market_data.get('btc_rv_7d'),
            btc_rv_30d=market_data.get('btc_rv_30d'),
            vix=market_data.get('vix'),
            move_index=market_data.get('move_index')
        )
        
        try:
            db.session.add(db_entry)
            db.session.commit()
        except Exception as db_error:
            logger.warning(f"Failed to store market data in DB: {db_error}")
            db.session.rollback()
        
        # Add options flow data
        market_data.update({
            'calls_bought': market_data.get('calls_bought', 20.8),
            'calls_sold': market_data.get('calls_sold', 26.4),
            'puts_bought': market_data.get('puts_bought', 32.5),
            'puts_sold': market_data.get('puts_sold', 24.8),
            'net_put_bias': market_data.get('net_put_bias', 10.1)
        })
        
        return jsonify({
            'success': True,
            'data': market_data,
            'timestamp': datetime.utcnow().isoformat()
        }), 200
        
    except Exception as e:
        logger.error(f"Error fetching market data: {e}")
        
        # Fallback to cached data
        try:
            collector = ETHDataCollector()
            cached_data = collector.get_cached_data()
            return jsonify({
                'success': True,
                'data': cached_data,
                'timestamp': datetime.utcnow().isoformat(),
                'warning': 'Using cached data due to API issues'
            }), 200
        except Exception as fallback_error:
            logger.error(f"Fallback failed: {fallback_error}")
            return jsonify({
                'success': False,
                'error': 'Failed to fetch market data'
            }), 500

@eth_bp.route('/analysis', methods=['POST'])
def run_analysis():
    """Run comprehensive ETH options analysis"""
    try:
        # Input validation
        schema = AnalysisRequestSchema()
        try:
            validated_data = schema.load(request.get_json() or {})
        except ValidationError as err:
            return jsonify({
                'success': False,
                'error': 'Invalid input',
                'details': err.messages
            }), 400
        
        # Get market data
        collector = ETHDataCollector()
        if validated_data.get('use_cached_data', False):
            market_data = collector.get_cached_data()
        else:
            market_data = collector.collect_all_data()
        
        # Run analysis
        analyzer = ETHOptionsAnalyzer()
        analysis_results = analyzer.comprehensive_analysis(market_data)
        
        # Add AI insights if requested
        if validated_data.get('include_ai_insights', True):
            try:
                ai_assistant = ETHOptionsAIAssistant()
                
                # Generate AI insights
                market_analysis = ai_assistant.analyze_market_conditions(market_data, analysis_results)
                executive_summary = ai_assistant.generate_executive_summary(analysis_results, market_data)
                risk_assessment = ai_assistant.generate_risk_assessment(analysis_results, market_data)
                
                # Generate position commentary
                positions = analysis_results.get('trading_positions', [])
                position_commentary = ai_assistant.generate_position_commentary(positions, market_data)
                
                analysis_results['ai_insights'] = {
                    'market_analysis': market_analysis,
                    'executive_summary': executive_summary,
                    'risk_assessment': risk_assessment,
                    'position_commentary': position_commentary
                }
            except Exception as ai_error:
                logger.warning(f"AI insights failed: {ai_error}")
                analysis_results['ai_insights'] = {
                    'error': 'AI insights temporarily unavailable'
                }
        
        # Store analysis results
        try:
            db_entry = ETHAnalysisResults(
                current_iv=analysis_results.get('current_metrics', {}).get('eth_iv'),
                vrp=analysis_results.get('current_metrics', {}).get('vrp'),
                iv_rank=analysis_results.get('current_metrics', {}).get('estimated_ivr'),
                put_call_skew=analysis_results.get('skew_analysis', {}).get('put_call_skew'),
                regime=analysis_results.get('regime_analysis', {}).get('crypto_regime'),
                analysis_data=analysis_results
            )
            db.session.add(db_entry)
            db.session.commit()
        except Exception as db_error:
            logger.warning(f"Failed to store analysis in DB: {db_error}")
            db.session.rollback()
        
        return jsonify({
            'success': True,
            'analysis': analysis_results,
            'timestamp': datetime.utcnow().isoformat()
        }), 200
        
    except Exception as e:
        logger.error(f"Error running analysis: {e}")
        return jsonify({
            'success': False,
            'error': 'Analysis failed',
            'details': str(e)
        }), 500

@eth_bp.route('/ai-chat', methods=['POST'])
def ai_chat():
    """AI assistant chat endpoint"""
    try:
        # Input validation
        schema = AIChatSchema()
        try:
            data = schema.load(request.get_json())
        except ValidationError as err:
            return jsonify({
                'success': False,
                'error': 'Invalid input',
                'details': err.messages
            }), 400
        
        question = data['question']
        
        # Get latest market data and analysis
        collector = ETHDataCollector()
        market_data = collector.get_cached_data()  # Use cached for speed
        
        analyzer = ETHOptionsAnalyzer()
        analysis_results = analyzer.comprehensive_analysis(market_data)
        
        # Get AI response
        ai_assistant = ETHOptionsAIAssistant()
        response = ai_assistant.answer_user_question(question, market_data, analysis_results)
        
        return jsonify({
            'success': True,
            'response': response,
            'timestamp': datetime.utcnow().isoformat()
        }), 200
        
    except Exception as e:
        logger.error(f"Error in AI chat: {e}")
        return jsonify({
            'success': False,
            'error': 'AI chat failed',
            'response': 'I apologize, but I\'m experiencing technical difficulties. Please try again later.'
        }), 500

@eth_bp.route('/historical-data', methods=['GET'])
def get_historical_data():
    """Get historical market data"""
    try:
        # Input validation for query parameters
        limit = request.args.get('limit', 100, type=int)
        if limit <= 0 or limit > 1000:
            return jsonify({
                'success': False,
                'error': 'Limit must be between 1 and 1000'
            }), 400
        
        # Get historical data from database
        historical_data = ETHMarketData.query.order_by(
            ETHMarketData.timestamp.desc()
        ).limit(limit).all()
        
        return jsonify({
            'success': True,
            'data': [entry.to_dict() for entry in historical_data],
            'count': len(historical_data)
        }), 200
        
    except Exception as e:
        logger.error(f"Error fetching historical data: {e}")
        return jsonify({
            'success': False,
            'error': 'Failed to fetch historical data'
        }), 500

@eth_bp.route('/analysis-history', methods=['GET'])
def get_analysis_history():
    """Get historical analysis results"""
    try:
        # Input validation
        limit = request.args.get('limit', 50, type=int)
        if limit <= 0 or limit > 500:
            return jsonify({
                'success': False,
                'error': 'Limit must be between 1 and 500'
            }), 400
        
        analyses = ETHAnalysisResults.query.order_by(
            ETHAnalysisResults.timestamp.desc()
        ).limit(limit).all()
        
        return jsonify({
            'success': True,
            'analyses': [analysis.to_dict() for analysis in analyses],
            'count': len(analyses)
        }), 200
        
    except Exception as e:
        logger.error(f"Error fetching analysis history: {e}")
        return jsonify({
            'success': False,
            'error': 'Failed to fetch analysis history'
        }), 500