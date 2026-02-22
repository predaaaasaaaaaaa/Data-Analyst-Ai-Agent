import os
import logging
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Bot Configuration
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')  # REQUIRED: Set in .env file
TELEGRAM_USER_ID = os.getenv('TELEGRAM_USER_ID')  # Optional: restrict to specific user

if not TELEGRAM_BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN environment variable is required")

# Paths
PROJECT_ROOT = Path(__file__).parent
DATA_DIR = PROJECT_ROOT / 'data'
UPLOADS_DIR = DATA_DIR / 'uploads'
REPORTS_DIR = DATA_DIR / 'reports'

# Create directories
DATA_DIR.mkdir(exist_ok=True)
UPLOADS_DIR.mkdir(exist_ok=True)
REPORTS_DIR.mkdir(exist_ok=True)

# Logging Configuration
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format=LOG_FORMAT,
    handlers=[
        logging.FileHandler(PROJECT_ROOT / 'bot.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Analysis Configuration
MAX_FILE_SIZE = 25 * 1024 * 1024  # 25MB
SUPPORTED_FORMATS = ['jpg', 'jpeg', 'png', 'gif', 'pdf']
ANALYSIS_TIMEOUT = 120  # seconds

# OCR Configuration
OCR_LANGUAGES = ['en']
OCR_GPU = False  # Set to True if GPU available

logger.info("Configuration loaded successfully")
