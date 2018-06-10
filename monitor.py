import base64
import json
import boto3
import datetime
import logging
import decimal
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
import sys
import time

def get_count(tab,q,m):
	dynamo_db = boto3.resource('dynamodb')
	table = dynamo_db.Table(tab)
	try:
		response = table.get_item(
			Key={
			'Queue': q, 'Metric': m,
			}
		)
	except ClientError as e:
		print(e.response['Error']['Message'])
		a0 = -1
		return
	if 'Item' in response:
		item = response['Item']
		#print("GetItem succeeded:")
		a0 = item['TotalVal']
		a1 = item['OrderCnt']

	return (a0,a1)

print("top 3")
dynamo_db = boto3.resource('dynamodb')
table = dynamo_db.Table('PickupLocation')
response = table.query(IndexName='SortCntIndex',KeyConditionExpression=Key('Queue').eq("create_order"),Limit=3,ScanIndexForward=False)
print(response['Items'])

q='create_order'
print(q)
m='Price'
(tot,n)=get_count('Metric',q,m)
print("avg price = " + str(tot/n) )

q='assign_driver'
m='Assign_Time'
(tot,n)=get_count('Metric',q,m)
print("avg assign time = " + str(tot/n) )
q='complete_order'
m='Complete_Time'
(tot,n)=get_count('Metric',q,m)
print("avg complete time = " + str(tot/n) )
m='Price'
(tot,n)=get_count('Metric',q,m)
print("avg price = " + str(tot/n) )

qlist=["create_order", "assign_driver"]
for q in qlist:
	print(q)
	#def get_count(tab,q,m):
	#m='Throughput'
	#(tot,n)=get_count('Metric',q,m)
	#prev = tot
	#print("total count = " + str(tot) + " " + str(n) )
	#time.sleep(10)
	#(tot,n)=get_count('Metric',q,m)
	#print("total count = " + str(tot) + " " + str(n) )
	#print("tps = " + str( (tot-prev) ))
	m='QLen'
	(tot,n)=get_count('Metric',q,m)
	print("qlen count = " + str(tot) )

