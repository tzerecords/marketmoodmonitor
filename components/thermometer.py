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
    
    # LEFT: Gauge with prominent needle
    with col_gauge:
        # Gauge configuration with color-matched needle
        fig = go.Figure(go.Indicator(
            mode="gauge",
            value=score,
            domain={'x': [0, 1], 'y': [0, 1]},
            number={'font': {'size': 1, 'color': 'rgba(0,0,0,0)'}},  # Hide number inside gauge
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
                'bar': {
                    'color': color,
                    'thickness': 0.25
                },
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
                    'line': {
                        'color': color,
                        'width': 4
                    },
                    'thickness': 0.95,
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
        
        # Score badge below gauge - centered, elevated
        st.markdown(
            f"""
            <div style="text-align: center; margin-top: 1.5rem;">
                <div style="display: inline-block; background: {color}33; padding: 0.75rem 2rem; border-radius: 16px; border: 2px solid {color}66; box-shadow: 0 4px 12px rgba(0,0,0,0.15);">
                    <span style="font-size: 3rem; color: {color}; font-weight: 700; line-height: 1.2;">
                        {score}
                    </span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    # RIGHT: Status + Historical Values
    with col_status:
        # Status section - HORIZONTAL COMPACT layout
        st.markdown(
            f"""
            <div style="padding: 1rem 0;">
                <div style="display: flex; align-items: center; justify-content: center; margin-bottom: 1rem;">
                    <span style="font-size: 1.5rem; line-height: 1; margin-right: 0.75rem;">{emoji}</span>
                    <div style="background: {color}1a; padding: 0.5rem 1.5rem; border-radius: 8px; border: 1px solid {color}40;">
                        <span style="font-size: 2rem; color: {color}; font-weight: 700; letter-spacing: 0.05em; text-transform: uppercase; line-height: 1;">
                            {status}
                        </span>
                    </div>
                </div>
                <div style="text-align: center;">
                    <div style="font-size: 2.5rem; color: #ffffff; font-weight: 500; margin-top: 0.75rem; margin-bottom: 0.5rem;">
                        {score}
                    </div>
                    <div style="color: #8b949e; font-size: 1rem; line-height: 1.5; margin-top: 0.5rem;">
                        {message}
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Historical Values section - STREAMLIT NATIVE with 2x2 grid
        try:
            # Color map for status (Streamlit native colors)
            color_map = {
                'Extreme Risk Off': 'red',
                'Risk Off': 'orange',
                'Neutral': 'orange',
                'Risk On': 'green',
                'Extreme Risk On': 'green'
            }
            
            # Wrapper for max-width
            st.markdown(
                """
                <div style="max-width: 800px; margin: 1.5rem auto 0 auto;">
                    <div style="color: #8b949e; font-size: 0.875rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 0.75rem;">
                        HISTORICAL VALUES
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            # Create 2x2 grid: Now/Yesterday LEFT, Last week/Last month RIGHT
            col_left, col_right = st.columns(2)
            
            with col_left:
                # Now
                now_data = historical.get('now')
                if now_data:
                    st.metric("Now", f"{now_data['score']}", delta=None, delta_color="off")
                    status_color = color_map.get(now_data['status'], 'gray')
                    st.caption(f":{status_color}[{now_data['status']}]")
                else:
                    st.metric("Now", "—")
                
                # Yesterday
                yesterday_data = historical.get('yesterday')
                if yesterday_data:
                    st.metric("Yesterday", f"{yesterday_data['score']}", delta=None, delta_color="off")
                    status_color = color_map.get(yesterday_data['status'], 'gray')
                    st.caption(f":{status_color}[{yesterday_data['status']}]")
                else:
                    st.metric("Yesterday", "—")
            
            with col_right:
                # Last week
                week_data = historical.get('last_week')
                if week_data:
                    st.metric("Last week", f"{week_data['score']}", delta=None, delta_color="off")
                    status_color = color_map.get(week_data['status'], 'gray')
                    st.caption(f":{status_color}[{week_data['status']}]")
                else:
                    st.metric("Last week", "—")
                
                # Last month
                month_data = historical.get('last_month')
                if month_data:
                    st.metric("Last month", f"{month_data['score']}", delta=None, delta_color="off")
                    status_color = color_map.get(month_data['status'], 'gray')
                    st.caption(f":{status_color}[{month_data['status']}]")
                else:
                    st.metric("Last month", "—")
                
        except Exception as e:
            st.info("Historical data is being aggregated")
