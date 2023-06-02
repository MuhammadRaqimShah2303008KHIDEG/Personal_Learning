#Getting Data from API using FASTAPI and convert data to dataframe than to parquet and upload that data to S3

from fastapi import FastAPI
import requests
import uvicorn
import pandas as pd
# from pyspark.sql import SparkSession
import boto3

app = FastAPI()
# spark = SparkSession.builder.config("spark.sql.files.maxRecordsPerFile", "100000").getOrCreate()
BUCKET_NAME = "raqim-module5-day5"
s3 = boto3.client('s3')

@app.get("/api")
def get_data():
    url = f"https://open.er-api.com/v6/latest/USD"
   #response = requests.get(url)

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an exception for any 4XX or 5XX status code
        data = response.json()
        rate = data["rates"]
        new_df = pd.DataFrame(rate,index=["Rates"])
        new_df = new_df.transpose()
        print(new_df)
        print(type(new_df))
        To_Parquet(new_df)
        upload_to_s3()
        return {"message": "Parquet file created successfully"}
    except requests.exceptions.RequestException as e:
    # Handle the exception or log the error message
        return {"error": str(e)}
    
def To_Parquet(new_df):
        new_df.to_parquet('data.parquet', index=False)

def upload_to_s3():
    # s3_file = 'parquet_files/data.parquet'
    s3_key = 'data.parquet'
    s3.upload_file(s3_key, BUCKET_NAME, s3_key)

if __name__ == '__main__':
    uvicorn.run(app='main:app', reload=True)
