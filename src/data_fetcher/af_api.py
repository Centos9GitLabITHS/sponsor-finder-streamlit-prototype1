# src/data_fetcher/af_api.py
import os  # Operating system operations
import requests
from dotenv import load_dotenv

load_dotenv()  # Load environment variables

class ArbetsformedlingenAPI:  # API for Arbetsförmedlingen
    BASE_URL = "https://api.arbetsformedlingen.se/v1"  # OBS! Måste bytas ut mot riktigt API-adress!
    
    def __init__(self):  # Initialize the API
        self.api_key = os.getenv('AF_API_KEY')
        if not self.api_key:  # If the API key is not found
            raise ValueError("Arbetsförmedlingen API key is required")  
    
    def fetch_job_postings(self, params=None):  # Fetch job postings with optional filtering parameters
        """
        Fetch job postings with optional filtering parameters
        
        Args:
            params (dict): Optional parameters for filtering job postings
        
        Returns:
            list: Job postings data
        """
        headers = {  # Headers for the API request
            'Authorization': f'Bearer {self.api_key}',  # Authorization header
            'Content-Type': 'application/json'
        }
        
        try:  # Try to fetch the job postings
            response = requests.get(  # Fetch the job postings
                f"{self.BASE_URL}/jobpostings",  # API endpoint
                headers=headers,  # Headers for the API request
                params=params  # Parameters for the API request
            )
            response.raise_for_status()
            return response.json()
        
        except requests.exceptions.RequestException as e:
            print(f"API Request Error: {e}")
            return []
    
    def extract_skills(self, job_postings):
        """
        Extract skills from job postings
        
        Args:
            job_postings (list): List of job posting data
        
        Returns:
            list: Extracted skills
        """
        # Placeholder for skill extraction logic
        # Will be enhanced with NLP techniques later
        pass