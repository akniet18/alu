from django.contrib import admin
from .models import *

class dateOrder(admin.ModelAdmin):
	readonly_fields = ('rented_day',)

admin.site.register(Rented)
