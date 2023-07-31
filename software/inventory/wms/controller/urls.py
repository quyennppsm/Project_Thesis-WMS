from django.urls import path
from controller.admin import controller_admin_site
from server import views as server_views
from controller import views

urlpatterns = [
    path('', views.home,  name='home'),
    path('admin/', controller_admin_site.urls,  name='admin'),
    path('recall/', server_views.home, name='recall'),
    path('layout/', views.layout, name='layout'),
    path('slot/', views.slot, name='slot'),
    path('product/', views.product, name='product'),
]