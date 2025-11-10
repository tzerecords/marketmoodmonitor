"""
Key Metrics Dashboard with 4 cards: Fear & Greed, BTC Trend, Volume, Dominance.
"""
import streamlit as st
import plotly.graph_objects as go
from typing import Dict, Any

from utils.helpers import format_large_number, format_percentage


def render_fear_greed_card(fear_greed_data: Dict[str, Any]):
    """Render Fear & Greed Index card with mini gauge and 7d history."""
    if not fear_greed_data:
        st.warning("Fear & Greed data unavailable")
        return
    
    value = fear_greed_data.get("value", 50)
    classification = fear_greed_data.get("classification", "Neutral")
    history = fear_greed_data.get("history_7d", [])
    
    color = "#ef4444" if value < 40 else "#eab308" if value < 60 else "#10b981"
    
    with st.container():
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">Fear & Greed Index</div>
                <div class="metric-value" style="color: {color};">{value}</div>
                <div class="metric-label">{classification}</div>
            </div>
            """,
            unsafe_allow_html=True
        )


def render_btc_trend_card(btc_data: Dict[str, Any]):
    """Render Bitcoin trend card with price and 24h change."""
    if not btc_data:
        st.warning("Bitcoin data unavailable")
        return
    
    price = btc_data.get("price_usd", 0)
    change_24h = btc_data.get("price_change_24h", 0)
    
    color = "#10b981" if change_24h > 0 else "#ef4444"
    arrow = "▲" if change_24h > 0 else "▼"
    
    with st.container():
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">Bitcoin Trend</div>
                <div class="metric-value">${price:,.0f}</div>
                <div class="metric-label" style="color: {color};">
                    {arrow} {format_percentage(change_24h)}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


def render_volume_card(global_data: Dict[str, Any]):
    """Render 24h volume card."""
    if not global_data:
        st.warning("Volume data unavailable")
        return
    
    volume = global_data.get("total_volume_24h_usd", 0)
    volume_formatted = format_large_number(volume)
    
    with st.container():
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">24h Volume</div>
                <div class="metric-value">{volume_formatted}</div>
                <div class="metric-label">Total Market</div>
            </div>
            """,
            unsafe_allow_html=True
        )


def render_dominance_card(global_data: Dict[str, Any]):
    """Render market dominance card with BTC and ETH percentages."""
    if not global_data:
        st.warning("Dominance data unavailable")
        return
    
    btc_dom = global_data.get("btc_dominance", 0)
    eth_dom = global_data.get("eth_dominance", 0)
    
    with st.container():
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">Market Dominance</div>
                <div class="metric-value">{btc_dom:.1f}%</div>
                <div class="metric-label">Bitcoin</div>
            </div>
            """,
            unsafe_allow_html=True
        )


def render_metrics_dashboard(market_data: Dict[str, Any]):
    """
    Render complete 4-card metrics dashboard.
    
    Args:
        market_data: Complete market data from fetcher
    """
    st.markdown('<div class="metrics-section">', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4, gap="large")
    
    with col1:
        render_fear_greed_card(market_data.get("fear_greed"))
    
    with col2:
        render_btc_trend_card(market_data.get("bitcoin"))
    
    with col3:
        render_volume_card(market_data.get("global_market"))
    
    with col4:
        render_dominance_card(market_data.get("global_market"))
    
    st.markdown('</div>', unsafe_allow_html=True)
