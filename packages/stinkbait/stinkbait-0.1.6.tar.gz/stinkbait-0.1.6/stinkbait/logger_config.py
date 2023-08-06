import logging
from logging.handlers import RotatingFileHandler

# Set up logging
logger = logging.getLogger('stinkbait')
logger.setLevel(logging.DEBUG)

# Create file handler that rotates logs
file_handler = RotatingFileHandler('stinkbait.log', maxBytes=10 * 1024 * 1024, backupCount=5)
file_handler.setLevel(logging.WARNING)

# Create console handler for non-debug messages
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Create formatter and add to handlers
formatter = logging.Formatter('%(levelname)s - %(asctime)s - %(message)s', datefmt='%Y/%m/%d/ %I:%M:%S %p %z' )
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add handlers to logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)
