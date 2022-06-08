from django.conf import settings
from django.conf.urls.static import static

from .views import login_view, registration_view, dashboard
from django.urls import path

urlpatterns = [
    path('', login_view, name='login'),
    path('register/', registration_view, name='register'),
    path('dashboard/', dashboard, name='dashboard'),
]