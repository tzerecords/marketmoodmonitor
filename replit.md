# Market Mood Monitor

## Overview

Market Mood Monitor is a real-time cryptocurrency market sentiment dashboard that synthesizes multiple market signals into a single actionable Risk Score (0-100). The application transforms complex market data into a visual "thermometer" indicating whether market conditions favor aggressive (Risk On) or defensive (Risk Off) positioning. Its core purpose is to distill data chaos into clear trading decisions, aggregating Fear & Greed sentiment, Bitcoin momentum, trading volume health, and market breadth into a weighted composite score, presented through an interactive Streamlit dashboard with auto-refresh capabilities.

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

**Framework:** Streamlit 1.38+ with custom CSS theming.

**UI/UX Decisions:**
- Component-based architecture with modular UI elements.
- Custom CSS (`assets/styles.css`) for a DefiLlama-inspired dark theme, system fonts, and professional typography.
- Single-page dashboard optimized for wide layout, featuring an asymmetric hero layout (gauge 40% / status 60%).
- Toast notifications for score updates and dual-timestamp refresh controls.
- Asymmetric Thermometer Component using Plotly `go.Indicator` gauge with dynamic color mapping, alongside a status panel.
- Professional Metrics Cards (4-card layout) displaying key market metrics like BTC Dominance, Total Market Cap, Altcoin Season Index, and 24H Volume.
- Horizontal Top Movers section displaying top 3 gainers and top 3 losers.
- Browser-native tooltips with ⓘ icons on metrics cards.
- About modal with professional copy.

### Backend Architecture

**Data Layer Pattern:** Fetch → Calculate → Cache → Render.

**Key Components:**
- **Data Fetcher (`data/fetcher.py`)**: Centralized API client using `requests.Session` for CoinGecko and Alternative.me APIs. Includes error handling, rate limiting, in-memory cache, and a persistent cache fallback system using `data/metrics_cache.json`.
- **Risk Score Calculator (`data/calculator.py`)**: Implements a weighted multi-factor scoring model: `(Fear & Greed × 35%) + (BTC Momentum × 25%) + (Volume Health × 20%) + (Market Breadth × 20%)`.
- **Score History Persistence (`data/score_history.py`)**: JSON-based system storing risk scores with timestamps in `data/score_history.json`, maintaining a 90-day rolling history.
- **Caching Strategy:** Streamlit's `@st.cache_data` (TTL=600s) for CSS and data functions, and `@st.cache_resource` for singleton instances.
- **Configuration Management (`utils/config.py`):** Centralized constants for API endpoints, weights, color palette, and risk score thresholds.

### System Design Choices:
- **Data Flow:** App opens/auto-refreshes → `fetch_and_calculate_data()` retrieves data → `RiskScoreCalculator` processes data → Components render visualizations.
- **Error Handling:** Global try-except in `main()` and robust API error handling within the fetcher with fallbacks.
- **Deployment:** Designed for Replit, Streamlit Cloud, or similar Python hosting.

## External Dependencies

### Third-Party APIs

1.  **CoinGecko API (Free Tier)**
    *   **Purpose:** Real-time cryptocurrency market data.
    *   **Endpoints Used:** `/global`, `/coins/markets`, `/simple/price`.
2.  **Alternative.me Fear & Greed API**
    *   **Purpose:** Crypto market sentiment index (0-100).
    *   **Endpoint:** `https://api.alternative.me/fng/`.

### Python Libraries

*   **streamlit 1.38+**: Web framework for data apps.
*   **plotly**: Interactive thermometer gauge visualization.
*   **requests**: HTTP client for API calls with session management.
*   **pathlib**: File path handling.

### Data Storage

*   **In-Memory Caching:** Streamlit's built-in `@st.cache_data` for API responses (10-min TTL).
*   **Score History Persistence:** JSON file (`data/score_history.json`) storing risk scores with 90-day retention.
*   **Metrics Cache Persistence:** JSON file (`data/metrics_cache.json`) for API fallback.