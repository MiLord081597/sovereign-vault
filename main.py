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
    if momentum >= 0.80:
        return "ACCUMULATE (HIGH CONVICTION)"
    elif momentum >= 0.30:
        return "ACCUMULATE (MOMENTUM BUILD)"
    elif momentum < 0.00:
        return "DISTRIBUTE (TAKING PROFITS)"
    else:
        return "HOLD (RECENTERING)"

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
        
        if not live_data:
            raise HTTPException(status_code=404, detail="No market data retrieved.")

        df = pd.DataFrame(live_data)
        clean_df = harmonize_888(df)
        clean_df['baxter_action'] = clean_df.apply(baxter_categorize, axis=1)
        return {"matrix": clean_df.to_dict(orient="records")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- MOBILE FRONTEND ENDPOINT ---
@app.get("/mobile", response_class=HTMLResponse)
def get_mobile_app():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        <title>Baxter Brain Tactical</title>
        <style>
            body { background-color: #0d1117; color: #c9d1d9; font-family: 'Courier New', monospace; padding: 15px; margin: 0; }
            h2 { color: #58a6ff; text-align: center; border-bottom: 1px solid #30363d; padding-bottom: 10px;}
            .card { background: #161b22; padding: 15px; border-radius: 8px; margin-bottom: 15px; border-left: 5px solid #3fb950; box-shadow: 0 4px 8px rgba(0,0,0,0.2); }
            .card.distribute { border-color: #f85149; }
            .card.hold { border-color: #d29922; }
            .ticker { font-size: 20px; font-weight: bold; margin: 0 0 5px 0; color: #ffffff; }
            .price { font-size: 18px; color: #8b949e; margin: 0 0 10px 0; }
            .action { font-size: 14px; padding: 5px 8px; background: #21262d; border-radius: 4px; display: inline-block; color: #ffffff;}
            button { width: 100%; padding: 15px; background: #238636; color: white; border: none; border-radius: 8px; font-size: 18px; font-weight: bold; margin-bottom: 20px; cursor: pointer; }
            button:active { background: #2ea043; }
            #loader { text-align: center; display: none; color: #8b949e; margin-bottom: 15px; }
        </style>
    </head>
    <body>
        <h2>BAXTER BRAIN NODE</h2>
        <button onclick="fetchData()">SCAN GRID</button>
        <div id="loader">Harmonizing 888 Hz Nexus...</div>
        <div id="matrix"></div>

        <script>
            async function fetchData() {
                document.getElementById('matrix').innerHTML = '';
                document.getElementById('loader').style.display = 'block';
                try {
                    const response = await fetch('/api/analyze', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({tickers: ["SPY", "BTC", "NVDA", "TSLA"]})
                    });
                    const data = await response.json();
                    document.getElementById('loader').style.display = 'none';
                    document.getElementById('matrix').innerHTML = data.matrix.map(row => {
                        let statusClass = row.baxter_action.includes('DISTRIBUTE') ? 'distribute' : row.baxter_action.includes('HOLD') ? 'hold' : '';
                        return `
                            <div class="card ${statusClass}">
                                <h3 class="ticker">${row.ticker}</h3>
                                <p class="price">$${row.harmonized_price}</p>
                                <p class="action">TARGET: <strong>${row.baxter_action}</strong></p>
                                <p style="margin: 8px 0 0 0; font-size: 12px; color: #8b949e;">MOMENTUM: ${row.momentum_indicator}%</p>
                            </div>
                        `;
                    }).join('');
                } catch (err) {
                    document.getElementById('loader').innerHTML = 'API Connection Failed.';
                }
            }
        </script>
    </body>
    </html>
    """
