from flask import Flask, request, render_template, redirect, url_for
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import joblib
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('upload.html')
@app.route('/home2')
def home2():
    return render_template('upload2.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file:
        df = pd.read_csv(file)
        # Assume the last column is the target variable
        df = df.drop("On-Peak", axis = 1)
        df = df.drop("On Peak per RM", axis = 1)
        df = df.drop("Off-Peak", axis = 1)
        df = df.drop("Off Peak per RM", axis = 1)
        y = df['Totalkwh']
        X = df.drop('Totalkwh', axis=1)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=10)
        clf = LinearRegression()
        clf.fit(X_train, y_train)
        # Save the model for future predictions
        joblib.dump(clf, 'model.pkl')
        return render_template('predict.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Load the trained model
        clf = joblib.load('model.pkl')
        
        # Expecting form data to be the feature values for prediction
        form_data = request.form.to_dict()
        feature_values = [float(value) for value in form_data.values()]
        prediction = clf.predict([feature_values])
        return render_template('result.html', prediction=prediction[0])
    except ValueError as e:  # Handle the case where conversion to float fails
        return render_template('error.html', error_message=f"Invalid input: {e}")
    except Exception as e:
        return render_template('error.html', error_message=str(e))

if __name__ == '__main__':
    app.run(host='0.0.0.0')
    app.run(debug=True)