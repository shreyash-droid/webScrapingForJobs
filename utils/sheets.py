import gspread
from oauth2client.service_account import ServiceAccountCredentials
from config.settings import settings
from utils.logger import logger
import pandas as pd

class InternshipTracker:
    def __init__(self):
        self.scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive"
        ]
        self.creds = None
        self.client = None
        self.spreadsheet = None
        self.sheet = None
        self.sheet_name = "Internship Tracker"
        
        # Columns required by the user
        self.columns = [
            "Company", "Role", "Location", "Remote/Visa", 
            "Link", "Date Posted", "Status", "Priority", "Notes"
        ]

    def authenticate(self):
        try:
            self.creds = ServiceAccountCredentials.from_json_keyfile_name(
                settings.GOOGLE_SHEETS_CREDENTIAL_FILE, self.scope
            )
            self.client = gspread.authorize(self.creds)
            
            # Open spreadsheet by ID
            self.spreadsheet = self.client.open_by_key(settings.SPREADSHEET_ID)
            
            # Try to get or create the worksheet
            try:
                self.sheet = self.spreadsheet.worksheet(self.sheet_name)
                logger.info(f"Connected to existing sheet: {self.sheet_name}")
            except gspread.exceptions.WorksheetNotFound:
                # Create sheet if not found
                self.sheet = self.spreadsheet.add_worksheet(title=self.sheet_name, rows="1000", cols=str(len(self.columns)))
                self.sheet.append_row(self.columns)
                logger.info(f"Created new sheet: {self.sheet_name}")
                
            return True
        except Exception as e:
            logger.error(f"Failed to authenticate with Google Sheets: {e}")
            return False

    def sync_jobs(self, df):
        """
        Appends only new jobs to the sheet, avoiding duplicates.
        """
        if not self.authenticate():
            return

        if df.empty:
            logger.info("No data to sync.")
            return

        # 1. Fetch existing data to check for duplicates
        existing_records = self.sheet.get_all_records()
        existing_links = {str(r.get('Link', '')) for r in existing_records} if existing_records else set()

        # 2. Map DataFrame to requirement columns
        # Scraper DataFrame usually has: Role, Company, Location, Tags, Apply Link, Date, Score, Priority
        new_rows = []
        for _, row in df.iterrows():
            link = str(row.get('Apply Link', ''))
            
            # Cloud-side Deduplication: Skip if link already exists in the sheet
            if link in existing_links:
                continue

            # Format the data for the sheet columns
            # Remote/Visa combines location tags and visa info
            remote_visa = f"{row.get('Location', '')} | {row.get('Tags', '')}"
            
            sheet_row = [
                row.get('Company', 'N/A'),
                row.get('Role', 'N/A'),
                row.get('Location', 'N/A'),
                remote_visa,
                link,
                row.get('Date', 'N/A'),
                "Not Applied", # Default Status
                row.get('Priority', 'Low'),
                ""             # Empty Notes
            ]
            new_rows.append(sheet_row)

        # 3. Append only new rows
        if new_rows:
            self.sheet.append_rows(new_rows, value_input_option='USER_ENTERED')
            logger.info(f"Successfully added {len(new_rows)} new unique jobs to Google Sheets.")
        else:
            logger.info("No new unique jobs found to append.")

tracker = InternshipTracker()
