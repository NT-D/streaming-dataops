import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import StructType, StructField, DoubleType

# Initialize spark env
# spark = SparkSession.builder.master('local').getOrCreate()
spark = SparkSession.builder.appName('StructredStreamingApp').getOrCreate()

# Azure setting information
EVENTHUB_CONNECTION_STRING = os.getenv('EVENTHUB_CONNECTION_STRING')
EVENTHUB_NAMESPACE = os.getenv('EVENTHUB_NAMESPACE')
EVENT_HUB_NAME = os.getenv('EVENT_HUB_NAME') # same as kafka topic

# Kafka stream settings
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
