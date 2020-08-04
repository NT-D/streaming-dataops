from pyspark.sql.functions import col, from_json, window
from pyot import schema


def create_averaged_df(raw_streaming_df, window_sec, watermark_sec):
    # Apply schema for later phase
    schemaed_df = raw_streaming_df \
        .withColumn("body", from_json("body", schema.basic_sensor)) \
        .withColumn("temperature", col("body.temperature")) \
        .withColumn("humidity", col("body.humidity")) \
        .withColumn("deviceid", col("systemProperties.iothub-connection-device-id")) \
        .withColumn("enqueuedTime", col("enqueuedTime").cast("timestamp")) \
        .drop("body")

    aggregated_df = schemaed_df \
        .withWatermark("enqueuedTime", f"{watermark_sec} seconds") \
        .groupBy(window("enqueuedTime", f"{window_sec} seconds"), "deviceid") \
        .avg("temperature", "humidity") \
        .withColumn("start", col("window.start"))

    return aggregated_df
