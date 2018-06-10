#!/bin/sh

list=`aws lambda list-event-source-mappings|grep UUID|awk  '{print $2}'|awk -F, '{print $1}'|sed -e "s/\"//g"`

for e in $list ; do
	aws lambda delete-event-source-mapping --uuid $e
done

list="create_order assign_driver complete_order"
for q in $list ; do
	echo $q
	aws lambda delete-function --function-name analyse_$q
done

