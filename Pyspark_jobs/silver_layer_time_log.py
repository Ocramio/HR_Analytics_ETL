import pyspark.sql.functions as F
import utils as u

#----------------------------------------------#
#------------- SPECIFIC FUNCTIONS -------------#
#----------------------------------------------#

def naming_first_col(df):
    return df.withColumnRenamed(df.columns[0], 'employee_id')

def melting_cols(df):
    stack_str = f"stack({len(df.columns[1::])}, " + \
                ", ".join(df.columns[1::]) + ") as (origin, datetime)"

    return df.select(
        "employee_id",
        F.expr(stack_str).drop("origin")
    )

def splitting_date(df):
    df = (df
        .withColumns('date', F.to_date(F.col("datetime")))
        .withColumns('time', F.date_format(F.col("datetime"), 'dd/MM/YYYY'))
    )
    return df.drop("datetime")

#----------------------------------------------#
#--------------- MAIN FUNCTION ----------------#
#----------------------------------------------#

def silver_layer_time_log():

    # Parser
    args = u.parser()

    # Creating the Spark Session
    spark = u.get_spark_session("silver_layer_time_log_job")
    
    # Reading the .parquet file
    df_in_time = spark.read.parquet(f'{args.bronze_path}/in_time/*.parquet')

    df_out_time = spark.read.parquet(f'{args.bronze_path}/out_time/*.parquet')
    
    if not df_in_time.head(1) or not df_out_time.head(1):
        print("Source data is empty. Skipping transformation.")
        return

    df_in_time = (df_in_time
                  # Naming first column "employee_id"
                  .transform(naming_first_col)
                  # Melting columns
                  .transform(melting_cols)
                  # Splitting date and time
                  .transform(splitting_date)
                  .transform(lambda df: u.add_metadata(df, args.bronze_path, "in_time"))
    )

    df_out_time = (df_out_time
                   # Naming first column "employee_id"
                   .transform(naming_first_col)
                   # Melting columns
                   .transform(melting_cols)
                   # Splitting date and time
                   .transform(splitting_date)
                   .transform(lambda df: u.add_metadata(df, args.bronze_path, "out_time"))
    )

    df_time_log = (df_in_time.join(df_out_time, ["employee_id","date"], "inner"))
    
    # Dropping duplicates
    df_time_log = (df_time_log
                   .transform(lambda df: df.dropDuplicates(["EmployeeID"]))
    )

    # Writing the files into the silver layer with .parquet extension
    u.writting_to_parquet(df_time_log, args.silver_path, "time_log")

if __name__ == "__main__":
    silver_layer_time_log()
