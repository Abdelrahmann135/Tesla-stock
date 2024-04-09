import requests
import smtplib

STOCK_KEY = "M7R32C8D399Z3025"
STOCK_END_POINT = "https://www.alphavantage.co/query?"
STOCK_PAR = {
    "function": "TIME_SERIES_DAILY",
    "symbol": "TSLA",
    "interval": 5,
    "apikey": STOCK_KEY,
}

NEWS_KEY = "4aff8188438046be908d023d3aa8e7cf"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything?"
NEWS_PAR = {
    "q": "Tesla",
    "apiKey": NEWS_KEY,
    "language": "en",
}

DEMO_EMAIL = "demo@gmail.com"
DEMO_PASS = "password"

stock_response = requests.get(url=STOCK_END_POINT, params=STOCK_PAR)
stock_response.raise_for_status()
stock_data = stock_response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in stock_data.items()]
second_close = float(data_list[1]["4. close"])
first_close = float(data_list[0]["4. close"])
differance = abs(first_close-second_close)
percentage = round((differance / first_close) * 100, 2)

if differance > 5:
    news_response = requests.get(url=NEWS_ENDPOINT, params=NEWS_PAR)
    news_response.raise_for_status()
    news_data = news_response.json()["articles"]
    news_list = [f"Title: {article['title']},\n{article['description']}\n" for article in news_data[:3]]
    news_formated = f"{news_list[0]}{news_list[1]}{news_list[2]}"

    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=DEMO_EMAIL, password=DEMO_PASS)
        connection.sendmail(
            to_addrs="my email@gmail.com",
            from_addr=DEMO_EMAIL,
            msg=f"Subject:Tesla stocks📈{percentage}\n\n"
                f"{news_formated}"
        )
