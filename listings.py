
class Listings():
    def __init__(self, listing_id='', nickname='', catergory='', quantity=2, floor=float('inf')):
        self.listing_id = listing_id 
        self.catergory = catergory 
        self.nickname = nickname
        self.quantity = quantity 
        self.floor = floor

    def to_dict(self):
        return {
            "nickname" : self.nickname,
            "listing_id" : self.listing_id,
            "catergory" : self.catergory,
            "quantity" : self.quantity,
            "floor" : self.floor
        }

