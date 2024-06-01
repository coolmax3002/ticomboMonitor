from cli import MonitorCLI

def main():
    listing_id = '625b7b5d-c70a-434c-8939-1491fbba8e19'
    quantity = '1' 
    catergory = 'Category%20Gold'
    cli = MonitorCLI()
    cli.cmdloop("Starting ticombo monitor CLI. Type 'help' for available commands")

if __name__ == "__main__":
    main()
