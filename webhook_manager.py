import requests

class WebhookManager():
    """
    Manages sending discord webhooks when the monitor detects a change
    """

    def __init__(self, webhook_url=""):
        self.webhook_url = webhook_url
        
    def set_webhook_url(self, webhook_url):
        self.webhook_url = webhook_url
        
    def send_webhook(self, nickname, new_price):
        if self.webhook == "":
            print("Set webhook!")
            return
        message = {"username": nickname, "content": new_price}
        r = requests.post(self.webhook, data=message)
        if 200 <= r.status_code < 300:
            print(f"Webhook sent {result.status_code}")
        else:
            print(f"Not sent with {result.status_code}, response:\n{result.json()}")
