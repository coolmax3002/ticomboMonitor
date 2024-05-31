import requests 

class Monitor():
    def __init__(self, proxy_path, listings=[], delay=5555):
        self.listings = listings 
        self.proxies = []
        self.delay = delay
        with open(proxy_path, 'r') as f:
            for proxy in f.readlines():
                self.proxies.append(proxy)

    def set_delay(self, delay):
        self.delay = delay

    def modify_proxies(self, proxies, mode='replace'):
        self.proxies = proxies
        #TODO create other modees like add/remove

    def start_monitor(self):
        pass

    def monitor(self):
        #TODO check if proxies exist
        for _ in range(20):
            for listing in self.listings:
                r = requests.get(f'https://www.ticombo.com/prod/discovery/events/{listing[0]}/listings?limit=20&include=$total&populate=rel.user:firstName,displayName,urlPicture,trustedSeller,metadata,features.priceOptimization,representative%7Creservations:amount,expiresAt,price&sort=bestprice&categories=1:{listing[1]}&quantity={listing[2]}')
                if r.status_code == 200:
                    data = r.json()
                    tickets = data.get('payload', [])
                    print(tickets[0])


def main():
    listing_id = '625b7b5d-c70a-434c-8939-1491fbba8e19'
    quantity = '1' 
    catergory = 'Catergory%20Gold'

if __name__ == "__main__":
    main()
