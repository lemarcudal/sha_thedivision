from django.conf.urls import url, include
from . import views
from django.contrib import admin
from .views import (
	viewguides,
	postthread,
	post_detail,
	post_update,
	post_delete,
	)
#from webapp import views
#from django.views.generic import ListView, DetailView#new
#from webapp.models import Post#new

urlpatterns = [
	url(r'^viewguides/$', views.viewguides, name='viewguides'),
	url(r'^postthread/create/$', views.postthread, name='postthread'),
    # url(r'^viewguides/detail/(?P<id>\d+)/$', views.post_detail, name='detail'),
    # url(r'^viewguides/detail/(?P<id>\d+)/edit/$', views.post_update, name='update'),
    # url(r'^viewguides/detail/(?P<id>\d+)/delete/$', views.post_delete, name='post_delete'),
    url(r'^viewguides/detail/(?P<slug>[\w-]+)/$', views.post_detail, name='detail'),
    url(r'^viewguides/detail/(?P<slug>[\w-]+)/edit/$', views.post_update, name='update'),
    url(r'^viewguides/detail/(?P<slug>[\w-]+)/delete/$', views.post_delete, name='post_delete'),

    url(r'^$', views.index, name='index'),
    # url(r'^postthread/', views.postthread, name='postthread'),
    url(r'^notify_success_login/', views.notify_success_login, name='notify_success_login'),
    url(r'^notify_success_register/', views.notify_success_register, name='notify_success_register'),
    url(r'^notify_success_create/', views.notify_success_create, name='notify_success_create'),
    url(r'^notify_success_edit/', views.notify_success_edit, name='notify_success_edit'),
    # url(r'^viewguides/', views.viewguides, name='viewguides'),
    
    


]
