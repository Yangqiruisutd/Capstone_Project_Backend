from flask import Flask, request, render_template, redirect, url_for
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import joblib

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
        # Data preprocessing and model training
        # (Omitted for brevity)
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
    app.run(host='0.0.0.0', debug=True)
