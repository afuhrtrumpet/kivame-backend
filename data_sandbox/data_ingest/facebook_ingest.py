__author__ = 'rakesh'

#Facebook Graph Explorer: https://developers.facebook.com/tools/explorer/145634995501895/?method=GET&path=me%3Ffields%3Did%2Cname&version=v2.0

from googlegeocoder import GoogleGeocoder
from facepy import GraphAPI
about_me_token = "CAACEdEose0cBACNbgZCsTIk0pwIxHa2UGYhKyrXZAxYfnkiUu8h96LmH1DqELHokGz5OONDxZBgxDKfBb6VzjywwsbrjAhdSpFEgDC3rkZAhTxYQ0XPM5bWh8OqvQsCqBZBl3FEAoEZBbU9PGoqWVZCIhIVudflXBvDntDBPRd2seI6Vhap6ACwThRbxhezZA57qOwUAsyJGsAZDZD"

class FacebookIngest():

    def __init__(self, oauth_access_token):
        self.graph = graph = GraphAPI(oauth_access_token)
        self.user_id = self.get_user_id()
        self.geocoder = GoogleGeocoder()

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

        return languages

    def get_tagged_places(self):
        countries = set()

        resp = self.graph.get('/v2.0/' + self.user_id + '/tagged_places')

        for place_dict in resp["data"]:
            reverse = self.geocoder.get((place_dict["place"]["location"]["latitude"], place_dict["place"]["location"]["longitude"]))
            address = reverse[0].formatted_address
            address_tokens = address.split()
            country =  address_tokens[len(address_tokens) - 1]
            countries.add(country)

        return countries


def main ():
    fi = FacebookIngest(about_me_token)

    #print "User Id:", fi.user_id
    #print "Location of Residence:", fi.get_location_of_residence()
    #print "Languages:", fi.get_languages()
    print "Tagged Places:", fi.get_tagged_places()

if __name__ == "__main__":
    main()
