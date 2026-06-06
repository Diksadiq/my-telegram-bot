import os
import requests
import time

TOKEN = os.getenv("8677041196:AAHI1rDkBTFXqX9PGJzjQvmyEkIG4GgR2qo")
CHAT_ID = os.getenv("7175085994")

BASE_URL = f"https://api.telegram.org/bot{TOKEN}"

DEX_URL = "https://api.dexscreener.com/latest/dex/pairs/solana"

def send_message(text):
    try:
        requests.get(BASE_URL + "/sendMessage", params={
            "chat_id": CHAT_ID,
            "text": text
        }, timeout=10)
    except Exception as e:
        print("Send error:", e)

def analyze(pair):
    try:
        name = pair["baseToken"]["symbol"]
        price_change = float(pair.get("priceChange", {}).get("h24", 0))
        volume = float(pair.get("volume", {}).get("h24", 0))
        liquidity = float(pair.get("liquidity", {}).get("usd", 0))

        # 🧠 STRATEGY (meme filter)
        if price_change > 25 and volume > 80000 and liquidity > 30000:
            return f"🟢 STRONG BUY SIGNAL 🔥\n{name}\n+{price_change}% | Vol: {volume}"

        elif price_change > 10 and volume > 30000:
            return f"🟡 WATCH LIST 👀\n{name}\n+{price_change}%"

    except:
        return None

    return None

print("Meme Signal Bot Running...")

while True:
    try:
        data = requests.get(DEX_URL, timeout=10).json()
        pairs = data.get("pairs", [])

        for pair in pairs[:25]:
            signal = analyze(pair)

            if signal:
                print(signal)
                send_message(signal)
                time.sleep(2)

        time.sleep(20)

    except Exception as e:
        print("Error:", e)
        time.sleep(10)

