from openlog import Logger

# Basic console-only logger
logger = Logger()
logger.log("This is an info message")
logger.error("Something went wrong")
logger.warn("This is a warning")
logger.init("System initialized")

# Logger with prefix (no need for manual brackets)
prefix_logger = Logger(prefix="APP")
prefix_logger.log("This is an info message with prefix")
prefix_logger.error("Something went wrong with prefix")

# Logger with short timestamp
short_timestamp_logger = Logger(short_timestamp=True)
short_timestamp_logger.log("This message has short timestamp")
short_timestamp_logger.error("Error with short timestamp")
