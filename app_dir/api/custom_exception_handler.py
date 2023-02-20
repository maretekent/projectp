from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
	response = exception_handler(exc, context)

	if response is not None:
		response.data['message'] = response.data['detail']
		response.data['error'] = response.data['error']
		response.data['data_info'] = {}
		response.data['status'] = response.data['status_code']
		del response.data['detail']
	return response
