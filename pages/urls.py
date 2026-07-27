from django.urls import path
from pages import views

urlpatterns = [
    path('', views.home_page, name='home'),
    path('tester/', views.welcome_user, name='welcome')
]
