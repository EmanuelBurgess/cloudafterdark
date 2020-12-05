#1/bin/bash

#creating this script tp create IAM user in AWS
# creating enviromental vairable. When script is ran this will be the first argument
#this is will be the group name.
group=$1
# Policy for group
policy=$2
# uset name
usrname=$3
# AWS CLI commands
aws iam create-group --group-name $group
aws iam list-attached-group-policies --group-name $policy
aws iam create-user --user-name $usrname
aws iam add-user-to-group --user-name $usrname --group-name $group

