#!/usr/bin/python3


##This code is replacement for intruder in burpsuite.
##He do what burpsuite can do but without restrictions and more faster.
##The default command is 'python3 Intruder_Replacement.py -F (file with request content)'
##  !You need to place the markeds before you start this!
##  To mark a place in the file you need to mark it with &; in the start of the place you want to mark and ;& in the end of place you want to mark.
##  It should look like this: Hey &;mark1;&, I`m &;mark2;&.
##Second you need to choose the way you want to do this (-S = SniperTool, -B = BatteringRam, -P = Pitchfork or -C = Clusterbomb).
##  SniperTool = Allows only 1 payload, and runs by order in all the marked postions.
##  BatteringRam = Allows only 1 payload, runs on ALL the marked postions in the same time.
##  Pitchfork = All the payload lists move at the same pace per postion (1 payload for each postion marked).
##  Clusterbomb = Tries all possible combinations of payloads per postion (1 payload for each postion marked).
##The command should look like this: python3 Intruder_Replacement.py -F Req.txt -C
##  In this command the file with the request content is Req.txt and we use Clusterbomb.


import requests, argparse, re, os.path, itertools
from urllib.parse import urlparse


parser = argparse.ArgumentParser(description='Default usage: HidParamsGess.py -F File')
parser.add_argument("-F", "--File", required=True, help="The file with the request content")
parser.add_argument("-S", "--SniperTool", action='store_const', const=1, default=0, help="Tell the code to use Sniper tool ")
parser.add_argument("-B", "--BatteringRam", action='store_const', const=1, default=0, help="Tell the code to use BatteringRam")
parser.add_argument("-P", "--Pitchfork", action='store_const', const=1, default=0, help="Tell the code to use Pitchfork")
parser.add_argument("-C", "--Clusterbomb", action='store_const', const=1, default=0, help="Tell the code to use Pitchfork")
args = parser.parse_args()


def Checker():
	if os.path.isfile(args.File) == 0:
		print('The file you gave is not exist!')
		exit()
	if args.SniperTool == 0 and args.BatteringRam == 0 and args.Pitchfork == 0 and args.Clusterbomb == 0:
		print('You need to choose a way to do this!')
		print('-S = Sniper Tool, -B = Battering Ram, -P = Pitchfork, -C = Clusterbomb')
		exit()
	elif args.SniperTool and args.BatteringRam or args.SniperTool and args.Pitchfork or args.BatteringRam and args.Pitchfork or args.Clusterbomb and args.SniperTool or args.Clusterbomb and args.BatteringRam or args.Clusterbomb and args.Pitchfork:
		print('Yoy need to choose ONLY one way to do this')
		print('-S = Sniper Tool, -B = Battering Ram, -P = Pitchfork, -C = Clusterbomb')
		exit()
	elif args.SniperTool or args.BatteringRam:
		Payload = []
		while True:
			print('1 = Numbers')
			print('2 = From file')
			P = input('Enter the number of the payload you want: ')
			while True:
				if P == '1':
					r = input('Enter the number range you want (like 1-10): ')
					if '-' in r and len(r.split('-')) == 2 and r.split('-')[0].isdigit() and r.split('-')[1].isdigit():
						for n in range(int(r.split('-')[0]), int(r.split('-')[1])+1):
							Payload.append(str(n))
						break
					else:
						print('Error, You don`t type it right!')
				elif P == '2':
					while True:
						f = input('Enter the file name with the payload you want: ')
						if os.path.isfile(f):
							F = open(f, 'r')
							for Pay in F.read().splitlines():
								Payload.append(Pay)
							F.close()
							break
						else:
							print('There is no file with this name!')
							print('Try Again\n')
				else:
					print('Your input is incurrect!')
					print('Try again\n')
					break
				if len(Payload) > 0:
					break
			if len(Payload) > 0:
				break
	elif args.Pitchfork or args.Clusterbomb:
		Payload = []
		F = open(args.File, 'r')
		RequestFile = F.read()
		F.close()
		for Re in range(len(re.findall('&;.[^;&]*;&', RequestFile))):
			while True:
				print('1 = Numbers')
				print('2 = From file')
				P = input('Enter the number of the payload number %s you want for : ' %(Re+1))
				while True:
					if P == '1':
						r = input('Enter the number range you want (like 1-10): ')
						if '-' in r and len(r.split('-')) == 2 and r.split('-')[0].isdigit() and r.split('-')[1].isdigit():
							Payload.append([])
							for n in range(int(r.split('-')[0]), int(r.split('-')[1])+1):
								Payload[int(Re)].append(str(n))
							break
						else:
							print('Error, You don`t type it right!')
					elif P == '2':
						while True:
							f = input('Enter the file name with the payload you want: ')
							if os.path.isfile(f):
								Payload.append([])
								F = open(f, 'r')
								for Pay in F.read().splitlines():
									Payload[int(Re)].append(Pay)
								F.close()
								break
							else:
								print('There is no file with this name!')
								print('Try Again\n')
					else:
						print('Your input is incurrect!')
						print('Try again\n')
						break
					if len(Payload) > 0:
						break
				if len(Payload) > 0:
					break
	Intruder_Replacement(Payload)

def Intruder_Replacement(Payload):
	F = open(args.File, 'r')
	RequestFile = F.read().splitlines()
	F.close()
	ORequest = []
	for l in RequestFile:
		O = re.sub('&;', '', l)
		ORequest.append(re.sub(';&', '', O))
	if args.BatteringRam:
		BatteringRam(ORequest, RequestFile, Payload)
	elif args.SniperTool:
		SniperTool(ORequest, RequestFile, Payload)
	elif args.Pitchfork:
		Pitchfork(ORequest, RequestFile, Payload)
	elif args.Clusterbomb:
		Clusterbomb(ORequest, RequestFile, Payload)

def SniperTool(ORequest, RequestFile, Payload):
	url, Head, m, Params = GetParams(ORequest)
	Data = {}
	for i in Params:
		Data[i] = Params[i]
	Page = Request(url, Head, Data, m).text
	print('Original = %s' %(len(Page)))
	for t in range(len(re.findall('&;.[^;&]*;&', '\n'.join(RequestFile)))):
		for Pay in Payload:
			if t > 0:
				r = re.sub('&;', '', '\n'.join(RequestFile), t)
				r = re.sub(';&', '', r, t)
				r = re.sub('&;.[^;&]*;&', Pay, r, 1)
				r = re.sub('&;', '', r)
				r = re.sub(';&', '', r)
			else:
				r = re.sub('&;.[^;&]*;&', Pay, '\n'.join(RequestFile), 1)
				r = re.sub('&;', '', r)
				r = re.sub(';&', '', r)
			url, Head, m, Params = GetParams(r.splitlines())
			Data = {}
			for i in Params:
				Data[i] = Params[i]
			Page = Request(url, Head, Data, m).text
			print('%s,%s = %s' %(t, Pay, len(Page)))

def BatteringRam(ORequest, RequestFile, Payload):
	url, Head, m, Params = GetParams(ORequest)
	Data = {}
	for i in Params:
		Data[i] = Params[i]
	Page = Request(url, Head, Data, m).text
	print('Original = %s' %(len(Page)))
	for Pay in Payload:
		Req = []
		for l in RequestFile:
			Req.append(re.sub('&;.[^;&]*;&', str(Pay), l))
		url, Head, m, Params = GetParams(Req)
		Data = {}
		for i in Params:
			Data[i] = Params[i]
		Page = Request(url, Head, Data, m).text
		print('%s = %s' %(Pay, len(Page)))

def Pitchfork(ORequest, RequestFile, Payload):
	t = 0
	for l in range(len(re.findall('&;.[^;&]*;&', '\n'.join(RequestFile)))):
		if len(Payload[l]) > t:
			t = len(Payload[l])
	url, Head, m, Params = GetParams(ORequest)
	Data = {}
	for i in Params:
		Data[i] = Params[i]
	Page = Request(url, Head, Data, m).text
	print('Original = %s' %(len(Page)))
	for p in range(t):
		r = '\n'.join(RequestFile)
		for l in range(len(re.findall('&;.[^;&]*;&', '\n'.join(RequestFile)))):
			if p < len(Payload[l]):
				r = re.sub('&;.[^;&]*;&', Payload[l][p], r, 1)
			else:
				r = re.sub('&;', '', r, 1)
				r = re.sub(';&', '', r, 1)
		url, Head, m, Params = GetParams(r.splitlines())
		Data = {}
		for i in Params:
			Data[i] = Params[i]
		Page = Request(url, Head, Data, m).text
		for l in range(len(re.findall('&;.[^;&]*;&', '\n'.join(RequestFile)))):
			if p < len(Payload[l]):
				if l != range(len(re.findall('&;.[^;&]*;&', '\n'.join(RequestFile))))[-1]:
					print('%s , ' %(Payload[l][p]), end = '')
				else:
					print(Payload[l][p], end = '')
			else:
				if l != range(len(re.findall('&;.[^;&]*;&', '\n'.join(RequestFile))))[-1]:
					print('Original , ' , end = '')
				else:
					print('Original', end = '')
		print(' = %s' %(len(Page)))

def Clusterbomb(ORequest, RequestFile, Payload):
	url, Head, m, Params = GetParams(ORequest)
	Data = {}
	for i in Params:
		Data[i] = Params[i]
	Page = Request(url, Head, Data, m).text
	print('Original = %s' %(len(Page)))
	Pay = list(itertools.product(*Payload))
	for t in range(len(Pay)):
		r = '\n'.join(RequestFile)
		for p in range(len(re.findall('&;.[^;&]*;&', '\n'.join(RequestFile)))):
			r = re.sub('&;.[^;&]*;&', Pay[t][p], r, 1)
		url, Head, m, Params = GetParams(r.splitlines())
		Data = {}
		for i in Params:
			Data[i] = Params[i]
		Page = Request(url, Head, Data, m).text
		print('%s = %s' %(' , '.join(Pay[t]), len(Page)))

def GetParams(Req):
	Head = {}
	Params = {}
	for i in Req:
		if i == '':
			break
		elif i.startswith('POST'):
			m = 'Post'
			u = i.split(' ')[1]
		elif i.startswith('GET'):
			m = 'Get'
			u = i.split(' ')[1]
		else:
			Head['%s' %(i.split(': ',1)[0])] = '%s' %(i.split(': ',1)[1])
	
	url = 'http://%s%s' %(Head["Host"], u)	
	if m == 'Get':
		if '=' in urlparse(url).query:
			if '&' in urlparse(url).query:
				for i in urlparse(url).query.split('&'):
					if '=' in i:
						Params[i.split('=')[0]] = i.split('=')[1]
			else:
				Params[urlparse(url).query.split('=')[0]] = urlparse(url).query.split('=')[1]
		url = 'http://%s%s' %(Head["Host"], urlparse(url).path)
	elif m == 'Post':
		if '=' in Req[-1]:
			if '&' in Req[-1]:
				for i in Req[-1].split('&'):
					if '=' in i:
						Params[i.split('=')[0]] = i.split('=')[1]
			else:
				Params[f[-1].split('=')[0]] = f[-1].split('=')[1]
		
	return (url, Head, m, Params)

def Request(url, Head, Data, m):
	if m == 'Post':
		return(requests.post(url, headers=Head, data=Data))
	elif m == 'Get':
		return(requests.get(url, headers=Head, params=Data))


Checker()
