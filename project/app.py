import os
import shutil
from flask import Flask, render_template, request, send_file
import tarfile
import csv
from fpdf import FPDF
 
app = Flask(__name__)
 
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
 
    # Create a temporary directory
    temp_dir = os.path.join(app.root_path, 'temp')
    os.makedirs(temp_dir, exist_ok=True)
 
    for file in uploaded_files:
        if file.filename == '':
            return 'No selected file'
 
        temp_file_path = os.path.join(temp_dir, file.filename)
        file.save(temp_file_path)
 
    # Extract tar contents
    extract_tar_contents(temp_file_path, temp_dir)
 
    # Dynamically load Markdown and CSV files
    markdown_file_path = find_file_with_extension(temp_dir, '.md')
    csv_file_path = find_file_with_extension(temp_dir, '.csv')
 
    if not (markdown_file_path and csv_file_path):
        return 'Markdown or CSV file not found'
 
    csv_data = load_csv(csv_file_path)
    markdown_content = read_markdown(markdown_file_path)
 
    modified_markdown = perform_replacements(csv_data, markdown_content)
 
    pdf_files = []
    for person, content in modified_markdown.items():
        pdf_file_path = os.path.join(temp_dir, f"{person}.pdf")
        convert_md_to_pdf(content, pdf_file_path)
        pdf_files.append(pdf_file_path)
 
    tar_gz_file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'output.tar.gz')
    compress_to_tar_gz(pdf_files, tar_gz_file_path)
 
    # Delete the temporary directory
    shutil.rmtree(temp_dir)
 
    return send_file(tar_gz_file_path, as_attachment=True)
 
# Function to extract contents from tar file
def extract_tar_contents(tar_file_path, extract_dir):
    with tarfile.open(tar_file_path, 'r:gz') as tar:
        tar.extractall(path=extract_dir)
 
# Function to find a file with a specific extension in a directory
def find_file_with_extension(directory, extension):
    for file in os.listdir(directory):
        if file.endswith(extension):
            return os.path.join(directory, file)
    return None
 
# Function to load CSV file and print column titles
def load_csv(csv_file_path):
    with open(csv_file_path, 'r', newline='') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        # Read the data rows
        csv_data = [row for row in csv_reader]
    return csv_data
 
# Function to read Markdown file
def read_markdown(markdown_file_path):
    with open(markdown_file_path, 'r') as markdown_file:
        markdown_content = markdown_file.read()
    return markdown_content
 
# Function to perform replacements in Markdown content
def perform_replacements(csv_data, markdown_content):
    modified_markdown = {}
    for person in csv_data:
        modified_content = markdown_content
        for title, value in person.items():
            modified_content = modified_content.replace(f'{{{{{title}}}}}', value)
        person_name = '_'.join([person[title] for title in person.keys()])
        modified_markdown[person_name] = modified_content
    return modified_markdown
 
# Function to convert Markdown content to PDF using FPDF
def convert_md_to_pdf(markdown_content, pdf_file_path):
    class PDF(FPDF):
        pass

    pdf = PDF()
    pdf.add_page()
    pdf.set_font('Times', '', 12)
    pdf.multi_cell(0, 10, markdown_content)
    pdf.output(pdf_file_path)

 
# Function to compress PDF files into a tar.gz file
def compress_to_tar_gz(pdf_files, tar_gz_file_path):
    with tarfile.open(tar_gz_file_path, 'w:gz') as tar:
        for pdf_file in pdf_files:
            tar.add(pdf_file, arcname=os.path.basename(pdf_file))
 
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5050))
    app.run(host='0.0.0.0', port=port)