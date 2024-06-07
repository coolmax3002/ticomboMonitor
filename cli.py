from cmd import Cmd
from monitor import Monitor
import shlex


class MonitorCLI(Cmd):
    monitor = Monitor(proxy_path="proxies.txt")
    prompt = "ticomboMonitor> "

    def do_start_monitor(self, arg):
        if self.monitor.get_monitor_status():
            print("Monitor already running")
            return
        invalid_settings = self.monitor.settings_manager.valid_settings()
        if not invalid_settings:
            self.monitor.start_monitor()
        else:
            if invalid_settings == 1:
                print("no listings are set")
            else:
                print("webhook is not set")

    def do_stop_monitor(self, arg):
        if self.monitor.get_monitor_status():
            print("Stopping Monitor...")
            self.monitor.stop_monitor()
        else:
            print("Monitor is not running")

    def do_add_listing(self, arg):
        if arg:
            args = shlex.split(arg)
            if len(args) != 1:
                print("Wrong number of arguments passed: add listing <url>")
                return
            if self.monitor.get_monitor_status():
                print("Monitor is runnnig, restarting to apply changes...")
                self.do_stop_monitor()
            listing_id = self.monitor.grab_listing_id(args[0])
            if not listing_id:
                print("Invalid url, error message above^")
                return
            category = input("Category to monitor('all' for all categories): ")
            # TODO category logic
            quantity = input("Quantity to monitor(1-4): ")
            while not quantity.isdigit() and 1 <= quantity <= 4:
                quantity = input("provide a valid quantity between 1 and 4: ")
            nickname = input("Provide a nickname for this event: ")
            self.monitor.add_listing(listing_id, category, quantity, nickname)
        else:
            print("No link provided")

    def do_set_webhook(self, arg):
        if not arg:
            print(
                "please include your webhook in the command: set_webhook <webhook_url>"
            )
            return
        args = shlex.split(arg)
        self.monitor.webhook_manager.set_webhook_url(args[0])
        self.monitor.settings_manager.set_setting("webhook", args[0])
        print(
            "Webhook successfuly saved. Test the webhook with the command: test_webhook"
        )
        return

    def do_test_webhook(self, arg):
        if self.monitor.webhook_manager.get_webhook_url() == "":
            print("webhook not set!")
            return
        self.monitor.webhook_manager.test_webhook()
        return

    def do_show_webhook(self, arg):
        if self.monitor.webhook_manager.get_webhook_url() == "":
            print("webhook not set!")
            return
        print(self.monitor.webhook_manager.get_webhook_url())

    def do_show_listings(self, args):
        for listing in self.monitor.listings:
            print(listing.to_dict())
