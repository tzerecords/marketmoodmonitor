# 🌡️ Market Mood Monitor

> Real-time crypto market sentiment dashboard with Risk On/Risk Off thermometer

![Market Mood Monitor](https://img.shields.io/badge/Status-Live-success)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.38-red)

## Overview

Market Mood Monitor synthesizes multiple cryptocurrency market signals into a single, actionable **Risk Score (0-100)** that indicates whether current conditions favor aggressive or defensive positioning.

**Key Value Proposition:** From data chaos to a clear decision in 30 seconds.

## Features

- **🌡️ Risk Thermometer**: Visual semicircular gauge showing market risk appetite with dynamic color gradient
- **🔥 Hot Tokens Ticker**: Auto-scrolling carousel of top 8 movers (>$100M market cap)
- **📊 Key Metrics Dashboard**: 
  - Fear & Greed Index with 7-day history
  - Bitcoin Trend with 24h price change
  - Total 24h Market Volume
  - BTC/ETH Market Dominance
- **🔄 Auto-Refresh**: Updates every 10 minutes with countdown timer
- **📖 Transparent Methodology**: Full explanation of score calculation and data sources

## How It Works

The Risk Score combines four weighted components:

```
Risk Score = (Fear & Greed × 35%) + (BTC Momentum × 25%) + 
             (Volume Health × 20%) + (Market Breadth × 20%)
```

### Components Explained

1. **Fear & Greed Index (35%)** - Market sentiment from Alternative.me
2. **BTC Momentum (25%)** - Bitcoin's 24h price trend
3. **Volume Health (20%)** - Trading volume relative to market cap
4. **Market Breadth (20%)** - % of top 100 coins with positive 24h performance

### Score Interpretation

- **0-30**: 🔴 Extreme Risk Off → Reduce exposure, move to stables
- **31-45**: 🟠 Risk Off → Defensive positioning recommended
- **46-60**: 🟡 Neutral → Wait for clearer signals
- **61-80**: 🟢 Risk On → Constructive for adding exposure
- **81-100**: 💚 Extreme Risk On → Full allocation may be justified

## Tech Stack

- **Frontend**: Streamlit with custom CSS (DefiLlama-inspired dark theme)
- **Backend**: Python 3.11
- **Data Visualization**: Plotly for interactive gauges and charts
- **APIs**: 
  - CoinGecko (market data, prices, volume)
  - Alternative.me (Fear & Greed Index)
- **Deployment**: Replit

## Project Structure

```
market-mood-monitor/
├── app.py                      # Main Streamlit application
├── components/
│   ├── thermometer.py          # Risk score gauge component
│   ├── hot_tokens.py           # Auto-scrolling ticker
│   ├── metrics_cards.py        # 4-card dashboard
│   └── methodology.py          # Methodology explanation panel
├── data/
│   ├── fetcher.py              # API integration layer
│   └── calculator.py           # Risk score calculation engine
├── utils/
│   ├── config.py               # Configuration constants
│   └── helpers.py              # Utility functions
└── assets/
    └── styles.css              # Custom styling
```

## Local Development

```bash
# Install dependencies
pip install streamlit requests pandas plotly python-dateutil

# Run the app
streamlit run app.py
```

The dashboard will be available at `http://localhost:8501`

## Design Philosophy

**Inspiration**: DefiLlama + Alternative.me Fear & Greed Index

**Principles**:
- **Clarity over complexity** - Users understand market state in 30 seconds
- **Transparency** - Show how everything is calculated (no black box)
- **Professionalism** - Clean aesthetics, consistent typography, purposeful colors
- **Actionability** - Not just data, but insights that guide decisions

## Skills Demonstrated

- **Business Analysis**: Synthesizing multiple signals into a single insight
- **Product Thinking**: User-centric dashboard design for quick decision-making
- **Data Engineering**: API integration with robust error handling and caching
- **Frontend Development**: Responsive UI with professional UX polish

## Future Enhancements (v2)

- [ ] Historical risk score chart (30-day trend)
- [ ] AI-generated narrative explanations using OpenAI/Anthropic
- [ ] Configurable alerts (email/webhook when score crosses thresholds)
- [ ] Multi-timeframe analysis (1h, 4h, 1d, 1w)
- [ ] Portfolio-specific risk metrics
- [ ] Export data to CSV

## Important Limitations

⚠️ This score reflects **current market state**, not future predictions.

⚠️ Use as **one input among many** for investment decisions.

⚠️ **Not financial advice**. Past performance doesn't guarantee future results.

## Data Sources & Attribution

- **CoinGecko API**: Market data, cryptocurrency prices, and trading volumes
- **Alternative.me**: Fear & Greed Index with historical data
- **Update Frequency**: Every 10 minutes with manual refresh option
- **Rate Limits**: Optimized to stay under 30 calls/minute (CoinGecko free tier)

## License

MIT

---

**Built with ❤️ for crypto traders, portfolio managers, and market analysts**

*Showcasing capabilities in data synthesis, business intelligence, and product thinking*
