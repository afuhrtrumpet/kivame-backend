""" Given a country find recent loans 
"""

import requests
import random
import pycountry
import logging
import logging.handlers
from datetime import datetime

LOG_FILENAME = 'kiva_api_requests_errors'

from facebook_ingest import FacebookIngest

class KivaAPI():
    """ Methods to parse Kiva API 
    """
    def __init__(self):

        self.logger = logging.getLogger('KivaAPI')
        self.logger.setLevel(logging.DEBUG)
        handlr = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=10000, backupCount=1000)
        self.logger.addHandler(handlr)


    def find_country_code(self, country_name):
    
        # Custom name wrangling
        if country_name == "USA" or country_name == "US":
            country_name = "United States"

        #  Define country hash 
        countries = {}
        for country in pycountry.countries:
            countries[country.name] = country.alpha2

        country_id = countries.get(country_name, 'Unknown code')
        
        return country_id 

    def get_loan_by_id(self, id):
        """  Get a single loan based on id
        """
        loan = {}
        url = 'http://api.kivaws.org/v1/loans/'+str(id)+'.json'
        response = requests.get(url)
        if response.status_code != requests.codes.ok:
            self.handle_error(response.status_code)

        response_dict = response.json()

        #print response_dict['loans'][0]

        #Pick up the necessary things
        loan['id'] = response_dict['loans'][0]['id']

        #images and image id
        loan['image_id'] = response_dict['loans'][0]['image']["id"]
        loan['short_image_url'] = 'http://www.kiva.org/img/w250/'+str(id)+'.jpg'
        loan['large_image_url'] = 'http://www.kiva.org/img/w800/'+str(id)+'.jpg'

        loan['borrower_name'] =  response_dict['loans'][0]['name']
        loan['country'] = response_dict['loans'][0]['location']['country']
        loan['country_code'] = response_dict['loans'][0]['location']['country_code']
        loan['short_description'] = response_dict['loans'][0]['use']

        try:
            loan['long_description'] = response_dict['loans'][0]['description']['texts']['en']
        except KeyError:
            loan['long_description'] = ""

        loan['loan_amount'] = response_dict['loans'][0]['loan_amount']
        loan['funded_amount'] = response_dict['loans'][0]['funded_amount']
        loan['funded_percentage'] = (loan['funded_amount'] * 1.0 / loan['loan_amount']) * 100
        #Badges


        #Get Partner Rating
        url = 'http://api.kivaws.org/v1/partners/'+str(response_dict['loans'][0]['partner_id'])+'.json'
        response = requests.get(url)

        if response.status_code != requests.codes.ok:
            self.handle_error(response.status_code)

        response_dict_partner = response.json()
        loan['partner_rating'] = response_dict_partner['partners'][0]['rating']

        return loan

    def get_ids_for_loans(self, loans):
         return [loan['id'] for loan in loans]

    def get_loans_fathers_day(self):
        
        url = 'http://api.kivaws.org/v1/loans/search.json&status=fundraising&gender=male&borrower_type=individuals'
        response = requests.get(url)
        if response.status_code != requests.codes.ok:  self.handle_error(response.status_code)
        response_dict = response.json()
        loans = response_dict['loans'] # 1st page only / 20 loans

        return loans

    def get_loans_expiring_soon(self):
        
        url = 'http://api.kivaws.org/v1/loans/search.json&status=fundraising&sort_by=expiration'
        response = requests.get(url)
        if response.status_code != requests.codes.ok:  self.handle_error(response.status_code)
        response_dict = response.json()
        loans = response_dict['loans'] # 1st page only / 20 loans

        return loans

    def get_loans_by_country(self, country_code):
        """  Get loans based on country
        """

        loans = []
        if len(country_code) == 2:
            url = 'http://api.kivaws.org/v1/loans/search.json&status=fundraising&country_code='+country_code
            response = requests.get(url)
            if response.status_code != requests.codes.ok:
                self.handle_error(response.status_code)

            response_dict = response.json()
            loans = response_dict['loans'] # 1st page only / 20 loans
        else:
            print('Invalid country code')

        return loans

    def get_loans_sample(self):
        """  Get 1st page of loans
        """
        url = 'http://api.kivaws.org/v1/loans/newest.json'
        response = requests.get(url)
        if response.status_code != requests.codes.ok:  self.handle_error(response.status_code)
        response_dict = response.json()
        
        return response_dict['loans'] # 1st page only / 20 loans

    def get_loans_all(self):
        """  Get all loans
        """

        url = 'http://api.kivaws.org/v1/loans/newest.json'
        response = requests.get(url)
        if response.status_code != requests.codes.ok:  self.handle_error(response.status_code)
        response_dict = response.json()
        total_loans = response_dict['loans'] # 1st page only / 20 loans

        # Go through each page of API call
        # XXX: Good chance of timing out
        paging = response_dict['paging']
        page = 1
        n_paging = paging["pages"]
        while page <= n_paging:
            page += 1
            url = url+'&page='+str(page)
            response = requests.get(url)
            if response.status_code != requests.codes.ok:  self.handle_error(response.status_code)

            response_dict = response.json()
            total_loans += response_dict['loans']

        return total_loans      

    def get_team_list(self,lender_id):
        """ Return a list of teams a lender belongs to 
        """
        url = 'https://api.kivaws.org/v1/lenders/'+lender_id+'/teams.json'
        response = requests.get(url)
        if response.status_code != requests.codes.ok:  self.handle_error(response.status_code)

        data = response.json()
        team_list = data['teams']
        return team_list

    def get_lender_in_team_list(self, team_list, team_id):
        """ Return the list of lenders in a team 
        """
        url = 'https://api.kivaws.org/v1/teams/'+str(team_list[team_id]['id'])+'/lenders.json'
        response = requests.get(url)
        if response.status_code != requests.codes.ok:  self.handle_error(response.status_code)

        data = response.json()

        # Get the list of lenders on this team
        lender_list = data['lenders']
        #print 'lender_list has '+ str(len(lender_list))+ ' entries'
        return lender_list

    def build_lender_id_list(self, lender_list):
        """  Return a list of comma-separated ids from the list of lenders
        """
        every_id = ''
        for j in range(len(lender_list)):
        # When lenders choose to be anonymous, we do not check their invitation count
            if ('name' in lender_list[j].keys()):
                if (lender_list[j]['name'] != 'Anonymous'):
                    id = lender_list[j]['lender_id']
                    every_id += id +','
        every_id = every_id[:-1] #remove the final comma
        return every_id

    def handle_error(self, status):
        if status == 'org.kiva.RateLimitExceeded':
            print('Status: ', response.status_code, 'You are blocked due to overuse. Retry in a few minutes. Exiting.')
        elif status == 400:
            print('Your url was wrong:', status, '. Exiting.')
        elif status == 403:
            print('Status: ', status, 'You are forbidden from requesting this resource at this moment. Retry in a few minutes. Exiting. ')
        else:
            print('Status: ', status, 'Problem with the request. Exiting')
        exit()

    def pad_loans(self, loans):

        try:
             # Make sure there is enough loans
            if len(loans) < 20:
                n_missing_loans = 20 - len(loans)
                more_loans = self.get_loans_sample()
                filler_loans = more_loans[0 : n_missing_loans]

                #TODO: make sure we aren't showing the same loans twice
                loans = loans + filler_loans
        except:
            self.logger.error(str(datetime.now()) + ":" + "pad_loans failure.")
            raise

        return loans

    def get_loans(self, facebook_access_token, type = "expiring"):

        loans = []

        if type == "geography":

            try:
                fi = FacebookIngest(facebook_access_token)
                countries = fi.get_tagged_places()

                # Get country and country code
                countries = list(countries) # should be from facebook_ingest.py
                country = random.choice(countries)

                #print("The current country is {0}.".format(country))
                country_code = self.find_country_code(country)

                # Get list of loan IDs for country
                loans = self.get_loans_by_country(country_code)

            except Exception, e:
                self.logger.error(str(datetime.now()) + ":" + "FacebookIngest failure - falling back.")
                self.logger.error(str(datetime.now()) + ":" + str(e))

            loans = self.pad_loans(loans)
            loan_ids = self.get_ids_for_loans(loans)
            random.shuffle(loan_ids)

            #print("The current loan ids are {0}.".format(loan_ids))

        elif type == "expiring":
            loans = self.get_loans_expiring_soon()
            loans = self.pad_loans(loans)
            loan_ids = self.get_ids_for_loans(loans)
            random.shuffle(loan_ids)

        elif type == "fathers_day":
            loans = self.get_loans_fathers_day()
            loans = self.pad_loans(loans)
            loan_ids = self.get_ids_for_loans(loans)
            random.shuffle(loan_ids)
        else:
            loans = self.pad_loans(loans)
            loan_ids = self.get_ids_for_loans(loans)
            random.shuffle(loan_ids)

        return loan_ids

def main():

    kapi = KivaAPI()
    loan_ids = kapi.get_loans("CAACEdEose0cBAHPbzgjLduEmnOiEXwdvDesCHfb7GTHv5hQtLY9CKHiIqIzhvjdEZCXQ4i2qhdZAEemIJVmH3VUZAajOYnylBGcSQAyxPUmTZAS8L3eNRsSZCLwLBKlHU7N1Il96c4lcZBMaIVZAssIrRb21vd28kqoaSZAitG91N0JHdMtAH1llxvXLZCgyGXJN4pXGpDZCtgBAZDZD",
                              type = "geography")

    for loan_id in loan_ids:
        print kapi.get_loan_by_id(loan_id)

if __name__ == '__main__':
    main()
