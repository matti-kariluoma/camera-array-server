#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A RESTful service that 
* multiple cameras announce themselves to
* a user (or software on the user's behalf) connects to 
in order to control the camera array.

:copyright: 2013 Matti Kariluoma <matti@kariluo.ma>
"""
from __future__ import unicode_literals, print_function

__author__ = 'Matti Kariluoma'
__version__ = '0.1.0'

from bottle import redirect, request, response, route, static_file
from bottle import HTTPResponse # for returning custom HTTP codes
from bottle import template, TEMPLATE_PATH, view
from bottle import run

TEMPLATE_PATH.append('templates')

SITE_URL = '' # referenced by the base template
cameras = {} # server state

'''
'@' is the python function decorator.

@wrapper 
def func(): 
	pass

Is equivalent to:

def func():
	pass
func = wrapper(func)
'''
@route('/')
@view('index')
def home():
	return {
			'links': [
					('List Cameras', '/cameras/')
				]
		}

class Camera:
	def __init__(self):
		pass
		
	def __unicode__(self):
		return u'Camera Info'
		
	def __str__(self):
		return str(unicode(self))

@route('/cameras/', method='GET')
@view('camera_list')
def list_cameras():
	return {
			'registered_cameras': cameras.keys()
		}

@route('/cameras/', method='POST')
def register_new_camera():
	camera_id = request.forms.camera_id
	if camera_id not in cameras:
		cameras[camera_id] = Camera()
		raise HTTPResponse(
			body=list_cameras(),
			status='201 Created',
			header={
					'Location': '/cameras/%s/' % camera_id
				}
		)
	else:
		raise HTTPResponse(
				body=template('error', status='400 Camera Already Exists'), 
				status='400 Camera Already Exists'
			)

@route('/cameras/:camera_id/', method='GET')
@view('control_cameras')
def show_camera(camera_id=None):
	if not camera_id or camera_id not in cameras:
		raise HTTPResponse(
				body=template('error', status='404 Camera not Found'),
				status='404 Camera not Found'
			)
	return {
			'camera_id': camera_id,
			'cameras': [cameras[camera_id]]
		}

@route('/cameras/:camera_id/', method='DELETE')
def deregister_camera(camera_id=None):
	if camera_id in cameras:
		del cameras[camera_id]
	else:
		raise HTTPResponse(
				body=template('error', status='404 Camera not Found'),
				status='404 Camera not Found'
			)
	return '<p>Camera Deleted.</p><a href="/">Home</a>'
	
@route('/cameras/:camera_id/settings/', method='GET')
def show_settings(camera_id=None):
	return {}
	
@route('/cameras/:camera_id/settings/', method='PUT')
def set_settings(camera_id=None):
	return {}	
	
@route('/cameras/:camera_id/capture/')
def camera_capture(camera_id=None):
	return {}
	
@route('/cameras/:camera_id/record/')
def camera_start_record(camera_id=None):
	return {}
	
@route('/cameras/:camera_id/preview/')
def show_camera_preview(camera_id=None):
	return {}
	
@route('/cameras/:camera_id/:date/')
def list_saved_image_video(camera_id=None, date=None):
	return {}
	
@route('/cameras/all/')
def show_all_cameras():
	return {
			'cameras': cameras.values()
		}
	
@route('/static/:path#.+#', name='static')
def static(path):
    return static_file(path, root='static')

def main():
	import sys
	if len(sys.argv) == 1:
		run(host='localhost', port=8080, reloader=True)
	elif len(sys.argv) > 2:
		run(host=sys.argv[1], port=int(sys.argv[2]), reloader=True)
	else:
		print("usage: %s hostname port" % (sys.argv[0]))
	
if __name__ == '__main__': main()
