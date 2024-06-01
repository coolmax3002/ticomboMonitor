import requests 

class Monitor():
    def __init__(self, proxy_path, listings=[], delay=5555):
        self.listings = listings 
        self.floor_prices = []
        self.proxies = []
        self.monitor_status = False
        self.delay = delay
        with open(proxy_path, 'r') as f:
            for proxy in f.read().splitlines():
                proxyElements = proxy.split(':')
                self.proxies.append({'http' : f"http://{proxyElements[2]}:{proxyElements[3]}@{proxyElements[0]}:{proxyElements[1]}"})

    def set_delay(self, delay):
        self.delay = delay

    def modify_proxies(self, proxies, mode='replace'):
        self.proxies = proxies
        #TODO create other modees like add/remove

    def start_monitor(self):
        pass

    def add_listing(self, listing_id, catergory, quantity):
        self.listings.append([listing_id, catergory, quantity])

    def monitor(self):
        #TODO check if proxies exist
        for i, proxy in enumerate(self.proxies):
            for j, listing in enumerate(self.listings):
                r = requests.get(f'https://www.ticombo.com/prod/discovery/events/{listing[0]}/listings?limit=20&include=$total&populate=rel.user:firstName,displayName,urlPicture,trustedSeller,metadata,features.priceOptimization,representative%7Creservations:amount,expiresAt,price&sort=bestprice&categories=1:{listing[1]}&quantity={listing[2]}')
                if r.status_code == 200:
                    data = r.json()
                    tickets = data.get('payload', [])
                    print(tickets[0]['price']['selling']['value'])
                    print(i)
                    break
                else:
                    print(r.status_code)
            break


def main():
    listing_id = '625b7b5d-c70a-434c-8939-1491fbba8e19'
    quantity = '1' 
    catergory = 'Category%20Gold'
    ticombo = Monitor(proxy_path='proxies.txt')
    ticombo.add_listing(listing_id, catergory, quantity)
    ticombo.monitor()

if __name__ == "__main__":
    main()
