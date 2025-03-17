# **Student Metrics Data Pipeline**

**Video Demonstration** - [LINK](https://youtu.be/NxrPnNJlVO8)



This project is an early-stage data pipeline built to assess and track student metrics using various AWS services. It extracts data from a CSV file uploaded to Amazon S3, processes and cleans the data using AWS Lambda, and loads the processed data into a PostgreSQL database via Glue. Finally, the data is visualized using Tableau for easier reporting and analysis.

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

## **Future Improvements and Considerations**

### **1\. Automation & Orchestration**  
- Right now, much of the process is manual (triggering Glue and uploads manually).  
- To fully automate it, could consider using: **AWS Step Functions** or **Apache Airflow** to orchestrate ETL jobs.  
- **AWS EventBridge** to trigger Glue jobs on S3 file uploads.  

### **2\. Schema Evolution & Data Quality**  
- AWS Glue crawlers detect schema changes, but how should the pipeline handle them?  
- Implement **AWS Deequ** (or similar) for data quality checks.  

### **3\. Error Handling & Logging**  
- If Glue or PostgreSQL fails, there could be a retry mechanism.  
- Add **AWS CloudWatch logging** to capture errors & job execution details.  

### **4\. Scalability & Performance**  
- How would the pipeline handle large datasets?  
- Consider **partitioning S3 data** and using **Parquet format** for efficiency.  

### **5\. CI/CD & Infrastructure as Code**  
- Right now, configurations in Glue are manually set up.  
- Consider using **Terraform** or **AWS CloudFormation** to define **Infrastructure as Code (IaC)**.  
- **CI/CD Pipeline:** Can set up a **GitHub Actions** pipeline to deploy changes to AWS.  

