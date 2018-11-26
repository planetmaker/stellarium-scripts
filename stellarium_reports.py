#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 25 15:28:39 2018

@author: planetmaker
"""

import requests
import subprocess
import os.path

from time import sleep

def start_stellarium(url, screenshot_dir):
    """ Ensure that there is a running and functional stellarium instance
    
    Test for a working instance and start our own, if we find no instance
    to communicate with
    @url: top level API url of stellarium
    @screenshot_dir: desired screenshot dir. Needed when we start stellarium
                     ourselves
    """
    proc_stellarium = None
    # We try to get info from stellarium. This is more reliable than testing
    # for PID as the process may be already zombified
    try:
        requests.get(url + "main/status")
    except:
        proc_stellarium = subprocess.Popen(['stellarium','--screenshot-dir', screenshot_dir], stdout=subprocess.PIPE);
        sleep(5)
    else:
        print("Found running stellarium. We are using it.")
        
    return proc_stellarium

def make_screenshot_dir():
    """ Create a screenshot dir as sub-dir of current directory
    
    We assume that we don't want the screenshot in Stellarium's default dir,
    thus we create our own for this session where we store our images.
    """
    script_dir = os.path.dirname(os.path.realpath(__file__))
    screenshot_dir = script_dir + '/screenshots'
    
    if os.path.isdir(screenshot_dir) == False:
        try:
            os.mkdir(screenshot_dir)
        except OSError:
            print("Cannot create screenshot dir {}".format(screenshot_dir))
            exit
            
    return screenshot_dir



url_main = "http://localhost:8090/api/"

screenshot_dir = make_screenshot_dir()
proc_stellarium = start_stellarium(url_main, screenshot_dir)

url_status = "main/status"
url_actionlist = "stelaction/list"
url_properties = "stelproperty/list"
response = requests.get(url_main + url_status)
print("Status: ",response.status_code)
actions = requests.get(url_main + url_actionlist)
print("Actions: ",actions.status_code)
properties = requests.get(url_main + url_properties)
print("Properties: ",properties.status_code)

#print(response.json())
#print(actions.json())
#print(properties.json())

#if response.status_code == 200:
#    print("Time: ", response.json().get('time'))
#    print("Location: ", response.json().get('location'))
#    print("View: ", response.json().get('view'))
#

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

#if actions.status_code == 200:
#    print(actions.json())

sleep(1)

url_screenshot = 'stelaction/do'
screenshot = requests.post(url_main + url_screenshot, data={'id':'actionSave_Screenshot_Global'})
print("Screenshot: ",screenshot)

url_planets = 'stelaction/do'
planet = requests.post(url_main + url_planets, data={'id':'actionShow_Planets'})
print("Show planets: ",planet)

if proc_stellarium is not None:
    print("We started it, so we are closing down stellarium now")
    proc_stellarium.kill()
