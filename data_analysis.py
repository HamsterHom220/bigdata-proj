from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *

def analyse():
    spark = SparkSession.builder.appName("MigrationAnalysis").getOrCreate()

    df = spark.read.parquet("hdfs:///data/preproc/ebd_US-VA_relAug-2025/ebd_US-VA_relAug-2025.parquet")  # or .csv() etc.
    print(f"Total records: {df.count()}")
    df.printSchema()
    df.show(5)

    REGION_BOUNDS = {
        'min_lat': 37.48358, 'max_lat': 39.74943,
        'min_lon': -80.39795, 'max_lon': -75.65186
    }

    filtered_df = (df
        .filter((col("LAT") >= REGION_BOUNDS['min_lat']) & 
                (col("LAT") <= REGION_BOUNDS['max_lat']) &
                (col("LON") >= REGION_BOUNDS['min_lon']) & 
                (col("LON") <= REGION_BOUNDS['max_lon']))
        .cache()
    )

    print(f"Filtered records: {filtered_df.count()}")

    # Basic temporal analysis
    species_trends = (filtered_df
        .groupBy("SCIENTIFIC NAME", year("DATE").alias("year"), 
                month("DATE").alias("month"))
        .agg(count("*").alias("observation_count"))
        .orderBy("SCIENTIFIC NAME", "year", "month")
    )

    species_trends.show(20)

    # Monthly aggregation for trend spotting
    monthly_summary = (filtered_df
        .groupBy(month("DATE").alias("month"), "SCIENTIFIC NAME")
        .agg(
            count("*").alias("total_observations"),
            mean("LAT").alias("avg_lat"),
            mean("LON").alias("avg_lon")
        )
        .orderBy("month", "SCIENTIFIC NAME")
    )

    # Species diversity and abundance
    species_stats = (filtered_df
        .groupBy("SCIENTIFIC NAME")
        .agg(
            count("*").alias("total_count"),
            countDistinct("DATE").alias("days_observed"),
            min("DATE").alias("first_seen"),
            max("DATE").alias("last_seen")
        )
        .orderBy(desc("total_count"))
    )

    species_stats.show(10)

    # Spatial distribution summary
    spatial_stats = filtered_df.select(
        mean("LAT").alias("avg_latitude"),
        mean("LON").alias("avg_longitude"),
        stddev("LAT").alias("lat_stddev"),
        stddev("LON").alias("lon_stddev")
    ).collect()

    # Sample data for quick plotting (if dataset is huge)
    sample_for_viz = (filtered_df
        .sample(0.1)  # 10% sample for quick visualization
        .select("SCIENTIFIC NAME", "DATE", "LAT", "LON")
        .toPandas()  # Convert to pandas for easy plotting
    )

    # Species count bar chart
    species_counts = (filtered_df
        .groupBy("SCIENTIFIC NAME")
        .count()
        .orderBy(desc("count"))
        .limit(10)
        .toPandas()
    )

    return spatial_stats, sample_for_viz, species_counts

if __name__=='__main__':
    analyse()