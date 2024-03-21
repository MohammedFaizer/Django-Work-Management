from django.urls import path
from . import views

urlpatterns = [
   path('',views.notfound,name='notfound'),
   path('login/', views.loginPage, name='loginPage'),
   path('register/', views.registerPage, name='registerPage'),  # Fixed typo here
   path('dashboard/', views.dashboard, name='dashboard'),
   path("logout/", views.logoutPage, name="logout"),

]
