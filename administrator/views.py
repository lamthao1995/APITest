from commonlib.manager.adminmanager import *
controller = Controller();
def event_display(request):
	return controller.display_event(request);
def insert_event_gui(request):
	return controller.insert_event_gui(request);
def insert_new_event_api(request):
	return controller.insert_new_event(request);
def index(request):
	return controller.index(request);

def admin_login(request):
	return controller.admin_login(request);
def admin_logout(request):
	return controller.admin_logout(request);
def admin_login_process(request):
	return controller.admin_login_process(request);
