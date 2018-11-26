#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 25 15:28:39 2018

@author: planetmaker
"""

import requests
import subprocess

import sys
import os.path

from time import sleep
import psutil    

def stellarium_running():
    for proc in psutil.process_iter():
        try:
            pinfo = proc.as_dict(attrs=['name'])
        except psutil.NoSuchProcess:
            pass
        else:
            if pinfo.get('name') == 'stellarium':
                return True

    return False


script_dir = os.path.dirname(os.path.realpath(__file__))
screenshot_dir = script_dir + '/screenshots'

if os.path.isdir(screenshot_dir) == False:
    try:
        os.mkdir(screenshot_dir)
    except OSError:
        print("Cannot create screenshot dir {}".format(screenshot_dir))
        exit

use_existing_stellarium = stellarium_running
if not use_existing_stellarium:
    proc_stellarium = subprocess.Popen(['stellarium','--screenshot-dir', screenshot_dir], stdout=subprocess.PIPE);
    sleep(10)

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

sleep(1)

url_screenshot = 'stelaction/do'
screenshot = requests.post(url_main + url_screenshot, data={'id':'actionSave_Screenshot_Global'})
print("Screenshot: ",screenshot)

url_planets = 'stelaction/do'
planet = requests.post(url_main + url_planets, data={'id':'actionShow_Planets'})
print("Show planets: ",planet)

if not use_existing_stellarium:
    proc_stellarium.kill()
