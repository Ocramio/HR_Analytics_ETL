import pyspark.sql.functions as F
from pyspark.sql.types import StringType, BooleanType, IntegerType
import utils as u

#----------------------------------------------#
#------------- SPECIFIC FUNCTIONS -------------#
#----------------------------------------------#

def correcting_bool_cols(df, bool_cols):
    for col in bool_cols:
        df = df.withColumn(col,
            (
            F.when(F.trim(F.lower(F.col(col)).isin(['yes','y','1'])), True)
            .when(F.trim(F.lower(F.col(col)).isin(['no','n','0'])), False)
            )
        )
    return df

def correcting_business_travel_col(df):
    df = (
        df
        .withColumn("BusinessTravel", 
                    F.when(F.trim(F.lower(df["BusinessTravel"])) == 'travel_rarely',
                        "Travel Rarely")
                    .when(F.trim(F.lower(df["BusinessTravel"])) == 'travel_frequently',
                        "Travel Frequently")
                    .when(F.trim(F.lower(df["BusinessTravel"])) == 'non-travel',
                        "Non Travel")
                    )
    )
    return df

def validating_marital_status_col(df):
    df = (
        df
        .withColumn("MaritalStatus",
                    F.when(~F.trim(F.lower(df["MaritalStatus"])).isin(
                        ['married','single','divorced']),None)
                    .otherwise(df["MaritalStatus"])
        )
    )

#----------------------------------------------#
#--------------- MAIN FUNCTION ----------------#
#----------------------------------------------#

def silver_layer_general_data():
    
    # Parser
    args = u.parser()

    # Creating the Spark Session
    spark = u.get_spark_session("silver_layer_employee_survey_data_job")
    
    # Reading the .parquet file
    df = spark.read.parquet(f'{args.bronze_path}/general_data/*.parquet')

    if not df.head(1):
        print("Source data is empty. Skipping transformation.")
        return
    
    # List(s) of the column(s) type(s)
    integer_cols = [
        "Age", "DistanceFromHome", "Education", "EmployeeCount", 
        "EmployeeID", "JobLevel", "MonthlyIncome", "NumCompaniesWorked", 
        "PercentSalaryHike", "StandardHours", "StockOptionLevel", 
        "TotalWorkingYears", "TrainingTimesLastYear", "YearsAtCompany", 
        "YearsSinceLastPromotion", "YearsWithCurrManager"
    ]

    text_cols = [
        "BusinessTravel", "Department", "EducationField",
        "Gender", "JobRole", "MaritalStatus"
    ]

    bool_cols = [
        "Attrition", "Over18"
    ]

    name_map = {
        "EmployeeID": "employee_id",
        "Age": "age_years",
        "Attrition": "is_attrited_last_year",
        "BusinessTravel": "cat_business_travel",
        "Department": "cat_department",
        "DistanceFromHome": "dist_from_home_km",
        "Education": "lvl_education",
        "EducationField": "cat_education_field",
        "Gender": "cat_gender",
        "JobLevel": "lvl_job",
        "JobRole": "cat_job_role",
        "MaritalStatus": "cat_marital_status",
        "MonthlyIncome": "amt_monthly_income",
        "NumCompaniesWorked": "cnt_companies_worked",
        "Over18": "is_over_18",
        "PercentSalaryHike": "pct_salary_hike",
        "StandardHours": "cnt_standard_hours",
        "StockOptionLevel": "lvl_stock_option",
        "TotalWorkingYears": "cnt_total_working_years",
        "TrainingTimesLastYear": "cnt_training_times_last_year",
        "YearsAtCompany": "cnt_years_at_company",
        "YearsSinceLastPromotion": "cnt_years_since_last_promotion",
        "YearsWithCurrManager": "cnt_years_with_curr_manager",
    }
    
    df = (df
          # Correcting bool cols
          .transform(lambda df: correcting_bool_cols(df, bool_cols))
          # Removing underscore from column "BusinessTravel" and validating the values
          .transform(correcting_business_travel_col)
          # Validating data from column "MaritalStatus"
          .transform(validating_marital_status_col)
          # Casting the right data types
          .transform(lambda df: u.cast_type(df, IntegerType(), integer_cols))
          .transform(lambda df: u.cast_type(df, StringType(), text_cols))
          .transform(lambda df: u.cast_type(df, BooleanType(), bool_cols))
          # Dropping duplicates using the employee id
          .transform(lambda df: df.dropDuplicates(["EmployeeID"]))
          # Changing the columns name to follow the naming conventions
          .transform(lambda df: u.rename_columns(df, name_map))
          # Adding Metadata
          .transform(lambda df: u.add_metadata(df, args.bronze_path, "general_data"))
    )

    # Writing the files into the silver layer with .parquet extension
    u.writting_to_parquet(df, args.silver_path, "general_data")

if __name__ == "__main__":
    silver_layer_general_data()