# The code is on ssh hardening by Maor Sofer.
# Anyone that use openssh-server should use it.
# On each sub-topic you have a question that asks if you want to harden this way.

#!/bin/bash

function updatessh()
{
apt update && apt install openssh-server -y
}

function changeport()
{
sed -i "s/$(cat /etc/ssh/sshd_config | grep -i "port ")/Port $sshportq/g" /etc/ssh/sshd_config
}

function x11disable()
{
sed -i "s/$(cat /etc/ssh/sshd_config | grep "^X11Forwarding")/X11Forwarding no/g" /etc/ssh/sshd_config
}

function ignorerhosts()
{
sed -i "s/$(cat /etc/ssh/sshd_config | grep "Rhosts")/IgnoreRhosts yes/g" /etc/ssh/sshd_config
}

function usedns()
{
sed -i "s/$(cat /etc/ssh/sshd_config | grep "UseDNS")/UseDNS yes/g" /etc/ssh/sshd_config
}

function pubkey()
{
sed -i "s/$(cat /etc/ssh/sshd_config | grep "PubkeyAuthentication")/PubkeyAuthentication yes/g" /etc/ssh/sshd_config
sed -i "s/$(cat /etc/ssh/sshd_config | grep "PasswordAuthentication yes\|PasswordAuthentication no")/PasswordAuthentication no/g" /etc/ssh/sshd_config
}

function maxtries()
{
sed -i "s/$(cat /etc/ssh/sshd_config | grep MaxAuthTries)/MaxAuthTries 3/g" /etc/ssh/sshd_config
}

function disableemptypasswords()
{
sed -i "s/$(cat /etc/ssh/sshd_config | grep "PermitEmptyPassword")/PermitEmptyPasswords yes/g" /etc/ssh/sshd_config
}

function norootlogin()
{
sed -i "s/$(cat /etc/ssh/sshd_config | grep "^PermitRootLogin\|^#PermitRootLogin")/PermitRootLogin no/g" /etc/ssh/sshd_config
}

function disconnect()
{
sed -i "s/$(cat /etc/ssh/sshd_config | grep "ClientAliveInterval")/ClientAliveInterval $interval/g" /etc/ssh/sshd_config
sed -i "s/$(cat /etc/ssh/sshd_config | grep "ClientAliveCountMax")/ClientAliveCountMax $countmax/g" /etc/ssh/sshd_config
}

function fail2ban()
{
apt update && apt install fail2ban -y
cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.local
sudo sed -i "s/# \[sshd\]/\[sshd\]/" /etc/fail2ban/jail.local
sed -i "s/$(cat /etc/fail2ban/jail.local | grep "# enabled = true")/enabled = true/g" /etc/fail2ban/jail.local
if [ "$whitelistq" == "y" ]; then
sed -i "s/#ignoreip = 127.0.0.1\/8 ::1/ignoreip = 127.0.0.1\/8 $ignoreipq/g" /etc/fail2ban/jail.local
fi
service fail2ban restart
}


echo "Starting to hardening your ssh..."
read -p "You want to update ssh? type (y)es if you want: " updateq
read -p "You want to change ssh port? if you want to change type the port you want: " sshportq
read -p "You want to disable X11Forwading? type (y)es if you want: " x11q
read -p "You want to disable rhost authenticate system? type (y)es if you want: " ignorerhostsq
read -p "You want to enable DNS hostname checking? type (y)es if you want: " usednsq
read -p "You want to use public key authentication instead of password? type (y)es or (n)o: " pubkeyq
if [ "$pubkeyq" == "n" ]; then
read -p "You want to set maximum authentication attempts to 3? type (y)es if you want: " maxtriesq
read -p "You want to disable empty passwords login? type (y)es if you want: " disableemptypasswordsq
fi
read -p "You want to disable root login? type (y)es if you want: " norootloginq
read -p "You want to use client alive method? type (y)es if you want: " disconnectq
if [ "$disconnectq" == "y" ]; then
read -p "Enter the time you want to send alive message to user (in seconds): " interval
read -p "Enter how much time you want to send alive message to user: " countmax
fi
read -p "You want to install and use Fail2Ban program? type (y)es if you want: " fail2banq
if [ "$fail2banq" == "y" ]; then
read -p "You want to add IP to white list of Fail2Ban? type (y)es if you want: " whitelistq
	if [ "$whitelistq" == "y" ]; then
	read -p "Type the IP you want (if you want more then one ip  separate them with a space): " ignoreipq
	fi
fi


cp /etc/ssh/sshd_config /etc/ssh/sshd_config.backup


if [ "$updateq" == "y" ]; then
updatessh
fi

if [ "$sshportq" -gt 0 ] 2>/dev/null ; then
changeport
fi

if [ "$x11q" == "y" ]; then
x11disable
fi

if [ "$ignorerhostsq" == "y" ]; then
ignorerhosts
fi

if [ "$usednsq" == "y" ]; then
usedns
fi

if [ "$pubkeyq" == "y" ]; then
pubkey
fi

if [ "$maxtriesq" == "y" ]; then
maxtries
fi

if [ "$disableemptypasswordsq" == "y" ]; then
disableemptypasswords
fi

if [ "$norootloginq" == "y" ]; then
norootlogin
fi

if [ "$disconnectq" == "y" ]; then
disconnect
fi

if [ "$disconnectq" == "y" ]; then
disconnect
fi

if [ "$fail2banq" == "y" ]; then
fail2ban
fi


service ssh restart
echo "We done to Hardening your ssh server! ;-)"
if [ "$pubkeyq" == "y" ]; then
echo "Now every user need to create public key to login in ssh!"
fi
echo "Always remember... it's harder to break if you have a strong and complex password"
