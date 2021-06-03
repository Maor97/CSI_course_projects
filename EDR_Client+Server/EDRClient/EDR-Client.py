#!/usr/bin/python3

from scapy.all import *
import subprocess, platform, socket, requests, threading, os

OS = platform.system()
PORT = 
SrvIP = ''

def MiTMCheck():
	threading.Timer(60.0, MiTMCheck).start()
	lst = []
	dct = {}
	arp=subprocess.check_output("arp -a",shell=True)

	if OS == 'Windows':		
		for Mac in arp.decode('utf-8').splitlines():
			if 'dynamic' in Mac:
				lst.append(Mac[24:41])

	if OS == 'Linux':
		for Mac in arp.decode('utf-8').splitlines():
			lst.append(Mac.split(')')[1][4:21])

	for m in lst:
		if m in dct:
			dct[m] = dct[m]+1
		else:
			dct[m] = 1

	for r in dct.values():
		if r > 1:
			SendToServer("M")

def HeartBeat():
	threading.Timer(30.0, HeartBeat).start()
	SendToServer("1")

def SiteChecker(p):
	if p.haslayer(DNS):
		if p.summary()[28:-2].startswith('b') == True:
			Site = p.summary()[30:-4]
		else:
			Site = p.summary()[28:-2]
		try:
			file = open("WebsiteBlackList.txt", 'r')
			Deny = file.read().splitlines()
			file.close()
			for D in Deny:
				if Site in D.split('=')[1][1:]:
					SendToServer("D%s" %(D.split('=')[0][:-1]))
		except:
			pass

def HashCheck():
	threading.Timer(3600.0, HashCheck).start()
	url = 'http://10.0.3.23/EDR/WebsiteBlackList.txt'
	if os.path.exists('WebsiteBlackList.txt') == True:
		with open('WebsiteBlackList.txt', 'rb') as fh:
			m = hashlib.md5()
			while True:
				data = fh.read(8192)
				if not data:
					break
				m.update(data)
			h1 = m.hexdigest()

		m = hashlib.md5()
		r = requests.get(url)
		for data in r.iter_content(8192):
			m.update(data)
		h2 = m.hexdigest()

		if h1 != h2:
			os.remove("WebsiteBlackList.txt")
			r = requests.get(url, allow_redirects=True)
			open('WebsiteBlackList.txt', 'wb').write(r.content)
	else:
		r = requests.get(url, allow_redirects=True)
		open('WebsiteBlackList.txt', 'wb').write(r.content)

def SendToServer(text):
	try:
		s = socket.socket()
		s.connect((SrvIP, PORT))
		s.send(text.encode('utf-8'))
		s.close()
	except:
		pass

if OS == 'Linux':
	if not os.geteuid() == 0:
		print("Only root can run this software!")
		exit()
        
MiTMCheck()
HeartBeat()
HashCheck()
sniff(prn=SiteChecker)
