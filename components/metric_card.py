"""
Reusable metric card component with new design specifications.
Dark theme with precise typography and spacing.
"""
import streamlit as st


def render_metric_card(label: str, value: str, tooltip: str, margin_bottom: str = "0"):
    """
    Render a single metric card with precise design specs.
    
    Design specifications:
    - Background: #1a2332
    - Border: #2d3b4d, 8px radius
    - Padding: 20px
    - Label: 11px uppercase #7a8ba0
    - Value: 32px bold white
    - Info icon ⓘ with tooltip
    
    Args:
        label: Uppercase label for the metric
        value: Formatted value to display
        tooltip: Tooltip text for the ⓘ icon
        margin_bottom: CSS margin-bottom value (e.g., "16px", "0")
    """
    st.markdown(
        f"""
        <div style="background: #1a2332; border: 1px solid #2d3b4d; border-radius: 8px; padding: 20px; margin-bottom: {margin_bottom};">
            <div style="color: #7a8ba0; font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 12px; cursor: help; display: flex; align-items: center; gap: 4px;" title="{tooltip}">
                {label} <span style="font-size: 10px;">ⓘ</span>
            </div>
            <div style="color: #ffffff; font-size: 32px; font-weight: 700; line-height: 1;">
                {value}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
