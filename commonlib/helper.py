import hashlib
from constant import *
from datetime import datetime
import string
import random
import os
import platform
def hash_password(password): # password is a string
	hashF = hashlib.md5();
	hashF.update(str(password));
	return hashF.hexdigest();

def generate_token(password):
	time_now = datetime.now();
	hashF = hashlib.md5();
	hashF.update(str(password) + str(time_now));
	return hashF.hexdigest();

def item_json_format(item_list):
	item_dict = [];	
	print("on roi nhe: ", len(item_list));
	for item in item_list:
		item_dict.append(item.as_dict());
	return item_dict;

def write_error_into_log(exception):
	file_error = open("error.txt", 'a+');
	time_now = str(datetime.now());
	error_log = '{} : {}'.format(exception, time_now);
	file_error.write(error_log);
	file_error.close();

def handle_upload_file(uploaded_file, file_name):
	now = datetime.now();
	str_ = str(now.strftime("%Y-%m-%d"));
	img_dir = str(MEDIA_PATH) + str('/') + str_ + str('/');
	if not os.path.exists(img_dir):
		os.mkdir(img_dir);
	with open(img_dir + '/' + file_name, 'wb+') as destination:
		for chunk in uploaded_file.chunks():
			destination.write(chunk);
	return str_ + '/' + file_name;

def generate_file_name(filename):
	i = int(len(filename) - 1);
	ext = '';
	while i >= 0 and filename[i] != '.':
		ext = str(filename[i]) + ext;
		i = i - 1;
	str_ = str(filename) + str(datetime.now());	
	hashF = hashlib.md5();
	hashF.update(str(str_)); 
	return '{}.{}'.format(hashF.hexdigest(), ext);
def init_token(size=30, chars=string.ascii_uppercase + string.digits):
	    return ''.join(random.choice(chars) for _ in range(size))

def init_salt(size=30, chars=string.ascii_uppercase + string.digits):
	    return ''.join(random.choice(chars) for _ in range(size))
