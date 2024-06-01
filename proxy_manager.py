class ProxyManager():
    """
    Manages the proxies used to monitor
    """
    def __init__(self, proxy_path=None):
        self.proxies = []
        if proxy_path:
            self.load_proxies(proxy_path)

    def load_proxies(self, proxy_path):
        with open(proxy_path, "r") as f:
            for proxy in f.read().splitlines():
                proxyElements = proxy.split(":")
                self.proxies.append(
                    {
                        "http": f"http://{proxyElements[2]}:{proxyElements[3]}@{proxyElements[0]}:{proxyElements[1]}"
                    }
                )

    def get_proxies(self):
        return self.proxies
            
