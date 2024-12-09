import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("averaged_full.csv")

corr_matrix = df.drop(columns=['year']).corr()

print(corr_matrix)

plt.figure(figsize=(16, 12))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm')
plt.title('Correlation Between Growth in GDP per Capita vs. Primary and Secondary Schooling\nEnrollment Rates on Average')

plt.savefig('figures/corr_matrix.png')
plt.show()