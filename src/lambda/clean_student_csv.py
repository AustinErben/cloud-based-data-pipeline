import boto3
import pandas as pd
from io import StringIO

# AWS S3 Setup
s3 = boto3.client("s3")
bucket_name = "austins-etl-project"
input_key = "student_dataset/raw/Students_Grading_Dataset.csv"
output_key = "student_dataset/cleaned/Students_Grading_Dataset.csv"

def lambda_handler(event, context):
    # Read CSV from S3
    obj = s3.get_object(Bucket=bucket_name, Key=input_key)
    df = pd.read_csv(obj["Body"])

    # Clean Column Names
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

    # Print Column Names
    print("Columns in DataFrame:", df.columns)

    # Fill Missing Values
    df["attendance_(%)"].fillna(df["attendance_(%)"].mean(), inplace=True)
    df["assignments_avg"].fillna(df["assignments_avg"].median(), inplace=True)
    df["parent_education_level"].fillna("Unknown", inplace=True)

    # Convert Data Types
    df["stress_level_(1-10)"] = df["stress_level_(1-10)"].astype(int)

    # Categorize Sleep Hours
    bins = [0, 4, 6, 8, 12]
    labels = ["Very Low", "Low", "Medium", "High"]
    df["sleep_category"] = pd.cut(df["sleep_hours_per_night"], bins=bins, labels=labels)

    # Remove Duplicates
    df.drop_duplicates(inplace=True)

    # Save back to S3
    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False)
    s3.put_object(Bucket=bucket_name, Key=output_key, Body=csv_buffer.getvalue())

    return {"statusCode": 200, "body": "Data cleaned and saved to S3!"}
