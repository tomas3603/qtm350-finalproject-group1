import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
import os

# Connect to the database
conn = psycopg2.connect(
        host='127.0.0.1',
        port='5433',
        database='postgres',
        user='postgres',
        password='tomas.36'
    )
cur = conn.cursor()

years = range(2003, 2023)
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








print(df, df.shape)


# Determine how many years of data each country has.
# A "year of data" is defined as having at least one non-null in pYYYY or sYYYY
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

# 2. Forward fill missing values.
# We need to forward fill along the timeline (2003 to 2022).
# We'll do this separately for primary and secondary columns to avoid mixing them.

primary_cols = [f"p{y}" for y in years]
secondary_cols = [f"s{y}" for y in years]

# Sort columns by year just to be sure they are in order (they likely are already)
df = df[['country_name'] + primary_cols + secondary_cols]

# Forward fill primary enrollment data row-wise
# We'll apply a forward fill across columns for each row.
def forward_fill_across_years(row, cols):
    # We will iterate through the cols and if we find a NaN, fill with previous non-NaN
    for i in range(1, len(cols)):
        if pd.isna(row[cols[i]]):
            row[cols[i]] = row[cols[i-1]]
    return row

df = df.apply(lambda r: forward_fill_across_years(r, primary_cols), axis=1)
df = df.apply(lambda r: forward_fill_across_years(r, secondary_cols), axis=1)

# The DataFrame now has forward-filled values for missing years, based on the previous year's value.

# Note:
# If the first year's data (e.g., p2003 or s2003) was missing, it won't get imputed since there's no previous year.
# If you need to handle that case differently, you might consider dropping that country or using another imputation strategy.

# At this point, 'df' contains only countries with >=15 years of data, and missing values within
# those rows have been forward filled from previous years.

# You can now proceed with additional analysis or saving the DataFrame.

print(df)






# Close the connection
cur.close()
conn.close()
