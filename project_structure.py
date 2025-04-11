
# project_structure.py
"""
Competence Gap Prdictor Project Structure
Group 14 - TIG 326 Course
University of Gothenburg
"""

import os

def create_project_structure():
    # Create main project directories
    directories = [
        "data", # For raw and processeddata  
        "src", # Source code
        "notebooks", # Jupyter notebooks
        "tests", # Unit tests
        "docs" # Documentation
    ]
    
    # Source code subdirectories
    src_subdirs = [
        'data_fetcher', # API interaction and d
        'data_cleaner',  # Data prep
        'feature_engineering',
        'models',  # ML Models
        'utils'  # Utility functions
    ]

    # Create main project subdirectories
    for dir in directories:
        os.makedirs(dir, exist_ok=True)

    for subdir in src_subdirs:
        os.makedirs(os.path.join('src', subdir), exist_ok=True)

    # Create initial files
    initial_files = {
        'README.md': "# Competence Gap Predictor\n\n## Project Overview\nA tool to predict skill trends in the Gothenburg job market.",
        'requirements.txt': "pandas\nnumpy\nrequests\nptyhon-dotenv\nstreamlit\nscikit-learn\nplotly\n",
        '.env': "# API Keys and Configuration\nAF_API_KEY=\nPROJECT_ENV=development\n",
        'src/data_fetcher/af_api.py': "# Arbetsförmedlingen API Interaction Module",
        'src/data_cleaner/preprocessor.py': "# Data Cleaning and Preprocessing Module",
        'src/feature_engineering/skill_extractor.py': "# Skill Extraction Techniques"
    }

    for filepath, content in initial_files.items():
        with open(filepath, 'w') as f:
            f.write(content)

    print("Project structure created successfully!")
    
if __name__ == '__main__':
    create_project_structure()
