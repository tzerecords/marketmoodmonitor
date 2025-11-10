"""
Top Movers component with horizontal single-row layout and timeframe selector.
"""
import streamlit as st
from typing import Dict, List, Any


def render_hot_tokens(movers_data: Dict[str, List[Dict]], timeframe: str = "24H"):
    """
    Render top 3 gainers + top 3 losers in single horizontal row.
    
    Args:
        movers_data: Dict containing 'gainers' and 'losers' lists
        timeframe: Selected timeframe (24H, 7D, 30D)
    """
    if not movers_data:
        return
    
    gainers = movers_data.get("gainers", [])[:3]
    losers = movers_data.get("losers", [])[:3]
    
    # Build gainer tokens
    gainer_tokens = []
    for gainer in gainers:
        symbol = gainer.get("symbol", "").upper()
        change = gainer.get("price_change_24h", 0)
        gainer_tokens.append(
            f'<span style="color: #10b981; font-weight: 600;">{symbol} +{change:.1f}%</span>'
        )
    
    # Build loser tokens
    loser_tokens = []
    for loser in losers:
        symbol = loser.get("symbol", "").upper()
        change = loser.get("price_change_24h", 0)
        loser_tokens.append(
            f'<span style="color: #ef4444; font-weight: 600;">{symbol} {change:.1f}%</span>'
        )
    
    # Join with separators
    gainers_html = " | ".join(gainer_tokens) if gainer_tokens else "—"
    losers_html = " | ".join(loser_tokens) if loser_tokens else "—"
    
    # Header
    st.markdown(
        f"""
        <div style="margin-bottom: 0.75rem;">
            <span style="color: #8b949e; font-size: 0.8125rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.1em;">
                TOP MOVERS (24H)
            </span>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Single row with all tokens
    st.markdown(
        f"""
        <div style="background: #0d1117; border: 1px solid #30363d; border-radius: 6px; padding: 1rem;">
            <div style="color: #ffffff; font-size: 1rem; line-height: 1.5;">
                {gainers_html} <span style="color: #6e7681; font-weight: 700; margin: 0 0.5rem;">●</span> {losers_html}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
