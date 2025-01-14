from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum, avg

# Create Spark session
spark = SparkSession.builder \
    .appName("DataPipeline") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
    .config("spark.hadoop.io.native.lib.available", "false") \
    .getOrCreate()

# File paths
input_path = "C:\\Users\\anude\\data_engineering\\data\\sales.csv"
output_path = "C:\\Users\\anude\\data_engineering\\data\\output"


# Step 1: Read the sales data
sales_df = spark.read.option("header", "true").csv(input_path)

# Step 2: Show original data and schema
print("Original Sales Data:")
sales_df.show()
sales_df.printSchema()

# Step 3: Data Cleaning
# Convert Amount to numeric and filter out negative values
cleaned_df = sales_df.withColumn("Amount", col("Amount").cast("float")) \
    .filter(col("Amount").isNotNull() & (col("Amount") > 0))

# Step 4: Show cleaned data and schema
print("Cleaned Sales Data:")
cleaned_df.show()
cleaned_df.printSchema()

# Step 5: Perform Aggregations
# Total Sales per Product
total_sales_df = cleaned_df.groupBy("Product").agg(sum(col("Amount")).alias("Total_Sales"))
print("Total Sales per Product:")
total_sales_df.show()

# Step 6: Save Cleaned Data to CSV
cleaned_df.coalesce(1).write.mode("overwrite").option("header", "true").csv(output_path)


print("Cleaned and Aggregated data saved!")
