import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DEFAULT_MODEL = "gpt-4o-mini"  # or "gpt-3.5-turbo" for faster/cheaper results

# Persona Configuration
DEFAULT_NUM_PERSONAS = 2

# Employment distribution by industry (probabilities sum to 1)
EMPLOYMENT_DISTRIBUTION = {
    "Education and Health Services": 0.2235,
    "Professional and Business Services": 0.1272,
    "Wholesale and Retail Trade": 0.1214,
    "Manufacturing": 0.0955,
    "Leisure and Hospitality": 0.0877,
    "Construction": 0.0730,
    "Financial Activities": 0.0676,
    "Transportation and Utilities": 0.0610,
    "Public Administration": 0.0484,
    "Other Services": 0.0467,
    "Information": 0.0171,
    "Agriculture and related": 0.0138,
    "Mining, Quarrying, and Oil and Gas": 0.0036
}

# Age distribution (simplified US demographics)
AGE_DISTRIBUTION = {
    "18-24": 0.12,
    "25-34": 0.17,
    "35-44": 0.16,
    "45-54": 0.15,
    "55-64": 0.14,
    "65+": 0.26
}

# Education levels (simplified)
EDUCATION_LEVELS = [
    "High School or less",
    "Some College",
    "Bachelor's Degree",
    "Master's Degree",
    "Doctorate or Professional Degree"
]

# US Regions
REGIONS = [
    "Northeast",
    "Midwest",
    "South",
    "West"
]

# Gender distribution (simplified)
GENDER_DISTRIBUTION = {
    "Male": 0.49,
    "Female": 0.51
}

# Personal values and beliefs that influence decision making
PERSONAL_VALUES = [
    "traditional", "progressive", "conservative", "liberal",
    "environmentalist", "business-oriented", "community-focused",
    "individualistic", "family-oriented", "career-driven"
]

# Life experiences that shape perspectives
LIFE_EXPERIENCES = [
    "immigrant", "veteran", "parent", "caregiver", "entrepreneur",
    "artist", "scientist", "teacher", "healthcare worker",
    "first-generation college graduate", "small business owner",
    "public servant", "activist", "religious leader"
]

# Personality traits (Big Five model)
PERSONALITY_TRAITS = {
    "openness": ["very open", "moderately open", "somewhat closed"],
    "conscientiousness": [
        "very conscientious", "moderately conscientious", "less conscientious"
    ],
    "extraversion": [
        "very extroverted", "moderately extroverted", "introverted"
    ],
    "agreeableness": [
        "very agreeable", "moderately agreeable", "less agreeable"
    ],
    "neuroticism": ["very stable", "moderately stable", "less stable"]
}
