from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import pandas as pd
import yfinance as yf

app = FastAPI(title="Baxter Brain Sovereign API")

class MarketRequest(BaseModel):
    tickers: list[str]

# --- BAXTER LOGIC ---
def harmonize_888(dataframe: pd.DataFrame) -> pd.DataFrame:
    dataframe['market_noise_ratio'] = 0.00
    dataframe['harmonized_price'] = round(
        dataframe['raw_price'] * (1 + (dataframe['momentum_indicator'] * 0.005)), 2
    )
    return dataframe

def baxter_categorize(row) -> str:
    momentum = row['momentum_indicator']
    if momentum >= 0.80: return "ACCUMULATE (HIGH CONVICTION)"
    elif momentum >= 0.30: return "ACCUMULATE (MOMENTUM BUILD)"
    elif momentum < 0.00: return "DISTRIBUTE (TAKING PROFITS)"
    else: return "HOLD (RECENTERING)"

# --- BACKEND API ENDPOINT ---
@app.post("/api/analyze")
def analyze_market_data(req: MarketRequest):
    try:
        live_data = []
        for t in req.tickers:
            fetch_ticker = t + '-USD' if t == 'BTC' else t
            stock = yf.Ticker(fetch_ticker)
            hist = stock.history(period="1d")
            if not hist.empty:
                current_price = round(hist['Close'].iloc[-1], 2)
                open_price = hist['Open'].iloc[0]
                momentum = round((current_price - open_price) / open_price * 100, 2)
                live_data.append({'ticker': t, 'raw_price': current_price, 'momentum_indicator': momentum})
        df = pd.DataFrame(live_data)
        clean_df = harmonize_888(df)
        clean_df['baxter_action'] = clean_df.apply(baxter_categorize, axis=1)
        return {"matrix": clean_df.to_dict(orient="records")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- ROOT DASHBOARD (REPLACES MOBILE) ---
@app.get("/", response_class=HTMLResponse)
def get_dashboard():
    return """
    <!DOCTYPE html>
    <html>
    <head><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Baxter Brain</title>
    <style>body { background-color: #0d1117; color: #fff; font-family: sans-serif; padding: 20px; }</style>
    </head>
    <body>
        <h2>BAXTER BRAIN NODE</h2>
        <button onclick="fetchData()">SCAN GRID</button>
        <div id="matrix"></div>
        <script>
            async function fetchData() {
                const response = await fetch('/api/analyze', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({tickers: ["SPY", "BTC", "NVDA", "TSLA"]})
                });
                const data = await response.json();
                document.getElementById('matrix').innerHTML = JSON.stringify(data.matrix);
            }
        </script>
    </body>
    </html>
    """
