#!/usr/bin/python3

# I really enjoyed making this file, this is slightly complex, and again, any feedback on efficiency or mistakes on my part is greatly encouraged!
# To walk through..
# currentTime is found with datetime python module, then an updateTime is set... more detail on this in a second.
# the database is connected to and all wanted values are queried using SELECT
# One of the values is "updated_at" which is a column in the sql database that gives a datetime.datetime variable for when the last change was made to a certain row (light)
# This datetime.datetime variable is is subtracted by the datetime.datetime. variable that is currentTime. If this difference is less than the updateTime, only that light is
# updated. This is to avoid sending update commands to every light and thus be more efficient. 

import mysql.connector
import re
import json
import requests
import datetime

# determine current time and update time
currentTime = datetime.datetime.now()

# updateTime is a datetime.timedelta variable because the difference between two datetime.datetime variables results in a datetime.timedelta difference
# here our "strictness" is 5 seconds
updateTime = datetime.timedelta(seconds = 5)

# query database
cnx = mysql.connector.connet(user='username', password = '***', database = 'teamBTG')
cursor = cnx.cursor()

objectQuery = ("SELECT IP, HOST_NAME, MODE, INTENSITY, CONNECTED, updated_at FROM lightObjects;")
cursor.execute(objectQuery)

lightObjects = []

# only send JSON POST requests for lights that have been updated in the past 'updateTime' seconds
for (IP, HOST_NAME, MODE, INTENSITY, CONNECTED, updated_at) in cursor:
    if CONNECTED == '1' and (currentTime-updated_at) < updateTime:
        # also, make lightObjects an array of dictionaries, this makes the conversion to JSON seemless
        lightObjects.append({'IP':IP, 'HOST':HOST_NAME, 'ON':MODE, 'INTENSITY':INTENSITY})
        
cursor.close()
cnx.close()

# helpful to check results - test by updating the database and waiting before or after 'updateTime' seconds to run the program to check to see if works
# I tested multiple times on several lights and had great success
for object in lightObjects:
    print(object)

# Send this data to the arduino WiFi chip: ESP8266
jsonObjects = json.dumps(lightObjects)

lightLength = len(lightObjects)
for h in range(0,(lightLength)):
    requestParam = "http://" + lightObjects[h].get('IP') + "/Python"
    print(requestParam)
    data = requests.post(requestParam, json = lightObjects[h])
    
    print("Status code: ", data.status_code)
    print "Printing Entire Post Request")
    print(data.json())
    
