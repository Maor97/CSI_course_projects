#!/bin/bash

##This script will install all the necessary stuff for IoTVulnScan software.
##You need to put your Shodan API key in the install commend to initialize the api key.
##bash Install.sh Your_API_Key OR ./Install.sh Your_API_Key
##The installer will install python 3 pip, shodan api, shodan API key and routersploit requirements.

#You need to run it with root permissions.
if [ $(whoami) != 'root' ]; then
	echo "You must be root to do this!"
	exit
fi

#You need to put your shodan API key.
if [ -z $1 ]; then
	echo "You need to put your API key in external variavle! (after the Install.sh)"
	exit
fi


ApiKey=$1	#shodan API key

apt-get install python3-pip -y -qq > /dev/null				#Install python 3 pip.
pip3 install shodan -q										#Install shodan through python pip.
shodan init $ApiKey											#Install shodan API key.
git clone -q https://github.com/threat9/routersploit.git	#Clone the RouterSploit files from github repositorie.
python3 -m pip install -r routersploit/requirements.txt		#Install RouterSploit requirements.
echo -e "\033[0;32mInstall Successful =]"
