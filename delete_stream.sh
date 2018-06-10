#!/bin/sh

list="create_order assign_driver complete_order"
for q in $list ; do
	echo $q
	aws kinesis delete-stream --stream-name $q  
done
