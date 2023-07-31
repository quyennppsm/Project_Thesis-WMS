from django.contrib import admin
from django.urls import path, include
from server import urls as server_urls
from controller import urls as controller_urls

urlpatterns = [
    path('', include(server_urls)),
    path('admin/', admin.site.urls),
    path('controller/', include(controller_urls))
]
