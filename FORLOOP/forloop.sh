#!/bin/bash


BUCKETS='jerry12345991 newuser12323023921 newuser08098709870 newuser000023023'

for x in $BUCKETS
do
aws s3 mb s3://$x
done


