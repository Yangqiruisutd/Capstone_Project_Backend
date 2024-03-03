import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
import sys
import json

def train_and_evaluate(csv_file_path, model_type='RandomForest'):
    # Step 1: Read the CSV file into a pandas DataFrame
    df = pd.read_csv(csv_file_path)

    # Step 2: Remove commas from numeric columns and convert them to float
    numeric_cols = ['Total (kWh)', 'kWh per Rm. Nights', 'On-Peak(kWh)', 'On Peak per RM', 'Off-Peak(kWh)',
                    'Off Peak per RM', 'Demand (kW)', 'Rm. night', 'Mean Temperature BKK', 'Food Covers-Outlet', 'Cover-Banquet', 'Total']
    df[numeric_cols] = df[numeric_cols].replace(',', '', regex=True).astype(float)

    # Features for training
    selected_columns = ['Rm. night', 'Mean Temperature BKK', 'Food Covers-Outlet', 'Cover-Banquet']
    X = df[selected_columns]
    y = df['Total (kWh)']

    # Choose a machine learning model
    if model_type == 'RandomForest':
        model = RandomForestRegressor()
    elif model_type == 'LinearRegression':
        model = LinearRegression()
    elif model_type == 'GradientBoosting':
        model = GradientBoostingRegressor()
    else:
        raise ValueError("Invalid model type. Supported types are 'RandomForest', 'LinearRegression', and 'GradientBoosting'")

    # Train the model
    model.fit(X, y)

    # Make predictions on new data (using all rows except the last one)
    X_new = df[selected_columns].iloc[:-1]
    y_new = df['Total (kWh)'].iloc[:-1]
    predicted_total_kwh = model.predict(X_new)

    # Calculate accuracy
    difference = 1 - abs(predicted_total_kwh - y_new) / y_new
    accuracy = difference.mean() * 100

    # Original and first column except first row
    original_data = df.iloc[:-1].to_dict(orient='records')
    first_column_except_first_row = df.iloc[1:, 0].tolist()

    return {
        'accuracy': accuracy,
        'predicted_total_kwh': predicted_total_kwh.tolist(),
        'original_data': original_data,
        'first_column_except_first_row': first_column_except_first_row
    }

if __name__ == "__main__":
    # Accept the CSV file path as command-line argument
    csv_file_path = sys.argv[1]

    # Train and evaluate models, and store results in a dictionary
    outputs = {}

    # Train and evaluate Random Forest model
    outputs['RandomForest'] = train_and_evaluate(csv_file_path, model_type='RandomForest')

    # Train and evaluate Linear Regression model
    outputs['LinearRegression'] = train_and_evaluate(csv_file_path, model_type='LinearRegression')

    # Train and evaluate Gradient Boosting model
    outputs['GradientBoosting'] = train_and_evaluate(csv_file_path, model_type='GradientBoosting')

    # Convert the dictionary to JSON
    json_output = json.dumps(outputs)

    # Print the JSON output
    print(json_output)
