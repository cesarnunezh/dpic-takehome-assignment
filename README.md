# DPIC Take Home Assignment - César Núñez

This repository contains a complete data pipeline, analysis and visualization on enrollment and citizen grievances in Odisha, India. It uses two main sources: enrollment data from Industrial Training Institutes  and citizen complaints related to vocational education.


## Project Structure
```
dpic_takehome/ 
├── air_flow_automation/
    ├── dpic_dag.py         # Airflow DAG script
    └── README.md           # Logic of the workflow
├── dashboard/
    ├── app.py              # Dashboard layout
    └── figures.py          # Contains functions to create charts
├── data_pipeline/          
    ├── cleaning.py         # Cleans the raw data
    ├── data_to_db.py       # Creates a db and inserts clean data into the db
    ├── fetch_data.py       # Fetches raw data from an URL
    └── run_queries.py      # Runs the queries required for the dashboard
├── sql/
    ├── queries.sql         # Contains the queries required for the dashboard
    └── schema.sql          # Contains the SQL schema
└── __main__.py             # Runs the whole project as a module
|
data/ 
├── raw/                    # Raw input files  
├── clean/                  # Cleaned datasets  
└── dpic.db                 # SQLite database 
README.md                   
```

## **Part 1: Data Pipeline & Cleaning**

### Input Files:
- `iti_enrollments.csv`: District-level enrollment counts by year
- `grievances.json`: Citizen complaints 

### Process:
- Cleaning scripts standardize district names, handle missing data, and remove duplicates.
- Data is loaded into an SQLite DB (`data/dpic.db`) using `data_pipeline/load_data.py`.

### SQL Schema:
Defined in `sql/schema.sql`, with:
- `iti_enrollments` table
- `grievances` table
- `districts` table
- `itis` table

### Queries:
Saved in `sql/queries.sql` and executed via `data_pipeline/run_queries.py`:
- Year-wise enrollment trends by gender
- Year-wise grievences trends by type of grievances
- Grievances per 1000 enrolled students by district
- Districts with high enrollments but low grievance submissions
- Types of grievances per district
- Enrollment by program and district

## **Part 2: Pipeline Automation**

This Apache Airflow DAG mimics the weekly automation for the take home assignment. It includes the following tasks in a sequence:
1. `fetch_raw_data`: Fetches the latest raw data from a GitHub repository.
2. `clean_data`: Runs the data cleaning functions.
3. `load_db_data`: Inserts cleaned data into the database.
4. `send_email_summary`: Emails a summary report from the weekly automation.


## **Part 3: Visualization & Insights**

For the visualization, I used Dash for dashboard layout and Altair for the creation of charts.  

### Features:
- Summary of Odisha's enrollment and grievances statistics.
- Analyzing missmatch between enrollment and grievances on district level.
- Interactive summary statistics for enrollment and grievances on district level.


## Setup Instructions

1. [Install UV](https://docs.astral.sh/uv/getting-started/installation/)

2. Clone the repo:
```
git clone git@github.com:cesarnunezh/dpic-takehome-assignment.git
cd dpic-takehome-assignment
```
3. Synchronize the virtual environment:
```
uv sync
```
4. Run the project as a module:
```
uv run -m dpic_takehome
```
