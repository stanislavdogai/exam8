from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from .views import register_view, ProfileDetailView, UserChangeView, UserPasswordChangeView

app_name = 'accounts'

urlpatterns = [
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('registration/', register_view, name='registration'),
    path('profile/<int:pk>', ProfileDetailView.as_view(), name='profile'),
    path('change/', UserChangeView.as_view(), name='change'),
    path('change_password/', UserPasswordChangeView.as_view(), name='change_password')
]