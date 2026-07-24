import requests
from config.settings import settings
from utils.logger import logger

class TelegramNotifier:
    def __init__(self):
        self.token = settings.TELEGRAM_BOT_TOKEN
        self.chat_id = settings.TELEGRAM_CHAT_ID
        self.base_url = f"https://api.telegram.org/bot{self.token}/sendMessage"

    def send_notification(self, df, top_n=10):
        """Sends a notification with the top-N highest-scoring job matches."""
        if not self.token or not self.chat_id:
            logger.warning("Telegram credentials not set. Skipping notification.")
            return

        top_jobs = df.head(top_n)

        if top_jobs.empty:
            logger.info("No jobs to notify.")
            return

        message = f"🚀 *Top {len(top_jobs)} Job Matches Found!*\n\n"

        for _, row in top_jobs.iterrows():
            company = row.get('Company', 'N/A')
            role = row.get('Role', 'N/A')
            link = row.get('Apply Link', '#')
            priority = row.get('Priority', 'N/A')

            message += f"🏢 *{company}*\n"
            message += f"💼 {role}\n"
            message += f"🔗 [Apply Here]({link})\n"
            message += f"⭐ Priority: {priority}\n"
            message += "─────────────────────\n"

        try:
            payload = {
                "chat_id": self.chat_id,
                "text": message,
                "parse_mode": "Markdown",
                "disable_web_page_preview": True
            }
            response = requests.post(self.base_url, json=payload)
            response.raise_for_status()
            logger.info("Telegram notification sent successfully.")
        except Exception as e:
            logger.error(f"Failed to send Telegram notification: {e}")

notifier = TelegramNotifier()
