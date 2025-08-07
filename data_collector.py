"""
ETH Options Data Collector
Real-time data collection from multiple sources
"""

import requests
import json
import time
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
from typing import Dict, Optional, List
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ETHDataCollector:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'ETH-Options-Dashboard/1.0'
        })
        
    def get_eth_price(self) -> Optional[float]:
        """Get current ETH price from CoinGecko"""
        try:
            url = "https://api.coingecko.com/api/v3/simple/price"
            params = {
                'ids': 'ethereum',
                'vs_currencies': 'usd'
            }
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            return data['ethereum']['usd']
        except Exception as e:
            logger.error(f"Error fetching ETH price: {e}")
            return None
    
    def get_deribit_iv_data(self) -> Dict:
        """Get ETH implied volatility data from Deribit"""
        try:
            # Deribit public API for volatility index
            url = "https://www.deribit.com/api/v2/public/get_volatility_index_data"
            params = {
                'currency': 'ETH',
                'start_timestamp': int((datetime.now() - timedelta(days=1)).timestamp() * 1000),
                'end_timestamp': int(datetime.now().timestamp() * 1000)
            }
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data.get('result') and len(data['result']) > 0:
                latest = data['result'][-1]
                return {
                    'eth_iv_deribit': latest[1],  # volatility value
                    'timestamp': datetime.fromtimestamp(latest[0] / 1000)
                }
            return {'eth_iv_deribit': None}
        except Exception as e:
            logger.error(f"Error fetching Deribit IV data: {e}")
            return {'eth_iv_deribit': None}
    
    def get_binance_options_data(self) -> Dict:
        """Get ETH options data from Binance (simulated for now)"""
        try:
            # Note: Binance options API requires authentication for detailed data
            # For demo purposes, we'll simulate based on typical patterns
            # In production, this would use actual Binance API
            return {
                'eth_iv_binance': 65.0,  # Placeholder
                'options_volume_24h': 150000000  # Placeholder
            }
        except Exception as e:
            logger.error(f"Error fetching Binance options data: {e}")
            return {'eth_iv_binance': None}
    
    def calculate_realized_volatility(self, prices: List[float], window: int = 30) -> float:
        """Calculate realized volatility from price series"""
        if len(prices) < window + 1:
            return None
        
        # Calculate log returns
        returns = []
        for i in range(1, len(prices)):
            returns.append(np.log(prices[i] / prices[i-1]))
        
        # Take last 'window' returns
        recent_returns = returns[-window:]
        
        # Calculate annualized volatility
        volatility = np.std(recent_returns) * np.sqrt(252) * 100
        return volatility
    
    def get_eth_historical_prices(self, days: int = 90) -> List[float]:
        """Get ETH historical prices for volatility calculation"""
        try:
            url = "https://api.coingecko.com/api/v3/coins/ethereum/market_chart"
            params = {
                'vs_currency': 'usd',
                'days': days,
                'interval': 'daily'
            }
            response = self.session.get(url, params=params, timeout=15)
            response.raise_for_status()
            data = response.json()
            
            prices = [price[1] for price in data['prices']]
            return prices
        except Exception as e:
            logger.error(f"Error fetching ETH historical prices: {e}")
            return []
    
    def get_btc_realized_volatility(self) -> Dict:
        """Get BTC realized volatility for comparison"""
        try:
            # Get BTC historical prices
            url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"
            params = {
                'vs_currency': 'usd',
                'days': 30,
                'interval': 'daily'
            }
            response = self.session.get(url, params=params, timeout=15)
            response.raise_for_status()
            data = response.json()
            
            prices = [price[1] for price in data['prices']]
            
            # Calculate 7-day and 30-day RV
            rv_7d = self.calculate_realized_volatility(prices, 7)
            rv_30d = self.calculate_realized_volatility(prices, 30)
            
            return {
                'btc_rv_7d': rv_7d,
                'btc_rv_30d': rv_30d
            }
        except Exception as e:
            logger.error(f"Error fetching BTC volatility: {e}")
            return {'btc_rv_7d': None, 'btc_rv_30d': None}
    
    def get_vix_data(self) -> Optional[float]:
        """Get current VIX level"""
        try:
            # Using Yahoo Finance API for VIX
            url = "https://query1.finance.yahoo.com/v8/finance/chart/%5EVIX"
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if 'chart' in data and 'result' in data['chart'] and len(data['chart']['result']) > 0:
                result = data['chart']['result'][0]
                if 'meta' in result and 'regularMarketPrice' in result['meta']:
                    return result['meta']['regularMarketPrice']
            return None
        except Exception as e:
            logger.error(f"Error fetching VIX data: {e}")
            return None
    
    def get_move_index(self) -> Optional[float]:
        """Get MOVE index (bond volatility)"""
        try:
            # MOVE index is harder to get real-time, using placeholder
            # In production, would use Bloomberg API or similar
            return 89.20  # Placeholder based on recent levels
        except Exception as e:
            logger.error(f"Error fetching MOVE index: {e}")
            return None
    
    def get_options_flow_data(self) -> Dict:
        """Get options flow data (simulated for demo)"""
        try:
            # In production, this would aggregate from multiple exchanges
            # For demo, using realistic simulated data
            return {
                'calls_bought': 20.8,
                'calls_sold': 26.4,
                'puts_bought': 32.5,
                'puts_sold': 24.8,
                'net_put_bias': 10.1
            }
        except Exception as e:
            logger.error(f"Error fetching options flow: {e}")
            return {}
    
    def collect_all_data(self) -> Dict:
        """Collect all market data in one call"""
        logger.info("Starting comprehensive data collection...")
        
        # Get current ETH price
        eth_price = self.get_eth_price()
        
        # Get historical prices for volatility calculation
        eth_prices = self.get_eth_historical_prices()
        
        # Calculate ETH realized volatilities
        eth_rv_1d = self.calculate_realized_volatility(eth_prices, 1) if eth_prices else None
        eth_rv_7d = self.calculate_realized_volatility(eth_prices, 7) if eth_prices else None
        eth_rv_30d = self.calculate_realized_volatility(eth_prices, 30) if eth_prices else None
        
        # Get implied volatility data
        deribit_data = self.get_deribit_iv_data()
        binance_data = self.get_binance_options_data()
        
        # Get cross-asset data
        btc_data = self.get_btc_realized_volatility()
        vix = self.get_vix_data()
        move = self.get_move_index()
        
        # Get options flow
        flow_data = self.get_options_flow_data()
        
        # Compile all data
        market_data = {
            'timestamp': datetime.utcnow(),
            'eth_price': eth_price,
            'eth_rv_1d': eth_rv_1d,
            'eth_rv_7d': eth_rv_7d,
            'eth_rv_30d': eth_rv_30d,
            'vix': vix,
            'move_index': move,
            **deribit_data,
            **binance_data,
            **btc_data,
            **flow_data
        }
        
        logger.info(f"Data collection completed. ETH Price: ${eth_price}")
        return market_data
    
    def get_cached_data(self) -> Dict:
        """Get cached/demo data for development"""
        return {
            'timestamp': datetime.utcnow(),
            'eth_price': 3614.96,
            'eth_iv_deribit': 65.4,
            'eth_iv_binance': 65.0,
            'eth_rv_1d': 23.63,
            'eth_rv_7d': 23.48,
            'eth_rv_30d': 59.0,
            'btc_rv_7d': 11.37,
            'btc_rv_30d': 12.47,
            'vix': 17.73,
            'move_index': 89.20,
            'calls_bought': 20.8,
            'calls_sold': 26.4,
            'puts_bought': 32.5,
            'puts_sold': 24.8,
            'net_put_bias': 10.1
        }

