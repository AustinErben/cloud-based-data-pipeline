# **Student Metrics Data Pipeline**

This project is an automated data pipeline built to assess and track student metrics using various AWS services. It extracts data from a CSV file uploaded to Amazon S3, processes and cleans the data using AWS Lambda, and loads the processed data into a PostgreSQL database. Finally, the data is visualized using Tableau for easier reporting and analysis.

## **Overview**

The goal of this project is to build a scalable and serverless data pipeline that allows a school district to collect, process, and analyze student performance data. The pipeline is designed to run on AWS using services such as Lambda, S3, Glue, and PostgreSQL, enabling automated data ingestion, transformation, and visualization.

## **Architecture**

The pipeline works as follows:

1. **Data Upload**:

   * CSV files containing student metrics (e.g., performance data, attendance, etc.) are uploaded to an S3 bucket.  
2. **Lambda Function**:

   * A Lambda function is triggered when a new file is uploaded to the S3 bucket. The Lambda function:  
     * Cleans the data (e.g., handles missing values, formats, or validates fields).  
     * Reuploads the cleaned data to a new S3 location.  
3. **Glue Crawler**:

   * An AWS Glue Crawler runs on the cleaned data in S3 to discover and catalog the schema in the Glue Data Catalog. This ensures that the schema is automatically updated for further ETL processing.  
4. **Glue Job**:

   * A Glue Job is run to extract the cleaned data from S3, transform it if necessary, and load it into a PostgreSQL database.  
5. **PostgreSQL Database**:

   * The PostgreSQL database stores the processed student metrics and serves as the data source for reporting.  
6. **Tableau Visualization**:

   * The PostgreSQL database is connected to Tableau for creating visual dashboards and reports, allowing administrators and educators to analyze student metrics.

## **Components**

### **1\. AWS S3**

* Stores both the raw and cleaned student data in CSV format.  
* Acts as the source and destination for the data processing flow.

### **2\. AWS Lambda**

* Triggered by S3 events when a new file is uploaded.  
* Cleans and transforms the uploaded data before reuploading it to S3.

### **3\. AWS Glue**

* **Glue Crawler**: Automatically discovers the schema of the cleaned data and updates the Glue Data Catalog.  
* **Glue Job**: Extracts the cleaned data from S3 and loads it into the PostgreSQL database.

### **4\. PostgreSQL**

* Stores the cleaned and transformed data for reporting.  
* Tables are structured to capture student metrics such as performance scores, attendance, and other relevant data.

### **5\. Tableau**

* Visualizes the data stored in PostgreSQL for reporting purposes.  
* Dashboards are created to help administrators, teachers, and other stakeholders analyze student performance and behavior.

## **Setup Instructions**

Follow the steps below to set up and run the project.

### **Prerequisites**

* An **AWS account** with access to the following services:  
  * S3  
  * Lambda  
  * Glue  
  * PostgreSQL (RDS or self-managed)  
  * IAM roles with appropriate permissions  
* **Tableau Desktop** or Tableau Server to visualize the data.  
* A **PostgreSQL instance** for storing the student metrics data.

### **1\. Create an S3 Bucket**

* Create an S3 bucket to store the raw and cleaned student data CSV files.

### **2\. Lambda Function**

* Create a Lambda function in AWS.  
* Set it to trigger on file uploads to the S3 bucket.  
* Implement data cleaning logic in the Lambda function (e.g., handling missing data, reformatting columns).  
* Reupload the cleaned data to a separate S3 location.

### **3\. Glue Crawler**

* Set up a Glue Crawler to scan the cleaned data in S3.  
* The Crawler will automatically detect the schema and update the Glue Data Catalog.

### **4\. Glue Job**

* Create a Glue Job that:  
  * Reads the cleaned data from S3.  
  * Transforms the data if necessary.  
  * Loads it into a PostgreSQL database.

### **5\. PostgreSQL Database**

* Set up a PostgreSQL database (either on RDS or on-premises).  
* Create the necessary tables to store student metrics.  
* Make sure the Glue job has the necessary permissions to insert data into the PostgreSQL database.

### **6\. Connect Tableau**

* Connect Tableau to the PostgreSQL database using the database connection details.  
* Create dashboards and reports to visualize the student metrics.

## **Future Improvements**

* **Schema Change Automation**: Currently, schema changes are managed manually. Automating this process through Glue jobs and database migrations is a potential enhancement.  
* **Data Validation**: Introduce more comprehensive data validation and error handling in the Lambda function.  
* **Alerting**: Set up notifications or alarms for failed Lambda executions, Glue job failures, or other issues in the pipeline.  
* **Security Enhancements**: Improve access controls and encryption for sensitive student data.