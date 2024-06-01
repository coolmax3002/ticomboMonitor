from monitor import Monitor

def main():
    listing_id = '625b7b5d-c70a-434c-8939-1491fbba8e19'
    quantity = '1' 
    catergory = 'Category%20Gold'
    ticombo = Monitor(proxy_path='proxies.txt')
    #ticombo.add_listing(listing_id, catergory, quantity, 'rg womens final')
    ticombo.webhook_manager.set_webhook_url('https://discord.com/api/webhooks/1246319073495875654/CyAySPByd8N3iRPvMwfoNLyBCD4q-fdYVHiRm-vwopycaN0mNpZFMITkey4KRtdKa-A5')
    ticombo.start_monitor()

if __name__ == "__main__":
    main()
