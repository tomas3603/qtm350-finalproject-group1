import pandas as pd
import os
import matplotlib.pyplot as plt

data = pd.read_csv('data/gdp_growth_top20.csv')

fig, ax = plt.subplots(figsize=(12, 6))

# Create a bar plot with countries on the x-axis and avg_growth_10yr on the y-axis
ax.bar(data['country'], data['avg_growth_10yr'], color='skyblue')

# Rotate x-axis labels for better readability
plt.xticks(rotation=45, ha='right')

# Add labels and title
plt.xlabel('Country')
plt.ylabel('Average GDP Growth (10-year)')
plt.title('Top 20 Countries by Average GDP Per Capita Growth in Sub-Saharan Africa, Latin America and the Carribean')

plt.tight_layout()

# Save the figure to the 'figures' folder with the title "top20_growth_hist"
plt.savefig('figures/top20_growth_hist.png')

plt.show()