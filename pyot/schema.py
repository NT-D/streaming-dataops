from pyspark.sql.types import StructType, StructField, DoubleType, StringType

# Set and apply schema
# Created simulator device in another repo
# It sends random temperature and humidity to IoT Hub
# https://github.com/NT-D/streaming-dataops-device/blob/master/simulator.py
# This part uses same schema with the repository.
basic_sensor = StructType([
    StructField("temperature", DoubleType(), False),
    StructField("humidity", DoubleType(), False)
])


# Use for test logics
eventhub_schema = StructType([
    StructField("body", StringType(), True),
    StructField("partition", StringType(), True),
    StructField("offset", StringType(), True),
    StructField("sequenceNumber", StringType(), True),
    StructField("enqueuedTime", StringType(), True),
    StructField("properties", StructType([]), True),
    StructField("systemProperties", StructType([
        StructField("iothub-enqueuedtime", StringType(), True),
        StructField("iothub-connection-auth-method", StringType(), True),
        StructField("iothub-connection-auth-generation-id", StringType(),
                    True),
        StructField("iothub-connection-device-id", StringType(), True),
        StructField("iothub-message-source", StringType(), True)
    ]), True)
])
