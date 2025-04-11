# Skill Extractor Module

## Overview
The Skill Extractor is a core component of the Competence Gap Predictor pipeline. It analyzes job posting descriptions to identify and extract mentioned skills, enabling trend analysis and identification of emerging competencies in the job market.

## Technical Approach
The module implements a hybrid approach to skill extraction:

1. **Rule-based extraction**: Uses regex patterns to identify skills based on common phrase structures in job descriptions
2. **Keyword matching**: Compares text against known skills from a predefined dictionary
3. **N-gram analysis**: Identifies potential multi-word skills through text chunking techniques

## Key Features

### Multilingual Support
The extractor is designed to work with both English and Swedish job postings, with pattern matching rules for both languages.

### Preprocessing Pipeline
Text is normalized through:
- Case normalization
- Special character removal
- Tokenization
- Stopword filtering
- Lemmatization

### Trend Analysis
The module can process job postings over time to:
- Track skill frequency changes
- Calculate growth rates
- Identify emerging and declining skills
- Generate time-series datasets for visualization

## Integration Points
- **Input**: Takes preprocessed job posting data from the data cleaning pipeline
- **Output**: Produces structured skill data for the ML model and visualization components

## Usage Example

```python
# Initialize the extractor, optionally with a custom skill dictionary
extractor = SkillExtractor(skill_keywords_path='data/known_skills.csv')

# Extract skills from job postings
enriched_df = extractor.extract_skills(
    job_postings_df, 
    text_column='description'
)

# Analyze trends over time
trend_data = extractor.analyze_skill_trends(
    enriched_df,
    time_column='posting_date'
)

# Identify fast-growing skills
emerging_skills = extractor.identify_emerging_skills(
    trend_data,
    window=3,  # 3-month window for calculations
    threshold=20  # 20% growth to qualify as "emerging"
)
```

## Future Improvements
- Integration with pre-trained language models for better skill recognition
- Support for skill categorization (technical, soft, domain-specific)
- Implementation of more sophisticated trend detection algorithms