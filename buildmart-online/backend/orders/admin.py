from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ("product", "quantity", "price_at_purchase")
    extra = 0
    can_delete = False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("order_number", "user", "status", "total_amount", "created_at")
    list_filter = ("status", "created_at")
    date_hierarchy = "created_at"
    inlines = [OrderItemInline]
    actions = ["mark_as_sent"]

    @admin.action(description="Mark selected orders as sent")
    def mark_as_sent(self, request, queryset):
        updated = queryset.update(status="Shipped")
        self.message_user(request, f"{updated} order(s) marked as sent")

