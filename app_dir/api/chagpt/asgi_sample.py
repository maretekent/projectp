from django.urls import path
from django.http import HttpResponse
from django.core.asgi import get_asgi_application


def my_asgi_endpoint(scope, receive, send):
	if scope["type"] == "http":
		response = HttpResponse("Hello, World!")
		response["Content-Type"] = "text/plain"
		send(response)


urlpatterns = [
	path("my_asgi_endpoint/", get_asgi_application(my_asgi_endpoint)),
]


def my_asgi_endpoint(scope, receive, send):
	if scope["type"] == "http" and scope["method"] == "POST":
		body = b""
		more_body = True
		while more_body:
			message = receive()
			if message["type"] == "http.request":
				body += message.get("body", b"")
				more_body = message.get("more_body", False)
		# do something with the body
		response = HttpResponse("Received your data")
		send(response)

# In this example, we define a simple function called my_asgi_endpoint that takes in three arguments: scope, receive,
# and send. The scope argument is a dictionary that contains information about the request, such as the type of request
# and the path. The receive argument is a function that can be used to receive messages from the client. The send
# argument is a function that can be used to send messages to the client.
#
# In this example, we check if the request type is "http" and if it is we create a simple HttpResponse object with the
# 	message "Hello, World!" and send it back to the client.
#
# We then create a URL pattern that maps the path /my_asgi_endpoint/ to our my_asgi_endpoint function using the
# get_asgi_application function provided by Django.
