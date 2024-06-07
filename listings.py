
class Listings():
    def __init__(self, listing_id='', nickname='', category='', quantity=2, floor=float('inf')):
        self.listing_id = listing_id 
        self.category = category 
        self.nickname = nickname
        self.quantity = quantity 
        self.floor = floor

    def to_dict(self):
        return {
            "nickname" : self.nickname,
            "listing_id" : self.listing_id,
            "category" : self.category,
            "quantity" : self.quantity,
            "floor" : self.floor
        }

    def __str__(self):
        pass
