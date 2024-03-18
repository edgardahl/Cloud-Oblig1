import os

def process_uploaded_files(folder_path):
    files = os.listdir(folder_path)
    for file in files:
        file_path = os.path.join(folder_path, file)
        if os.path.isfile(file_path):
            with open(file_path, 'r') as f:
                print(f'Contents of {file}:')
                print(f.read())
                print('\n')

if __name__ == '__main__':
    process_uploaded_files('uploads')
