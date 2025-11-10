"""
Risk Score Thermometer component with asymmetric layout.
Gauge left (40%), Status + Historical Values right (60%).
"""
import streamlit as st
import plotly.graph_objects as go
from typing import Dict, Any, Optional
from datetime import datetime
from data.score_history import get_historical_values


def _render_history_grid_item(label: str, data: Optional[Dict[str, Any]]) -> str:
    """Render single history item as grid cell."""
    if not data:
        return f"""
        <div style="background: #0d1117; border: 1px solid #21262d; border-radius: 4px; padding: 0.75rem;">
            <div style="color: #8b949e; font-size: 0.75rem; margin-bottom: 0.25rem;">{label}</div>
            <div style="color: #6e7681; font-size: 0.875rem;">—</div>
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
    <div style="background: #0d1117; border: 1px solid #21262d; border-radius: 4px; padding: 0.75rem;">
        <div style="color: #8b949e; font-size: 0.75rem; margin-bottom: 0.25rem;">{label}</div>
        <div style="color: #ffffff; font-size: 1.125rem; font-weight: 700; margin-bottom: 0.125rem;">{score}</div>
        <div style="color: {color}; font-size: 0.75rem; font-weight: 500;">{status}</div>
    </div>
    """


def render_thermometer(risk_data: Dict[str, Any], last_updated: Optional[datetime] = None):
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
    
    # LEFT: Gauge with score badge below
    with col_gauge:
        # Gauge without number (clean arc only)
        fig = go.Figure(go.Indicator(
            mode="gauge",
            value=score,
            domain={'x': [0, 1], 'y': [0, 1]},
            gauge={
                'axis': {
                    'range': [0, 100],
                    'tickwidth': 1,
                    'tickcolor': "#21262d",
                    'tickmode': 'array',
                    'tickvals': [0, 25, 50, 75, 100],
                    'ticktext': ['0', '25', '50', '75', '100'],
                    'tickfont': {'size': 10, 'color': '#6e7681'}
                },
                'bar': {'color': color, 'thickness': 0.25},
                'bgcolor': "#161b22",
                'borderwidth': 1,
                'bordercolor': "#21262d",
                'steps': [
                    {'range': [0, 20], 'color': '#2d1a1a'},
                    {'range': [20, 40], 'color': '#2d2319'},
                    {'range': [40, 60], 'color': '#2d2a19'},
                    {'range': [60, 80], 'color': '#1a2d23'},
                    {'range': [80, 100], 'color': '#1a2d24'},
                ],
                'threshold': {
                    'line': {'color': color, 'width': 6},
                    'thickness': 0.9,
                    'value': score
                }
            }
        ))
        
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font={'color': "#ffffff", 'family': "-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"},
            height=240,
            margin=dict(l=10, r=10, t=10, b=10)
        )
        
        st.plotly_chart(fig, width='stretch', config={'displayModeBar': False})
        
        # Score badge below gauge
        st.markdown(
            f"""
            <div style="text-align: center; margin-top: -1rem;">
                <div style="display: inline-block; background: {color}; padding: 0.75rem 1.5rem; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.3);">
                    <span style="font-size: 2.5rem; color: #ffffff; font-weight: 700; line-height: 1;">
                        {score}
                    </span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    # RIGHT: Status + Historical Values
    with col_status:
        # Status section - Vertical layout: emoji → status → score → message
        st.markdown(
            f"""
            <div style="padding: 1rem 0; text-align: center;">
                <div style="font-size: 2.5rem; line-height: 1; margin-bottom: 0.75rem;">
                    {emoji}
                </div>
                <div style="display: inline-block; background: {color}1a; padding: 0.5rem 1.25rem; border-radius: 6px; margin-bottom: 0.75rem;">
                    <span style="font-size: 1.75rem; color: {color}; font-weight: 700; letter-spacing: 0.05em;">
                        {status}
                    </span>
                </div>
                <div style="font-size: 1.5rem; color: #ffffff; font-weight: 600; margin-bottom: 0.5rem;">
                    {score}
                </div>
                <div style="color: #8b949e; font-size: 1rem; line-height: 1.5;">
                    {message}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Historical Values section - 2x2 Grid with error handling
        try:
            now_html = _render_history_grid_item("Now", historical.get('now'))
            yesterday_html = _render_history_grid_item("Yesterday", historical.get('yesterday'))
            week_html = _render_history_grid_item("Last week", historical.get('last_week'))
            month_html = _render_history_grid_item("Last month", historical.get('last_month'))
            
            st.markdown(
                f"""
                <div style="margin-top: 1.5rem; padding: 0.75rem; background: #161b22; border: 1px solid #30363d; border-radius: 6px;">
                    <div style="color: #8b949e; font-size: 0.6875rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 0.75rem;">
                        HISTORICAL VALUES
                    </div>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.75rem;">
                        {now_html}
                        {yesterday_html}
                        {week_html}
                        {month_html}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
        except Exception:
            st.markdown(
                """
                <div style="margin-top: 1.5rem; padding: 0.75rem; background: #161b22; border: 1px solid #30363d; border-radius: 6px; text-align: center;">
                    <div style="color: #8b949e; font-size: 0.875rem; font-style: italic;">
                        Historical data aggregating, check back in 10 minutes
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
