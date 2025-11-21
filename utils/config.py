"""
Configuration constants for Market Mood Monitor.
Contains API endpoints, design system variables, and application settings.
"""

COINGECKO_BASE_URL = "https://api.coingecko.com/api/v3"
FEAR_GREED_URL = "https://api.alternative.me/fng/"

COINGECKO_ENDPOINTS = {
    "global": f"{COINGECKO_BASE_URL}/global",
    "markets": f"{COINGECKO_BASE_URL}/coins/markets",
    "simple_price": f"{COINGECKO_BASE_URL}/simple/price",
}

API_TIMEOUT = 10
CACHE_TTL_SECONDS = 600
REFRESH_INTERVAL_SECONDS = 600

RISK_SCORE_WEIGHTS = {
    "fear_greed": 0.35,
    "btc_momentum": 0.25,
    "volume_health": 0.20,
    "market_breadth": 0.20,
}

COLOR_PALETTE = {
    "bg_primary": "#0d1117",
    "bg_secondary": "#161b22",
    "border_color": "#30363d",
    "text_primary": "#ffffff",
    "text_secondary": "#8b949e",
    "text_muted": "#6e7681",
    "success": "#10b981",
    "warning": "#eab308",
    "danger": "#ef4444",
    "info": "#3b82f6",
    "extreme_risk_off": "#ef4444",
    "risk_off": "#f97316",
    "neutral": "#eab308",
    "risk_on": "#10b981",
    "extreme_risk_on": "#22c55e",
}

RISK_SCORE_THRESHOLDS = [
    {"min": 0, "max": 30, "status": "Extreme Risk Off", "color": COLOR_PALETTE["extreme_risk_off"], "emoji": "🔴", "message": "Protect capital mode - Market showing extreme weakness"},
    {"min": 31, "max": 45, "status": "Risk Off", "color": COLOR_PALETTE["risk_off"], "emoji": "🟠", "message": "Cautious positioning - Defensive stance recommended"},
    {"min": 46, "max": 60, "status": "Neutral", "color": COLOR_PALETTE["neutral"], "emoji": "🟡", "message": "Wait for confirmation - No clear directional bias"},
    {"min": 61, "max": 80, "status": "Risk On", "color": COLOR_PALETTE["risk_on"], "emoji": "🟢", "message": "Constructive conditions - Market showing strength"},
    {"min": 81, "max": 100, "status": "Extreme Risk On", "color": COLOR_PALETTE["extreme_risk_on"], "emoji": "💚", "message": "Maximum exposure justified - Strong bullish momentum"},
]

MIN_MARKET_CAP_FOR_MOVERS = 100_000_000
TOP_MOVERS_COUNT = 8
