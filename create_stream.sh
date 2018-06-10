#!/bin/sh

list="create_order assign_driver complete_order"
for q in $list ; do
	echo $q
	aws kinesis create-stream --stream-name $q  --shard-count 2
done
