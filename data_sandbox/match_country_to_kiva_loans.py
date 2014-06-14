""" Given a country find recent loans 
"""

import requests

class KivaAPI():
    """ Methods to parse Kiva API 
    """

    def get_loans_sample(self):
        """  Get 1st page of loans
        """
        url = 'http://api.kivaws.org/v1/loans/newest.json'
        response = requests.get(url)
        if response.status_code != requests.codes.ok:  self.handle_error(response.status_code)
        response_dict = response.json()
        
        return response_dict['loans']

    def get_loans_all(self):
        """  Get all loans
        """

        url = 'http://api.kivaws.org/v1/loans/newest.json'
        response = requests.get(url)
        if response.status_code != requests.codes.ok:  self.handle_error(response.status_code)
        response_dict = response.json()
        total_loans = response_dict['loans']

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

def main():
    
    current_country = 'foo'
    n_loans = 10

    test = KivaAPI()
    current_loans = test.get_loans_sample()
    print("The lastest loan is from {0}.".format(current_loans[0]['location']['country']))

    # lender_id = 'premal'
    # # Change 'premal' to your own lender id to see the impact of the teams you belong to
    # team_list = test.get_team_list(lender_id)
    # for i in range(len(team_list)):
    #     print 'Team id is %d' % team_list[i]['id']
    #     lender_list = test.get_lender_in_team_list(team_list, i)
    #     id_list = test.build_lender_id_list(lender_list)
    #     team_impact = test.get_lender_invitee_sum(id_list)
    #     print "Team %10s invited %d others" % (team_list[i]['name'], team_impact )

if __name__ == '__main__':
    main()
