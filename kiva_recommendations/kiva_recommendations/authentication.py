from django.http import HttpResponse
from django.conf import settings
import time
import urllib
import json
import oauth2 as oauth
import httplib

def kiva_request(request):
	consumer_key = settings.KIVA_CLIENT_ID
	consumer_secret = settings.KIVA_CLIENT_SECRET
	callback_url = 'oob'

	connection = httplib.HTTPConnection("localhost:3000")
	request_token_url = 'https://api.kivaws.org/oauth/request_token.json?oauth_callback='+urllib.quote_plus(callback_url)
	consumer = oauth.Consumer(consumer_key, consumer_secret)
	client = oauth.Client(consumer)

	resp, content = client.request(request_token_url, "POST")

	if resp['status'] != '200':
		raise Exception("Invalid response. Status: "+resp['status']+" Message: "+content)

	request_token = dict(json.loads(content))

	return HttpResponse(content)

def kiva_access(request):
	verifier = request.POST.get('verifier')
	oauth_token = request.POST.get('oauth_token')
	oauth_token_secret = request.POST.get('oauth_token_secret')

	consumer_key = settings.KIVA_CLIENT_ID
	cosumer_secret = settings.KIVA_CLIENT_SECRET

	consumer = oauth.Consumer(consumer_key, consumer_secret)

	access_token_url = 'https://api.kivaws.org/oauth/access_token.json'

	resp, content = client.request(access_token_url, "POST")

	if resp['status'] != '200':
		raise Exception("Invalid response. Status: "+resp['status']+" Message: "+content)

	access_token = dict(json.loads(content))

	#TODO: Pass to data

	return HttpResponse(content)
