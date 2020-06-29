from pyspark.sql import SparkSession, Row
from pyspark.sql.functions import col

# Initialize spark env
spark = SparkSession.builder.master('local').getOrCreate()

# Define data schema, then set data
user_row = Row('birth','age','is_fan')

data = [
    user_row('1990-01-01', 29, True),
    user_row('2000-10-02', 19, False)
]

user_df = spark.createDataFrame(data)
user_df.show()

filtered_userdf = user_df.filter(col('is_fan') == True)
filtered_userdf.show()