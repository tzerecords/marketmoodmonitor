"""
Market Mood Monitor - Main Streamlit Application
Real-time crypto market sentiment dashboard with Risk On/Off thermometer.
"""
import streamlit as st
from datetime import datetime, timedelta
from pathlib import Path
import time

from data.fetcher import MarketDataFetcher
from data.calculator import RiskScoreCalculator
from components.thermometer import render_thermometer
from components.hot_tokens import render_hot_tokens
from components.metrics_cards import render_metrics_dashboard
from components.methodology import render_methodology_panel
from utils.config import REFRESH_INTERVAL_SECONDS
from utils.helpers import get_time_until_next_refresh

st.set_page_config(
    page_title="Market Mood Monitor",
    page_icon="🌡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

@st.cache_data(ttl=REFRESH_INTERVAL_SECONDS)
def load_css():
    """Load custom CSS styles."""
    css_file = Path("assets/styles.css")
    if css_file.exists():
        with open(css_file) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

@st.cache_resource
def get_fetcher():
    """Get singleton instance of MarketDataFetcher."""
    return MarketDataFetcher()

@st.cache_resource
def get_calculator():
    """Get singleton instance of RiskScoreCalculator."""
    return RiskScoreCalculator()

def fetch_and_calculate_data():
    """
    Fetch market data and calculate risk score.
    
    Returns:
        Tuple of (market_data, risk_score_data)
    """
    fetcher = get_fetcher()
    calculator = get_calculator()
    
    with st.spinner("Fetching latest market data..."):
        market_data = fetcher.fetch_all_data()
    
    risk_score_data = calculator.calculate_risk_score(market_data)
    
    return market_data, risk_score_data

def render_header(last_update_time):
    """
    Render header with title, refresh button, and countdown timer.
    
    Args:
        last_update_time: Timestamp of last data fetch
    """
    col1, col2, col3 = st.columns([3, 1, 1])
    
    with col1:
        st.markdown(
            """
            <div class="header-title">
                🌡️ MARKET MOOD MONITOR
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col2:
        time_remaining = get_time_until_next_refresh(last_update_time, REFRESH_INTERVAL_SECONDS)
        st.markdown(
            f"""
            <div class="countdown-timer">
                ⏱️ Next update: {time_remaining}
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col3:
        if st.button("🔄 Refresh Now", use_container_width=True):
            st.cache_data.clear()
            st.rerun()
    
    st.markdown("<hr style='border: 1px solid #30363d; margin: 1rem 0;'>", unsafe_allow_html=True)

def main():
    """Main application entry point."""
    load_css()
    
    if 'last_fetch_time' not in st.session_state:
        st.session_state.last_fetch_time = None
    
    market_data, risk_score_data = fetch_and_calculate_data()
    
    if market_data.get("timestamp"):
        st.session_state.last_fetch_time = market_data["timestamp"]
    
    render_header(st.session_state.last_fetch_time)
    
    render_thermometer(risk_score_data)
    
    if market_data.get("top_movers"):
        render_hot_tokens(market_data["top_movers"])
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    render_metrics_dashboard(market_data)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    render_methodology_panel()
    
    st.markdown(
        """
        <div style="text-align: center; color: #6e7681; font-size: 0.75rem; margin-top: 2rem; padding: 1rem;">
            Market Mood Monitor | Data from CoinGecko & Alternative.me | Not financial advice
        </div>
        """,
        unsafe_allow_html=True
    )
    
    time.sleep(1)
    if st.session_state.last_fetch_time:
        elapsed = (datetime.now() - st.session_state.last_fetch_time).total_seconds()
        if elapsed >= REFRESH_INTERVAL_SECONDS:
            st.cache_data.clear()
            st.rerun()

if __name__ == "__main__":
    main()
