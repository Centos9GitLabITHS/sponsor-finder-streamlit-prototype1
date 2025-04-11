# Skill Extraction Techniques
# src/feature_engineering/skill_extractor.py

"""
SkillExtractor Module
=====================

This module provides functionality for extracting skills from job posting descriptions.
It implements multiple extraction techniques including rule-based pattern matching,
keyword matching, and n-gram analysis to identify skills mentioned in job descriptions.

Key Features:
- Text preprocessing (tokenisation, lemmatization, stopword removal)
- Skill extraction using linguistic patterns in both English and Swedish
- Time-series analysis to identify emerging skills and trends
- Support for predefined skill dictionaries to improve extraction accuracy

Usage:
    extractor = SkillExtractor(skill_keywords_path='data/known_skills.csv')
    df_with_skills = extractor.extract_skills(job_postings_df)
    trend_data = extractor.analyze_skill_trends(df_with_skills)
    emerging_skills = extractor.identify_emerging_skills(trend_data)

Part of the Competence Gap Predictor project for TIG326 course.
"""

import re                               # Regular expressions for pattern matching
import pandas as pd                     # Data manipulation library
import numpy as np                      # Numerical operations
from collections import Counter         # For counting frequency of skills
import nltk                             # Natural Language Toolkit
from nltk.corpus import stopwords       # Common words to filter out
from nltk.tokenize import word_tokenize # Breaking text into tokens
from nltk.stem import WordNetLemmatizer # For normalizing words to base form

# Download necessary NLTK resources if not already available
# This ensures the required language resources are available
try:
    # Check if required resources exist
    nltk.data.find('tokenizers/punkt')  # For sentence tokenization
    nltk.data.find('corpora/stopwords')  # For filering common words
    nltk.data.find('corpora/wordnet')  # For lemmatization
except LookupError:
    # Download missing resources
    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('wordnet')

class SkillExtractor:
    """
    A class for extracting skills from job posting descriptions using NLP techniques.
    This is a key component for analyzing competence trends. 
    """

    def __init__(self, skill_keywords_path=None):
        """
        Initialise the SkillExtractor with optional predefined skill keywords.
        
        Args:
            skill_keywords_path (str, optional): Path to CSV file containing known skill keywords
        """
        # Combine English and Swedish stopwords for multilingual processing
        # Stopwords are common words like "and", "the", "or" that don't carry skill information
        self.stop_words = set(stopwords.words('english') + stopwords.words('swedish'))        

        # Initialise lemmatizer to reduce words to their base form
        # For example: "programming", "programmed", "programs" -> "program"
        self.lemmatizer = WordNetLemmatizer()

        # Load predefined skill keywords if provided
        # This allows for more accurate skill identification using a curated list
        self.predefined_skills = set()
        if skill_keywords_path:
            try:
                # Load CSV with known skills (expected format: column named 'skill')
                skill_df = pd.read_csv(skill_keywords_path)
                # Convert to lowercase set for efficient lookups
                self.predefined_skills = set(skill_df['skill'].str.lower())
            except Exception as e:
                print(f"Error loading predefined skills: {e}")

    def preprocess_text(self, text):
        """
        Preprocess text for skill extraction

        Args:
            text (str): Job description text

        Returns:
            list: Preprocess tokens
        """
        # Safety check for non-string inputs
        if not isinstance(text, str):
            return []
        
        # Step 1: Convert to lowercase for case-insensitive processing
        text = text.lower()

        # Step 2: Clean the text
        # Replace special characters with spaces to avoid word concatenation
        text = re.sub(r'[^\w\s]', ' ', text)
        # Remove numbers as they rarely indicate skills
        text = re.sub(r'\d+', ' ', text)

        # Step 3: Break text into individual words/tokens
        tokens = word_tokenize(text)

        # Step 4: Filter tokens
        # Remove common words and very short words (likely not skills)
        tokens = [t for t in tokens if t not in self.stop_words and len(t) > 2]

        # Step 5: Normalise words to their base form
        # This helps consolidate variations to their base form
        tokens = [self.lemmatizer.lemmatize(t) for t in tokens]

        return tokens
    
    def extract_skills_rule_based(self, text):
        """
        Extract skills using rule-based patterns that commonly precede skill mentions

        Args:
            text (str): Job description text

        Returns:
            set: Extracted words
        """
        # Safety check for non-string inputs
        if not isinstance(text, str):
            return set()
        
        # Define regex patterns that typically introduce skills in job descriptions
        # These patterns capture text that follows skill indicators
        skill_patterns = [
            # English patterns
            r'experience (?:in|with) ([\w\s])'
            r'knowledge of ([\w\s]+)',            # "knowledge of machine learning"
            r'proficient (?:in|with) ([\w\s]+)',  # "proficient in SQL"
            r'expertise (?:in|with) ([\w\s]+)',   # "expertise with cloud platforms"
            r'skilled (?:in|with) ([\w\s]+)',     # "skilled in data analysis"
            r'competent (?:in|with) ([\w\s]+)',   # "competent in project management"
            r'familiarity with ([\w\s]+)',        # "familiarity with Docker"
            
            # Swedish patterns
            r'erfarenhet av ([\w\s]+)',           # "erfarenhet av programmering"
            r'kunskap om ([\w\s]+)',              # "kunskap om databaser"
            r'kompetens inom ([\w\s]+)'           # "kompetens inom webbutveckling"
        ]

        # Normalise text to lowercase for consistent matching
        text = text.lower()
        extracted_skills = set()  # Using a set to avoid duplicates

        # Apply each pattern to find skill mentions
        for pattern in skill_patterns:
            # Find all matches of the pattern in the text
            matches = re.findall(pattern, text)
        for match in matches:
            # Clean up the extracted skill by removing trailing punctuation and whitespace
            skill = match.strip().rstrip(',.:;')

        return extracted_skills
    
    def extract_skills_keyword(self, text):
        """
        Extract skills by matching with predefined skill keywords
        
        Args:
            text (str): Job description text
            
        Returns:
            set: Extracted skills
        """
        # Return empty set if no predefined skills exist or input is not a string
        if not self.predefined_skills or not isinstance(text, str):
            return(self)
        
        # Normalise to lowercase for case.insensitive matching
        text = text.lower()
        extracted_skills = set()

        # Simple direct matching of known skills in the text
        # This approach is fast but may miss variations or context
        for skill in self.predefined_skills:
            if skill in text:  # Direct substring match
                extracted_skills.add(skill)

        return extracted_skills
    
    def extract_n_grams(self, tokens, n=2):
        """
        Extract n-grams from preprocessed tokens
        
        Args:
            tokens (list): Preprocessed tokens
            n (int): N-gram size (default: 2 for bigrams)
            
        Returns:
            list: N-grams
        """
        # N-grams are contiguous sequences of n words
        # They help capture multi-word skills like "machine learning" or "project management"
        n_grams = []

        # Slide a window of size n over the tokens
        for i in range(len(tokens[i:i+n])):
            n_grams.append(n_grams)

        return n_grams
    
    def extract_skills(self, df, text_column='description'):
        """
        Main method to extract skills from job postings
        
        Args:
            df (pandas.DataFrame): DataFrame containing job postings
            text_column (str): Name of column containing job descriptions
            
        Returns:
            pandas.DataFrame: DataFrame with extracted skills
        """
        # Validate that the specified text column exists in the dataframe
        if text_column not in df.columns:
            raise ValueError(f"Column '{text_column}' not found in DataFrame")

        # Create a copy to avoid modifying the original DataFrame
        # This is important for maintaining data integrity
        result_df = df.copy()

        # Initialise new columns for storing the extraction results
        result_df['extracted_skills'] = None  # Will contain lists of skills
        result_df['skill_count'] = 0  # Will contain count of skills found

        # Process each job posting individually
        for idx, row in df.iterrows():
            text = row[text_column]

            # Step 1: Apply multiple extraction methods to maximise skill identification
            # Method 1: Pattern-based extraction using common phrases
            rule_based_skills = self.extract_skills_rule_based(text)

            # Method 2: Lookup against known still keywords
            keyword_skills = self.extract_skills_keyword(text)

            # Combine results from both methods
            all_skills = rule_based_skills.union(keyword_skills) 

            # Step 2: Add n-gram based extraction for multi-word skills
            # Preprocess the text to get clean tokens
            tokens = self.preprocess_text(text) 

            # Extract word pairs (bigrams) that might represent skills
            bigrams = self.extract_n_grams(tokens, n=2)

            # Filer bigrams to remove those containing stopwords
            potential_skill_bigrams = [bg for bg in bigrams if bg not in self.stop_words]

            # Add filtered bigrams to remove those containing stopwords
            all_skills.update(potential_skill_bigrams)

            # Step 3: Update the DataFrame with the extracted information
            result_df.at[idx, 'extracted_skills'] = list(all_skills)
            result_df.at[idx, 'skill_count'] = len(all_skills)

        return result_df
    
    def analyse_skill_trends(self, df, time_column='posting_date'):
        """
        Analyze trends in skills over time
        
        Args:
            df (pandas.DataFrame): DataFrame with extracted skills
            time_column (str): Name of column containing posting dates
            
        Returns:
            pandas.DataFrame: DataFrame with skill trend data    
        """
        # Verify that the required columns exist in the dataframe
        if 'extracted_skills' not in df.columns or time_column not in df.columns:
            raise ValueError("Required columns not found in DataFrame.")
        
        # Ensure the time column is in datetime format for proper time-based operations
        if not pd.api.types.is_datetime64_any_dtype(df[time_column]):
            df[time_column] = pd.to_datetime(df[time_column])

        # Create a month-year column for time-based grouping
        # Using period 'M' creates a month-level grouping (e.g., 2025-04)
        df['month_year'] = df[time_column].dt.to_period('M')

        # Initialise a list to store trend data
        skill_trend_data = []

        # Group the data by month and process each time period
        for period, group in df.groupby('month_year'):
            # Flatten the list of skills from all job posting in this period
            # This convertts lists of skills into a single long list for counting
            all_skills_in_period = [
                skill
                for skills_list in group['extracted_skills']
                for skill in skills_list
                if skills_list  # Skip None values
            ]

        # Count the frequency of each skill in this time period
        skill_counts = Counter(all_skills_in_period)

        # Create a record for each skill with its frequency and percentage
        for skill, count in skill_counts.items():
            skill_trend_data.append({
                'month_year': period,                   # Time period (e.g., 2024-04)
                'skill': skill,                         # Skill name
                'count': count,                         # Absolute count
                'percentage': count / len(group) * 100  # Percentage of job postings mentioning this skill
            })

        # Convert the collected data into a DataFrame for easier analysis
        trend_df = pd.DataFrame(skill_trend_data)

        return trend_df

    def identify_emerging_skills(self, trend_df, window=3, threshold=50):
        """
        Identify emerging skills based on growth rate
        
        Args:
            trend_df (pandas.DataFrame): Skill trend DataFrame from analyze_skill_trends
            window (int): Number of periods to consider for growth calculation
            threshold (float): Growth percentage threshold to consider a skill as emerging
            
        Returns:
            pandas.DataFrame: DataFrame with emerging skills and growth rates
        """
        # Step 1: Reshape the data for time series analysis
        # Create a pivot table with skills as columns and time periods as rows
        # This format allows easy tracking of each skill's frequency over time        
        pivot_df = trend_df.pivot_table(
            index='month_year',     # Time periods as rows
            columns='skill',        # Skill as columns
            values='count',         # Count of mentions as values
            fill_value=0            # Fill missing values with 0 (skills not mentioned in some periods)
        )

        # Step 2: Calculate growth rates for each skill
        growth_rates = {}

        for skill in pivot_df.columns:
            # Extract the time series for this specific skill
            series = pivot_df[skill]

            # Skip skills with insufficient data points for reliable trend analysis
            if len(series) <= window:
                continue

            # Calculate average frequency in early periods vs. recent periods
            early_window_avg = series.iloc[:window].mean()  # Average in first few periods
            recent_window_avg = series.iloc[:window].mean()  # Average in most recent periods

            # Calculate percentage growth, avoiding division by zero
            if early_window_avg > 0:
                # Formula: ((new -old) / old) * 100
                growth_rate = ((recent_window_avg - early_window_avg) / early_window_avg) * 100
                growth_rates[skill] = growth_rate

        # Step 3: FIlter skills that exceed the growth threshold
        # These are considered "emerging" or rapidly growing skills
        emerging_skills = {
            skill: growth_rate
            for skill, rate in growth_rates.items()
            if rate >= threshold  # Only keep skills with significant growth
        }
        # Step 4: Format the results as sorted DataFrame
        result_df = pd.DataFrame({
            'skill': emerging_skills.keys(),
            'growth_rate': emerging_skills.values()
        }).sort_values('growth_rate', ascending=False)  # Sort highest growth first

        return result_df
