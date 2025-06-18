from django.contrib import admin
from . import models
from django.db.models import Count

@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ["title", "total_product"]
    @admin.display(ordering="total_product")
    def total_product(self, collection):
        return collection.total_product
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(total_product = Count("product"))
    
@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["title", "unit_price", "inventory_status", "collection_title"]
    list_editable = ["unit_price"]
    list_per_page = 10
    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory<10:
            return "LOW"
        return "OK"
    list_select_related = ["collection"]
    def collection_title(self, product):
        return product.collection.title
@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name", "membership"]
    list_editable = ["membership"]
    list_per_page =10
@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["customer_name","placed_at"]



    list_select_related = ["customer"]
    @admin.display(ordering="customer")
    def customer_name(self, order):
        return order.customer.first_name+" "+ order.customer.last_name