import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
import os
from functions import forward_fill_across_years

years = range(2002, 2023)
year_cols = [f"y{y}" for y in years]


conn = psycopg2.connect(
        host='127.0.0.1',
        port='5433',
        database='postgres',
        user='postgres',
        password='tomas.36'
    )
cur = conn.cursor()
# Execute the query to fetch all data from expenditure_by_gdp
cur.execute("SELECT * FROM expenditure_by_gdp;")

# Fetch all rows
rows = cur.fetchall()

# Get column names from cursor description
colnames = [desc[0] for desc in cur.description]

# Create a DataFrame
df = pd.DataFrame(rows, columns=colnames)

# Close the connection
cur.close()
conn.close()

year_has_data = []
for _, row in df.iterrows():
    count = 0
    for y in years:
        col = f"y{y}"
        # Check if at least one of pYYYY or sYYYY is non-null
        if not (pd.isna(row[col])):
            count += 1
    year_has_data.append(count)

df['years_of_data'] = year_has_data

# Keep only countries with at least 15 years of data
df = df[df['years_of_data'] >= 15].drop(columns='years_of_data')

df = df.apply(lambda r: forward_fill_across_years(r, year_cols), axis=1)
df.fillna(0, inplace=True)

df.to_csv("data/expenditure_as_pct_gdp.csv")
