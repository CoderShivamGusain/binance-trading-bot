import logging
import sys
from pathlib import Path

# Directory for logs (same folder as this module)
LOG_DIR = Path(__file__).resolve().parent
LOG_FILE = LOG_DIR / "bot.log"

# Ensure the log file exists
LOG_FILE.touch(exist_ok=True)

# Log format includes timestamp, level, module name, and message
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
formatter = logging.Formatter(LOG_FORMAT)

# File handler (writes to bot.log)
file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
file_handler.setFormatter(formatter)

# Console handler (stdout)
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(formatter)

# Configure root logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
# Avoid adding duplicate handlers if this module is re‑imported
if not any(isinstance(h, logging.FileHandler) for h in logger.handlers):
    logger.addHandler(file_handler)
if not any(isinstance(h, logging.StreamHandler) for h in logger.handlers):
    logger.addHandler(console_handler)
