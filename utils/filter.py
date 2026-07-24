import re
import pandas as pd
from utils.logger import logger
from config.settings import settings


class JobFilter:
    def __init__(self):
        self.keywords = [k.lower() for k in settings.TARGET_ROLES]
        self.exclude_keywords = [k.lower() for k in settings.EXCLUDE_KEYWORDS]
        self.experience_keywords = [k.lower() for k in settings.EXPERIENCE_KEYWORDS]
        self.senior_keywords = [k.lower() for k in settings.SENIOR_KEYWORDS]
        self.strict = settings.STRICT_ENTRY_LEVEL

    def clean_text(self, text):
        """Removes extra whitespace and normalizes a string."""
        if not text or not isinstance(text, str):
            return ""
        return re.sub(r"\s+", " ", text).strip()

    def _has_senior_years(self, text):
        """True if the text mentions 2+ (or more) years of required experience."""
        for match in re.findall(r"(\d+)\s*\+?\s*(?:-\s*\d+\s*)?years?", text):
            try:
                if int(match) >= 2:
                    return True
            except ValueError:
                continue
        return False

    def is_relevant(self, role_title, description=""):
        """
        Relevance is decided in two independent stages:

        1. ROLE match  -> the title must mention one of our target roles.
        2. SENIORITY   -> drop only titles that are *explicitly* too senior.

        Experience level is NOT a hard gate (unless STRICT_ENTRY_LEVEL is on):
        an untitled/ambiguous role is kept and left for the scorer to rank, which
        is what stops the pipeline from silently discarding almost everything.
        """
        if not role_title:
            return False

        title = role_title.lower()
        desc = (description or "").lower()

        # 1. Target-role match (required).
        if not any(kw in title for kw in self.keywords):
            return False

        # 2. Hard exclusions (game, backend, ...).
        if any(ex in title for ex in self.exclude_keywords):
            return False

        # 3. Explicitly-senior roles are dropped.
        if any(term in title for term in self.senior_keywords):
            return False
        if self._has_senior_years(title):
            return False

        # 4. Entry-level handling.
        is_entry = (
            any(kw in title for kw in self.experience_keywords)
            or any(kw in desc[:1000] for kw in self.experience_keywords)
        )
        if self.strict:
            # Only keep roles with an explicit entry-level signal.
            return is_entry

        # Non-strict (default): also drop roles whose *description* demands 2+ years.
        if self._has_senior_years(desc[:1000]):
            return False
        return True

    def normalize_fields(self, df):
        """Normalizes column names and cleans text fields."""
        column_mapping = {
            "Title": "Role",
            "Job Title": "Role",
            "Position": "Role",
            "Link": "Apply Link",
        }
        df = df.rename(columns=column_mapping)

        for col in df.select_dtypes(include=["object"]).columns:
            df[col] = df[col].apply(self.clean_text)

        return df

    def filter_jobs(self, all_jobs_list):
        """Takes a list of job dicts, filters and normalizes them into a DataFrame."""
        if not all_jobs_list:
            return pd.DataFrame()

        df = pd.DataFrame(all_jobs_list)
        df = self.normalize_fields(df)

        if "Role" not in df.columns:
            logger.warning("Column 'Role' not found for filtering.")
            return df

        initial_count = len(df)

        def apply_filter(row):
            return self.is_relevant(row.get("Role", ""), row.get("Description", ""))

        df = df[df.apply(apply_filter, axis=1)]
        logger.info(
            f"Filtered out {initial_count - len(df)} irrelevant roles. remaining: {len(df)}"
        )
        return df


job_filter = JobFilter()
