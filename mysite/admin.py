from django.contrib import admin
from .models import Products, Category, Shop,Cart
# Register your models here.

admin.site.register(Products)
admin.site.register(Category)
admin.site.register(Shop)
admin.site.register(Cart)
