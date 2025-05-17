
import pickle
import pandas as pd
import os

day_parts = ['Breakfast','Lunch','Snack','Dinner','Late-nite']
combined_df = pd.DataFrame()
day_part_dict = {
        'Breakfast' : 3,
        'Lunch' : 3,
        'Snack' : 3,
        'Dinner' : 3,
        'Late-nite' : 4
    }


for day_part in day_parts:
    # Location of the models
    path = r'C:\Users\admin\Documents\Learning\MTech (EBAC)\Year 2\Capstone\Phase 2\Models'
    filename = f'{day_part}_model.pkl'
    full_path = os.path.join(path, filename)

    with open(full_path, 'rb') as file:
        # Load the mode
        loaded_model = pickle.load(file)

        # Forecast
        loaded_model.forecast(7)

        # Make a dataframe for the forecasted data.
        loaded_model.convert_forecast_dataframe(day_part,day_part_dict.get(day_part))

        # Merge all the dataframe together into 1
        combined_df = pd.concat([combined_df, loaded_model.predicted_dataframe], ignore_index=True)

# The dataframe to be used in Streamlit
unique_df = combined_df.drop_duplicates(subset=['Day Part', 'Day'])

