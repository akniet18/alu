from django.contrib import admin
from .models import *

class dateOrder(admin.ModelAdmin):
	readonly_fields = ('created',)

admin.site.register(Message, dateOrder)