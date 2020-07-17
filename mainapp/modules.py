from .models import *


class Pricing:
    def __init__(self):
        self.current_price = 1.50
        self.location_factor = 0.02
        self.rate_history_factor = 0.00
        self.gallons_requested_factor = 0.3
        self.company_profit_factor = 0.1

    def get_suggested_price(self, userid, gallon_req):
        sugg_price = self.current_price + self.get_margin(userid, gallon_req)
        return sugg_price

    def get_margin(self, userid, gallon_req):
        margin = (self.get_location_factor(userid) - self.get_rate_history_factor(userid) +
                  self.get_gallons_requested_factor(gallon_req) + self.company_profit_factor) * self.current_price
        return margin

    def get_location_factor(self, userid):
        state = ClientInformations.objects.get(userid=userid).state
        if state != 'TX':
            self.location_factor = 0.04
        return self.location_factor

    def get_rate_history_factor(self, userid):
        history = FuelQuotes.objects.filter(userid=userid).exists()
        if history:
            self.rate_history_factor = 0.01
        return self.rate_history_factor

    def get_gallons_requested_factor(self, gallon_req):
        if gallon_req > 1000:
            self.gallons_requested_factor = 0.02
        return self.gallons_requested_factor
