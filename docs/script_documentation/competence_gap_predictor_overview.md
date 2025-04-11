# Competence Gap Predictor - Project Overview

## Project Purpose
The Competence Gap Predictor aims to analyze job posting data from Arbetsförmedlingen to identify trends in skill demand, predict emerging competencies, and help organizations prepare for future workforce needs. The tool focuses particularly on the Gothenburg job market with special attention to key sectors like IT, automotive, healthcare, and maritime industries.

## System Architecture
The system follows a modular pipeline architecture:

```
Data Collection → Data Cleaning → Feature Engineering → ML Modeling → Visualization
```

### Core Components

1. **Data Collection (af_api.py)**
   - Interfaces with Arbetsförmedlingen's API
   - Retrieves historical and current job posting data
   - Manages authentication and request handling

2. **Data Preprocessing (preprocessor.py)**
   - Cleans and standardizes the raw job posting data
   - Handles duplicates, missing values, and date formatting
   - Prepares data for feature extraction

3. **Skill Extraction (skill_extractor.py)**
   - Applies NLP techniques to identify skills in job descriptions
   - Uses rule-based patterns, keyword matching, and n-gram analysis
   - Builds a structured dataset of skills mentioned in job postings

4. **Trend Analysis and Prediction (implemented in future modules)**
   - Analyzes skill frequency changes over time
   - Identifies emerging competencies based on growth rates
   - Predicts future skill demand using time series models

5. **Visualization Interface (planned Streamlit app)**
   - Provides interactive dashboards for exploring competence trends
   - Enables filtering by industry, region, and time period
   - Visualizes skill gaps and emerging competencies

## Data Processing Pipeline

The data flows through the system as follows:

1. Job postings are fetched from Arbetsförmedlingen's API
2. Raw data is cleaned and standardized
3. Skill extraction is performed on job descriptions
4. Time-series analysis identifies trends and emerging skills
5. Predictive models forecast future skill demand
6. Results are presented through interactive visualizations

## Key Features

- **Multilingual Processing**: Handles both Swedish and English job descriptions
- **Trend Analysis**: Identifies growing and declining skill demands
- **Emerging Skill Detection**: Highlights fast-growing competencies
- **Time-Series Forecasting**: Predicts future skill requirements
- **Interactive Visualization**: Enables exploration of competence trends

## Target Users

The system is designed primarily for:
- HR specialists planning workforce development
- Educational institutions designing relevant courses
- Individual professionals planning career development
- Recruitment agencies advising clients on talent acquisition

## Implementation Status

The project currently has the following components implemented:
- Project structure and organization
- API connection framework for Arbetsförmedlingen
- Basic data preprocessing functionality
- Skill extraction using NLP techniques

Upcoming development will focus on:
- Machine learning model implementation
- Time-series forecasting
- Streamlit visualization interface
- Comprehensive documentation and testing

## Project Context

This project is being developed as part of the TIG326 course at the University of Gothenburg, focusing on data-driven business development. It demonstrates the application of design thinking methodologies, agile development practices, and data science techniques to address real-world business challenges.