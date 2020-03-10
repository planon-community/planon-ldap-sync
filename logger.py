import logging
import os
import sys
import time

log_level = str.upper(os.environ.get('LOG_LEVEL', 'INFO'))

log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

logging.basicConfig(stream = sys.stdout, level = log_level, format = log_format)

# Set the log to use GMT time zone
logging.Formatter.converter = time.gmtime

# Add milliseconds
logging.Formatter.default_msec_format = '%s.%03d'

log = logging.getLogger()

log.debug('Logging started.')