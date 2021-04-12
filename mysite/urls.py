from django.conf.urls import url
from django.http import HttpResponse
from django.urls import path
from . import views

app_name = 'mysite'

urlpatterns = [
    path('', views.top, name='top'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
]
