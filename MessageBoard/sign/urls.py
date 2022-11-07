# Импорт из Джанго
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

# Импорт из ресурсов проекта
from .views import SignupView, ActivateView

urlpatterns = [
    path('login/', LoginView.as_view(template_name='sign/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='sign/logout.html'), name='logout'),
    path('signup/', SignupView.as_view(template_name='sign/signup.html'), name='signup'),
    path('activate/', ActivateView.as_view(template_name='sign/activate.html'), name='activate'),
]