import requests
import threading
import time

class Monitor():
    """
    A monitor class to create a lowest price monitor for ticombo listings
    """

    def __init__(self, proxy_path=None, listings=[], delay=5555):
        self.listings = listings 
        self.floor_prices = []
        self.proxies = []
        self.running = False
        self.monitor_status = False
        self.thread = None
        self.webhook = ''
        self.nickname = ''
        self.delay = delay
        self.check_settings()
        if proxy_path:
            self.set_proxies(proxy_path)

    def set_proxies(self, proxy_path):
        with open(proxy_path, 'r') as f:
            for proxy in f.read().splitlines():
                proxyElements = proxy.split(':')
                self.proxies.append({'http' : f"http://{proxyElements[2]}:{proxyElements[3]}@{proxyElements[0]}:{proxyElements[1]}"})

    def set_delay(self, delay):
        self.delay = delay

    def modify_proxies(self, proxies, mode='replace'):
        self.proxies = proxies
        #TODO create other modees like add/remove

    def send_webhook(self, nickname, new_price):
        if self.webhook == '':
            print('Set webhook!')
            return
        message = {
            "username" : nickname,
            "content" : new_price
        }
        r = requests.post(self.webhook, data=message)
        if 200 <= r.status_code < 300:
            print(f"Webhook sent {result.status_code}")
        else:
            print(f"Not sent with {result.status_code}, response:\n{result.json()}")

    def start_monitor(self):
        self.running = True
        self.thread = threading.Thread(target=self.monitor, args=())
        self.thread.start()

    def stop_monitor(self):
        self.running = False
        self.thread.join()

    def check_settings(self):
        with open('settings.json') as j:
            d = json.load(j)
            if d['webhook'] != '':
                self.webhook = d['webhook']
            if len(d['listings']) > 0:
                print('no listings')

    def set_webhook_url(self, webhook):
        self.webhook = webhook

    def get_monitor_status(self):
        return self.running

    def add_listing(self, listing_id, catergory, quantity, nickname):
        self.nickname = nickname
        self.listings.append([listing_id, catergory, quantity])
        self.floor_prices.append(['EUR', 999999999999999999999])

    def monitor(self):
        #TODO check if proxies exist
        while self.running:
            for i, proxy in enumerate(self.proxies):
                for j, listing in enumerate(self.listings):
                    print("making request")
                    r = requests.get(f'https://www.ticombo.com/prod/discovery/events/{listing[0]}/listings?limit=20&include=$total&populate=rel.user:firstName,displayName,urlPicture,trustedSeller,metadata,features.priceOptimization,representative%7Creservations:amount,expiresAt,price&sort=bestprice&categories=1:{listing[1]}&quantity={listing[2]}', proxies=proxy)
                    if r.status_code == 200:
                        data = r.json()
                        tickets = data.get('payload', [])
                        try:
                            print("trying to grab price")
                            floor = tickets[0]['price']['selling']['value']
                            currency = tickets[0]['price']['selling']['currency']
                            if self.floor_prices[j][0] == 'EUR' and self.floor_prices[j][1] > floor:
                                self.floor_prices[j][1] = floor
                                print('New price!!')
                                self.send_webhook(self.nickname, floor)
                        except Exception as e:
                            print("couldn't grab floor price")
                    else:
                        print(r.status_code)
                    time.sleep(self.delay)
                break



