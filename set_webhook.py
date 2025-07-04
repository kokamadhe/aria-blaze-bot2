import requests

BOT_TOKEN = "7579467782:AAFRXWF0OQV-fe0Wp5UBN-ZGHPPGeMIXDtQ"
WEBHOOK_URL = "https://aria-blaze-bot2-1.onrender.com/webhook"

set_webhook_url = f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook?url={WEBHOOK_URL}"

response = requests.get(set_webhook_url)

print(response.status_code)
print(response.json())

