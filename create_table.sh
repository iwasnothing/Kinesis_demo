#!/bin/sh

#aws dynamodb create-table --table-name Counting --attribute-definitions AttributeName=Queue,AttributeType=S AttributeName=OrderCnt,AttributeType=N --key-schema AttributeName=Queue,KeyType=HASH --provisioned-throughput ReadCapacityUnits=10,WriteCapacityUnits=10 --global-secondary-indexes IndexName=SortCntIndex,KeySchema=["{AttributeName=Queue,KeyType=HASH}","{AttributeName=OrderCnt,KeyType=RANGE}"],Projection="{ProjectionType=ALL}",ProvisionedThroughput="{ReadCapacityUnits=10,WriteCapacityUnits=10}"


#ResponeTime {Queue,OrderCnt,TotalTime,AvgTime}
#aws dynamodb create-table --table-name ResponseTime --attribute-definitions AttributeName=Queue,AttributeType=S AttributeName=AvgTime,AttributeType=N --key-schema AttributeName=Queue,KeyType=HASH --provisioned-throughput ReadCapacityUnits=10,WriteCapacityUnits=10 --global-secondary-indexes IndexName=SortAvgIndex,KeySchema=["{AttributeName=Queue,KeyType=HASH}","{AttributeName=AvgTime,KeyType=RANGE}"],Projection="{ProjectionType=ALL}",ProvisionedThroughput="{ReadCapacityUnits=10,WriteCapacityUnits=10}"

#Price {Queue,OrderCnt,TotalPrice,AvgPrice}
#aws dynamodb create-table --table-name Price --attribute-definitions AttributeName=Queue,AttributeType=S AttributeName=AvgPrice,AttributeType=N --key-schema AttributeName=Queue,KeyType=HASH --provisioned-throughput ReadCapacityUnits=10,WriteCapacityUnits=10 --global-secondary-indexes IndexName=SortAvgIndex,KeySchema=["{AttributeName=Queue,KeyType=HASH}","{AttributeName=AvgPrice,KeyType=RANGE}"],Projection="{ProjectionType=ALL}",ProvisionedThroughput="{ReadCapacityUnits=10,WriteCapacityUnits=10}"

#Metric {Metric,Queue,OrderCnt,Total,Avg}
aws dynamodb create-table --table-name Metric --attribute-definitions AttributeName=Metric,AttributeType=S AttributeName=Queue,AttributeType=S AttributeName=AvgVal,AttributeType=N --key-schema AttributeName=Metric,KeyType=HASH AttributeName=Queue,KeyType=RANGE --provisioned-throughput ReadCapacityUnits=10,WriteCapacityUnits=10 --global-secondary-indexes IndexName=SortAvgIndex,KeySchema=["{AttributeName=Metric,KeyType=HASH}","{AttributeName=AvgVal,KeyType=RANGE}"],Projection="{ProjectionType=ALL}",ProvisionedThroughput="{ReadCapacityUnits=10,WriteCapacityUnits=10}"

aws dynamodb create-table --table-name PickupLocation --attribute-definitions AttributeName=Queue,AttributeType=S AttributeName=Region,AttributeType=S AttributeName=OrderCnt,AttributeType=N --key-schema AttributeName=Queue,KeyType=HASH AttributeName=Region,KeyType=RANGE --provisioned-throughput ReadCapacityUnits=10,WriteCapacityUnits=10 --global-secondary-indexes IndexName=SortCntIndex,KeySchema=["{AttributeName=Queue,KeyType=HASH}","{AttributeName=OrderCnt,KeyType=RANGE}"],Projection="{ProjectionType=ALL}",ProvisionedThroughput="{ReadCapacityUnits=10,WriteCapacityUnits=10}"
