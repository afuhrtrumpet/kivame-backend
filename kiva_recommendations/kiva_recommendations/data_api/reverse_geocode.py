__author__ = 'rakesh'

from googlegeocoder import GoogleGeocoder

class ReverseGeoCode():

    def __init__(self):
        pass


    def reverse_geocode_country(self, latitude, longitude):
        country = None

        try:
            reverse = self.geocoder.get((latitude, longitude))
        except:
            raise Exception('Error reverse geo-coding the location')

        try:
            address = reverse[0].formatted_address
            address_tokens = address.split()
            country = address_tokens[len(address_tokens) - 1]

        except:
            raise Exception('Error post-processing the location into country')

        return country