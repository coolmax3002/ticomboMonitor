import requests
import json
from datetime import datetime
from listings import Listings


class WebhookManager:
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
                    "color": None,
                    "timestamp": datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z',
                }
            ],
            "username": "ticombo monitor",
            "attachments": [],
        }
        result = requests.post(
            self.webhook_url,
            data=json.dumps(message),
            headers={"Content-type": "application/json"},
        )
        if not (200 <= result.status_code < 300):
            print(f"Webhook could not be sent, please check webhook.")
            print(f"Not sent with {result.status_code}, response:\n{result.json()}")

    def send_webhook(self, nickname, new_price, old_price, url):
        # TODO pass in the listing itself, and then parse within this function
        if old_price == 999999999:
            percent_change = "initial"
            change = "webhook"
        else:
            percent_change = round(abs(old_price - new_price) / old_price * 100, 1)
            percent_change = str(percent_change) + '%'
            change = "increase" if new_price >= old_price else "decrease"
        print("here")
        message = {
            "content": None,
            "embeds": [
                {
                    "title": f"{nickname}",
                    "description": f"New lowest price: ${old_price} -> ${new_price}\nThis is a {percent_change} {change}",
                    "url": f"{url}",
                    "color": 11478235,
                    "timestamp": datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z',
                }
            ],
            "username": "ticombo monitor",
            "attachments": [],
        }
        print(json.dumps(message))
        result = requests.post(
            self.webhook_url,
            data=json.dumps(message),
            headers={"Content-type": "application/json"},
        )
        if not (200 <= result.status_code < 300):
            print(f"Webhook could not be sent, please check webhook.")
            print(f"Not sent with {result.status_code}, response:\n{result.json()}")

    def send_new_listing_webhook(self, listing, url):
        message = {
            "content": None,
            "embeds": [
                {
                    "title": "New Listing Added to Monitor!",
                    "description": f"Nickname: {listing.nickname}\nCategory: {listing.category}\nQuantity: {listing.quantity}\nUrl: {url}",
                    "color": None,
                    "timestamp": datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z',
                }
            ],
            "username": "ticombo monitor",
            "attachments": [],
        }
        result = requests.post(
            self.webhook_url,
            data=json.dumps(message),
            headers={"Content-type": "application/json"},
        )
        if not (200 <= result.status_code < 300):
            print(f"Webhook could not be sent, please check webhook.")
            print(f"Not sent with {result.status_code}, response:\n{result.json()}")


    def send_webhook_event(self, nickname, new_price, old_price, url):
        # TODO pass in the listing itself, and then parse within this function
        message = {
            "content": None,
            "embeds": [
                {
                    "title": f"{nickname}: Number of Listings Changed!",
                    "description": f"Number of ticket for sale for this event has changed.\n{old_price} tickets -> {new_price} tickets",
                    "url": f"{url}",
                    "color": 11478235,
                    "timestamp": datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z',
                }
            ],
            "username": "ticombo monitor",
            "attachments": [],
        }
        print(json.dumps(message))
        result = requests.post(
            self.webhook_url,
            data=json.dumps(message),
            headers={"Content-type": "application/json"},
        )
        if not (200 <= result.status_code < 300):
            print(f"Webhook could not be sent, please check webhook.")
            print(f"Not sent with {result.status_code}, response:\n{result.json()}")

