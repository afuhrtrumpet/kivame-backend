from django.http import HttpResponse
import data_api.kiva_api_requests as api
import json

def loan_list(request):
	#facebook_token = request.POST.get('token')
	kapi = api.KivaAPI()
	loan_ids = kapi.get_loans("CAACEdEose0cBAB4cPZC8UFYxWkfFs9ODZCPbPoVfEcXfuVrbSJ1NL3gW9yHxL2lf7Mbb6xPrGB9XJgVdZAi1Tgn86gDeRb81rFesPmWFDQxWT6VqyrCBju8sI4i0mU5a3NZBJwBzWskePuuAeKwrWapBCV7MLIz7HFtUSDZCDQeArOZCZA1zvCmtauY4kdOdMyT4hWWhaZBU8gZDZD")

	result = []
	for loan_id in loan_ids:
		result.append(kapi.get_loan_by_id(loan_id))
	return HttpResponse(json.dumps(result))
