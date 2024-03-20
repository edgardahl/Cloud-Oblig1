import os
import shutil  # Import shutil module for directory removal
from flask import Flask, render_template, request, send_file
import tarfile
import csv
from markdown2 import markdown
from fpdf import FPDF

app = Flask(__name__)

# Define the upload folder and temporary directory
UPLOAD_FOLDER = os.path.join(app.root_path, 'uploads')
TEMP_DIR = os.path.join(app.root_path, 'temp')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['TEMP_DIR'] = TEMP_DIR

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

    # Create temporary directory
    os.makedirs(app.config['TEMP_DIR'], exist_ok=True)

    # Process uploaded files
    for file in uploaded_files:
        if file.filename == '':
            return 'No selected file'

        # Save the file to the temporary directory
        temp_file_path = os.path.join(app.config['TEMP_DIR'], file.filename)
        file.save(temp_file_path)

    # Process the uploaded tar.gz file
    tar_file_path = temp_file_path
    extract_dir = app.config['TEMP_DIR']
    extract_tar_contents(tar_file_path, extract_dir)

    # Load CSV and Markdown files
    csv_data = load_csv(os.path.join(extract_dir, 'dummy.csv'))
    markdown_content = read_markdown(os.path.join(extract_dir, 'dummy.md'))

    # Perform replacements and store modified Markdown files per person
    modified_markdown = perform_replacements(csv_data, markdown_content)

    # Convert Markdown files to PDF
    pdf_files = []
    for person, content in modified_markdown.items():
        pdf_file_path = os.path.join(app.config['TEMP_DIR'], f"{person}.pdf")
        convert_md_to_pdf(content, pdf_file_path)
        pdf_files.append(pdf_file_path)

    # Compress PDF files into a new tar.gz file
    tar_gz_file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'output.tar.gz')
    compress_to_tar_gz(pdf_files, tar_gz_file_path)

    # Remove temporary directory
    shutil.rmtree(app.config['TEMP_DIR'])  # Use shutil.rmtree instead of os.rmdir

    # Provide download link for the generated tar.gz file
    return send_file(tar_gz_file_path, as_attachment=True)

def extract_tar_contents(tar_file_path, extract_dir):
    with tarfile.open(tar_file_path, 'r:gz') as tar:
        tar.extractall(path=extract_dir)

def load_csv(csv_file_path):
    with open(csv_file_path, 'r', newline='') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        csv_data = [row for row in csv_reader]
    return csv_data

def read_markdown(markdown_file_path):
    with open(markdown_file_path, 'r') as markdown_file:
        markdown_content = markdown_file.read()
    return markdown_content

def perform_replacements(csv_data, markdown_content):
    modified_markdown = {}
    for person in csv_data:
        modified_content = markdown_content.replace('{{FirstName}}', person['FirstName'])
        modified_content = modified_content.replace('{{LastName}}', person['LastName'])
        modified_markdown[f"{person['FirstName']}_{person['LastName']}"] = modified_content
    return modified_markdown

def convert_md_to_pdf(markdown_content, pdf_file_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt=markdown_content)
    pdf.output(pdf_file_path)

def compress_to_tar_gz(pdf_files, tar_gz_file_path):
    with tarfile.open(tar_gz_file_path, 'w:gz') as tar:
        for pdf_file in pdf_files:
            tar.add(pdf_file, arcname=os.path.basename(pdf_file))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
