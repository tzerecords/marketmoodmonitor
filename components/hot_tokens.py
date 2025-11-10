"""
Hot Tokens component with separated gainers and losers sections.
"""
import streamlit as st
from typing import Dict, List, Any


def render_hot_tokens(movers_data: Dict[str, List[Dict]]):
    """
    Render separated gainers and losers sections side-by-side.
    
    Args:
        movers_data: Dict containing 'gainers' and 'losers' lists
    """
    if not movers_data:
        return
    
    gainers = movers_data.get("gainers", [])
    losers = movers_data.get("losers", [])
    
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        gainer_items = []
        for gainer in gainers[:5]:
            symbol = gainer.get("symbol", "").upper()
            change = gainer.get("price_change_24h", 0)
            gainer_items.append(f'<span style="color: #10b981; font-weight: 500;">{symbol} <span style="font-weight: 700;">+{change:.1f}%</span></span>')
        
        gainer_html = " ● ".join(gainer_items)
        
        st.markdown(
            f"""
            <div class="movers-section">
                <div class="movers-title" style="color: #10b981;">TOP GAINERS</div>
                <div class="movers-content">
                    {gainer_html}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col2:
        loser_items = []
        for loser in losers[:5]:
            symbol = loser.get("symbol", "").upper()
            change = loser.get("price_change_24h", 0)
            loser_items.append(f'<span style="color: #ef4444; font-weight: 500;">{symbol} <span style="font-weight: 700;">{change:.1f}%</span></span>')
        
        loser_html = " ● ".join(loser_items)
        
        st.markdown(
            f"""
            <div class="movers-section">
                <div class="movers-title" style="color: #ef4444;">TOP LOSERS</div>
                <div class="movers-content">
                    {loser_html}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
