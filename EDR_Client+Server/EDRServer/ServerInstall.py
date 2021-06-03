#!/usr/bin/python3

##This is the installation of EDR-Server.
##Only root can run the installation!
##This will installing apache2, create "EDR" folder in apache2 folder and create the "WebsiteBlackList.txt".
##After this it will "Log" folder in the "EDR-Server" and create inside 4 files (EDR.log, AlivePCs.log, MiTMDetect.log, BlackListDetect.log).
##After this it will write in crontab script for the software to run automatically after a restart.
##After this it will open "ChangeWebsiteBlackList.py" so you can edit the "WebsiteBlackList.txt" file.
##At the end of the installation you will be notified that the installation is complete and now you can either run the EDR-Server software or restart the operating system so that the software runs automatically.

import os, subprocess

if not os.geteuid() == 0:
    print("Only root can run this script!")
    exit()

print("Installing your EDR Server...")
os.system('apt update && apt install apache2 -y')

try:
	os.mkdir('/var/www/html/EDR/')
except:
	pass

WBL = open('/var/www/html/EDR/WebsiteBlackList.txt', 'a')
WBL.close()

try:
	os.mkdir('Logs')
except:
	pass

l1 = open('Logs/EDR.log', 'a')
l1.close()
l2 = open('Logs/AlivePCs.log', 'a')
l2.close()
l3 = open('Logs/MiTMDetect.log', 'a')
l3.close()
l4 = open('Logs/BlackListDetect.log', 'a')
l4.close()

os.system('if [ -z "$(crontab -l | grep "@reboot $(pwd)/EDR-Server.py")" ]; then (crontab -l ; echo "@reboot $(pwd)/EDR-Server.py")| crontab -; fi')
os.system('python3 ChangeWebsiteBlackList.py')

print('Installation Complete. :-)')
print('You can now run EDR-Server.py software or restart your OS to have the software run automatically in the background.')
