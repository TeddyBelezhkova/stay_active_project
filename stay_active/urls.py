from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('common.urls')),
    path('participants/', include('participants.urls')),
    path('activities/', include('activities.urls')),
]
