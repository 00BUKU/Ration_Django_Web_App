from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # '' -> localhost:8000
    path('', include('main_app.urls')),
    # include the built-in auth urls for the built-in views
    path('accounts/', include('django.contrib.auth.urls')),
]