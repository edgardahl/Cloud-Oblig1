from flask import Flask, render_template, request
import os
import base64

app = Flask(__name__)

# Define the upload folder
UPLOAD_FOLDER = os.path.join(app.root_path, 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Route to render the upload form
@app.route('/')
def upload_form():
    return render_template('upload_form.html')

# Route to handle file upload
@app.route('/upload', methods=['POST'])
def upload_files():
    uploaded_files = request.files.getlist('files[]')

    if len(uploaded_files) == 0:
        return 'No files selected'
    
    response = ''
    for file in uploaded_files:
        if file.filename == '':
            return 'No selected file'
        
        # Ensure the uploads directory exists
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        
        # Save the file to the uploads directory
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        
        # Read the content of the uploaded file
        with open(file_path, 'rb') as f:
            file_content = f.read()
        
        # Encode file content as Base64
        encoded_content = base64.b64encode(file_content).decode('utf-8')
        
        # Embed the Base64-encoded content as a data URL in HTML
        response += f'<div style="margin-bottom: 20px;">'
        response += f'<p style="font-weight: bold;">File: {file.filename}</p>'
        if file.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            response += f'<img style="width:400px;" src="data:image/{file.filename.split(".")[-1]};base64,{encoded_content}" alt="{file.filename}" style="max-width: 100%;">'
        else:
            response += f'<p>{file_content.decode("utf-8")}</p>'
        response += f'</div>'
    
    return response

if __name__ == '__main__':
    app.run(debug=True, port=5000)
