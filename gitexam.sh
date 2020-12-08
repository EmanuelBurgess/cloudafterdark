#!/bin/bash

echo What is git? GIT is a cloud based Repository and version control system that allows collaboration among users. 

echo What is github? github is a platform that works with GIT. GIT is where users manage their local repository. 

echo What is a pull request? A pull request is feature of github that allows a user to make changes in their
echo code. Once the changes are made the user creates a pull request, which alerts another user to review
echo the changes made to the code.

echo What is the name of the github file that holds the names of all the people who can review a pull request?

echo How do I check if my files are tracked or untracked "(in the staging area / not in the staging area)"? git status

echo What command do I use to comment on my changes? git commit -m

echo How can I see the git log? git log

echo What is a commit hash? An id number assigned to each commit that allows you to revert back to a version
echo of the code that worked before changes were made

echo What command do I use to get my changes locally to the repo? git clone filename

echo What is a feature branch? Allows you to make changes to code and have it reviewed, before it is merged to main branch

echo What command do I run to check my current branch? git branch -a

echo What command do I run to create a feature branch? git checkout -b branchname

echo What command do I run to show all branches? git branch - a

echo What command do I run to make sure my local repo has all the changes as the remote repo? git push

echo How do I decide what to name the feature branch? Use the name of your Jira task

echo What is the name of the file that holds my git credentials "( like username and email address)"?.git/config

echo What commands do I run to configure git on my local machine "( username and password )"?
echo git config --global user.name tmahone / git config use.email mahoneandson55@aol.com
echo What command do I run to add all of the untracked files to the staging area? git add .
