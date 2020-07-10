import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import StructType, StructField, DoubleType

# Initialize spark env
# spark = SparkSession.builder.master('local').getOrCreate()
spark = SparkSession.builder.appName('StructredStreamingApp').getOrCreate()

# Get Azure setting information from environmental variable
EVENTHUB_CONNECTION_STRING = os.getenv('EVENTHUB_CONNECTION_STRING')
EVENTHUB_NAMESPACE = os.getenv('EVENTHUB_NAMESPACE')
EVENT_HUB_NAME = os.getenv('EVENT_HUB_NAME') # same as kafka topic

# Connect IoT Hub from Spark
# IoT Hub has Event Hub compatible build-in endpoint. Event Hub is compatible with Kafka.
# Use Kafka connector in this repo because developers sometimes want to use Kafka in the onpremises.
EH_SASL = f'org.apache.kafka.common.security.plain.PlainLoginModule required \
    username="$ConnectionString" password="{EVENTHUB_CONNECTION_STRING}";'
BOOTSTRAP_SERVERS = f'{EVENTHUB_NAMESPACE}:9093'

rowStreamDf = spark.readStream \
    .format("kafka") \
    .option("kafka.sasl.mechanism", "PLAIN") \
    .option("kafka.security.protocol", "SASL_SSL") \
    .option("kafka.sasl.jaas.config", EH_SASL) \
    .option("kafka.bootstrap.servers", BOOTSTRAP_SERVERS) \
    .option("subscribe", EVENT_HUB_NAME) \
    .load() \
    .select(col("value").cast("STRING"))

# Set and apply schema
# Created simulator device in another repo and send random temperature and humidity to IoT Hub
# https://github.com/NT-D/streaming-dataops-device/blob/master/simulator.py
# This part uses same schema with the repository.
schema = StructType([
    StructField("temperature", DoubleType(), True),
    StructField("humidity", DoubleType(), True)
])

schemaedStreamDf = rowStreamDf.select(from_json("value", schema).alias("json")) \
    .select(col("json.temperature").alias("temperature"),
            col("json.humidity").alias("humidity") \
    )

# Write data in the console
stream = schemaedStreamDf.writeStream.outputMode('append').format('console').start()
stream.awaitTermination()
