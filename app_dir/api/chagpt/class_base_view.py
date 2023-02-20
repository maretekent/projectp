from django.shortcuts import render
from rest_framework import generics
from .models import MyModel
from .serializers import MyModelSerializer


class MyModelView(generics.GenericAPIView):
	queryset = MyModel.objects.all()
	serializer_class = MyModelSerializer

	def get(self, request, *args, **kwargs):
		instance = self.get_object()
		serializer = self.get_serializer(instance)
		return Response(serializer.data)

	def post(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#####################################################

from django.shortcuts import render
from rest_framework import generics
from .models import MyModel
from .serializers import MyModelSerializer


class MyModelCreateView(generics.CreateAPIView):
	queryset = MyModel.objects.all()
	serializer_class = MyModelSerializer


from rest_framework import serializers
from .models import MyModel


class MyModelSerializer(serializers.ModelSerializer):
	class Meta:
		model = MyModel
		fields = '__all__'


##########################################################

from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from .models import MyModel
from .serializers import MyModelSerializer


class MyModelView(generics.GenericAPIView):
	queryset = MyModel.objects.all()
	serializer_class = MyModelSerializer
	permission_classes = [permissions.IsAuthenticatedOrReadOnly]

	def get(self, request, *args, **kwargs):
		instance = self.get_object()
		self.check_object_permissions(request, instance)
		serializer = self.get_serializer(instance)
		return Response(serializer.data)

	def post(self, request, *args, **kwargs):
		self.check_permissions(request)
		serializer = self.get_serializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


##############################################################################################

from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from .models import MyModel, ForeignModel
from .serializers import MyModelSerializer


class MyModelView(generics.GenericAPIView):
	queryset = MyModel.objects.all()
	serializer_class = MyModelSerializer
	permission_classes = [permissions.IsAuthenticatedOrReadOnly]

	def get(self, request, *args, **kwargs):
		instance = self.get_object()
		self.check_object_permissions(request, instance)
		serializer = self.get_serializer(instance)
		return Response(serializer.data)

	def post(self, request, *args, **kwargs):
		self.check_permissions(request)
		serializer = self.get_serializer(data=request.data)
		if serializer.is_valid():
			foreign_key = ForeignModel.objects.get(pk=request.data['foreign_key'])
			instance = serializer.save(foreign_key=foreign_key)
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


###############################################################################

from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from .models import MyModel, ForeignModel
from .serializers import MyModelSerializer


class MyModelView(generics.GenericAPIView):
	queryset = MyModel.objects.all()
	serializer_class = MyModelSerializer
	permission_classes = [permissions.IsAuthenticatedOrReadOnly]

	def put(self, request, *args, **kwargs):
		instance = self.get_object()
		self.check_object_permissions(request, instance)
		serializer = self.get_serializer(instance, data=request.data)
		if serializer.is_valid():
			foreign_key = ForeignModel.objects.get(pk=request.data['foreign_key'])
			instance = serializer.save(foreign_key=foreign_key)
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


###############################################################################

posts = Post.objects.select_related('author').all()
for post in posts:
	print(post.title)
	print(post.author.name)

posts = Post.objects.prefetch_related('comments').all()
for post in posts:
	print(post.title)
	for comment in post.comments.all():
		print(comment.text)

################################################################################
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

#################################################################################

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

#################################################################################


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


############################################################################################

class CountryResidenceRisk(models.Model):
	country = models.ForeignKey(Country, unique=True, related_name='CountryResidenceRisks', on_delete=models.CASCADE)
	country_risk_score = models.IntegerField(blank=True, null=True)


class Country(models.Model):
	country_name = models..CharField(max_length=100)


class CountrySerializer(serializers.ModelSerializer):
	class Meta:
		model = Country
		fields = ['country_id_alpha2', 'country_id_alpha3', 'country_name']


class CountryResidenceRiskSerializer(serializers.ModelSerializer):
	country = CountrySerializer(many=True, read_only=True)

	class Meta:
		model = CountryResidenceRisk
		fields = ['country', 'country_risk_score', 'country_risk_level']


class CountryResidenceRiskView(APIView):
	queryset = CountryResidenceRisk.objects.all()
	serializer_class = CountryResidenceRiskSerializer
	permission_classes = [permissions.IsAuthenticatedOrReadOnly]

	def get(self, request, *args, **kwargs):
		instance = self.get_object()
		self.check_object_permissions(request, instance)
		serializer = self.get_serializer(instance)
		return Response(serializer.data)

	def post(self, request, *args, **kwargs):
		self.check_permissions(request)
		serializer = self.get_serializer(data=request.data)
		if serializer.is_valid():
			foreign_key = Country.objects.get(pk=request.data['foreign_key'])
			instance = serializer.save(country=foreign_key)
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


	def put(self, request, *args, **kwargs):
		countries = request.data.get('countries')
		for country in countries:
			pk = country.get('country_residence_id')
			residence_risk = get_object_or_404(CountryResidenceRisk, pk=pk)
			serializer = CountryResidenceRiskSerializer(residence_risk, data=request.data)
			if serializer.is_valid():
				serializer.save()
				return Response(serializer.data)
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


###################################################################################################

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


######################################################################################

def log_benchmark(start_time, response, event, clazz):
	end_time = time.time()
	duration = (end_time - start_time) * 1000
	logger.info(
		event=event,
		view_class=clazz,
		status_code=response.status_code,
		response_data=response.data,
		end_time=end_time,
		duration_millis=duration
	)

