from commonlib.constant import *
from commonlib.models import *
from commonlib.helper import *
from time import gmtime, strftime
from django.http import HttpResponse
from django.core.cache import cache
import json
#decorator for checking login status
def require_login(func):
	def fun_wrapper(self, request):
		if not TOKEN in request.COOKIES:
			return HttpResponse(json.dumps({ERROR : STATUS_NOT_LOG_IN})); 
		token = request.COOKIES[TOKEN];
		if cache.get(token) == None:
			return HttpResponse(json.dumps({ERROR : STATUS_TIME_OUT}));
		return func(self, request);
	return fun_wrapper
class Controller(object):
	def get_salt():
		user_name = request.POST[USER_NAME];
		query = '{} : {}'.format(user_name, SALT);
		if not cache.get(query) == None:
			return HttpResponse(cache.get(query));
		try:		
			user = Individual.objects.get(username = user_name);
			context = {SALT : user.salt};
			result =json.dumps({SUCCESS : context});
			cache.set(query, result, TIME_LIFE_FOR_SALT);
			return HttpResponse(result);
		except Exception as e:
			write_error_into_log(e);
			result = json.dumps({ERROR : STATUS_ACCOUNT_NOT_EXISTED});
			return HttpResponse(result);
	def do_login(self, request):
		user_name = request.POST[USER_NAME];	
		encrypted_password = request.POST[PASSWORD];
		if not cache.get(user_name) == None:
			return HttpResponse(json.dumps({ERROR : context}));
		user = None;	
		try:	
			user = Individual.objects.get(username = user_name, password = encrypted_password);
		except Exception as e:
			write_error_into_log(e)
			user = None;

		res = HttpResponse(json.dumps({SUCCESS : STATUS_IS_LOGINED}));
		if user == None:
			context = {ERROR : STATUS_FAILED_IN_LOGIN};
			return HttpResponse(json.dumps({ERROR : context}));
		else:
			token = generate_token(encrypted_password);
			user.token = token;
			user.save();
			res.set_cookie(key = TOKEN, value = token, max_age = TIME_OUT_FOR_COOKIE);
			cache.set(token, user);
			return res;
	@require_login
	def do_logout(self, request):
		res = HttpResponse(json.dumps({SUCCESS : STATUS_LOG_OUT_SUCESSFULLY}));
		#get token and then delete it
		token = request.COOKIES[TOKEN];
		if not cache.get(token) == None:
			cache.delete(token);
		res.delete_cookie(TOKEN);
		return res;
	@require_login
	def insert_new_like(self, request):
		new_event_id = int(request.GET[EVENT_ID]);
		token = request.COOKIES[TOKEN];
		user = cache.get(token);
		print(user.individual_id, "------ ", new_event_id);
		try:			
			like_list = Like.objects.filter(event_id = new_event_id, individual_id = user.individual_id);
			if not len(like_list) == 0:
				return HttpResponse(json.dumps({ERROR : STATUS_ERROR_LIKE}));
			new_like = Like(event_id = new_event_id, individual_id = user.individual_id);
			new_like.save();
		except Exception as e:
			write_error_into_log(e);
			return HttpResponse(json.dumps({ERROR : STATUS_ERROR_LIKE}));	
		self.delete_cache(GET_USER_LIKE_POST);
		return HttpResponse(json.dumps({SUCCESS : STATUS_SUCCESS_LIKE}));
	@require_login
	def insert_new_comment(self, request):	
		token = request.COOKIES[TOKEN];
		user = cache.get(token);
		user_id = user.individual_id;
		event_id = int(request.POST[EVENT_ID]);
		content = request.POST[COMMENT_CONTENT];
		time_now = str(strftime("%Y-%m-%d", gmtime()));	
		try:
			comment = Comment(event_id = event_id, individual_id = user_id, content = content, date = time_now);
			comment.save();
		except Exception as e:
			write_error_into_log(e);
			return HttpResponse(json.dumps({ERROR : 'Something wrong with db'}));
		#delete date in cache because something changes in db
		self.delete_cache(GET_COMMENT_CACHE);
		return HttpResponse(json.dumps({SUCCESS : STATUS_COMMENT_SUCCESS}));	
	@require_login
	def insert_new_participant(self, request):
		token = request.COOKIES[TOKEN];
		user = cache.get(token);
		eventid = int(request.GET[EVENT_ID]);
		try:
			user_list = Participant.objects.filter(event_id = eventid, individual_id = user.individual_id);
			if not len(user_list) == 0:
				return HttpResponse(json.dumps({ERROR : STATUS_HAVE_JOINED_EVENT}));
			parti = Participant(event_id = int(eventid), individual_id = int(user.individual_id));
			parti.save();
		except Exception as e:
			write_error_into_log(e);
			return HttpResponse(json.dumps({ERROR : STATUS_HAVE_JOINED_EVENT}));
		self.delete_cache(GET_PARTICIPANT_CACHE);
		return HttpResponse(json.dumps({SUCCESS : STATUS_JOIN_EVENT_SUCCESSFULLY}));
	@require_login
	def get_participant(self, request):
		event_id = int(request.GET[EVENT_ID]);
		query = '{}'.format(event_id);
		if not cache.get(GET_PARTICIPANT_CACHE) == None:
			participant_dict = cache.get(GET_PARTICIPANT_CACHE);
			if not participant_dict.get(query) == None:
				return HttpResponse(participant_dict.get(query));
		participant_item = Participant.objects.filter(event_id = event_id);
		individual_item = [];
		for parti in participant_item:
			try:
				individual_item.append(Individual.objects.get(individual_id = parti.individual_id));
			except Exception as e:
				write_error_into_log(e);
		individual_dict = item_json_format(individual_item);
		result = json.dumps({SUCCESS : individual_dict});
		self.save_data_into_cache(GET_PARTICIPANT_CACHE, query, result);
		return HttpResponse(result);
	@require_login
	def get_comment(self, request):
		eventid = int(request.GET[EVENT_ID]);
		query = '{}'.format(eventid);
		if not cache.get(GET_COMMENT_CACHE) == None:
			comment_dict = cache.get(GET_COMMENT_CACHE);
			if not comment_dict.get(query) == None:
				return HttpResponse(comment_dict.get(query));
		items = None;
		result = '';
		try:	
			items = Comment.objects.filter(event_id = eventid);	
		except Exception as e:
			write_error_into_log(e);		
		comment_dict = item_json_format(items);
		result = json.dumps({SUCCESS : comment_dict});
		self.save_data_into_cache(GET_COMMENT_CACHE, query, result);
		return HttpResponse(result);
	@require_login	
	def get_paginated_list_of_event(self, request):
		start_index = int(request.GET[START_INDEX]);
		end_index = int(request.GET[END_INDEX]);
		query = '{} {}'.format(start_index, end_index);
		if not cache.get(GET_PAGINATED_EVENT_CACHE) == None:
			event_dict = cache.get(GET_PAGINATED_EVENT_CACHE);
			if not event_dict.get(query) == None:
				return HttpResponse(event_dict.get(query));
		event_list = Event.objects.all().order_by('-event_date')[start_index : end_index];
		event_dict = item_json_format(event_list);
		result = json.dumps({SUCCESS :event_dict});
		self.save_data_into_cache(GET_PAGINATED_EVENT_CACHE, query, result);
		return HttpResponse(result);		
	@require_login
	def get_number_of_events(self, request):
		if not cache.get(GET_NUMBER_OF_EVENT_CACHE) == None:
			return HttpResponse(cache.get(GET_NUMBER_OF_EVENT_CACHE));
		number_of_events = Event.objects.count();
		context = {NUM_OF_EVENT : number_of_events};
		result = json.dumps({SUCCESS : context});
		cache.set(GET_NUMBER_OF_EVENT_CACHE, result);
		return HttpResponse(result);
	@require_login	
	def get_search_text_event(self, request):
		search_text = request.GET[SEARCH_TEXT];
		start_index = int(request.GET[START_INDEX]);
		end_index = int(request.GET[END_INDEX]);
		query = '{} {} {}'.format(search_text, start_index, end_index);
		if not cache.get(GET_SEARCH_TEXT_EVENT_CACHE) == None:
			search_event_dict = cache.get(GET_SEARCH_TEXT_EVENT_CACHE);
			if not search_event_dict.get(query) == None:
				return HttpResponse(search_event_dict.get(query));
		event_list = Event.objects.filter(event_title__startswith = search_text)[start_index : end_index];
		event_dict = item_json_format(event_list);
		result = json.dumps({SUCCESS : event_dict});
		#save in cache
		self.save_data_into_cache(GET_SEARCH_TEXT_EVENT_CACHE, query, result);
		return HttpResponse(result);
	@require_login
	def get_number_of_search_event(self, request):
		search_text = request.GET[SEARCH_TEXT];
		query = '{}:{}'.format(search_text, GET_NUMBER_OF_SEARCH_TEXT_EVENT_CACHE);
		if not cache.get(query) == None:
			return HttpResponse(cache.get(query));
			
		number_of_events = Event.objects.filter(event_title__startswith = search_text).count();
		context = {NUM_OF_EVENT : number_of_events};
		result = json.dumps({SUCCESS : context});
		cache.set(query, result);
		return HttpResponse(result);
	@require_login
	def get_users_like_event(self, request):
		event_id = int(request.GET[EVENT_ID]);
		query = '{}'.format(event_id);
		if not cache.get(GET_USER_LIKE_POST) == None:
			user_dict = cache.get(GET_USER_LIKE_POST);
			if not user_dict.get(query) == None:
				return HttpResponse(user_dict.get(query));
		list_like = Like.objects.filter(event_id = event_id);
		individual_item = [];
		for item in list_like:
			try:
				individual_item.append(Individual.objects.get(individual_id = item.individual_id));
			except Exception as e:
				write_error_into_log(e);
		individual_dict = item_json_format(individual_item);
		result = json.dumps({SUCCESS : individual_dict});
		self.save_data_into_cache(GET_USER_LIKE_POST, query, result);
		return HttpResponse(result);
	#support function for delete cache if something changes in database
	def delete_cache(self, key):
		if not cache.get(key) == None:
			cache.delete(key);
	def save_data_into_cache(self, key, query, result):
		print("vao roi cac ban oi..............................................");
		if cache.get(key) == None:
			context = {};
			cache.set(key, context);
		new_dict = cache.get(key);
		new_dict[query] = result;
		cache.set(key, new_dict);
	#support function for insertion of new user
	def insert_new_user(self, request):
		phone = request.POST[PHONE];
		email = request.POST[EMAIL];
		firstname = request.POST[FIRST_NAME];
		lastname = request.POST[LAST_NAME];
		username = request.POST[USER_NAME];
		password = request.POST[PASSWORD];
		token = init_token();
		salt = init_salt();
		try:		
			user = Individual.objects.filter(username = username);
			if len(user) != 0:
				return HttpResponse(json.dumps({ERROR : STATUS_ACCOUNT_EXISTED}));
			new_user = Individual(username = username, password = hashPassword(password), firstname = firstname, lastname = lastname, phone = phone, email = email, token = token, salt = salt);
			new_user.save();
		except Exception as e:
			write_error_into_log(e);
			return HttpResponse(json.dumps({ERROR : STATUS_ACCOUNT_EXISTED}));
		return HttpResponse(json.dumps({SUCCESS : STATUS_ACCOUNT_CREATED_SUCCESSFULLY}));
