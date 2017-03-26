from django.conf.urls import url
from anandhibot import views
from django.views.generic import TemplateView

urlpatterns = [
   	 url(r'^$', views.callback, name='callback')
]