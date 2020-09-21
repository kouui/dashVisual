from django.urls import path

from . import views

from . import dashApp_1

urlpatterns = [
    path('', views.home, name="home"),

    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
]
