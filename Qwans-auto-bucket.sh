#!/bin/bash
Names='allfallsdown manonthemoon upupandaway'
for N in $Names 
do
echo "making buckets" 
aws s3 mb s3://$N 
done 
