from django.contrib import admin
from .models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "full_name",
        "cart_summary",   
        "amount",
        "created_at",
    )
    search_fields = ("payment_id", "order_id", "full_name", "email", "phone")

    readonly_fields = (
        "payment_id",
        "order_id",
        "signature",
        "amount",
        "cart_items",
        "cart_summary",
        "created_at",
    )

    fieldsets = (
        ("Payment", {
            "fields": ("payment_id", "order_id", "signature", "amount")
        }),
        ("Customer", {
            "fields": ("full_name", "email", "phone")
        }),
        ("Address", {
            "fields": ("address", "city", "pincode")
        }),
        ("Cart", {
            "fields": ("cart_summary", "cart_items")  
        }),
        ("Meta", {
            "fields": ("created_at",)
        }),
    )
