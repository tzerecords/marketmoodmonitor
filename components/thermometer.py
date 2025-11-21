"""
Risk Score Thermometer component - Hero gauge centered layout.
Large 340px gauge with score inside, status badge below, historical timeline to the right.
"""
import streamlit as st
import plotly.graph_objects as go
from typing import Dict, Any, Optional
from datetime import datetime
from data.score_history import get_historical_values


def render_thermometer(risk_data: Dict[str, Any], last_updated: Optional[datetime] = None):
    """
    Render hero Risk Score thermometer with centered gauge.
    
    Design specs:
    - Gauge: 340px diameter, smooth gradient red→yellow→green
    - Score: 48px bold inside ring
    - Status badge: 14px compact below gauge
    - Subtle glow effect
    
    Args:
        risk_data: Risk score calculation results
        last_updated: Timestamp of last data fetch
    """
    score = risk_data.get("score", 50)
    status = risk_data.get("status", "Unknown")
    emoji = risk_data.get("emoji", "⚪")
    message = risk_data.get("message", "")
    color = risk_data.get("color", "#808080")
    
    # Helper function to convert hex to rgba
    def hex_to_rgba(hex_color: str, alpha: float) -> str:
        """Convert hex color to rgba with specified alpha."""
        hex_color = hex_color.lstrip('#')
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        return f'rgba({r}, {g}, {b}, {alpha})'
    
    # Create Plotly gauge with smooth gradient
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        number={
            'font': {
                'size': 48,
                'color': '#ffffff',
                'family': 'system-ui, -apple-system, BlinkMacSystemFont, sans-serif',
                'weight': 700
            },
            'suffix': ''
        },
        domain={'x': [0, 1], 'y': [0, 1]},
        gauge={
            'axis': {
                'range': [0, 100],
                'tickwidth': 1,
                'tickcolor': "#30363d",
                'tickmode': 'array',
                'tickvals': [0, 25, 50, 75, 100],
                'ticktext': ['0', '25', '50', '75', '100'],
                'tickfont': {'size': 12, 'color': '#8b949e'}
            },
            'bar': {
                'color': color,
                'thickness': 0.15,
                'line': {'width': 0}
            },
            'bgcolor': "#161b22",
            'borderwidth': 2,
            'bordercolor': "#30363d",
            'steps': [
                {'range': [0, 20], 'color': hex_to_rgba('#ef4444', 0.15)},    # Red zone
                {'range': [20, 40], 'color': hex_to_rgba('#f97316', 0.12)},   # Orange zone
                {'range': [40, 60], 'color': hex_to_rgba('#eab308', 0.10)},   # Yellow zone
                {'range': [60, 80], 'color': hex_to_rgba('#10b981', 0.12)},   # Green zone
                {'range': [80, 100], 'color': hex_to_rgba('#22c55e', 0.15)},  # Bright green
            ],
            'threshold': {
                'line': {'color': color, 'width': 3},
                'thickness': 0.75,
                'value': score
            }
        }
    ))
    
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={'color': "#ffffff", 'family': "system-ui, -apple-system, BlinkMacSystemFont, sans-serif"},
        height=340,
        margin=dict(l=20, r=20, t=30, b=20)
    )
    
    st.plotly_chart(fig, width='stretch', config={'displayModeBar': False})
    
    # Status badge below gauge - compact design (14px)
    st.markdown(
        f"""
        <div style="text-align: center; margin-top: 8px;">
            <div style="display: inline-flex; align-items: center; gap: 8px; background: {hex_to_rgba(color, 0.12)}; border: 1px solid {hex_to_rgba(color, 0.3)}; border-radius: 6px; padding: 8px 16px;">
                <span style="color: {color}; font-size: 14px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em;">
                    {status}
                </span>
                <span style="font-size: 14px;">{emoji}</span>
            </div>
        </div>
        <div style="text-align: center; color: #8b949e; font-size: 12px; margin-top: 8px; max-width: 400px; margin-left: auto; margin-right: auto;">
            {message}
        </div>
        """,
        unsafe_allow_html=True
    )


def render_historical_timeline(risk_data: Dict[str, Any]):
    """
    Render historical values as vertical timeline.
    
    Design specs:
    - Width: 300px fixed
    - Score circles: 56px diameter
    - Labels to the right
    - 12px spacing between rows
    - Color-coded by status
    
    Args:
        risk_data: Current risk score data (for color reference)
    """
    # Get historical values
    historical = get_historical_values()
    
    # Color map
    color_map = {
        'Extreme Risk Off': '#ef4444',
        'Risk Off': '#f97316', 
        'Neutral': '#eab308',
        'Risk On': '#10b981',
        'Extreme Risk On': '#22c55e'
    }
    
    # Historical items
    historical_items = [
        ("Now", historical.get('now')),
        ("Yesterday", historical.get('yesterday')),
        ("Last week", historical.get('last_week')),
        ("Last month", historical.get('last_month'))
    ]
    
    # Container
    st.markdown(
        """
        <div style="background: #1a2332; border: 1px solid #2d3b4d; border-radius: 8px; padding: 20px;">
            <div style="color: #7a8ba0; font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 16px;">
                Historical Values
            </div>
        """,
        unsafe_allow_html=True
    )
    
    # Timeline rows
    for i, (label, data) in enumerate(historical_items):
        margin_bottom = "12px" if i < len(historical_items) - 1 else "0"
        
        if data and data.get('score') is not None:
            score = data['score']
            status = data['status']
            status_color = color_map.get(status, '#f97316')
            
            st.markdown(
                f"""
                <div style="display: flex; align-items: center; gap: 12px; margin-bottom: {margin_bottom};">
                    <div style="background: {status_color}; border-radius: 50%; width: 56px; height: 56px; display: flex; align-items: center; justify-content: center; flex-shrink: 0; box-shadow: 0 2px 8px rgba(0,0,0,0.3);">
                        <span style="color: white; font-size: 18px; font-weight: 700;">{int(score)}</span>
                    </div>
                    <div style="flex: 1;">
                        <div style="color: #c9d1d9; font-size: 13px; font-weight: 600; margin-bottom: 2px;">{label}</div>
                        <div style="color: {status_color}; font-size: 11px; font-weight: 600;">{status}</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"""
                <div style="display: flex; align-items: center; gap: 12px; margin-bottom: {margin_bottom};">
                    <div style="background: rgba(139, 148, 158, 0.2); border: 1px dashed #30363d; border-radius: 50%; width: 56px; height: 56px; display: flex; align-items: center; justify-content: center; flex-shrink: 0;">
                        <span style="color: #8b949e; font-size: 18px; font-weight: 600;">—</span>
                    </div>
                    <div style="flex: 1;">
                        <div style="color: #8b949e; font-size: 13px; font-weight: 500; margin-bottom: 2px;">{label}</div>
                        <div style="color: #6e7681; font-size: 11px; font-style: italic;">Collecting data</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
    
    st.markdown('</div>', unsafe_allow_html=True)
