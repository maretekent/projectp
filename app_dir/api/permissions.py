from rest_framework import permissions


class MyModelViewPermission(permissions.BasePermission):
	def has_object_permission(self, request, view, obj):
		if request.method in permissions.SAFE_METHODS:
			return True
		return request.user.has_perm('myapp.can_view_mymodel', obj)


from rest_framework import generics


class MyModelView(generics.RetrieveAPIView):
	queryset = MyModel.objects.all()
	serializer_class = MyModelSerializer
	permission_classes = [MyModelViewPermission]


#############################################################################

from django.contrib.auth.models import Permission, User
from django.db import models


class MyModel(models.Model):
	name = models.CharField(max_length=100)

	class Meta:
		permissions = [
			("can_view_mymodel", "Can view mymodel"),
			("can_edit_mymodel", "Can edit mymodel"),
		]


user = User.objects.get(username='johndoe')
if user.has_perm('myapp.can_view_mymodel'):
    # user has the permission
else:
    # user doesn't have the permission

#####################################################################################
class MultipleFieldLookupMixin:
	"""
	Apply this mixin to any view or viewset to get multiple field filtering
	based on a `lookup_fields` attribute, instead of the default single field filtering.
	"""

	def get_object(self):
		queryset = self.get_queryset()  # Get the base queryset
		queryset = self.filter_queryset(queryset)  # Apply any filter backends
		filter = {}
		for field in self.lookup_fields:
			if self.kwargs.get(field):  # Ignore empty fields.
				filter[field] = self.kwargs[field]
		obj = get_object_or_404(queryset, **filter)  # Lookup the object
		self.check_object_permissions(self.request, obj)
		return obj


class RetrieveUserView(MultipleFieldLookupMixin, generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_fields = ['account', 'username']


