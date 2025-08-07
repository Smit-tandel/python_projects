import requests
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_API_KEY = os.getenv("STOCK_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
TO_EMAIL = os.getenv("TO_EMAIL")

# STEP 1: Get stock data
stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY,
}

response = requests.get(STOCK_ENDPOINT, params=stock_params)
if response.status_code != 200:
    print("Failed to fetch stock data")
    exit()

try:
    data = response.json()["Time Series (Daily)"]
except KeyError:
    print("Invalid stock data format")
    exit()

data_list = [value for (key, value) in data.items()]
yesterday_data = data_list[0]
day_before_yesterday_data = data_list[1]

yesterday_close = float(yesterday_data["4. close"])
day_before_close = float(day_before_yesterday_data["4. close"])
difference = yesterday_close - day_before_close
up_down = "🔺" if difference > 0 else "🔻"
diff_percent = round((abs(difference) / yesterday_close) * 100)

# STEP 2: Get news if price change is significant
if diff_percent > 5:
    news_params = {
        "apiKey": NEWS_API_KEY,
        "qInTitle": COMPANY_NAME,
    }

    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    if news_response.status_code != 200:
        print("Failed to fetch news")
        exit()

    articles = news_response.json().get("articles", [])[:3]
    if not articles:
        print("No relevant articles found.")
        exit()

    # Format articles
    formatted_articles = [
        f"{STOCK_NAME}: {up_down}{diff_percent}%\nHeadline: {article['title']}\nBrief: {article['description']}"
        for article in articles
    ]

    # STEP 3: Send each article as an email
    for article in formatted_articles:
        msg = EmailMessage()
        msg.set_content(article)
        msg["Subject"] = f"{STOCK_NAME} Stock Alert 🚨"
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = TO_EMAIL

        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                smtp.send_message(msg)
                print("Email sent successfully!")
        except Exception as e:
            print(f"Error sending email: {e}")

else:
    print(f"Stock change {diff_percent}% is below threshold. No email sent.")
