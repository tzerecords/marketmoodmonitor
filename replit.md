# Market Mood Monitor

## Overview

Market Mood Monitor is a real-time cryptocurrency market sentiment dashboard that synthesizes multiple market signals into a single actionable Risk Score (0-100). The application transforms complex market data into a visual "thermometer" indicating whether market conditions favor aggressive (Risk On) or defensive (Risk Off) positioning. Its core purpose is to distill data chaos into clear trading decisions. The system aggregates Fear & Greed sentiment, Bitcoin momentum, trading volume health, and market breadth into a weighted composite score, presented through an interactive Streamlit dashboard with auto-refresh capabilities.

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
- Component-based architecture with modular UI elements (Main Application, Component System).
- Custom CSS (`assets/styles.css`) with a DefiLlama-inspired dark theme, system fonts, tight spacing, and zero decorative animations for an institutional aesthetic.
- Single-page dashboard with an asymmetric hero layout (gauge 40% / status 60%), optimized for wide layout (1400px max width), and professional typography scale (48/32/16/13px).
- Toast notifications for score updates and dual-timestamp refresh controls.
- Asymmetric Thermometer Component: Plotly `go.Indicator` gauge (0-100 range) with dynamic color mapping, alongside a status panel showing the score, status text, message, last updated timestamp, and historical values.
- Professional Metrics Cards: A 4-card layout displaying BTC Dominance, Total Market Cap, Altcoin Season Index, and 24H Volume, with uppercase labels, main numbers, and deltas.
- Horizontal Top Movers: Displays top 3 gainers and top 3 losers in a single row with green/red indicators.
- Browser-native tooltips (title attribute) with ⓘ icons on metrics cards.
- About modal with professional copy.

### Backend Architecture

**Data Layer Pattern:** Fetch → Calculate → Cache → Render.

**Key Components:**
- **Data Fetcher (`data/fetcher.py`)**: Centralized API client using `requests.Session` for CoinGecko and Alternative.me APIs. Handles error handling, timeouts, rate limiting, and an in-memory cache. Implements a persistent cache fallback system using `data/metrics_cache.json` for graceful degradation during API failures.
- **Risk Score Calculator (`data/calculator.py`)**: Implements a weighted multi-factor scoring model: `(Fear & Greed × 35%) + (BTC Momentum × 25%) + (Volume Health × 20%) + (Market Breadth × 20%)`. Contains business logic for momentum normalization and integrates with score persistence.
- **Score History Persistence (`data/score_history.py`)**: JSON-based system storing risk scores with timestamps in `data/score_history.json`. Maintains a 90-day rolling history with automatic cleanup and provides historical value retrieval.
- **Caching Strategy:** Streamlit's `@st.cache_data` (TTL=600s) for CSS and data functions, and `@st.cache_resource` for singleton instances.
- **Configuration Management (`utils/config.py`):** Centralized constants for API endpoints, weights, color palette, and risk score thresholds defining 5 market states.

### System Design Choices:
- **Data Flow:** App opens/auto-refreshes → `fetch_and_calculate_data()` retrieves data → `RiskScoreCalculator` processes data → Components render visualizations.
- **Error Handling:** Global try-except in `main()` for graceful error handling, and robust API error handling within the fetcher with fallbacks.
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