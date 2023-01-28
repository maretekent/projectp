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

