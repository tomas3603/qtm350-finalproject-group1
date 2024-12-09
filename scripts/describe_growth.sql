SELECT 
    COUNT(*) AS count_countries,
    AVG(avg_growth_10yr) AS mean_growth,
    MIN(avg_growth_10yr) AS min_growth,
    MAX(avg_growth_10yr) AS max_growth
FROM gdp_growth_top20;
