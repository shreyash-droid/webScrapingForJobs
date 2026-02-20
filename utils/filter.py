import re
import pandas as pd
from utils.logger import logger

class JobFilter:
    def __init__(self):
        # Specific keywords for target roles
        self.keywords = ["ui", "ux", "product", "frontend"]
        # Explicit exclusion keywords to avoid irrelevant roles
        self.exclude_keywords = ["game", "gaming", "unity", "unreal"]
        
    def clean_text(self, text):
        """Removes extra whitespace and special characters from text."""
        if not text or not isinstance(text, str):
            return ""
        # Remove extra whitespace and newlines
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def is_relevant(self, role_title):
        """Checks if the role title is relevant and not explicitly excluded."""
        if not role_title:
            return False
        
        role_title_lower = role_title.lower()
        
        # 1. Check for exclusion keywords (like Game Design)
        if any(ex in role_title_lower for ex in self.exclude_keywords):
            return False

        # 2. Check for inclusion keywords
        for kw in self.keywords:
            if kw in role_title_lower:
                return True
        return False

    def normalize_fields(self, df):
        """Normalizes column names and cleans text fields."""
        # Ensure consistent column naming
        column_mapping = {
            "Title": "Role",
            "Job Title": "Role",
            "Position": "Role",
            "Link": "Apply Link"
        }
        df = df.rename(columns=column_mapping)
        
        # Clean all string columns
        for col in df.select_dtypes(include=['object']).columns:
            df[col] = df[col].apply(self.clean_text)
            
        return df

    def filter_jobs(self, all_jobs_list):
        """
        Takes a list of job dicts, filters them, normalizes them, 
        and returns a cleaned DataFrame.
        """
        if not all_jobs_list:
            return pd.DataFrame()

        df = pd.DataFrame(all_jobs_list)
        
        # 1. Normalize fields first to have consistent 'Role' column
        df = self.normalize_fields(df)
        
        # 2. Filter based on keywords in 'Role'
        if 'Role' in df.columns:
            initial_count = len(df)
            df = df[df['Role'].apply(self.is_relevant)]
            filtered_count = initial_count - len(df)
            logger.info(f"Filtered out {filtered_count} irrelevant roles. remaining: {len(df)}")
        else:
            logger.warning("Column 'Role' not found for filtering.")

        return df

job_filter = JobFilter()
