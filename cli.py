from cmd import Cmd 
from monitor import Monitor
import shlex

class MonitorCLI(Cmd):
    prompt = 'ticomboMonitor> '

    def __init__(self):
        super.__init__()
        self.monitor = Monitor(proxy_path='proxies.txt')

    def do_start_monitor(self, arg):
        if self.monitor.get_monitor_status():
            print("Monitor already running")
            return
        if self.monitor.settings_manager.validSettings():
            self.monitor.start_monitor()
        else:
            print("Monitor settings are not set")
    
    def do_stop_monitor(self, arg):
        if self.monitor.get_monitor_status():
            print("Stopping Monitor...")
        else:
            print("Monitor is not running")

    def do_add_listing(self, arg):
        if arg:
            args = shlex.split(arg)
            if len(args) != 4:
                print("Wrong number of arguments passed: add listing <url> <catergory> <quantity> <nickname>")
                return            
            print("Monitor stopping to apply changes")
            if self.monitor.get_monitor_status():
                print("Monitor is runnnig, restarting to apply changes...")
                self.do_stop_monitor()
            listing_id = self.monitor.grab_listing_id(args[0])
            if not listing_id:
                print("Invalid url, error message above^")
                return
            self.monitor.add_listing(listing_id, args[1], arg[2], args[3])
        else:
            print("No link provided")
