# payment/models.py
from django.db import models
from django.conf import settings

class Transaction(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="transactions"
    )

    payment_id = models.CharField(max_length=200, verbose_name="Payment ID")
    order_id = models.CharField(max_length=200, verbose_name="Order ID")
    signature = models.CharField(
        max_length=500, verbose_name="Signature", blank=True, null=True
    )
    amount = models.IntegerField(verbose_name="Amount")   

    full_name = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)  
    city = models.CharField(max_length=100, blank=True, null=True)
    pincode = models.CharField(max_length=10, blank=True, null=True)
    cart_items = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id} - {self.payment_id}"
    
    def cart_summary(self):
        
        if not self.cart_items:
            return ""

        try:
            parts = []
            for item in self.cart_items:
                product = item.get("product", {}) or {}
                name = (
                    product.get("product_name")
                    or product.get("name")
                    or "Unknown"
                )
                qty = item.get("quantity", 1)
                parts.append(f"{name} x{qty}")
            return ", ".join(parts)
        except Exception:
            return str(self.cart_items)

    cart_summary.short_description = "Items"
