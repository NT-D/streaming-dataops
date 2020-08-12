# lint_ignore=E501
from pyspark.sql.functions import col


def create_eventhub_streamdf(spark, connection_string, consumer_group):
    """Read eventhub stream and return raw data stream"""
    if connection_string is None or consumer_group is None:
        raise ValueError

    encrypted_string = spark._jvm.org.apache.spark \
        .eventhubs.EventHubsUtils.encrypt(connection_string)
    event_hub_config = {
        "eventhubs.connectionString": encrypted_string,
        "eventhubs.consumerGroup": consumer_group
    }

    raw_streaming_df = (spark
                        .readStream
                        .format("eventhubs")
                        .options(**event_hub_config)
                        .load()
                        .withColumn("body", col("body").cast("string"))
                        )

    return raw_streaming_df
