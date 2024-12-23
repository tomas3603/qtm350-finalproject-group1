# QTM 350 Final Project (Group 1)

## Project Description

This project investigates the relationship between GDP per capita growth and education indicators in Sub-Saharan African and Latin American countries. We focus on the top 20 fastest-growing countries over a given period (the last two decades) and examine whether increased educational engagement—measured through enrollment rates, tertiary education, and government expenditure on education—correlates with higher economic growth.

Using the World Bank’s World Development Indicators (WDI) dataset, we extracted and cleaned GDP per capita growth data and several education-related indicators. We performed data cleaning, missing value imputation, and aggregation in PostgreSQL and Python. We then produced visualizations (bar plots, line plots, and a correlation heatmap) to summarize and interpret the findings. Our final Quarto report documents the entire workflow, from raw data retrieval to modeling and visualization.

## Technologies and Tools

- **Python**: Data fetching, cleaning, analysis, and plotting.
- **wbdata**: Fetching World Bank indicators directly from the API.
- **PostgreSQL**: Storing raw and processed data, SQL-based data cleaning, and aggregation.
- **pandas, matplotlib, seaborn**: Data manipulation and visualization in Python.
- **Quarto**: Reproducible report generation, integrating code, analysis, and narrative.
- **Jupyter Notebook**: Interactively running and verifying Python code.
  
## Project Structure

```
qtm350-finalproject-group1/
├─ data/                     # Processed datasets, CSV files
├─ scripts/                  # Python scripts for data fetching, cleaning, and analysis
│  ├─ get_gdp_growth_data.py
│  ├─ describe_growth.sql
│  ├─ gdp_growth_hist.py
│  ├─ gdp_growth_linplot.py
│  ├─ get_edu_data.py
│  ├─ expenditure_pct_gdp.sql
│  ├─ create_expenditure.py
│  ├─ create_avg_enrollment_data.py
│  ├─ create_tertiary_avg_enrollment.py
│  ├─ visualizing_edu_growth.py
│  ├─ create_avg_full_data.py
│  ├─ correlation.py
│  └─ regressionplot.py
├─ figures/                  # Figures generated by the analysis
├─ report.qmd                # Quarto report documenting the analysis workflow
└─ README.md                 # This README file
```

## Instructions to Reproduce

### 1. Install Dependencies

Ensure you have the following installed and accessible in your environment:

- Python 3.x  
- pip or conda for installing Python packages  
- PostgreSQL server and client  
- Quarto (for rendering the report)  
- Jupyter Notebook

Install the required Python packages:

```bash
pip install pandas wbdata psycopg2 matplotlib seaborn
```

### 2. Set Up the Database

1. Start your PostgreSQL server.
2. Create a database for the project if you haven’t already:

   ```sql
   CREATE DATABASE qtm350_project;
   ```

3. Update the connection parameters inside the Python scripts to match your PostgreSQL credentials and database name.

### 3. Run the Data Preparation Scripts

From the project’s root directory, run the scripts in the following order:

```bash
python scripts/get_gdp_growth_data.py
python scripts/describe_growth.sql        # Run this inside psql or a Postgres client
python scripts/gdp_growth_hist.py
python scripts/gdp_growth_linplot.py
python scripts/get_edu_data.py
python scripts/expenditure_pct_gdp.sql     # Also run inside psql
python scripts/create_expenditure.py
python scripts/create_avg_enrollment_data.py
python scripts/create_tertiary_avg_enrollment.py
python scripts/visualizing_edu_growth.py
python scripts/create_avg_full_data.py
python scripts/correlation.py
python scripts/regressionplot.py
```

**Note:** The `.sql` files should be run using a PostgreSQL client (e.g., psql):

```bash
psql -d qtm350_project -f scripts/describe_growth.sql
psql -d qtm350_project -f scripts/expenditure_pct_gdp.sql
```

The scripts above:
- Fetch GDP growth and education data using `wbdata`.
- Load the data into PostgreSQL tables.
- Perform SQL-based cleaning and aggregation.
- Export clean datasets to CSV.
- Create visualizations (saved in `figures/`) and other analytical outputs.

### 4. Render the Quarto Report

Once all data and figures are generated, render the Quarto report:

```bash
quarto render report.qmd
```

This will produce `report.html` or `report.pdf` (as specified in the YAML header), showing the complete analysis and results.

## Authors

- Howie Brown (2585210)
- Leila Buchan (2550498)
- Gabe Schwartz (2545628)
- Tomas Hossain-Aguilar (2582623)