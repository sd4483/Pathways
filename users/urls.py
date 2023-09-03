from django.urls import path
from . import views
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.views.generic import RedirectView


urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', LoginView.as_view(template_name='registration/login_template.html', next_page='view_pathway'), name='login'),
    path('logout/', LogoutView.as_view(next_page='view_pathway'), name='logout'),
    path('', RedirectView.as_view(pattern_name='view_pathway'), name='home'),
]