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

## Recent Changes

### November 11, 2025 (v2.8 - 1080p No-Scroll Spacing Optimization)

**Reduced Vertical Spacing for Full Dashboard Viewport Fit:**
- ✅ **Thermometer → Metrics**: Changed from 0.75rem to 1.25rem for better breathing room
- ✅ **Metrics → Top Movers**: Changed from 0.5rem to 1.25rem for consistent spacing rhythm
- ✅ **Top Movers → About**: Maintained 1.5rem for section separation
- ✅ **Comments Updated**: Layout comments now reference "1080p no-scroll" optimization goal
- ✅ **Visual Balance**: Tighter spacing maintains professional feel without cramped appearance

**1080p Viewport Validation:**
- Entire dashboard (header → thermometer → metrics → top movers → about) fits in 1920×1080 without vertical scroll
- Spacing rhythm: 1.25rem → 1.25rem → 1.5rem creates consistent visual flow
- Architect-reviewed with zero regressions

### November 11, 2025 (v2.7 - Historical Values Vertical Redesign)

**Historical Values Vertical List (Fear & Greed Style):**
- ✅ **Vertical Layout**: Changed from horizontal to vertical list with 2 columns (Label left | Badge + Status right)
- ✅ **Circular Badges**: All badges 48x48px (consistent sizing across all rows)
- ✅ **Improved Contrast**: Font-weight 800 + text-shadow (0 1px 2px rgba(0,0,0,0.3)) for better number visibility
- ✅ **Single Container**: Header and rows in one container (rgba(30, 35, 45, 0.2) background, 12px border-radius)
- ✅ **Max-width 700px**: Centered container prevents oversizing on desktop
- ✅ **Proper Spacing**: 0.75rem vertical padding per row, 0.75rem gap between badge and status text
- ✅ **Border Separators**: Subtle border-bottom (rgba 0.3 opacity) between rows
- ✅ **Pattern Consistency**: Same badge circular + text pattern as status section, just smaller size

**Visual Continuity Achieved:**
- Status section: 72px badge → Historical Values: 48px badges = Clear size hierarchy
- Both sections use identical pattern: circular badge for number + text flotando for status

### November 11, 2025 (v2.6 - Status Section Visual Consistency)

**Status Section Redesign for Visual Continuity:**
- ✅ **Circular Badge Pattern**: Moved score to 72x72px circular badge (matching Historical Values pattern)
- ✅ **Layout Standardization**: Badge circular (left) + pill badge with status text (right) + emoji inside pill
- ✅ **Size Hierarchy**: 72px status badge → 48px historical badges creates clear visual hierarchy
- ✅ **Depth Enhancement**: Box-shadow (0 2px 8px rgba(0,0,0,0.15)) on circular badge
- ✅ **Message Indentation**: Descriptive message indented 2rem for alignment
- ✅ **Flexbox Implementation**: Gap 1.5rem for proper spacing, text-align left for status info
- ✅ **Emoji Position**: Moved emoji inside pill badge (right side) for cleaner layout

### November 11, 2025 (v2.5 - Historical Values Compact Redesign)

**Historical Values Final Refinement:**
- ✅ **Simplified Layout**: Changed from CSS Grid to Flexbox with `justify-content: space-between` to avoid potential bugs
- ✅ **Compact Badge**: Reduced circular badges from 48px to 36px for tighter spacing
- ✅ **Max-width Adjustment**: Changed from 1000px to 900px for better desktop proportions
- ✅ **Visual Refinements**:
  - Added `flex-shrink: 0` to badges to prevent deformation
  - Added `box-shadow: 0 1px 4px rgba(0,0,0,0.1)` to badges for depth
  - Increased label font-weight to 500 for better readability
  - Tighter padding: 0.4rem vertical (vs 0.75rem)
  - Lighter border-bottom: rgba 0.2 opacity (vs 0.3)
- ✅ **No Emojis**: Removed emoji visual clutter for cleaner, more professional look
- ✅ **Bug Prevention**: Eliminated problematic `<div style="flex: 1;">` pattern

**Gauge Badge Refinement:**
- ✅ Ultra-subtle badge inside gauge: 28px font, alpha 0.04 background, 0.06 border, 1px border-width

### November 11, 2025 (v2.4 - Production-Ready Final Polish)

**Validaciones Críticas Pre-Production:**
- ✅ **Data Source Verification**: Confirmed ALL metrics come from real API calls or systematic calculations - ZERO synthetic data
  - BTC Dominance: Real from CoinGecko `/global` endpoint
  - Total Market Cap: Real from CoinGecko `/global` endpoint
  - 24H Volume: Real from CoinGecko `/global` endpoint
  - Historical Values: Real from `score_history.json` with timestamps
  - Altcoin Season: Real calculation using top movers vs BTC performance

**Transparency Fixes:**
- ✅ **Altcoin Season Tooltip Correction**: Updated tooltip from misleading "top 50 coins" to honest "Percentage of top movers outperforming BTC in 24h. Alternative metric to traditional altcoin season index." - describes the ACTUAL calculation

**Production Polish - 3 Final Improvements:**
- ✅ **MEJORA 1 - Score Tooltip**: Added ⓘ info icon next to score on right panel with tooltip: "Composite score: Fear & Greed 35%, BTC Momentum 25%, Volume 20%, Breadth 20%" for user education
- ✅ **MEJORA 2 - Gauge Badge Professional Refinement**:
  - Converted from `mode="gauge+number"` to `mode="gauge"` with custom annotation
  - Score badge inside gauge: font-size 36px (smaller than right score 40px for visual hierarchy)
  - Professional system-ui font family for institutional aesthetic
  - Subtle background pill with alpha 0.1 + border alpha 0.2 to anchor score visually
  - Increased gauge axis tick font from 10px to 11px for better readability
  - Added hex_to_rgba helper function for color conversions
- ✅ **MEJORA 3 - Historical Values Intelligent Placeholders**:
  - When no historical data exists (fresh install or deleted JSON), displays "—" with "Collecting data" caption
  - NEVER invents or hardcodes placeholder values
  - Maintains transparency: if data doesn't exist, tell user honestly instead of showing fake numbers

**Technical Implementation:**
- Modified `components/thermometer.py`: Gauge annotation system with professional badge styling, score tooltip, historical placeholders
- Modified `components/metrics_cards.py`: Corrected Altcoin Season tooltip for transparency
- All changes architect-reviewed and approved with zero regressions

**Design Philosophy:**
- **Transparency First**: Every metric honestly describes its source and calculation
- **Visual Hierarchy**: Gauge badge subtle (36px, 50% opacity) → Right score prominent (40px, full color)
- **User Education**: Tooltips provide context without overwhelming interface
- **Honest Placeholders**: Missing data shows "—" + explanation, never fake values

**Production Readiness Validation:**
- ✅ Persistent cache system functioning correctly (handles CoinGecko 429 rate limits)
- ✅ All data sources verified as real/systematic
- ✅ Tooltips accurate and educational
- ✅ Visual polish matches institutional dashboard standards
- ✅ Zero synthetic data in entire application

### November 11, 2025 (v2.3 - Production-Ready Polish)

**6 Critical Fixes for V1 Launch:**
- ✅ **FIX 6 - Altcoin Season Precision**: Changed format from `.0f` to `.1f` in metrics cards
- ✅ **FIX 10 - Persistent Metrics Cache**: Implemented `data/metrics_cache.json` fallback system
- ✅ **FIX 9 - API Fallback Indicator**: Added yellow "⚠ Using cached data" badge in header
- ✅ **FIX 8 - Score Badge in Gauge**: Moved risk score inside Plotly gauge with 50% opacity
- ✅ **FIX 7 - Historical Values Single Row**: Redesigned from 2x2 grid to horizontal 4-column layout
- ✅ **FIX 11 - Tight Spacing Global**: Ultra-professional DefiLlama-style spacing

**Critical Bug Fix:**
- ✅ **Cache Timestamp Regression**: Fixed stale timestamps in persistent cache - now all cache paths inject `datetime.now()`