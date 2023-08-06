#!/usr/bin/env python3

import logging
from logging.handlers import RotatingFileHandler

class ColoredFormatter(logging.Formatter):
    COLORS = {
        logging.DEBUG: '\033[36m',    # cyan
        logging.INFO: '\033[32m',     # green
        logging.WARNING: '\033[33m',  # yellow
        logging.ERROR: '\033[31m',    # red
        logging.CRITICAL: '\033[35m'  # magenta
    }
    RESET = '\033[0m'
    
    def format(self, record):
        levelname = record.levelname
        if record.levelno in self.COLORS:
            levelname_color = self.COLORS[record.levelno] + levelname + self.RESET
            record.levelname = levelname_color
        return super(ColoredFormatter, self).format(record)

# Set up logging
logger = logging.getLogger('stinkbait')
logger.setLevel(logging.DEBUG)

# Create file handler that rotates logs
file_handler = RotatingFileHandler('stinkbait.log', maxBytes=10 * 1024 * 1024, backupCount=5)
file_handler.setLevel(logging.WARNING)

# Create console handler for all messages
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# Create formatter and add to handlers
file_formatter = logging.Formatter('%(levelname)s - %(asctime)s - %(message)s', datefmt='%Y/%m/%d %I:%M:%S %p %z UTC')
console_formatter = ColoredFormatter('%(levelname)s - %(asctime)s - %(message)s', datefmt='%Y/%m/%d %I:%M:%S %p %z UTC')
file_handler.setFormatter(file_formatter)
console_handler.setFormatter(console_formatter)

# Add handlers to logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)
