"""
API data fetcher for Market Mood Monitor.
Handles calls to CoinGecko and Alternative.me with error handling and caching.
"""
from typing import Dict, List, Optional, Any
import requests
from datetime import datetime
import logging
import time

from utils.config import (
    COINGECKO_ENDPOINTS,
    FEAR_GREED_URL,
    API_TIMEOUT,
    MIN_MARKET_CAP_FOR_MOVERS,
    TOP_MOVERS_COUNT,
)

logger = logging.getLogger(__name__)


class MarketDataFetcher:
    """Fetches market data from CoinGecko and Alternative.me APIs."""
    
    def __init__(self):
        self.session = requests.Session()
        self.cache: Dict[str, Any] = {}
        self.last_fetch_time: Optional[datetime] = None
    
    def _make_request(self, url: str, params: Optional[Dict] = None) -> Optional[Dict]:
        """
        Make HTTP request with error handling.
        
        Args:
            url: API endpoint URL
            params: Query parameters
            
        Returns:
            JSON response or None if error
        """
        try:
            logger.info(f"API call: {url}")
            response = self.session.get(url, params=params, timeout=API_TIMEOUT)
            response.raise_for_status()
            logger.info(f"API success: {url} - Status: {response.status_code}")
            time.sleep(0.5)
            return response.json()
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error for {url}: {e}")
            return None
        except requests.exceptions.Timeout:
            logger.warning(f"Timeout for {url}")
            return None
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error for {url}: {e}")
            return None
        except ValueError as e:
            logger.error(f"JSON decode error for {url}: {e}")
            return None
    
    def get_fear_greed_index(self) -> Optional[Dict]:
        """
        Get Fear & Greed Index with 7-day history.
        
        Returns:
            Dict with current value, classification, and historical data
        """
        data = self._make_request(FEAR_GREED_URL, params={"limit": 7})
        
        if not data or "data" not in data or len(data["data"]) == 0:
            logger.error("Invalid Fear & Greed response")
            return None
        
        current = data["data"][0]
        history = [int(item["value"]) for item in data["data"]]
        
        return {
            "value": int(current["value"]),
            "classification": current["value_classification"],
            "timestamp": current["timestamp"],
            "history_7d": history,
        }
    
    def get_global_market_data(self) -> Optional[Dict]:
        """
        Get global cryptocurrency market statistics.
        
        Returns:
            Dict with total market cap, volume, BTC dominance, etc.
        """
        data = self._make_request(COINGECKO_ENDPOINTS["global"])
        
        if not data or "data" not in data:
            logger.error("Invalid global market data response")
            return None
        
        global_data = data["data"]
        
        return {
            "total_market_cap_usd": global_data.get("total_market_cap", {}).get("usd", 0),
            "total_volume_24h_usd": global_data.get("total_volume", {}).get("usd", 0),
            "btc_dominance": global_data.get("market_cap_percentage", {}).get("btc", 0),
            "eth_dominance": global_data.get("market_cap_percentage", {}).get("eth", 0),
            "active_cryptocurrencies": global_data.get("active_cryptocurrencies", 0),
        }
    
    def get_bitcoin_data(self) -> Optional[Dict]:
        """
        Get Bitcoin price, volume, and 24h change.
        
        Returns:
            Dict with BTC price and market data
        """
        params = {
            "ids": "bitcoin",
            "vs_currencies": "usd",
            "include_24hr_vol": "true",
            "include_24hr_change": "true",
        }
        data = self._make_request(COINGECKO_ENDPOINTS["simple_price"], params=params)
        
        if not data or "bitcoin" not in data:
            logger.error("Invalid Bitcoin data response")
            return None
        
        btc_data = data["bitcoin"]
        
        return {
            "price_usd": btc_data.get("usd", 0),
            "volume_24h_usd": btc_data.get("usd_24h_vol", 0),
            "price_change_24h": btc_data.get("usd_24h_change", 0),
        }
    
    def get_top_movers(self) -> Optional[Dict[str, List[Dict]]]:
        """
        Get top gainers and losers (>100M market cap).
        
        Returns:
            Dict with 'gainers' and 'losers' lists
        """
        params = {
            "vs_currency": "usd",
            "order": "market_cap_desc",
            "per_page": 100,
            "page": 1,
            "sparkline": "false",
            "price_change_percentage": "24h",
        }
        data = self._make_request(COINGECKO_ENDPOINTS["markets"], params=params)
        
        if not data or not isinstance(data, list):
            logger.error("Invalid top movers response")
            return None
        
        filtered_coins = [
            coin for coin in data
            if coin.get("market_cap", 0) >= MIN_MARKET_CAP_FOR_MOVERS
            and coin.get("price_change_percentage_24h") is not None
        ]
        
        sorted_by_change = sorted(
            filtered_coins,
            key=lambda x: x.get("price_change_percentage_24h", 0),
            reverse=True
        )
        
        gainers = sorted_by_change[:TOP_MOVERS_COUNT // 2]
        losers = sorted_by_change[-TOP_MOVERS_COUNT // 2:]
        
        format_coin = lambda c: {
            "symbol": c.get("symbol", "").upper(),
            "name": c.get("name", ""),
            "price_change_24h": c.get("price_change_percentage_24h", 0),
        }
        
        return {
            "gainers": [format_coin(c) for c in gainers],
            "losers": [format_coin(c) for c in losers],
        }
    
    def get_market_breadth(self) -> Optional[float]:
        """
        Calculate market breadth: % of top 100 coins with positive 24h change.
        
        Returns:
            Percentage (0-100) of coins in the green
        """
        params = {
            "vs_currency": "usd",
            "order": "market_cap_desc",
            "per_page": 100,
            "page": 1,
            "sparkline": "false",
            "price_change_percentage": "24h",
        }
        data = self._make_request(COINGECKO_ENDPOINTS["markets"], params=params)
        
        if not data or not isinstance(data, list):
            logger.error("Invalid market breadth response")
            return None
        
        positive_count = sum(
            1 for coin in data
            if coin.get("price_change_percentage_24h") is not None and coin.get("price_change_percentage_24h") > 0
        )
        
        total_count = len(data)
        breadth_percentage = (positive_count / total_count * 100) if total_count > 0 else 0
        
        logger.info(f"Market breadth: {breadth_percentage:.1f}% ({positive_count}/{total_count} coins positive)")
        
        return breadth_percentage
    
    def fetch_all_data(self) -> Dict[str, Any]:
        """
        Fetch all market data from APIs.
        
        Returns:
            Dict containing all market data or cached fallback
        """
        logger.info("Starting full market data fetch...")
        
        results = {
            "fear_greed": self.get_fear_greed_index(),
            "global_market": self.get_global_market_data(),
            "bitcoin": self.get_bitcoin_data(),
            "top_movers": self.get_top_movers(),
            "market_breadth": self.get_market_breadth(),
            "timestamp": datetime.now(),
        }
        
        if all([results["fear_greed"], results["global_market"], results["bitcoin"], results["market_breadth"]]):
            self.cache = results
            self.last_fetch_time = datetime.now()
            logger.info("Successfully fetched all market data")
        else:
            logger.warning("Some API calls failed, using cached data if available")
            if self.cache:
                results = self.cache
        
        return results
