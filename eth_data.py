"""
ETH Options Data Models
Database models for storing ETH options and market data
"""

from src.models.user import db
from datetime import datetime
import json

class ETHMarketData(db.Model):
    """Store current ETH market data"""
    __tablename__ = 'eth_market_data'
    
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    eth_price = db.Column(db.Float, nullable=False)
    eth_iv_deribit = db.Column(db.Float)
    eth_iv_binance = db.Column(db.Float)
    eth_rv_1d = db.Column(db.Float)
    eth_rv_7d = db.Column(db.Float)
    eth_rv_30d = db.Column(db.Float)
    btc_rv_7d = db.Column(db.Float)
    btc_rv_30d = db.Column(db.Float)
    vix = db.Column(db.Float)
    move_index = db.Column(db.Float)
    
    def to_dict(self):
        return {
            'id': self.id,
            'timestamp': self.timestamp.isoformat(),
            'eth_price': self.eth_price,
            'eth_iv_deribit': self.eth_iv_deribit,
            'eth_iv_binance': self.eth_iv_binance,
            'eth_rv_1d': self.eth_rv_1d,
            'eth_rv_7d': self.eth_rv_7d,
            'eth_rv_30d': self.eth_rv_30d,
            'btc_rv_7d': self.btc_rv_7d,
            'btc_rv_30d': self.btc_rv_30d,
            'vix': self.vix,
            'move_index': self.move_index
        }

class ETHOptionsFlow(db.Model):
    """Store ETH options flow data"""
    __tablename__ = 'eth_options_flow'
    
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    calls_bought = db.Column(db.Float)
    calls_sold = db.Column(db.Float)
    puts_bought = db.Column(db.Float)
    puts_sold = db.Column(db.Float)
    net_put_bias = db.Column(db.Float)
    
    def to_dict(self):
        return {
            'id': self.id,
            'timestamp': self.timestamp.isoformat(),
            'calls_bought': self.calls_bought,
            'calls_sold': self.calls_sold,
            'puts_bought': self.puts_bought,
            'puts_sold': self.puts_sold,
            'net_put_bias': self.net_put_bias
        }

class ETHAnalysisResults(db.Model):
    """Store analysis results"""
    __tablename__ = 'eth_analysis_results'
    
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    iv_rank = db.Column(db.Float)
    iv_percentile = db.Column(db.Float)
    vrp = db.Column(db.Float)
    put_call_skew = db.Column(db.Float)
    regime = db.Column(db.String(50))
    mc_expected_iv = db.Column(db.Float)
    mc_5th_percentile = db.Column(db.Float)
    mc_95th_percentile = db.Column(db.Float)
    analysis_data = db.Column(db.Text)  # JSON string for full analysis
    
    def to_dict(self):
        return {
            'id': self.id,
            'timestamp': self.timestamp.isoformat(),
            'iv_rank': self.iv_rank,
            'iv_percentile': self.iv_percentile,
            'vrp': self.vrp,
            'put_call_skew': self.put_call_skew,
            'regime': self.regime,
            'mc_expected_iv': self.mc_expected_iv,
            'mc_5th_percentile': self.mc_5th_percentile,
            'mc_95th_percentile': self.mc_95th_percentile,
            'analysis_data': json.loads(self.analysis_data) if self.analysis_data else None
        }

class TradingPositions(db.Model):
    """Store recommended trading positions"""
    __tablename__ = 'trading_positions'
    
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    position_type = db.Column(db.String(100), nullable=False)
    strategy = db.Column(db.String(200), nullable=False)
    strikes = db.Column(db.String(200))
    expiry = db.Column(db.String(50))
    net_credit_debit = db.Column(db.Float)
    max_risk = db.Column(db.Float)
    max_profit = db.Column(db.Float)
    win_probability = db.Column(db.Float)
    priority = db.Column(db.String(20))
    entry_criteria_met = db.Column(db.Boolean, default=False)
    position_details = db.Column(db.Text)  # JSON string
    
    def to_dict(self):
        return {
            'id': self.id,
            'timestamp': self.timestamp.isoformat(),
            'position_type': self.position_type,
            'strategy': self.strategy,
            'strikes': self.strikes,
            'expiry': self.expiry,
            'net_credit_debit': self.net_credit_debit,
            'max_risk': self.max_risk,
            'max_profit': self.max_profit,
            'win_probability': self.win_probability,
            'priority': self.priority,
            'entry_criteria_met': self.entry_criteria_met,
            'position_details': json.loads(self.position_details) if self.position_details else None
        }

