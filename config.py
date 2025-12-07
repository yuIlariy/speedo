# config.py


from dotenv import load_dotenv
import os

load_dotenv()

RESULTS_LOG = os.getenv("RESULTS_LOG", "results/speedlog.json")
TREND_IMAGE = os.getenv("TREND_IMAGE", "results/speedplot.png")
TOKEN = os.getenv("TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))
THUMBNAIL_URL = os.getenv("THUMBNAIL_URL")
LOG_FILE = os.getenv("LOG_FILE", "logs/bot.log")
