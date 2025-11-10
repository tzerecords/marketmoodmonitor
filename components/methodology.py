"""
Methodology Panel component explaining Risk Score calculation.
"""
import streamlit as st
from typing import Dict, Any

from utils.config import RISK_SCORE_WEIGHTS


def render_methodology_panel():
    """Render expandable methodology panel with formula explanation."""
    
    with st.expander("📖 METHODOLOGY - How Risk Score Works", expanded=False):
        st.markdown(
            f"""
            <div style="color: #8b949e; line-height: 1.8;">
                <h3 style="color: #ffffff; margin-top: 0;">Formula</h3>
                <div style="background: #161b22; padding: 1rem; border-radius: 8px; border: 1px solid #30363d; margin: 1rem 0;">
                    <code style="color: #10b981; font-size: 1rem;">
                        Risk Score = (Fear & Greed × {RISK_SCORE_WEIGHTS['fear_greed']*100:.0f}%) + 
                                    (BTC Momentum × {RISK_SCORE_WEIGHTS['btc_momentum']*100:.0f}%) + 
                                    (Volume Health × {RISK_SCORE_WEIGHTS['volume_health']*100:.0f}%) + 
                                    (Market Breadth × {RISK_SCORE_WEIGHTS['market_breadth']*100:.0f}%)
                    </code>
                </div>
                
                <h3 style="color: #ffffff;">Components Explained</h3>
                
                <h4 style="color: #3b82f6;">🧠 Fear & Greed Index ({RISK_SCORE_WEIGHTS['fear_greed']*100:.0f}%)</h4>
                <p>
                    Measures overall market sentiment based on volatility, volume, social media, surveys, and dominance metrics.
                    <br><strong>Source:</strong> Alternative.me
                    <br><strong>Why:</strong> Best established proxy for retail/institutional sentiment in crypto markets.
                </p>
                
                <h4 style="color: #3b82f6;">📈 BTC Momentum ({RISK_SCORE_WEIGHTS['btc_momentum']*100:.0f}%)</h4>
                <p>
                    Tracks Bitcoin's short-term trend using 24h price change as momentum indicator.
                    <br><strong>Why:</strong> Bitcoin typically leads the market; its momentum predicts general direction.
                    <br><strong>Interpretation:</strong> >60 = bullish, <40 = bearish
                </p>
                
                <h4 style="color: #3b82f6;">📊 Volume Health ({RISK_SCORE_WEIGHTS['volume_health']*100:.0f}%)</h4>
                <p>
                    Compares current 24h volume to market cap ratio for validation.
                    <br><strong>Why:</strong> High volume with rising prices confirms real conviction (not artificial pumps).
                    <br><strong>Interpretation:</strong> >80 = strong participation
                </p>
                
                <h4 style="color: #3b82f6;">🌐 Market Breadth ({RISK_SCORE_WEIGHTS['market_breadth']*100:.0f}%)</h4>
                <p>
                    Percentage of top 100 cryptocurrencies with positive 24h performance.
                    <br><strong>Why:</strong> Broad-based rallies are more sustainable than isolated BTC pumps.
                    <br><strong>Interpretation:</strong> >60% = healthy breadth
                </p>
                
                <h3 style="color: #ffffff;">Interpretation Thresholds</h3>
                <ul style="list-style: none; padding-left: 0;">
                    <li><strong style="color: #ef4444;">0-30:</strong> Extreme Risk Off → Reduce exposure, move to stables</li>
                    <li><strong style="color: #f97316;">31-45:</strong> Risk Off → Defensive positioning recommended</li>
                    <li><strong style="color: #eab308;">46-60:</strong> Neutral → Wait for clearer signals</li>
                    <li><strong style="color: #10b981;">61-80:</strong> Risk On → Constructive for adding exposure</li>
                    <li><strong style="color: #22c55e;">81-100:</strong> Extreme Risk On → Full allocation may be justified</li>
                </ul>
                
                <h3 style="color: #ffffff;">Data Sources & Updates</h3>
                <p>
                    <strong>APIs:</strong> CoinGecko (market data, prices, volume), Alternative.me (Fear & Greed Index)
                    <br><strong>Update Frequency:</strong> Every 10 minutes | Manual refresh available
                    <br><strong>Rate Limits:</strong> Optimized to stay under 30 calls/minute (CoinGecko free tier)
                </p>
                
                <h3 style="color: #ffffff;">Important Limitations</h3>
                <p style="color: #eab308;">
                    ⚠️ This score reflects <strong>current market state</strong>, not future predictions.
                    <br>⚠️ Use as <strong>one input among many</strong> for investment decisions.
                    <br>⚠️ Not financial advice. Past performance doesn't guarantee future results.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
