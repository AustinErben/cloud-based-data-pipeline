import boto3
import pandas as pd
import logging
from io import StringIO
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, ClientError

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# AWS S3 Setup
s3 = boto3.client("s3")
bucket_name = "austins-etl-project"
input_key = "student_dataset/raw/Students_Grading_Dataset.csv"
output_key = "student_dataset/cleaned/Students_Grading_Dataset.csv"

def read_csv_from_s3(bucket, key):
    """ Reads a CSV file from S3 and returns a Pandas DataFrame. """
    try:
        obj = s3.get_object(Bucket=bucket, Key=key)
        return pd.read_csv(obj["Body"])
    except ClientError as e:
        logger.error(f"S3 ClientError: {e}")
        raise
    except pd.errors.EmptyDataError:
        logger.error("CSV file is empty.")
        raise
    except Exception as e:
        logger.error(f"Unexpected error reading CSV: {e}")
        raise

def clean_data(df):
    """ Cleans and transforms the DataFrame. """
    try:
        # Clean Column Names
        df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

        logger.info(f"Columns in DataFrame: {df.columns.tolist()}")

        # Ensure required columns exist before processing
        required_columns = ["attendance_(%)", "assignments_avg", "parent_education_level", "stress_level_(1-10)", "sleep_hours_per_night"]
        missing_columns = [col for col in required_columns if col not in df.columns]

        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")

        # Fill Missing Values and Round to 2 Decimal Places
        df["attendance_(%)"].fillna(round(df["attendance_(%)"].mean(), 2), inplace=True)
        df["assignments_avg"].fillna(round(df["assignments_avg"].median(), 2), inplace=True)
        df["parent_education_level"].fillna("Unknown", inplace=True)

        # Convert Data Types with error handling
        try:
            df["stress_level_(1-10)"] = df["stress_level_(1-10)"].astype(int)
        except ValueError:
            logger.error("Invalid data in stress_level_(1-10), cannot convert to int.")
            raise

        # Categorize Sleep Hours
        bins = [0, 4, 6, 8, 12]
        labels = ["Very Low", "Low", "Medium", "High"]
        df["sleep_category"] = pd.cut(df["sleep_hours_per_night"], bins=bins, labels=labels)

        # Remove Duplicates
        df.drop_duplicates(inplace=True)

        return df
    except Exception as e:
        logger.error(f"Error cleaning data: {e}")
        raise

def save_csv_to_s3(df, bucket, key):
    """ Saves a DataFrame as CSV back to S3. """
    try:
        csv_buffer = StringIO()
        df.to_csv(csv_buffer, index=False)
        s3.put_object(Bucket=bucket, Key=key, Body=csv_buffer.getvalue())
        logger.info(f"Cleaned data saved to s3://{bucket}/{key}")
    except NoCredentialsError:
        logger.error("AWS credentials not found.")
        raise
    except PartialCredentialsError:
        logger.error("Incomplete AWS credentials.")
        raise
    except ClientError as e:
        logger.error(f"S3 ClientError while saving file: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error saving CSV to S3: {e}")
        raise

def lambda_handler(event, context):
    """ AWS Lambda handler function. """
    try:
        df = read_csv_from_s3(bucket_name, input_key)
        cleaned_df = clean_data(df)
        save_csv_to_s3(cleaned_df, bucket_name, output_key)
        return {"statusCode": 200, "body": "Data cleaned and saved to S3 successfully!"}
    except Exception as e:
        logger.error(f"Lambda function failed: {e}")
        return {"statusCode": 500, "body": f"Error: {str(e)}"}
