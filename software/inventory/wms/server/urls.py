from django.urls import path
from server import views
from controller import views as controller_views

urlpatterns = [
    path('', views.home,  name='home'),
    path('about/', views.about,  name='about'),
    path('contact/', views.contact,  name='contact'),
    path('panel/', controller_views.home, name='panel'),
]