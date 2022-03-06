import pandas as pd
from pytrends.request import TrendReq
import seaborn as sns
import matplotlib.pyplot as plt

# Keyword code generation
pytrend = TrendReq()
keywords = ['Nike', 'Adidas', 'Under Armour', 'Zara', 'H&M', 'Louis Vuitton']
keyword_codes = [pytrend.suggestions(keyword=i)[0] for i in keywords]
df_codes = pd.DataFrame(keyword_codes)

# Parameters
exact_keywords = df_codes['mid'].to_list()
date_interval = '2020-01-01 2020-05-01'
countries = ['US', 'GB', 'DE']
category = 0
search_type = ''

# Generate trends for each iteration of country and keywords
individual_exact_keyword = list(zip(*[iter(exact_keywords)]*1))
individual_exact_keyword = [list(x) for x in individual_exact_keyword]
dicti = {}
i = 1
for country in countries:
    for keyword in individual_exact_keyword:
        pytrend.build_payload(kw_list=keyword, timeframe=date_interval, geo=country, cat=category, gprop=search_type)
        dicti[i] = pytrend.interest_over_time()
        i += 1
df_trends = pd.concat(dicti, axis=1)

# Data Cleanup
# Remove outside header
df_trends.columns = df_trends.columns.droplevel(0)
# Drop isPartial
df_trends = df_trends.drop('isPartial', axis=1)
# Reset Index
df_trends.reset_index(level=0, inplace=True)
# Change column name
df_trends.columns = ['date', 'Nike-US', 'Adidas-US', 'Under Armour-US', 'Zara-US' ,'H&M-US', 'Louis Vuitton-US',
                     'Nike-UK', 'Adidas-UK', 'Under Armour-UK', 'Zara-UK','H&M-UK', 'Louis Vuitton-UK', 'Nike-Germany',
                     'Adidas-Germany', 'Under Armour-Germany', 'Zara-Germany', 'H&M-Germany', 'Louis Vuitton-Germany']

# Data Visualization
sns.set(color_codes=True)
dx = df_trends.plot(figsize = (12, 8), x="date", y=['Louis Vuitton-US', 'Louis Vuitton-UK', 'Louis Vuitton-Germany'],
                    kind='line', title='Louis Vuitton Google Trends')
dx.set_xlabel('Date')
dx.set_ylabel('Trends Index')
dx.tick_params(axis='both', which='both', labelsize=10)
plt.show()