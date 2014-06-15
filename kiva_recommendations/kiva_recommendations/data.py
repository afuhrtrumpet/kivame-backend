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
