import pandas as pd
import seaborn as sns

enrollment = pd.read_csv("data/avg_enrollment.csv")
tertiary = pd.read_csv("data/tertiary_enrollment.csv")
import matplotlib.pyplot as plt

long_enrollment = (enrollment.melt(id_vars=['country_name'], var_name='year', value_name='enrollment_rate'))

long_enrollment['year'] = long_enrollment['year'].astype(int)

# Create the line plot
fig, ax = plt.subplots(figsize=(10, 6))
ax.tick_params(axis='x', rotation=45)

# Group by country and plot each group's data
for ctry, enrollment in long_enrollment.groupby('country_name'):
    color = 'black' if ctry == 'World' else None
    ax.plot(enrollment['year'], enrollment['enrollment_rate'], label=ctry, marker='o', color=color)

# Set x-axis ticks to integer years
years = sorted(long_enrollment['year'].unique())
ax.set_xticks(years)

# Labeling the plot
ax.set_xlabel('Year')
ax.set_ylabel('Average of Primary and Secondary Schooling Enrollment Rate (gross %)')
ax.set_title('Average of Primary and Secondary Enrollment Rates Over Time (2003-2022)')

# Create a legend
ax.legend(title='Country', bbox_to_anchor=(1.05, 1), loc='upper left')

plt.tight_layout()
plt.savefig('figures/enrollment_rates.png')
plt.show()


long_df = (tertiary.melt(id_vars=['country_name'], var_name='year', value_name='tertiary_enrollment_rate'))

# Create the line plot
fig, ax = plt.subplots(figsize=(10, 6))
ax.tick_params(axis='x', rotation=45)

# Group by country and plot each group's data
for ctry, enrollment in long_df.groupby('country_name'):
    color = 'black' if ctry == 'World' else None
    ax.plot(enrollment['year'], enrollment['tertiary_enrollment_rate'], label=ctry, marker='o', color=color)

# Set x-axis ticks to integer years
years = (long_df['year'].unique())
ax.set_xticks(years)

# Labeling the plot
ax.set_xlabel('Year')
ax.set_ylabel('Tertiary Schooling Enrollment Rate (gross %)')
ax.set_title('Tertiary Enrollment Rates Over Time (2003-2022)')

# Create a legend
ax.legend(title='Country', bbox_to_anchor=(1.05, 1), loc='upper left')

plt.tight_layout()
plt.savefig('figures/tertiary_enrollment_rates.png')
plt.show()
