"""
Risk Score Thermometer component with asymmetric layout.
Gauge left (40%), Status + Historical Values right (60%).
"""
import streamlit as st
import plotly.graph_objects as go
from typing import Dict, Any, Optional
from datetime import datetime
from data.score_history import get_historical_values


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
    
    # LEFT: Gauge with pointer/needle + score badge inside
    with col_gauge:
        # Helper function to convert hex to rgba
        def hex_to_rgba(hex_color: str, alpha: float) -> str:
            """Convert hex color to rgba with specified alpha."""
            hex_color = hex_color.lstrip('#')
            r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
            return f'rgba({r}, {g}, {b}, {alpha})'
        
        # Gauge with gray pointer/needle (Fear & Greed style)
        fig = go.Figure(go.Indicator(
            mode="gauge",  # Gauge only, score added via annotation
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
                    'tickfont': {'size': 11, 'color': '#8b949e'}  # Increased for readability
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
        
        # Add professional score badge annotation with pill-like background
        fig.add_annotation(
            text=f'<b>{score:.1f}</b>',
            x=0.5, 
            y=0.25,  # Positioned lower in gauge
            showarrow=False,
            font=dict(
                size=30,  # Slightly larger but still subtle
                color=hex_to_rgba(color, 0.6),  # 60% opacity on text
                family='system-ui, -apple-system, "Segoe UI", sans-serif'
            ),
            bgcolor=hex_to_rgba(color, 0.03),  # Ultra subtle background
            borderpad=14,  # Pill shape padding
            bordercolor=hex_to_rgba(color, 0.06),  # Border barely visible
            borderwidth=1.5  # Thin border
        )
        
        # Configure border radius for pill shape
        fig.update_annotations(borderradius=24)
        
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font={'color': "#ffffff", 'family': "-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"},
            height=240,
            margin=dict(l=10, r=10, t=10, b=10)
        )
        
        st.plotly_chart(fig, width='stretch', config={'displayModeBar': False})
    
    # RIGHT: Status + Historical Values
    with col_status:
        # Status section - Centered and organized layout
        status_html = f"""
        <style>
            @keyframes fadeIn {{
                from {{ opacity: 0; }}
                to {{ opacity: 1; }}
            }}
        </style>
        <div style="text-align: center; max-width: 600px; margin: 2rem auto; padding: 1.5rem; background: rgba(30, 35, 45, 0.3); border-radius: 12px; animation: fadeIn 0.5s ease-out;">
            <!-- Primera línea: emoji + status pill inline -->
            <div style="display: flex; align-items: center; justify-content: center; margin-bottom: 1rem;">
                <span style="font-size: 1.5rem; margin-right: 0.75rem;">{emoji}</span>
                <span style="background: {color}26; color: {color}; padding: 0.5rem 1.5rem; border-radius: 8px; font-size: 1.75rem; font-weight: 700; letter-spacing: 0.05em; text-transform: uppercase; border: 2px solid {color}40;">
                    {status}
                </span>
            </div>
            <!-- Segunda línea: score centrado con tooltip -->
            <div style="font-size: 2.5rem; font-weight: 600; color: {color}; margin-bottom: 0.75rem;">
                {score} <span style="font-size: 1rem; color: #8b949e; cursor: help; margin-left: 0.5rem;" title="Composite score: Fear &amp; Greed 35%, BTC Momentum 25%, Volume 20%, Breadth 20%">ⓘ</span>
            </div>
            <!-- Tercera línea: mensaje descriptivo -->
            <div style="color: #8b949e; font-size: 1rem; line-height: 1.5;">
                {message}
            </div>
        </div>
        """
        
        st.markdown(status_html, unsafe_allow_html=True)
        
        # Historical Values - Ultra compacto para one-pager
        st.markdown("""
        <div style="max-width: 900px; margin: 1rem auto 0 auto;">
            <p style="font-size: 0.75rem; color: #8b949e; letter-spacing: 0.1em; margin-bottom: 0.5rem; text-transform: uppercase; font-weight: 600; text-align: left;">Historical Values</p>
        </div>
        """, unsafe_allow_html=True)
        
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
        
        # Container con max-width fijo
        st.markdown('<div style="max-width: 900px; margin: 0 auto;">', unsafe_allow_html=True)
        
        for label, data in historical_items:
            if data and data.get('score') is not None:
                score = data['score']
                status = data['status']
                status_color = color_map.get(status, '#f97316')
                
                st.markdown(f"""
                <div style="display: grid; grid-template-columns: 120px auto 50px 130px; gap: 1.5rem; align-items: center; padding: 0.4rem 0.75rem; border-bottom: 1px solid rgba(48, 54, 61, 0.2);">
                    <span style="color: #c9d1d9; font-size: 0.875rem; font-weight: 500;">{label}</span>
                    <div></div>
                    <div style="background: {status_color}; border-radius: 50%; width: 36px; height: 36px; display: flex; align-items: center; justify-content: center; box-shadow: 0 1px 4px rgba(0,0,0,0.1);">
                        <span style="color: white; font-size: 0.875rem; font-weight: 700;">{int(score)}</span>
                    </div>
                    <span style="color: {status_color}; font-size: 0.8rem; font-weight: 600; text-align: right;">{status}</span>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="display: grid; grid-template-columns: 120px auto 50px 130px; gap: 1.5rem; align-items: center; padding: 0.4rem 0.75rem; border-bottom: 1px solid rgba(48, 54, 61, 0.2);">
                    <span style="color: #c9d1d9; font-size: 0.875rem; font-weight: 500;">{label}</span>
                    <div></div>
                    <div style="background: rgba(139, 148, 158, 0.15); border-radius: 50%; width: 36px; height: 36px; display: flex; align-items: center; justify-content: center;">
                        <span style="color: #8b949e; font-size: 0.875rem; font-weight: 700;">—</span>
                    </div>
                    <span style="color: #8b949e; font-size: 0.75rem; font-style: italic; text-align: right;">Collecting</span>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
