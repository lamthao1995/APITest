from django.conf.urls import include, url
from django.conf.urls.static import static
from django.conf import settings
from . import views
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns = [
	url(r'EventDisplay', views.event_display, name = 'EventDisplay'),
	url(r'InsertEventGUI', views.insert_event_gui, name = 'InsertEventGUI'),
	url(r'InsertNewEventAPI', views.insert_new_event_api, name = 'InsertNewEventAPI'),
	url(r'index', views.index, name = 'index'),
	url('AdminLogin/', views.admin_login, name = 'AdminLogin'),
	url('AdminLogout/', views.admin_logout, name = 'AdminLogout'),
	url('AdminLoginProcess/', views.admin_login_process, name = 'AdminLoginProcess'),
] 
urlpatterns += staticfiles_urlpatterns()
