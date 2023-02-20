from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import pgettext_lazy
from django.utils.timezone import now


class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	bio = models.TextField(max_length=500, blank=True)

	class Meta:
		permissions = (
			('can_create_view_via_API', 'Create or View via API'),
			('can_view_via_API', 'Create View only via API'),
			('create_medical_record', 'create medical records'),
		)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
	instance.profile.save()


class Payment(models.Model):
	msisdn = models.CharField(
		pgettext_lazy('Payment field', 'MSISDN (e.g 254708374149)'),
		blank=True, null=True, max_length=255)
	first_name = models.CharField(
		pgettext_lazy('Payment field', 'FirstName'),
		blank=True, null=True, max_length=255)
	middle_name = models.CharField(
		pgettext_lazy('Payment field', 'MiddleName'),
		blank=True, null=True, max_length=255)
	last_name = models.CharField(
		pgettext_lazy('Payment field', 'LastName'),
		blank=True, null=True, max_length=255)
	trans_time = models.CharField(
		pgettext_lazy('Payment field', 'TransTime (e.g 20181009075311)'),
		blank=True, null=True, max_length=255)
	trans_id = models.CharField(
		pgettext_lazy('Payment field', 'TransID (e.g MJ951H6YF7)'),
		blank=True, null=True, max_length=255, unique=True)
	trans_amount = models.CharField(
		pgettext_lazy('Payment field', 'TransAmount (e.g 100.00)'),
		blank=True, null=True, max_length=255)
	org_account_balance = models.CharField(
		pgettext_lazy('Payment field', 'OrgAccountBalance (e.g 518663.00)'),
		blank=True, null=True, max_length=255)
	invoice_number = models.CharField(
		pgettext_lazy('Payment field', 'InvoiceNumber'),
		blank=True, null=True, max_length=255)
	bill_ref_number = models.CharField(
		pgettext_lazy('Payment field', 'BillRefNumber e.g(account name - testapi)'),
		blank=True, null=True, max_length=255)
	third_party_transid = models.CharField(
		pgettext_lazy('Payment field', 'ThirdPartyTransID'),
		blank=True, null=True, max_length=255)
	business_short_code = models.CharField(
		pgettext_lazy('Payment field', 'BusinessShortCode (e.g 600520)'),
		blank=True, null=True, max_length=255)
	transaction_type = models.CharField(
		pgettext_lazy('Payment field', 'TransactionType (e.g Pay Bill)'),
		blank=True, null=True, max_length=255)
	status = models.IntegerField(
		pgettext_lazy('Payment field',
					  'status( [0 - not picked], [1 - picked], [2 -inserted to db] )'),
		default=0)

	updated_at = models.DateTimeField(
		pgettext_lazy('Payment field', 'date of update'),
		auto_now=True, null=True)

	created_at = models.DateTimeField(pgettext_lazy('Payment field', 'date of create'),
									  default=now, editable=False)

	class Meta:
		verbose_name = pgettext_lazy('Payment model', 'Mpesa Payment')
		verbose_name_plural = pgettext_lazy('Payment model', 'Mpesa Payment')

	def __str__(self):
		return self.trans_id


class Reporter(models.Model):
	first_name = models.CharField(max_length=30)
	last_name = models.CharField(max_length=30)
	email = models.EmailField()

	def __str__(self):
		return "%s %s" % (self.first_name, self.last_name)


class Article(models.Model):
	headline = models.CharField(max_length=100)
	pub_date = models.DateField()
	reporter = models.ForeignKey(Reporter, on_delete=models.CASCADE)

	def __str__(self):
		return self.headline

	class Meta:
		ordering = ['headline']


# >>> r = Reporter(first_name='John', last_name='Smith', email='john@example.com')
# >>> r.save()
#
# >>> r2 = Reporter(first_name='Paul', last_name='Jones', email='paul@example.com')
# >>> r2.save()


# >>> from datetime import date
# >>> a = Article(id=None, headline="This is a test", pub_date=date(2005, 7, 27), reporter=r)
# >>> a.save()
#
# >>> a.reporter.id
# 1
#
# >>> a.reporter
# <Reporter: John Smith>

# >>> r.article_set.filter(headline__startswith='This')
# <QuerySet [<Article: This is a test>]>
#
# # Find all Articles for any Reporter whose first name is "John".
# >>> Article.objects.filter(reporter__first_name='John')
# <QuerySet [<Article: John's second story>, <Article: This is a test>]>
#
# >>> Article.objects.filter(reporter__first_name='John')
# <QuerySet [<Article: John's second story>, <Article: This is a test>]>
#
# >>> Article.objects.filter(reporter__first_name='John', reporter__last_name='Smith')
# <QuerySet [<Article: John's second story>, <Article: This is a test>]>
#
# >>> Article.objects.filter(reporter__pk=1)
# <QuerySet [<Article: John's second story>, <Article: This is a test>]>
# >>> Article.objects.filter(reporter=1)
# <QuerySet [<Article: John's second story>, <Article: This is a test>]>
# >>> Article.objects.filter(reporter=r)
# <QuerySet [<Article: John's second story>, <Article: This is a test>]>
#
# >>> Article.objects.filter(reporter__in=[1,2]).distinct()
# <QuerySet [<Article: John's second story>, <Article: Paul's story>, <Article: This is a test>]>
# >>> Article.objects.filter(reporter__in=[r,r2]).distinct()
# <QuerySet [<Article: John's second story>, <Article: Paul's story>, <Article: This is a test>]>
#
# >>> Article.objects.filter(reporter__in=Reporter.objects.filter(first_name='John')).distinct()
# <QuerySet [<Article: John's second story>, <Article: This is a test>]>
#
#
# >>> Reporter.objects.filter(article__pk=1)
# <QuerySet [<Reporter: John Smith>]>
# >>> Reporter.objects.filter(article=1)
# <QuerySet [<Reporter: John Smith>]>
# >>> Reporter.objects.filter(article=a)
# <QuerySet [<Reporter: John Smith>]>
#
# >>> Reporter.objects.filter(article__headline__startswith='This')
# <QuerySet [<Reporter: John Smith>, <Reporter: John Smith>, <Reporter: John Smith>]>
# >>> Reporter.objects.filter(article__headline__startswith='This').distinct()
# <QuerySet [<Reporter: John Smith>]>
#
# >>> Reporter.objects.filter(article__headline__startswith='This').count()
# 3
# >>> Reporter.objects.filter(article__headline__startswith='This').distinct().count()
# 1

# >>> Reporter.objects.filter(article__reporter__first_name__startswith='John')
# <QuerySet [<Reporter: John Smith>, <Reporter: John Smith>, <Reporter: John Smith>, <Reporter: John Smith>]>
# >>> Reporter.objects.filter(article__reporter__first_name__startswith='John').distinct()
# <QuerySet [<Reporter: John Smith>]>
# >>> Reporter.objects.filter(article__reporter=r).distinct()
# <QuerySet [<Reporter: John Smith>]>

class Place(models.Model):
	name = models.CharField(max_length=50)
	address = models.CharField(max_length=80)

	def __str__(self):
		return "%s the place" % self.name


class Restaurant(models.Model):
	place = models.OneToOneField(
		Place,
		on_delete=models.CASCADE,
		primary_key=True,
	)
	serves_hot_dogs = models.BooleanField(default=False)
	serves_pizza = models.BooleanField(default=False)

	def __str__(self):
		return "%s the restaurant" % self.place.name


class Waiter(models.Model):
	restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
	name = models.CharField(max_length=50)

	def __str__(self):
		return "%s the waiter at %s" % (self.name, self.restaurant)

# >>> p1 = Place(name='Demon Dogs', address='944 W. Fullerton')
# >>> p1.save()
# >>> p2 = Place(name='Ace Hardware', address='1013 N. Ashland')
# >>> p2.save()
#
# >>> r = Restaurant(place=p1, serves_hot_dogs=True, serves_pizza=False)
# >>> r.save()

# >>> from django.utils import timezone
# >>> Post.objects.filter(published_date__lte=timezone.now())

# >>> Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
# <QuerySet [<Post: Post number 2>, <Post: My 3rd post!>, <Post: 4th title of post>, <Post: Sample title>]>

# >>> Post.objects.order_by('-created_date')
# <QuerySet [<Post: 4th title of post>,  <Post: My 3rd post!>, <Post: Post number 2>, <Post: Sample title>]>

# prefetch_related  vs select_relateds


# The select_related method is used to fetch related objects with a single database query.
# It is useful when you want to fetch data from multiple tables in a single query, as it reduces the number of
# database queries. For example:

posts = Post.objects.select_related('author').all()
for post in posts:
    print(post.title)
    print(post.author.name)

# In this example, the Post model has a foreign key to the Author model, and the select_related method is used to
#
# fetch data from both tables in a single query. The result is a queryset of Post objects with the related Author
# objects loaded.
#
# The prefetch_related method is used to fetch related objects with multiple database queries. It is useful when you
# want to fetch data from multiple related tables, as it reduces the number of database queries compared to fetching
# each related table separately. For example:

posts = Post.objects.prefetch_related('comments').all()
for post in posts:
    print(post.title)
    for comment in post.comments.all():
        print(comment.text)

# In this example, the Post model has a many-to-many relationship with the Comment model,
# and the prefetch_related method is used to fetch data from both tables in multiple queries.
# The result is a queryset of Post objects with the related Comment objects loaded.




Kenneth Marete
django roles permission library usage
There are several libraries available in Django to handle role-based permissions, some popular ones include:

django-guardian: This library provides a simple way to manage object-level permissions in Django. It integrates with the Django authentication system and allows you to define custom permissions for your models.

django-role-permissions: This library provides an easy way to define role-based permissions in Django. It uses the Django authentication system and allows you to assign roles to users and define custom permissions for each role.

django-rules: This library provides a simple way to define rule-based permissions in Django. It allows you to define permissions based on conditions, such as a user's group membership or the object being accessed.

Here's an example of how to use django-guardian:

python
Copy code
# models.py
from django.contrib.auth.models import User
from guardian.shortcuts import assign_perm

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

# views.py
from guardian.mixins import PermissionRequiredMixin

class BookDetailView(PermissionRequiredMixin, DetailView):
    model = Book
    permission_required = 'books.view_book'

# assign permission to user
book = Book.objects.first()
user = User.objects.first()
assign_perm('books.view_book', user, book)
In this example, django-guardian is used to define a custom permission for viewing a book (books.view_book). The BookDetailView is a class-based view that requires the user to have the books.view_book permission in order to access the book detail page. The permission is assigned to a user for a specific book using the assign_perm function.




Kenneth Marete
django-role-permissions usage
Here's an example of how to use django-role-permissions:

python
Copy code
# models.py
from django.contrib.auth.models import User
from rolepermissions.roles import assign_role

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

# roles.py
from rolepermissions.roles import AbstractUserRole

class Author(AbstractUserRole):
    available_permissions = {
        'view_book': True,
        'add_book': True,
    }

# views.py
from rolepermissions.decorators import has_role_decorator

@has_role_decorator('author')
def add_book(request):
    # code to add a book
    pass

# assign role to user
user = User.objects.first()
assign_role(user, 'author')
In this example, django-role-permissions is used to define a role Author with two permissions (view_book and add_book). The add_book view is decorated with the has_role_decorator to check if the user has the author role before allowing them to add a book. The role is assigned to a user using the assign_role function.




Kenneth Marete
django classview based put method to update many to one field
Here's an example of a Django class-based view using the PUT method to update a foreign key relationship:

kotlin
Copy code
# models.py
class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

class User(models.Model):
    username = models.CharField(max_length=100)

# serializers.py
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

# views.py
class BookUpdateView(APIView):
    def put(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        serializer = BookSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
In this example, a BookUpdateView class is defined to handle PUT requests for updating a book. The view uses the get_object_or_404 function to retrieve the book based on the primary key (pk) provided in the URL. The BookSerializer is then used to validate the data in the PUT request and to update the book. If the serializer is valid, the updated book data is returned in the response. If the serializer is not valid, an error response is returned with a status code of 400 Bad Request.



Here's an example of how to loop through a list of objects in a Django request:

ruby
Copy code
# views.py
class BookCreateView(APIView):
    def post(self, request):
        books = request.data.get('books')
        for book in books:
            # access each book object
            title = book.get('title')
            author = book.get('author')
            # ... process each book object
        # ... process the entire list of books
        return Response({'message': 'Books processed'})
In this example, a BookCreateView class is defined to handle POST requests for creating books. The view uses the request.data property to access the data in the request. The request.data.get('books') method is used to retrieve the list of books from the request data. The view then uses a for loop to iterate over each book in the list and access its properties. The code inside the for loop can be used to process each book as needed. Finally, the view returns a response indicating that the books have been processed.



