"""
Risk Score Thermometer component with asymmetric layout.
Gauge left (40%), Status + Historical Values right (60%).
"""
import streamlit as st
import plotly.graph_objects as go
from typing import Dict, Any
from datetime import datetime
from data.score_history import get_historical_values


def _render_history_item(label: str, data: Dict[str, Any]) -> str:
    """Render single history item with colored badge."""
    if not data:
        return f"""
        <div style="display: flex; justify-content: space-between; align-items: center; padding: 0.5rem 0; border-bottom: 1px solid #21262d;">
            <span style="color: #8b949e; font-size: 0.8125rem;">{label}</span>
            <span style="color: #6e7681; font-size: 0.8125rem;">—</span>
        </div>
        """
    
    score = data['score']
    status = data['status']
    
    # Color based on status
    color_map = {
        'Extreme Risk Off': '#ef4444',
        'Risk Off': '#f97316',
        'Neutral': '#eab308',
        'Risk On': '#10b981',
        'Extreme Risk On': '#22c55e'
    }
    color = color_map.get(status, '#8b949e')
    
    return f"""
    <div style="display: flex; justify-content: space-between; align-items: center; padding: 0.5rem 0; border-bottom: 1px solid #21262d;">
        <span style="color: #c9d1d9; font-size: 0.8125rem;">{label}</span>
        <div style="display: flex; align-items: center; gap: 0.5rem;">
            <span style="color: {color}; font-weight: 500; font-size: 0.8125rem;">{status}</span>
            <span style="color: #ffffff; font-size: 1rem; font-weight: 700; background: {color}22; padding: 0.25rem 0.5rem; border-radius: 4px; min-width: 2.5rem; text-align: center;">
                {score}
            </span>
        </div>
    </div>
    """


def render_thermometer(risk_data: Dict[str, Any], last_updated: datetime = None):
    """
    Render asymmetric Risk Score thermometer.
    
    Args:
        risk_data: Risk score calculation results
        last_updated: Timestamp of last data fetch
    """
    score = risk_data.get("score", 50)
    status = risk_data.get("status", "Unknown")
    emoji = risk_data.get("emoji", "⚪")
    message = risk_data.get("message", "")
    color = risk_data.get("color", "#808080")
    
    # Calculate time since last update
    time_ago = ""
    if last_updated:
        delta = datetime.now() - last_updated
        minutes = int(delta.total_seconds() / 60)
        if minutes < 1:
            time_ago = "Just now"
        elif minutes == 1:
            time_ago = "1 min ago"
        else:
            time_ago = f"{minutes} min ago"
    
    # Get historical values
    historical = get_historical_values()
    
    # Create asymmetric layout
    col_gauge, col_status = st.columns([0.4, 0.6], gap="large")
    
    # LEFT: Gauge only
    with col_gauge:
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=score,
            domain={'x': [0, 1], 'y': [0, 1]},
            number={
                'font': {'size': 64, 'color': color},
                'suffix': ""
            },
            gauge={
                'axis': {
                    'range': [0, 100],
                    'tickwidth': 2,
                    'tickcolor': "#30363d",
                    'tickfont': {'size': 12, 'color': '#8b949e'}
                },
                'bar': {'color': color, 'thickness': 0.3},
                'bgcolor': "#0d1117",
                'borderwidth': 2,
                'bordercolor': "#30363d",
                'steps': [
                    {'range': [0, 30], 'color': 'rgba(239, 68, 68, 0.1)'},
                    {'range': [30, 45], 'color': 'rgba(249, 115, 22, 0.1)'},
                    {'range': [45, 60], 'color': 'rgba(234, 179, 8, 0.1)'},
                    {'range': [60, 80], 'color': 'rgba(16, 185, 129, 0.1)'},
                    {'range': [80, 100], 'color': 'rgba(34, 197, 94, 0.1)'},
                ],
                'threshold': {
                    'line': {'color': color, 'width': 4},
                    'thickness': 0.75,
                    'value': score
                }
            }
        ))
        
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font={'color': "#ffffff", 'family': "-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"},
            height=280,
            margin=dict(l=10, r=10, t=20, b=20)
        )
        
        st.plotly_chart(fig, width='stretch', config={'displayModeBar': False})
    
    # RIGHT: Status + Historical Values
    with col_status:
        # Status section
        st.markdown(
            f"""
            <div style="padding: 1rem 0;">
                <div style="font-size: 3rem; color: #ffffff; font-weight: 700; line-height: 1; margin-bottom: 0.5rem;">
                    {score} {emoji}
                </div>
                <div style="font-size: 2rem; color: {color}; font-weight: 600; margin-bottom: 0.75rem; letter-spacing: -0.02em;">
                    {status}
                </div>
                <div style="color: #8b949e; font-size: 1rem; line-height: 1.5; margin-bottom: 0.5rem;">
                    {message}
                </div>
                <div style="color: #6e7681; font-size: 0.8125rem; margin-top: 0.5rem;">
                    {f'Last updated: {time_ago}' if time_ago else ''}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Historical Values section
        st.markdown(
            f"""
            <div style="margin-top: 1.5rem; padding: 1rem; background: #161b22; border: 1px solid #30363d; border-radius: 6px;">
                <div style="color: #8b949e; font-size: 0.6875rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 0.75rem;">
                    HISTORICAL VALUES
                </div>
                {_render_history_item("Now", historical['now'])}
                {_render_history_item("Yesterday", historical['yesterday'])}
                {_render_history_item("Last week", historical['last_week'])}
                {_render_history_item("Last month", historical['last_month'])}
            </div>
            """,
            unsafe_allow_html=True
        )
