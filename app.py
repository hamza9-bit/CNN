from flask import Flask, render_template, request, jsonify
from test import test_model
import os
from werkzeug.utils import secure_filename
from tensorflow.keras.models import load_model

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
global GlobalResult
GlobalResult = ""

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# model_path = "model.h5"  # Chemin vers le modèle
# model = load_model(model_path)

@app.route('/symptoms', methods=['GET', 'POST'])
def symptoms():
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'})

        file = request.files['file']

        if file.filename == '':
            return jsonify({'error': 'No selected file'})

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            # Appeler la fonction test_model avec le fichier téléchargé
            result = test_model(file_path)
            GlobalResult = result
            
            return jsonify({'result': result})

        return jsonify({'error': 'Invalid file format'})
    else:
        return render_template('symptoms.html')
@app.route('/')
def index():
    return render_template('index.html', title='Welcome to Health diagnosis')

@app.route('/result')
def result():
        return render_template('result.html')


# @app.route('/symptoms')
# def symptoms():
#     return render_template('symptoms.html')

    

if __name__ == '__main__':
    app.run(debug=True)

