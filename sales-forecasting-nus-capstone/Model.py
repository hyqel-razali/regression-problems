from Transformer import DataTransform
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from sklearn.metrics import mean_squared_error, mean_absolute_error
import numpy as np
import time
import pandas as pd
import warnings
warnings.filterwarnings("ignore")

class WinterHolts():
    def __init__(self,dataframe,trend,seasonal):
        print("#####################              Model Creation             #####################")
        np.random.seed(99)
        self.dataframe = dataframe
        self.model = ExponentialSmoothing(self.dataframe['Total Sales'],trend= trend, seasonal=seasonal, seasonal_periods=6)
        self.fit_model = self.model.fit(smoothing_level=0.1,smoothing_trend = 0.1, smoothing_seasonal = 0.1)
        self.forecasted_value = None
        self.value = None
        self.predicted_dataframe = None
        

    def forecast(self,value):
        print("#####################             Model Forecasting           #####################")
        self.value = value
        self.forecasted_value = self.fit_model.forecast(self.value)  # Forecast the next 5 periods

    def evaluation(self,value):
        print("#####################              Model Evaluation           #####################")

        # Display predictions
        #print("Predictions:", y_pred)
        
        actual_value = self.dataframe['Total Sales'].values[-value:]  # Assuming last 5 actual values for comparison
        mae = mean_absolute_error(actual_value, self.forecasted_value)
        print(f"Mean Absolute Error (MAE): {mae}")

        # Calculate Mean Squared Error (MSE)
        mse = mean_squared_error(actual_value, self.forecasted_value)
        print(f"Mean Squared Error (MSE): {mse}")

        # Calculate Root Mean Squared Error (RMSE)
        rmse = np.sqrt(mse)
        print(f"Root Mean Squared Error (RMSE): {rmse}")


    def convert_forecast_dataframe(self,day_part,multiplier):

        self.predicted_dataframe = pd.DataFrame({
        'Day Part' : day_part,
        'Day': range(1, self.value + 1),
        'Predicted Sales': self.forecasted_value.astype(int)})

        # Create a new DataFrame by repeating each row 'multiplier' times
        self.predicted_dataframe = pd.DataFrame(
            self.predicted_dataframe.values.repeat(multiplier, axis=0), 
            columns=self.predicted_dataframe.columns
        )

        # If needed, reset the index or create a new column to reflect the new row number
        self.predicted_dataframe = self.predicted_dataframe.reset_index(drop=True)

