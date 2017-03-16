from django.conf.urls import url
from anandhibot import views


urlpatterns = [
     url(r'^$', views.HomePageView.as_view()),
]