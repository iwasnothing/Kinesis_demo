#!/bin/sh

list="PickupLocation Metric"
for tab in $list ; do
	aws dynamodb  delete-table --table-name $tab
done
