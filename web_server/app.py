from flask import Flask, render_template, request, send_from_directory
import os
import base64

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
    file_contents = {}

    for file in files:
        filename = file.filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Read the contents of the uploaded file
        if filename.endswith('.png') or filename.endswith('.jpg') or filename.endswith('.jpeg'):
            # If the file is an image, encode it as base64
            with open(file_path, 'rb') as f:
                file_contents[filename] = base64.b64encode(f.read()).decode('utf-8')
        else:
            # If the file is not an image, read it as text
            with open(file_path, 'r') as f:
                file_contents[filename] = f.read()

    return render_template('file_contents.html', file_contents=file_contents)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
