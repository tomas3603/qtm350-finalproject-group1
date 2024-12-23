import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
import numpy as np

tertiary = pd.read_csv("data/tertiary_enrollment.csv")

df = pd.read_csv("data/averaged_full.csv")
y = df['avg_gdp_growth']
x = df['avg_tertiary_enrollment_growth']

x = x.values.reshape(-1, 1)

model = LinearRegression()
model.fit(x, y)

y_pred = model.predict(x)

plt.figure(figsize=(10, 6))
sns.scatterplot(x=x.flatten(), y=y, label='Data')
plt.plot(x, y_pred, color='red', label='Regression Line')
plt.xlabel('Average Tertiary Enrollment Growth')
plt.ylabel('Average GDP Growth')
plt.title('Linear Regression of GDP Growth on Tertiary Enrollment Growth')
plt.legend()
plt.savefig('figures/regression_plot.png')
plt.show()