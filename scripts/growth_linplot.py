import pandas as pd
import matplotlib.pyplot as plt

growth_data = pd.read_csv('data/gdp_growth_top20.csv')
growth_data.drop(columns=['country_code', 'avg_growth_20yr'], inplace=True)

# Melt the DataFrame so that 'year' becomes a variable column and 'value' holds the gdp growth
long_df = growth_data.melt(id_vars='country', var_name='year', value_name='gdp_growth')

# Convert 'year' to a numeric type if it's not already
long_df['year'] = long_df['year'].astype(int)

# Create the line plot
fig, ax = plt.subplots(figsize=(10, 6))

# Group by country and plot each group's data
for ctry, grp in long_df.groupby('country'):
    ax.plot(grp['year'], grp['gdp_growth'], label=ctry, marker='o')

# Set x-axis ticks to integer years
years = sorted(long_df['year'].unique())
ax.set_xticks(years)

# Labeling the plot
ax.set_xlabel('Year')
ax.set_ylabel('GDP per Capita Growth (%)')
ax.set_title('GDP per Capita Growth Over Time (2003-2022)')

# Create a legend
ax.legend(title='Country', bbox_to_anchor=(1.05, 1), loc='upper left')

plt.tight_layout()

# Save the plot to the figures folder
plt.savefig('figures/growth_lineplot.png')

plt.show()