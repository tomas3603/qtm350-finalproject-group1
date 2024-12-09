import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

gdp = pd.read_csv("data/gdp_growth_top20.csv")
enrollment = pd.read_csv("data/top20_enrollment_growth.csv")

gdp.drop(columns=["avg_growth_20yr","country_code"], inplace=True)

top20_avg_growth_gdp = gdp.drop(columns=['country']).mean(axis=0)
top20_avg_growth_enrollment = enrollment.drop(columns=['country_name']).mean(axis=0)
avg_growth_df = pd.concat([top20_avg_growth_gdp, top20_avg_growth_enrollment], axis=1)
avg_growth_df.columns = ['avg_gdp_growth', 'avg_enrollment_growth']
avg_growth_df.index.name = 'year'

avg_growth_df.drop(avg_growth_df.tail(1).index, inplace=True)

corr_matrix = avg_growth_df.corr()

print(corr_matrix)

plt.figure(figsize=(8, 6))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm')
plt.title('Correlation Between Growth in GDP per Capita vs. Primary and Secondary Schooling\nEnrollment Rates on Average')
plt.show()