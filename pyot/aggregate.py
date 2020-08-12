from pyspark.sql import DataFrame
from pyspark.sql.functions import col, from_json, window
from pyot import schema


def create_averaged_df(raw_streaming_df: DataFrame, window_sec: int,
                       watermark_sec: int) -> DataFrame:
    """
    Returns streaming DataFrame including window_sec average sensor data
    grouped by IoT Hub device id

    Parameters
    ----------
    raw_streaming_df: DataFrame
        raw streaming data frame injested from event hubs
    window_sec: int
        window time (seconds) for aggregation
    watermark_sec: int
        watermark time (seconds) for keeping window data

    Returns
    -------
    aggregated_df: DataFrame
        DataFrame including aggregated sensor data
    """

    # Apply schema for later phase
    schemaed_df = raw_streaming_df \
        .withColumn("body", from_json("body", schema.basic_sensor)) \
        .withColumn("temperature", col("body.temperature")) \
        .withColumn("humidity", col("body.humidity")) \
        .withColumn("deviceid",
                    col("systemProperties.iothub-connection-device-id")) \
        .withColumn("enqueuedTime", col("enqueuedTime").cast("timestamp")) \
        .drop("body")

    aggregated_df = schemaed_df \
        .withWatermark("enqueuedTime", f"{watermark_sec} seconds") \
        .groupBy(window("enqueuedTime", f"{window_sec} seconds"), "deviceid") \
        .avg("temperature", "humidity") \
        .withColumn("start", col("window.start"))

    return aggregated_df
