from django.urls import include, re_path

import app_test.views

urlpatterns = [
    re_path(r'^$', app_test.views.index, name='index'),
    re_path(r'^home$', app_test.views.index, name='home'),
    re_path(r'^about$', app_test.views.about, name='about')
]