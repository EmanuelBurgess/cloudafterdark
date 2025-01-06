#!/bin/bash

BUCKETS="todayissunday tomorrowismonday thedayafteristuesday"

for x in $BUCKETS
do
aws s3 mb s3://$x
done
