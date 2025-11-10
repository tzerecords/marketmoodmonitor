"""
Professional metrics cards: BTC Dominance, Market Cap, Altcoin Season, Volume.
Clean numbers with deltas, no charts.
"""
import streamlit as st
from typing import Dict, Any
from utils.helpers import format_large_number, format_percentage


def _calculate_altcoin_season(top_movers: Dict[str, Any], btc_change_24h: float) -> float:
    """
    Calculate Altcoin Season Index: % of top 50 coins outperforming BTC.
    
    Args:
        top_movers: Dict with 'gainers' and 'losers' lists
        btc_change_24h: Bitcoin 24h price change percentage
        
    Returns:
        Percentage of coins beating BTC (0-100)
    """
    if not top_movers or not isinstance(top_movers, dict):
        return 0.0
    
    # Combine gainers and losers into single list
    gainers = top_movers.get("gainers", [])
    losers = top_movers.get("losers", [])
    all_coins = gainers + losers
    
    if not all_coins:
        return 0.0
    
    # Count coins with better performance than BTC
    outperforming = sum(
        1 for coin in all_coins 
        if isinstance(coin, dict) and coin.get('price_change_24h', -999) > btc_change_24h
    )
    
    # Use min of actual count vs 50 for percentage
    total = min(len(all_coins), 50)
    return (outperforming / total * 100) if total > 0 else 0.0


def render_metrics_dashboard(market_data: Dict[str, Any]):
    """
    Render 4 professional metrics cards in tight layout.
    
    Args:
        market_data: Complete market data from fetcher
    """
    global_data = market_data.get("global_market", {})
    btc_data = market_data.get("bitcoin", {})
    top_movers = market_data.get("top_movers", [])
    
    # Extract values
    btc_dominance = global_data.get("btc_dominance", 0)
    total_mcap = global_data.get("total_market_cap_usd", 0)
    volume_24h = global_data.get("total_volume_24h_usd", 0)
    btc_change_24h = btc_data.get("price_change_24h", 0)
    
    # Calculate Altcoin Season Index
    altcoin_season = _calculate_altcoin_season(top_movers, btc_change_24h)
    
    # TODO: Get previous day values for delta calculation
    # For now, using dummy deltas (will implement with historical data)
    btc_dom_delta = 0.0
    mcap_delta = 0.0
    volume_delta = 0.0
    altcoin_delta = 0.0
    
    # Tight spacing: gap="medium" = 1rem
    col1, col2, col3, col4 = st.columns(4, gap="medium")
    
    with col1:
        delta_color = "#10b981" if btc_dom_delta > 0 else "#ef4444" if btc_dom_delta < 0 else "#6e7681"
        delta_sign = "+" if btc_dom_delta > 0 else ""
        
        st.markdown(
            f"""
            <div style="background: #0d1117; border: 1px solid #30363d; border-radius: 6px; padding: 1rem;">
                <div style="color: #8b949e; font-size: 0.8125rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.5rem;">
                    BTC DOMINANCE
                </div>
                <div style="color: #ffffff; font-size: 2rem; font-weight: 700; line-height: 1; margin-bottom: 0.25rem;">
                    {btc_dominance:.1f}%
                </div>
                <div style="color: {delta_color}; font-size: 1rem; font-weight: 500;">
                    {delta_sign}{btc_dom_delta:.2f}%
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col2:
        delta_color = "#10b981" if mcap_delta > 0 else "#ef4444" if mcap_delta < 0 else "#6e7681"
        delta_sign = "+" if mcap_delta > 0 else ""
        
        st.markdown(
            f"""
            <div style="background: #0d1117; border: 1px solid #30363d; border-radius: 6px; padding: 1rem;">
                <div style="color: #8b949e; font-size: 0.8125rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.5rem;">
                    TOTAL MARKET CAP
                </div>
                <div style="color: #ffffff; font-size: 2rem; font-weight: 700; line-height: 1; margin-bottom: 0.25rem;">
                    {format_large_number(total_mcap)}
                </div>
                <div style="color: {delta_color}; font-size: 1rem; font-weight: 500;">
                    {delta_sign}{mcap_delta:.2f}%
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col3:
        # Altcoin season: > 75% = bullish, < 25% = bearish
        delta_color = "#10b981" if altcoin_delta > 0 else "#ef4444" if altcoin_delta < 0 else "#6e7681"
        delta_sign = "+" if altcoin_delta > 0 else ""
        
        st.markdown(
            f"""
            <div style="background: #0d1117; border: 1px solid #30363d; border-radius: 6px; padding: 1rem;">
                <div style="color: #8b949e; font-size: 0.8125rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.5rem;">
                    ALTCOIN SEASON
                </div>
                <div style="color: #ffffff; font-size: 2rem; font-weight: 700; line-height: 1; margin-bottom: 0.25rem;">
                    {altcoin_season:.0f}%
                </div>
                <div style="color: {delta_color}; font-size: 1rem; font-weight: 500;">
                    {delta_sign}{altcoin_delta:.0f}% vs BTC
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col4:
        delta_color = "#10b981" if volume_delta > 0 else "#ef4444" if volume_delta < 0 else "#6e7681"
        delta_sign = "+" if volume_delta > 0 else ""
        
        st.markdown(
            f"""
            <div style="background: #0d1117; border: 1px solid #30363d; border-radius: 6px; padding: 1rem;">
                <div style="color: #8b949e; font-size: 0.8125rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.5rem;">
                    24H VOLUME
                </div>
                <div style="color: #ffffff; font-size: 2rem; font-weight: 700; line-height: 1; margin-bottom: 0.25rem;">
                    {format_large_number(volume_24h)}
                </div>
                <div style="color: {delta_color}; font-size: 1rem; font-weight: 500;">
                    {delta_sign}{volume_delta:.2f}%
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
