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
    global_data = market_data.get("global_market") or {}
    btc_data = market_data.get("bitcoin") or {}
    top_movers = market_data.get("top_movers") or []
    
    # Extract values
    btc_dominance = global_data.get("btc_dominance", 0)
    total_mcap = global_data.get("total_market_cap_usd", 0)
    volume_24h = global_data.get("total_volume_24h_usd", 0)
    btc_change_24h = btc_data.get("price_change_24h", 0)
    
    # Calculate Altcoin Season Index
    altcoin_season = _calculate_altcoin_season(top_movers, btc_change_24h)
    
    # Tight spacing: gap="medium" = 1rem
    col1, col2, col3, col4 = st.columns(4, gap="medium")
    
    with col1:
        st.markdown(
            f"""
            <div style="background: #0d1117; border: 1px solid #30363d; border-radius: 6px; padding: 1rem;">
                <div style="color: #8b949e; font-size: 0.8125rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.5rem; cursor: help;" title="Bitcoin market cap as percentage of total crypto market">
                    BTC DOMINANCE ⓘ
                </div>
                <div style="color: #ffffff; font-size: 2rem; font-weight: 700; line-height: 1;">
                    {btc_dominance:.1f}%
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col2:
        # Format as Trillions if > 1000B
        if total_mcap > 1_000_000_000_000:
            mcap_display = f"${total_mcap / 1_000_000_000_000:.1f}T"
        elif total_mcap > 1_000_000_000:
            mcap_display = f"${total_mcap / 1_000_000_000:.1f}B"
        else:
            mcap_display = format_large_number(total_mcap)
        
        st.markdown(
            f"""
            <div style="background: #0d1117; border: 1px solid #30363d; border-radius: 6px; padding: 1rem;">
                <div style="color: #8b949e; font-size: 0.8125rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.5rem; cursor: help;" title="Combined market capitalization of all cryptocurrencies">
                    TOTAL MARKET CAP ⓘ
                </div>
                <div style="color: #ffffff; font-size: 2rem; font-weight: 700; line-height: 1;">
                    {mcap_display}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col3:
        st.markdown(
            f"""
            <div style="background: #0d1117; border: 1px solid #30363d; border-radius: 6px; padding: 1rem;">
                <div style="color: #8b949e; font-size: 0.8125rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.5rem; cursor: help;" title="Percentage of top 50 coins outperforming BTC in 24h">
                    ALTCOIN SEASON ⓘ
                </div>
                <div style="color: #ffffff; font-size: 2rem; font-weight: 700; line-height: 1;">
                    {altcoin_season:.0f}%
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col4:
        st.markdown(
            f"""
            <div style="background: #0d1117; border: 1px solid #30363d; border-radius: 6px; padding: 1rem;">
                <div style="color: #8b949e; font-size: 0.8125rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.5rem; cursor: help;" title="Total trading volume across all crypto markets in last 24 hours">
                    24H VOLUME ⓘ
                </div>
                <div style="color: #ffffff; font-size: 2rem; font-weight: 700; line-height: 1;">
                    {format_large_number(volume_24h)}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
