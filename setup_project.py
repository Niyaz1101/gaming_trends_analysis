import os 
from pathlib import Path

def create_project_structure():

    structure = {
        'directories': [
            'config',
            'data/raw',
            'data/processed',
            'data/features',
            'data/models',
            'src/ingestion',
            'src/processing',
            'src/modeling',
            'src/visualization',
            'src/utils',
            'notebooks',
            'dashboards',
            'tests',
            'docker'
        ],
        'files': [
            'config/__init__.py'
            'src/__init__.py',
            'src/ingestion/__init__.py',
            'src/processing/__init__.py',
            'src/modeling/__init__.py',
            'src/visualization/__init__.py',
            'src/utils/__init__.py',
            'requirements.txt',
            '.env.example'
        ]
    }

    #Create directories
    for dir_path in structure['directories']:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        print(f"Created Directory:{dir_path}")

    #Create files
    for file_path in structure['files']:
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        Path(file_path).touch(exist_ok=True)
        print(f"Created file: {file_path}")


    print("\n Project structure created successfully!")

if __name__ == "__main__":
    create_project_structure()