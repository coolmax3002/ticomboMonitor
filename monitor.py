import requests
import math
import json
import threading
import time
from time import sleep
from proxy_manager import ProxyManager
from settings_manager import SettingsManager
from webhook_manager import WebhookManager
from urllib.parse import urlparse, parse_qs
from listings import Listings, Events


class Monitor:
    """
    A monitor class to create a lowest price monitor for ticombo listings
    """

    def __init__(self, proxy_path=None, listings=[], delay=60000):
        self.proxy_manager = ProxyManager(proxy_path)
        self.settings_manager = SettingsManager()
        self.webhook_manager = WebhookManager(
            webhook_url=self.settings_manager.get_setting("webhook")
        )
        self.listings = []
        self.events = []
        self.url_map = self.settings_manager.get_url_map()
        self.running = False
        self.thread = None
        self.vivid = None 
        self.stubhub = None
        self.delay = delay
        self.euro_exchange_rate = 1.089

        listings = self.settings_manager.get_listings()
        events = self.settings_manager.get_events()
        print(listings)
        for listing in listings:
            self.listings.append(
                Listings(
                    listing_id=listing["listing_id"],
                    category=listing["category"],
                    quantity=listing["quantity"],
                    nickname=listing["nickname"],
                    floor=listing["floor"]
                )
            )

        for event in events:
            self.events.append(
                Events(
                    listing_id=event["listing_id"],
                    url=event["url"],
                    total_tickets=event["total_tickets"]
                )
            )

    def set_delay(self, delay):
        self.delay = delay

    def start_monitor(self):
        self.running = True
        self.thread = threading.Thread(target=self.monitor, args=())
        self.thread.start()

    def start_vivid_monitor(self):
        self.running = True
        self.thread = threading.Thread(target=self.vivid_monitor, args=())
        self.thread.start()


    def stop_monitor(self):
        self.running = False
        sleep(5)
        self.thread.join()
        print("Monitor Stopped!")

    def get_monitor_status(self):
        return self.running

    def add_listing(self, listing_id, category, quantity, nickname):
        # TODO pull all the categories and choose the closest one to the one provided
        new_listing = Listings(
            listing_id=listing_id,
            category=category,
            quantity=quantity,
            nickname=nickname,
        )
        self.listings.append(new_listing)
        self.settings_manager.set_listings(self.listings)
        # TODO add url to the listing class instead of passing url too
        self.webhook_manager.send_new_listing_webhook(
            new_listing, self.url_map[new_listing.listing_id]
        )

    def add_event(self, listing_id, url):
        new_event = Events(
            listing_id=listing_id,
            url=url
        )
        self.events.append(new_event)
        self.settings_manager.set_events(self.events)

    def grab_listing_id(self, url):
        # grab listing name from url
        parsed_url = urlparse(url)
        url_parts = parsed_url.path.split("/")
        listing_name = url_parts[-1]

        api_url = (
            f"https://www.ticombo.com/prod/discovery/events?id={listing_name}&limit=1"
        )

        r = requests.get(api_url)
        if r.status_code == 200:
            data = r.json()
            try:
                listing_id = data["payload"][0]["eventId"]
                self.url_map[listing_id] = url
                self.settings_manager.set_url_map(listing_id, url)
            except Exception as e:
                print("listing ID coud not be found")
                return None
            return listing_id
        else:
            print(f"events api request failed {r.status_code=}")
            return None

    def monitor(self):
        # TODO check if proxies exist
        while True:
            for i, proxy in enumerate(self.proxy_manager.get_proxies()):
                for j, listing in enumerate(self.listings):
                    if not self.running:
                        print("monitor has been requested to stop")
                        return
                    print("making request")
                    r = requests.get(
                        f"https://www.ticombo.com/prod/discovery/events/{listing.listing_id}/listings?limit=20&include=$total&populate=rel.user:firstName,displayName,urlPicture,trustedSeller,metadata,features.priceOptimization,representative%7Creservations:amount,expiresAt,price&sort=bestprice&categories=1:{listing.category}&quantity={listing.quantity}",
                        proxies=proxy,
                    )
                    if r.status_code == 200:
                        data = r.json()
                        tickets = data.get("payload", [])
                        try:
                            print("trying to grab price")
                            floor = math.ceil(float(tickets[0]["price"]["sellingEur"]) * self.euro_exchange_rate)
                            if floor != listing.floor: 
                                print(f"New price!! {floor=}")
                                self.webhook_manager.send_webhook(
                                    listing.nickname,
                                    floor,
                                    listing.floor,
                                    self.url_map[listing.listing_id],
                                )
                                print("webhook sent")
                                listing.floor = floor
                                self.settings_manager.set_listings(self.listings)
                            else:
                                print("no change")
                        except Exception as e:
                            print("couldn't grab floor price")
                    else:
                        print(r.status_code)

                    #check events now
                    event = self.events[j % len(self.events)]
                    events_resp = requests.get(
                        f"https://www.ticombo.com/prod/discovery/events/{event.listing_id}/listings/stats?platform=tc_de",
                        proxies=proxy,
                    )
                    try:
                        print("grabbing number of tickets left")
                        data = events_resp.json()
                        payload = data.get("payload", {})
                        total_tickets = payload["availableTickets"]
                        if total_tickets != event.total_tickets:
                            #TODO change this hardcode, set nickname in event
                            self.webhook_manager.send_webhook_event("RG womens final", total_tickets, event.total_tickets, event.url)
                            event.total_tickets = total_tickets
                            self.settings_manager.set_events(self.events)
                        print("stock request complete")
                    except Exception as e:
                        print("couldn't grab number of tickets left")
                    if self.running: 
                        time.sleep(self.delay / 1000)

    def vivid_monitor(self):
        current_listing_count = 1 
        current_lowest_price = 1
        url = "https://www.vividseats.com/kendrick-lamar-tickets-inglewood-kia-forum-6-19-2024--concerts-rap-hip-hop/production/5013509?productionId=5013509"
        production_id = 5013509
        print("vivid monitor started")
        headers = {
            'Accept': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
        }
        while True:
            for i, proxy in enumerate(self.proxy_manager.get_proxies()):
                if not self.running:
                    print("monitor has been requested to stop")
                    return
                print("making request")
                r = requests.get(f"https://www.vividseats.com/hermes/api/v1/listings?productionId={production_id}&currency=USD", headers=headers, proxies=proxy)
                if r.status_code != 200:
                    print(f"request failed {r.status_code=}")
                else:
                    data = r.json()
                    listing_count = data.get("global")
                    print(listing_count)
                    listing_count = int(listing_count[0]["listingCount"])
                    lowest_price = data.get("tickets")
                    lowest_price = float(lowest_price[0]["p"])
                    if listing_count != current_listing_count:
                        self.webhook_manager.send_webhook_event("Kendrick Lamar", listing_count, current_listing_count, url)
                        current_listing_count = listing_count

                    if lowest_price != current_lowest_price:
                        self.webhook_manager.send_webhook("Kendrick Lamar", lowest_price, current_lowest_price, url)
                        current_lowest_price = lowest_price
                if self.running:
                    time.sleep(self.delay / 1000)
    
    def stubhub_monitor(self):
        




