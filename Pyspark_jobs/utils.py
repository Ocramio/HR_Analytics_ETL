import argparse
from pyspark.sql import SparkSession
import pyspark.sql.functions as F

#----------------------------------------------#
#------------- GENERAL FUNCTIONS --------------#
#----------------------------------------------#

# Parser
def parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--landing_path", type=str)
    parser.add_argument("--bronze_path", type=str)
    parser.add_argument("--silver_path", type=str)
    return parser.parse_args()

# Creating the Spark Session
def get_spark_session(app_name):
    return SparkSession.builder.appName(app_name).config('spark.sql.repl.eagerEval.enabled', True).getOrCreate()

# Casting the right data types
def cast_type(df, type, cols):
    for col in cols:
        df = df.withColumn(col, df[col].cast(type))
    return df

# Adding Metadata
def add_metadata(df, args, folder_name):
    return (
            df.withColumn("sys_ingestion_timestamp", F.current_timestamp()) 
            .withColumn("sys_source", F.lit(f'{args}/{folder_name}'))
    )

# Writing the files into the target
def writting_to_parquet(df, args, folder_name):
    target_path = f"{args}/{folder_name}"
    df.write.mode("overwrite").parquet(target_path)

# Changing the columns name to follow the naming conventions
def rename_columns(df, name_map):
    renamed_cols = [F.col(old).alias(new) for old, new in name_map.items() if old in df.columns]
    extra_cols = [F.col(c) for c in df.columns if c not in name_map]
    return df.select(*(renamed_cols + extra_cols))