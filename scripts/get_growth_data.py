import datetime
import pandas as pd
import wbdata
from wbdata import get_countries
import os

import psycopg2
from psycopg2.extras import execute_values

# Parameters
start_year = 2013
end_year = 2022
indicator = "NY.GDP.PCAP.KD.ZG"  # GDP per capita growth (annual %)
regions = ["SSF", "LCN"]  # Sub-Saharan Africa, Latin America & Caribbean

# Get countries in Sub-Saharan Africa, Latin American and the Caribbean
all_countries = get_countries()
filtered_countries = [c['id'] for c in all_countries if c['region']['id'] in regions]

# Fetch data for the last 10 years for these countries using wbdata api
data = wbdata.get_dataframe({indicator: 'value'}, country=filtered_countries, date=(datetime.datetime(start_year, 1, 1), datetime.datetime(end_year, 12, 31)))

# Pivot the data to have the index be the country and the columns be the years
data.reset_index(inplace=True)
data = data.pivot(index='country', columns='date', values='value')

# Impute missing values using the average, drop rows with more than 5 missing values
data = data.dropna(thresh=data.shape[1] - 5)
data = data.apply(lambda row: row.fillna(row.mean()), axis=1)

# Calculate the average growth over the time period for each country
data['avg_growth_10yr'] = data.mean(axis=1)

# Select the top 20 countries with the highest average growth and sort by the avg
top_20_df = data.nlargest(20, 'avg_growth_10yr')
top_20_df.sort_values(by = 'avg_growth_10yr', ascending=False, inplace=True)

# Get the country code for the top 20 countries
country_codes = {country['name']: country['id'] for country in all_countries}

# Add the country code as a new column
top_20_df['country_code'] = top_20_df.index.map(country_codes)

print(top_20_df.head())

# Save the top 20 dataframe to a CSV file in the data folder
data_path = os.path.join('data', 'gdp_growth_top20.csv')
top_20_df.to_csv(data_path, index=True)

# Save the codes for the top 20 to a CSV file
codes_top20 = (top_20_df['country_code'])
path = os.path.join('data', 'codes_top20.csv')
codes_top20.to_csv(path)


# Connect to your PostgreSQL database
conn = psycopg2.connect(
        host='127.0.0.1',
        port='5433',
        database='postgres',
        user='postgres',
        password='tomas.36'
    )

cur = conn.cursor()

# Create the table if it doesn't exist
create_table_query = """
DROP TABLE IF EXISTS gdp_growth_top20;
CREATE TABLE IF NOT EXISTS gdp_growth_top20 (
    country TEXT,
    country_code TEXT,
    Y2013 NUMERIC,
    Y2014 NUMERIC,
    Y2015 NUMERIC,
    Y2016 NUMERIC,
    Y2017 NUMERIC,
    Y2018 NUMERIC,
    Y2019 NUMERIC,
    Y2020 NUMERIC,
    Y2021 NUMERIC,
    Y2022 NUMERIC,
    avg_growth_10yr NUMERIC
);
"""
cur.execute(create_table_query)
conn.commit()

# Prepare DataFrame for insertion
# Reset index so that 'country' becomes a column instead of the index
insert_df = top_20_df.reset_index()
insert_df.rename(columns={'index': 'country'}, inplace=True)

# prepend 'Y' to them to match the table schema.
for col in insert_df.columns:
    if col.isdigit():
        insert_df.rename(columns={col: 'Y' + col}, inplace=True)

# Now insert_df should have columns:
# ['country', 'Y2013', 'Y2014', ..., 'Y2022', 'avg_growth_10yr', 'country_code']

# Extract column names from DataFrame
cols = insert_df.columns.tolist()

# Convert DataFrame to list of tuples for insertion
values = [tuple(x) for x in insert_df.to_numpy()]

# Construct the INSERT statement
insert_stmt = f"INSERT INTO gdp_growth_top20 ({', '.join(cols)}) VALUES %s;"

# Execute the insertion using execute_values for efficiency
execute_values(cur, insert_stmt, values)
conn.commit()

print("Data successfully created and inserted into the gdp_growth_top20 table.")

# Close the connection
cur.close()
conn.close()