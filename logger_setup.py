# logger_setup.py — Sets up logging so FlowKeys can record what it's doing.
# Logs go to BOTH the terminal (so you can see them) AND a file on disk
# (so you can check them later if something goes wrong).

# === IMPORTS ===
import os                          # For creating folders and working with paths
import logging                     # Python's built-in logging system
from logging.handlers import RotatingFileHandler  # Auto-rotates log files when they get big
import config                      # Our settings file — has LOG_DIR and LOG_FILE

def setup_logger():
    """
    Creates and configures a logger for FlowKeys.
    Returns the logger object that other files can use to write log messages.
    """

    # Create a logger with the name "FlowKeys".
    # All log messages from any file will go through this one logger.
    logger = logging.getLogger("FlowKeys")

    # Set the minimum log level to DEBUG.
    # This means ALL messages (DEBUG, INFO, WARNING, ERROR) will be captured.
    logger.setLevel(logging.DEBUG)

    # If the logger already has handlers, don't add more.
    # This prevents duplicate log messages if setup_logger() is called twice.
    if logger.handlers:
        return logger  # Already set up — just return the existing logger

    # === LOG FORMAT ===
    # This defines what each log line looks like.
    # Example: "2024-01-15 14:30:22 [INFO] FlowKeys started successfully"
    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(message)s",  # timestamp + level + message
        datefmt="%Y-%m-%d %H:%M:%S"                 # date format: year-month-day hour:min:sec
    )

    # === FILE HANDLER (writes logs to a file on disk) ===
    # First, make sure the log folder exists. If not, create it.
    # exist_ok=True means "don't complain if the folder already exists".
    os.makedirs(config.LOG_DIR, exist_ok=True)

    # Build the full path to the log file (e.g., ~/Library/Logs/FlowKeys/flowkeys.log).
    log_path = os.path.join(config.LOG_DIR, config.LOG_FILE)

    # RotatingFileHandler keeps the log file from growing forever.
    # maxBytes=1_000_000 means rotate when the file reaches ~1 MB.
    # backupCount=3 means keep the 3 most recent old log files.
    file_handler = RotatingFileHandler(
        log_path,            # Where to write the log file
        maxBytes=1_000_000,  # Max size before rotating (~1 MB)
        backupCount=3        # Keep 3 old log files (flowkeys.log.1, .2, .3)
    )

    # Apply our format to the file handler so log lines look consistent.
    file_handler.setFormatter(formatter)

    # Only write INFO and above to the file (skip DEBUG to keep file clean).
    file_handler.setLevel(logging.INFO)

    # === CONSOLE HANDLER (prints logs to the terminal) ===
    # This lets you see log messages in real time when running manually.
    console_handler = logging.StreamHandler()

    # Apply the same format to console output.
    console_handler.setFormatter(formatter)

    # Show INFO and above in the terminal too.
    console_handler.setLevel(logging.INFO)

    # === ATTACH HANDLERS TO LOGGER ===
    # Add both handlers so logs go to file AND console simultaneously.
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    # Return the configured logger so other files can use it.
    return logger
