#!/bin/bash

#This is a very simple for loop.
# this is the for statement. declaring the variable i.  It will take on different values in the output of ls
for i in $( ls ); 
#do command. It will print item for every file listed in the output of the ls
do
	echo item: $i
#done statement completes the loop	
done


#########################################################
# This is an example of a whilre loo

# This line sets the variable as 1. Counting starts at the number 1
number=1
# This is the while statement. the list inside the brackets ends at 10
while [ $number -le 10 ]
#do command. Telling the system to go through the list, 1-10
do
# This echo command prints the nummber/list to screen
	echo $number
# Counter command inside double parenthesis. Tells syetem to count
	(( COUNTER++ ))
#This done command ends the loop	
done
# Prints statement to the screen
echo "im finished"

###################################################
#until loop
#declaring variable
counter=0
#imtil command. until counter gets to 15 it will do what the do command tells it to do
until [ $counter -gt 15 ]
# do command.
do
	echo Counting until 15 and then I will stop: $counter
	((counter++))
done


