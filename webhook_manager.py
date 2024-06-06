import requests
import json

class WebhookManager():
    """
    Manages sending discord webhooks when the monitor detects a change
    """

    def __init__(self, webhook_url=""):
        self.webhook_url = webhook_url

    def get_webhook_url(self):
        return self.webhook_url
        
    def set_webhook_url(self, webhook_url):
        self.webhook_url = webhook_url

    def test_webhook(self):
        message = {
          "content": None,
          "embeds": [
            {
              "title": "Webhook Test",
              "description": "Your webhook is working!",
              "color": None 
            }
          ],
          "username": "ticombo monitor",
          "attachments": []
        }
        result = requests.post(self.webhook_url, data=json.dumps(message), headers={'Content-type': "application/json"})
        if not (200 <= result.status_code < 300):
            print(f"Webhook could not be sent, please check webhook.")
            print(f"Not sent with {result.status_code}, response:\n{result.json()}")
        
    def send_webhook(self, nickname, new_price, old_price, url):
        # TODO pass in the listing itself, and then parse within this function
        percent_change = round(abs(old_price - new_price) / old_price * 100, 1)
        change = "increase" if new_price >= old_price else "decrease"
        message = {
          "content": None,
          "embeds": [
            {
              "title": f"{nickname}",
              "description": f"The new lowest price for event is: {floor}\nThis is a {percent_change} {change}",
              "url": f"{url}",
              "color": 11478235
            }
          ],
          "username": "ticombo monitor",
          "attachments": []
        } 
        r = requests.post(self.webhook_url, data=json.dumps(message))
        if 200 <= r.status_code < 300:
            print(f"Webhook sent {result.status_code}")
        else:
            print(f"Not sent with {result.status_code}, response:\n{result.json()}")
