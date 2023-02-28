# pip install django-role-permissions

# settings.py
INSTALLED_APPS = [
	...
	'rolepermissions',
	...
]

# roles.py
from rolepermissions.roles import AbstractUserRole


class Employee(AbstractUserRole):
	available_permissions = {
		'view_dashboard': True,
		'view_employee_list': True,
	}


class Manager(AbstractUserRole):
	available_permissions = {
		'view_dashboard': True,
		'view_employee_list': True,
		'add_employee': True,
		'edit_employee': True,
		'delete_employee': True,
	}


# settings.py
ROLEPERMISSIONS_MODULE = 'your_project.roles'

# settings.py
MIDDLEWARE = [
	...
	'rolepermissions.middleware.RolePermissionMiddleware',
	...
]

# python manage.py makemigrations
# python manage.py migrate


from rolepermissions.checkers import has_permission
from rolepermissions.decorators import has_role_decorator


@has_role_decorator('manager')
def my_view(request):
	if has_permission(request.user, 'view_dashboard'):
	# Do something
	else:
# Do something else


from django.contrib.auth.mixins import LoginRequiredMixin
from rolepermissions.decorators import has_role_decorator


@has_role_decorator('manager')
class MyView(LoginRequiredMixin, TemplateView):
	template_name = 'my_template.html'

	def get(self, request, *args, **kwargs):
# Do something

'''
In this example, the MyView class is decorated with the has_role_decorator function, which checks if the user
accessing the view has the "manager" role. If the user does not have the "manager" role, they will be
redirected to the login page.
'''


from django.contrib.auth.mixins import LoginRequiredMixin
from rolepermissions.decorators import has_role_decorator


class MyView(LoginRequiredMixin, TemplateView):
	template_name = 'my_template.html'

	@has_role_decorator('manager')
	def dispatch(self, request, *args, **kwargs):
		return super().dispatch(request, *args, **kwargs)

	def get(self, request, *args, **kwargs):
# Do something


'''
In Django, the dispatch method is a function that is called when a request is made to a class-based view.
It is responsible for determining which method (such as get, post, put, etc.) should handle the request,
and then calling that method. The dispatch method is implemented in the View class, which is the base class
for all class-based views in Django.

When a request is made to a class-based view, the dispatch method is called first. It examines the request's
method (e.g. GET, POST, PUT, etc.) and calls the corresponding method on the view (e.g. get, post, put, etc.).
If the request method is not handled by the view, the dispatch method will raise a HttpResponseNotAllowed exception.

You can also customize the dispatch method to add additional functionality that should be executed before the
request method is called. For example, you can use the dispatch method to check if a user is authenticated or
has a specific role, or to add additional context data to the view.

Here's an example of how you can customize the dispatch method in a class-based view:

In this example, the dispatch method checks if the user is authenticated before the request method is called.
If the user is not authenticated, they will be redirected to the login page.
The super().dispatch(request, *args, **kwargs) call is used to call the parent class's dispatch method,
 which will determine which request method should be called and then call it.
'''

class MyView(View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        # Do something

'''In Django, the HttpResponseNotAllowed exception is raised by the dispatch method when a request is made to a
class-based view and the request method is not handled by the view. You can customize the behavior of this exception
 by overriding the handle_exception method in a middleware class.'''

from django.http import HttpResponseNotAllowed

class CustomExceptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        if isinstance(exception, HttpResponseNotAllowed):
            # Customize the response here
            return HttpResponse("Method not allowed", status=405)

'''In this example, the process_exception method is overridden to check if the exception raised is an instance of
HttpResponseNotAllowed, if so the response is customized to return a "Method not allowed" message with a status
code of 405.'''

MIDDLEWARE = [
    ...
    'path.to.CustomExceptionMiddleware',
    ...
]

##################################################################################
# Django's AbstractUser model is a base class that you can use to create your own custom user model. It provides a ' \
# 	  'lot of fields and methods out of the box, and you can also add your own.
#
# To use groups and permissions with your custom user model, you need to define the model and then configure the
# settings in your Django project. Here's an example:

from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class CustomUser(AbstractUser):
    # add any additional fields you need

    def has_perm(self, perm, obj=None):
        # check if user has permission
        return self.is_superuser or self.groups.filter(
            permissions__codename=perm).exists()

    def has_module_perms(self, app_label):
        # check if user has permission for app
        return self.is_superuser or self.groups.filter(
            permissions__content_type__app_label=app_label).exists()

    @property
    def get_groups(self):
        # get all groups for user
        return self.groups.all()

    @property
    def get_permissions(self):
        # get all permissions for user
        return Permission.objects.filter(
            Q(group__user=self) | Q(user=self)).distinct()

# In this example, we have defined a CustomUser model that extends the AbstractUser model. We have also defined
# two methods to check if the user has a specific permission or if they have permissions for a specific app.
#
# We have also defined two properties: get_groups and get_permissions. These properties allow us to get all of the
# groups and permissions for a user, respectively.
#
# To use groups and permissions with this custom user model, you need to configure the AUTH_USER_MODEL,
# AUTH_GROUP_MODEL, and AUTH_PERMISSION_MODEL settings in your Django project's settings:

AUTH_USER_MODEL = 'yourapp.CustomUser'
AUTH_GROUP_MODEL = 'auth.Group'
AUTH_PERMISSION_MODEL = 'auth.Permission'

# Once you have configured these settings, you can use groups and permissions with your custom user model just
# like you would with the default User model. For example, to add a user to a group:

user = CustomUser.objects.get(username='example')
group = Group.objects.get(name='example_group')
user.groups.add(group)


user = CustomUser.objects.get(username='example')
if user.has_perm('example_permission'):
    # do something


##############################################################################

	# How
	# to
	# add
	# Custom
	# Permissions
	# to
	# Views
	# Just
	# like
	# when
	# you
	# were
	# working
	# with the built- in Django permissions, you can also add custom permissions to views by using the
	# permission_required decorator or, in a class -based view, using the PermissionRequiredMixin.For function-
	# based views:

	from django.contrib.auth.decorators import permission_required


	@permission_required('app.change_name')
	def the_view(request):
		pass
		# ...


	# For

	# class -based views:


	from django.contrib.auth.mixins import PermissionRequiredMixin


	class MyView(PermissionRequiredMixin, View):
		permission_required = 'app.change_name'
		# Or multiple permissions
		permission_required = ('app.change_name', 'app.edit_name')
	# Note that 'catalog.can_edit' is just an example, you can replace it with
	# whatever permissions you have created


# https://testdriven.io/blog/django-permissions/#:~:text=With%20Django%2C%20you%20can%20create,auth.

# Create user groups
user_roles = ["Read only", "Maintainer"]
for name in user_roles:
	Group.objects.create(name=name)

# Permissions have to be created before applying them
for app_config in apps.get_app_configs():
	app_config.models_module = True
	create_permissions(app_config, verbosity=0)
	app_config.models_module = None

# Assign model-level permissions to maintainers
all_perms = Permission.objects.all()
maintainer_perms = [i for i in all_perms if i.content_type.app_label == "batteryDB"]
Group.objects.get(name="Maintainer").permissions.add(*maintainer_perms)


# because superusers always have permission to do anything, even if that permission doesn’t exist.
