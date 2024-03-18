import os

def create_folders():
    # Create web_server/templates folder
    web_templates_folder = os.path.join('web_server', 'templates')
    os.makedirs(web_templates_folder, exist_ok=True)
    
    # Create web_server/app.py
    with open(os.path.join('web_server', 'app.py'), 'w') as f:
        pass  # Just creating an empty file
    
    # Create processing_layer folder
    os.makedirs('processing_layer', exist_ok=True)
    
    # Create processing_layer/process_files.py
    with open(os.path.join('processing_layer', 'process_files.py'), 'w') as f:
        pass  # Just creating an empty file

if __name__ == '__main__':
    create_folders()
    print("Folders and files created successfully.")
