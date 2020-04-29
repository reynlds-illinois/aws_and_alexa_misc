s3 = boto3.resource('s3')
S3BUCKET = "bb-status-bucket"

for subdir, dirs, FILES in os.walk("/tmp/bb-status/"):
    for F in FILES:
        if F.endswith(".txt"):
            FPATH = os.path.join(subdir, F)
            print(FPATH + " === " + F)
#            f = open(full_path, "rb")
#            conn.upload(full_path, f, "bb-status-bucket")
            S3.Bucket(S3BUCKET).upload_file(FPATH,F)
            

import requests, lxml, os, sys, tinys3, boto3
from lxml import html
from lxml import etree

PAGE = requests.get("http://status.blackboard.com")
TREE = html.fromstring(PAGE.content)

S3KEY = "XXXXXXXXXX"
S3SECRET = "XXXXXXXXXX"

SVC_UP = 0
SVC_REV = 0
SVC_DOWN = 0
SVC_INFO = 0

if not os.path.exists("/tmp/bb-status"):
    os.makedirs("/tmp/bb-status")
FILE_UP = open("/tmp/bb-status/bb-status_up.txt", "a+")
FILE_UP.truncate()
FILE_DOWN = open("/tmp/bb-status/bb-status_down.txt", "a+")
FILE_DOWN.truncate()
FILE_REV = open("/tmp/bb-status/bb-status_rev.txt", "a+")
FILE_REV.truncate()
FILE_INFO = open("/tmp/bb-status/bb-status_info.txt", "a+")
FILE_INFO.truncate()
FILE_SUM = open("/tmp/bb-status/bb-status_sum.txt", "a+")
FILE_SUM.truncate()

RESULT_UP = {}
RESULT_DOWN = {}
RESULT_REV = {}
RESULT_INFO = {}

SERVICES = {"Ally":"//div[@id='content']/table[@id='services']/tbody/tr[@id='ally']/td[@class='status highlight']/a/img[@class='sym']/@src", "Managed Hosting Analytics":"//div[@id='content']/table[@id='services']/tbody/tr[@id='analytics---managed-hosting']/td[@class='status highlight']/a/img[@class='sym']/@src", "Behind The Blackboard":"//div[@id='content']/table[@id='services']/tbody/tr[@id='behind-the-blackboard']/td[@class='status highlight']/a/img[@class='sym']/@src", "Collaborate I.M.":"//div[@id='content']/table[@id='services']/tbody/tr[@id='blackboard-collaborate---blackboard-im']/td[@class='status highlight']/a/img[@class='sym']/@src", "Collaborate U.S.":"//div[@id='content']/table[@id='services']/tbody/tr[@id='blackboard-collaborate---web-conferencing-us-hosted']/td[@class='status highlight']/a/img[@class='sym']/@src", "Developer Portal":"//div[@id='content']/table[@id='services']/tbody/tr[@id='developer-portal---developer-blackboard-com']/td[@class='status highlight']/a/img[@class='sym']/@src", "Learn - Blackboard Open Content":"//div[@id='content']/table[@id='services']/tbody/tr[@id='xplor']/td[@class='status highlight']/a/img[@class='sym']/@src", "Learn - Cloud and Social Tools":"//div[@id='content']/table[@id='services']/tbody/tr[@id='cloud--social-tools']/td[@class='status highlight']/a/img[@class='sym']/@src", "Learn - New Box View":"//div[@id='content']/table[@id='services']/tbody/tr[@id='inline-grading-crocodoc']/td[@class='status highlight']/a/img[@class='sym']/@src", "Learn - Managed Hosting U.S.":"//div[@id='content']/table[@id='services']/tbody/tr[@id='blackboard-learn-data-centers']/td[@class='status highlight']/a/img[@class='sym']/@src", "Learn - Mobile Services":"//div[@id='content']/table[@id='services']/tbody/tr[@id='learn---mobile-services']/td[@class='status highlight']/a/img[@class='sym']/@src", "Learn - Open Education":"//div[@id='content']/table[@id='services']/tbody/tr[@id='open-education-platform']/td[@class='status highlight']/a/img[@class='sym']/@src", "Learn - Partner Cloud":"//div[@id='content']/table[@id='services']/tbody/tr[@id='partner-cloud']/td[@class='status highlight']/a/img[@class='sym']/@src", "Learn - S.I.S Central":"//div[@id='content']/table[@id='services']/tbody/tr[@id='learn---sis-central']/td[@class='status highlight']/a/img[@class='sym']/@src", "Learn - SaaS U.S.":"//div[@id='content']/table[@id='services']/tbody/tr[@id='saas-deployment-for-blackboard-learn']/td[@class='status highlight']/a/img[@class='sym']/@src", "Moodlerooms U.S.":"//div[@id='content']/table[@id='services']/tbody/tr[@id='moodlerooms']/td[@class='status highlight']/a/img[@class='sym']/@src", "Moodlerooms Enterprise":"//div[@id='content']/table[@id='services']/tbody/tr[@id='enterprise-moodle']/td[@class='status highlight']/a/img[@class='sym']/@src", "SafeAssign":"//div[@id='content']/table[@id='services']/tbody/tr[@id='safeassign']/td[@class='status highlight']/a/img[@class='sym']/@src"}

TOTAL_SVCS = len(SERVICES)

for KEY,VALUE in SERVICES.items():
    TEMPVAL = TREE.xpath(VALUE)
    if TEMPVAL[0] == "/images/icons/fugue/tick-circle.png":
        RESULT = "is UP"
        SVC_UP += 1
        RESULT_UP[KEY] = RESULT
        FILE_UP.write(KEY + " " + RESULT + "\n")
    elif TEMPVAL[0] == "/images/icons/fugue/traffic-cone.png":
        RESULT = "should be reviewed for recent maintenance."
        SVC_REV += 1
        RESULT_REV[KEY] = RESULT
        FILE_REV.write(KEY + " " + RESULT + "\n")
    elif TEMPVAL[0] == "/images/icons/fugue/x_alt.png":
        RESULT = "is currently unavailable."
        SVC_DOWN += 1
        RESULT_DOWN[KEY] = RESULT
        FILE_DOWN.write(KEY + " " + RESULT + "\n")
    elif TEMPVAL[0] == "/images/icons/fugue/exclamation.png":
        RESULT = "is experiencing intermittent problems."
        SVC_DOWN += 1
        RESULT_DOWN[KEY] = RESULT
        FILE_DOWN.write(KEY + " " + RESULT + "\n")
    else:
        RESULT = "has extra information available."
        SVC_INFO += 1
        RESULT_INFO[KEY] = RESULT
        FILE_INFO.write(KEY + " " + RESULT + "\n")
    TEMP = str("/tmp/bb-status/" + KEY + ".txt")
    FILE = open(TEMP, "w+")
    TEMPF = str(KEY + " " + RESULT + "\n")
    FILE.write(TEMPF)
    FILE.close()
    print(KEY, RESULT)

print()

print("There are", TOTAL_SVCS, "services being checked for status. Of these:")

if TOTAL_SVCS == SVC_UP:
        print("ALL Blackboard Services are fully available.")
        FILE_SUM.write("All Blackboard Services are fully available." + "\n")

else:
        print(SVC_UP, "are fully available.")
        FILE_SUM.write(str(SVC_UP) + " are fully available." + "\n")
        print(SVC_DOWN, "are in a substantially degraded state.")
        FILE_SUM.write(str(SVC_DOWN) + " are in a substantially degraded state." + "\n")
        print(SVC_REV, "should be reviewed for recent maintenance.")
        FILE_SUM.write(str(SVC_REV) + " should be reviewed for recent maintenance." + "\n")
        print(SVC_INFO, "should be reviewed for extra information.")
        FILE_SUM.write(str(SVC_INFO) + " should be reviewed for extra information." + "\n")
