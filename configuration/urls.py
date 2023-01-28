"""paymentapi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from app_dir.api.views import (
	PaymentFlow,
	PaymentView,
	login,
	validate_payment,
	confirm_payment,
	sample_api,
	TestToken, MessageAPI)

urlpatterns = [
				  path('admin/', admin.site.urls),
				  path('api/v1/pay', PaymentFlow.as_view(), name="payment-flow"),
				  path('api/v1/login', login),
				  path('api/v1/payments/', PaymentView.as_view(), name="payments"),
				  path('api/v1/payments/validate/', validate_payment),
				  path('api/v1/payments/confirm/', confirm_payment),
				  path('api/v1/sampleapi', sample_api),
				  path('api/v1/message', MessageAPI.as_view()),
				  path('api/v1/test', TestToken.as_view(), name="testing"),
			  ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
