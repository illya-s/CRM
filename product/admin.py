from django_celery_beat.models import PeriodicTask, IntervalSchedule
from django.contrib import admin
from .models import *

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'article', 'price', 'created')

admin.site.register(Product, ProductAdmin)
admin.site.register(MyProduct)

admin.site.register(Supplier)