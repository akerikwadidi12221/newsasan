# backend/catalog/models.py
from django.db import models
from django.conf import settings  # برای گرفتن مدل User
from mptt.models import MPTTModel, TreeForeignKey

# --------------------------------------------------
# 1) دسته‌بندی‌ها
# --------------------------------------------------
class Category(MPTTModel):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    parent = TreeForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="children",
    )
    image_url = models.CharField(max_length=255, blank=True)
    display_order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["display_order", "name"]

    class MPTTMeta:
        order_insertion_by = ["name"]

    def __str__(self):
        return self.name


# --------------------------------------------------
# 2) برندها
# --------------------------------------------------
class Brand(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    logo_url = models.CharField(max_length=255, blank=True)
    website = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# --------------------------------------------------
# 3) محصول
# --------------------------------------------------
class Product(models.Model):
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    brand = models.ForeignKey(
        Brand, on_delete=models.SET_NULL, null=True, blank=True
    )
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    min_order_quantity = models.PositiveIntegerField(default=1)
    shipping_availability = models.BooleanField(default=True)
    supplier = models.ForeignKey(
        'users.SupplierProfile',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='products'
    )
    stock_quantity = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["category"]),
            models.Index(fields=["code"]),
        ]

    def __str__(self):
        return self.name


# --------------------------------------------------
# 4) تصاویر محصول
# --------------------------------------------------
class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="images"
    )
    image_url = models.CharField(max_length=255)
    alt_text = models.CharField(max_length=255, blank=True)
    is_primary = models.BooleanField(default=False)
    display_order = models.IntegerField(default=0)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["display_order"]

    def __str__(self):
        return f"{self.product.name} image"


# --------------------------------------------------
# 5) انواع مشخصات (Specification Types)
# --------------------------------------------------
class SpecificationType(models.Model):
    DATA_TYPES = [
        ("text", "Text"),
        ("int", "Integer"),
        ("float", "Float"),
        ("bool", "Boolean"),
    ]

    name = models.CharField(max_length=255)
    data_type = models.CharField(max_length=50, choices=DATA_TYPES)
    unit = models.CharField(max_length=50, blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# --------------------------------------------------
# 6) مقدار مشخصات برای هر محصول
# --------------------------------------------------
class ProductSpecification(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="specifications"
    )
    specification_type = models.ForeignKey(
        SpecificationType, on_delete=models.CASCADE
    )
    value = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.specification_type.name}: {self.value}"


# --------------------------------------------------
# 7) واریانت‌ها / مدل‌های مختلف محصول
# --------------------------------------------------
class ProductVariant(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="variants"
    )
    variant_name = models.CharField(max_length=255)
    price_difference = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    stock_quantity = models.IntegerField(default=0)
    sku = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.product.name} - {self.variant_name}"


# --------------------------------------------------
# 8) محصولات مرتبط
# --------------------------------------------------
class RelatedProduct(models.Model):
    RELATION_CHOICES = [
        ("upsell", "Upsell"),
        ("crosssell", "Cross-sell"),
        ("similar", "Similar"),
    ]

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="related_base"
    )
    related_product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="related_to"
    )
    relation_type = models.CharField(max_length=50, choices=RELATION_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("product", "related_product", "relation_type")

    def __str__(self):
        return f"{self.product} → {self.related_product} ({self.relation_type})"


# --------------------------------------------------
# 9) برچسب‌های محصول
# --------------------------------------------------
class ProductTag(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="tags"
    )
    tag_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["product"]),
            models.Index(fields=["tag_name"]),
        ]
        unique_together = ("product", "tag_name")

    def __str__(self):
        return self.tag_name


# --------------------------------------------------
# 10) نظرات و امتیازها
# --------------------------------------------------
class ProductReview(models.Model):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="reviews"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField(blank=True)
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("product", "user")

    def __str__(self):
        return f"{self.product} ({self.rating})"
