#!/bin/bash

# We are using the read command. It allows you to manually input text and that text is stored ad a variable that can be reused within your script

echo "Who is the best player"
read bestplayer

echo "you stated the best player is $bestplayer"

# This is my if statement. Notice space after first bracket and before 2nd bracket
# An if statement make a decision whther a specifc line of code should be ran or not.  Here we see that is the variable best player is Jordan then the condition is true and it will execute the command after "then"
#If it is not ture then it will execute the code after "else"


if [ $bestplayer = "Jordan" ]
# next is my then statement. Tells scrupt what to do.
	then
echo "$bestplayer is the best"
# next is the else statment, meaning "or else do" this
	else
echo "$bestplayer is not the GOAT Jordan is"

fi


