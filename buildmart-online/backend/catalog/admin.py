# backend/catalog/admin.py
from django.contrib import admin
from .models import (
    Category, Brand, Product, ProductImage,
    SpecificationType, ProductSpecification,
    ProductVariant, RelatedProduct, ProductTag,
    ProductReview
)

# --------------------------------------------------
# 1) دسته‌بندی و برند (ساده)
# --------------------------------------------------
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "parent", "display_order")
    list_filter  = ("parent",)
    search_fields = ("name",)


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active")
    search_fields = ("name",)
    list_filter = ("is_active",)


# --------------------------------------------------
# 2) اینلاین‌های کمکی برای محصول
# --------------------------------------------------
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1


class ProductSpecInline(admin.TabularInline):
    model = ProductSpecification
    extra = 1


class ProductTagInline(admin.TabularInline):
    model = ProductTag
    extra = 1


class RelatedInline(admin.TabularInline):
    """
    نشان‌دادن محصولاتی که به‌عنوان «مشابه/پیشنهادی» ثبت شده‌اند.
    فیلد محصول مرتبط به‌صورت Lookup باز می‌شود تا جستجو سریع باشد.
    """
    model = RelatedProduct
    fk_name = "product"     # کلید اصلی این Inline
    extra = 1
    raw_id_fields = ("related_product",)  # جلوگیری از لیست طولانی


# --------------------------------------------------
# 3) محصول اصلی
# --------------------------------------------------
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display  = ("name", "category", "brand",
                     "price", "stock_quantity", "is_active")
    list_filter   = ("category", "brand", "is_active")
    search_fields = ("name", "description")
    inlines       = [
        ProductImageInline,
        ProductVariantInline,
        ProductSpecInline,
        ProductTagInline,
        RelatedInline,
    ]
    fieldsets = (
        (None, {
            "fields": (("name", "is_active"),
                       "description",
                       ("category", "brand"),
                       ("price", "stock_quantity"))
        }),
    )


# --------------------------------------------------
# 4) انواع مشخصات (SpecificationType)
# --------------------------------------------------
@admin.register(SpecificationType)
class SpecTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "data_type", "unit", "category")
    list_filter  = ("data_type", "category")
    search_fields = ("name",)


# --------------------------------------------------
# 5) محصولات مرتبط، برچسب‌ها و تصاویر
# (ثبت ساده، چون در Inline هم استفاده شده)
# --------------------------------------------------
admin.site.register(ProductImage)
admin.site.register(ProductSpecification)
admin.site.register(ProductVariant)
admin.site.register(ProductTag)
admin.site.register(RelatedProduct)


# --------------------------------------------------
# 6) نظرات و امتیازها
# --------------------------------------------------
@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ("product", "user", "rating",
                    "is_approved", "created_at")
    list_filter  = ("rating", "is_approved", "created_at")
    search_fields = ("product__name", "user__username", "comment")
    actions = ["approve_reviews"]

    @admin.action(description="Approve selected reviews")
    def approve_reviews(self, request, queryset):
        updated = queryset.update(is_approved=True)
        self.message_user(request, f"{updated} review(s) approved.")
