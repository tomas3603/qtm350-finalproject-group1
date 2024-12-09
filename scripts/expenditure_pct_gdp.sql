DROP TABLE IF EXISTS expenditure_by_gdp;

CREATE TABLE expenditure_by_gdp AS
WITH country_stats AS (
    SELECT country_name,
           AVG(gov_expenditure_edu_pct_gdp) AS country_avg,
           COUNT(gov_expenditure_edu_pct_gdp) AS nonnull_count
    FROM education_data
    WHERE year BETWEEN 2003 AND 2022
    GROUP BY country_name
    HAVING COUNT(gov_expenditure_edu_pct_gdp) >= 15
)
SELECT 
    ed.country_name,
    COALESCE(MAX(CASE WHEN year = 2003 THEN gov_expenditure_edu_pct_gdp END), cs.country_avg) AS Y2003,
    COALESCE(MAX(CASE WHEN year = 2004 THEN gov_expenditure_edu_pct_gdp END), cs.country_avg) AS Y2004,
    COALESCE(MAX(CASE WHEN year = 2005 THEN gov_expenditure_edu_pct_gdp END), cs.country_avg) AS Y2005,
    COALESCE(MAX(CASE WHEN year = 2006 THEN gov_expenditure_edu_pct_gdp END), cs.country_avg) AS Y2006,
    COALESCE(MAX(CASE WHEN year = 2007 THEN gov_expenditure_edu_pct_gdp END), cs.country_avg) AS Y2007,
    COALESCE(MAX(CASE WHEN year = 2008 THEN gov_expenditure_edu_pct_gdp END), cs.country_avg) AS Y2008,
    COALESCE(MAX(CASE WHEN year = 2009 THEN gov_expenditure_edu_pct_gdp END), cs.country_avg) AS Y2009,
    COALESCE(MAX(CASE WHEN year = 2010 THEN gov_expenditure_edu_pct_gdp END), cs.country_avg) AS Y2010,
    COALESCE(MAX(CASE WHEN year = 2011 THEN gov_expenditure_edu_pct_gdp END), cs.country_avg) AS Y2011,
    COALESCE(MAX(CASE WHEN year = 2012 THEN gov_expenditure_edu_pct_gdp END), cs.country_avg) AS Y2012,
    COALESCE(MAX(CASE WHEN year = 2013 THEN gov_expenditure_edu_pct_gdp END), cs.country_avg) AS Y2013,
    COALESCE(MAX(CASE WHEN year = 2014 THEN gov_expenditure_edu_pct_gdp END), cs.country_avg) AS Y2014,
    COALESCE(MAX(CASE WHEN year = 2015 THEN gov_expenditure_edu_pct_gdp END), cs.country_avg) AS Y2015,
    COALESCE(MAX(CASE WHEN year = 2016 THEN gov_expenditure_edu_pct_gdp END), cs.country_avg) AS Y2016,
    COALESCE(MAX(CASE WHEN year = 2017 THEN gov_expenditure_edu_pct_gdp END), cs.country_avg) AS Y2017,
    COALESCE(MAX(CASE WHEN year = 2018 THEN gov_expenditure_edu_pct_gdp END), cs.country_avg) AS Y2018,
    COALESCE(MAX(CASE WHEN year = 2019 THEN gov_expenditure_edu_pct_gdp END), cs.country_avg) AS Y2019,
    COALESCE(MAX(CASE WHEN year = 2020 THEN gov_expenditure_edu_pct_gdp END), cs.country_avg) AS Y2020,
    COALESCE(MAX(CASE WHEN year = 2021 THEN gov_expenditure_edu_pct_gdp END), cs.country_avg) AS Y2021,
    COALESCE(MAX(CASE WHEN year = 2022 THEN gov_expenditure_edu_pct_gdp END), cs.country_avg) AS Y2022
FROM education_data ed
JOIN country_stats cs ON ed.country_name = cs.country_name
WHERE ed.year BETWEEN 2003 AND 2022
GROUP BY ed.country_name, cs.country_avg;
