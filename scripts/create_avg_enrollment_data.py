import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
import os

conn = psycopg2.connect(
        host='127.0.0.1',
        port='5433',
        database='postgres',
        user='postgres',
        password='tomas.36'
    )
cur = conn.cursor()

years = range(2002, 2023)
primary_cols = ",\n       ".join([f"COALESCE(MAX(CASE WHEN year = {y} THEN primary_enrollment END), ca.avg_primary) AS p{y}" for y in years])
secondary_cols = ",\n       ".join([f"COALESCE(MAX(CASE WHEN year = {y} THEN secondary_enrollment END), ca.avg_secondary) AS s{y}" for y in years])

final_query = f"""
WITH country_avgs AS (
    SELECT country_name,
           AVG(primary_enrollment) AS avg_primary,
           AVG(secondary_enrollment) AS avg_secondary
    FROM education_data
    WHERE year BETWEEN 2003 AND 2022
    GROUP BY country_name
)
SELECT ed.country_name,
       {primary_cols},
       {secondary_cols}
FROM education_data ed
JOIN country_avgs ca ON ed.country_name = ca.country_name
WHERE ed.year BETWEEN 2003 AND 2022
GROUP BY ed.country_name, ca.avg_primary, ca.avg_secondary;
"""

cur.execute(final_query)
rows = cur.fetchall()
colnames = [desc[0] for desc in cur.description]

# Convert to DataFrame
df = pd.DataFrame(rows, columns=colnames)

year_has_data = []
for _, row in df.iterrows():
    count = 0
    for y in years:
        p_col = f"p{y}"
        s_col = f"s{y}"
        # Check if at least one of pYYYY or sYYYY is non-null
        if not (pd.isna(row[p_col]) and pd.isna(row[s_col])):
            count += 1
    year_has_data.append(count)

df['years_of_data'] = year_has_data

# Keep only countries with at least 15 years of data
df = df[df['years_of_data'] >= 15].drop(columns='years_of_data')

primary_cols = [f"p{y}" for y in years]
secondary_cols = [f"s{y}" for y in years]

df = df[['country_name'] + primary_cols + secondary_cols]

def forward_fill_across_years(row, cols):
    for i in range(1, len(cols)):
        if pd.isna(row[cols[i]]):
            prev_val = row[cols[i-1]]
            
            # Check if there's a next column and that it's not missing
            if i < len(cols)-1 and not pd.isna(row[cols[i+1]]):
                next_val = row[cols[i+1]]
                # Use the average of prev_val and next_val
                row[cols[i]] = (prev_val + next_val) / 2
            else:
                # If no next value is available, fall back to prev_val
                row[cols[i]] = prev_val
    return row


df = df.apply(lambda r: forward_fill_across_years(r, primary_cols), axis=1)
df = df.apply(lambda r: forward_fill_across_years(r, secondary_cols), axis=1)

def backward_fill_across_years(row, cols):
    # Start from the last column and move backwards
    for i in range(len(cols)-2, -1, -1):  # from second-last to first
        if pd.isna(row[cols[i]]):
            row[cols[i]] = row[cols[i+1]]
    return row

df = df.apply(lambda r: backward_fill_across_years(r, primary_cols), axis=1)
df = df.apply(lambda r: backward_fill_across_years(r, secondary_cols), axis=1)

numeric_cols = [col for col in df.columns if col.startswith('p') or col.startswith('s')]

for col in numeric_cols:
    df[col] = df[col].astype(float)


avg_df = df[['country_name']].copy()
for y in years:
    avg_col = str(y)  # name the average column simply as year
    avg_df[avg_col] = (df[f"p{y}"] + df[f"s{y}"]) / 2.0

avg_df.to_csv("data/avg_enrollment.csv", index=False)

print(avg_df)
print("Succesfully saved average enrollment data as csv in data")

growth_df = avg_df.copy()

# Compute growth for each subsequent year compared to the previous year
for y in years:
    if y == 2002:
        continue
    prev_year = y - 1
    # percentage growth:
    growth_df[str(y)] = ((avg_df[str(y)] - avg_df[str(prev_year)]) / avg_df[str(prev_year)]) * 100



growth_df.drop(columns=['2002'], inplace=True)

growth_df.to_csv("data/avg_enrollment_growth.csv")

print("Saved enrollment growth data")
print(growth_df)

cur.close()
conn.close()