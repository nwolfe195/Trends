from tkinter import *
from pytrends_processing import *
import matplotlib.pyplot as plt
from tkcalendar import DateEntry
from datetime import datetime
import numpy as np


class QueryGui(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        Label(text='Trend Keywords (separate with commas)').grid(row=0, column=0)
        self.keywords = Text(height=1, width=30)
        self.keywords.grid(row=0, column=1)
        Label(text='Countries').grid(row=1, column=0)
        Label(text='For now, just US').grid(row=1, column=1)
        Label(text='Start Date').grid(row=2, column=0)
        self.start_date = DateEntry()
        self.start_date.grid(row=2, column=1)
        Label(text='End Date').grid(row=3, column=0)
        self.end_date = DateEntry()
        self.end_date.grid(row=3, column=1)
        Button(text='Search Trend', command=self.trend_graph).grid(row=4, column=0, columnspan=2)
        Button(text='Get Correlation', command=self.correlation).grid(row=5, column=0, columnspan=2)

    def trend_graph(self):
        data = self.search()
        data.set_index('date').plot(kind='line')
        plt.show()

    def correlation(self):
        data = self.search()
        corr = data.corr()
        stack = corr.stack()
        no_self_pair = stack[stack.index.get_level_values(0) != stack.index.get_level_values(1)]
        no_self_or_dup_pair = no_self_pair[no_self_pair.index.get_level_values(0) < no_self_pair.index.get_level_values(1)]
        no_self_or_dup_pair_df = no_self_or_dup_pair.to_frame()

    def search(self):
        keywords_input = self.keywords.get("1.0", "end")
        keywords = [x.strip() for x in keywords_input.split(',')]
        start_date = str(datetime.strptime(self.start_date.get(), '%m/%d/%y').date())
        end_date = str(datetime.strptime(self.end_date.get(), '%m/%d/%y').date())
        countries = ['US']
        keyword_search_results = TrendsData(keywords, start_date, end_date, countries).get_trends()
        return keyword_search_results


if __name__ == "__main__":
    root = Tk()
    root.title('Google Trend Search')
    root.geometry('500x250')
    QueryGui(root)
    root.mainloop()