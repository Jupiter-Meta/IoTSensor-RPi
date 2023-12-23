#!/usr/bin/python

import pymysql,sys,subprocess,mqttservice
from subprocess import check_output

#get IP addresses
ip_scanoutput=check_output(["hostname -I"],shell=1)
ip_eth0=ip_scanoutput.decode().split()[0]
ip_wlan0=ip_scanoutput.decode().split()[1]

temp=subprocess.check_output(["vcgencmd","measure_temp"])
temp=temp.decode()
temp=temp.replace("temp=","")
temp=temp.replace("'C\n","")

#get node ID
id_scanoutput=check_output(["hostname"],shell=1)
id_node=id_scanoutput.decode().split()[0]

if len(id_node)>9:
	nodeId=int(id_node[-2:])
else:
	nodeId=int(id_node[-1:])

#Obtain Signal strength of RPi WLan and WLan SSID
#signal=subprocess.check_output(["iwconfig", "wlan0", "|" "grep "Signal""])
try:
	ssid=subprocess.check_output(["iwgetid","-r"])
	ssid=ssid.decode()
	ss=subprocess.check_output(["iwconfig", "wlan0"])
	ss=ss.decode()
	ss=ss.split()[29] 
	ss=ss.replace("level=","")
except:
	try:
		ssid=subprocess.check_output(["iwgetid","-r"])
		ssid=ssid.decode()
		ss=subprocess.check_output(["iwconfig", "wlan1"])
		ss=ss.decode()
		ss=ss.split()[29] 
		ss=ss.replace("level=","")
	except:
		ssid="not connected"
		ss=0
		pass

print(ssid,ss)
	
#Store to DB
dataHealth={'nodeid':nodeId,'alive':1,'temp':temp,'ssid':ssid,'ss':ss}
print(dataHealth)
#conn =pymysql.connect(database="AmritaSGM",user="admin",password="admin",host="localhost")
#cur=conn.cursor()
#cur.execute("INSERT INTO nodeHealth(nodeid,alive,temp,SSID,wlan_ss) VALUES(%(nodeid)s,%(alive)s,%(temp)s,%(ssid)s,%(ss)s);",dataHealth)
#conn.commit()
#conn.close()
print ("DB Dump success")

#MQTT to server
#mqttservice.mqtt_publish("192.168.112.110",1883,"node_alive_direct",dataHealth,ip_wlan0)
