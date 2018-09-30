# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from commonlib.manager.usermanager import *
# Create your views here.
controller = Controller();
@csrf_exempt
def do_login_api(request):
	return controller.do_login(request);
def get_salt_api(request):
	return controller.get_salt(request);
def do_logout_api(request):
	return controller.do_logout(request);
def get_number_of_events_api(request):
	return controller.get_number_of_events(request);
def get_paginated_list_of_event_api(request):
	return controller.get_paginated_list_of_event(request);
def get_participant_api(request):
	return controller.get_participant(request);
def get_comment_api(request):
	return controller.get_comment(request);
def get_number_of_event_api(request):
	return controller.get_number_of_events(request);

def get_number_of_search_event_api(request):
	return controller.get_number_of_search_event(request);

def get_search_text_event_api(request):
	return controller.get_search_text_event(request);
def get_users_like_event_api(request):
	return controller.get_users_like_event(request);
@csrf_exempt
def insert_new_user_api(request):
	return controller.insert_new_user(request);
@csrf_exempt
def insert_new_comment_api(request):
	return controller.insert_new_comment(request);
def insert_new_like_api(request):
	return controller.insert_new_like(request);
def insert_new_participant_api(request):
	return controller.insert_new_participant(request);
