"""
Reusable metric card component - Dark theme design.
"""
import streamlit as st


def render_metric_card(label: str, value: str, tooltip: str, margin_bottom: str = "0"):
    """
    Render metric card with dark background.
    
    Design:
    - Background: #1a2332
    - Border: 1px solid #2d3b4d, 8px radius
    - Padding: 20px
    - Label: gray small uppercase
    - Value: large white bold
    - Soft shadow
    
    Args:
        label: Metric label (uppercase)
        value: Formatted value
        tooltip: Tooltip text
        margin_bottom: CSS margin-bottom
    """
    st.markdown(
        f"""
        <div style="
            background: #1a2332; 
            border: 1px solid #2d3b4d; 
            border-radius: 8px; 
            padding: 20px; 
            margin-bottom: {margin_bottom};
            box-shadow: 0 2px 8px rgba(0,0,0,0.2);
        ">
            <div style="
                color: #7a8ba0; 
                font-size: 11px; 
                font-weight: 600; 
                text-transform: uppercase; 
                letter-spacing: 0.1em; 
                margin-bottom: 12px;
                display: flex;
                align-items: center;
                gap: 4px;
            " title="{tooltip}">
                {label} <span style="font-size: 10px; cursor: help;">ⓘ</span>
            </div>
            <div style="
                color: #ffffff; 
                font-size: 32px; 
                font-weight: 700; 
                line-height: 1;
            ">
                {value}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
