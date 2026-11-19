import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from pathlib import Path

YEARS = range(2015, 2020)
Path("images").mkdir(exist_ok=True)

# ---------- Load + unify column names ----------
COLS = {
    "Country": "country", "Country or region": "country",
    "Region": "region",
    "Happiness Rank": "rank", "Happiness.Rank": "rank", "Overall rank": "rank",
    "Happiness Score": "score", "Happiness.Score": "score", "Score": "score",
    "Economy (GDP per Capita)": "gdp", "Economy..GDP.per.Capita.": "gdp", "GDP per capita": "gdp",
    "Health (Life Expectancy)": "health", "Health..Life.Expectancy.": "health", "Healthy life expectancy": "health",
    "Freedom": "freedom", "Freedom to make life choices": "freedom",
    "Trust (Government Corruption)": "corruption", "Trust..Government.Corruption.": "corruption",
    "Perceptions of corruption": "corruption",
    "Generosity": "generosity",
}
KEEP = ["country", "region", "rank", "score", "gdp", "health", "freedom", "corruption", "generosity", "year"]

# Same country written differently in different years
NAME_FIX = {
    "Somaliland region": "Somaliland Region",
    "Hong Kong S.A.R., China": "Hong Kong",
    "Taiwan Province of China": "Taiwan",
    "Northern Cyprus": "North Cyprus",
    "Trinidad & Tobago": "Trinidad and Tobago",
    "Macedonia": "North Macedonia",
}

def load(year):
    df = pd.read_csv(f"data/{year}.csv").rename(columns=COLS)
    df["country"] = df["country"].str.strip().replace(NAME_FIX)
    df["year"] = year
    if "region" not in df.columns:      # 2017-2019 have no region column
        df["region"] = pd.NA
    return df[KEEP]

data = {y: load(y) for y in YEARS}

# Fill region for later years using the 2015/2016 files
region_map = (pd.concat([data[2015], data[2016]])
              .dropna(subset=["region"])
              .drop_duplicates("country")
              .set_index("country")["region"])
for y in YEARS:
    data[y]["region"] = data[y]["region"].fillna(data[y]["country"].map(region_map))

# ---------- Task 1: score distribution ----------
for y, df in data.items():
    plt.figure(figsize=(7, 4))
    plt.hist(df["score"], bins=15, edgecolor="black")
    plt.title(f"Distribution of Happiness Score, {y}")
    plt.xlabel("Happiness Score"); plt.ylabel("Number of countries")
    plt.tight_layout(); plt.savefig(f"images/task1_score_hist_{y}.png", dpi=150); plt.close()

# ---------- Tasks 2 and 3: labeled scatter plots ----------
def scatter(xcol, ycol, xlabel, ylabel, prefix):
    for y, df in data.items():
        d = df.dropna(subset=[xcol, ycol])
        plt.figure(figsize=(10, 7))
        plt.scatter(d[xcol], d[ycol], s=18)
        for _, r in d.iterrows():
            plt.annotate(r["country"], (r[xcol], r[ycol]), fontsize=5, alpha=0.7)
        plt.title(f"{xlabel} vs {ylabel}, {y}")
        plt.xlabel(xlabel); plt.ylabel(ylabel)
        plt.tight_layout(); plt.savefig(f"images/{prefix}_{y}.png", dpi=200); plt.close()

scatter("gdp", "health", "GDP per Capita", "Health", "task2_gdp_health")
scatter("freedom", "generosity", "Freedom", "Generosity", "task3_freedom_generosity")

# ---------- Task 4: 3D scatter (GDP, Corruption, Generosity) ----------
for y, df in data.items():
    d = df.dropna(subset=["gdp", "corruption", "generosity"])
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection="3d")
    ax.scatter(d["gdp"], d["corruption"], d["generosity"], s=15)
    for _, r in d.iterrows():
        ax.text(r["gdp"], r["corruption"], r["generosity"], r["country"], fontsize=4)
    ax.set_xlabel("GDP per Capita"); ax.set_ylabel("Corruption"); ax.set_zlabel("Generosity")
    ax.set_title(f"GDP vs Corruption vs Generosity, {y}")
    plt.tight_layout(); plt.savefig(f"images/task4_3d_{y}.png", dpi=200); plt.close()

# ---------- Task 5: countries missing between consecutive years ----------
for a, b in zip(YEARS, list(YEARS)[1:]):
    ca, cb = set(data[a]["country"]), set(data[b]["country"])
    print(f"\n{a} -> {b}")
    print("  in", a, "but not", b, ":", sorted(ca - cb))
    print("  in", b, "but not", a, ":", sorted(cb - ca))

# ---------- Task 6: correlations ----------
PAIRS = [("score", "generosity"), ("freedom", "generosity"),
         ("gdp", "corruption"), ("gdp", "freedom")]
rows = []
for y, df in data.items():
    for a, b in PAIRS:
        d = df[[a, b]].dropna()
        rows.append({"year": y, "pair": f"{a} & {b}",
                     "pearson": d[a].corr(d[b], method="pearson"),
                     "spearman": d[a].corr(d[b], method="spearman"),
                     "kendall": d[a].corr(d[b], method="kendall")})
corr = pd.DataFrame(rows).round(3)
print("\nTask 6 correlations:\n", corr.to_string(index=False))
corr.to_csv("images/task6_correlations.csv", index=False)

# ---------- Task 7: which variables relate most strongly to score ----------
VARS = ["gdp", "health", "freedom", "corruption", "generosity"]
rows = []
for y, df in data.items():
    for v in VARS:
        d = df[["score", v]].dropna()
        rows.append({"year": y, "variable": v,
                     "pearson": d["score"].corr(d[v], method="pearson"),
                     "spearman": d["score"].corr(d[v], method="spearman")})
rel = pd.DataFrame(rows).round(3)
print("\nTask 7: Pearson correlation with happiness score:")
print(rel.pivot(index="variable", columns="year", values="pearson"))
print("\nAverage Pearson across years (strongest first):")
print(rel.groupby("variable")["pearson"].mean().sort_values(ascending=False).round(3))

plt.figure(figsize=(8, 4))
sns.heatmap(rel.pivot(index="variable", columns="year", values="pearson"),
            annot=True, cmap="coolwarm", vmin=-1, vmax=1)
plt.title("Pearson correlation with Happiness Score")
plt.tight_layout(); plt.savefig("images/task7_score_correlations.png", dpi=150); plt.close()

# ---------- Task 8: world map of happiness score ----------
for y, df in data.items():
    fig = px.choropleth(df, locations="country", locationmode="country names",
                        color="score", color_continuous_scale="Viridis",
                        title=f"Happiness Score by Country, {y}")
    fig.write_html(f"images/task8_map_{y}.html")      # always works
    try:
        fig.write_image(f"images/task8_map_{y}.png", width=1200, height=700)
    except Exception as e:
        print(f"PNG export failed for {y}: {e}")

# ---------- Task 9: rank trends by year and by region ----------
by_region = (pd.concat(data.values())
             .dropna(subset=["region"])
             .groupby(["region", "year"])["rank"].mean().unstack("year").round(1))
print("\nTask 9: average happiness rank by region and year:\n", by_region)

plt.figure(figsize=(11, 6))
for region, row in by_region.iterrows():
    plt.plot(row.index, row.values, marker="o", label=region)
plt.gca().invert_yaxis()                  # rank 1 = happiest, so lower is better
plt.xticks(list(YEARS)); plt.xlabel("Year"); plt.ylabel("Average rank (lower = happier)")
plt.title("Average Happiness Rank by Region")
plt.legend(fontsize=7, bbox_to_anchor=(1.01, 1), loc="upper left")
plt.tight_layout(); plt.savefig("images/task9_rank_by_region.png", dpi=150); plt.close()
