from django.contrib import admin
from .models import *


class dateOrder(admin.ModelAdmin):
	readonly_fields = ('created_date',)

admin.site.register(Product, dateOrder)
admin.site.register(ProductImage)
admin.site.register(Recomendation)

