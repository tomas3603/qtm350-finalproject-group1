import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
from functions import forward_fill_across_years

conn = psycopg2.connect(
        host='127.0.0.1',
        port='5433',
        database='postgres',
        user='postgres',
        password='tomas.36'
    )
cur = conn.cursor()
years = range(2002, 2023)
year_cols = [f"y{y}" for y in years]
year_cases = []
for y in years:
    year_cases.append(f"MAX(CASE WHEN year = {y} THEN tertiary_enrollment END) AS y{y}")

year_select = ",\n    ".join(year_cases)

query = f"""
SELECT 
    country_name,
    {year_select}
FROM education_data
GROUP BY country_name
ORDER BY country_name;
"""

cur.execute(query)
rows = cur.fetchall()
colnames = [desc[0] for desc in cur.description]

df = pd.DataFrame(rows, columns=colnames)

cur.close()
conn.close()

df.to_csv("data/tertiary_enrollment.csv")

year_has_data = []
for _, row in df.iterrows():
    count = 0
    for y in years:
        col = f"y{y}"
        if not (pd.isna(row[col])):
            count += 1
    year_has_data.append(count)

df['years_of_data'] = year_has_data

# Keep only countries with at least 15 years of data
df = df[df['years_of_data'] >= 15].drop(columns='years_of_data')

df = df.apply(lambda r: forward_fill_across_years(r, year_cols), axis=1)

print(df)

growth_df = df.copy()

for y in years:
    if y == 2002:
        continue
    prev_year = f"y{y-1}"
    # percentage growth:
    growth_df[f"y{y}"] = ((df[f"y{y}"] - df[str(prev_year)]) / df[str(prev_year)]) * 100

growth_df.drop(columns=['y2002'], inplace=True)
growth_df.fillna(0, inplace=True)

growth_df.to_csv("data/tertiary_enrollment_growth.csv")

print("Saved tertiary enrollment growth data")
print(growth_df)
