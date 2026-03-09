import utils as u 

#----------------------------------------------#
#--------------- MAIN FUNCTION ----------------#
#----------------------------------------------#

def bronze_layer():

    # List of files to process
    tables = [
        "employee_survey_data",
        "general_data",
        "in_time",
        "manager_survey_data",
        "out_time"
    ]

    # Parser
    args = u.parser()

    # Creating the Spark Session
    spark = u.get_spark_session("bronze_layer_job")

    for table in tables:
        print(f"Processing: {table}")
        
        # Reading the file with every column as a string (inferSchema=False)
        df = spark.read.csv(f'{args.landing_path}/{table}.csv', encoding='utf-8', header=True, inferSchema=False)
        
        df = (df
              # Adding Metadata 
              .transform(lambda df: u.add_metadata(df, args.landing_path, table))
        )
        
        # Writing the files into the bronze layer with .parquet extension
        u.writting_to_parquet(df, args.bronze_path, table)

if __name__ == '__main__':
    bronze_layer()