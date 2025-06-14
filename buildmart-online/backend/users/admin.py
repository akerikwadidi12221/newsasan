from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

# اگر هیچ فیلد سفارشی دیگری ندارید می‌توانید همان BaseUserAdmin را استفاده کنید
class UserAdmin(BaseUserAdmin):
    pass

admin.site.register(User, UserAdmin)
