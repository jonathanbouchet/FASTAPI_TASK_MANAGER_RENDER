import logging
import sys

# get logger: returns a logger instance
logger = logging.getLogger()

# formatter: add options to the formatting, ie which fields, etc ...
formatter = logging.Formatter(
    fmt="%(asctime)s - %(levelname)s - %(message)s"
)

# create hanlders: specifies the output of the logger
# in this example, there will be 2 outputs: 1 @ the console, the other in a file called app.log
stream_handler = logging.StreamHandler(sys.stdout)
file_handler = logging.FileHandler('app.log')
stream_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# add handler(s) to the logger
logger.handlers = [stream_handler, file_handler]

# set the level of the logger: INFO, DEBUG, WARN, ERROR, CRITICAL
logger.setLevel(logging.INFO)