"""
Reusable metric card component for consistent styling.
"""
import streamlit as st


def render_metric_card(label: str, value: str, tooltip: str, margin_bottom: str = "0"):
    """
    Render a single metric card with consistent styling.
    
    Args:
        label: Uppercase label for the metric
        value: Formatted value to display
        tooltip: Tooltip text for the ⓘ icon
        margin_bottom: CSS margin-bottom value (e.g., "1rem", "0")
    """
    st.markdown(
        f"""
        <div style="background: #0d1117; border: 1px solid #30363d; border-radius: 6px; padding: 1rem; margin-bottom: {margin_bottom};">
            <div style="color: #8b949e; font-size: 0.75rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 0.5rem; cursor: help;" title="{tooltip}">
                {label} ⓘ
            </div>
            <div style="color: #ffffff; font-size: 2rem; font-weight: 700; line-height: 1;">
                {value}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
