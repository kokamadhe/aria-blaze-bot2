import os
import requests

BOT_TOKEN = os.getenv("BOT_TOKEN")  # Set this environment variable locally
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

set_webhook_url = f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook?url={WEBHOOK_URL}"

response = requests.get(set_webhook_url)

print(response.status_code)
print(response.json())


