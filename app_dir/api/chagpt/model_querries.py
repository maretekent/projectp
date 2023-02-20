# models.py
class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

class User(models.Model):
    username = models.CharField(max_length=100)

# views.py
class BookListView(APIView):
    def get(self, request):
        books = Book.objects.select_related('author').filter(author__username='john')
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)
