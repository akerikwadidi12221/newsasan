from django.contrib import admin
from django.urls import path, re_path, include
from . import views

urlpatterns = [
    # return a simple JSON message at the site root
    re_path(r"^$", views.index, name="index"),
    path('admin/', admin.site.urls),
    path('api/catalog/', include('catalog.urls')),
]
