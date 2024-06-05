import requests
import json
import threading
import time
from proxy_manager import ProxyManager
from settings_manager import SettingsManager
from webhook_manager import WebhookManager
from urllib.parse import urlparse, parse_qs
from listings import Listings

class Monitor:
    """
    A monitor class to create a lowest price monitor for ticombo listings
    """

    def __init__(self, proxy_path=None, listings=[], delay=60000):
        self.proxy_manager = ProxyManager(proxy_path)
        self.settings_manager = SettingsManager()
        self.listings = self.settings_manager.get_listings()
        self.webhook_manager = WebhookManager()
        self.urlMap = dict() 
        self.running = False
        self.thread = None
        self.delay = delay

    def set_delay(self, delay):
        self.delay = delay

    def start_monitor(self):
        if len(self.listings) == 0:
            print('There are no listings, please add at least one listing')
            return
        self.running = True
        self.thread = threading.Thread(target=self.monitor, args=())
        self.thread.start()

    def stop_monitor(self):
        self.running = False
        self.thread.join()

    def get_monitor_status(self):
        return self.running

    def add_listing(self, listing_id, catergory, quantity, nickname):
        #TODO figure out good way to save json
        self.listings.append(Listings(listing_id=listing_id, catergory=catergory, quantity=quantity, nickname=nickname))
        self.settings_manager.set_listings(self.listings)

    def grab_listing_id(self, url):
        #grab listing name from url
        parsed_url = urlpase(url)
        url_parts = parsed_url.path.split('/')
        listing_name = url_parts[-1]

        api_url = f"https://www.ticombo.com/prod/discovery/events?id={listing_name}&limit=1"

        r = requests.get(api_url)
        if r.status_code == 200:
                data = r.json()
                try:
                    listing_id = data['payload'][0]['eventId']
                    self.urlMap[listing_id] = url
                except Exception as e:
                    print("listing ID coud not be found")
                    return None
                return listing_id
        else:
                print(f"events api request failed {r.status_code=}")
                return None

    def monitor(self):
        # TODO check if proxies exist
        while self.running:
            for i, proxy in enumerate(self.proxy_manager.get_proxies()):
                for j, listing in enumerate(self.listings):
                    print("making request")
                    r = requests.get(
                        f"https://www.ticombo.com/prod/discovery/events/{listing[0]}/listings?limit=20&include=$total&populate=rel.user:firstName,displayName,urlPicture,trustedSeller,metadata,features.priceOptimization,representative%7Creservations:amount,expiresAt,price&sort=bestprice&categories=1:{listing[1]}&quantity={listing[2]}",
                        proxies=proxy,
                    )
                    if r.status_code == 200:
                        data = r.json()
                        tickets = data.get("payload", [])
                        try:
                            print("trying to grab price")
                            floor = tickets[0]["price"]["selling"]["value"]
                            currency = tickets[0]["price"]["selling"]["currency"]
                            if floor < listing[4]:
                                print(f"New price!! {floor=}")
                                self.webhook_manager.send_webhook(listing[3], floor, listing[4], self.urlMap[listing[0]])
                                listing[4] = floor
                                self.settings_manager.set_listings(self.listings)
                            else:
                                print("no change")
                        except Exception as e:
                            print("couldn't grab floor price")
                    else:
                        print(r.status_code)
                    time.sleep(self.delay / 1000)
