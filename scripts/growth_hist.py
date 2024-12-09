import pandas as pd
import matplotlib.pyplot as plt

# Read the data
data = pd.read_csv('data/gdp_growth_top20.csv')

# Extract the global average (World)
world_avg = data.loc[data['country'] == 'World', 'avg_growth_20yr'].values[0]

# Filter out the 'World' row from the DataFrame so we only have the top 20 countries
data_countries = data[data['country'] != 'World']

fig, ax = plt.subplots(figsize=(12, 6))

# Create a bar plot with countries on the x-axis and avg_growth_20yr on the y-axis
ax.bar(data_countries['country'], data_countries['avg_growth_20yr'], color='skyblue')

# Add a horizontal line at the global average
ax.axhline(y=world_avg, color='red', linestyle='--', label=f'World Avg: {world_avg:.2f}%')

# Rotate x-axis labels for better readability
plt.xticks(rotation=45, ha='right')

# Add labels and title
plt.xlabel('Country')
plt.ylabel('Average GDP Growth (20-year)')
plt.title('Top 20 Countries by Average GDP Per Capita Growth vs. Global Average')

# Add legend
ax.legend()

plt.tight_layout()

# Save the figure to the 'figures' folder with the title "top20_growth_hist"
plt.savefig('figures/top20_growth_hist.png')

plt.show()
