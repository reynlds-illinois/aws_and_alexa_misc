#!/usr/bin/env python

# configure python virtual environment...comment this out if you don't use it
import os
virtual_env_file = '/services/ic-tools/python-virtualenv/bin/activate_this.py'
execfile(virtual_env_file, dict(__file__=virtual_env_file))

# imports and variables
import pycurl, sys, time, smtplib, pprint, mimetypes
from selenium import webdriver
RESULTS = {}
TOKEN = "XXXXXXXXXXXXXXXXXXXXXXX"             # < change this
MYSERVER = "XXXXXXXXXXXXXXXXXXXXXXXXXXX"      # < change this
HOST = "status.blackboard.com"
bb_status_url = "http://status.blackboard.com"
TODAY = time.strftime("%Y-%m-%d")
NOW = time.strftime("%H:%M:%S")
DATESTAMP = TODAY+"_"+NOW

# configure web driver and timeouts
driver = webdriver.PhantomJS("/services/ic-tools/bin/phantomjs/bin/phantomjs")      # < change this path
driver.set_window_size(1120,550)
driver.implicitly_wait(5)
driver.set_page_load_timeout(30)

# open a working browser "driver"
driver.get(bb_status_url)

# Check Collaborate (NA) status
#collab_status = driver.find_element_by_xpath('//*[@id="blackboard-collaborate---web-conferencing-us-hosted"]/td[@class="status highlight"]/a/img[@class="sym"]').get_attribute("alt")
collab_status = driver.find_element_by_xpath('//*[@id="blackboard-collaborate---web-conferencing-us-hosted"]/td[@class="active"]/a/img[@class="status"]').get_attribute("alt")
RESULTS.update({"collaborate":collab_status})

# Check Managed Hosting status
#bbmh_status = driver.find_element_by_xpath('//*[@id="blackboard-learn-data-centers"]/td[@class="status highlight"]/a/img[@class="sym"]').get_attribute("alt")
bbmh_status = driver.find_element_by_xpath('//*[@id="blackboard-learn-data-centers"]/td[@class="active"]/a/img[@class="status"]').get_attribute("alt")
RESULTS.update({"managed-hosting":bbmh_status})

# Check SafeAssign status
#sa_status = driver.find_element_by_xpath('//*[@id="safeassign"]/td[@class="status highlight"]/a/img[@class="sym"]').get_attribute("alt")
sa_status = driver.find_element_by_xpath('//*[@id="safeassign"]/td[@class="active"]/a/img[@class="status"]').get_attribute("alt")
RESULTS.update({"safeassign":sa_status})

# Update Nagios with results of checks
for KEY, VALUE in RESULTS.iteritems():
    if (VALUE == "Up" or VALUE == "Info"):
        STATE = "0"
        COMMENT = "Service_is_Normal_"+DATESTAMP
    elif (VALUE == "Intermittent Problems"):
        STATE = "1"
        COMMENT = "Service_is_Degraded_"+DATESTAMP
    elif (VALUE == "Down"):
        STATE = "2"
        COMMENT = ">>>_SERVICE_IS_DOWN_<<<_"+DATESTAMP
    else:
        STATE = "3"
        COMMENT = "Service_state_is_Unknown_"+DATESTAMP
    CMD_URL = str("https://"+MYSERVER+"/nrdp/?cmd=submitcmd&token="+TOKEN+"&command=PROCESS_SERVICE_CHECK_RESULT%3B"+HOST+"%3B"+KEY+"%3B"+STATE+"%3B"+COMMENT+"%5Cn&btnSubmit=Submit+Command")

    bburl = pycurl.Curl()
    bburl.setopt(bburl.URL, CMD_URL)
    bburl.perform()

# Close connections
driver.close()
os.system('pkill phantomjs')
sys.exit()
