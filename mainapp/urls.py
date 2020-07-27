from . import views
from django.urls import path

urlpatterns = [
    path('', views.login),
    path('login', views.login),
    path('register', views.register),
    path('create_profile', views.user_profile),
    path('edit_profile', views.user_profile),
    path('quote', views.fuel_quote),
    path('history', views.fuel_quote_history),
    path('logout', views.logout),
    path('suggested_price', views.suggested_price)
]
