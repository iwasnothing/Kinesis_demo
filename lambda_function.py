import base64
import json
import boto3
import datetime
import logging
import decimal
import os

def updateRegion(dynamo_db,q,reg):
	logger = logging.getLogger()
	logger.setLevel(logging.INFO)
	pickup_table = dynamo_db.Table('PickupLocation')
	#logger.info(reg)
	try:
		response = pickup_table.get_item(Key={
			'Queue': q,
			'Region': reg
		})
	except Exception as e:
		#logger.info("fail get reg")
		#logger.info(e)
		response={}
	if 'Item' not in response:
		#logger.info("create reg")
		response = pickup_table.put_item(
			Item={
				'Queue': 'create_order',
				'Region': reg,
				'OrderCnt': 1
			}
		)
	else:	
		#logger.info("update reg")
		try:
			response = pickup_table.update_item(
			Key={
				'Queue': q,
				'Region': reg,
			},
			UpdateExpression="set OrderCnt = OrderCnt + :val",
			ExpressionAttributeValues={
				':val': decimal.Decimal(1)
			},
			ReturnValues="UPDATED_NEW"
			)
			#logger.info(response)
		except Exception as e:
			logger.info("fail inc reg")
			logger.info(e)
		
def updateAvg(dynamo_db,q,metric,value):
	logger = logging.getLogger()
	logger.setLevel(logging.INFO)
	table = dynamo_db.Table('Metric')
	#logger.info(metric)
	try:
		response = table.get_item(Key={
			'Metric': metric,	
			'Queue': q
		})
		print(response)
	except Exception as e:
		logger.info("fail get avg")
		logger.info(e)
		response={}
	if 'Item' not in response:
		#logger.info("create item")
		response = table.put_item(
			Item={
				'Metric': metric,	
				'Queue': q,
				'OrderCnt': 1,
				'TotalVal': value,
				'AvgVal': value
			}
		)
	
	else:
		item = response['Item']
		print("GetItem succeeded:")
		tot = item['TotalVal']
		cnt = item['OrderCnt']
		a = (tot + value)/(cnt+1)
		try:
			response = table.update_item(
			Key={
				'Metric': metric,	
				'Queue': q,
			},
			UpdateExpression="set OrderCnt = OrderCnt + :one, TotalVal = TotalVal + :val, AvgVal = :avgval ",
			ExpressionAttributeValues={
				':one': decimal.Decimal(1),
				':val': decimal.Decimal(value),
				':avgval': decimal.Decimal(a)
			},
			ReturnValues="UPDATED_NEW"
			)
			#logger.info(response)
		except Exception as e:
			logger.info("fail inc avg")
			logger.info(e)


def minus(dynamo_db,q,metric,value):
	logger = logging.getLogger()
	logger.setLevel(logging.INFO)
	table = dynamo_db.Table('Metric')
	#logger.info(metric)
	try:
		response = table.get_item(Key={
			'Metric': metric,	
			'Queue': q
		})
	except :
		logger.info("no item")
	
	else:
		item = response['Item']
		print("GetItem succeeded:")
		tot = item['TotalVal']
		cnt = item['OrderCnt']
		a = (tot - value)/(cnt-1)
		try:
			response = table.update_item(
			Key={
				'Metric': metric,	
				'Queue': q,
			},
			UpdateExpression="set OrderCnt = OrderCnt - :one, TotalVal = TotalVal - :val, AvgVal = :avgval ",
			ExpressionAttributeValues={
				':one': decimal.Decimal(1),
				':val': decimal.Decimal(value),
				':avgval': decimal.Decimal(a)
			},
			ReturnValues="UPDATED_NEW"
			)
			#logger.info(response)
		except:
			logger.info("fail minus avg")

		

def lambda_handler(event, context):
	"""
	Receive a batch of events from Kinesis and insert as-is into our DynamoDB table if invoked asynchronously,
	otherwise perform an asynchronous invocation of this Lambda and immediately return
	"""
	if not event.get('async'):
		invoke_self_async(event, context)
		return

	logger = logging.getLogger()
	logger.setLevel(logging.INFO)
	print('Received request')
	logger = logging.getLogger()
	logger.setLevel(logging.INFO)
	#logger.info('get req')
	item = None
	dynamo_db = boto3.resource('dynamodb')
	decoded_record_data = [base64.b64decode(record['kinesis']['data']) for record in event['Records']]
	deserialized_data = [json.loads(decoded_record) for decoded_record in decoded_record_data]

	for item in deserialized_data:
		
		q = os.getenv('QUEUE', 'create_order')
		#logger.info(q)
		#create_order
		if q == 'create_order':
			#logger.info("count throughput")
			updateAvg(dynamo_db,q,'Throughput',1)
			#logger.info("count qlen")
			updateAvg(dynamo_db,q,'QLen',1)
			reg = item['ship_from_region']
			updateRegion(dynamo_db,q,reg)

			price = item['price']
			#logger.info("count price")
			updateAvg(dynamo_db,q,'Price',price)

		#assign_driver
		if q == 'assign_driver':
			#logger.info("count throughput")
			updateAvg(dynamo_db,q,'Throughput',1)
			updateAvg(dynamo_db,q,'QLen',1)
			time = item['assign_time_taken']
			#logger.info("count assign time")
			updateAvg(dynamo_db,q,'Assign_Time',time)
			q = 'create_order'
			minus(dynamo_db,q,'QLen',1)
			minus(dynamo_db,q,'Price',price)

		#complete_order
		if q == 'complete_order':
			#logger.info("count throughput")
			updateAvg(dynamo_db,q,'Throughput',1)
			time = item['complete_time_taken']
			#logger.info("count assign time")
			updateAvg(dynamo_db,q,'Complete_Time',time)
			price = item['price']
			#logger.info("count price")
			updateAvg(dynamo_db,q,'Price',price)
			q = 'assign_driver'
			minus(dynamo_db,q,'QLen',1)



def invoke_self_async(event, context):
	"""
	Have the Lambda invoke itself asynchronously, passing the same event it received originally,
	and tagging the event as 'async' so it's actually processed
	"""
	event['async'] = True
	called_function = context.invoked_function_arn
	boto3.client('lambda').invoke(
	FunctionName=called_function,
	InvocationType='Event',
	Payload=bytes(json.dumps(event), 'utf8')
	)



