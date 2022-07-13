from django.conf import settings
from django.conf.urls.static import static

from .views import login_view, registration_view, dashboard, logout_view, razorpay
from django.urls import path

urlpatterns = [
    path('', login_view, name='login'),
    path('register/', registration_view, name='register'),
    path('dashboard/<int:status>', dashboard, name='dashboard'),
    path('genId/', razorpay, name='razorpay'),
    path('logout/', logout_view, name="logout"),
]