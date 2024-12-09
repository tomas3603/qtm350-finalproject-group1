import pandas as pd


gdp = pd.read_csv("data/gdp_growth_top20.csv")
enrollment = pd.read_csv("data/avg_enrollment_growth.csv")
tertiary = pd.read_csv("data/tertiary_enrollment_growth.csv")
expend = pd.read_csv("data/edu_expenditure_growth.csv")

# Remove the country 'World' if it exists in any of these dataframes
gdp = gdp[gdp['country'] != 'World']
enrollment = enrollment[enrollment['country_name'] != 'World']
tertiary = tertiary[tertiary['country_name'] != 'World']
expend = expend[expend['country_name'] != 'World']



gdp.drop(columns=["avg_growth_20yr","country_code"], inplace=True)

avg_gdp = gdp.drop(columns=['country']).mean(axis=0)
avg_enrollment = enrollment.drop(columns=['country_name']).mean(axis=0)

tertiary.columns = [col[1:] if col.startswith('y') else col for col in tertiary.columns]
expend.columns = [col[1:] if col.startswith('y') else col for col in expend.columns]

avg_tertiary = tertiary.drop(columns=['country_name']).mean(axis=0)
avg_expend = expend.drop(columns=['country_name']).mean(axis=0)

avg_full_df = pd.concat([avg_gdp, avg_enrollment, avg_tertiary, avg_expend], axis=1)



avg_full_df.columns = ['avg_gdp_growth', 'avg_enrollment_growth', 'avg_tertiary_enrollment_growth', 'avg_expenditure_on_edu_growth']
avg_full_df.index.name = 'year'

avg_full_df.drop(avg_full_df.tail(1).index, inplace=True)

print(avg_full_df)

avg_full_df.to_csv("data/averaged_full.csv")
