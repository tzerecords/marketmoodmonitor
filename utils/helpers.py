"""
Utility helper functions for Market Mood Monitor.
"""
from typing import Optional
import logging
from datetime import datetime, timedelta

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def format_large_number(num: float) -> str:
    """
    Format large numbers with B/M/K suffixes.
    
    Args:
        num: Number to format
        
    Returns:
        Formatted string (e.g., "1.5B", "234.5M")
    """
    if num >= 1_000_000_000:
        return f"${num / 1_000_000_000:.1f}B"
    elif num >= 1_000_000:
        return f"${num / 1_000_000:.1f}M"
    elif num >= 1_000:
        return f"${num / 1_000:.1f}K"
    else:
        return f"${num:.2f}"


def format_percentage(num: float, decimals: int = 1) -> str:
    """
    Format percentage with + or - sign.
    
    Args:
        num: Percentage value
        decimals: Decimal places
        
    Returns:
        Formatted percentage string (e.g., "+3.2%", "-1.5%")
    """
    sign = "+" if num > 0 else ""
    return f"{sign}{num:.{decimals}f}%"


def get_time_until_next_refresh(last_update: Optional[datetime], interval_seconds: int) -> str:
    """
    Calculate time remaining until next refresh.
    
    Args:
        last_update: Timestamp of last update
        interval_seconds: Refresh interval in seconds
        
    Returns:
        Formatted time string (e.g., "9m 32s")
    """
    if last_update is None:
        return "Updating..."
    
    now = datetime.now()
    next_update = last_update + timedelta(seconds=interval_seconds)
    time_diff = next_update - now
    
    if time_diff.total_seconds() <= 0:
        return "Updating..."
    
    minutes = int(time_diff.total_seconds() // 60)
    seconds = int(time_diff.total_seconds() % 60)
    
    return f"{minutes}m {seconds}s"


def normalize_to_100(value: float, min_val: float = 0, max_val: float = 100) -> float:
    """
    Normalize a value to 0-100 scale.
    
    Args:
        value: Value to normalize
        min_val: Minimum expected value
        max_val: Maximum expected value
        
    Returns:
        Normalized value capped at 0-100
    """
    normalized = ((value - min_val) / (max_val - min_val)) * 100
    return max(0, min(100, normalized))
