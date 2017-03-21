from django.conf.urls import url
from anandhibot import views
from django.views.generic import TemplateView

urlpatterns = [
     # url(r'^$', views.HomePageView.as_view()),
     url(r'^input', TemplateView.as_view(template_name = 'input.html')),
   	 url(r'^output/', views.input, name = 'input'),
   	 url(r'^$', views.callback, name='callback')
]