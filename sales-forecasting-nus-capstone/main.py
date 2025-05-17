from Transformer import DataTransform
from Model import WinterHolts

from pyfiglet import figlet_format
import pickle
import pandas as pd
import time
import os


def daily_prediction(df):
    filtered_df = df.query('Day == 1')
    filtered_df['Predicted Sales'].tolist()
    prediction_string = ','.join(map(str, filtered_df['Predicted Sales']))
    return prediction_string


# def retrieveTrend(day_part):
#     trend = {
#         'Breakfast' : 'add',
#         'Lunch' : 'add',
#         'Snack' : 'add',
#         'Dinner' : 'mul',
#         'Late-nite' : 'add'
#     }

#     return trend[day_part]

# def retrieveSeasonal(day_part):
#     seasonal = {
#         'Breakfast' : 'mul',
#         'Lunch' : 'add',
#         'Snack' : 'mul',
#         'Dinner' : 'mul',
#         'Late-nite' : 'mul'
#     }

#     return seasonal[day_part]



if __name__ == '__main__':
    file_location = r'C:\Users\admin\Documents\Learning\MTech (EBAC)\Year 2\Capstone\Phase 2\Data\Data - No RegSales No Null Neg or 0.csv'
    day_parts = ['Breakfast','Lunch','Snack','Dinner','Late-nite']
    daily_forecast = []

    day_part_dict = {
        'Breakfast' : 3,
        'Lunch' : 3,
        'Snack' : 3,
        'Dinner' : 3,
        'Late-nite' : 4
    }

    print(figlet_format("Burger King",font = 'standard'))
    print(figlet_format("Sales Forecast",font = 'standard'))

    df = pd.read_csv(file_location)

    combined_df = pd.DataFrame()

    for day_part in day_parts:
        df_reader = DataTransform(df)
        df_reader.transformer(day_part)

        time.sleep(2)


        #trend = retrieveTrend(day_part)
        #seasonal = retrieveSeasonal(day_part)

        trend = 'add'
        seasonal = 'add'

        model = WinterHolts(df_reader.dataframe,trend,seasonal)
        model.forecast(7)
        model.evaluation(7)
        model.convert_forecast_dataframe(day_part,day_part_dict.get(day_part))
        combined_df = pd.concat([combined_df, model.predicted_dataframe], ignore_index=True)

        path = r'C:\Users\admin\Documents\Learning\MTech (EBAC)\Year 2\Capstone\Phase 2\Models'
        filename = f'{day_part}_model.pkl'
        full_path = os.path.join(path, filename)

        with open(full_path, 'wb') as file:
            pickle.dump(model, file)

        print("\n")


    prediction_string = daily_prediction(combined_df)

    result = ','.join(daily_forecast)

    # Write the text string to the file
    with open('daily_sales_forecast.txt', 'w') as file:
        file.write(prediction_string)




