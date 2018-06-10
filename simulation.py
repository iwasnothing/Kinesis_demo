import boto3
import json
from datetime import datetime
import time
import threading
import calendar
import random
import uuid
from joblib import Parallel, delayed
import sys
import numpy as np

def complete_msg(final_stream_name ,  shd):
	begin = calendar.timegm(datetime.utcnow().timetuple())
	total = 0
	#my_shard_id = response['StreamDescription']['Shards'][shd]['ShardId']
	my_shard_id = shd['ShardId']
	print(my_shard_id + "-->" + "hello")
	print(shd)


	
	while True:
		shard_iterator = kinesis_client.get_shard_iterator(StreamName=my_stream_name, ShardId=my_shard_id, ShardIteratorType='LATEST')
		while ( 'ShardIterator' not in shard_iterator):
			shard_iterator = kinesis_client.get_shard_iterator(StreamName=my_stream_name, ShardId=my_shard_id, ShardIteratorType='LATEST')
			
		my_shard_iterator = shard_iterator['ShardIterator']
		print(my_shard_id + "-->" + "loop")
		record_response = kinesis_client.get_records(ShardIterator=my_shard_iterator, Limit=100)
		time.sleep(0.001)
		for rec in record_response['Records']:
			#print(rec['Data'])
			jdat = json.loads(rec["Data"])
			print(my_shard_id + "-->" + jdat['ship_from_region'])
			jdat['complete_time_taken'] = int(abs(np.random.normal()*10))
		while 'NextShardIterator' in record_response:
			try:
				record_response = kinesis_client.get_records(ShardIterator=record_response['NextShardIterator'],Limit=100)
				for rec in record_response['Records']:
					total = total + 1
					#print(rec['Data'])
					jdat = json.loads(rec["Data"])
					now = calendar.timegm(datetime.utcnow().timetuple())
					elapse = now - begin
					#print(my_shard_id + "-->" + jdat['ship_from_region']  )
					#print(my_shard_id + "-->" + jdat['pick_up_time']  )
					thrput = total/float(elapse) 
					print(final_stream_name + " " + my_shard_id + " thoughput -->" + str(thrput) )
					#print(jdat)
					thing_id = jdat['order_id']
					#print(put_response)

				time.sleep(0.0001)
			except:
				print("exception")
				pass


def finisher(final_stream_name  ):
	#my_stream_name = 'python-stream'
	threads=[]	
	response = kinesis_client.describe_stream(StreamName=my_stream_name)
	shards = response['StreamDescription']['Shards']
	print(shards)
	n = 0
	for shd in shards:
		n = n + 1
		print(shd)
		print(shd['ShardId'])
		thread0 = threading.Thread(target=complete_msg, args=(final_stream_name,shd) )
		thread0.start()
		threads.append(thread0)
	#Parallel(n_jobs=n)(delayed(get_msg)(my_stream_name , shd) for shd in shards)

	return threads

	
def get_msg(my_stream_name,next_stream_name ,  shd):
	begin = calendar.timegm(datetime.utcnow().timetuple())
	total = 0
	#my_shard_id = response['StreamDescription']['Shards'][shd]['ShardId']
	my_shard_id = shd['ShardId']
	print(my_shard_id + "-->" + "hello")
	print(shd)


	
	while True:
		shard_iterator = kinesis_client.get_shard_iterator(StreamName=my_stream_name, ShardId=my_shard_id, ShardIteratorType='LATEST')
		while ( 'ShardIterator' not in shard_iterator):
			shard_iterator = kinesis_client.get_shard_iterator(StreamName=my_stream_name, ShardId=my_shard_id, ShardIteratorType='LATEST')
			
		my_shard_iterator = shard_iterator['ShardIterator']
		print(my_shard_id + "-->" + "loop")
		record_response = kinesis_client.get_records(ShardIterator=my_shard_iterator, Limit=100)
		time.sleep(0.001)
		for rec in record_response['Records']:
			#print(rec['Data'])
			jdat = json.loads(rec["Data"])
			print(my_shard_id + "-->" + jdat['ship_from_region'])
			jdat['driver'] = "Ah Tong"
			jdat['assign_time_taken'] = int(abs(np.random.normal()*10))
			#print(jdat)
			thing_id = jdat['order_id']
			put_response = kinesis_client.put_record( StreamName=next_stream_name, Data=json.dumps(jdat), PartitionKey=thing_id)
			#print(put_response)
		while 'NextShardIterator' in record_response:
			try:
				record_response = kinesis_client.get_records(ShardIterator=record_response['NextShardIterator'],Limit=100)
				for rec in record_response['Records']:
					total = total + 1
					#print(rec['Data'])
					jdat = json.loads(rec["Data"])
					now = calendar.timegm(datetime.utcnow().timetuple())
					elapse = now - begin
					#print(my_shard_id + "-->" + jdat['ship_from_region']  )
					#print(my_shard_id + "-->" + jdat['pick_up_time']  )
					thrput = total/float(elapse) 
					print(my_stream_name + " " + my_shard_id + " thoughput -->" + str(thrput) )
					# Assign Driver
					if next_stream_name == 'assign_driver':
						#order_assigned, data: order id, driver (who accepted the order)
						jdat['driver'] = "Ah Tong"
						jdat['assign_timestamp'] = str(now)
						#
						#assign_time_taken = now - create_timestamp(property_timestamp), but we use random number as value for simulation
						#
						jdat['assign_time_taken'] = int(abs(np.random.normal()*10+5))
				
					if next_stream_name == 'complete_order':
						#
						#complete_time_taken = now - assign_time, but we use random number as value for simulation
						#
						jdat['complete_time_taken'] = int(abs(np.random.normal()*10+10))
					#print(jdat)
					thing_id = jdat['order_id']
					put_response = kinesis_client.put_record( StreamName=next_stream_name, Data=json.dumps(jdat), PartitionKey=thing_id)
					#print(put_response)

				time.sleep(0.0001)
			except:
				print("exception")
				pass


def consumer(my_stream_name,next_stream_name  ):
	#my_stream_name = 'python-stream'
	threads=[]	
	response = kinesis_client.describe_stream(StreamName=my_stream_name)
	shards = response['StreamDescription']['Shards']
	print(shards)
	n = 0
	for shd in shards:
		n = n + 1
		print(shd)
		print(shd['ShardId'])
		thread0 = threading.Thread(target=get_msg, args=(my_stream_name,next_stream_name,shd) )
		thread0.start()
		threads.append(thread0)
	#Parallel(n_jobs=n)(delayed(get_msg)(my_stream_name , shd) for shd in shards)

	return threads

def producer(my_stream_name,t):
	property_value = 0
	while True:
		property_value = property_value + 1
		property_timestamp = calendar.timegm(datetime.utcnow().timetuple())
		thing_id = str(uuid.uuid4())

		payload = {
			'prop': str(property_value),
			'timestamp': str(property_timestamp),
			'thing_id': thing_id
		}
		rand01 = int(abs(np.random.normal()*10)+8)
		rand02 = int(abs(np.random.normal()*10)+3)
		rand_price = int(abs(np.random.normal()*10)+200)
		region_from = "Region" + str(rand01)
		region_to = "Region" + str(rand02)
		order_created = { "order_id": thing_id , "ship_from_region": region_from, "ship_to_region": region_to, "pick_up_time": str(property_timestamp), "price": rand_price}

		#print(payload)
		put_response = kinesis_client.put_record( StreamName=my_stream_name, Data=json.dumps(order_created), PartitionKey=thing_id)

		#time.sleep(0.001)
		time.sleep(t)


# MAIN


kinesis_client = boto3.client('kinesis', region_name='ap-southeast-1')

stream_list=["create_order", "assign_driver", "complete_order"]

my_stream_name = stream_list[0]
next_stream_name = stream_list[1]
final_stream_name = stream_list[2]

print(my_stream_name)
#order_assigned, data: order id, driver (who accepted the order)
#order_completed, data: order id,

threads=[]
for i in range(2):
	producer_thread0 = threading.Thread(target=producer, args=(my_stream_name,0.001) )
	producer_thread0.start()
	threads.append(producer_thread0)
threads = threads + consumer(my_stream_name,next_stream_name)
threads = threads + consumer(next_stream_name,final_stream_name)
threads = threads + finisher(final_stream_name)
for x in threads:
	x.join()
