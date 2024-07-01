from time import sleep

from requests import request
from settings_manager import SettingsManager
from proxy_manager import ProxyManager
import threading
from webhook_manager import WebhookManager


class TicomboMonitor():
    def __init__(self, proxy_path='proxies.txt', delay=60000) -> None:
        self.ticombo_config = SettingsManager(settings_path="ticombo_settings.json")
        self.proxy_manager = ProxyManager(proxy_path)
        self.webhook_manager = WebhookManager(
            webhook_url=self.settings_manager.get_setting("webhook")
        )
        self.running = False
        self.delay = delay
        self.ticombo_thread = None
        self.events = []
        events = self.ticombo_config.get_events()
        for event in events:
            self.events.append(
                Events(
                    listing_id=event["listing_id"],
                    url=event["url"],
                    total_tickets=event["total_tickets"]
                )
            )


    def start_ticombo_monitor(self):
        if self.running:
            print("monitor running already...")
            return

        self.running = True
        self.ticombo_thread = threading.Thread(target=self.ticombo_monitor, args=())
        self.ticombo_thread.start()

    def stop_ticombo_monitor(self):
        if not self.running or not self.ticombo_thread:
            print("Monitor is not running...")
            return
        
        self.running = False
        sleep(self.delay)
        self.ticombo_thread.join()
 
    def ticombo_monitor_status(self):
        return self.running

    def ticombo_monitor(self):
        while True:
            for i, proxy in enumerate(self.proxy_manager.get_proxies()):
                for j, event in enumerate(self.events):
                    if not self.running:
                        return

                    event_req = requests.get(
                        f"https://www.ticombo.com/prod/discovery/events/{event.listing_id}/listings/stats?platform=tc_de",
                        proxies=proxy,
                    )
                    
                    try:
                        data = event_req.json()
                        payload = data.get("payload", {})
                        total_tickets = payload["availableTickets"]
                        if total_tickets != event.total_tickets:
                            #TODO change this hardcode, set nickname in event
                            self.webhook_manager.send_webhook_event("RG womens final", total_tickets, event.total_tickets, event.url)
                            event.total_tickets = total_tickets
                            self.settings_manager.set_events(self.events)
                    except expression as e:
                        pass

                    if self.running: 
                        time.sleep(self.delay / 1000)
