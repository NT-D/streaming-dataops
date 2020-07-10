TODO: 
- Documentation
    - Update repository problem statement (motivation) and goal.
    - Add architecutre diagram
- Add Unit test
- Add CI/CD pipeline including submit spark jobs
- Monitor streaming and alert to admin team whenever streaming job fail

# streaming-dataops
- Sample repo for understanding spark structured streaming and data ops
- You can utilize device simulator in my [GitHub](https://github.com/NT-D/streaming-dataops-device). It can send expected telemetry to IoT Hub and Spark.

## How to run app
1. If you are new for developing inside a container, please read [this document](https://code.visualstudio.com/docs/remote/containers) and setup environment by refering [Getting started](https://code.visualstudio.com/docs/remote/containers#_getting-started).
1. Clone and open repository inside the container with [this document](https://code.visualstudio.com/docs/remote/containers#_quick-start-open-a-git-repository-or-github-pr-in-an-isolated-container-volume).
1. Set environment variable with event hub (IoT Hub) information
```shell
export EVENTHUB_CONNECTION_STRING="{Your event hub connection string}"
export EVENTHUB_NAMESPACE="{Your event hub name space}"
export EVENT_HUB_NAME="{Your event hub name}"
```
4. Run `pyspark --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.0 < stream_app.py` in Visual Studio Code terminal to execute structred streaming. It shows telemetry in console.

### environment variable example
|Name|Example|IoT Hub Build-in endpoints name|
|--|--|--|
|EVENTHUB_CONNECTION_STRING|`Endpoint=sb://xxx.servicebus.windows.net/;  SharedAccessKeyName=xxxxx;SharedAccessKey=xxx;EntityPath=xxxx`|Event Hub-compatible endpoint|
|EVENTHUB_NAMESPACE|`xxxx.servicebus.windows.net`|Pick up from `Event Hub-compatible endpoint string`|
|EVENT_HUB_NAME|Unique event hub name such as `streaming-ops-masota`|Event Hub-compatible name|

- Uses `xxx` for mocking secrets
- If you use Azure IoT Hubs, please refer 3rd column to pick up connection setting from [built-in endpoint](https://docs.microsoft.com/en-us/azure/iot-hub/iot-hub-devguide-messages-read-builtin)


## Reference
### DataOps strategy
For understanding concept of this repo, please read following repo and blog
- [DataOps for the Modern Data Warehouse](https://github.com/Azure-Samples/modern-data-warehouse-dataops)
- [Spark Streaming part 3: DevOps, tools and tests for Spark applications](https://www.adaltas.com/en/2019/06/19/spark-devops-tools-test/)

### Spark structured streaming and Azure Event Hubs
- [Connect your Apache Spark application with Azure Event Hubs](https://docs.microsoft.com/en-us/azure/event-hubs/event-hubs-kafka-spark-tutorial)
- [Structured Streaming + Kafka Integration Guide (Kafka broker version 0.10.0 or higher)](https://spark.apache.org/docs/latest/structured-streaming-kafka-integration.html)
- [Structured Streaming Programming Guide](http://spark.apache.org/docs/latest/structured-streaming-programming-guide.html)

### Setup development environment
- [Update vscode setting for resolving pyspark import error problem](https://stackoverflow.com/questions/40163106/cannot-find-col-function-in-pyspark)
