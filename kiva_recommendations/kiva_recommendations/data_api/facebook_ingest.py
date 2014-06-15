__author__ = 'rakesh'

#Facebook Graph Explorer: https://developers.facebook.com/tools/explorer/145634995501895/?method=GET&path=me%3Ffields%3Did%2Cname&version=v2.0

from facepy import GraphAPI
from reverse_geocode import ReverseGeoCode
from datetime import datetime


class FacebookIngest():

    def __init__(self, logger_instance, oauth_access_token=None):

        if oauth_access_token != None:
            try:
                self.graph = GraphAPI(oauth_access_token)
            except:
                raise Exception('Could not instantiate Facebook GraphAPI with provided access token')

        else:
            raise Exception('No facebook access token provided.')

        self.user_id = self.get_user_id()
        self.reverse_geocoder = ReverseGeoCode()
        self.logger = logger_instance

    def get_user_id(self):
        resp = self.graph.get('/v2.0/me?fields=id')
        return resp['id']

    def get_location_of_residence(self):
        profile = self.graph.get('/v2.0/me?fields=location')
        return profile['location']['name']

    def get_last_location_visited(self):
        profile = self.graph.get('/v2.0/me?fields=location')
        print profile['location']['name']

    def get_languages(self):
        languages = set()
        resp = self.graph.get('/v2.0/me?fields=languages')

        for l in resp['languages']:
            languages.add(l['name'])

        return list(languages)


    def get_tagged_places(self):
        countries = set()

        try:
            resp = self.graph.get('/v2.0/' + self.user_id + '/tagged_places')
        except:
            raise Exception('Error getting tagged_places from Facebook')

        for place_dict in resp["data"]:
            country = self.reverse_geocoder.reverse_geocode_country(place_dict["place"]["location"]["latitude"],
                                                                    place_dict["place"]["location"]["longitude"])

            if country:
                countries.add(country)

            self.logger.error(str(datetime.now()) + ":" + "countries_returned: " + str(list(countries)))

        return list(countries)
