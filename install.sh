#!/bin/bash
# Project: bp-voltmeter
# File: install.sh
# Version: 0.1
# Create by: Rom1 <rom1@canel.ch>
#            CANEL - https://www.canel.ch
# Date: 24/09/17
# Licence: GNU GENERAL PUBLIC LICENSE v3
# Language: Bash
# Description: Install bp-voltmeter. It's a voltmeter for the Bus Pirate


usage()
{
	echo "Usage: $(basename $0) [-fh] [-i <apt|pip|none>] [-n <name>] [-p <prefix>]"
	echo -e "\t-h\tHelp"
	echo -e "\t-i\tInstall libraries with APT or PIP3 or NONE (Default: None))"
	echo -e "\t-n\tExecutable's name (Default: voltmeter)"
	echo -e "\t-p\tPath to install (Default: /usr/local/bin)"
}

be_root()
{
	if  [  `id  -u`  -eq  0  ]
	then
		"$@"
	elif  [  -x  /bin/sudo  -o  -x  /usr/bin/sudo    ]
	then
		/usr/bin/sudo  "$@"
	else
		echo  "Need administrator privileges"
	fi
}

while getopts "hi:n:p:" sel
do
	case $sel in
		h)
			usage
			exit 0
			;;
		i)
			package_type="$OPTARG"
			case $package_type in
				apt|APT)
					serial=python3-serial
					dpkg -s "$serial" > /dev/null 2>&1
					if [ "$?" -ne 0 ]
					then
						be_root apt-get install --no-install-recommends $serial
					fi
					;;
				pip|PIP)
					serial=pyserial
					pip3 list --format=legacy | grep $serial > /dev/null 2>&1
					if [ "$?" -ne 0 ]
					then
						be_root pip3 install $serial
					fi
					;;
				*)
					echo "Bad argument"
					usage
					exit 1
					;;
			esac
			;;
		n)
			name="$OPTARG"
			;;
		p)
			dir_install="$OPTARG"
			;;
		*)
			usage
			exit 1
			;;
	esac
done

dir_install=${dir_install:-/usr/local/bin}
name=${name:-voltmeter}

if [ -O "$dir_install" ]
then
	ln -f -v -s "$(pwd)/bp-voltmeter.py" "${dir_install}/${name}"
else
	be_root ln -f -v -s "$(pwd)/bp-voltmeter.py" "${dir_install}/${name}"
fi

exit 0


# vim: ft=bash tw=100 et ts=8 sw=8
