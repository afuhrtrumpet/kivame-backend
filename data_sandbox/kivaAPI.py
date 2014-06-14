import urllib.request
import json

#Kiva API wrapper created by Eivind


#
#Method to get hold of the latest action on kiva
#
def getRecentAction():
    url='http://api.kivaws.org/v1/lending_actions/recent.json'
    json_obj = jsonFromURL(url)
    return json_obj.get('lending_actions')

#
#Methods to get hold of the lender data
#
def getLendersByID(uids):
    url='http://api.kivaws.org/v1/lenders/'+uids+'.json'
    json_obj = jsonFromURL(url)
    return json_obj.get('lenders')

def getLenderLoans(uid, sort_by=None):
    url='http://api.kivaws.org/v1/lenders/'+uid+'/loans.json?'
    #Parameters
    if sort_by is not None:
        url=url+'sort_by='+sort_by
    json_obj = jsonFromURL(url)
    loans = json_obj.get('loans')

    paging = json_obj.get('paging')
    page = 1
    pages = int(paging.get('pages'))
    while page <= pages:
        page=page+1
        url=url+'&page='+str(page)
        json_obj = jsonFromURL(url)
        loans=loans+json_obj.get('loans')

    return loans

#
#Methods to get hold of the loan data
#
def getLatestLoans():
    url='http://api.kivaws.org/v1/loans/newest.json'
    json_obj = jsonFromURL(url)
    loans = json_obj.get('loans')

    paging = json_obj.get('paging')
    page = 1
    pages = int(paging.get('pages'))
    while page <= pages:
        page=page+1
        url=url+'&page='+str(page)
        json_obj = jsonFromURL(url)
        loans=loans+json_obj.get('loans')

    return loans    

def getLoansByID(ids):
    url='http://api.kivaws.org/v1/loans/'+ids+'.json'
    json_obj = jsonFromURL(url)
    return json_obj.get('loans')

def getLoanLenders(lid):
    url='http://api.kivaws.org/v1/loans/'+lid+'/lenders.json?'
    json_obj = jsonFromURL(url)
    lenders = json_obj.get('lenders')

    paging = json_obj.get('paging')
    page = 1
    pages = int(paging.get('pages'))
    while page <= pages:
        page=page+1
        url=url+'&page='+str(page)
        json_obj = jsonFromURL(url)
        lenders=lenders+json_obj.get('lenders')

    return lenders

def getLoans(sort_by=None, status=None, gender=None,
             sector=None, region=None, country_code=None, partner=None, q=None):

    URL_BASE = 'http://api.kivaws.org/v1/loans/search.json?'
    url = URL_BASE

    #Parameters
    if sort_by is not None:
        url=url+'&sort_by='+sort_by
    
    #Filtering    
    if status is not None:
        url=url+'&status='+status
    if gender is not None:
        url=url+'&gender='+gender
    if sector is not None:
        url=url+'&sector='+sector
    if region is not None:
        url=url+'&region='+region
    if country_code is not None:
        url=url+'&country_code='+country_code
    if partner is not None:
        url=url+'&partner='+partner
    if q is not None:
        url=url+'&q='+q
    
    json_obj = jsonFromURL(url)
    loans = json_obj.get('loans')

    paging = json_obj.get('paging')
    page = 1
    pages = int(paging.get('pages'))
    while page <= pages:
        page=page+1
        url=url+'&page='+str(page)
        json_obj = jsonFromURL(url)
        loans=loans+json_obj.get('loans')

    return loans    

#
#Method to get hold of the partner data
#                                
def getPartners():
    url='http://api.kivaws.org/v1/partners.json?'
    json_obj = jsonFromURL(url)
    partners = json_obj.get('partners')

    paging = json_obj.get('paging')
    page = 1
    pages = int(paging.get('pages'))
    while page <= pages:
        page=page+1
        url=url+'page='+str(page)
        json_obj = jsonFromURL(url)
        partners=partners+json_obj.get('partners')

    return partners


#
#Some methods for extracting the .json
#
def jsonFromURL(my_url):
    byte_obj = urllib.request.urlopen(my_url).read()
    dec_obj = bytes.decode(byte_obj)
    kiva_string = trimJSON(dec_obj)
    return json.loads(kiva_string)

    
def trimJSON(kiva_response):
    found_start = 0
    found_end = 0
    i=-1
    j=len(kiva_response)
    while found_start==0:
        i=i+1
        if kiva_response[i] == '{':
            found_start = 1
    while found_end==0:
        j=j-1
        if kiva_response[j] =='}':
            found_end = 1
    return kiva_response[i:j+1]
