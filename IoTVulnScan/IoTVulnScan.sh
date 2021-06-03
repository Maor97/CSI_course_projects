#!/bin/bash

##Welcome To IoTVulnScan...
##This software will scan with shodan API for all the IP addresses that are using vendors from RouterSploit.
##Shodan site = https://www.shodan.io/
##RouterSploit Github = https://github.com/threat9/routersploit
##The software extract the IP addresses with the countries and organizations for each IP and save it in IoTDevices.db file.
##After it get all the IP addresses it need, it start to search for vulnerabilities for each IP with RouterSploiut.
##If it found vulnerability in IP it will save the IP address in ScansReport.log file with the relevant routersploit vulnerability, the country and organization of the IP and the time it was found.
##When the software ends it will delete routersploit.log and IoTDevices.db files.

##Anyone looking for IoT devices with vulnerabilities should use this software.
##You don't need any special skills to run it.
##Just run it with the commend "bash IoTVulnScan.sh" or add execute option to the software and run it with "./IoTVulnScan.sh".

function ShodanScan {
	#This function will search in shodan and get IP addresses with the countries and organizations for each IP.
	shodan search --fields ip_str,location.country_code,org $Ven 2>/dev/null
}

function RSploitScan {
	#This function will start RouterSploit with the autopwn scanner and start scan target.
	./routersploit/rsf.py -m scanners/autopwn -s "target $IP" 2>/dev/null
}

function VendorsScan {
	#This function will go for each vendor in Vendors.db file and search it in shodan.
	#If Shodan founds IP addresses of the vendor it will save it in the IoTDevices.db file.
	for Ven in $(cat Vendors.db); do
		echo "Scan for $Ven IoT device in shodan"
		SS=$(ShodanScan)
		if [ $(echo "$SS" | sed '/^\s*#/d;/^\s*$/d' | wc -l) == 0 ]; then
			echo "[-] No IP addresses found"
		elif [ $(echo "$SS" | sed '/^\s*#/d;/^\s*$/d' | wc -l) == 1 ]; then
			echo "[+] $(echo "$SS" | sed '/^\s*#/d;/^\s*$/d' | wc -l) IP address found"
			echo "$SS" | sed '/^\s*#/d;/^\s*$/d'>> ./IoTDevices.db
		else
			echo "[+] $(echo "$SS" | sed '/^\s*#/d;/^\s*$/d' | wc -l) IP addresses found"
			echo "$SS" | sed '/^\s*#/d;/^\s*$/d' >> ./IoTDevices.db
		fi
		echo "Shodan scan for $Ven IoT device done"
	done
}

function IPsScan {
	#This function will scan each IP address that shodan found with RouterSploit,
	#If RouterSploit found any vulnerability it will save the IP address in ScansReport.log file with the relevant routersploit vulnerability, the country and organization of the IP and the time it was found.
	for line in $(cat ./IoTDevices.db); do
		IP=$(echo $line | awk '{print$1}')
		echo "Start scan $IP"
		RSS=$(RSploitScan)
		if [ $(echo "$RSS" | grep "[+]" | grep -v "target => $IP" | wc -l) -gt 0 ]; then
			echo "IP = $IP" >> ScansReport.log
			echo "Relevant RouterSploit vulnerability: $(echo "$RSS" | grep "[+]" | grep -v "target => $IP" | cut -d' ' -f 3-4)" >> ScansReport.log
			echo "Country: $(echo $line | awk '{print$2}')" >> ScansReport.log
			echo "Organization: $(echo $line | awk '{print$3}')" >> ScansReport.log
			echo "Time: $(date '+%d/%m/%Y %H:%M')" >> ScansReport.log
			echo "---------------------------------------------------------------------------------------------------------------" >> ScansReport.log
			echo "[+] Find vulnerability"
		else
			echo "[-] Don't find vulnerability"
		fi
		echo "Scan $IP done"
	done
}


IFS=$(echo -en "\n\b") #Ignore spaces.


VendorsScan	#Start "VendorsScan founction.
#If the shodan scans found any IP addressess run IPsScan function and after that delete the routersploit.log and IoTDevices.db files.
if [ -f ./IoTDevices.db ]; then
	IPsScan
	rm ./routersploit.log
	rm ./IoTDevices.db
else
	echo "[!] Don't find any IPs"
fi

echo "IoT vulnerability scan done."
