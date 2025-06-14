from rest_framework import serializers
from .models import (
    Category, Brand, Product, ProductImage,
    SpecificationType, ProductSpecification,
    ProductVariant, RelatedProduct, ProductTag, ProductReview
)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'id', 'name', 'description', 'parent',
            'image_url', 'display_order', 'created_at', 'updated_at'
        ]


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = [
            'id', 'name', 'description', 'logo_url', 'website',
            'is_active', 'created_at'
        ]


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = [
            'id', 'image_url', 'alt_text', 'is_primary',
            'display_order', 'uploaded_at'
        ]


class SpecificationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpecificationType
        fields = ['id', 'name', 'data_type', 'unit', 'category', 'created_at']


class ProductSpecificationSerializer(serializers.ModelSerializer):
    specification_type = SpecificationTypeSerializer(read_only=True)

    class Meta:
        model = ProductSpecification
        fields = ['id', 'specification_type', 'value', 'created_at']


class ProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = [
            'id', 'variant_name', 'price_difference',
            'stock_quantity', 'sku', 'is_active'
        ]


class RelatedProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = RelatedProduct
        fields = ['id', 'related_product', 'relation_type', 'created_at']


class ProductTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductTag
        fields = ['id', 'tag_name', 'created_at']


class ProductReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = ProductReview
        fields = ['id', 'user', 'rating', 'comment', 'is_approved',
                  'created_at', 'updated_at']


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    specifications = ProductSpecificationSerializer(many=True, read_only=True)
    variants = ProductVariantSerializer(many=True, read_only=True)
    tags = ProductTagSerializer(many=True, read_only=True)
    reviews = ProductReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'category', 'brand',
            'price', 'stock_quantity', 'is_active',
            'created_at', 'updated_at',
            'images', 'specifications', 'variants',
            'tags', 'reviews'
        ]
