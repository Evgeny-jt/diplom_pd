"""
URL configuration for orders project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from rest_framework.routers import DefaultRouter

from backend.views import UserRegistration, ShopView, CategoryView, UpPriseView, ProductView, ProductFilterView, LoginView, OrderView, ContactView, BasketView, SendInvoice, Status


urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', UserRegistration.as_view()),
    path('user/register/', UserRegistration.as_view()),
    path('user/login/', LoginView.as_view()),
    path('product/filter/', ProductFilterView.as_view()),
    path('orderitem/', BasketView.as_view()),

    path('order/', OrderView.as_view()),
    path('contact/', ContactView.as_view()),
    path('sendinvoice/', SendInvoice.as_view()),
    path('status/', Status.as_view()),

    path('shop/', ShopView.as_view()),
    path('category/', CategoryView.as_view()),
    path('up/', UpPriseView.as_view()),
    path('product/', ProductView.as_view()),

]
