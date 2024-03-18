from flask import Flask, render_template, request
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def upload_form():
    return render_template('upload_form.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'
    
    files = request.files.getlist('file')

    for file in files:
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    
    return 'Files uploaded successfully'

if __name__ == '__main__':
    app.run(debug=True, port=5001)  # Set the port to 5001
