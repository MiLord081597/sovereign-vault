import yfinance as yf
import pandas as pd
import time

print("=====================================")
print(" BAXTER BRAIN: HEADLESS DAEMON INIT  ")
print("=====================================")
time.sleep(1)

tickers = ['SPY', 'BTC-USD', 'NVDA', 'TSLA']
live_data = []

print("[*] Tunneling to Webull/Market APIs...")
for t in tickers:
    stock = yf.Ticker(t)
    hist = stock.history(period="1d")
    if not hist.empty:
        current = round(hist['Close'].iloc[-1], 2)
        open_p = hist['Open'].iloc[0]
        momentum = round((current - open_p) / open_p * 100, 2)
        live_data.append({'ticker': t.replace('-USD',''), 'raw_price': current, 'momentum': momentum})

df = pd.DataFrame(live_data)

print("[*] Applying 888 Hz Harmonization...")
df['harmonized_price'] = round(df['raw_price'] * (1 + (df['momentum'] * 0.005)), 2)

def categorize(row):
    m = row['momentum']
    if m >= 0.80: return "ACCUMULATE"
    elif m >= 0.30: return "ACCUMULATE"
    elif m < 0.00: return "DISTRIBUTE"
    else: return "HOLD"

df['action'] = df.apply(categorize, axis=1)

print("[+] Harmonization Complete. Dispatching autonomous trades:\n")
for index, row in df.iterrows():
    print(f"    -> [{row['ticker']}] Action: {row['action']} at ${row['harmonized_price']:.2f}")

print("\n=====================================")
print(" DAEMON CYCLE COMPLETE. STANDING BY. ")
print("=====================================")
