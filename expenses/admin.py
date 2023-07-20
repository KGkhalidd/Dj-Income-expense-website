from django.contrib import admin
from .models import Category , Expense
# Register your models here.

admin.site.register(Expense)
admin.site.register(Category)




# to create superuser use -> winpty python manage.py createsuperuser
