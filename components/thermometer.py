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
        
        # Add professional score badge annotation with VERY subtle pill-like background
        fig.add_annotation(
            text=f'<b>{score:.1f}</b>',
            x=0.5, 
            y=0.35,  # Centered in gauge
            showarrow=False,
            font=dict(
                size=28,  # Smaller - más discreto
                color=hex_to_rgba(color, 0.5),  # 50% opacity on text
                family='system-ui, -apple-system, BlinkMacSystemFont, sans-serif'
            ),
            bgcolor=hex_to_rgba(color, 0.04),  # Ultra subtle background
            borderpad=8,  # Compact padding
            bordercolor=hex_to_rgba(color, 0.06),  # Border barely visible
            borderwidth=1  # Very thin border
        )
        
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
        # Status section - Badge circular + pill badge (patrón consistente con Historical Values)
        status_html = f"""
        <style>
            @keyframes fadeIn {{
                from {{ opacity: 0; }}
                to {{ opacity: 1; }}
            }}
        </style>
        <div style="text-align: center; max-width: 600px; margin: 2rem auto; padding: 1.5rem; background: rgba(30, 35, 45, 0.3); border-radius: 12px; animation: fadeIn 0.5s ease-out;">
            <!-- Layout horizontal: badge circular + status info -->
            <div style="display: flex; align-items: center; justify-content: center; gap: 1.5rem; margin-bottom: 1rem;">
                <!-- Badge circular con score (72x72px) -->
                <div style="background: {color}; border-radius: 50%; width: 72px; height: 72px; display: flex; align-items: center; justify-content: center; box-shadow: 0 2px 8px rgba(0,0,0,0.15); flex-shrink: 0;">
                    <span style="color: white; font-size: 1.5rem; font-weight: 700;">{score:.1f}</span>
                </div>
                <!-- Status info (pill + tooltip) -->
                <div style="text-align: left;">
                    <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.25rem;">
                        <span style="background: {color}26; color: {color}; padding: 0.4rem 1.25rem; border-radius: 8px; font-size: 1.5rem; font-weight: 700; letter-spacing: 0.05em; text-transform: uppercase; border: 2px solid {color}40; display: flex; align-items: center; gap: 0.5rem;">
                            {status} <span style="font-size: 1.25rem;">{emoji}</span>
                        </span>
                        <span style="font-size: 0.875rem; color: #8b949e; cursor: help;" title="Composite score: Fear &amp; Greed 35%, BTC Momentum 25%, Volume 20%, Breadth 20%">ⓘ</span>
                    </div>
                    <div style="color: #8b949e; font-size: 0.875rem; line-height: 1.5; margin-left: 2rem;">
                        {message}
                    </div>
                </div>
            </div>
        </div>
        """
        
        st.markdown(status_html, unsafe_allow_html=True)
        
        # Historical Values - Lista vertical de 2 columnas (estilo Fear & Greed)
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
        
        # Single container with header and rows
        st.markdown('<div style="max-width: 700px; margin: 1.5rem auto 0 auto; padding: 1rem; background: rgba(30, 35, 45, 0.2); border-radius: 12px;">', unsafe_allow_html=True)
        
        # Header
        st.markdown('<p style="font-size: 0.75rem; color: #8b949e; letter-spacing: 0.1em; margin-bottom: 1rem; text-transform: uppercase; font-weight: 600; text-align: left;">Historical Values</p>', unsafe_allow_html=True)
        
        # Rows
        for label, data in historical_items:
            if data and data.get('score') is not None:
                score = data['score']
                status = data['status']
                status_color = color_map.get(status, '#f97316')
                
                # Layout: Label izquierda | Badge circular + Status derecha
                st.markdown(f"""
                <div style="display: flex; justify-content: space-between; align-items: center; padding: 0.75rem 0; border-bottom: 1px solid rgba(48, 54, 61, 0.3);">
                    <span style="color: #c9d1d9; font-size: 0.9rem; font-weight: 500;">{label}</span>
                    <div style="display: flex; align-items: center; gap: 0.75rem;">
                        <div style="background: {status_color}; border-radius: 50%; width: 48px; height: 48px; display: flex; align-items: center; justify-content: center; box-shadow: 0 2px 6px rgba(0,0,0,0.2); flex-shrink: 0;">
                            <span style="color: white; font-size: 1.1rem; font-weight: 800; text-shadow: 0 1px 2px rgba(0,0,0,0.3);">{int(score)}</span>
                        </div>
                        <span style="color: {status_color}; font-size: 0.85rem; font-weight: 600; min-width: 140px; text-align: left;">{status}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="display: flex; justify-content: space-between; align-items: center; padding: 0.75rem 0; border-bottom: 1px solid rgba(48, 54, 61, 0.3);">
                    <span style="color: #c9d1d9; font-size: 0.9rem; font-weight: 500;">{label}</span>
                    <div style="display: flex; align-items: center; gap: 0.75rem;">
                        <div style="background: rgba(139, 148, 158, 0.2); border-radius: 50%; width: 48px; height: 48px; display: flex; align-items: center; justify-content: center; flex-shrink: 0;">
                            <span style="color: #8b949e; font-size: 1.1rem; font-weight: 700;">—</span>
                        </div>
                        <span style="color: #8b949e; font-size: 0.75rem; font-style: italic; min-width: 140px; text-align: left;">Collecting data</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
