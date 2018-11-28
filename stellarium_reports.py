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
        sleep(10)
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

def setup_viewport(properties):
    param_fov = {'fov':'190'}
    url_fov = "main/fov"
    fov = requests.post(url_main+url_fov, data=param_fov)
    print("FOV: ",fov)
    param_view = {'altAz':'[0.0001,0,1]'}
    url_view = "main/view"
    view = requests.post(url_main+url_view, data=param_view)
    print("View: ",view)
    
    settings = [
        {'url':'stelproperty/set', 'id':'actionShow_Nebulas', 'value':False},
        {'url':'stelproperty/set', 'id':'SolarSystem.planetsDisplayed', 'value': False},
        {'url':'stelproperty/set', 'id':'actionShow_MeteorShowers', 'value': False},
        {'url':'stelproperty/set', 'id':'actionShow_Planets', 'value': False},
        {'url':'stelproperty/set', 'id':'actionShow_DSO_Textures', 'value': False},
        ]
    for item in settings:
        answer = requests.post(url_main + item.get('url'), data={'id':item.get('id'), 'value':item.get('value')})
        print("{}: {}".format(item.get('id'),answer.text))

def make_screenshot():
    """ Create a screenshot of the given name)
    """
    url_screenshot = 'stelaction/do'
    screenshot = requests.post(url_main + url_screenshot, data={'id':'actionSave_Screenshot_Global'})
    print("Screenshot: ",screenshot)


url_main = "http://localhost:8090/api/"
screenshot_dir = ""

def main(url_main):
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
    
    #jd_next = response.json().get('time').get('jday') + 60
    #url_time = "main/time"
    #param_main = {'time':str(jd_next)}
    #answer = requests.post(url_main+url_time, data=param_main)
    #print("Set time: ",answer.status_code)
    
    setup_viewport(properties.json())
    # Sleep so that the commands have been executed
    sleep(5)
    
    make_screenshot()
    
    if proc_stellarium is not None:
        print("We started it, so we are closing down stellarium now")
        proc_stellarium.kill()

if __name__ == "__main__":
    main(url_main)