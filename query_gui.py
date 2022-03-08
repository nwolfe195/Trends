from tkinter import *
from pytrends_processing import *
import matplotlib.pyplot as plt
from tkcalendar import DateEntry
from datetime import datetime


class MainApplication(Frame):
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
        Button(text='Search Trend!', command=self.search).grid(row=4, column=0, columnspan=2)

    def search(self):
        keywords_input = self.keywords.get("1.0", "end")
        keywords = [x.strip() for x in keywords_input.split(',')]
        start_date = str(datetime.strptime(self.start_date.get(), '%m/%d/%y').date())
        end_date = str(datetime.strptime(self.end_date.get(), '%m/%d/%y').date())
        countries = ['US']
        keyword_search_results = TrendsData(keywords, start_date, end_date, countries).get_trends()
        self.graph(keyword_search_results)

    def graph(self, data):
        data.set_index('date').plot(kind='line')
        print(data)
        plt.show()


if __name__ == "__main__":
    root = Tk()
    root.title('Google Trend Search')
    root.geometry('500x250')
    MainApplication(root)
    root.mainloop()