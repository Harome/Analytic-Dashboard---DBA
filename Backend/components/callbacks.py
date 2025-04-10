from dash import callback
from dash.dependencies import Input, Output
import pandas as pd

data = pd.read_csv(r"D:\zDonludoz\Git\Analytic-Dashboard---DBA\Data\Raw data\sample_data.csv")

def register_callbacks(app):
    @app.callback(
        Output('output-component-id', 'children'),
        Input('input-component-id', 'value')
    )
    def update_output(input_value):
        if not input_value:  
            return "Please enter a value."

        filtered_data = data[data['column_name'].astype(str) == str(input_value)]  # ✅ Ensure correct data type

        if filtered_data.empty:  
            return "No matching data found."

        return f'Filtered Data: {filtered_data.to_dict(orient="records")}'  # ✅ Convert DataFrame to JSON format
