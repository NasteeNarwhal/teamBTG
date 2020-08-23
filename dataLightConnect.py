#!/usr/bin/python3

# Linux - Debian 8 - Python 3 - mySql - python-mysql-connector
# This file searches a network for ESP's and saves the results. It also modifies an existing database to show that those lights are connected
# in two cases: the lights had previously been connected OR the lights are new lights. 

import os
import mysql.connector
import re

# Set all connected values to '0' in database
cnx = mysql.connector.connect(user='username', password = '***', host='127.0.0.1', database='teamBTG')
cursor = cnx.cursor()
defConnect = ("UPDATE lightObjects "
      "SET CONNECTED = '0' "
      "WHERE CONNECTED != '0'")

# compare .lastrowid before and after execute to check if database was successfully updated
rowBef = cursor.lastrowid
cursor.execute(defConnect)
rowAft = cursor.lastrowid
if rowBef == rowAft:
    print("ERROR: EXECUTE FAIL\n")
    sys.exit(-1)

# always commit your changes in the database with .commit on your connection variable
cnx.commit()
cursor.close()
cnx.close()

# Now do a scan for ESPs IPs - this assumes that the SSIDs of the ESPs is standard. It would not be hard to modify this to pick up particular types of SSIDs
# However... If you do modify the SSIDs of your ESPs, this program will work best if they all have the same prefix. The standard for ESP8266s is 'ESP-', so that is
# what is searched for in the grep portion of the command.
# The following command is based on using a linux-debian OS.
IPScan = os.system("sudo nmap -Pn -p 80 --max-parallelism=5 -oG ipscan.txt 10.3.141.0/24 | grep -i 'ESP-' > ipScanClean.txt")

# Put each scanned chip into a string
ESPs = []
with open ('ipScanClean.txt', 'rt') as ESPFile:
    for ESP in ESPFile:
        ESPs.append(ESP)
# optional print to test if worked
print(ESPs)

# helpful to determine the length of the ESPs array
ipLines = len(ESPs)

# The nmap command above gives the hostname and IP address of each chip, the following split commands just isolate those out of the ESPs string into two more
# arrays: IPs and hostNames
IPs = []
hostNames = []
for h in range(0, ipLines):
    hostNames.append(ESPs[h].split('for ')[1].split(' (')[0])
    IPs.append(ESPs[h].split('(')[1].split(')'[0])
    
# helpful to check to see if worked properly
print(IPs)
print(hostNames)

# Now insert the hostnames and IP addresses of connected ESPs into the database
for h in range(0, ipLines):
    cnx = mysql.connector.connect(user='username', password = '***', host='127.0.0.1', database='teamBTG')
    cursor = cnx.cursor()
    
    addLight = ("INSERT INTO lightObjects"
                "(HOST_NAME, IP, CONNECTED)"
                "VALUES (%s, %s, '1')"
                "ON DUPLICATE KEY UPDATE CONNECTED = '1'")
                
    dataLight = (hostNames[h], IPs[h])

    # commit data to database: teamBTG
    rowBef = cursor.lastrowid
    cursor.execute(addLight, dataLight)
    rowAft = cursor.lastrowid
    if rowBef == rowAft:
       print("ERROR: EXECUTE FAIL\n")
       sys.exit(-1)
   
    cnx.commit()
    
