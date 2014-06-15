__author__ = 'rakesh'

from googlegeocoder import GoogleGeocoder
from geopy import YahooPlaceFinder


import json
import urllib2


import urllib
import urllib2
import json
import time

from factual import Factual

FACTUAL_KEY = "8Oyh0iOezwTHc5tAUAANK9lYL1hprzkamtfEu4kR"
FACTUAL_SECRET = "qezuK3PdoZGu6otRGbqy4hYc6QPMVAtqYqCj4CWg"


class NominatimReverseGeocoder(object):
    def __init__(self, base_url = "http://open.mapquestapi.com/nominatim/v1/reverse?format=json"):
        self.base_url = base_url + "&%s"

    def geocode(self, lat, lon, zoom = 18):

        params = { 'lat' : lat , 'lon' : lon , 'zoom' : zoom}

        url = self.base_url % urllib.urlencode(params)
        data = urllib2.urlopen(url)
        response = data.read()

        return self.parse_json(response)

    def parse_json(self, data):
        try:
            jsondata = json.loads(data)

            if "error" in data:
              jsondata['full_address'] = jsondata['error']
            elif "display_name" in data:
              jsondata['full_address'] = jsondata['display_name']
            else:
              jsondata['full_address'] = "Unknown"

        except json.JSONDecodeError:
            jsondata = []

        return jsondata



class ReverseGeoCode():

    def __init__(self):
        self.nrgc = NominatimReverseGeocoder()
        self.factual = Factual(FACTUAL_KEY, FACTUAL_SECRET)


    def reverse_geocode_country_google(self, latitude, longitude):
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

    def reverse_geocode_country_nominatim(self, latitude, longitude):

        country = None
        reverse = None

        try:
            reverse = self.nrgc.geocode(latitude, longitude)
        except:
            raise Exception('Error reverse geo-coding the location via Nominatim')

        try:
            print reverse['address']['country']
            country = reverse['address']['country']

        except:
            raise Exception('Error post-processing the Nominatim reverse geocoded location into country')

        return country


    def reverse_geocode_country_factual(self, latitude, longitude):

        latitude = float(latitude)
        longitude = float(longitude)

        country = None
        query = None

        try:
            query = self.factual.geocode({'$point': [latitude, longitude]})
            data = query.data()

        except Exception,e:
            print str(e)
            raise Exception('Error reverse geo-coding the location via Factual')

        try:
            #print data
            if len (data) > 0:
                country = data[0]['country']

        except Exception,e:
            print str(e)
            raise Exception('Error reverse geo-coding the location via Factual')

        return country



    def reverse_geocode_country(self, latitude, longitude):

        country = None

        try:
            country = self.reverse_geocode_country_factual(latitude, longitude)
        except:
            raise Exception('Factual Reverse Coding failed')

        return country