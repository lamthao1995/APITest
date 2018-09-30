from django.db import models
from django import forms
from constant import *
class Individual(models.Model):
	individual_id = models.IntegerField(primary_key = True);
	username = models.CharField(max_length = 50);
	password = models.CharField(max_length = 50);
	firstname = models.CharField(max_length = 50);
	lastname = models.CharField(max_length =50);
	phone = models.CharField(max_length = 50);
	email = models.CharField(max_length = 50);
	token = models.CharField(max_length = 50);
	salt = models.CharField(max_length = 50);
	#generate a dict	
	def as_dict(self):
		item_dict = {};
		item_dict[str(USER_ID)] = str(self.individual_id);
		item_dict[str(USER_NAME)] = str(self.username);
		item_dict[str(FIRST_NAME)] = str(self.firstname);
		item_dict[str(LAST_NAME)] = str(self.lastname);
		item_dict[str(PHONE)] = str(self.phone);
		item_dict[str(EMAIL)] = str(self.email);
		return item_dict;
	class Meta:
		db_table = 'individuals';
class Event(models.Model):
	event_id = models.IntegerField(primary_key = True);
	event_title = models.CharField(max_length = 50);
	event_date = models.DateField();
	event_description = models.CharField(max_length = 1000);
	event_location = models.CharField(max_length = 100);
	url_media = models.CharField(max_length = 200);

	#generate a dict
	def as_dict(self):
		item_dict = {};
		item_dict[str(EVENT_ID)] = str(self.event_id); 
		item_dict[str(EVENT_TITLE)] = str(self.event_title);
		item_dict[str(EVENT_DESCRIPTION)] = str(self.event_description);
		item_dict[str(EVENT_LOCATION)] = str(self.event_location);
		item_dict[str(EVENT_DATE)] = str(self.event_date);
		item_dict[str(EVENT_URL_MEDIA)] = str(self.url_media);
		return item_dict;
	class Meta:
		db_table = 'events';

class Participant(models.Model):
	id = models.IntegerField(primary_key=True)
	event_id = models.IntegerField();
	individual_id = models.IntegerField();
	
	#generate a dict
	def as_dict(self):
		item_dict = {};
		item_dict[str(EVENT_ID)] = str(self.event_id); 
		item_dict[str(USER_ID)] = str(self.individual_id); 
		return item_dict;
	class Meta:
		db_table = 'individuals_at_event';

class Comment(models.Model):
	id = models.IntegerField(primary_key=True)
	event_id = models.IntegerField();
	individual_id = models.IntegerField();
	content = models.CharField(max_length = 400);
	date = models.DateField();
	def as_dict(self):
		item_dict = {};
		item_dict[str(EVENT_ID)] = str(self.event_id); 
		item_dict[str(USER_ID)] = str(self.individual_id);
		item_dict[str(COMMENT_CONTENT)] = str(self.content);
		item_dict[str(DATE_OF_COMMENT)] = str(self.date);
		return item_dict;
	class Meta:
		db_table = 'comment_of_events';
class Like(models.Model):
	id = models.IntegerField(primary_key=True)
	event_id = models.IntegerField();
	individual_id = models.IntegerField();
	def as_dict(self):
		item_dict = {};
		return item_dict;
	class Meta:
		#unique_together = (('event_id', 'individual_id'),)
		db_table = 'likes_of_event';
class Admin(models.Model):
	admin_id = models.IntegerField(primary_key = True);
	username = models.CharField(max_length = 50);
	password = models.CharField(max_length = 50);
	token = models.CharField(max_length = 50);
	class Meta:
		db_table = 'admin';
