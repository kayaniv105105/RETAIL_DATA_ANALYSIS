#importing required lib
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *

#initialising the Spark session    
spark = SparkSession.builder.appName("spark-streaming-RetailDataAnalysis").getOrCreate()


# Reading input data from Kafka 
orderRawData = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers","18.211.252.152:9092") \
    .option("subscribe","real-time-project") \
    .option("startingOffsets", "latest")  \
    .load()


# Define Schema
JSON_Schema = StructType() \
    .add("invoice_no", LongType()) \
    .add("country",StringType()) \
    .add("timestamp", TimestampType()) \
    .add("type", StringType()) \
    .add("items", ArrayType(StructType([
        StructField("SKU", StringType()),
        StructField("title", StringType()),
        StructField("unit_price", FloatType()),
        StructField("quantity", IntegerType()) 
        ])))

orderStream = orderRawData.select(from_json(col("value").cast("string"), JSON_Schema).alias("orderdata")).select("orderdata.*")


# Factory function for addition columns to get KPI

#check if the order is new or not
def is_a_order(type):
   return 1 if type == 'ORDER' else 0

#check if order is return type
def is_a_return(type):
   return 1 if type == 'RETURN' else 0
 
# calculate total items in order  
def total_item_count(items):
    if items is not None:
        item_count =0
        for item in items:
            item_count = item_count + item['quantity']
        return item_count   

# calculate total cost of items from order
def total_cost(items,type):
    if items is not None:
        total_cost =0
        item_price =0
    for item in items:
        item_price = (item['quantity']*item['unit_price'])
        total_cost = total_cost+ item_price
        item_price=0

    if type  == 'RETURN':
        return total_cost *-1
    else:
        return total_cost  



# calling the user defined functions as defined above 
agg_isOrder = udf(is_a_order, IntegerType())
agg_isReturn = udf(is_a_return, IntegerType())
agg_total_item_count = udf(total_item_count, IntegerType())
agg_total_order_cost = udf(total_cost, FloatType())


# deriving additional columns
expandedOrderStream = orderStream \
   .withColumn("total_cost", agg_total_order_cost(orderStream.items,orderStream.type)) \
   .withColumn("total_items", agg_total_item_count(orderStream.items)) \
   .withColumn("is_order", agg_isOrder(orderStream.type)) \
   .withColumn("is_return", agg_isReturn(orderStream.type))

# appending the calculated input values to console
extendedOrderQuery = expandedOrderStream \
   .select("invoice_no", "country", "timestamp","total_cost","total_items","is_order","is_return") \
   .writeStream \
   .outputMode("append") \
   .format("console") \
   .option("truncate", "false") \
   .option("path", "Console_output") \
   .option("checkpointLocation", "Console_output_checkpoints") \
   .trigger(processingTime="1 minute") \
   .start()

# Calculating time based KPI values
aggStreamByTime = expandedOrderStream \
    .withWatermark("timestamp","1 minutes") \
    .groupby(window("timestamp", "1 minute")) \
    .agg(sum("total_cost").alias("total_volume_of_sales"),
        avg("total_cost").alias("average_transaction_size"),
        count("invoice_no").alias("OPM"),
        avg("is_Return").alias("rate_of_return")) \
    .select("window.start","window.end","OPM","total_volume_of_sales","average_transaction_size","rate_of_return")

# Writing to the Console and hadoop location for Time based KPI values 
queryByTime = aggStreamByTime.writeStream \
    .format("json") \
    .outputMode("append") \
    .option("truncate", "false") \
    .option("path", "timeKPIvalue") \
    .option("checkpointLocation", "timeKPIvalue_checkpoints") \
    .trigger(processingTime="1 minutes") \
    .start()

# Calculating Time and country based KPIs values
aggStreamByCountry = expandedOrderStream \
    .withWatermark("timestamp", "1 minutes") \
    .groupBy(window("timestamp", "1 minutes"), "country") \
    .agg(sum("total_cost").alias("total_volume_of_sales"),
        count("invoice_no").alias("OPM"),
        avg("is_Return").alias("rate_of_return")) \
    .select("window.start","window.end","country", "OPM","total_volume_of_sales","rate_of_return")

# WWriting to the Console and hadoop location for Time and country based KPI values
ByTime_country = aggStreamByCountry.writeStream \
    .format("json") \
    .outputMode("append") \
    .option("truncate", "false") \
    .option("path", "time_countryKPIvalue") \
    .option("checkpointLocation", "time_countryKPIvalue_checkpoints") \
    .trigger(processingTime="1 minutes") \
    .start()

# Spark to await for termination
extendedOrderQuery.awaitTermination()
queryByTime.awaitTermination()
queryByCountry.awaitTermination()