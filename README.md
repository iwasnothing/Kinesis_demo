This is a demo of AWS Kinesis for the logistsic system event streaming.  There are 3 events:
1. event: order_created, data: order id, ship from region, ship to region, pick up time, price
2. event: order_assigned, data: order id, driver (who accepted the order)
3. event: order_completed, data: order id,

We created 3 Kinesis Streams by the script (create_stream.sh).  Each stream has 2 shards.  The simulator.py will create 2 threads for producer to create order, and then 2 threads to consumer the event message and then forward to the 2nd stream (assign_driver).  It will set a random time for the driver assignment time taken for simulation.  And then there will also be 2 threads to receive the event and forward to the final queue (complete_order)

Each consumer thread will print out its own message througput.

We also created 3 lambda functions (create_lambda.sh/lamda_function.py) to listen the Kinesis event to analyse the statistics: price, ship_from_region, and time taken. The function will update the statistics into DynamoDB.  The tables was created by (create_table.sh).  And the statistics will be shown by (monitor.py).

