from datetime import timedelta, datetime, timezone

from structlog import get_logger
from rest_framework import permissions
import requests

logger = get_logger(__name__)


class IsAdminOrPermitted(permissions.BasePermission):
	def has_permission(self, request, view):
		user = request.user
		return user.is_superuser or user.has_perm(
			"can_create_view_via_API"
		)


class IsPermittedCreateView(permissions.BasePermission):
	def has_permission(self, request, view):
		user = request.user
		return user.has_perm(
			"can_create_view_via_API",
		)


class IsFinancesMember(permissions.BasePermission):
	def has_permission(self, request, view):
		if request.user.groups.filter(name="Finances").exists():
			return True


class IsDoctor(permissions.BasePermission):
	def has_permission(self, request, view):
		user = request.user
		return user.has_perm("create_medical_record",)


class ExpiredObjectSuperuserOnly(permissions.BasePermission):
	message = "This object is expired."  # custom error message

	def object_expired(self, obj):
		expired_on = timezone.make_aware(datetime.now() - timedelta(minutes=10))
		return obj.created < expired_on

	def has_object_permission(self, request, view, obj):

		if self.object_expired(obj) and not request.user.is_superuser:
			return False
		else:
			return True


class AuthorOrReadOnly(permissions.BasePermission):

	def has_permission(self, request, view):
		if request.user.is_authenticated:
			return True
		return False

	def has_object_permission(self, request, view, obj):
		if obj.author == request.user:
			return True
		return False


def generate_token():
	# api urls
	# change this api_token_URL after getting the real token generating url
	api_token_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"

	# consumer details
	# change accordingly after going live
	consumer_key = "Q2k2z3SQVHMTmghG4utquiC7eDLqWAIv"
	consumer_secret = "9Sqre2c4ykkVYOym"

	response = requests.get(api_token_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))

	stripped_response = (response.text).strip()
	token = json.loads(stripped_response).get('access_token')

	return token
