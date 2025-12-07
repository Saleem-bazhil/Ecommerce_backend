from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Product, Card, CardItem


@admin.register(Product)
class ProductAdmin(ImportExportModelAdmin):
    list_display = (
        "product_name",   
        "category",
        "price",
        "rating",
        "slug",
    )
    search_fields = ("product_name", "category")
    list_filter = ("category",)


@admin.register(Card)
class CardAdmin(ImportExportModelAdmin):
    list_display = ("cart_code", "user", "paid", "created_at", "modified_at")


@admin.register(CardItem)
class CardItemAdmin(ImportExportModelAdmin):
    list_display = ("product", "cart", "quantity")
