'''Integrating Django with Elasticsearch can be done using the Elasticsearch-Django library.
Here are the general steps to set it up:'''

# Install the elasticsearch-dsl and elasticsearch libraries using pip:
# pip install elasticsearch-dsl elasticsearch

# In your Django project's settings.py file, add the Elasticsearch server's host and port to the DATABASES setting:
DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.postgresql',
		'NAME': 'mydatabase',
		'USER': 'mydatabaseuser',
		'PASSWORD': 'mypassword',
		'HOST': '127.0.0.1',
		'PORT': '5432',
	},
	'elasticsearch': {
		'ENGINE': 'elasticsearch_dsl.backends.elasticsearch',
		'HOSTS': [{'host': 'localhost', 'port': 9200}],
		'INDEX_NAME': 'myindex',
	}
}

# Create a documents.py file in your app, where you will define the Elasticsearch documents that you want to index.
# Here is an example for an index of Book model:

from django_elasticsearch_dsl import DocType, fields
from .models import Book


class BookDocument(DocType):
	title = fields.TextField()
	author = fields.TextField()
	description = fields.TextField()

	class Meta:
		model = Book
		fields = [
			'title',
			'author',
			'description',
		]


#
# In your models.py file, import the BookDocument and connect it to the Book model using the
# @registry.register_documents decorator:

from django_elasticsearch_dsl import registry
from .documents import BookDocument


class Book(models.Model):
	title = models.CharField(max_length=255)
	author = models.CharField(max_length=255)
	description = models.TextField()

	def __str__(self):
		return self.title


registry.register(Book, BookDocument)

# Run the command python manage.py search_index --create to create the index
# You can now use the search method to search through the index:

from elasticsearch_dsl import Search

s = Search().filter("term", author="John Smith")
response = s.execute()

for hit in response:
	print(hit.title)
