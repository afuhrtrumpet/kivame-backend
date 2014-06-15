__author__ = 'rakesh'

from googlegeocoder import GoogleGeocoder
from facepy import GraphAPI
about_me_token = "CAACEdEose0cBACNbgZCsTIk0pwIxHa2UGYhKyrXZAxYfnkiUu8h96LmH1DqELHokGz5OONDxZBgxDKfBb6VzjywwsbrjAhdSpFEgDC3rkZAhTxYQ0XPM5bWh8OqvQsCqBZBl3FEAoEZBbU9PGoqWVZCIhIVudflXBvDntDBPRd2seI6Vhap6ACwThRbxhezZA57qOwUAsyJGsAZDZD"

class FacebookIngest():

    def __init__(self, oauth_access_token):
        self.graph = graph = GraphAPI(oauth_access_token)
        self.user_id = self.get_user_id()

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

    def get_tagged_photo_locations(self):
        geocoder = GoogleGeocoder()

        locations = ()

        resp = self.graph.get('/v2.0/' + self.user_id + '/photos')
        for photo in resp['data']:
            x = photo['tags']['data'][0]['x']
            y = photo['tags']['data'][0]['y']
            print str(x) + ", " + str(y)
            reverse = geocoder.get((x, y))
            print reverse[0].formatted_address

            print str(y) + ", " + str(x)
            reverse = geocoder.get((y, x))
            print reverse[0].formatted_address

        return locations


def main ():
    fi = FacebookIngest(about_me_token)

    print "User Id:", fi.user_id
    #print "Location of Residence:", fi.get_location_of_residence()
    print "Languages:", fi.get_languages()

    #print fi.get_tagged_photo_locations()

if __name__ == "__main__":
    main()
