#1/bin/bash


cat="files"
cat2="system"

	show_files () {
	
	cd 
	ls -la
	pwd 
}

show_system () {
	
        uname -a
	lshw 
}

echo This program will let you view $cat and $cat2 
echo choose files for file info or system for system info.
read choice
if 
	[  $choice = $cat ]

then
        show_files
else
	echo not a valid choice. Ending program
fi
if
	[ $choice = $cat2 ]
then
	show_system
else
	echo not an option. ending program
fi





	
