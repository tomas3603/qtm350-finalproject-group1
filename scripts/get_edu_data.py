import datetime
import os
import wbdata
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
start_year = 2003
end_year = 2022

codes = pd.read_csv('data/codes_top20.csv')
top_20_codes = codes['country_code'].tolist()

# Let us include the global averages for all of these metrics

top_20_codes.append('WLD')

indicators = {
    "SE.PRM.ENRR": "primary_enrollment",
    "SE.SEC.ENRR": "secondary_enrollment",
    "SE.TER.ENRR": "tertiary_enrollment",
    "SE.COM.DURS": "compulsory_edu_duration",
    "SE.XPD.CTOT.ZS": "current_edu_expenditure_pct_total_public",
    "SE.XPD.TOTL.GD.ZS": "gov_expenditure_edu_pct_gdp",
    "SE.XPD.PRIM.PC.ZS": "gov_exp_student_primary_pct_gdp_per_capita",
    "SE.XPD.SECO.PC.ZS": "gov_exp_student_secondary_pct_gdp_per_capita",
    "SE.XPD.TERT.PC.ZS": "gov_exp_student_tertiary_pct_gdp_per_capita"
}

# Retrieve the data from wbdata
data_edu = wbdata.get_dataframe(
    indicators,
    country=top_20_codes,
    date=(datetime.datetime(start_year, 1, 1), datetime.datetime(end_year, 12, 31))
)

data_edu = data_edu.reset_index()
data_edu.rename(columns={'country': 'country_name', 'date': 'year'}, inplace=True)

# Save to CSV in the data folder
data_edu.to_csv("data/education_data.csv", index=False)

print("Education data successfully saved to 'data/education_data.csv'")

conn = psycopg2.connect(
        host='127.0.0.1',
        port='5433',
        database='postgres',
        user='postgres',
        password='tomas.36'
    )
cur = conn.cursor()

create_table_query = """
DROP TABLE IF EXISTS education_data;
CREATE TABLE education_data (
    country_name TEXT,
    year INT,
    primary_enrollment NUMERIC,
    secondary_enrollment NUMERIC,
    tertiary_enrollment NUMERIC,
    compulsory_edu_duration NUMERIC,
    current_edu_expenditure_pct_total_public NUMERIC,
    gov_expenditure_edu_pct_gdp NUMERIC,
    gov_exp_student_primary_pct_gdp_per_capita NUMERIC,
    gov_exp_student_secondary_pct_gdp_per_capita NUMERIC,
    gov_exp_student_tertiary_pct_gdp_per_capita NUMERIC
);
"""
cur.execute(create_table_query)
conn.commit()

# Prepare data for insertion
# Convert DataFrame to list of tuples
values = [tuple(x) for x in data_edu.to_numpy()]

# Insert into the table
columns = data_edu.columns.tolist()
insert_statement = f"INSERT INTO education_data ({', '.join(columns)}) VALUES %s"

execute_values(cur, insert_statement, values)
conn.commit()

print("Data successfully inserted into the 'education_data' table.")

cur.close()
conn.close()
