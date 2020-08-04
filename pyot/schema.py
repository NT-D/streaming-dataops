from pyspark.sql.types import StructType, StructField, DoubleType

# Set and apply schema
# Created simulator device in another repo
# It sends random temperature and humidity to IoT Hub
# https://github.com/NT-D/streaming-dataops-device/blob/master/simulator.py
# This part uses same schema with the repository.
basic_sensor = StructType([
    StructField("temperature", DoubleType(), False),
    StructField("humidity", DoubleType(), False)
])
