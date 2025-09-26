from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *

def preprocess_with_spark():
    spark = SparkSession.builder.appName("eBirdPreprocessing").getOrCreate()
    
    # Read tab-separated file
    df = spark.read \
        .option("sep", "\t") \
        .option("header", "true") \
        .option("inferSchema", "false") \
        .csv("/data/ebd_US-VA_relAug-2025/ebd_US-VA_relAug-2025.txt")
    
    # Select only needed columns
    FEATURES = [
        "SCIENTIFIC NAME", "OBSERVATION COUNT", "BREEDING CODE", "BREEDING CATEGORY", "BEHAVIOR CODE", 
        "COUNTY", "IBA CODE", "BCR CODE", "USFWS CODE", "LATITUDE", "LONGITUDE",
        "OBSERVATION DATE", "TIME OBSERVATIONS STARTED"
    ]
    
    df = df.select(*[col(c) for c in FEATURES if c in df.columns])
    
    # Create binary flags for code columns
    codes = ["IBA CODE", "BCR CODE", "USFWS CODE"]
    
    for col_name in codes:
        if col_name in df.columns:
            df = df.withColumn(f"HAS_{col_name.replace(' ', '_')}", 
                              when(col(col_name).isNotNull(), 1).otherwise(0))
    
    # Drop original code columns
    df = df.drop(*codes)
    
    # Convert data types
    df = df.withColumn("TIME OBSERVATIONS STARTED", to_time(col("TIME OBSERVATIONS STARTED")))
    df = df.withColumn("OBSERVATION DATE", to_date(col("OBSERVATION DATE")))
    df = df.withColumn("OBSERVATION COUNT", col("OBSERVATION COUNT").cast("int"))
    df = df.withColumn("LATITUDE", col("LATITUDE").cast("double"))
    df = df.withColumn("LONGITUDE", col("LONGITUDE").cast("double"))
    
    # Save to Parquet
    df.write \
      .option("compression", "snappy") \
      .mode("overwrite") \
      .parquet("hdfs:///data/preproc/")
    
    print("Spark preprocessing completed!")
    return df

if __name__ == "__main__":
    preprocess_with_spark()