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


def render_header_controls(last_update_time, using_cache=False):
    """
    Render refresh controls with dual timestamps and cache indicator.
    
    Args:
        last_update_time: Timestamp of last data fetch
        using_cache: Whether current data is from cache (rate limited)
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
    
    # Cache indicator badge
    cache_badge = ""
    if using_cache:
        cache_badge = '<span style="margin-left: 1rem; background: rgba(234, 179, 8, 0.15); color: #eab308; padding: 0.25rem 0.75rem; border-radius: 12px; font-size: 0.75rem;">⚠ Using cached data</span>'
    
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
                {cache_badge}
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
    try:
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
        
        # Header controls with cache indicator
        render_header_controls(st.session_state.last_fetch_time, market_data.get("using_cache", False))
        
        # Layout structure - 3-column grid inspired by reference design
        # Grid: 2 cards left | Thermometer center | 2 cards right
        st.markdown('<div style="margin-bottom: 1rem;"></div>', unsafe_allow_html=True)
        
        col_left, col_center, col_right = st.columns([1, 1.2, 1], gap="medium")
        
        # Extract metrics for manual rendering
        global_data = market_data.get("global_market") or {}
        btc_data = market_data.get("bitcoin") or {}
        top_movers_data = market_data.get("top_movers") or {}
        
        btc_dominance = global_data.get("btc_dominance", 0)
        total_mcap = global_data.get("total_market_cap_usd", 0)
        volume_24h = global_data.get("total_volume_24h_usd", 0)
        btc_change_24h = btc_data.get("price_change_24h", 0)
        
        # Calculate altcoin season (public function)
        from components.metrics_cards import calculate_altcoin_season
        altcoin_season = calculate_altcoin_season(top_movers_data, btc_change_24h)
        
        # Format market cap
        if total_mcap > 1_000_000_000_000:
            mcap_display = f"${total_mcap / 1_000_000_000_000:.1f}T"
        elif total_mcap > 1_000_000_000:
            mcap_display = f"${total_mcap / 1_000_000_000:.1f}B"
        else:
            mcap_display = f"${total_mcap / 1_000_000:.1f}M"
        
        from utils.helpers import format_large_number
        
        # LEFT COLUMN: BTC Dominance + Total Market Cap
        from components.metric_card import render_metric_card
        
        with col_left:
            render_metric_card(
                label="BTC DOMINANCE",
                value=f"{btc_dominance:.1f}%",
                tooltip="Bitcoin market cap as percentage of total crypto market",
                margin_bottom="1rem"
            )
            render_metric_card(
                label="TOTAL MARKET CAP",
                value=mcap_display,
                tooltip="Combined market capitalization of all cryptocurrencies",
                margin_bottom="0"
            )
        
        # CENTER COLUMN: Thermometer (larger)
        with col_center:
            render_thermometer(risk_score_data, st.session_state.last_fetch_time)
        
        # RIGHT COLUMN: Altcoin Season + 24H Volume
        with col_right:
            render_metric_card(
                label="ALTCOIN SEASON",
                value=f"{altcoin_season:.1f}%",
                tooltip="Percentage of top 100 coins outperforming BTC in 24h",
                margin_bottom="1rem"
            )
            render_metric_card(
                label="24H VOLUME",
                value=format_large_number(volume_24h),
                tooltip="Total trading volume across all crypto markets in last 24 hours",
                margin_bottom="0"
            )
        
        # BOTTOM: Top movers horizontal strip (full-width)
        st.markdown('<div style="margin-top: 1.25rem;"></div>', unsafe_allow_html=True)
        if market_data.get("top_movers"):
            render_hot_tokens(market_data["top_movers"])
        st.markdown('<div style="margin-bottom: 1.5rem;"></div>', unsafe_allow_html=True)
        
        # 4. About section - margin-top: 2.5rem (Custom HTML to avoid Material Icons)
        st.markdown('<div style="margin-top: 2.5rem; border-top: 1px solid #30363d; padding-top: 2rem;"></div>', unsafe_allow_html=True)
        
        st.markdown(
            """
            <details style="background: #161b22; border: 1px solid #30363d; border-radius: 6px; padding: 0; margin-bottom: 1rem;">
                <summary style="padding: 0.75rem 1rem; color: #8b949e; font-weight: 500; font-size: 0.8125rem; cursor: pointer; user-select: none; list-style: none;">
                    <span style="margin-right: 0.5rem;">▸</span> About
                </summary>
                <div style="padding: 1rem; border-top: 1px solid #30363d;">
                    <p style="margin: 0 0 1rem 0;"><strong>Technical Stack</strong></p>
                    <ul style="margin: 0; padding-left: 1.5rem; color: #8b949e;">
                        <li><strong>Backend:</strong> Python 3.11 with Streamlit 1.28 framework</li>
                        <li><strong>Caching layer:</strong> <code>st.cache_data</code> decorators with 10min TTL</li>
                        <li><strong>APIs:</strong> CoinGecko for market data, Alternative.me for sentiment</li>
                        <li><strong>Rate limiting:</strong> 50 req/min with exponential backoff</li>
                        <li><strong>Persistence:</strong> JSON append-only logs with 90-day retention</li>
                        <li><strong>SQL:</strong> Query layer prepared for future PostgreSQL/Snowflake integration</li>
                    </ul>
                    <p style="margin: 1rem 0;"><strong>Methodology</strong></p>
                    <ul style="margin: 0; padding-left: 1.5rem; color: #8b949e;">
                        <li><strong>Fear & Greed Index:</strong> 35% weight</li>
                        <li><strong>BTC Momentum:</strong> 25% weight</li>
                        <li><strong>Volume Health:</strong> 20% weight</li>
                        <li><strong>Market Breadth:</strong> 20% weight</li>
                        <li><strong>Normalization:</strong> Z-score transformation to 0-100 scale</li>
                        <li><strong>Fallbacks:</strong> Implemented for degraded API sources</li>
                    </ul>
                </div>
            </details>
            
            <style>
            details > summary {
                list-style: none;
            }
            details > summary::-webkit-details-marker {
                display: none;
            }
            details[open] > summary span {
                display: inline-block;
                transform: rotate(90deg);
                transition: transform 0.2s ease;
            }
            </style>
            """,
            unsafe_allow_html=True
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
                
    except Exception as e:
        st.error('⚠️ An error occurred while loading the dashboard.')
        st.info('Please refresh the page. If the problem persists, check your internet connection or try again later.')
        
        st.markdown(
            f"""
            <details style="background: #161b22; border: 1px solid #30363d; border-radius: 6px; padding: 0; margin-top: 1rem;">
                <summary style="padding: 0.75rem 1rem; color: #8b949e; font-weight: 500; font-size: 0.8125rem; cursor: pointer; user-select: none; list-style: none;">
                    <span style="margin-right: 0.5rem;">▸</span> Technical Details
                </summary>
                <div style="padding: 1rem; border-top: 1px solid #30363d;">
                    <pre style="background: #0d1117; padding: 1rem; border-radius: 4px; overflow-x: auto; color: #f97316; font-family: monospace; font-size: 0.875rem; margin: 0;">{str(e)}</pre>
                    <p style="color: #6e7681; font-size: 0.75rem; margin: 0.5rem 0 0 0;">If this error continues, please report it with the details above.</p>
                </div>
            </details>
            """,
            unsafe_allow_html=True
        )

if __name__ == "__main__":
    main()
