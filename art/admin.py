from django.contrib import admin

from .models import Art, Category, Order, OrderItem

admin.site.register(Art)
admin.site.register(Category)
admin.site.register(Order)
admin.site.register(OrderItem)

