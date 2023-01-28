from django.shortcuts import render
from rest_framework import authentication, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from structlog import get_logger
from django.utils.decorators import method_decorator

from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_200_OK

from app_dir.api.utils import IsPermittedCreateView, IsAdminOrPermitted, generate_token, IsFinancesMember, IsDoctor
from app_dir.api.models import Payment
from app_dir.api.serializers import PaymentSerializer

logger = get_logger(__name__)


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
	username = request.data.get("username")
	password = request.data.get("password")
	if username is None or password is None:
		return Response(
			{"error": "Please provide both username and password"},
			status=HTTP_400_BAD_REQUEST,
		)
	user = authenticate(username=username, password=password)
	if not user:
		return Response({"error": "Invalid Credentials"}, status=HTTP_404_NOT_FOUND)
	token, _ = Token.objects.get_or_create(user=user)
	return Response({"token": token.key}, status=HTTP_200_OK)


@csrf_exempt
@api_view(["GET"])
def sample_api(request):
	data = {"sample_data": 123}
	logger.info("sample_api", data=data)
	return Response(data, status=HTTP_200_OK)


# @method_decorator(csrf_exempt, name='dispatch')
class TestToken(APIView):
	"""docstring for ClassName"""
	csrf_exempt = True

	authentication_classes = (
		authentication.TokenAuthentication,
	)
	# permission_classes = (IsPermittedCreateView,)
	permission_classes = (IsDoctor,)

	def get(self, request):
		data = {"sample_data": 123}
		logger.info("sample_api", data=data)
		return Response(data, status=HTTP_200_OK)

	def post(self, request):
		data = request.data
		logger.info("Testing data", data=data)
		return Response(data, status=HTTP_200_OK)


class MessageAPI(APIView):
	authentication_classes = (
		authentication.TokenAuthentication,
	)
	# permission_classes = [~IsFinancesMember] # using not operator
	permission_classes = (IsFinancesMember,)  # who are members of finace group

	def post(self, request):
		data = request.data
		logger.info("Testing data", data=data)
		return Response(data, status=HTTP_200_OK)


class PaymentFlow(APIView):
	"""docstring for ClassName"""
	authentication_classes = (
		authentication.TokenAuthentication,
		authentication.SessionAuthentication,
	)
	permission_classes = (IsPermittedCreateView,)

	def post(self, request):
		data = request.data
		logger.info("PaymentFlow", data=data)
		return Response(data, status=HTTP_200_OK)


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def register_payments(request):
	access_token = generate_token()

	headers = {"Authorization": "Bearer %s" % access_token}

	request_to_send = {
		"ShortCode": "600520",
		"ResponseType": "Completed",
		"ConfirmationURL": "http://example.com/confirmation/",
		"ValidationURL": "http://example.com/validation/"
	}

	response = requests.post(api_register_url, json=request_to_send, headers=headers)

	return {"status": "registerd successfully"}


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def validate_payment(request):
	# auth_header = request.headers.get('Authorization')

	# if auth_header:
	#     auth_token = auth_header.split(" ")[1]
	# else:
	#     auth_token = ''

	# generated_token = generate_token()

	""" check if the token exists """
	# if not generated_token:
	#     return {"status": "Technical Error"}

	""" check if the token matches what you had generated """
	# if auth_token != generated_token:
	#     return {"status": "Invalid authorization"}

	""" check if posted data is valid """
	# if request.data.get_json():
	#     return {"status": "Invalid input"}

	data = {}
	data["business_short_code"] = request.data.get("BusinessShortCode")
	data["bill_ref_number"] = request.data.get("BillRefNumber")
	data["trans_id"] = request.data.get("TransID")
	data["org_account_balance"] = request.data.get("OrgAccountBalance")
	data["first_name"] = request.data.get("FirstName")
	data["middle_name"] = request.data.get("MiddleName")
	data["last_name"] = request.data.get("LastName")
	data["trans_time"] = request.data.get("TransTime")
	data["trans_amount"] = request.data.get("TransAmount")
	data["invoice_number"] = request.data.get("InvoiceNumber")
	data["msisdn"] = request.data.get("MSISDN")
	data["transaction_type"] = request.data.get("TransactionType")
	data["third_party_transid"] = request.data.get("ThirdPartyTransID")
	data["status"] = 0

	"""
	Reject an Mpesa transaction
	by replying with the below code
	"""
	# response_data = {"ResultCode":1, "ResultDesc":"Failed", "ThirdPartyTransID": 0}

	"""
	Accept an Mpesa transaction
	by replying with the below code
	"""
	response_data = {"ResultCode": 0, "ResultDesc": "Success", "ThirdPartyTransID": 0}

	return Response(response_data, status=HTTP_201_CREATED)


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def confirm_payment(request):
	""" Function to receive payments from the mpesa api after validation """
	data = {}
	data["business_short_code"] = request.data.get("BusinessShortCode")
	data["bill_ref_number"] = request.data.get("BillRefNumber")
	data["trans_id"] = request.data.get("TransID")
	data["org_account_balance"] = request.data.get("OrgAccountBalance")
	data["first_name"] = request.data.get("FirstName")
	data["middle_name"] = request.data.get("MiddleName")
	data["last_name"] = request.data.get("LastName")
	data["trans_time"] = request.data.get("TransTime")
	data["trans_amount"] = request.data.get("TransAmount")
	data["invoice_number"] = request.data.get("InvoiceNumber")
	data["msisdn"] = request.data.get("MSISDN")
	data["transaction_type"] = request.data.get("TransactionType")
	data["third_party_transid"] = request.data.get("ThirdPartyTransID")
	data["status"] = 0

	if data["trans_id"] and data["trans_amount"]:
		Payment.objects.create(**data)

	"""
	Reject an Mpesa transaction
	by replying with the below code
	"""
	# return {"ResultCode":1, "ResultDesc":"Failed", "ThirdPartyTransID": 0}

	"""
	Accept an Mpesa transaction
	by replying with the below code
	"""
	# return {"ResultCode":0, "ResultDesc":"Success", "ThirdPartyTransID": 0}
	response_data = {"ResultCode": 0, "ResultDesc": "Success", "ThirdPartyTransID": 0}

	return Response(response_data, status=HTTP_200_OK)


class PaymentView(APIView):
	"""
	View to list all payments in the system and to post their status.

	* Only authenticated users are able to access this view.
	"""
	authentication_classes = (
		authentication.TokenAuthentication,
		authentication.SessionAuthentication,
	)
	permission_classes = (IsPermittedCreateView,)

	def get(self, request):
		"""
		Return a list of all payments.
		"""
		payments = Payment.objects.all()

		payment_status = request.query_params.get('status')

		if payment_status:
			try:
				picked_status = int(payment_status)
			except (ValueError, Exception) as e:
				picked_status = 0
			payments = payments.filter(status=picked_status)

		serializer = PaymentSerializer(payments, many=True)
		logger.info("PaymentView | get()", data=serializer.data)
		return Response(serializer.data)

	def post(self, request):
		try:
			transaction_ids = request.data.get("transaction_ids")
			transaction_status = request.data.get("status")

			ids = [int(i) for i in list(transaction_ids)]
			payments = Payment.objects.filter(pk__in=[i for i in ids])

			response = {'message': 'cannot change status of non-existent payments'}

			if payments.exists():
				if transaction_status.lower() == "success":
					"""
					update all queried payments status to inserted
					"""
					payments.update(status=2)
					response['message'] = 'db insertion status updated'
					logger.info("PaymentView | post()", status="db insertion status updated")
				else:
					"""
					update all queried payments status to initial (not picked)
					to be picked again
					"""
					payments.update(status=0)
					response['message'] = 'reverted to initial state'
					logger.info("PaymentView | post()", status="reverted to initial state")

			return Response(response, status=status.HTTP_200_OK)
		except Exception as exception:
			logger.error("PaymentView | post()", exception=exception)
			return Response({'message': 'error'}, status=status.HTTP_400_BAD_REQUEST)
