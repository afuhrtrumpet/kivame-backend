__author__ = 'rakesh'

from googlegeocoder import GoogleGeocoder


import json
import urllib2


import urllib
import urllib2
import json
import time


class ReverseGeoCode():

    def __init__(self):
        self.geocoder = GoogleGeocoder()

    def reverse_geocode_country(self, latitude, longitude):
        country = None
        reverse = None

        attempts = 0
        success = False

        while success != True and attempts < 3:
            try:
                attempts += 1
                reverse = self.geocoder.get((latitude, longitude))
            except:
                time.sleep(1)
                continue

            success = True

        if success == False:
            raise Exception('Error reverse geo-coding the location via Google')

        try:
            address = reverse[0].formatted_address
            address_tokens = address.split()
            country = address_tokens[len(address_tokens) - 1]

        except:
            raise Exception('Error post-processing the Google reverse geocoded location into country')

        return country



def main():

    rgc = ReverseGeoCode()
    country = rgc.reverse_geocode_country(30, 70)

if __name__ == '__main__':
    main()
