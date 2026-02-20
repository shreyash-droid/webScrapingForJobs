import pandas as pd
from utils.logger import logger

class JobScorer:
    def __init__(self):
        # Scoring criteria keywords
        self.visa_keywords = ["visa", "sponsor", "sponsorship", "h1b"]
        self.remote_keywords = ["remote", "work from home", "anywhere"]
        self.startup_keywords = ["startup", "early stage", "series a", "wellfound", "yc"]
        
    def calculate_score(self, row):
        """Calculates a priority score for a single job row."""
        score = 0
        role = str(row.get('Role', '')).lower()
        location = str(row.get('Location', '')).lower()
        source = str(row.get('Source', '')).lower()
        
        # 1. Visa Sponsorship (+3)
        if any(kw in role for kw in self.visa_keywords) or any(kw in location for kw in self.visa_keywords):
            score += 3
            
        # 2. Remote (+2)
        if any(kw in location for kw in self.remote_keywords) or row.get('Remote/On-site', '') == 'Remote':
            score += 2
            
        # 3. Startup (+1)
        if any(kw in source for kw in self.startup_keywords) or any(kw in role for kw in self.startup_keywords):
            score += 1
            
        # 4. Keyword Match (+1)
        # Assuming the filter already ensured base relevance, 
        # but we can add bonus for specific high-interest keywords
        preferred = ["uiux", "product design", "senior frontend"]
        if any(p in role for p in preferred):
            score += 1
            
        return score

    def classify_priority(self, score):
        """Classifies the score into High, Medium, or Low."""
        if score >= 4:
            return "High"
        elif score >= 2:
            return "Medium"
        else:
            return "Low"

    def process(self, df):
        """
        Removes duplicates, assigns scores, and classifies priority.
        """
        if df.empty:
            return df

        # 1. Deduplication
        # Key: Company + Role + Apply Link
        initial_count = len(df)
        df = df.drop_duplicates(subset=['Company', 'Role', 'Apply Link'], keep='first')
        dedup_count = initial_count - len(df)
        if dedup_count > 0:
            logger.info(f"Removed {dedup_count} duplicate listings.")

        # 2. Assign Scores
        df['Score'] = df.apply(self.calculate_score, axis=1)
        
        # 3. Classify Priority
        df['Priority'] = df['Score'].apply(self.classify_priority)
        
        # Sort by Score descending
        df = df.sort_values(by='Score', ascending=False)
        
        return df

job_scorer = JobScorer()
