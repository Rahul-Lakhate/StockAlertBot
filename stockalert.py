import requests
from openai import OpenAI
from twilio.rest import Client
import schedule
import time

# 🔐 API Keys directly in code (not secure for production)
OPENAI_API_KEY = "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"
NEWSAPI_KEY = "bef0619fd80b41f28c79462207085f4b"
TWILIO_SID = "AC42780646eba5c3a74b443838a8e5de38"
TWILIO_AUTH_TOKEN = "f9aa8b9b8a21185705d099eb6a621452"
TWILIO_PHONE = "whatsapp:+14155238886"
MY_PHONE = "whatsapp:+919096718193"

# Step 1: Setup OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# Step 2: Get Stock Market News
def get_news():
    url = "https://newsapi.org/v2/top-headlines"
    params = {
        "q": "stock market",
        "category": "business",
        "language": "en",
        "apiKey": NEWSAPI_KEY
    }
    response = requests.get(url, params=params)
    articles = response.json().get("articles", [])
    news_text = "\n\n".join([f"{a['title']} - {a['description']}" for a in articles[:5]])
    return news_text

# Step 3: Summarize using GPT-4.1
def summarize_news(news_text):
    prompt = f"Summarize the following stock market news in 5 short bullet points with emojis:\n\n{news_text}"
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",  # ✅ supported model
        messages=[
            {"role": "system", "content": "You are a financial analyst assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()


# Step 4: Send to WhatsApp via Twilio
def send_whatsapp(message):
    twilio_client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
    twilio_client.messages.create(
        body=message,
        from_=TWILIO_PHONE,
        to=MY_PHONE
    )

# Step 5: Full Bot Task
def run_daily_news_bot():
    print("⏳ Getting news...")
    news = get_news()
    summary = summarize_news(news)
    final_message = f"📊 *Daily Share Market News Summary*\n\n{summary}"
    send_whatsapp(final_message)
    print("✅ Sent on WhatsApp!")

# Schedule daily at 8:30 AM (adjust time as needed)
schedule.every().day.at("20:07").do(run_daily_news_bot)

# For testing: Uncomment below to run instantly
# run_daily_news_bot()

print("🚀 Bot started... waiting for next schedule.")
while True:
    schedule.run_pending()
    time.sleep(60)
