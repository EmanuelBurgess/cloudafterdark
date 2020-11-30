#!/bin/bash
#best player is my variable
bestplayer="Jordan"
# This is my if statement. Notice space after first bracket and before 2nd bracket
if [ $bestplayer = "Lebron" ]
# next is my then statement. Tells scrupt what to do.
then
	        echo $bestplayer is not even close to being better than MJ
# next is the else statment, meaning "or else do" this  
else
	        echo  $bestplayer is the GOAT

fi
