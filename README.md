# DPIC Take Home Assignment - César Núñez

This project presents a full data pipeline and analysis workflow for monitoring vocational training programs in Odisha, using ITI enrollments and citizen grievances.

## 📦 Project Structure
```
dpic_takehome/ 
├── air_flow_automation/
    ├── dpic_dag.py         # Airflow DAG script
    └── README.md           # Logic of the workflow
├── dashboard/
    ├── app.py              # Dashboard layout
    └── figures.py          # 
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

### 📍 Tool:
- [Plotly Dash] or [Streamlit] (see `dashboard/`)

### Features:
- Line/bar charts of district enrollments
- Grievance submission patterns
- Mismatch highlights: high enrollments vs low grievance rates

### 📝 Insight Brief:
See `insight_brief.md` or `insight_brief.pdf` for a summary of 3 actionable insights derived from the data.


## 🛠️ Setup Instructions

1. Clone the repo:
```bash
git clone https://github.com/your-username/dpic-takehome-assignment.git
cd dpic-takehome-assignment
```
2. Clone the repo:
```bash

```
3. Run the project as a module:
```
uv run -m dpic_takehome
```