from django.http import HttpResponse
import data_api.kiva_api_requests as api
import json
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def loan_list(request):
	facebook_token = request.POST.get('token')
	#if (!facebook_token):
		#facebook_token = "CAACEdEose0cBAB4cPZC8UFYxWkfFs9ODZCPbPoVfEcXfuVrbSJ1NL3gW9yHxL2lf7Mbb6xPrGB9XJgVdZAi1Tgn86gDeRb81rFesPmWFDQxWT6VqyrCBju8sI4i0mU5a3NZBJwBzWskePuuAeKwrWapBCV7MLIz7HFtUSDZCDQeArOZCZA1zvCmtauY4kdOdMyT4hWWhaZBU8gZDZD"
	kapi = api.KivaAPI()
	loan_ids = kapi.get_loans(facebook_token)

	result = []
	for loan_id in loan_ids:
		result.append(kapi.get_loan_by_id(loan_id))
	return HttpResponse(json.dumps(result))
