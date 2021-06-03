#!/usr/bin/python3


##This code is a web spider, you need to give him a link with '-U' or '--URL'.
##He can also do this with tor network (-T, --Tor).
##At the default it get the link just from the website you give.
##If you want to scan also sublinks you need to type how many do you want with '-S' or '--Sub'.
##It will also search in the robots.txt file for links.
##The code make all the links that he found to a usable links and sort them if they from inside the website or outside link.


import requests, argparse, os, time, os.path, tldextract
from bs4 import BeautifulSoup


AllURL = []
WebURL = []
NotWebURL = []
Disallow = []
Allow = []
Sitemap = []
TorProxies = { 'http': 'socks5://127.0.0.1:9050', 'https': 'socks5://127.0.0.1:9050' }

parser = argparse.ArgumentParser(description='default usage: Spider.py -U URL')
parser.add_argument("-U", "--URL", required=True, help="Need to be the URL of the website")
parser.add_argument("-T", "--Tor", action='store_const', const=1, default=0, help="Tell the code to use tor")
parser.add_argument("-S", "--Sub", type=int, default=0, help="Tell the code to stop after x sublinks")
args = parser.parse_args()

ext = tldextract.extract(args.URL)
WebDomain = "%s.%s" %(ext.domain, ext.suffix)


def Spider(URL):
	try:
		if args.Tor == 1:
			os.system('service tor restart')
			time.sleep(0.2)
			r = requests.get(URL, proxies=TorProxies)
		elif args.Tor == 0:
			r = requests.get(URL)
		
		soup = BeautifulSoup(r.content, 'html.parser')
		
		for link in soup.find_all('a'):
			if link.get('href').startswith('/'):
				if URL.endswith('/'):
					if ("%s%s" %(URL[:-1], link.get('href'))) not in AllURL:
						AllURL.append("%s%s" %(URL[:-1], link.get('href')))
						WebURL.append("%s%s" %(URL[:-1], link.get('href')))
				else:
					if ("%s%s" %(URL, link.get('href'))) not in AllURL:
						AllURL.append("%s%s" %(URL, link.get('href')))
						WebURL.append("%s%s" %(URL, link.get('href')))
			elif link.get('href').startswith('./'):
				if URL.endswith('/'):
					if ("%s%s" %(URL[:-1], link.get('href')[1:])) not in AllURL:
						AllURL.append("%s%s" %(URL[:-1], link.get('href')[1:]))
						WebURL.append("%s%s" %(URL[:-1], link.get('href')[1:]))
				else:
					if ("%s%s" %(URL, link.get('href')[1:])) not in AllURL:
						AllURL.append("%s%s" %(URL, link.get('href')[1:]))
						WebURL.append("%s%s" %(URL, link.get('href')[1:]))
			elif WebDomain in link.get('href').split("//")[-1].split("/")[0].split('?')[0]:
				if link.get('href') not in AllURL:
					AllURL.append(link.get('href'))
					WebURL.append(link.get('href'))
			else:
				if link.get('href') not in AllURL:
					AllURL.append(link.get('href'))
					NotWebURL.append(link.get('href'))
	except:
		pass

def Check_Alive():
	if args.URL.startswith('http://') != True and args.URL.startswith('https://') != True:
		print('Error: You need to enter the full URL with the protocol (http / https)!')
		exit()
	
	if os.path.isfile('SpiderFiles/%s' %(WebDomain)):
		while True:
			print("You've already scan this page, if you scan this again its will remove your old scan!")
			i = input("Enter 1 to scan again or 0 to exit: ")
			if i == '1':
				break
			elif i == '0':
				exit()
			else:
				print('Incorrect input! \nTry again.')
	
	try:
		if args.Tor == 1:
			os.system('service tor restart')
			time.sleep(0.2)
			CAlive = requests.head(args.URL, proxies=TorProxies).status_code
		elif args.Tor == 0:
			CAlive = requests.head(args.URL).status_code
	except:
		CAlive = 0

	if CAlive != 200:
		print("The Website not up!")
		exit()
	
	Start_Spider()

def Start_Spider():
	if os.path.isdir('SpiderFiles') == False:
		os.mkdir('SpiderFiles')
		
	AllURL.append(args.URL)
	WebURL.append(args.URL)
	
	for Sub in range(args.Sub + 1):
		if Sub <= len(WebURL) - 1:
			Spider(WebURL[Sub])
			Stop = Sub
		else:
			break
	
	Robots_Parse(Stop)

def Robots_Parse(Stop):
	if args.URL.endswith('/'):
		URL = args.URL[:-1]
	else:
		URL = args.URL
	
	if args.Tor == 1:
		os.system('service tor restart')
		time.sleep(0.2)
		r = requests.get("%s/robots.txt" %(URL), proxies=TorProxies)
	elif args.Tor == 0:
		r = requests.get("%s/robots.txt" %(URL))
	
	for l in r.text.splitlines():
		if l.startswith("Disallow: ") or l.startswith("Allow: ") or l.startswith("Sitemap: "):
			if l.split(' ')[-1].startswith('/'):
				url = URL + l.split(' ')[-1]
			elif l.split(' ')[-1].startswith('*'):
				url = URL + "/" + l.split(' ')[-1]
			elif l.split(' ')[-1].startswith(' '):
				pass
			else:
				url = l.split(' ')[-1]
			
			if l.split(' ')[-1].startswith(' ') != True:
				if url not in AllURL:
					if l.startswith("Disallow: "):
						Disallow.append(url)
						AllURL.append(url)
					elif l.startswith("Allow: "):
						Allow.append(url)
						AllURL.append(url)
					elif l.startswith("Sitemap:"):
						Sitemap.append(url)
						AllURL.append(url)

	Save_To_File(Stop)

def Save_To_File(Stop):
	WebURL.sort()
	NotWebURL.sort()
	Disallow.sort()
	Allow.sort()
	Sitemap.sort()
	
	f = open('SpiderFiles/%s' %(WebDomain) ,'w')
	f.write('Here the spider scan the website %s and %s sublinks.\n' %(args.URL, Stop))
	if Stop < args.Sub:
		f.write('[*] The spider stops because he don`t found more links of the site.\n')
	f.write('The spider foud %s links in the website:\n' %(len(AllURL)))
	if len(WebURL) > 0:
		f.write('	%s links is inside the site.\n' %(len(WebURL)))
	if len(NotWebURL) > 0:
		f.write('	%s links is outside the site.\n' %(len(NotWebURL)))
	if len(Disallow) > 0 or len(Allow) > 0 or len(Sitemap) > 0:
		f.write('	%s links from robots.txt file.\n\n' %(len(Disallow)+len(Allow)+len(Sitemap)))
	f.flush()
	
	if len(WebURL) > 0:
		f.write('Links inside the site:\n')
		for u in WebURL:
			f.write('	%s\n' %(u))
			f.flush()

	if len(NotWebURL) > 0:
		f.write('\nLinks outside the site:\n')
		for u in NotWebURL:
			f.write('	%s\n' %(u))
			f.flush()

	if len(Disallow) > 0 or len(Allow) > 0 or len(Sitemap) > 0:
		f.write('\nLinks from robots.txt file:\n')
	if len(Disallow) > 0:
		f.write('	Disallow:\n')
		for u in Disallow:
			f.write('		%s\n' %(u))
			f.flush()
	if len(Allow) > 0:
		f.write('	Allow:\n')
		for u in Allow:
			f.write('		%s\n' %(u))
			f.flush()
	if len(Sitemap) > 0:
		f.write('	Sitemap:\n')
		for u in Sitemap:
			f.write('		%s\n' %(u))
			f.flush()
	f.close()


if args.Tor == 1:
	if not os.geteuid() == 0:
		print("Only root can run this with tor!")
		exit()

Check_Alive()
