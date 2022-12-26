from django.contrib import admin
from .models import Payment, Order, OrderProduct
# Register your models here.

# To show ordered products in Order we need to create this class.
class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    readonly_fields = ('payment', 'user', 'product', 'quantity', 'product_price', 'ordered')
    extra = 0

# Creating own style of Orders in admin page
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number',
                    'full_name',
                    'phone',
                    'email',
                    'city',
                    'order_total',
                    'tax',
                    'status',
                    'is_ordered',
                    'created_at',
                    'ip'
                    ]
    list_filter = ['status', 'is_ordered']
    search_fields = ['order_number', 'first_name', 'last_name', 'phone', 'email']
    list_per_page = 50
    inlines = [OrderProductInline]


admin.site.register(Order, OrderAdmin)
admin.site.register(Payment)
admin.site.register(OrderProduct)

