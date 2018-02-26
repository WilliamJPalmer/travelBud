from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^newTrip$', views.newTrip, name='newTrip'),
    url(r'^addTrip$', views.addTrip, name='addTrip'),
    url(r'^destDetail/(?P<id>\d+)$', views.destDetail, name='destDetail'),
    url(r'^joinPlan/(?P<id>\d+)$', views.joinPlan, name='joinPlan'),

]
