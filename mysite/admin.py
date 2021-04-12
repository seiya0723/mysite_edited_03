from django.contrib import admin
from .models import Products, Category, Shop,Cart,History
# Register your models here.

admin.site.register(Products)
admin.site.register(Category)
admin.site.register(Shop)
admin.site.register(Cart)
admin.site.register(History)
