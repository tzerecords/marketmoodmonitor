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

- **Main Application (`app.py`)**: Orchestrates data fetching, caching, and component rendering with auto-refresh every 10 minutes
- **Component System**: Isolated rendering modules for thermometer gauge, hot tokens ticker, metrics cards, and methodology panel
- **Styling Strategy**: Custom CSS (`assets/styles.css`) with DefiLlama-inspired dark theme, overriding Streamlit defaults for professional appearance

**Design Pattern:** Single-page dashboard with collapsible methodology section, optimized for wide layout (1400px max width)

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
   - Maintains historical tracking lists for volumes and BTC prices (prepared for future MA calculations)

3. **Caching Strategy**:
   - Streamlit's `@st.cache_data` decorator with TTL=600s for CSS and data functions
   - `@st.cache_resource` for singleton instances (fetcher, calculator)
   - Prevents redundant API calls and expensive recalculations on reruns

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

**Thermometer Component:** Plotly `go.Indicator` gauge with:
- Semicircular display (0-100 range)
- Dynamic color mapping based on score thresholds
- Large number display with status emoji and descriptive message

**Metrics Dashboard:** 4-card grid layout using custom CSS cards with hover effects, displaying Fear & Greed, BTC trend, volume, and dominance metrics

**Hot Tokens Ticker:** HTML/CSS infinite scroll animation with duplicated content for seamless looping

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

**Current Implementation:** In-memory caching only (no persistent database)

**Note:** Repository references SQLite (`cache.db` in project structure documentation) but actual implementation uses Streamlit's built-in caching decorators. If persistent caching is required, Drizzle ORM integration would need to be added with appropriate database provider (Postgres, SQLite, etc.).

### Design Assets

- Custom CSS theme inspired by DefiLlama's dark mode aesthetic
- Color palette optimized for financial data visualization (reds for bearish, greens for bullish)
- Google Fonts or system font stack (not explicitly defined in current CSS)

### Deployment Considerations

- **Platform:** Designed for Replit, Streamlit Cloud, or any Python hosting supporting background refresh
- **Environment Variables:** No API keys currently required (using free/public endpoints)
- **Resource Requirements:** Minimal - mostly stateless with 10-minute refresh cycle
- **Logging:** Python's built-in `logging` module with INFO level for API tracking