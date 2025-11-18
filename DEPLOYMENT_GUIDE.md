# Market Mood Monitor - Deployment & Export Guide

## 1. Project Structure

```
market-mood-monitor/
├── app.py                          # Main Streamlit application entry point
├── main.py                         # Alternative entry point (unused)
├── pyproject.toml                  # Python dependencies (uv package manager)
├── uv.lock                         # Locked dependencies
├── README.md                       # Project documentation
├── replit.md                       # Development notes and architecture
├── .replit                         # Replit configuration
│
├── .streamlit/
│   └── config.toml                 # Streamlit server configuration (port 5000)
│
├── components/
│   ├── thermometer.py              # Risk score gauge visualization
│   ├── hot_tokens.py               # Top movers display (gainers/losers)
│   ├── metrics_cards.py            # 4-card metrics dashboard
│   └── methodology.py              # Methodology explanation panel
│
├── data/
│   ├── fetcher.py                  # API client (CoinGecko + Alternative.me)
│   ├── calculator.py               # Risk score calculation engine
│   ├── score_history.py            # Historical score persistence logic
│   ├── score_history.json          # Historical scores (90-day rolling)
│   └── metrics_cache.json          # Persistent API cache fallback
│
├── utils/
│   ├── config.py                   # Configuration constants and API endpoints
│   └── helpers.py                  # Utility functions (formatters)
│
├── assets/
│   └── styles.css                  # Custom CSS (dark theme)
│
└── attached_assets/                # Screenshots and design iterations (not needed for deployment)
```

**Total Core Files**: 16 Python files + 3 config files + 2 JSON data files

---

## 2. Environment Variables

### ✅ **NO API KEYS REQUIRED**

This project uses **100% free public APIs** with no authentication:

- **CoinGecko API (Free Tier)**: No API key needed
- **Alternative.me Fear & Greed API**: No API key needed

### Optional Environment Variables

None required. The application is fully self-contained.

### Replit-Specific Variables (Auto-Provided)

If deploying on Replit, these are automatically available but NOT required:
- `REPLIT_DOMAINS` (optional, for custom domain)
- `REPL_ID` (auto-generated)

---

## 3. Databases

### **File-Based Storage (JSON)**

No SQL database required. Uses JSON files for persistence:

#### `data/score_history.json`
```json
{
  "history": [
    {
      "timestamp": "2025-11-17T08:18:15.572103",
      "score": 31.8,
      "status": "Risk Off",
      "message": "Cautious positioning - Defensive stance recommended"
    }
  ]
}
```

**Schema**:
- `timestamp`: ISO 8601 datetime string
- `score`: float (0-100)
- `status`: string (Extreme Risk Off | Risk Off | Neutral | Risk On | Extreme Risk On)
- `message`: string (descriptive message)

**Retention**: 90 days rolling window, automatic cleanup

#### `data/metrics_cache.json`
```json
{
  "fear_greed": {...},
  "global_market": {...},
  "bitcoin": {...},
  "top_movers": {...},
  "timestamp": "2025-11-17T08:18:15.069000"
}
```

**Purpose**: Persistent cache fallback when APIs fail (rate limits, downtime)

### **In-Memory Caching**

- Streamlit `@st.cache_data` with 600-second TTL
- Session-based, does not persist across restarts

---

## 4. External Dependencies & APIs

### Python Dependencies

```toml
[project.dependencies]
pandas = ">=2.3.3"
plotly = ">=6.4.0"
python-dateutil = ">=2.9.0.post0"
requests = ">=2.32.5"
streamlit = ">=1.51.0"
```

### External APIs (Free, No Keys)

#### 1. **CoinGecko API v3**
- **Base URL**: `https://api.coingecko.com/api/v3`
- **Endpoints Used**:
  - `/global` - Global market stats (BTC dominance, total market cap, volume)
  - `/coins/markets` - Top 100 coins with 24h data
  - `/simple/price` - Bitcoin price and 24h change
- **Rate Limits**: 50 requests/minute (free tier)
- **Authentication**: None
- **Documentation**: https://www.coingecko.com/en/api/documentation

#### 2. **Alternative.me Fear & Greed Index**
- **URL**: `https://api.alternative.me/fng/`
- **Data**: Crypto Fear & Greed sentiment (0-100 scale)
- **Rate Limits**: None specified
- **Authentication**: None
- **Documentation**: https://alternative.me/crypto/fear-and-greed-index/

### API Resilience Features

- **Timeout**: 10 seconds per request
- **Session Pooling**: HTTP connection reuse
- **Exponential Backoff**: On failures
- **Persistent Cache**: Falls back to last successful data if APIs fail
- **In-Memory Cache**: 10-minute TTL to reduce API calls

---

## 5. Export to GitHub

### Step 1: Initialize Git Repository (if not already)

```bash
git init
git add .
git commit -m "Initial commit: Market Mood Monitor v2.8"
```

### Step 2: Create GitHub Repository

1. Go to https://github.com/new
2. Create repository: `marketmoodmonitor`
3. **DO NOT** initialize with README (already exists)

### Step 3: Push to GitHub

```bash
git remote add origin https://github.com/YOUR_USERNAME/marketmoodmonitor.git
git branch -M main
git push -u origin main
```

### Step 4: Create `.gitignore` (if missing)

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python

# Streamlit
.streamlit/secrets.toml

# Data (optional - include if you want history)
# data/score_history.json
# data/metrics_cache.json

# IDE
.vscode/
.idea/
*.swp

# Replit-specific (optional)
.replit
.upm/
replit.nix
uv.lock

# Attachments (not needed)
attached_assets/
```

**Note**: `score_history.json` and `metrics_cache.json` can be committed (they contain no secrets), but will be regenerated on first run if missing.

---

## 6. Alternative Platform Deployment

### Option A: **Streamlit Community Cloud** (Recommended)

**Pros**: Free, optimized for Streamlit, automatic HTTPS, custom domains

**Steps**:
1. Push code to GitHub (see section 5)
2. Go to https://share.streamlit.io
3. Connect GitHub account
4. Deploy from repository: `YOUR_USERNAME/marketmoodmonitor`
5. Main file: `app.py`
6. Python version: `3.11`

**Build Command**: None (automatic)
**Start Command**: `streamlit run app.py --server.port 8501`

**Configuration**: Reads `.streamlit/config.toml` automatically

---

### Option B: **Railway** (Docker Container)

**Pros**: Supports long-running processes, PostgreSQL if needed later, $5/month free tier

**Steps**:

1. Create `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY pyproject.toml ./
RUN pip install uv && uv pip install --system -r pyproject.toml

# Copy application
COPY . .

# Expose port
EXPOSE 5000

# Start Streamlit
CMD ["streamlit", "run", "app.py", "--server.port", "5000", "--server.address", "0.0.0.0"]
```

2. Create `railway.toml`:
```toml
[build]
builder = "DOCKERFILE"

[deploy]
startCommand = "streamlit run app.py --server.port 5000 --server.address 0.0.0.0"
```

3. Push to GitHub
4. Connect Railway to repository: https://railway.app
5. Deploy automatically

**Environment Variables**: None required

---

### Option C: **Heroku**

**Steps**:

1. Create `Procfile`:
```
web: streamlit run app.py --server.port $PORT --server.address 0.0.0.0
```

2. Create `runtime.txt`:
```
python-3.11
```

3. Create `requirements.txt` (from pyproject.toml):
```
pandas>=2.3.3
plotly>=6.4.0
python-dateutil>=2.9.0.post0
requests>=2.32.5
streamlit>=1.51.0
```

4. Deploy:
```bash
heroku create marketmoodmonitor
git push heroku main
```

**⚠️ Note**: Heroku discontinued free tier. Use Streamlit Cloud instead.

---

### ❌ **Not Compatible**

- **Vercel/Netlify**: Streamlit requires long-running Python backend. These platforms only support static sites or serverless functions.

---

## 7. Build & Start Commands

### Local Development

```bash
# Install dependencies (using uv)
uv pip install -r pyproject.toml

# OR using pip
pip install streamlit requests pandas plotly python-dateutil

# Start application
streamlit run app.py --server.port 5000
```

**Default URL**: http://localhost:5000

### Production Build

**No build step required**. Streamlit is interpreted at runtime.

### Start Command Options

```bash
# Basic (auto-detects port)
streamlit run app.py

# Custom port
streamlit run app.py --server.port 8501

# Headless mode (for servers)
streamlit run app.py --server.headless true

# Bind to all interfaces (Docker/cloud)
streamlit run app.py --server.address 0.0.0.0
```

### Health Check Endpoint

Streamlit exposes `/_stcore/health` for container health checks:

```bash
curl http://localhost:5000/_stcore/health
```

---

## 8. Backend Architecture: On-Demand vs Always-On

### **Refresh Button Behavior**

**🔘 Refresh Now Button**:
- **Type**: On-demand user action
- **Trigger**: `st.button("Refresh Now")` click
- **Action**: Clears `@st.cache_data` → Forces API refetch → `st.rerun()`
- **Backend Requirement**: ❌ **NO** always-on backend needed
- **How it works**: User clicks → Python executes → APIs called → Page reloads

**Conclusion**: Works entirely on-demand when user opens the page.

---

### **Auto-Refresh Mechanism**

**⏱️ Automatic Updates**:
```python
# In app.py line 220-226
if st.session_state.last_fetch_time:
    elapsed = (datetime.now() - st.session_state.last_fetch_time).total_seconds()
    if elapsed >= REFRESH_INTERVAL_SECONDS:  # 600 seconds = 10 minutes
        st.cache_data.clear()
        st.rerun()
```

**Type**: Client-side polling (Streamlit reruns script continuously)

**How it works**:
1. User opens page → Streamlit script runs
2. Script checks elapsed time since last fetch
3. If ≥10 minutes → clear cache → rerun script → APIs called
4. Streamlit keeps WebSocket connection alive while page is open
5. If user closes tab → **no background process runs**

**Backend Requirement**: ⚠️ **Active browser session required**

**Conclusion**: 
- ✅ Auto-refresh works ONLY while user has page open
- ❌ NO background cron jobs or schedulers
- ❌ Data does NOT update when nobody is viewing the dashboard

---

### **Background Processes**

**Question**: Are there any background processes writing data?

**Answer**: ❌ **NO**

**Data writes happen ONLY when**:
1. User opens the page (initial load)
2. User clicks "Refresh Now"
3. Auto-refresh triggers (10-minute interval, page must be open)

**Files written**:
- `data/score_history.json` (appends new score on each data fetch)
- `data/metrics_cache.json` (overwrites on each successful API call)

**Process Model**:
- **Stateless**: Each page load starts fresh
- **No daemons**: No background workers or schedulers
- **No queues**: No Redis, Celery, or job processors

**Implication for Deployment**:
- ✅ Can run on platforms with "scale to zero" (Railway, Replit autoscale)
- ✅ No need for always-on $5/month Heroku dynos
- ✅ Works perfectly with serverless cold starts
- ⚠️ If nobody visits for days, data becomes stale (by design)

---

### **Serverless vs Always-On Recommendation**

| Platform | Type | Cost | Best For |
|----------|------|------|----------|
| **Streamlit Cloud** | Serverless (auto-sleep) | Free | ✅ Recommended for this project |
| **Railway** | Container (scale to zero) | $5/month free tier | ✅ Good alternative |
| **Replit Autoscale** | Serverless | Paid plan | ✅ Current platform |
| **Heroku** | Always-on dyno | $7/month | ⚠️ Overkill for this use case |
| **Vercel/Netlify** | Serverless functions | N/A | ❌ Not compatible with Streamlit |

---

## 9. Production Checklist

### Before Deployment

- [ ] Verify `pyproject.toml` has all dependencies
- [ ] Test locally: `streamlit run app.py`
- [ ] Check `.streamlit/config.toml` port matches platform (5000 for Replit, 8501 for Streamlit Cloud)
- [ ] Commit `data/score_history.json` and `metrics_cache.json` (optional, will regenerate)
- [ ] Remove `attached_assets/` folder (design artifacts)
- [ ] Update `README.md` with live deployment URL

### Post-Deployment

- [ ] Verify thermometer gauge displays correctly
- [ ] Test "Refresh Now" button functionality
- [ ] Confirm historical values show (may take 24h for "Yesterday")
- [ ] Check browser console for errors (F12 → Console)
- [ ] Validate APIs are being called (Network tab)
- [ ] Monitor CoinGecko rate limits (50 req/min)

### Performance Optimization

- [ ] Streamlit caching enabled (already configured)
- [ ] 10-minute refresh interval prevents excessive API calls
- [ ] Persistent cache (`metrics_cache.json`) handles API failures gracefully
- [ ] All images served from static assets (no external CDNs)

---

## 10. Troubleshooting

### "Thermometer gauge not displaying"

**Cause**: Plotly package missing
**Fix**: `pip install plotly>=6.4.0`

### "API rate limit exceeded"

**Cause**: Too many requests to CoinGecko (>50/min)
**Fix**: Application already implements caching. If persistent, increase `CACHE_TTL_SECONDS` in `utils/config.py`

### "Historical Values show '—' for all periods"

**Cause**: First-time deployment, no historical data yet
**Fix**: Wait 24 hours for data to accumulate. `score_history.json` will populate over time.

### "Score changes every refresh"

**Cause**: Cache not persisting (fixed in v2.8)
**Fix**: Ensure `@st.cache_data(ttl=600)` is applied to `fetch_and_calculate_data()`

### "Dashboard doesn't auto-refresh"

**Cause**: User closed browser tab
**Fix**: Auto-refresh only works while page is open. This is by design.

---

## 11. Future Enhancements (Optional)

If you want **true** background updates (data updates even when nobody is viewing):

### Option A: Add Background Worker (Railway)

1. Create `worker.py`:
```python
import time
from data.fetcher import MarketDataFetcher
from data.calculator import RiskScoreCalculator

while True:
    fetcher = MarketDataFetcher()
    calculator = RiskScoreCalculator()
    data = fetcher.fetch_all_data()
    score_data = calculator.calculate_risk_score(data)
    time.sleep(600)  # 10 minutes
```

2. Deploy as separate service on Railway
3. Modify `app.py` to read from database instead of API calls

**Requires**: PostgreSQL or Redis for shared state

### Option B: Add Scheduled Job (GitHub Actions)

1. Create `.github/workflows/update_data.yml`:
```yaml
name: Update Market Data
on:
  schedule:
    - cron: '*/10 * * * *'  # Every 10 minutes
jobs:
  update:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: python scripts/update_data.py
      - run: git commit -am "Auto-update data"
      - run: git push
```

**Drawback**: Commits clutter Git history

---

## Summary

**Market Mood Monitor** is a **stateless, on-demand Streamlit dashboard** that:

✅ Requires **zero** API keys or secrets
✅ Uses **file-based JSON storage** (no SQL database)
✅ Fetches data **on page load** (not background)
✅ Auto-refreshes **only when browser is open**
✅ Works perfectly on **serverless platforms** (Streamlit Cloud, Railway)

**Best Deployment Platform**: **Streamlit Community Cloud** (free, optimized, zero config)

**Export Ready**: Push to GitHub → Deploy to Streamlit Cloud → Done in 5 minutes.

---

**Document Version**: 1.0 (November 17, 2025)
**Project Version**: v2.8 (1080p No-Scroll Spacing Optimization)
