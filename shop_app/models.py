from django.db import models
from django.utils.text import slugify
from django.conf import settings
from cloudinary.models import CloudinaryField
from decimal import Decimal

class Product(models.Model):
    CATEGORY_CHOICES = (
        ('timepieces', 'Timepieces'),
        ('jewellery', 'Jewellery'),
        ('fashion', 'Fashion'),
        ('accessories', 'Accessories'),
    )

    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='fashion')
    product_name = models.CharField(max_length=200, blank=True, null=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)
    image = models.URLField(max_length=500, blank=True, null=True)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=Decimal('0.0'))
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=500, blank=True, null=True)
    key_features = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.product_name

    def save(self, *args, **kwargs):
        if not self.slug and self.product_name:
            base_slug = slugify(self.product_name)
            unique_slug = base_slug
            counter = 1
            while Product.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = unique_slug
        super().save(*args, **kwargs)


class Card(models.Model):
    cart_code = models.CharField(max_length=11, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modified_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.cart_code


class CardItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Card, on_delete=models.CASCADE, related_name='items')
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.product_name} - {self.quantity} in cart {self.cart.id}"
