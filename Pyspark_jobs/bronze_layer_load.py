import argparse
from pyspark.sql import SparkSession
from pyspark.sql.functions import lit, current_timestamp

# Creating the Spark Session
spark = SparkSession.builder.appName("bronze_layer_job").getOrCreate()

# Parser
parser = argparse.ArgumentParser()
parser.add_argument("--landing_path", type=str)
parser.add_argument("--bronze_path", type=str)
parser.add_argument("--silver_path", type=str)
args = parser.parse_args()

# List of files to process
tables = [
    "employee_survey_data",
    "general_data",
    "in_time",
    "manager_survey_data",
    "out_time"
]

for table in tables:
    print(f"Processing: {table}")
    
    # Reading the file
    df = spark.read.csv(f'{args.landing_path}/{table}.csv', encoding='utf-8', header=True)
    
    # Adding Metadata 
    df = df.withColumn("load_date", current_timestamp()) \
           .withColumn("source_system_nm", lit(table))
    
    # Writing the files into the bronze layer with .parquet extension
    target_path = f"{args.bronze_path}/{table}"
    df.write.mode("overwrite").parquet(target_path)

print("Bronze layer load complete!")