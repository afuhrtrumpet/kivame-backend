from django.http import HttpResponse
import data_api.kiva_api_requests as api
import json
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def loan_list(request):
	facebook_token = request.POST.get('token')
	result_type = request.POST.get('type')

	kapi = api.KivaAPI()
	loan_ids = kapi.get_loans(facebook_token, result_type)

	result = []
	for loan_id in loan_ids:
		result.append(kapi.get_loan_by_id(loan_id))
	return HttpResponse(json.dumps(result))

@csrf_exempt
def all_loans(request):
	facebook_token = request.POST.get('token')
	types = ['geography', 'expiring']
	result = {}
	kapi = api.KivaAPI()
	for result_type in types:
		result[result_type] = []
		loan_ids = kapi.get_loans(facebook_token, result_type)
		
		for loan_id in loan_ids:
			result[result_type].append(kapi.get_loan_by_id(loan_id))
	return HttpResponse(json.dumps(result))
