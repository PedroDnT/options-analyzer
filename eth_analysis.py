"""
ETH Options Analysis API Routes
RESTful API endpoints for the dashboard
"""

from flask import Blueprint, request, jsonify
from datetime import datetime
import json
import logging

from src.models.eth_data import db, ETHMarketData, ETHOptionsFlow, ETHAnalysisResults, TradingPositions
from src.services.data_collector import ETHDataCollector
from src.services.analysis_engine import ETHOptionsAnalyzer
from src.services.ai_assistant import ETHOptionsAIAssistant

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

eth_bp = Blueprint('eth_analysis', __name__)

# Initialize services
data_collector = ETHDataCollector()
analyzer = ETHOptionsAnalyzer()
ai_assistant = ETHOptionsAIAssistant()

@eth_bp.route('/market-data', methods=['GET'])
def get_market_data():
    """Get current market data"""
    try:
        # Check if we should use live data or cached data
        use_live = request.args.get('live', 'false').lower() == 'true'
        
        if use_live:
            market_data = data_collector.collect_all_data()
        else:
            market_data = data_collector.get_cached_data()
        
        # Store in database
        market_record = ETHMarketData(
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
        
        flow_record = ETHOptionsFlow(
            calls_bought=market_data.get('calls_bought'),
            calls_sold=market_data.get('calls_sold'),
            puts_bought=market_data.get('puts_bought'),
            puts_sold=market_data.get('puts_sold'),
            net_put_bias=market_data.get('net_put_bias')
        )
        
        db.session.add(market_record)
        db.session.add(flow_record)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': market_data,
            'timestamp': market_data['timestamp'].isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error fetching market data: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@eth_bp.route('/analysis', methods=['POST'])
def run_analysis():
    """Run comprehensive ETH options analysis"""
    try:
        # Get latest market data
        latest_market = ETHMarketData.query.order_by(ETHMarketData.timestamp.desc()).first()
        latest_flow = ETHOptionsFlow.query.order_by(ETHOptionsFlow.timestamp.desc()).first()
        
        if not latest_market:
            return jsonify({'success': False, 'error': 'No market data available'}), 400
        
        # Combine market data
        market_data = latest_market.to_dict()
        if latest_flow:
            market_data.update(latest_flow.to_dict())
        
        # Run comprehensive analysis
        analysis_results = analyzer.comprehensive_analysis(market_data)
        
        # Generate AI insights
        ai_analysis = ai_assistant.analyze_market_conditions(market_data, analysis_results)
        position_commentary = ai_assistant.generate_position_commentary(
            analysis_results['trading_positions'], market_data
        )
        risk_assessment = ai_assistant.generate_risk_assessment(analysis_results, market_data)
        executive_summary = ai_assistant.generate_executive_summary(analysis_results, market_data)
        
        # Add AI insights to results
        analysis_results['ai_insights'] = {
            'market_analysis': ai_analysis,
            'position_commentary': position_commentary,
            'risk_assessment': risk_assessment,
            'executive_summary': executive_summary
        }
        
        # Store analysis results
        analysis_record = ETHAnalysisResults(
            iv_rank=analysis_results['current_metrics']['estimated_ivr'],
            iv_percentile=analysis_results['current_metrics']['iv_percentile'],
            vrp=analysis_results['current_metrics']['vrp'],
            put_call_skew=analysis_results['skew_analysis']['put_call_skew'],
            regime=analysis_results['regime_analysis']['crypto_regime'],
            mc_expected_iv=analysis_results['forward_projections']['mc_mean'],
            mc_5th_percentile=analysis_results['forward_projections']['mc_5th_percentile'],
            mc_95th_percentile=analysis_results['forward_projections']['mc_95th_percentile'],
            analysis_data=json.dumps(analysis_results)
        )
        
        # Store trading positions
        for position in analysis_results['trading_positions']:
            position_record = TradingPositions(
                position_type=position['position_type'],
                strategy=position['strategy'],
                strikes=position['strikes'],
                expiry=position['expiry'],
                net_credit_debit=position['net_credit_debit'],
                max_risk=position['max_risk'],
                max_profit=position['max_profit'],
                win_probability=position['win_probability'],
                priority=position['priority'],
                entry_criteria_met=position['entry_criteria_met'],
                position_details=json.dumps(position['position_details'])
            )
            db.session.add(position_record)
        
        db.session.add(analysis_record)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'analysis': analysis_results,
            'timestamp': datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error running analysis: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@eth_bp.route('/positions', methods=['GET'])
def get_trading_positions():
    """Get latest trading position recommendations"""
    try:
        # Get latest positions
        positions = TradingPositions.query.order_by(TradingPositions.timestamp.desc()).limit(10).all()
        
        positions_data = [pos.to_dict() for pos in positions]
        
        return jsonify({
            'success': True,
            'positions': positions_data
        })
        
    except Exception as e:
        logger.error(f"Error fetching positions: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@eth_bp.route('/historical-data', methods=['GET'])
def get_historical_data():
    """Get historical market data and analysis"""
    try:
        days = request.args.get('days', 30, type=int)
        
        # Get historical market data
        market_history = ETHMarketData.query.order_by(ETHMarketData.timestamp.desc()).limit(days).all()
        analysis_history = ETHAnalysisResults.query.order_by(ETHAnalysisResults.timestamp.desc()).limit(days).all()
        
        market_data = [record.to_dict() for record in market_history]
        analysis_data = [record.to_dict() for record in analysis_history]
        
        return jsonify({
            'success': True,
            'market_history': market_data,
            'analysis_history': analysis_data
        })
        
    except Exception as e:
        logger.error(f"Error fetching historical data: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@eth_bp.route('/ai-chat', methods=['POST'])
def ai_chat():
    """Chat with AI assistant about the analysis"""
    try:
        data = request.get_json()
        question = data.get('question', '')
        
        if not question:
            return jsonify({'success': False, 'error': 'Question is required'}), 400
        
        # Get latest market data and analysis
        latest_market = ETHMarketData.query.order_by(ETHMarketData.timestamp.desc()).first()
        latest_analysis = ETHAnalysisResults.query.order_by(ETHAnalysisResults.timestamp.desc()).first()
        
        if not latest_market or not latest_analysis:
            return jsonify({'success': False, 'error': 'No recent data available for analysis'}), 400
        
        market_data = latest_market.to_dict()
        analysis_results = json.loads(latest_analysis.analysis_data) if latest_analysis.analysis_data else {}
        
        # Get AI response
        response = ai_assistant.answer_user_question(question, market_data, analysis_results)
        
        return jsonify({
            'success': True,
            'question': question,
            'response': response,
            'timestamp': datetime.utcnow().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error in AI chat: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@eth_bp.route('/dashboard-summary', methods=['GET'])
def get_dashboard_summary():
    """Get comprehensive dashboard summary"""
    try:
        # Get latest data
        latest_market = ETHMarketData.query.order_by(ETHMarketData.timestamp.desc()).first()
        latest_analysis = ETHAnalysisResults.query.order_by(ETHAnalysisResults.timestamp.desc()).first()
        latest_positions = TradingPositions.query.filter_by(entry_criteria_met=True).order_by(TradingPositions.timestamp.desc()).limit(3).all()
        
        if not latest_market:
            return jsonify({'success': False, 'error': 'No market data available'}), 400
        
        summary = {
            'market_data': latest_market.to_dict(),
            'analysis': latest_analysis.to_dict() if latest_analysis else None,
            'top_positions': [pos.to_dict() for pos in latest_positions],
            'last_updated': latest_market.timestamp.isoformat()
        }
        
        return jsonify({
            'success': True,
            'summary': summary
        })
        
    except Exception as e:
        logger.error(f"Error fetching dashboard summary: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@eth_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'success': True,
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'services': {
            'database': 'connected',
            'data_collector': 'ready',
            'analyzer': 'ready',
            'ai_assistant': 'ready'
        }
    })

