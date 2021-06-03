#!/usr/bin/python3

##In here you can edit the "WebsiteBlackList.txt" file for the EDR.
##Only root can run the installation!
##The script will copy the file to the current directory.
##After this it will ask you what you want to do, view the file/ add URLs to the file or delete URLs from the file.
##In the end the script after you done to edit the file the script will replace ht original file in his folder with the new file.

import shutil, os

shutil.copyfile('/var/www/html/EDR/WebsiteBlackList.txt', './WebsiteBlackList.txt')

def Main():
	print("What you want to do with the Website Black List?")
	print("1 = See The Black List.")
	print("2 = Edit The Black List.")
	print("0 = Exit.")
	
	print("\nInput only the number of your choice!")
	c = input("Your choose is: ")
	
	print("-------------------------------------------------------")
	
	if c == "1":
		SeeWBL()

	elif c == "2":
		EditWBL()

	elif c == "0":
		print("Bye Bye...")
		Done()

	else:
		print("Wrong Answer!")
		print("-------------------------------------------------------")
		Main()

def SeeWBL():
	f = open("WebsiteBlackList.txt", 'r')
	WBL = f.read().splitlines()
	f.close()
	for l in WBL:
		print(l)
	print("-------------------------------------------------------")
	Main()

def EditWBL():
	print("What you want to do?")
	print("1 = Add website to the Black List.")
	print("2 = Delete website from the Black List.")
	print("0 = Back to main manu") 

	print("\nInput only the number of your choice!")
	c = input("Your choose is: ")
	
	print("-------------------------------------------------------")
		
	if c == "1":
		AddWBL()

	elif c == "2":
		DelWBL()

	elif c == "0":
		Main()

	else:
		print("Wrong Answer!")
		EditWBL()

def AddWBL():
	print("Enter the website url you want to enter in to black list:")
	web = input()
	
	f = open("WebsiteBlackList.txt", 'r')
	WBL = f.read().splitlines()
	f.close()
	
	num = "0"
	
	for l in WBL:
		num = l.split('=')[0][:-1]
	num = str(int(num)+1)
	WBL = open("WebsiteBlackList.txt", 'a')
	WBL.write("%s = %s\n" %(num, web))
	WBL.close()
	
	print("-------------------------------------------------------")

	EditWBL()

def DelWBL():
	web = input("Enter the website url number you want to delete from black list:")
	num = "1"
	f = open("WebsiteBlackList.txt", 'r')
	WBL = f.read().splitlines()
	f.close()
	
	wbl = open("WebsiteBlackList.txt", 'w')
	for l in WBL:
		if l.split('=')[0][:-1] is not web:
			wbl.write("%s = %s\n" %(num, l.split('=')[1][1:]))
			wbl.flush()
			num = str(int(num)+1)
		else:
			print("You sure you want to delete %s from black list?" %(l.split('=')[1][1:]))
			print("1 = Yes")
			print("2 = No")
			
			print("\nInput only the number of your choice!")
			c = input("Your choose is: ")
			
			if c == "1":
				pass
			elif c == "2":
				wbl.write("%s = %s\n" %(num, l.split('=')[1][1:]))
				wbl.flush()
				num = str(int(num)+1)
			else:
				print("Wrong Answer!")
				print("We are not delete %s from black list" %(l.split('=')[1][1:]))
				wbl.write("%s = %s\n" %(num, l.split('=')[1][1:]))
				wbl.flush()
				num = str(int(num)+1)
	wbl.close()
	
	print("-------------------------------------------------------")
	
	EditWBL()

def Done():
	os.remove("/var/www/html/EDR/WebsiteBlackList.txt")
	shutil.move("WebsiteBlackList.txt", "/var/www/html/EDR/WebsiteBlackList.txt")

if not os.geteuid() == 0:
    print("Only root can run this script!")
    exit()

Main()
