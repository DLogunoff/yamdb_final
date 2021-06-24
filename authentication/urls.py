from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import UserViewSet, EmailViewSet


v1_auth_router = DefaultRouter()
v1_auth_router.register(r'users', UserViewSet, basename='users')
v1_auth_router.register(r'auth', EmailViewSet, basename='auth')

app_name = 'authentication'
urlpatterns = [
    path('v1/', include(v1_auth_router.urls)),
]
