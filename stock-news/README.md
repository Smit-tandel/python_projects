# 📈 TSLA Stock Alert via Email

This Python script tracks Tesla Inc. (TSLA) stock price using the Alpha Vantage API. If the price changes more than 5% between the last two trading days, it fetches the latest news using NewsAPI and sends email alerts with the headlines.

---

## 🚀 Features

- Fetches daily stock data using Alpha Vantage.
- Calculates percentage change over 2 days.
- If change > 5%, fetches 3 latest news articles via NewsAPI.
- Sends each article as a separate email alert using SMTP (Gmail).
- Can be scheduled to run daily with Task Scheduler (Windows)