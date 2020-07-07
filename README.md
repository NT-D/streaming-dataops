# streaming-dataops
- Sample repo for understanding spark structured streaming and data ops
- You can utilize device simulator in my [GitHub](https://github.com/NT-D/streaming-dataops-device)

## Run app
1. Set environment variable with event hub (IoT Hub) information
```
export EVENTHUB_CONNECTION_STRING="{Your event hub connection string}"
export EVENTHUB_NAMESPACE="{Your event hub name space}"
export EVENT_HUB_NAME="{Your event hub name}"
```
1. Run `pyspark --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.0 < stream_app.py` to execute structred streaming. It shows kafka messages in console.

### environment variable example
Uses `xxx` for mocking secrets
|Name|Example|
|--|--|
|EVENTHUB_CONNECTION_STRING| `Endpoint=sb://xxx.servicebus.windows.net/;SharedAccessKeyName=xxxxx;SharedAccessKey=xxx;EntityPath=xxxx`|
|EVENTHUB_NAMESPACE|`xxxx.servicebus.windows.net`|
|EVENT_HUB_NAME|Unique event hub name such as `streaming-ops-masota`|


## Refer
https://github.com/Azure/azure-event-hubs-for-kafka/tree/master/tutorials/spark#running-spark

Update vscode setting for resolving pyspark import error problem
https://stackoverflow.com/questions/40163106/cannot-find-col-function-in-pyspark

Structured Streaming + Kafka Integration Guide (Kafka broker version 0.10.0 or higher)
https://spark.apache.org/docs/latest/structured-streaming-kafka-integration.html