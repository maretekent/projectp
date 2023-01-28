from django.contrib.auth.models import Permission, User
from django.db import models

class MyModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        permissions = (
            ("view_mymodel", "Can view my model"),
            ("change_mymodel", "Can change my model"),
        )

user = User.objects.get(username='john')
view_permission = Permission.objects.get(codename='view_mymodel')
change_permission = Permission.objects.get(codename='change_mymodel')

user.user_permissions.add(view_permission)
user.user_permissions.add(change_permission)


# usage

from django.contrib.auth.decorators import permission_required

@permission_required('myapp.view_mymodel')
def view_mymodel(request):
    # view code

@permission_required('myapp.change_mymodel', raise_exception=True)
def change_mymodel(request):
    # change code

	# custom exception handler in django rest framework

	from rest_framework.views import exception_handler
	from rest_framework.response import Response

	def custom_exception_handler(exc, context):
		# Call REST framework's default exception handler first,
		# to get the standard error response.
		response = exception_handler(exc, context)

		# Now add the HTTP status code to the response.
		if response is not None:
			response.data['status_code'] = response.status_code

		if isinstance(exc, MyCustomException):
			response = Response({'message': 'There was a problem with your request'},
								status=status.HTTP_400_BAD_REQUEST)

		return response


REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'path.to.custom_exception_handler',
}

# Django many to many relationship query

from myapp.models import Book, Author

# Get all books written by a specific author
author = Author.objects.get(name='John Smith')
books = Book.objects.filter(authors__name='John Smith')

# Get all authors that have written a specific book
book = Book.objects.get(title='The Great Gatsby')
authors = Author.objects.filter(book__title='The Great Gatsby')


# Get all books that have multiple authors
authors = Author.objects.filter(name__in=['John Smith', 'Jane Doe'])
books = Book.objects.filter(authors__in=authors)

# Add an author to a book
book = Book.objects.get(title='The Great Gatsby')
author = Author.objects.get(name='F. Scott Fitzgerald')
book.authors.add(author)

# Remove an author from a book
book.authors.remove(author)

