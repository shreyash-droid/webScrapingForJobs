import re
import pandas as pd
from utils.logger import logger
from config.settings import settings


class JobScorer:
    def __init__(self):
        self.visa_keywords = ["visa", "sponsor", "sponsorship", "h1b", "h-1b", "relocation"]
        self.remote_keywords = ["remote", "work from home", "anywhere", "worldwide"]
        self.startup_keywords = ["startup", "early stage", "seed", "series a", "yc", "y combinator"]
        self.experience_keywords = [k.lower() for k in settings.EXPERIENCE_KEYWORDS]
        self.genuine_sources = [s.lower() for s in settings.GENUINE_SOURCES]

    def _text(self, row):
        """Combined lowercase text for keyword scoring (title + tags + description)."""
        parts = [
            str(row.get("Role", "")),
            str(row.get("Tags", "")),
            str(row.get("Description", "")),
        ]
        return " ".join(parts).lower()

    def calculate_score(self, row):
        """Calculates a priority score for a single job row."""
        score = 0
        text = self._text(row)
        location = str(row.get("Location", "")).lower()
        source = str(row.get("Source", "")).lower()

        # Genuine source boost (+2)
        if any(gs in source for gs in self.genuine_sources):
            score += 2

        # Visa sponsorship / relocation (+3) -- now works because we capture descriptions.
        if any(kw in text for kw in self.visa_keywords):
            score += 3

        # Remote (+2)
        if any(kw in location for kw in self.remote_keywords) \
                or any(kw in text for kw in self.remote_keywords) \
                or str(row.get("Remote/On-site", "")).lower() == "remote":
            score += 2

        # Startup signal (+1)
        if any(kw in source for kw in self.startup_keywords) \
                or any(kw in text for kw in self.startup_keywords):
            score += 1

        # Entry-level match (+3 in title, +1 in body) -- surfaces the roles the user wants.
        title = str(row.get("Role", "")).lower()
        if any(kw in title for kw in self.experience_keywords):
            score += 3
        elif any(kw in text for kw in self.experience_keywords):
            score += 1

        return score

    def classify_priority(self, score):
        if score >= 6:
            return "High"
        elif score >= 3:
            return "Medium"
        return "Low"

    @staticmethod
    def _dedup_key(row):
        """Normalized company+role key so the same job on two boards dedupes."""
        raw = f"{row.get('Company', '')} {row.get('Role', '')}".lower()
        return re.sub(r"[^a-z0-9]+", "", raw)

    def process(self, df):
        """Removes duplicates, assigns scores, and classifies priority."""
        if df.empty:
            return df

        # Cross-source deduplication on normalized company+role.
        initial_count = len(df)
        df = df.assign(_key=df.apply(self._dedup_key, axis=1))
        df = df.drop_duplicates(subset=["_key"], keep="first").drop(columns=["_key"])
        removed = initial_count - len(df)
        if removed > 0:
            logger.info(f"Removed {removed} duplicate listings.")

        df["Score"] = df.apply(self.calculate_score, axis=1)
        df["Priority"] = df["Score"].apply(self.classify_priority)
        df = df.sort_values(by="Score", ascending=False).reset_index(drop=True)

        return df


job_scorer = JobScorer()
