from flask import Flask, render_template, request, send_file
import os
import shutil
import tempfile
import tarfile
import csv
from markdown2 import markdown
from fpdf import FPDF

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def upload_form():
    return render_template('upload_form.html')

def process_files(files):
    temp_dir = tempfile.mkdtemp()
    md_dir = os.path.join(temp_dir, 'MD')
    pdf_dir = os.path.join(temp_dir, 'PDF')

    os.makedirs(md_dir)
    os.makedirs(pdf_dir)

    csv_file = None
    md_template = None

    # Extract files and find CSV and Markdown template
    for file in files:
        filename = file.filename
        file_path = os.path.join(temp_dir, filename)
        file.save(file_path)

        if filename.endswith('.csv'):
            csv_file = file_path
        elif filename.endswith('.md'):
            md_template = file_path

    # Read CSV file
    names = []
    if csv_file:
        with open(csv_file, 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                names.append(row)

    # Read Markdown template
    template_content = ''
    if md_template:
        with open(md_template, 'r') as md_file:
            template_content = md_file.read()

    # Process files
    for name in names:
        # Replace placeholders in Markdown template
        md_content = template_content.replace('{{FirstName}}', name[0]).replace('{{LastName}}', name[1])
        # Save Markdown file
        md_filename = f"{name[0]}_{name[1]}.md"
        md_file_path = os.path.join(md_dir, md_filename)
        with open(md_file_path, 'w') as md_file:
            md_file.write(md_content)
        # Convert Markdown to PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, markdown(md_content))
        pdf_filename = f"{name[0]}_{name[1]}.pdf"
        pdf_file_path = os.path.join(pdf_dir, pdf_filename)
        pdf.output(pdf_file_path)

    # Create tar.gz file
    output_filename = 'output.tar.gz'
    output_path = os.path.join(temp_dir, output_filename)
    with tarfile.open(output_path, "w:gz") as tar:
        tar.add(pdf_dir, arcname=os.path.basename(pdf_dir))

    return output_path

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'

    files = request.files.getlist('file')
    output_path = process_files(files)

    return send_file(output_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, port=5001)