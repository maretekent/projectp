# When the DEBUG setting in Django is set to False, the framework will no longer allow cross-site
# request forgery (CSRF) tokens to be passed in via GET requests. This is because GET requests are
# typically used for retrieving data, and allowing CSRF tokens to be passed in via GET requests could
# potentially allow an attacker to perform actions on behalf of a user without their knowledge.
#
# To fix this issue, you will need to ensure that CSRF tokens are only passed in via POST, PUT, or DELETE
# requests. This can be done by adding the csrf_exempt decorator to any views that should be allowed to receive
# CSRF tokens via GET requests. Here's an example of how to use the csrf_exempt decorator:
from django.views import View
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def my_view(request):
	# Your view logic here
	pass


class MyView(View):
	csrf_exempt = True

	def nothing(self):
		pass


# However, be aware that disabling CSRF protection globally is not recommended and can leave your application
# vulnerable to CSRF attacks. The best practice is to apply the csrf_exempt decorator only to views
# that don't require CSRF protection.
#
# Another option is to use the CsrfViewMiddleware to check for the csrf token on the headers instead of the
# cookies, this way the token will be sent via GET requests as well

CSRF_USE_SESSIONS = False
CSRF_COOKIE_HTTPONLY = False
CSRF_HEADER_NAME = "X-CSRF-TOKEN"
