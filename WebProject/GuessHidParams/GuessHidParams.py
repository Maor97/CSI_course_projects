#!/usr/bin/python3


##This code will search for hidden parameters in url with request file.
##It search in post or get method (depends on the request file).
##First it sent request with the default request to see the default page response.
##Second, it sent requests with parameters from 'Params.db' file (one per request and if the parameter does not exist in the default request).
##If the code notices a change in response from the default it store it (in Hidden list).
##At the end if the code find any hidden parameters it print them.


import requests, argparse
from urllib.parse import urlparse


parser = argparse.ArgumentParser(description='Default usage: HidParamsGess.py -F File')
parser.add_argument("-F", "--File", required=True, help="The file with the requests content")
args = parser.parse_args()


def GuessHidParams():
	url, Head, m, Params = GetParams()
	f = open('Params.db', 'r')
	Guess = f.read().splitlines()
	f.close()
	
	Data = {}
	for i in Params:
		Data[i] = Params[i]
	Page = Request(url, Head, Data, m).text
	
	Hidden = []
	for g in Guess:
		if g not in Params:
			for n in range(2):
				Data = {}
				for i in Params:
					Data[i] = Params[i]
				Data[g] =  n
				r = Request(url, Head, Data, m).text
				if r != Page:
					Hidden.append(g)
					break
	
	if len(Hidden) == 0:
		print('With the requests file from the website (%s), We could not find any hidden parameters... :-(' %(url))
		exit()
	elif len(Hidden) == 1:
		print('With the requests file from the website (%s), we pulled this hidden parameter: %s' %(url, Guess[0]))
	elif len(Hidden) > 1:
		print('With the requests file from the website (%s), we pulled this hidden parameters:' %(url))
		for h in Hidden:
			if h != Hidden[-1]:
				print('%s, ' %(h), end='')
			else:
				print(h)

def GetParams():
	Head = {}
	Params = {}
	F = open(args.File, 'r')
	f = F.read().splitlines()
	F.close()
	for i in f:
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
		if '=' in f[-1]:
			if '&' in f[-1]:
				for i in f[-1].split('&'):
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


GuessHidParams()
