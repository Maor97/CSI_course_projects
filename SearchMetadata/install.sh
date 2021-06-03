##Install all necessary software and configuration to SearchMetadata software
##needed premisions to run!

#!/bin/bash

if [ "$(whoami)" == "root" ]; then
	apt update
	apt install tor -y
	systemctl enable tor
	apt install xterm
	if [ -z "$(crontab -l | grep "@reboot $(pwd)/searchmetadata.sh")" ]; then
		(crontab -l ; echo "@reboot $(pwd)/searchmetadata.sh")| crontab -
	fi
	bash searchmetadata.sh
else
	echo "You need to be root to run this!"
fi
