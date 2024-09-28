import logging
import os

def setup_logger():
    # Create logger instance
    logger = logging.getLogger('app_logger')
    logger.setLevel(logging.DEBUG)  # Set lowest level to capture all messages
    
    # Create a file handler to save logs to a file
    file_handler = logging.FileHandler(os.environ.get('LOGGING_LOCATION', 'app.log'))
    file_handler.setLevel(logging.DEBUG)  # Log everything to the file
    
    # Create a console handler to print logs to the console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)  # Log info and above to the console
    
    # Define the format for log messages
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # Add handlers to the logger
    if not logger.hasHandlers():
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
    
    return logger

logger = setup_logger()
