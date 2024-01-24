from django.urls import include, path

urlpatterns = [
    path('user/', include('apps.user.urls')),
    path('categories/', include('apps.category.urls')),
]
