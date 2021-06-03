##The software downloads images from sites that are in the url.db file and looks for hidden data behind them & GPS coordinates.
##If the software find hidden data behind the image, it record it in searchmetadata.log in the log folder and tell you in the log where it save the file with binwalk results.
##If the software find GPS coordinates, it record it in searchmetadata.log in the log folder and tell you in the log where it saved the file with exiftool results.

#!/bin/bash

function searchphotos()
{
	service tor restart
	if [ "$(service tor status | grep "active" | awk '{print $2}')" == "active" ]; then
		if [ "$(whois "$(echo $(torify curl -s ifconfig.me))" | grep -i country | awk '{print $2}')" == "IL" ]; then
			echo "$(date +%F-%X) -> [!] Exit from the software because you are not anonymous" >> ./log/searchmetadata.log
			xterm -e "echo -e '\033[1m'[!] You are not anonymous;echo -e '\033[0m'Exit From the software because you are not anonymous;echo Fix this by restart your PC and run install.sh again;read"
			exit
		else
			torify wget --no-check-certificate -mke robots=off -nd -r -c -q -P ./WebsitePhotos -A jpeg,jpg,nmp,gif,png $url
			for file in $(ls ./WebsitePhotos); do
				if [ -z "$(cat ./log/scanhashes.log | grep $(md5sum ./WebsitePhotos/$file | awk '{print $1}') | awk '{print $1}')" ]; then
					Date=$(date +%F-%X)
					binwalk ./WebsitePhotos/$file > ./WebsitePhotos/$file-binwalk.txt
					if [ $(cat ./WebsitePhotosl/$file-binwalk.txt | wc -l) -gt 6 ]; then
						echo "$Date -> [+] In $file from $url found hidden data behind them" >> ./log/searchmetadata.log
						mkdir ./log/files/$Date
						cp ./WebsitePhotos/$file ./log/files/$Date/
						mv ./WebsitePhotos/$file-binwalk.txt ./log/files/$Date/
						echo "The file saved in log/files/$Date/ folder with binwalk result" >> ./log/searchmetadata.log
						md5sum ./WebsitePhotos/$file >> ./log/scanhashes.log
					else
						echo "$Date -> [-] In $file from $url not found hidden data behind them" >> ./log/searchmetadata.log
						rm -f ./WebsitePhotos/$file-binwalk.txt
					fi
					exiftool ./WebsitePhotos/$file >> ./WebsitePhotos/$file-exiftool.txt
					if [[ $(cat ./WebsitePhotos/$file-exiftool.txt| grep -i gps) ]]; then
						echo "$Date -> [+] In $file from $url exist GPS data" >> ./log/searchmetadata.log
						mkdir ./log/files/$Date
						cp ./WebsitePhotos/$file ./log/files/
						mv ./WebsitePhotos/$file-exiftool.txt ./log/files/$Date
						echo "The file saved in log/files/$Date/ folder with exiftool result" >> ./log/searchmetadata.log
					else
						echo "$Date -> [-] In $file from $url not exist GPS data" >> ./log/searchmetadata.log
						rm -f ./WebsitePhotos/$file-exiftool.txt
					fi
					md5sum ./WebsitePhotos/$file >> ./log/scanhashes.log
					rm -f ./WebsitePhotos/$file
				fi
			done
			rm -rf ./WebsitePhotos
			sed -i '1d' ./log/lasturls.log
		fi
		else
			echo "$(date +%F-%X) -> [!] Exit from the software because the tor service are not working" >> ./log/searchmetadata.log
			xterm -e "echo -e '\033[1m'[!] Tor service are not working;echo -e '\033[0m'Exit from the software because tor service are not working;echo Fix this by restart your PC and run install.sh again;read"
			exit
		fi

}

if [ "$(whoami)" == "root" ]; then
	if [[ $(ls ./log/ | grep lasturls.log) ]]; then
		if [[ $(cat ./log/lasturls.log) ]]; then
			for url in $(cat ./log/lasturls.log); do
				searchphotos
			done
		fi
	fi
	#while true; do
		if [[ $(cat url.db | tail -n +4) ]]; then
			cat url.db | tail -n +4 > ./log/lasturls.log
			for url in $(cat ./log/lasturls.log); do
				searchphotos
			done
		else
			echo "$(date +%F-%X) -> [!] Exit from the softwer because there is no urls inside the file url.db" >> ./log/searchmetadata.log
			xterm -e "echo -e '\033[1m'[!] There is no urls inside the file url.db;echo -e '\033[0m'Exit from the softwer because there is no urls inside the file url.db;echo Fix this by adding urls in to url.db and reopen the software or jush restart your PC;read"
			exit
		fi
	#done
else
        echo "You need to be root to run this!"
fi
