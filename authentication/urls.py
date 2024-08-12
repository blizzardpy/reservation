from django.urls import path
from .views import login_view, home_view, register_view
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('home/', home_view, name='home'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
]
