"""
Risk Score Thermometer - Hero gauge centered design.
Gauge with visible gradient, score inside, badge below.
"""
import streamlit as st
import plotly.graph_objects as go
from typing import Dict, Any, Optional
from datetime import datetime
from data.score_history import get_historical_values


def render_thermometer(risk_data: Dict[str, Any], last_updated: Optional[datetime] = None):
    """
    Render hero thermometer gauge (360px) with score inside and badge below.
    
    Design specs:
    - Gauge: 360px, circular with visible red→yellow→green gradient
    - Score: Large number centered inside gauge
    - Gradient: Red (0-20), Orange (20-40), Yellow (40-60), Light green (60-80), Green (80-100)
    - Glow on current indicator
    - Badge: Compact pill BELOW gauge (not beside)
    
    Args:
        risk_data: Risk score calculation results
        last_updated: Timestamp of last data fetch
    """
    score = risk_data.get("score", 50)
    status = risk_data.get("status", "Unknown")
    emoji = risk_data.get("emoji", "⚪")
    message = risk_data.get("message", "")
    color = risk_data.get("color", "#808080")
    
    # Helper for rgba colors
    def hex_to_rgba(hex_color: str, alpha: float) -> str:
        hex_color = hex_color.lstrip('#')
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        return f'rgba({r}, {g}, {b}, {alpha})'
    
    # Create Plotly gauge with VISIBLE gradient zones
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        number={
            'font': {
                'size': 56,  # Large score inside gauge
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
                'tickwidth': 2,
                'tickcolor': "#30363d",
                'tickmode': 'array',
                'tickvals': [0, 25, 50, 75, 100],
                'ticktext': ['0', '25', '50', '75', '100'],
                'tickfont': {'size': 13, 'color': '#8b949e', 'weight': 600}
            },
            'bar': {
                'color': color,  # Current indicator with color
                'thickness': 0.2,
                'line': {'width': 0}
            },
            'bgcolor': "#0d1117",
            'borderwidth': 3,
            'bordercolor': "#30363d",
            # VISIBLE gradient steps (not subtle, VISIBLE)
            'steps': [
                {'range': [0, 20], 'color': '#ef4444'},      # Red
                {'range': [20, 40], 'color': '#f97316'},    # Orange
                {'range': [40, 60], 'color': '#eab308'},    # Yellow
                {'range': [60, 80], 'color': '#84cc16'},    # Light green
                {'range': [80, 100], 'color': '#22c55e'},   # Green
            ],
            'threshold': {
                'line': {
                    'color': color,
                    'width': 5  # Thicker indicator with glow effect
                },
                'thickness': 0.85,
                'value': score
            }
        }
    ))
    
    # Add glow effect at indicator position using scatter marker
    # Calculate position on gauge arc (gauge is semicircle, radius ~0.4 in relative coords)
    import math
    angle_deg = 180 - (score * 1.8)  # 0→180°, 100→0°
    angle_rad = math.radians(angle_deg)
    radius = 0.85  # Position on outer arc
    
    # Convert polar to cartesian (center at 0.5, 0.3)
    glow_x = 0.5 + radius * math.cos(angle_rad)
    glow_y = 0.3 + radius * math.sin(angle_rad)
    
    # Add glow marker at indicator position
    fig.add_trace(go.Scatter(
        x=[glow_x],
        y=[glow_y],
        mode='markers',
        marker=dict(
            size=25,
            color=color,
            opacity=0.6,
            line=dict(color=color, width=10),
            symbol='circle'
        ),
        showlegend=False,
        hoverinfo='skip'
    ))
    
    # Layout with fixed size
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={
            'color': "#ffffff",
            'family': "system-ui, -apple-system, BlinkMacSystemFont, sans-serif"
        },
        width=360,   # FIXED width
        height=360,  # FIXED height (square)
        margin=dict(l=20, r=20, t=30, b=20)
    )
    
    # Render gauge with FIXED width in centered container
    st.markdown(
        """
        <div style="display: flex; justify-content: center; align-items: center;">
        """,
        unsafe_allow_html=True
    )
    st.plotly_chart(fig, width='content', config={'displayModeBar': False})
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Badge BELOW gauge (compact red pill)
    st.markdown(
        f"""
        <div style="text-align: center; margin-top: 12px;">
            <div style="
                display: inline-flex; 
                align-items: center; 
                gap: 8px; 
                background: {hex_to_rgba(color, 0.15)}; 
                border: 2px solid {hex_to_rgba(color, 0.4)}; 
                border-radius: 8px; 
                padding: 10px 20px;
                box-shadow: 0 2px 8px {hex_to_rgba(color, 0.3)};
            ">
                <span style="
                    color: {color}; 
                    font-size: 16px; 
                    font-weight: 700; 
                    text-transform: uppercase; 
                    letter-spacing: 0.05em;
                ">
                    {status}
                </span>
                <span style="font-size: 16px;">{emoji}</span>
            </div>
        </div>
        <div style="
            text-align: center; 
            color: #8b949e; 
            font-size: 13px; 
            margin-top: 10px; 
            max-width: 450px; 
            margin-left: auto; 
            margin-right: auto;
            line-height: 1.5;
        ">
            {message}
        </div>
        """,
        unsafe_allow_html=True
    )


def render_historical_timeline(risk_data: Dict[str, Any]):
    """
    Render historical values as vertical timeline with colored bubbles.
    
    Design:
    - Max width: 320px
    - Bubbles: 56px diameter circles with score
    - Text: To the right of each bubble
    - Compact spacing: 12px between rows
    - Color-coded: Red, Orange, Yellow, Green
    
    Args:
        risk_data: Current risk score data
    """
    # Get historical values
    historical = get_historical_values()
    
    # Color map
    color_map = {
        'Extreme Risk Off': '#ef4444',
        'Risk Off': '#f97316', 
        'Neutral': '#eab308',
        'Risk On': '#84cc16',
        'Extreme Risk On': '#22c55e'
    }
    
    # Historical items
    historical_items = [
        ("Now", historical.get('now')),
        ("Yesterday", historical.get('yesterday')),
        ("Last week", historical.get('last_week')),
        ("Last month", historical.get('last_month'))
    ]
    
    # Container with dark background
    st.markdown(
        """
        <div style="
            background: #1a2332; 
            border: 1px solid #2d3b4d; 
            border-radius: 8px; 
            padding: 20px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.2);
            max-width: 320px;
        ">
            <div style="
                color: #7a8ba0; 
                font-size: 11px; 
                font-weight: 600; 
                text-transform: uppercase; 
                letter-spacing: 0.1em; 
                margin-bottom: 16px;
            ">
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
                <div style="
                    display: flex; 
                    align-items: center; 
                    gap: 14px; 
                    margin-bottom: {margin_bottom};
                ">
                    <div style="
                        background: {status_color}; 
                        border-radius: 50%; 
                        width: 56px; 
                        height: 56px; 
                        display: flex; 
                        align-items: center; 
                        justify-content: center; 
                        flex-shrink: 0;
                        box-shadow: 0 3px 10px rgba(0,0,0,0.4);
                    ">
                        <span style="
                            color: white; 
                            font-size: 20px; 
                            font-weight: 700;
                            text-shadow: 0 1px 3px rgba(0,0,0,0.5);
                        ">{int(score)}</span>
                    </div>
                    <div style="flex: 1;">
                        <div style="
                            color: #c9d1d9; 
                            font-size: 14px; 
                            font-weight: 600; 
                            margin-bottom: 3px;
                        ">{label}</div>
                        <div style="
                            color: {status_color}; 
                            font-size: 12px; 
                            font-weight: 600;
                        ">{status}</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"""
                <div style="
                    display: flex; 
                    align-items: center; 
                    gap: 14px; 
                    margin-bottom: {margin_bottom};
                ">
                    <div style="
                        background: rgba(139, 148, 158, 0.15); 
                        border: 2px dashed #30363d; 
                        border-radius: 50%; 
                        width: 56px; 
                        height: 56px; 
                        display: flex; 
                        align-items: center; 
                        justify-content: center; 
                        flex-shrink: 0;
                    ">
                        <span style="
                            color: #6e7681; 
                            font-size: 20px; 
                            font-weight: 600;
                        ">—</span>
                    </div>
                    <div style="flex: 1;">
                        <div style="
                            color: #8b949e; 
                            font-size: 14px; 
                            font-weight: 500; 
                            margin-bottom: 3px;
                        ">{label}</div>
                        <div style="
                            color: #6e7681; 
                            font-size: 11px; 
                            font-style: italic;
                        ">Collecting data</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
    
    st.markdown('</div>', unsafe_allow_html=True)
