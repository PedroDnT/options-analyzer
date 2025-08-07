"""
Database models for ETH market data storage
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from .user import db

class ETHMarketData(db.Model):
    """Store ETH market data snapshots"""
    __tablename__ = 'eth_market_data'
    
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    eth_price = db.Column(db.Float)
    eth_iv_deribit = db.Column(db.Float)
    eth_iv_binance = db.Column(db.Float)
    eth_rv_1d = db.Column(db.Float)
    eth_rv_7d = db.Column(db.Float)
    eth_rv_30d = db.Column(db.Float)
    btc_rv_7d = db.Column(db.Float)
    btc_rv_30d = db.Column(db.Float)
    vix = db.Column(db.Float)
    move_index = db.Column(db.Float)
    
    def __repr__(self):
        return f'<ETHMarketData {self.timestamp}>'
    
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
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    calls_bought = db.Column(db.Float)
    calls_sold = db.Column(db.Float)
    puts_bought = db.Column(db.Float)
    puts_sold = db.Column(db.Float)
    net_put_bias = db.Column(db.Float)
    options_volume_24h = db.Column(db.BigInteger)
    
    def to_dict(self):
        return {
            'id': self.id,
            'timestamp': self.timestamp.isoformat(),
            'calls_bought': self.calls_bought,
            'calls_sold': self.calls_sold,
            'puts_bought': self.puts_bought,
            'puts_sold': self.puts_sold,
            'net_put_bias': self.net_put_bias,
            'options_volume_24h': self.options_volume_24h
        }

class ETHAnalysisResults(db.Model):
    """Store analysis results"""
    __tablename__ = 'eth_analysis_results'
    
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    current_iv = db.Column(db.Float)
    vrp = db.Column(db.Float)
    iv_rank = db.Column(db.Float)
    put_call_skew = db.Column(db.Float)
    regime = db.Column(db.String(50))
    analysis_data = db.Column(db.JSON)  # Store full analysis as JSON
    
    def to_dict(self):
        return {
            'id': self.id,
            'timestamp': self.timestamp.isoformat(),
            'current_iv': self.current_iv,
            'vrp': self.vrp,
            'iv_rank': self.iv_rank,
            'put_call_skew': self.put_call_skew,
            'regime': self.regime,
            'analysis_data': self.analysis_data
        }

class TradingPositions(db.Model):
    """Store trading position recommendations"""
    __tablename__ = 'trading_positions'
    
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    analysis_id = db.Column(db.Integer, db.ForeignKey('eth_analysis_results.id'))
    position_type = db.Column(db.String(100))
    priority = db.Column(db.String(20))
    strategy = db.Column(db.Text)
    strikes = db.Column(db.String(200))
    expiry = db.Column(db.String(50))
    net_credit_debit = db.Column(db.Float)
    max_risk = db.Column(db.Float)
    max_profit = db.Column(db.Float)
    win_probability = db.Column(db.Float)
    entry_criteria_met = db.Column(db.Boolean)
    position_details = db.Column(db.JSON)
    
    def to_dict(self):
        return {
            'id': self.id,
            'timestamp': self.timestamp.isoformat(),
            'analysis_id': self.analysis_id,
            'position_type': self.position_type,
            'priority': self.priority,
            'strategy': self.strategy,
            'strikes': self.strikes,
            'expiry': self.expiry,
            'net_credit_debit': self.net_credit_debit,
            'max_risk': self.max_risk,
            'max_profit': self.max_profit,
            'win_probability': self.win_probability,
            'entry_criteria_met': self.entry_criteria_met,
            'position_details': self.position_details
        }