import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pyot import schema
from pyot import connector

# Initialize spark env
# spark = SparkSession.builder.master('local').getOrCreate()
spark = SparkSession.builder.appName('StructredStreamingApp').getOrCreate()

# Get Azure setting information from environmental variable
EVENTHUB_CONNECTION_STRING = os.getenv('EVENTHUB_CONNECTION_STRING')
EVENTHUB_CONSUMER_GROUP = os.getenv('EVENTHUB_CONSUMER_GROUP')
if type(EVENTHUB_CONSUMER_GROUP) is not str:
    EVENTHUB_CONSUMER_GROUP = "$Default"

# Connect and get streaming data frame
raw_streaming_df = connector.create_eventhub_streamdf(
    spark,
    EVENTHUB_CONNECTION_STRING,
    EVENTHUB_CONSUMER_GROUP
)

# Apply schema for later phase
schemaed_df = (raw_streaming_df
               .withColumn("body", from_json("body", schema.basic_sensor))
               .withColumn("temperature", col("body.temperature"))
               .withColumn("humidity", col("body.humidity"))
               .withColumn("deviceid", col("systemProperties.iothub-connection-device-id"))
               .drop("body")
               )

# Write data in the console
try:
    stream = (schemaed_df
              .writeStream
              .outputMode('append')
              .format('console')
              .start()
              )
    stream.awaitTermination()

except KeyboardInterrupt:
    print("Streaming is terminated by user input")

except Exception:
    # If the query has terminated with an exception, exception will be thrown.
    # Can write code for sending alert/email to IT admin to know
    print("Streaming is terminated by exception")
