#### SearchMetadata ####
The software downloads images from sites that are in the url.db file and looks for hidden data behind them & GPS coordinates.
If the software find hidden data behind the image, it record it in searchmetadata.log in log folder and tell you in the log where it save the file with binwalk results.
If the software find GPS coordinates, it record it in searchmetadata.log in log folder and tell you in the log where it saved the file with exiftool results.
The software runs all the time and you can add or remove urls any time you want from url.db file.
The software uses crontab to continue to run after restart.
In each sites scan-loop of the software, it keeps all the sites it has left to scan within the log/lasturls.log file, so that the software can return exactly where it was before the restart.
The software saves all the photo`s md5-hashes that he scans in the log/scanhashes.log to avoid a duplication scan and allows you to know which photos were scanned by the software.
The main log file of the software is log/searchmetadata.log that contains all the logs of the software itself, and shows you whether or not the software found any hidden files and/or GPS coordinates,
as well as any errors in the software.
The software uses pop ups to tell you if there are  any error and shows you what the error are and how to fix them.
In the log/files folder the software contains all the files that he found with any hidden files or GPS coordinates, including them in the folder with binwalk or exiftool results.
The software uses binwalk to scan for hidden files behind the photos.
The software uses exiftool to see if there are any GPS coordinates in the photos.
The software uses tor service and torify command to be a 100% anonymous.

#### Install and preparation for start ####
Before you can run the software you need to add urls to the url.db file.
After this you need to run install.sh.
The file will install all the important stuff (such as: tor service and xterm commend) and writes a commend in crontab to run after any reboot.
After the file finish running, it starts the searchmetadata software.

#### How to use ####
The software runs automatically and does all the scans on its own, all you have to do is to insert the urls of the sites you want to scan to url.db file.
Ifat any point you'd like to add or remove urls, you just need to edit the url.db file without touching the software's code.

