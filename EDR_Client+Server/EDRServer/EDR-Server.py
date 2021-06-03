#!/usr/bin/python3

##This is the main file from EDR-Server.
##Only root can run the installation!
##The software always run with while loop.
##In "ReciveFromClient" function the code will listen for connection, after connection it will send it to "Logs" function.
##The "Logs" function sorts the logs and arranges them in the appropriate place.
##  If it get MiTM detect log it will write it in "MiTMDetect.log" file.
##  If it get HeartBeat from PC it will update this in "AlivePSc.log" file.
##  If it get BlackList detect from user, it will write it in "BlackListDetect.log" file.
##  The software also write every log in "EDR.log" file.
##All the logs files are in the "Logs" folder.
##The "AlivePCCheck" function check if the PCs send HeartBeat in the pass 2 minutes.
##  If the PC sent the code it will leave them in the AlivePCs.log file.
##  If the PC don`t sent the code it will remove the PC frome AlivePCs.log file and write it in the EDR.log file.

import socket, datetime, os

Port = 
	
def ReciveFromClient():
	try:
		s = socket.socket()
		s.settimeout(1)
		s.bind(('',Port))
		s.listen(5)
		conn, addr = s.accept()
		r = conn.recv(1024).decode('utf-8')
		c = addr[0]
		Logs(r, c)
		s.close()
	except:
		pass

def Logs(r, c):
	l = open('Logs/EDR.log', 'a')
	t = datetime.datetime.now().strftime("%Y/%m/%d | %H:%M:%S")

	if r == "M":
		#The software detect MiTM on PC.
		#The software write this on MiTMDetect.log and EDR.log files.
		m = open('Logs/MiTMDetect.log', 'a')
		m.write("%s - MiTM attack happend on %s\n" %(t, c))
		m.close()
		l.write("%s - [!] MiTM attack happend on %s\n" %(t, c))
		l.flush()

	elif r == "1":
		#The software detect HeartBeat from PC.
		#The software write this in EDR.log file and update this in AlivePSc.log file.
		l.write("%s - [+] Detect HeartBeat from %s\n" %(t, c))
		l.flush()
		f = open("Logs/AlivePCs.log", 'r')
		PCs = f.read().splitlines()
		f.close()
		f = open("Logs/AlivePCs.log", 'w')
		count = 0
		for PC in PCs:
			if PC.split('|')[0][:-1] == c:
				f.write("%s | %s\n" %(c, t))
				f.flush()
				count = count+1
			else:
				f.write("%s\n" %(PC))
				f.flush()
		if count == 0:
			f.write("%s | %s\n" %(c, t))
			f.flush()
		f.close()

	elif r.startswith('D') == True:
		#The software detect PC log in site from black list.
		#The software write this in EDR.log and BlackListDetect.log files.
		f = open("/var/www/html/EDR/WebsiteBlackList.txt", 'r')
		WBL = f.read().splitlines()
		f.close()
		for w in WBL:
			if w.split('=')[0][:-1] == r[1:]:
				web = w.split('=')[1][1:]
				break
		bl = open('Logs/BlackListDetect.log', 'a')
		bl.write("%s - %s log in site %s (%s) from black list\n" %(t, c, r[1:], web))
		bl.close()
		l.write("%s - [!] %s log in site %s (%s) from black list\n" %(t, c, r[1:], web))
		l.flush()
	
	l.close()

def AlivePCCheck():
	#Check if the PCs send HeartBeat in the pass 2 minutes.
	#If the PC sent HartBeat in the pass 2 minutes it will do the "ALIVE" function.
	#If the PC don`t sent HartBeat in the pass 2 minutes it will do the "NotALIVE" function.
	f = open("Logs/AlivePCs.log", 'r')
	pcs = f.read().splitlines()
	f.close()
	d = datetime.datetime.now()
	f = open("Logs/AlivePCs.log", 'w')
	f.close()
	t = datetime.datetime.now().strftime("%Y/%m/%d | %H:%M:%S")
	for pc in pcs:
		PCY = pc.split('|')[1][1:-1].split('/')[0]
		PCm = pc.split('|')[1][1:-1].split('/')[1]
		PCd = pc.split('|')[1][1:-1].split('/')[2]
		PCH = pc.split('|')[2][1:].split(':')[0]
		PCMin = pc.split('|')[2][1:].split(':')[1]
		if pc.split('|')[1][1:-1] == d.strftime("%Y/%m/%d"):
			if pc.split('|')[2][1:].split(':')[0] == d.strftime("%H"):
				if PCMin == d.strftime("%M") or int(PCMin) == int(d.strftime("%M"))-1 or int(PCMin) == int(d.strftime("%M"))-2:
					NotALIVE(pc)
				else:
					ALIVE(t, pc)
			elif int(pc.split('|')[2][1:].split(':')[0]) == int(d.strftime("%H"))-1:
				if int(PCMin) == int(d.strftime("%M"))+59 or int(PCMin) == int(d.strftime("%M"))+58:
					NotALIVE(pc)
				else:
					ALIVE(t, pc)
			else:
				ALIVE(t, pc)
		elif PCY == d.strftime("%Y") and PCm == d.strftime("%m") and int(PCd) == int(d.strftime("%d"))-1:
			if PCH == "23" and int(PCMin) == int(d.strftime("%M"))+59 or PCH == "23" and int(PCMin) == int(d.strftime("%M"))+58:
				NotALIVE(pc)
			else:
				ALIVE(t, pc)
		elif PCY == d.strftime("%Y") and int(PCm) == int(d.strftime("%m"))-1 and PCd == "01":
			if PCH == "23" and int(PCMin) == int(d.strftime("%M"))+59 or PCH == "23" and int(PCMin) == int(d.strftime("%M"))+58:
				NotALIVE(pc)
			else:
				ALIVE(t, pc)
		elif int(PCY) == int(d.strftime("%Y"))-1 and PCm == "01" and PCd == "01":
			if PCH == "23" and int(PCMin) == int(d.strftime("%M"))+59 or PCH == "23" and int(PCMin) == int(d.strftime("%M"))+58:
				NotALIVE(pc)
			else:
				ALIVE(t, pc)
		else:
			ALIVE(t, pc)

def ALIVE(t, pc):
	#If the PC sent HartBeat in the pass 2 minutes it will leave them in the AlivePCs.log file.
	l = open('Logs/EDR.log', 'a')
	l.write("%s - [-] %s are not alive\n" %(t, pc.split('|')[0][:-1]))
	l.close()

def NotALIVE(pc):
	#If the PC don`t sent HartBeat in the pass 2 minutes it will remove the PC frome AlivePCs.log file and write it in the EDR.log file.
	f = open("Logs/AlivePCs.log", 'a')
	f.write("%s\n" %(pc))
	f.close()

if not os.geteuid() == 0:
    print("Only root can run this software!")
    exit()

while True:
	ReciveFromClient()
	AlivePCCheck()
