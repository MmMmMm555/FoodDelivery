from django.contrib import admin

from .models import Order, OrderItem


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'payment_type', 'state', 'cancelled',)
    list_editable = ('state',)
    search_fields = ('name',)
    list_filter = ('payment_type', 'state', 'branch', 'cancelled',)
    list_per_page = 10


admin.site.register(Order, OrderAdmin)


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'food', 'amount',)
    list_per_page = 10


admin.site.register(OrderItem, OrderItemAdmin)
