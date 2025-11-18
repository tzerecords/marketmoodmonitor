# 🌡️ Market Mood Monitor

> Real-time crypto market sentiment dashboard with Risk On/Risk Off thermometer

![Market Mood Monitor](https://img.shields.io/badge/Status-Live-success)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.38-red)

## Overview

Market Mood Monitor synthesizes multiple cryptocurrency market signals into a single, actionable **Risk Score (0-100)** that indicates whether current conditions favor aggressive or defensive positioning.

**Key Value Proposition:** From data chaos to a clear decision in 30 seconds.

## Sprint Summary (v2.8)

**Latest Release**: November 17, 2025 - 1080p No-Scroll Spacing Optimization

This sprint focused on visual continuity, professional polish, and viewport optimization:

✅ **Visual Hierarchy System**: Implemented consistent badge patterns (72px status → 40px historical → 28px gauge) creating clear information hierarchy  
✅ **Spacing Optimization**: Reduced vertical spacing (1.25rem rhythm) enabling full dashboard fit in 1920×1080 without scroll  
✅ **Typography Decisions**: Maintained professional two-tier system (primary metrics 0.8125rem, secondary sections 0.75rem) for optimal readability  
✅ **Historical Values Fix**: Eliminated duplicate entries using sequential exclusion algorithm  
✅ **Production Ready**: Zero synthetic data, transparent tooltips, persistent cache fallback for API resilience

**Key Learnings**:
- Visual consistency trumps uniformity - intelligent hierarchy improves UX over strict standardization
- User validation critical - multiple iterations revealed subtle bugs only visible in production UI
- Professional polish requires architect review - code correctness ≠ visual correctness

## Features

### 🌡️ Risk Thermometer (Asymmetric Layout)
- **Gauge Visualization** (40%): Plotly indicator with gray pointer, 0-100 scale, dynamic color bands
- **Status Panel** (60%): 72px circular score badge + status pill with emoji + descriptive message
- **Historical Values**: Vertical 2-column layout showing Now, Yesterday, Last week, Last month with 40px circular badges
- **Intelligent Placeholders**: Shows "—" + "Collecting data" when historical data not yet available

### 📊 Professional Metrics Dashboard
- **BTC Dominance**: Bitcoin market cap as % of total crypto market
- **Total Market Cap**: Combined capitalization of all cryptocurrencies
- **Altcoin Season Index**: % of top movers outperforming BTC in 24h
- **24H Volume**: Total trading volume across all markets
- **Design**: 4-card layout with tooltips (ⓘ icons), uppercase labels, clean typography

### 🔥 Top Movers Ticker
- **Horizontal Display**: Top 3 gainers + top 3 losers in single row
- **Color Coding**: Green for gains, red for losses
- **Clean Format**: "BTC +5.2% | ETH +3.1% | SOL +2.8% ● DOGE -4.1% | SHIB -3.2% | ADA -1.9%"

### 🔄 Auto-Refresh System
- **10-Minute Interval**: Automatic data updates while page is open
- **Manual Refresh**: "Refresh Now" button for on-demand updates
- **Dual Timestamps**: "Last updated: X min ago" + "Next update in: Y min"
- **Cache Indicator**: Yellow badge shows when using cached data (API rate limits)

### 🛡️ API Resilience
- **Persistent Cache**: `metrics_cache.json` fallback when CoinGecko returns 429 (rate limit)
- **In-Memory Cache**: 10-minute TTL reduces API calls
- **Graceful Degradation**: Shows last successful data instead of errors
- **Timeout Protection**: 10-second timeouts prevent hanging

### 📖 Transparent Methodology
- **Collapsible About Section**: Technical stack, methodology breakdown, risk score weights
- **Tooltip Education**: Every metric has hover tooltip explaining calculation
- **Score Formula**: Composite score breakdown (Fear & Greed 35%, BTC Momentum 25%, Volume 20%, Breadth 20%)

## How It Works

The Risk Score combines four weighted components:

```
Risk Score = (Fear & Greed × 35%) + (BTC Momentum × 25%) + 
             (Volume Health × 20%) + (Market Breadth × 20%)
```

### Components Explained

1. **Fear & Greed Index (35%)** - Market sentiment from Alternative.me API
2. **BTC Momentum (25%)** - Bitcoin's 24h price trend normalized to 0-100
3. **Volume Health (20%)** - Trading volume relative to market cap (optimal: 5-6%)
4. **Market Breadth (20%)** - % of top 100 coins with positive 24h performance

### Score Interpretation

| Range | Status | Action |
|-------|--------|--------|
| **0-30** | 🔴 Extreme Risk Off | Protect capital mode - Market showing extreme weakness |
| **31-45** | 🟠 Risk Off | Cautious positioning - Defensive stance recommended |
| **46-60** | 🟡 Neutral | Wait for confirmation - No clear directional bias |
| **61-80** | 🟢 Risk On | Constructive conditions - Market showing strength |
| **81-100** | 💚 Extreme Risk On | Maximum exposure justified - Strong bullish momentum |

## Tech Stack

- **Frontend**: Streamlit 1.51+ with custom CSS (DefiLlama-inspired dark theme)
- **Backend**: Python 3.11
- **Data Visualization**: Plotly for interactive gauges
- **APIs**: 
  - CoinGecko (market data, prices, volume) - **FREE, no API key**
  - Alternative.me (Fear & Greed Index) - **FREE, no API key**
- **Deployment**: Replit (autoscale), compatible with Streamlit Cloud, Railway, Heroku
- **Persistence**: File-based JSON (no SQL database required)

## Project Structure

```
market-mood-monitor/
├── app.py                      # Main Streamlit application
├── components/
│   ├── thermometer.py          # Risk score gauge + historical values
│   ├── hot_tokens.py           # Top movers horizontal display
│   ├── metrics_cards.py        # 4-card metrics dashboard
│   └── methodology.py          # Methodology explanation panel
├── data/
│   ├── fetcher.py              # API integration layer (CoinGecko + Alternative.me)
│   ├── calculator.py           # Risk score calculation engine
│   ├── score_history.py        # Historical score persistence logic
│   ├── score_history.json      # Historical scores (90-day rolling)
│   └── metrics_cache.json      # Persistent API cache fallback
├── utils/
│   ├── config.py               # Configuration constants and API endpoints
│   └── helpers.py              # Utility functions (formatters)
└── assets/
    └── styles.css              # Custom CSS (GitHub dark theme)
```

## Local Development

```bash
# Install dependencies
pip install streamlit requests pandas plotly python-dateutil

# Run the app
streamlit run app.py --server.port 5000
```

The dashboard will be available at `http://localhost:5000`

## Deployment

See **[DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md)** for:
- Complete file structure and dependencies
- GitHub export instructions
- Deployment to Streamlit Cloud, Railway, Heroku
- Environment variables (none required!)
- On-demand vs always-on architecture
- Troubleshooting guide

**Quick Deploy to Streamlit Cloud**:
1. Push to GitHub
2. Connect at https://share.streamlit.io
3. Deploy from `app.py`
4. Done in 5 minutes (free, zero config)

## Design Philosophy

**Inspiration**: DefiLlama + Alternative.me Fear & Greed Index + GitHub Dark Theme

**Principles**:
- **Clarity over complexity** - Users understand market state in 30 seconds
- **Transparency** - Show how everything is calculated (no black box)
- **Professionalism** - Clean aesthetics, consistent typography, purposeful colors
- **Actionability** - Not just data, but insights that guide decisions
- **Visual Hierarchy** - Intelligent sizing creates intuitive information flow (not arbitrary uniformity)

## Architecture Decisions

### Typography Hierarchy
- **Primary Elements** (Metrics Cards): 0.8125rem (13px) with 0.05em letter-spacing
- **Secondary Elements** (Historical Values, Top Movers): 0.75rem (12px) with 0.1em letter-spacing
- **Rationale**: Primary metrics deserve prominence for scannability. Strict uniformity would flatten visual hierarchy and hurt UX.

### Badge System
- **Status Badge**: 72px circular (largest, most important)
- **Historical Badges**: 40px circular (secondary reference)
- **Gauge Badge**: 28px ultra-subtle (background context)
- **Rationale**: Size hierarchy guides eye naturally from primary score → historical context → gauge visualization

### Spacing Rhythm
- **Thermometer → Metrics**: 1.25rem
- **Metrics → Top Movers**: 1.25rem
- **Top Movers → About**: 1.5rem
- **Goal**: Full dashboard visible in 1920×1080 without scroll, while maintaining breathing room

## Skills Demonstrated

- **Product Thinking**: User-centric dashboard design for quick decision-making, validated through multiple UI iterations
- **Data Engineering**: API integration with robust error handling, persistent caching, rate limit management
- **Frontend Development**: Responsive UI with professional UX polish, visual hierarchy system
- **Business Analysis**: Synthesizing multiple signals into a single actionable insight
- **Systems Design**: Stateless architecture enabling serverless deployment (scale-to-zero)

## Future Enhancements (v3)

- [ ] Historical risk score chart (30-day trend line)
- [ ] AI-generated narrative explanations (OpenAI/Anthropic integration)
- [ ] Configurable alerts (email/webhook when score crosses thresholds)
- [ ] Multi-timeframe analysis (1h, 4h, 1d, 1w toggle)
- [ ] Portfolio-specific risk metrics (connect wallet)
- [ ] Export data to CSV
- [ ] True background worker (PostgreSQL + scheduled updates)

## Important Limitations

⚠️ This score reflects **current market state**, not future predictions.

⚠️ Use as **one input among many** for investment decisions.

⚠️ **Not financial advice**. Past performance doesn't guarantee future results.

⚠️ Auto-refresh only works **while page is open** (no background updates by design).

## Data Sources & Attribution

- **CoinGecko API**: Market data, cryptocurrency prices, and trading volumes
- **Alternative.me**: Fear & Greed Index with historical data
- **Update Frequency**: Every 10 minutes (while page is open) with manual refresh option
- **Rate Limits**: Optimized to stay under 50 calls/minute (CoinGecko free tier)
- **Cache Strategy**: 10-minute in-memory + persistent fallback for graceful degradation

## Version History

### v2.8 (November 17, 2025)
- 1080p no-scroll spacing optimization (1.25rem rhythm)
- Historical values duplicate elimination (sequential exclusion)
- Typography hierarchy validation (architect-reviewed)

### v2.7 (November 11, 2025)
- Historical values vertical 2-column redesign
- Improved number contrast (text-shadow + font-weight 900)
- Visual continuity with badge pattern consistency

### v2.6 (November 11, 2025)
- Status section circular badge pattern (72px)
- Emoji moved inside pill badge
- Size hierarchy: 72px → 40px → 28px

### v2.5 (November 11, 2025)
- Historical values compact refinement (40px badges)
- Flexbox layout to avoid CSS Grid bugs
- Ultra-subtle gauge badge (alpha 0.04)

### v2.4 (November 11, 2025)
- Production-ready final polish
- Data source verification (zero synthetic data)
- Persistent metrics cache implementation
- Score tooltip + altcoin season transparency fix

## License

MIT

---

**Built with ❤️ for crypto traders, portfolio managers, and market analysts**

*Showcasing capabilities in data synthesis, business intelligence, product thinking, and professional UI/UX design*
