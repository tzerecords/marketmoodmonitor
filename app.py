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
from utils.config import REFRESH_INTERVAL_SECONDS, RISK_SCORE_WEIGHTS
from utils.helpers import get_time_until_next_refresh

st.set_page_config(
    page_title="Market Mood Monitor",
    page_icon="📊",
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

@st.cache_data(ttl=REFRESH_INTERVAL_SECONDS, show_spinner=False)
def fetch_and_calculate_data():
    """
    Fetch market data and calculate risk score.
    Cached for 10 minutes to ensure score stability.
    
    Returns:
        Tuple of (market_data, risk_score_data)
    """
    fetcher = get_fetcher()
    calculator = get_calculator()
    
    with st.spinner("Aggregating market signals from CoinGecko & Alternative.me..."):
        market_data = fetcher.fetch_all_data()
        time.sleep(0.5)
    
    risk_score_data = calculator.calculate_risk_score(market_data)
    
    return market_data, risk_score_data


def render_header_controls(last_update_time):
    """
    Render refresh controls with dual timestamps.
    
    Args:
        last_update_time: Timestamp of last data fetch
    """
    # Calculate time ago
    time_ago = ""
    if last_update_time:
        delta = datetime.now() - last_update_time
        minutes = int(delta.total_seconds() / 60)
        if minutes < 1:
            time_ago = "Just now"
        elif minutes == 1:
            time_ago = "1 min ago"
        else:
            time_ago = f"{minutes} min ago"
    
    # Calculate next update
    time_remaining = get_time_until_next_refresh(last_update_time, REFRESH_INTERVAL_SECONDS) if last_update_time else "—"
    
    col1, col2 = st.columns([0.8, 0.2])
    
    with col1:
        st.markdown(
            f"""
            <div style="display: flex; gap: 1.5rem; align-items: center; padding: 0.5rem 0;">
                <span style="color: #8b949e; font-size: 0.8125rem;">
                    Last updated: <span style="color: #c9d1d9; font-weight: 500;">{time_ago}</span>
                </span>
                <span style="color: #6e7681; font-size: 1.25rem; font-weight: 300;">•</span>
                <span style="color: #8b949e; font-size: 0.8125rem;">
                    Next update in: <span style="color: #c9d1d9; font-weight: 500;">{time_remaining}</span>
                </span>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col2:
        if st.button("Refresh Now", use_container_width=True, type="primary"):
            st.cache_data.clear()
            st.rerun()


def main():
    """Main application entry point."""
    load_css()
    
    # Initialize session state
    if 'last_fetch_time' not in st.session_state:
        st.session_state.last_fetch_time = None
    if 'previous_score' not in st.session_state:
        st.session_state.previous_score = None
    
    # Fetch data
    market_data, risk_score_data = fetch_and_calculate_data()
    current_score = risk_score_data.get("score")
    current_status = risk_score_data.get("status")
    
    # Update last fetch time
    if market_data.get("timestamp"):
        st.session_state.last_fetch_time = market_data["timestamp"]
    
    # Toast notification on score change (auto-refresh only)
    if st.session_state.previous_score is not None:
        if current_score != st.session_state.previous_score:
            st.toast(f"Score updated: {current_score} ({current_status})", icon="✅")
    
    # Update previous score
    st.session_state.previous_score = current_score
    
    # Header controls
    render_header_controls(st.session_state.last_fetch_time)
    
    # Layout structure with ultra-tight spacing
    # 1. Hero section (thermometer asymmetric) - margin-bottom: 0.75rem
    render_thermometer(risk_score_data, st.session_state.last_fetch_time)
    st.markdown('<div style="margin-bottom: 0.75rem;"></div>', unsafe_allow_html=True)
    
    # 2. Metrics cards (4 cards tight) - margin-bottom: 0.5rem
    render_metrics_dashboard(market_data)
    st.markdown('<div style="margin-bottom: 0.5rem;"></div>', unsafe_allow_html=True)
    
    # 3. Top movers (horizontal single row) - margin-bottom: 1.5rem
    if market_data.get("top_movers"):
        render_hot_tokens(market_data["top_movers"])
    st.markdown('<div style="margin-bottom: 1.5rem;"></div>', unsafe_allow_html=True)
    
    # 4. About modal/expander - margin-top: 2.5rem
    st.markdown('<div style="margin-top: 2.5rem; border-top: 1px solid #30363d; padding-top: 2rem;"></div>', unsafe_allow_html=True)
    
    with st.expander("About", expanded=False):
        st.markdown(
            """
            **Technical Stack**
            
            - **Backend:** Python 3.11 with Streamlit 1.28 framework
            - **Caching layer:** `st.cache_data` decorators with 10min TTL
            - **APIs:** CoinGecko for market data, Alternative.me for sentiment
            - **Rate limiting:** 50 req/min with exponential backoff
            - **Data persistence:** JSON append-only logs with planned SQL migration for scalability
            
            **Methodology**
            
            - **Fear & Greed Index:** 35% weight
            - **BTC Momentum:** 25% weight
            - **Volume Health:** 20% weight
            - **Market Breadth:** 20% weight
            - **Normalization:** Z-score transformation to 0-100 scale
            - **Fallbacks:** Implemented for degraded API sources
            """,
            unsafe_allow_html=False
        )
    
    # Footer
    st.markdown(
        """
        <div style="text-align: center; color: #6e7681; font-size: 0.75rem; margin-top: 2.5rem; padding: 1rem;">
            Data from CoinGecko & Alternative.me • Not financial advice
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Auto-refresh logic
    time.sleep(1)
    if st.session_state.last_fetch_time:
        elapsed = (datetime.now() - st.session_state.last_fetch_time).total_seconds()
        if elapsed >= REFRESH_INTERVAL_SECONDS:
            st.cache_data.clear()
            st.rerun()

if __name__ == "__main__":
    main()
