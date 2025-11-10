"""
Risk Score Thermometer component with asymmetric layout.
Gauge left (40%), Status + Historical Values right (60%).
"""
import streamlit as st
import plotly.graph_objects as go
from typing import Dict, Any, Optional
from datetime import datetime
from data.score_history import get_historical_values


def _validate_html_tags(html: str) -> bool:
    """Validate HTML tags are balanced."""
    try:
        opening = html.count('<div')
        closing = html.count('</div>')
        return opening == closing
    except Exception:
        return False


def _render_history_row(label: str, data: Optional[Dict[str, Any]]) -> str:
    """Render single history item as vertical row (Fear & Greed style)."""
    if not data:
        return f"""
        <div style="display: flex; justify-content: space-between; align-items: center; padding: 0.5rem 0; border-bottom: 1px solid #21262d;">
            <span style="color: #8b949e; font-size: 0.875rem;">{label}</span>
            <span style="color: #6e7681; font-size: 0.875rem;">—</span>
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
    <div style="display: flex; justify-content: space-between; align-items: center; padding: 0.75rem 0; border-bottom: 1px solid #21262d;">
        <div>
            <span style="color: #8b949e; font-size: 0.875rem; margin-right: 0.5rem;">{label}</span>
            <span style="color: {color}; font-size: 0.875rem; font-weight: 600;">{status}</span>
        </div>
        <div style="background: {color}; color: #ffffff; font-size: 0.875rem; font-weight: 700; padding: 0.25rem 0.75rem; border-radius: 50px;">
            {score}
        </div>
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
    
    # Get historical values
    historical = get_historical_values()
    
    # Create asymmetric layout
    col_gauge, col_status = st.columns([0.4, 0.6], gap="large")
    
    # LEFT: Gauge with pointer/needle
    with col_gauge:
        # Gauge with gray pointer/needle (Fear & Greed style)
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
                'bar': {'color': 'rgba(0,0,0,0)', 'thickness': 0},  # Hide bar, show only pointer
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
                    'line': {'color': '#8b949e', 'width': 4},  # Gray pointer/needle
                    'thickness': 0.75,
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
        
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        
        # Score badge below gauge with subtle pulse animation
        st.markdown(
            f"""
            <style>
                @keyframes scorePulse {{
                    0%, 100% {{
                        box-shadow: 0 2px 8px rgba(0,0,0,0.3);
                        transform: scale(1);
                    }}
                    50% {{
                        box-shadow: 0 4px 16px rgba(0,0,0,0.4);
                        transform: scale(1.02);
                    }}
                }}
            </style>
            <div style="text-align: center; margin-top: -1rem;">
                <div style="display: inline-block; background: {color}; padding: 0.75rem 1.5rem; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.3); animation: scorePulse 2s ease-in-out infinite;">
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
        # Status section - HORIZONTAL COMPACT (Fear & Greed style)
        # "Now: Fear" layout - emoji inline + status dominant with fade-in animation
        status_html = f"""
        <style>
            @keyframes fadeIn {{
                from {{ opacity: 0; }}
                to {{ opacity: 1; }}
            }}
        </style>
        <div style="padding: 1rem 0; animation: fadeIn 0.5s ease-out;">
            <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem;">
                <span style="font-size: 2rem; line-height: 1;">{emoji}</span>
                <div style="background: {color}1a; padding: 0.5rem 1.5rem; border-radius: 6px; border: 1px solid {color}40;">
                    <span style="font-size: 2.5rem; color: {color}; font-weight: 700; letter-spacing: 0.05em; line-height: 1;">
                        {status}
                    </span>
                </div>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 2rem; color: #ffffff; font-weight: 700; margin-bottom: 0.5rem;">
                    {score}
                </div>
                <div style="color: #8b949e; font-size: 1rem; line-height: 1.5;">
                    {message}
                </div>
            </div>
        </div>
        """
        
        # Validate HTML before rendering
        if _validate_html_tags(status_html):
            st.markdown(status_html, unsafe_allow_html=True)
        else:
            st.error("Status rendering error - please refresh")
        
        # Historical Values section - SINGLE COLUMN VERTICAL (Fear & Greed style)
        try:
            now_row = _render_history_row("Now", historical.get('now'))
            yesterday_row = _render_history_row("Yesterday", historical.get('yesterday'))
            week_row = _render_history_row("Last week", historical.get('last_week'))
            month_row = _render_history_row("Last month", historical.get('last_month'))
            
            historical_html = f"""
            <style>
                @keyframes slideInUp {{
                    from {{
                        opacity: 0;
                        transform: translateY(10px);
                    }}
                    to {{
                        opacity: 1;
                        transform: translateY(0);
                    }}
                }}
            </style>
            <div style="margin-top: 1.5rem; padding: 0.75rem; background: #161b22; border: 1px solid #30363d; border-radius: 6px; animation: slideInUp 0.4s ease-out;">
                <div style="color: #8b949e; font-size: 0.6875rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 0.75rem;">
                    HISTORICAL VALUES
                </div>
                <div style="display: flex; flex-direction: column;">
                    {now_row}
                    {yesterday_row}
                    {week_row}
                    {month_row}
                </div>
            </div>
            """
            
            # Validate HTML before rendering
            if _validate_html_tags(historical_html):
                st.markdown(historical_html, unsafe_allow_html=True)
            else:
                raise ValueError("HTML validation failed")
                
        except Exception as e:
            st.markdown(
                """
                <div style="margin-top: 1.5rem; padding: 0.75rem; background: #161b22; border: 1px solid #30363d; border-radius: 6px; text-align: center;">
                    <div style="color: #8b949e; font-size: 0.875rem; font-style: italic;">
                        Historical data loading, please wait...
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
