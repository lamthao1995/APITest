from __future__ import unicode_literals
from commonlib.models import *
from commonlib.constant import *
from commonlib.helper import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django import forms
from django.core.cache import cache
import json
def require_login(func):
	def is_login(self, request):
		if not ADMIN_TOKEN in request.COOKIES:
			return HttpResponse(json.dumps({ERROR : STATUS_NEED_LOGIN}));
		admin_token = request.COOKIES[ADMIN_TOKEN];
		admin_user = None;
		try:
			admin_user = Admin.objects.get(token = admin_token);
		except Exception as e:
			write_error_into_log(e);
			return HttpResponse(json.dumps({ERROR : STATUS_NEED_LOGIN}));
		return func(self, request);
	return is_login
class Controller(object):
	@require_login
	def display_event(self, request):
		event_list = Event.objects.all();
		paginator = Paginator(event_list, NUM_OF_EVENT_FOR_DISPLAY_IN_A_PAGE);
		page = request.GET[PAGE];
		try:
			posts = paginator.page(page);
		except PageNotAnInteger as e:
			write_error_into_log(e);
			posts = paginator.page(DEFAULT_PAGE);
		except EmptyPage as e:
			write_error_into_log(e);
			posts = paginator.page(paginator.num_pages);
		
		template = loader.get_template('administrator/displayforadmin.html');
		context = {'posts' : posts};
		return HttpResponse(template.render(context, request));
	@require_login
	def insert_event_gui(self, request):
		template = loader.get_template('administrator/upload.html');
		context = {'redirect' : '/administrator/InsertNewEventAPI/'};	
		return HttpResponse(template.render(context, request));
	@require_login
	def insert_new_event(self, request):
		event_title = request.POST[EVENT_TITLE];
		event_location = request.POST[EVENT_LOCATION];
		event_description = request.POST[EVENT_DESCRIPTION];
		event_date = request.POST[EVENT_DATE];
		image_file = request.FILES[EVENT_IMAGE_FILE];
		event_url_image_name = str(image_file);
		event_url_image_name = generate_file_name(event_url_image_name);
		event_url_image_name = handle_upload_file(image_file, event_url_image_name);
		new_event = Event(event_title = event_title, event_location = event_location, event_description = event_description, event_date = event_date, url_media = event_url_image_name);
		new_event.save();
		if not cache.get(GET_NUMBER_OF_EVENT_CACHE) == None:
			cache.delete(GET_NUMBER_OF_EVENT_CACHE);
		if not cache.get(GET_NUMBER_OF_SEARCH_TEXT_EVENT_CACHE) == None:
			cache.delete(GET_NUMBER_OF_SEARCH_TEXT_EVENT_CACHE);
		if not cache.get(GET_PAGINATED_EVENT_CACHE) == None:
			cache.delete(GET_PAGINATED_EVENT_CACHE);
		if not cache.get(GET_SEARCH_TEXT_EVENT_CACHE) == None:
			cache.delete(GET_SEARCH_TEXT_EVENT_CACHE);
		return HttpResponse(json.dumps({SUCCESS : STATUS_UPLOADED_INFO_SUCCESSFULLY}));
	@require_login
	def index(self, request):
		template = loader.get_template('administrator/admingui.html');
		context = {'insert_event' : '/administrator/InsertEventGUI/', 'page_num' : DEFAULT_PAGE};
		return HttpResponse(template.render(context, request));
	@require_login
	def admin_login(self, request):
		template = loader.get_template('administrator/adminlogin.html');
		context = {'link' : '/administrator/AdminLoginProcess'};		
		return HttpResponse(template.render(context, request));
	@require_login
	def admin_logout(self, request):
		admin_token = request.COOKIES[ADMIN_TOKEN];
		res = HttpResponseRedirect('/administrator/AdminLogin/');
		res.delete_cookie(ADMIN_TOKEN);
		return res;
	@require_login
	def admin_login_process(self, request):
		password = request.POST[PASSWORD];
		username = request.POST[USER_NAME];
		password_hash = hash_password(password);
		try:
			admin_user = Admin.objects.get(username = username, password = password_hash);
			token = generate_token(password);
			admin_user.token = token;
			admin_user.save();
			res = HttpResponseRedirect('/administrator/index');
			res.set_cookie(ADMIN_TOKEN, token);
			return res;
		except Exception as e:
			write_error_into_log(e);
			return HttpResponse(json.dumps({ERROR : 'Your password or username was wrong'}));
