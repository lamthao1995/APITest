from django.conf.urls import include, url
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
	#for admin
	#for user API'
	url(r'DoLoginAPI', views.do_login_api, name = 'DoLoginAPI'),
	url(r'DoLogoutAPI', views.do_logout_api, name = 'DoLogoutAPI'),
	url(r'GetSaltAPI', views.get_salt_api, name = 'GetSaltAPI'),
	url(r'GetNumberOfEventsAPI', views.get_number_of_events_api, name = 'GetNumberOfEvents'),
	url(r'GetPaginatedListOfEventAPI', views.get_paginated_list_of_event_api, name = 'GetPaginatedListOfEventAPI'),
	url(r'GetParticipant', views.get_participant_api, name = 'GetParticipantAPI'),
	url(r'GetCommentAPI', views.get_comment_api, name = 'GetCommentAPI'),
	url(r'InsertNewCommentAPI', views.insert_new_comment_api, name = 'InsertNewCommentAPI'),
	url(r'InsertNewLikeAPI', views.insert_new_like_api, name = 'insertNewLikeAPI'),
	url(r'InsertNewParticipantAPI', views.insert_new_participant_api, name = 'InsertNewParticipantAPI'),
	url(r'GetNumberOfEventAPI', views.get_number_of_event_api, name = 'GetNumberOfEventAPI'),
	url(r'GetNumberOfSearchEventAPI', views.get_number_of_search_event_api, name = 'GetNumberOfSearchEventAPI'),
	url(r'GetSearchTextEventAPI', views.get_search_text_event_api, name = 'GetSearchTextEventAPI'),
	url(r'GetUsersLikeEventAPI', views.get_users_like_event_api, name = 'GetUsersLikeEventAPI'),
	url(r'InsertNewUserAPI', views.insert_new_user_api, name = 'InsertNewUserAPI'),
]
