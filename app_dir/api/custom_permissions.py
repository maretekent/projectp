from rest_framework.permissions import BasePermission


class CustomPermissions(BasePermission):
	edit_methods = ("PUT", "PATCH")

	def has_permission(self, request, view):
		return bool(request.user and request.user.is_authenticated)

	def has_object_permission(self, request, view, obj):
		if obj.author == request.user:
			return True

		if request.user.is_authenticated and request.method not in self.edit_methods:
			return True
		return False
