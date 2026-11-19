# World Happiness Report Analysis (2015-2019)

Exploratory data analysis of the World Happiness Report using Python (pandas, matplotlib, seaborn, plotly).
All code is in `eda.py`; all figures are saved in `images/`. The raw data files are confidential and are not included in this repository.

## How to run
```
uv venv elation
elation\Scripts\activate
uv pip install pandas matplotlib seaborn scipy plotly kaleido
python eda.py
```

## Data preparation
Column names differ between years, so they were renamed to a common set (score, gdp, health, freedom, corruption, generosity, rank, country). Some countries are spelled differently across years (for example "Hong Kong" and "Hong Kong S.A.R., China"), so names were standardized before comparing years. Only the 2015 and 2016 files contain a region column, so regions for 2017-2019 were filled in from those files.

## Answers

**1. Distribution of the happiness score** (`images/task1_score_hist_*.png`)
[Describe the shape you see: for example, roughly bell-shaped or skewed, where most scores fall, and whether it looks similar across the five years.]

**2. GDP per Capita vs Health** (`images/task2_gdp_health_*.png`)
[Describe the relationship you see: for example, a clear positive relationship where richer countries tend to have higher life expectancy scores. Mention one or two outliers if you notice any.]

**3. Freedom vs Generosity** (`images/task3_freedom_generosity_*.png`)
[Describe it: the correlations below are moderate and positive, so the points should show a loose upward trend with a lot of scatter.]

**4. GDP per Capita, Corruption and Generosity in 3D** (`images/task4_3d_*.png`)
[Describe what you see: for example, countries with higher GDP tend to have higher corruption-trust scores, while generosity does not follow a clear pattern.]

**5. Countries missing between consecutive years**
- 2015 to 2016:   in 2015 but not 2016 : ['Central African Republic', 'Djibouti', 'Lesotho', 'Mozambique', 'Oman', 'Swaziland']
  in 2016 but not 2015 : ['Belize', 'Namibia', 'Puerto Rico', 'Somalia', 'South Sudan']
- 2016 to 2017: missing in 2017: Comoros, Laos, Puerto Rico, Somaliland Region, Suriname. New in 2017: Central African Republic, Lesotho, Mozambique.
- 2017 to 2018: no countries dropped. New in 2018: Laos.
- 2018 to 2019: missing in 2019: Angola, Belize, Sudan. New in 2019: Comoros, Gambia, Swaziland.

Spelling variants were standardized first, so these are genuine differences between the files.

**6. Correlation coefficients** (full table in `images/task6_correlations.csv`)

| Pair | Pearson (2015 to 2019) | Notes |
|---|---|---|
| Score and Generosity | 0.18 down to 0.08 | weak, fading over time |
| Freedom and Generosity | 0.37 down to 0.27 | moderate positive, strongest of the four |
| GDP and Corruption | about 0.29 to 0.35 | modest positive |
| GDP and Freedom | about 0.33 to 0.38 | moderate positive |

Spearman and Kendall show the same pattern as Pearson, with Kendall values smaller, which is normal for that coefficient. The "corruption" variable measures trust in government (higher means better), so the positive link with GDP means wealthier countries tend to score better on it. Correlation does not show causation.

**7. Variables most related to happiness** (`images/task7_score_correlations.png`)
Average Pearson correlation with the happiness score across the five years:
GDP per capita 0.80, Health 0.77, Freedom 0.56, Corruption (trust) 0.40, Generosity 0.14.
GDP and health are the strongest, and generosity is the weakest. The ordering is the same in every year.

**8. World map of happiness scores** (`images/task8_map_*.png` and `.html`)
[Describe the pattern: for example, which regions look happiest and which least happy.]

**9. Rank trends by year and region** (`images/task9_rank_by_region.png`)
Lower rank means happier. Average rank by region:

| Region | 2015 | 2019 |
|---|---|---|
| Australia and New Zealand | 9.5 | 9.5 |
| North America | 10.0 | 14.0 |
| Western Europe | 29.5 | 23.4 |
| Latin America and Caribbean | 46.9 | 51.4 |
| Eastern Asia | 64.5 | 64.8 |
| Central and Eastern Europe | 79.0 | 71.0 |
| Middle East and Northern Africa | 77.6 | 84.9 |
| Southeastern Asia | 81.2 | 85.1 |
| Southern Asia | 113.1 | 115.9 |
| Sub-Saharan Africa | 127.9 | 124.9 |

Western Europe and Central and Eastern Europe improved, while North America, the Middle East and Northern Africa, and Southeastern Asia moved down. Regional averages are also affected by countries entering and leaving the dataset.