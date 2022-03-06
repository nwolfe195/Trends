import pandas as pd
from pytrends.request import TrendReq


class TrendsData:
    def __init__(self, keywords, start_date, end_date, countries):
        pytrend = TrendReq()
        # Generate keyword codes
        keyword_codes = [pytrend.suggestions(keyword=i)[0] for i in keywords]
        # Convert to dataframe
        df_codes = pd.DataFrame(keyword_codes)
        # Gather exact keywords
        exact_keywords = df_codes['mid'].to_list()
        # Create date interval
        date_interval = '%s %s' % (start_date, end_date)
        # Generate trends for each iteration of country and keywords
        individual_exact_keyword = list(zip(*[iter(exact_keywords)] * 1))
        individual_exact_keyword = [list(x) for x in individual_exact_keyword]
        dict = {}
        i = 1
        for country in countries:
            for keyword in individual_exact_keyword:
                pytrend.build_payload(kw_list=keyword, timeframe=date_interval, geo=country, cat=0, gprop='')
                dict[i] = pytrend.interest_over_time()
                i += 1
        df_trends = pd.concat(dict, axis=1)
        # Remove outside header
        df_trends.columns = df_trends.columns.droplevel(0)
        # Drop isPartial
        df_trends = df_trends.drop('isPartial', axis=1)
        # Reset Index
        df_trends.reset_index(level=0, inplace=True)
        print(df_trends)
