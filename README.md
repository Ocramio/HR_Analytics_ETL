## HR Analytics Data Lakehouse (GCP)

**Project Objective**

The primary objective of this project is to centralize and normalize HR information to provide a "Single Source of Truth." By transforming raw data into a structured Lakehouse format, we enable data scientists and analysts to perform deep-dive attrition analysis and predictive modeling without the overhead of manual data preparation.

**Architecture Overview**

The architecture follows the Medallion (Multi-Hop) Design, leveraging GCP-native services:

**Ingestion (Sources):**

Raw HR CSV files uploaded to the bronze layer.

**Bronze Layer:**

Data is converted to Parquet format to optimize storage and read performance. No transformations occur here to preserve original data state.

**Silver Layer:**
 
PySpark jobs running on GCP Dataproc perform:

- Data Cleansing & Standardization (handling nulls, uniform casing).

- Derived Columns (calculating tenure, age buckets).

- Normalization of employee attributes.

**Gold Layer:**
 
Business-logic-heavy BigQuery Views structured in a Star Schema. This layer is optimized for BI Tools (Power BI/Looker)


![alt text](/Documentation/Images/image.png)


**Infrastructure:**

Fully automated via Terraform for state management and resource monitoring.

**Tech Stack**

- Cloud Provider: Google Cloud Platform (GCP)

- Storage: Google Cloud Storage (GCS)

- Processing Engine: Apache Spark (PySpark) on Dataproc

- Data Warehouse: BigQuery

- Infrastructure as Code: Terraform

- Language: Python, SQL

**Getting Started**