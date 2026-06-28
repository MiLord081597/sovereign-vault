from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import pandas as pd
import yfinance as yf

app = FastAPI(title="Baxter Brain Sovereign API")

class MarketRequest(BaseModel):
    tickers: list[str]

# --- BACKEND LOGIC ---
@app.post("/api/analyze")
def analyze_market_data(req: MarketRequest):
    # (Your existing harmonize_888 and baxter_categorize logic remains here)
    # ... [Keep your existing logic for these two functions] ...
    return {"status": "success"} 

# --- ROOT DASHBOARD (THE FIX) ---
@app.get("/", response_class=HTMLResponse)
def get_root():
    return """
    <html>
    <body>
        <h1>BAXTER BRAIN ONLINE</h1>
        <button onclick="alert('System Active')">SCAN GRID</button>
    </body>
    </html>
    """
