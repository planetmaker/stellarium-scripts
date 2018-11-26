#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 25 15:28:39 2018

@author: planetmaker
"""

import requests
from time import sleep

url_main = "http://localhost:8090/api/"

url_status = "main/status"

response = requests.get(url_main + url_status)
print("Status: ",response.status_code)
if response.status_code == 200:
    print("Time: ", response.json().get('time'))
    print("Location: ", response.json().get('location'))
    print("View: ", response.json().get('view'))


#jd_next = response.json().get('time').get('jday') + 60
#url_time = "main/time"
#param_main = {'time':str(jd_next)}
#answer = requests.post(url_main+url_time, data=param_main)
#print("Set time: ",answer.status_code)

#sleep(1)

param_fov = {'fov':'190'}
url_fov = "main/fov"
fov = requests.post(url_main+url_fov, data=param_fov)
print("FOV: ",fov)
param_view = {'altAz':'[0.0001,0,1]'}
url_view = "main/view"
view = requests.post(url_main+url_view, data=param_view)
print("View: ",view)
#if answer.status_code == 200:
#    print(answer.json())
#else:
#    print("Post request did not succeed")
#
#url_actions = "stelaction/list"
#actions = requests.get(url_main + url_actions)
#print(actions.status_code)
#if actions.status_code == 200:
#    print(actions.json())

#url_screenshot = 'stelaction/do'
#screenshot = requests.get(url_main + url_screenshot, json={'id':'actionSave_Screenshot_Global'})
#print(screenshot.status_code)

url_planets = 'stelaction/do'
planet = requests.post(url_main + url_planets, data={'id':'actionShow_Planets'})
print("Show planets: ",planet)
