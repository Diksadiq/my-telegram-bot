import requests
import time

TOKEN = "8677041196:AAHI1rDkBTFXqX9PGJzjQvmyEkIG4GgR2qo"
CHAT_ID = "7175085994"

BASE_URL = f"https://api.telegram.org/bot{TOKEN}"

DEX_URL = "https://api.dexscreener.com/latest/dex/tokens/solana"

def send_message(text):
    requests.get(BASE_URL + "/sendMessage", params={
        "chat_id": CHAT_ID,
        "text": text
    })

def analyze(pair):
    try:
        symbol = pair["baseToken"]["symbol"]
        price_change = pair.get("priceChange", {}).get("h24", 0)
        volume = pair.get("volume", {}).get("h24", 0)
        liquidity = pair.get("liquidity", {}).get("usd", 0)

        # 🧠 SIMPLE NARRATIVE FILTER
        if price_change > 20 and volume > 50000 and liquidity > 20000:
            return f"🟢 STRONG MEME SIGNAL: {symbol} | +{price_change}%"
        elif price_change > 10 and volume > 20000:
            return f"🟡 WATCH LIST: {symbol} | +{price_change}%"

    except:
        return None

    return None


print("Meme bot is running...")

while True:
    try:
        data = requests.get(DEX_URL, timeout=10).json()
        pairs = data.get("pairs", [])

        for pair in pairs[:20]:
            signal = analyze(pair)

            if signal:
                print(signal)
                send_message(signal)

        time.sleep(15)

    except Exception as e:
        print("Error:", e)
        time.sleep(10)
