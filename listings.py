#TODO change this name since it holds events too
class Listings:
    def __init__(
        self, listing_id="", nickname="", category="", quantity=2, floor=999999999
    ):
        self.listing_id = listing_id
        self.category = category
        self.nickname = nickname
        self.quantity = quantity
        self.floor = floor

    def to_dict(self):
        return {
            "nickname": self.nickname,
            "listing_id": self.listing_id,
            "category": self.category,
            "quantity": self.quantity,
            "floor": self.floor,
        }

    def __str__(self):
        pass

class Events:
    def __init__(self, listing_id, url, total_tickets=0):
        self.listing_id = listing_id
        self.url = url
        self.total_tickets = total_tickets

    def to_dict(self):
        return {
            "listing_id": self.listing_id,
            "url": self.url,
            "total_tickets": self.total_tickets,
        }

