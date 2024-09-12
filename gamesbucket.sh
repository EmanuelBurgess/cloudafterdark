#!/bin/bash
games="gdepo gprod gdev gusers"
for g in $games
do
echo 'making buckets in progress...' 
sleep 3
aws s3 mb s3://$g
done 
