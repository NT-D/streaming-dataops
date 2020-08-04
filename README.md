TODO: 
- Documentation
    - Update repository problem statement (motivation) and goal.
    - Add architecutre diagram
- Add Unit test
- Add CI/CD pipeline with DataBricks CLI
- Monitor streaming and alert to admin team whenever streaming job fail

# streaming-dataops
- Sample repo for understanding spark structured streaming and data ops with DataBricks and Azure IoT tools
- You can utilize device simulator in my [GitHub](https://github.com/NT-D/streaming-dataops-device). It can send expected telemetry to IoT Hub and Spark.
- This repo uses [Azure Event Hubs Connector for Apache Spark](https://github.com/Azure/azure-event-hubs-spark) instead of Kafka Connector, because it supports Azure IoT Hubs message property. See more detail in [this blog](https://medium.com/@masayukiota/comparison-kafka-or-event-hubs-connector-to-consume-streaming-data-from-databricks-in-iot-scenario-5053a3d85f4f).

## How to run app
1. If you are new for developing inside a container, please read [this document](https://code.visualstudio.com/docs/remote/containers) and setup environment by refering [Getting started](https://code.visualstudio.com/docs/remote/containers#_getting-started).
1. Clone and open repository inside the container with [this document](https://code.visualstudio.com/docs/remote/containers#_quick-start-open-a-git-repository-or-github-pr-in-an-isolated-container-volume).
1. Set environment variable with event hub (IoT Hub) information
```shell
export EVENTHUB_CONNECTION_STRING="{Your event hub connection string}"
export EVENTHUB_CONSUMER_GROUP="{Your consumer group name}"
```
4. Run `pyspark --packages com.microsoft.azure:azure-eventhubs-spark_2.11:2.3.16 < stream_app.py` in Visual Studio Code terminal to execute structred streaming. It shows telemetry in console.

### environment variable example
|Name|Example|IoT Hub Build-in endpoints name|
|--|--|--|
|EVENTHUB_CONNECTION_STRING|`Endpoint=sb://xxx.servicebus.windows.net/;  SharedAccessKeyName=xxxxx;SharedAccessKey=xxx;EntityPath=xxxx`|Event Hub-compatible endpoint|
|EVENTHUB_CONSUMER_GROUP|Consume group name which you created. Default is `$Default`|Consumer Groups|

- Uses `xxx` for mocking secrets
- Please refer 3rd column to pick up connection setting from Azure IoT Hub's [built-in endpoint](https://docs.microsoft.com/en-us/azure/iot-hub/iot-hub-devguide-messages-read-builtin)

## Deploy library to Azure DataBricks
I'll update this section, because I want to automate it with CI/CD pipeline. Currently I note manual steps for future CI/CD development.

### Build the python package
1. Run `python setup.py sdist bdist_wheel`

### Publish the package to the Azure DataBricks
1. [Setup DataBricks CLI](https://docs.databricks.com/dev-tools/cli/index.html)
1. Run `dbfs mkdirs dbfs:/FileStore/whls` to make library folder in DBFS (DataBricks File System)
1. Run `dbfs cp "{Your code path}/streaming-dataops/dist/pyot-0.0.1-py3-none-any.whl" dbfs:/FileStore/whls`
1. Run `databricks clusters list` to see cluster id
1. Run `databricks clusters start --cluster-id {Your cluster id}` to start your cluster
1. Install own python library by runnning `databricks libraries install --cluster-id {Your cluster id} --whl "dbfs:/FileStore/whls/pyot-0.0.1-py3-none-any.whl"`


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

### Build and publish python package
- [Packaging Python Projects](https://packaging.python.org/tutorials/packaging-projects/)
- [Libraries CLI](https://docs.microsoft.com/en-us/azure/databricks/dev-tools/cli/libraries-cli)