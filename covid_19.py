import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import FuncFormatter
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 7)
plt.rcParams['axes.titlesize'] = 16
plt.rcParams['axes.labelsize'] = 14

df = pd.read_csv("C:/Users/COOL/Downloads/covid_data.csv")
df.columns = df.columns.str.replace(r'[/\s",]', '', regex=True)
df.rename(columns={'CountryRegion': 'Country',
                   'SeriousCritical': 'Serious_Critical',
                   'TotCases1Mpop': 'Cases_Per_Million',
                   'Deaths1Mpop': 'Deaths_Per_Million',
                   'Tests1Mpop': 'Tests_Per_Million',
                   'WHORegion': 'WHO_Region'}, inplace=True)

df.replace('', np.nan, inplace=True)
numerical_cols = ['Population', 'TotalCases', 'NewCases', 'TotalDeaths', 'NewDeaths', 
                  'TotalRecovered', 'NewRecovered', 'ActiveCases', 'Serious_Critical', 
                  'Cases_Per_Million', 'Deaths_Per_Million', 'TotalTests', 'Tests_Per_Million']
# using cahtgpt
for col in numerical_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    if col not in ['Cases_Per_Million', 'Deaths_Per_Million', 'Tests_Per_Million']:
        df[col] = df[col].astype(int)

df[['Continent', 'WHO_Region']] = df[['Continent', 'WHO_Region']].fillna('Unknown')
df['CFR_Percentage'] = np.where(df['TotalCases'] > 0, 
                                (df['TotalDeaths'] / df['TotalCases']) * 100, 
                                0
                                )

continent_summary = df.groupby('Continent').agg(
    TotalCases=('TotalCases', 'sum'),
    TotalDeaths=('TotalDeaths', 'sum'),
    Population=('Population', 'sum')
).reset_index()

continent_summary['Cases_Per_Million'] = np.where(continent_summary['Population'] > 0,
                                                  (continent_summary['TotalCases'] / continent_summary['Population']) * 1000000,
                                                  0)
print("Generating visualizations...")
top_10_countries = df.sort_values(by='TotalCases', ascending=False).head(10)
plt.figure(figsize=(12, 7))
ax = sns.barplot(
    x='TotalCases', 
    y='Country', 
    data=top_10_countries, 
    palette='rocket' 
)
plt.savefig("8_data_comparison.png", dpi=100)
ax.set_title('Top 10 Countries by Total COVID-19 Cases', pad=20)
ax.set_xlabel('Total Cases (in Millions)')
ax.set_ylabel('Country')
#chatgpt
def millions_formatter(x, pos):
    return f'{x/1000000:.1f}M'
ax.xaxis.set_major_formatter(FuncFormatter(millions_formatter))
plt.tight_layout()
plt.show()
plt.figure(figsize=(10, 6))
# Create the Matplotlib Bar Plot
plt.bar(
    continent_summary['Continent'], 
    continent_summary['Cases_Per_Million'], 
    color=sns.color_palette("Set2", len(continent_summary))
)
plt.title('COVID-19 Cases Per Million Population by Continent', pad=20)
plt.xlabel('Continent')
plt.ylabel('Cases per 1 Million Population')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig("9_data_comparison.png", dpi=200)

plt.show()
cfr_data = df[df['TotalCases'] >= 1000]

plt.figure(figsize=(10, 6))
# Create the Seaborn Histogram
sns.histplot(
    cfr_data['CFR_Percentage'], 
    bins=15, 
    kde=True,
    color='darkred',
    edgecolor='black'
)
plt.savefig("10_data_comparison.png", dpi=300)
plt.title('Distribution of Case Fatality Rate (CFR) across Countries (> 1000 Cases)', pad=20)
plt.xlabel('CFR Percentage (%) (Total Deaths / Total Cases)')
plt.ylabel('Number of Countries')
plt.legend()
plt.show()


