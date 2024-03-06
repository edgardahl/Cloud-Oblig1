from flask import Flask, request, jsonify, send_file
import os
import shutil
import tarfile
import csv

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'tar.gz'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Function to check if the file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Function to process the uploaded file
def process_file(file_path):
    # Extract the tar.gz file
    with tarfile.open(file_path, 'r:gz') as tar:
        tar.extractall(app.config['UPLOAD_FOLDER'])
    
    # Read CSV file
    csv_file = os.path.join(app.config['UPLOAD_FOLDER'], 'data.csv')
    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        data = list(reader)
    
    # Process the data
    processed_data = []
    for row in data:
        # Perform your processing here, for example, you can modify the data
        
        # Append the modified row to the processed data list
        processed_data.append(row)
    
    # Here you would generate PDF files and compress them
    
    # Return the path to the compressed file
    return os.path.join(app.config['UPLOAD_FOLDER'], 'certificates.tar.gz')

# Route to handle file uploads
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'message': 'No file part in the request'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        # Process the uploaded file
        output_file_path = process_file(file_path)

        # Clean up uploaded files
        shutil.rmtree(app.config['UPLOAD_FOLDER'])

        # Return the processed file for download
        return send_file(output_file_path, as_attachment=True), 200

    return jsonify({'message': 'Invalid file format. Please upload a .tar.gz file'}), 400

if __name__ == '__main__':
    app.run(debug=True)
