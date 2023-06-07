import requests 
import pandas as pd
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.functions import col
from pyspark.sql.types import StructType, StructField, StringType, DoubleType
import redis 

def main():
    global redis_client
    # Create SparkSession
    spark = SparkSession.builder.appName("Data Transformation").getOrCreate()
    #Initializing Radis 
    redis_client = redis.Redis(host='redis', port=6379, db=0)

    schema = create_schema()
    account_data = get_data_from_api("https://xloop-dummy.herokuapp.com/account")
    accounts_df = df = spark.createDataFrame(account_data, schema)
    councillor_data = get_data_from_api("https://xloop-dummy.herokuapp.com/councillor")
    councilor_df = spark.createDataFrame(councillor_data)
    patient_data = get_data_from_api("https://xloop-dummy.herokuapp.com/patient")
    patients_df = spark.createDataFrame(patient_data)

     # Drop unnecessary columns from councilor table
    columns_to_drop_from_councilor_df = ["created", "guardian_phone_number","updated","specialization","description"]
    councilor_df = councilor_df.drop(*columns_to_drop_from_councilor_df)
    councilor_df=councilor_df.withColumnRenamed("user_id", "councilors_user_id")
    councilor_df=councilor_df.withColumnRenamed("id", "councilors_id")

    # Drop unnecessary columns from patients table
    columns_to_drop_from_patients_df = ["created", "guardian_phone_number","updated"]
    patients_df = patients_df.drop(*columns_to_drop_from_patients_df)
    patients_df=patients_df.withColumnRenamed("user_id", "patients_user_id")
    patients_df=patients_df.withColumnRenamed("id", "patients_id")

    # Extract latitude, longitude, and region from accounts table
    accounts_df = accounts_df.withColumn('latitude', F.col('address.location.lat'))
    accounts_df = accounts_df.withColumn('longitude', F.col('address.location.lng'))
    accounts_df = accounts_df.withColumn('region', F.col('address.region'))
    columns_to_drop_from_accounts_df = ["address","phone_number", "email","gender","is_active","last_name","created","updated","national_identity","role","password","first_name"]
    accounts_df = accounts_df.drop(*columns_to_drop_from_accounts_df)

    
    # Join accounts table and patients table based on ID
    joined_df_patient = accounts_df.join(patients_df, accounts_df.id == patients_df.patients_user_id, "inner")
    joined_df_patient=joined_df_patient.withColumnRenamed("latitude", "patients_latitude")
    joined_df_patient=joined_df_patient.withColumnRenamed("longitude", "patients_longitude")
    joined_df_patient=joined_df_patient.withColumnRenamed("region", "patients_region")

    # Join accounts table and councilor table based on ID
    joined_df_councilor = accounts_df.join(councilor_df, accounts_df.id == councilor_df.councilors_user_id, "inner")

    # Convert joined DataFrames to Pandas DataFrames
    joined_df_councilor=joined_df_councilor.toPandas()
    joined_df_patient=joined_df_patient.toPandas()

    # Convert DataFrames to JSON
    joined_df_councilor = joined_df_councilor.to_json()
    joined_df_patient = joined_df_patient.to_json()

    Upload_to_Redis(joined_df_councilor, joined_df_patient)
    # data= Get_data_from_Redis()
    # print(data)

# function to upload data to Radis
def Upload_to_Redis(joined_df_councilor, joined_df_patient):
    redis_client.set('councilor_data', joined_df_councilor)
    redis_client.set('patient_data', joined_df_patient)
    print("Data successfully uploaded to Redis")

# def Get_data_from_Redis():
#     councilor_df = radis_client.get('councilor_data') 
#     councilor_df = councilor_df.decode('utf-8')
#     councilor_df = pd.read_json(councilor_df)
#     patient_df = radis_client.get('patient_data') 
#     patient_df = patient_df.decode('utf-8')
#     patient_df = pd.read_json(patient_df)
#     return(councilor_df, patient_df)


# function to get data from APIs
def get_data_from_api(url):
    response = requests.get(url)
    data = response.json()
    return data

#Schema for the account's table
def create_schema():
    schema = StructType([
    StructField("id", StringType(), True),
    StructField("created", StringType(), True),
    StructField("updated", StringType(), True),
    StructField("email", StringType(), True),
    StructField("password", StringType(), True),
    StructField("first_name", StringType(), True),
    StructField("last_name", StringType(), True),
    StructField("gender", StringType(), True),
    StructField("phone_number", StringType(), True),
    StructField("address", StructType([
        StructField("address", StringType(), True),
        StructField("location", StructType([
            StructField("lat", DoubleType(), True),
            StructField("lng", DoubleType(), True)
        ]), True),
        StructField("placeId", StringType(), True),
        StructField("region", StringType(), True)
    ]), True),
    StructField("national_identity", StringType(), True),
    StructField("role", StringType(), True),
    StructField("is_active", StringType(), True)
])
    return schema


main()

# data= Get_data_from_Redis()
# print(data)