"""
Risk Score calculation engine for Market Mood Monitor.
Implements weighted multi-factor model combining Fear & Greed, BTC momentum, volume health, and market breadth.
"""
from typing import Dict, Any, Optional
import logging
from datetime import datetime, timedelta

from utils.config import RISK_SCORE_WEIGHTS, RISK_SCORE_THRESHOLDS
from utils.helpers import normalize_to_100

logger = logging.getLogger(__name__)


class RiskScoreCalculator:
    """Calculates Market Mood risk score from market data components."""
    
    def __init__(self):
        self.historical_volumes: list = []
        self.historical_btc_prices: list = []
    
    def calculate_btc_momentum(self, btc_price: float, price_change_24h: float) -> float:
        """
        Calculate BTC momentum indicator using rate of change.
        For MVP, we use 24h change as proxy since we don't have historical MA data.
        
        Args:
            btc_price: Current BTC price
            price_change_24h: 24h price change percentage
            
        Returns:
            Normalized momentum score (0-100)
        """
        if price_change_24h > 10:
            momentum = 90
        elif price_change_24h > 5:
            momentum = 75
        elif price_change_24h > 2:
            momentum = 65
        elif price_change_24h > 0:
            momentum = 55
        elif price_change_24h > -2:
            momentum = 45
        elif price_change_24h > -5:
            momentum = 35
        elif price_change_24h > -10:
            momentum = 25
        else:
            momentum = 10
        
        logger.info(f"BTC momentum calculated: {momentum} (based on {price_change_24h:.2f}% change)")
        return momentum
    
    def calculate_volume_health(self, current_volume: float, market_data: Dict) -> float:
        """
        Calculate volume health metric.
        For MVP, we compare against a reasonable baseline.
        
        Args:
            current_volume: Current 24h volume
            market_data: Global market data
            
        Returns:
            Normalized volume health score (0-100)
        """
        total_market_cap = market_data.get("total_market_cap_usd", 1)
        volume_to_mcap_ratio = (current_volume / total_market_cap * 100) if total_market_cap > 0 else 0
        
        if volume_to_mcap_ratio > 8:
            volume_health = 95
        elif volume_to_mcap_ratio > 6:
            volume_health = 80
        elif volume_to_mcap_ratio > 4:
            volume_health = 65
        elif volume_to_mcap_ratio > 2:
            volume_health = 50
        else:
            volume_health = 35
        
        logger.info(f"Volume health calculated: {volume_health} (ratio: {volume_to_mcap_ratio:.2f}%)")
        return volume_health
    
    def get_risk_status(self, score: float) -> Dict[str, Any]:
        """
        Get risk status details based on score.
        
        Args:
            score: Risk score (0-100)
            
        Returns:
            Dict with status, color, emoji, and message
        """
        for threshold in RISK_SCORE_THRESHOLDS:
            if threshold["min"] <= score <= threshold["max"]:
                return {
                    "status": threshold["status"],
                    "color": threshold["color"],
                    "emoji": threshold["emoji"],
                    "message": threshold["message"],
                }
        
        return {
            "status": "Unknown",
            "color": "#808080",
            "emoji": "⚪",
            "message": "Unable to determine market status",
        }
    
    def calculate_risk_score(self, market_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate comprehensive risk score from all market data.
        
        Formula:
        Risk Score = (Fear & Greed × 35%) + (BTC Momentum × 25%) + 
                     (Volume Health × 20%) + (Market Breadth × 20%)
        
        Args:
            market_data: Complete market data from fetcher
            
        Returns:
            Dict with score, components, status, and metadata
        """
        try:
            fear_greed_data = market_data.get("fear_greed") or {}
            fear_greed_value = fear_greed_data.get("value", 50) if fear_greed_data else 50
            btc_data = market_data.get("bitcoin") or {}
            global_data = market_data.get("global_market") or {}
            market_breadth = market_data.get("market_breadth") if market_data.get("market_breadth") is not None else 50
            
            btc_momentum = self.calculate_btc_momentum(
                btc_data.get("price_usd", 0),
                btc_data.get("price_change_24h", 0)
            )
            
            volume_health = self.calculate_volume_health(
                global_data.get("total_volume_24h_usd", 0),
                global_data
            )
            
            components = {
                "fear_greed": fear_greed_value,
                "btc_momentum": btc_momentum,
                "volume_health": volume_health,
                "market_breadth": market_breadth,
            }
            
            risk_score = (
                components["fear_greed"] * RISK_SCORE_WEIGHTS["fear_greed"] +
                components["btc_momentum"] * RISK_SCORE_WEIGHTS["btc_momentum"] +
                components["volume_health"] * RISK_SCORE_WEIGHTS["volume_health"] +
                components["market_breadth"] * RISK_SCORE_WEIGHTS["market_breadth"]
            )
            
            risk_score = max(0, min(100, risk_score))
            
            status_info = self.get_risk_status(risk_score)
            
            result = {
                "score": round(risk_score, 1),
                "status": status_info["status"],
                "color": status_info["color"],
                "emoji": status_info["emoji"],
                "message": status_info["message"],
                "components": components,
                "weights": RISK_SCORE_WEIGHTS,
                "timestamp": market_data.get("timestamp", datetime.now()),
                "explanation_prompt": self._generate_explanation_prompt(risk_score, components),
            }
            
            logger.info(f"Risk Score calculated: {risk_score:.1f} - Status: {status_info['status']}")
            
            return result
            
        except Exception as e:
            logger.error(f"Error calculating risk score: {e}")
            return {
                "score": 50,
                "status": "Error",
                "color": "#808080",
                "emoji": "⚪",
                "message": "Unable to calculate risk score due to data issues",
                "components": {},
                "weights": RISK_SCORE_WEIGHTS,
                "timestamp": datetime.now(),
                "explanation_prompt": "",
            }
    
    def _generate_explanation_prompt(self, score: float, components: Dict[str, float]) -> str:
        """
        Generate explanation prompt for future AI integration (v2).
        
        Args:
            score: Calculated risk score
            components: Component values
            
        Returns:
            Formatted prompt string for AI explanation
        """
        return (
            f"Market Risk Score is {score:.1f}/100. "
            f"Fear & Greed: {components.get('fear_greed', 0)}, "
            f"BTC Momentum: {components.get('btc_momentum', 0)}, "
            f"Volume Health: {components.get('volume_health', 0)}, "
            f"Market Breadth: {components.get('market_breadth', 0)}%. "
            f"Explain market conditions in one sentence."
        )
