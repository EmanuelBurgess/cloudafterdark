#!/bin/bash
# Bash script to automate deleting s3 bucket
#command to list buckets
sudo aws s3 ls
echo "What bucket would you like to delete"
#read command allows user to input bucket name and declares the bucket name as a variable
read bucket
# command to delete s3 bucket. Using variable 
sudo aws s3 rb s3://$bucket 
#list buckets to verify bucket has been removed
sudo aws s3 ls

