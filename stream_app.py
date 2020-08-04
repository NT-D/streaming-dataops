import os
from pyspark.sql import SparkSession
from pyot import connector, aggregate


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

aggregated_df = aggregate.create_averaged_df(raw_streaming_df, 30, 60)

# Write data in the console
try:
    stream = (aggregated_df
              .writeStream
              .outputMode('append')
              .format('console')
              .start()
              )
    stream.awaitTermination()
    
except KeyboardInterrupt:
    print("Streaming is terminated by user input")
