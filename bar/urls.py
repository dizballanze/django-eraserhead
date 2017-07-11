from django.conf.urls import url

from bar.views import index, empty


urlpatterns = [
    url(r'^$', index),
    url(r'^/empty$', empty),
]
