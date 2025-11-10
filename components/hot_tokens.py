"""
Hot Tokens Ticker component with auto-scrolling animation.
"""
import streamlit as st
from typing import Dict, List, Any


def render_hot_tokens(movers_data: Dict[str, List[Dict]]):
    """
    Render auto-scrolling ticker with top gainers and losers.
    
    Args:
        movers_data: Dict containing 'gainers' and 'losers' lists
    """
    if not movers_data:
        return
    
    gainers = movers_data.get("gainers", [])
    losers = movers_data.get("losers", [])
    
    ticker_items = []
    
    for gainer in gainers:
        symbol = gainer.get("symbol", "")
        change = gainer.get("price_change_24h", 0)
        ticker_items.append(f'<span style="color: #10b981;">🔥 {symbol} +{change:.1f}%</span>')
    
    for loser in losers:
        symbol = loser.get("symbol", "")
        change = loser.get("price_change_24h", 0)
        ticker_items.append(f'<span style="color: #ef4444;">❄️ {symbol} {change:.1f}%</span>')
    
    ticker_html = " ● ".join(ticker_items)
    
    doubled_ticker = ticker_html + " ● " + ticker_html + " ● " + ticker_html
    
    st.markdown(
        f"""
        <div class="ticker-container">
            <div class="ticker-title">🔥 TOP MOVERS (24H)</div>
            <div class="ticker-wrapper">
                <div class="ticker-content">
                    {doubled_ticker}
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
