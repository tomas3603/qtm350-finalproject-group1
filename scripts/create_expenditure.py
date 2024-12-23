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


df.to_csv("data/edu_expenditure_as_pct_gdp.csv")


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

growth_df = df.copy()

for y in years:
    if y == 2002:
        continue
    prev_year = f"y{y-1}"
    # percentage growth:
    growth_df[f"y{y}"] = ((df[f"y{y}"] - df[str(prev_year)]) / df[str(prev_year)]) * 100

growth_df.drop(columns=['y2002'], inplace=True)
growth_df.fillna(0, inplace=True)

growth_df.to_csv("data/edu_expenditure_growth.csv")

print("Saved education expenditure growth data")
print(growth_df)
