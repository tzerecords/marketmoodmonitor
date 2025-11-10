"""
Score history persistence module.
Stores risk score snapshots for historical analysis.
"""
import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional

HISTORY_FILE = Path("data/score_history.json")
MAX_HISTORY_DAYS = 90


def load_history() -> List[Dict[str, Any]]:
    """Load score history from JSON file."""
    if not HISTORY_FILE.exists():
        return []
    
    try:
        with open(HISTORY_FILE, 'r') as f:
            data = json.load(f)
            return data.get('history', [])
    except (json.JSONDecodeError, IOError):
        return []


def save_score(score: float, status: str, message: str):
    """
    Append new score to history and cleanup old entries.
    
    Args:
        score: Risk score value (0-100)
        status: Risk status text (e.g. "Fear", "Greed")
        message: Status message
    """
    history = load_history()
    
    # Add new entry
    entry = {
        "timestamp": datetime.now().isoformat(),
        "score": round(score, 1),
        "status": status,
        "message": message
    }
    history.append(entry)
    
    # Cleanup entries older than MAX_HISTORY_DAYS
    cutoff_date = datetime.now() - timedelta(days=MAX_HISTORY_DAYS)
    history = [
        h for h in history 
        if datetime.fromisoformat(h['timestamp']) > cutoff_date
    ]
    
    # Save back to file
    HISTORY_FILE.parent.mkdir(exist_ok=True)
    with open(HISTORY_FILE, 'w') as f:
        json.dump({'history': history}, f, indent=2)


def get_historical_values() -> Dict[str, Optional[Dict[str, Any]]]:
    """
    Get key historical score values.
    
    Returns:
        Dict with keys: now, yesterday, last_week, last_month
    """
    history = load_history()
    
    if not history:
        return {
            'now': None,
            'yesterday': None,
            'last_week': None,
            'last_month': None
        }
    
    now = datetime.now()
    
    # Get latest (now)
    latest = history[-1] if history else None
    
    # Find closest to 24h ago
    yesterday = None
    if len(history) > 1:
        target_yesterday = now - timedelta(days=1)
        yesterday = min(
            history,
            key=lambda h: abs(datetime.fromisoformat(h['timestamp']) - target_yesterday)
        )
    
    # Find closest to 7d ago
    last_week = None
    if len(history) > 1:
        target_week = now - timedelta(days=7)
        last_week = min(
            history,
            key=lambda h: abs(datetime.fromisoformat(h['timestamp']) - target_week)
        )
    
    # Find closest to 30d ago
    last_month = None
    if len(history) > 1:
        target_month = now - timedelta(days=30)
        last_month = min(
            history,
            key=lambda h: abs(datetime.fromisoformat(h['timestamp']) - target_month)
        )
    
    return {
        'now': latest,
        'yesterday': yesterday,
        'last_week': last_week,
        'last_month': last_month
    }
