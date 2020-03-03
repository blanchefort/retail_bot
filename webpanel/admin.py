from django.contrib import admin
from .models.product_category import ProductCategory
from .models.product_unit_type import ProductUnitType
from .models.product import Product
from .models.order import Order
from .models.seller_bill import SellerBill
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

admin.site.register(ProductCategory)
admin.site.register(Order)
admin.site.register(SellerBill)


@admin.register(ProductUnitType)
class AdminProductUnitType(admin.ModelAdmin):
    list_display = ('name', 'short',)


@admin.register(Product)
class AdminProduct(admin.ModelAdmin):
    list_display = ('title', 'category', 'user', 'unit', 'price',)
    list_filter = ('title', 'category', 'user',)
    search_fields = ('title',)