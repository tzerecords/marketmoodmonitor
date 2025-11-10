"""
Mini charts for market internals visualization.
"""
import streamlit as st
import plotly.graph_objects as go
from typing import Dict, Any, List
from datetime import datetime, timedelta


def render_breadth_chart(breadth_value: float):
    """
    Render market breadth bar chart showing % positive vs negative.
    
    Args:
        breadth_value: Percentage of coins with positive 24h performance
    """
    if breadth_value is None:
        breadth_value = 50.0
    
    positive_pct = breadth_value
    negative_pct = 100 - breadth_value
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=[positive_pct],
        y=['Market'],
        orientation='h',
        marker=dict(color='#10b981'),
        name='Positive',
        hovertemplate='<b>%{x:.1f}%</b> Positive<extra></extra>',
        showlegend=False
    ))
    
    fig.add_trace(go.Bar(
        x=[negative_pct],
        y=['Market'],
        orientation='h',
        marker=dict(color='#ef4444'),
        name='Negative',
        hovertemplate='<b>%{x:.1f}%</b> Negative<extra></extra>',
        showlegend=False
    ))
    
    fig.update_layout(
        barmode='stack',
        height=80,
        margin=dict(l=0, r=0, t=5, b=0),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(visible=False, range=[0, 100]),
        yaxis=dict(visible=False),
        showlegend=False
    )
    
    st.plotly_chart(fig, width='stretch', config={'displayModeBar': False})


def render_volume_trend_chart(volume_value: float):
    """
    Render volume trend mini area chart (synthetic for now).
    
    Args:
        volume_value: Current 24h volume in USD
    """
    hours = 24
    volumes = []
    base_volume = volume_value
    
    for i in range(hours):
        variance = (i / hours - 0.5) * 0.3
        volume = base_volume * (1 + variance)
        volumes.append(volume)
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        y=volumes,
        mode='lines',
        line=dict(color='#3b82f6', width=2),
        fill='tozeroy',
        fillcolor='rgba(59, 130, 246, 0.1)',
        hovertemplate='<b>$%{y:.2s}</b><extra></extra>',
        showlegend=False
    ))
    
    fig.update_layout(
        height=80,
        margin=dict(l=0, r=0, t=5, b=0),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        showlegend=False
    )
    
    st.plotly_chart(fig, width='stretch', config={'displayModeBar': False})


def render_btc_momentum_chart(btc_change_24h: float):
    """
    Render BTC momentum line chart (synthetic hourly data).
    
    Args:
        btc_change_24h: BTC 24h price change percentage
    """
    hours = 24
    changes = []
    current_change = 0
    
    for i in range(hours):
        progress = i / hours
        drift = (btc_change_24h - current_change) * 0.4
        noise = (i % 3 - 1) * 0.5
        current_change += drift + noise
        changes.append(current_change)
    
    changes.append(btc_change_24h)
    
    color = '#10b981' if btc_change_24h > 0 else '#ef4444'
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        y=changes,
        mode='lines',
        line=dict(color=color, width=2, shape='spline'),
        hovertemplate='<b>%{y:+.2f}%</b><extra></extra>',
        showlegend=False
    ))
    
    fig.update_layout(
        height=80,
        margin=dict(l=0, r=0, t=5, b=0),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(visible=False),
        yaxis=dict(visible=False, zeroline=True, zerolinecolor='#374151', zerolinewidth=1),
        showlegend=False
    )
    
    st.plotly_chart(fig, width='stretch', config={'displayModeBar': False})


def render_mini_charts_section(market_data: Dict[str, Any]):
    """
    Render all 3 mini charts in a row below metrics cards.
    
    Args:
        market_data: Complete market data from fetcher
    """
    st.markdown('<div style="margin: 2rem 0;">', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3, gap="large")
    
    with col1:
        st.markdown('<p style="color: #9ca3af; font-size: 0.8125rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.5rem;">MARKET BREADTH</p>', unsafe_allow_html=True)
        breadth = market_data.get("market_breadth") or 50.0
        render_breadth_chart(breadth)
        st.markdown(f'<p style="color: #ffffff; font-size: 0.875rem; margin-top: 0.25rem;">{breadth:.1f}% Positive</p>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<p style="color: #9ca3af; font-size: 0.8125rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.5rem;">24H VOLUME TREND</p>', unsafe_allow_html=True)
        global_data = market_data.get("global_market", {})
        volume = global_data.get("total_volume_24h_usd", 0)
        render_volume_trend_chart(volume)
        st.markdown(f'<p style="color: #ffffff; font-size: 0.875rem; margin-top: 0.25rem;">${volume/1e9:.1f}B Total</p>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<p style="color: #9ca3af; font-size: 0.8125rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.5rem;">BTC MOMENTUM 24H</p>', unsafe_allow_html=True)
        btc_data = market_data.get("bitcoin", {})
        btc_change = btc_data.get("price_change_24h", 0)
        render_btc_momentum_chart(btc_change)
        color = '#10b981' if btc_change > 0 else '#ef4444'
        arrow = '▲' if btc_change > 0 else '▼'
        st.markdown(f'<p style="color: {color}; font-size: 0.875rem; margin-top: 0.25rem;">{arrow} {btc_change:+.2f}%</p>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
