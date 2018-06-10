#!/bin/sh

zip lambda.zip lambda_function.py

list="create_order assign_driver complete_order"
for q in $list ; do
	echo $q
	aws lambda create-function \
	--function-name analyse_$q  \
	--zip-file fileb://lambda.zip \
	--role arn:aws:iam::223168353417:role/service-role/KineseWatcher \
	--handler lambda_function.lambda_handler \
	--runtime python3.6 \
	--environment Variables={QUEUE=$q}

	aws lambda create-event-source-mapping \
	--function-name analyse_$q \
	--event-source  arn:aws:kinesis:ap-southeast-1:223168353417:stream/$q \
	--batch-size 100 \
	--starting-position LATEST

done
