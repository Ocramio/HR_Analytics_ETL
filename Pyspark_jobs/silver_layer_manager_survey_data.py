from pyspark.sql.types import IntegerType
import utils as u

#----------------------------------------------#
#--------------- MAIN FUNCTION ----------------#
#----------------------------------------------#

def silver_layer_manager_survey_data():

    name_map = {
        "EmployeeID" : "employee_id",
        "JobInvolvement" : "lvl_job_involvement", 
        "PerformanceRating" : "lvl_performance_rating"
    }

    # Parser
    args = u.parser()

    # Creating the Spark Session
    spark = u.get_spark_session("silver_layer_manager_survey_data_job")

    # Reading the .parquet file
    df = spark.read.parquet(f'{args.bronze_path}/manager_survey_data/')

    if not df.head(1):
        print("Source data is empty. Skipping transformation.")
        return

    # List(s) of the column(s) type(s)
    integer_cols = ["EmployeeID", "JobInvolvement", "PerformanceRating"]
    
    df = (df
        # Casting the right data types
        .transform(lambda df: u.cast_type(df, IntegerType(), integer_cols))
        # Adding Metadata 
        .transform(lambda df: u.add_metadata(df, args.bronze_path, "manager_survey_data"))
        # Dropping unnecessary duplicates
        .transform(lambda df: df.dropDuplicates(["EmployeeID"]))
        # Changing the columns name to follow the naming conventions
        .transform(lambda df: u.rename_columns(df, name_map))
    )

    # Writing the files into the silver layer with .parquet extension
    u.writting_to_parquet(df, args.silver_path, "employee_survey_data")

if __name__ == '__main__':
    silver_layer_manager_survey_data()


    


    