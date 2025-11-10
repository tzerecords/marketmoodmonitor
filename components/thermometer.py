"""
Risk Score Thermometer component with semicircular gauge visualization.
"""
import streamlit as st
import plotly.graph_objects as go
from typing import Dict, Any


def render_thermometer(risk_data: Dict[str, Any]):
    """
    Render the Risk Score thermometer gauge component.
    
    Args:
        risk_data: Risk score calculation results
    """
    score = risk_data.get("score", 50)
    status = risk_data.get("status", "Unknown")
    emoji = risk_data.get("emoji", "⚪")
    message = risk_data.get("message", "")
    color = risk_data.get("color", "#808080")
    
    st.markdown(
        f"""
        <div style="text-align: center; padding: 2rem 0;">
            <h1 style="color: #ffffff; font-size: 2.5rem; margin-bottom: 1rem;">
                🌡️ MARKET PULSE THERMOMETER
            </h1>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        domain={'x': [0, 1], 'y': [0, 1]},
        number={
            'font': {'size': 72, 'color': color},
            'suffix': ""
        },
        gauge={
            'axis': {
                'range': [0, 100],
                'tickwidth': 2,
                'tickcolor': "#30363d",
                'tickfont': {'size': 14, 'color': '#8b949e'}
            },
            'bar': {'color': color, 'thickness': 0.3},
            'bgcolor': "#161b22",
            'borderwidth': 2,
            'bordercolor': "#30363d",
            'steps': [
                {'range': [0, 30], 'color': 'rgba(239, 68, 68, 0.15)'},
                {'range': [30, 45], 'color': 'rgba(249, 115, 22, 0.15)'},
                {'range': [45, 60], 'color': 'rgba(234, 179, 8, 0.15)'},
                {'range': [60, 80], 'color': 'rgba(16, 185, 129, 0.15)'},
                {'range': [80, 100], 'color': 'rgba(34, 197, 94, 0.15)'},
            ],
            'threshold': {
                'line': {'color': color, 'width': 6},
                'thickness': 0.8,
                'value': score
            }
        }
    ))
    
    fig.update_layout(
        paper_bgcolor="#0d1117",
        plot_bgcolor="#0d1117",
        font={'color': "#ffffff", 'family': "Inter, sans-serif"},
        height=350,
        margin=dict(l=20, r=20, t=20, b=20)
    )
    
    st.plotly_chart(fig, width='stretch')
    
    st.markdown(
        f"""
        <div style="text-align: center; padding: 1rem 0 2rem 0;">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">
                {emoji} <span style="color: {color}; font-weight: bold;">{status.upper()}</span>
            </div>
            <div style="color: #8b949e; font-size: 1.1rem; max-width: 600px; margin: 0 auto; line-height: 1.6;">
                {message}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
