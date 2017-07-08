from django.conf.urls import url

from bar.views import index


urlpatterns = [
    url(r'^$', index),
]
