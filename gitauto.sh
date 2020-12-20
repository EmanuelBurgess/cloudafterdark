#!/bin/bash
#writing script to automate pushing to git

# setting enviromental variable
branch=$1
fname=$2
commitmsg=$3


git checkout -b $branch


git add $fname
git status 
git commit -m "$commitmsg"
git push
sudo git push --set-upstream origin $branch


