#!/usr/bin/python3
#    Copyright (C) 2018 I Sagar
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301 US

import requests
from websocket import create_connection,WebSocket
import ssl
import sys
import os

requests.packages.urllib3.disable_warnings()

def get_token_value(url,username,password):
	r = requests.get(url,auth=(username,password),verify=False)
	token_value = r.cookies['jwt']
	return token_value

#To enable trace add below line
#websocket.enableTrace(True)

def get_doc_info(socket_url,token_value):
	data = {}
	ws = create_connection(socket_url,sslopt={"cert_reqs": ssl.CERT_NONE})
	"""Authenticating with Server  """
	ws.send('auth '+'jwt='+token_value)
	"""Now fethcing information """
	word = ['active_users_count', 'active_docs_count', 'mem_consumed', 'sent_bytes', 'recv_bytes']
	for i in word:
		ws.send(i)
		result = ws.recv()
		result = result.split()
		data[result[0]] = result[1]
	ws.close()
	return data

if __name__ == '__main__':
	url = "https://"+sys.argv[2]+"/loleaflet/dist/admin/admin.html"
	username = sys.argv[3]
	password = sys.argv[4]
	token_value = get_token_value(url,username,password)
	socket_url = "wss://"+sys.argv[2]+"/lool/adminws"
	data = get_doc_info(socket_url,token_value)
	#Remove old file
	os.system('rm -f lool_data.txt')
	for key,value in data.items() :
		with open('lool_data.txt','a') as file:
			file.write("%s %s %s\n" % (sys.argv[1], "lool."+key , value))
