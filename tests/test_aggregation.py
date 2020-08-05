import pytest
from pyot import schema, aggregate


# Const
file_location = './tests/data/aggregation'
spark_partition_num = 1  # Set 1 because local spark doesn't have much resource
window_sec = 5  # Time window
termination_time = 10
stream_name = "input_stream"


@pytest.fixture
def spark():
    from pyspark.sql import SparkSession
    spark = SparkSession.builder.appName('StructredStreamingApp').getOrCreate()
    return spark


def test_aggregate_sensordata(spark):
    # Write data in the console
    initialDF = (spark
                 .readStream
                 .option("maxFilesPerTrigger", 1)
                 .schema(schema.eventhub_schema)
                 .json(file_location)
                 )

    aggregated_result = aggregate.create_averaged_df(initialDF, window_sec,
                                                     termination_time)

    spark.conf.set("spark.sql.shuffle.partitions", spark_partition_num)
    stream = (aggregated_result
              .writeStream
              .queryName(stream_name)
              .outputMode('complete')
              .format('memory')
              .start()
              )

    # TODO: Want to terminate immediatelly after reading all test files
    # without fixed param
    stream.awaitTermination(termination_time)
    result = spark.sql("select count(*) as count from input_stream")

    assert aggregated_result.isStreaming
    # test data has 30 sec duration
    assert result.first()["count"] == 30 / window_sec
