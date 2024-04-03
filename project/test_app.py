import os
import shutil
import tempfile
from app import extract_tar_contents, find_file_with_extension, load_csv, read_markdown, perform_replacements, convert_md_to_pdf, compress_to_tar_gz
 
def test_extract_tar_contents():
    # Create temporary directory
    temp_dir = tempfile.mkdtemp()
 
    # Extract tar contents
    tar_file_path = './dummy_data_file/files.tar.gz'
    extract_tar_contents(tar_file_path, temp_dir)
 
    # Test if extraction was successful
    assert os.path.isdir(temp_dir)
 
    # Clean up temporary directory
    shutil.rmtree(temp_dir)
 
def test_find_file_with_extension():
    # Create temporary directory
    temp_dir = tempfile.mkdtemp()
 
    # Extract tar contents
    tar_file_path = './dummy_data_file/files.tar.gz'
    extract_tar_contents(tar_file_path, temp_dir)
 
    # Test find_file_with_extension
    md_file_path = find_file_with_extension(temp_dir, '.md')
    csv_file_path = find_file_with_extension(temp_dir, '.csv')
 
    # Test if files are found
    assert md_file_path is not None
    assert csv_file_path is not None
 
    # Clean up temporary directory
    shutil.rmtree(temp_dir)
 
def test_load_csv():
    # Create temporary directory
    temp_dir = tempfile.mkdtemp()
 
    # Extract tar contents
    tar_file_path = './dummy_data_file/files.tar.gz'
    extract_tar_contents(tar_file_path, temp_dir)
 
    # Test load_csv
    csv_file_path = find_file_with_extension(temp_dir, '.csv')
    csv_data = load_csv(csv_file_path)
 
    # Test if CSV data is loaded
    assert len(csv_data) > 0
 
    # Clean up temporary directory
    shutil.rmtree(temp_dir)
 
def test_read_markdown():
    # Create temporary directory
    temp_dir = tempfile.mkdtemp()
 
    # Extract tar contents
    tar_file_path = './dummy_data_file/files.tar.gz'
    extract_tar_contents(tar_file_path, temp_dir)
 
    # Test read_markdown
    md_file_path = find_file_with_extension(temp_dir, '.md')
    markdown_content = read_markdown(md_file_path)
 
    # Test if markdown content is read
    assert markdown_content.startswith('#')
 
    # Clean up temporary directory
    shutil.rmtree(temp_dir)
 
def test_perform_replacements():
    # Create temporary directory
    temp_dir = tempfile.mkdtemp()
 
    # Extract tar contents
    tar_file_path = './dummy_data_file/files.tar.gz'
    extract_tar_contents(tar_file_path, temp_dir)
 
    # Test perform_replacements
    csv_file_path = find_file_with_extension(temp_dir, '.csv')
    markdown_file_path = find_file_with_extension(temp_dir, '.md')
    csv_data = load_csv(csv_file_path)
    markdown_content = read_markdown(markdown_file_path)
    modified_markdown = perform_replacements(csv_data, markdown_content)
 
    # Test if replacements are performed
    assert len(modified_markdown) > 0
 
    # Clean up temporary directory
    shutil.rmtree(temp_dir)
 
def test_convert_md_to_pdf():
    # Create temporary directory
    temp_dir = tempfile.mkdtemp()
 
    # Extract tar contents
    tar_file_path = './dummy_data_file/files.tar.gz'
    extract_tar_contents(tar_file_path, temp_dir)
 
    # Test convert_md_to_pdf
    pdf_files = []
    csv_file_path = find_file_with_extension(temp_dir, '.csv')
    markdown_file_path = find_file_with_extension(temp_dir, '.md')
    csv_data = load_csv(csv_file_path)
    markdown_content = read_markdown(markdown_file_path)
    modified_markdown = perform_replacements(csv_data, markdown_content)
    for person, content in modified_markdown.items():
        pdf_file_path = os.path.join(temp_dir, f"{person}.pdf")
        convert_md_to_pdf(content, pdf_file_path)
        assert os.path.exists(pdf_file_path)
        pdf_files.append(pdf_file_path)
 
    # Clean up temporary directory
    shutil.rmtree(temp_dir)
 
def test_compress_to_tar_gz():
    # Create temporary directory
    temp_dir = tempfile.mkdtemp()
 
    # Extract tar contents
    tar_file_path = './dummy_data_file/files.tar.gz'
    extract_tar_contents(tar_file_path, temp_dir)
 
    # Test compress_to_tar_gz
    pdf_files = []
    csv_file_path = find_file_with_extension(temp_dir, '.csv')
    markdown_file_path = find_file_with_extension(temp_dir, '.md')
    csv_data = load_csv(csv_file_path)
    markdown_content = read_markdown(markdown_file_path)
    modified_markdown = perform_replacements(csv_data, markdown_content)
    for person, content in modified_markdown.items():
        pdf_file_path = os.path.join(temp_dir, f"{person}.pdf")
        convert_md_to_pdf(content, pdf_file_path)
        assert os.path.exists(pdf_file_path)
        pdf_files.append(pdf_file_path)
   
    tar_gz_file_path = os.path.join(temp_dir, 'output.tar.gz')
    compress_to_tar_gz(pdf_files, tar_gz_file_path)
   
    # Test if tar.gz file is created
    assert os.path.exists(tar_gz_file_path)
 
    # Clean up temporary directory
    shutil.rmtree(temp_dir)