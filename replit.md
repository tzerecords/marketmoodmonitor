# Market Mood Monitor

## Overview

Market Mood Monitor is a real-time cryptocurrency market sentiment dashboard that synthesizes multiple market signals into a single actionable Risk Score (0-100). The application transforms complex market data from various sources into a visual "thermometer" that indicates whether current market conditions favor aggressive (Risk On) or defensive (Risk Off) positioning.

**Core Value:** Distills data chaos into a clear trading decision in 30 seconds.

The system aggregates Fear & Greed sentiment, Bitcoin momentum, trading volume health, and market breadth into a weighted composite score, presented through an interactive Streamlit dashboard with auto-refresh capabilities.

## User Preferences

### Communication Style
Preferred communication style: Simple, everyday language.

### Git Workflow
**Manual Git Push Policy** - Agent does NOT automatically push to GitHub.

**Workflow:**
1. User provides feature request or bug fix
2. Agent implements code changes and completes all tasks
3. Agent confirms completion to user
4. User reviews changes in running application
5. **User manually pushes to GitHub** via UI button "Push branch as 'origin/main'" when satisfied
6. GitHub updates → Perplexity.ai (user's project manager connected to GitHub) sees all changes

**Repository:** https://github.com/tzerecords/marketmoodmonitor

**DO NOT:**
- Automatically run `git push` after completing tasks
- Push to GitHub without user's explicit instruction

**DO:**
- Complete all code changes and thorough testing
- Notify user when all tasks are done and ready for review
- Let user control when changes go to GitHub

## System Architecture

### Frontend Architecture

**Framework:** Streamlit 1.38+ with custom CSS theming

The application uses a component-based architecture with modular UI elements:

- **Main Application (`app.py`)**: Orchestrates data fetching, caching, and component rendering with auto-refresh every 10 minutes. Implements toast notifications for score updates and dual-timestamp refresh controls.
- **Component System**: Isolated rendering modules for asymmetric thermometer gauge, horizontal top movers, professional metrics cards, and About modal
- **Styling Strategy**: Custom CSS (`assets/styles.css`) with DefiLlama-inspired dark theme using system fonts (-apple-system, Segoe UI), tight spacing (1.5rem gaps), and zero decorative animations for institutional aesthetic

**Design Pattern:** Single-page dashboard with asymmetric hero layout (gauge 40% / status 60%), optimized for wide layout (1400px max width), professional typography scale (48/32/16/13px)

### Backend Architecture

**Data Layer Pattern:** Fetch → Calculate → Cache → Render

**Key Components:**

1. **Data Fetcher (`data/fetcher.py`)**: 
   - Centralized API client using `requests.Session` for connection pooling
   - Handles calls to CoinGecko API (market data) and Alternative.me (Fear & Greed Index)
   - Implements request-level error handling with logging, 10-second timeouts, and 0.5s rate limiting between calls
   - In-memory cache dictionary to reduce redundant API calls within refresh windows

2. **Risk Score Calculator (`data/calculator.py`)**:
   - Implements weighted multi-factor scoring model
   - Formula: `(Fear & Greed × 35%) + (BTC Momentum × 25%) + (Volume Health × 20%) + (Market Breadth × 20%)`
   - Contains business logic for momentum normalization based on 24h price change thresholds
   - Integrates with score persistence layer to save every calculation to `score_history.json`

3. **Score History Persistence (`data/score_history.py`)**:
   - JSON-based persistence system storing risk scores with timestamps
   - Maintains 90-day rolling history with automatic cleanup
   - Provides historical value retrieval (Now/Yesterday/Last week/Last month)
   - Powers historical values display in thermometer status panel
   - File location: `data/score_history.json`

4. **Caching Strategy**:
   - Streamlit's `@st.cache_data` decorator with TTL=600s for CSS and data functions
   - `@st.cache_resource` for singleton instances (fetcher, calculator)
   - Prevents redundant API calls and expensive recalculations on reruns
   - Score stability ensured through cache TTL + JSON persistence

**Configuration Management (`utils/config.py`):**
- Centralized constants for API endpoints, timeouts, weights, color palette
- Risk score thresholds defining 5 market states (Extreme Risk Off → Extreme Risk On)
- Design system tokens for consistent UI rendering

### Data Flow

1. User opens app or auto-refresh triggers
2. `fetch_and_calculate_data()` retrieves market data via `MarketDataFetcher`
3. Raw data passes to `RiskScoreCalculator` for weighted scoring
4. Components receive processed data and render visualizations
5. Plotly generates interactive thermometer gauge
6. CSS animations drive hot tokens ticker carousel

### Visualization Strategy

**Thermometer Component (Asymmetric Layout):** 
- LEFT (40%): Plotly `go.Indicator` gauge with semicircular display (0-100 range), dynamic color mapping
- RIGHT (60%): Status panel with large score number (48px), status text (32px), message (16px), last updated timestamp, and Historical Values section showing Now/Yesterday/Last week/Last month with colored badges

**Metrics Cards (Professional):** 4-card layout with tight spacing (gap="medium" = 1rem):
- BTC Dominance (%)
- Total Market Cap ($)
- Altcoin Season Index (% of top 50 coins outperforming BTC in 24h)
- 24H Volume ($)
- Each card: uppercase label (13px gray), main number (32px white), delta (16px green/red), no charts

**Top Movers (Horizontal Single Row):** 
- Header with "TOP MOVERS" label + timeframe selector (24H ▼ | 7D | 30D)
- Single line display: Top 3 gainers + top 3 losers
- Format: BTC +3.2% | ETH +1.8% | SOL +5.4% ● ADA -2.1% | DOT -1.5%
- Green for positive, red for negative, bullet separator between sections

## External Dependencies

### Third-Party APIs

1. **CoinGecko API (Free Tier)**
   - **Purpose:** Real-time cryptocurrency market data
   - **Endpoints Used:**
     - `/global`: Total market cap, volume, BTC/ETH dominance
     - `/coins/markets`: Top 100 coins with prices, volumes, 24h changes
     - `/simple/price`: Specific coin price queries
   - **Rate Limits:** 10-50 calls/min (free tier), mitigated by 600s cache TTL and 0.5s request delays
   - **Error Handling:** Graceful degradation with None returns, logged errors

2. **Alternative.me Fear & Greed API**
   - **Purpose:** Crypto market sentiment index (0-100)
   - **Endpoint:** `https://api.alternative.me/fng/`
   - **Data:** Current value, classification, 7-day history
   - **Reliability:** No authentication required, robust public endpoint

### Python Libraries

- **streamlit 1.38+**: Web framework for data apps
- **plotly**: Interactive thermometer gauge visualization
- **requests**: HTTP client for API calls with session management
- **pathlib**: File path handling for CSS loading

### Data Storage

**Current Implementation:** Hybrid approach

1. **In-Memory Caching:** Streamlit's built-in `@st.cache_data` decorators for API responses (10-min TTL)
2. **Score History Persistence:** JSON file (`data/score_history.json`) storing risk scores with 90-day retention
   - Enables historical comparison (Now vs Yesterday vs Last week vs Last month)
   - Survives app restarts and deployments
   - Lightweight, version-controllable, no database required

**Note:** For production scale with thousands of daily data points, consider migrating score_history.json to PostgreSQL/SQLite with Drizzle ORM.

### Design Assets

- Custom CSS theme inspired by DefiLlama's dark mode aesthetic
- Color palette optimized for financial data visualization (reds for bearish, greens for bullish)
- **System Font Stack:** `-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif` for institutional aesthetic (zero latency, native feel on macOS/Windows)
- **Typography Scale:** 48px (hero score) / 32px (status) / 16px (body) / 13px (labels)
- **Spacing System:** Tight layout with 1.5rem section gaps, 1rem card gaps, 2rem before footer
- **Professional UI:** No hover animations, flat borders (1px solid #30363d), minimal decorative elements

### Deployment Considerations

- **Platform:** Designed for Replit, Streamlit Cloud, or any Python hosting supporting background refresh
- **Environment Variables:** No API keys currently required (using free/public endpoints)
- **Resource Requirements:** Minimal - mostly stateless with 10-minute refresh cycle + lightweight JSON persistence
- **Logging:** Python's built-in `logging` module with INFO level for API tracking
- **User Feedback:** Toast notifications on score updates (auto-refresh only, not manual refresh)

## Recent Changes

### November 11, 2025 (v2.1 - Critical UI/UX Fixes)

**Post-Rollback Rendering Fixes:**
- ✅ **Historical Values**: Migrated from custom HTML to native Streamlit components (`st.metric` + `st.markdown`) to eliminate HTML escaping issues (no more visible `</div>` tags)
- ✅ **Status Layout**: Reorganized status section with centered max-width 600px container, subtle background, and clear hierarchy: emoji + status pill inline, score number centered, descriptive message below
- ✅ **Tooltips**: Added browser-native tooltips (title attribute) with ⓘ icons to all 4 metrics cards (BTC Dominance, Total Market Cap, Altcoin Season, 24H Volume) for improved UX and accessibility
- ✅ **Error Boundary**: Implemented global try-except in `main()` for graceful error handling with user-friendly fallback messages instead of red stack traces
- ✅ **Material Icons Fix**: Added CSS rules to hide Material Icons fallback text ("keyboard_arrow_right", "keyboard_arrow_down") by setting font-size: 0 on icon classes
- ✅ **Deprecation Warning**: Fixed Streamlit 1.38+ deprecation by replacing `use_container_width=True` with `width='stretch'` in Plotly chart rendering

**Technical Details:**
- All fixes architect-reviewed and approved with zero regressions
- Refactored `components/thermometer.py` to use native Streamlit metrics with dynamic color coding from `utils/config.py` color map
- Updated `components/metrics_cards.py` to include explanatory tooltips on card labels
- Enhanced `assets/styles.css` with Material Icons fallback text hiding rules
- Error boundary provides technical details in collapsible expander for debugging

**Design Principles Maintained:**
- Native Streamlit components over custom HTML for reliability and accessibility
- Browser-native tooltips over custom implementations for performance
- Professional color coding using existing design system (Risk Off: #f97316, Neutral: #eab308, Risk On: #10b981)

### November 10, 2025 (v2.0 - Professional Redesign)

**Major UI/UX Overhaul:**
- ✅ Asymmetric hero layout (gauge left 40%, status + history right 60%)
- ✅ Score history persistence system with JSON storage (90-day retention)
- ✅ Historical values display (Now/Yesterday/Last week/Last month) with colored badges
- ✅ System font stack for institutional aesthetic (SF Pro/Segoe UI)
- ✅ Tight spacing layout matching DefiLlama density (1.5rem/1rem gaps)
- ✅ Professional metrics cards: BTC Dom, Market Cap, Altcoin Season Index, Volume
- ✅ Horizontal top movers (top 3 gainers + losers in single row)
- ✅ Toast notifications on score updates
- ✅ Dual-timestamp refresh controls ("Last updated" + "Next update in")
- ✅ About modal with professional copy (removed "Portfolio demonstration" language)
- ✅ Removed ALL synthetic/fake data (BTC momentum chart, volume trend, market breadth)
- ✅ Removed decorative emojis from UI (kept only in gauge result)
- ✅ Removed hover animations on cards for flat, professional feel

**Technical Improvements:**
- Added `data/score_history.py` module for persistent score tracking
- Integrated score persistence in calculator with graceful error handling
- Deleted `components/mini_charts.py` (synthetic data violates project integrity)
- Typography scale standardized to 48/32/16/13px
- Card spacing reduced from gap="large" (2rem) to gap="medium" (1rem)

**Design Philosophy:**
- **Zero synthetic data:** If real data unavailable, remove feature entirely
- **DefiLlama-grade professionalism:** Asymmetric layouts, system fonts, tight spacing
- **Portfolio demonstration:** Dashboard showcases advanced Streamlit skills, multi-source API integration, data persistence, and product thinking