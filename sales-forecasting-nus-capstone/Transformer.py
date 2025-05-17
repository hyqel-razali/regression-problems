
import pandas as pd
import numpy as np

class DataTransform():
    def __init__(self,dataframe):
        self.dataframe = dataframe

    def display_contents(self):
        if self.dataframe is not None:
            print(self.dataframe)
        else:
            print("Dataframe was not loaded. Please load before attempting to display the contents.")

    def reformat_date(self):
        print("#####################      Date Reformatting In-Progress      #####################")

        # Reformat date column to a datetime object
        self.dataframe['Calendar Date'] = pd.to_datetime(self.dataframe['Calendar Date'],format = '%d/%m/%Y')


        end_date = pd.Timestamp('2023-12-31')
        start_date = (end_date - pd.DateOffset(months=11)) +  pd.DateOffset(day=1)   

        self.dataframe = self.dataframe[(self.dataframe['Calendar Date'] >= start_date) & (self.dataframe['Calendar Date'] <= end_date)]

        print("#####################      Date Reformatting Completed        #####################")


    def aggregate_sales(self):
        self.dataframe['Total Sales'] =  self.dataframe['Total Sales'].round(0).astype(int)
        self.dataframe = self.dataframe.groupby(['Calendar Date'])['Total Sales'].sum().reset_index()
        self.display_contents()


    def filter(self,day_part):
        print("#####################     Day Part Filtering In-Progress      #####################")
        self.dataframe =  self.dataframe[self.dataframe['Day Part'] == day_part]

        q1 = np.percentile(self.dataframe['Total Sales'], 25)
        q2 = np.percentile(self.dataframe['Total Sales'], 50)
        q3 = np.percentile(self.dataframe['Total Sales'], 75)
        iqr1 = q2 - q1
        iqr2 = q3 - q2
        iqr3 = np.percentile(self.dataframe['Total Sales'], 75) - np.percentile(self.dataframe['Total Sales'], 25)

        self.dataframe =  pd.DataFrame(self.dataframe[(self.dataframe['Total Sales'] > iqr1/1.5) | (self.dataframe['Total Sales'] < iqr3*1.5)])
        print("#####################      Day Part Filtering Completed       #####################")


    def fill_missing_dates(self):
        print("#####################        Fill NA Dates In-Progress        #####################")
        # Detect the rows that are missing
        full_date_range = pd.date_range(start='2021-01-01', end='2023-12-31')
        full_date_range = pd.date_range(start='2023-01-01', end='2023-12-31')

        dates_in_df = pd.to_datetime(self.dataframe['Calendar Date'])
        missing_dates = full_date_range.difference(dates_in_df)

        # Print the missing dates
        #print("\nMissing Dates:")
        #print(missing_dates)

        self.dataframe.set_index('Calendar Date',inplace=True)

        # Reindex the DataFrame to include the complete date range
        self.dataframe = self.dataframe.reindex(full_date_range)

        median_2023 = self.dataframe.loc['2023', 'Total Sales'].median()
        self.dataframe.loc['2023', 'Total Sales'] = self.dataframe.loc['2023', 'Total Sales'].fillna(median_2023)
        self.dataframe.reset_index(inplace=True)

        self.dataframe.rename(columns={'index': 'Calendar Date'}, inplace=True)

        # Convert the values to integers
        self.dataframe['Total Sales'] = self.dataframe['Total Sales'].astype(int)
        print("#####################         Fill NA Dates Completed         #####################")

        
    def sort_dates(self):
        print("#####################        Sorting Dates In-Progress        #####################")
        self.dataframe.sort_values('Calendar Date', inplace=True)
        self.dataframe['Date'] = (self.dataframe['Calendar Date'] - self.dataframe['Calendar Date'].min()).dt.days
        print("#####################         Sorting Dates Completed         #####################")


    def export_csv(self):
        self.dataframe.to_csv("transformed_data.csv")

    def transformer(self,day_part):
        upper_daypart = day_part.upper()
        print("\n")
        print(f"@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ {upper_daypart} @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        print("##################### Initiate Data Transformation Procedure  #####################")

        self.filter(day_part)
        self.reformat_date()
        self.aggregate_sales()
        self.fill_missing_dates()
        self.sort_dates()

        self.export_csv()
        print("##################### Data Transformation Procedure Completed #####################")
        print('\n')
