from tests.test_cli_log import logger

# OpenLog Features Documentation

This document provides detailed information about OpenLog's features and capabilities.

## Table of Contents
- [Core Logging Features](#core-logging-features)
- [Batch Logging](#batch-logging)
- [Object Formatting](#object-formatting)
- [File Logging](#file-logging)
- [Configuration Options](#configuration-options)
- [Advanced Usage](#advanced-usage)

## Core Logging Features

### Log Levels
OpenLog supports four distinct log levels, each with its own color coding:

- **`log()`** - General information messages (blue)
- **`error()`** - Error messages (red)
- **`warn()`** - Warning messages (yellow)
- **`init()`** - Initialization messages (purple)

### Basic Usage
```python
from openlog import Logger

logger = Logger()
logger.log("This is an info message")
logger.error("Something went wrong")
logger.warn("This is a warning")
logger.init("System initialized")
```

## Batch Logging

### Multiple Messages at Once
OpenLog can process lists of strings, logging each message individually with proper timestamps:

```python
logger.batch.add_message("Starting application")
logger.batch.add_message("Configuration loaded successfully")
logger.batch.add_message("Warning: Using default settings")
logger.add_message("Database connection established")

# Log all messages in the batch
logger.flush_batch()

# You can also use different log levels
logger.flush_batch("ERROR")
```

## Object Formatting

### Intelligent Object Display
OpenLog automatically detects when objects should be formatted vertically for better readability:

- **Threshold-based formatting**: Objects exceeding 50% of terminal width are formatted vertically
- **Smart nested formatting**: Nested objects under 20% width stay inline
- **Clean indentation**: Uses 2-space indentation for optimal terminal readability

### Supported Object Types
- **Lists and Tuples**: Formatted with proper brackets `[]` or `()`
- **Dictionaries**: Clean key-value formatting with `{}`
- **Sets**: Formatted with set notation `{}`
- **Nested structures**: Intelligent mixed inline/vertical formatting
- **String Lists**: Special handling for batch logging

### Examples

#### Simple Objects (Stay Inline)
```python
logger.log([1, 2, 3])  # Short list stays inline
logger.log({"a": 1, "b": 2})  # Short dict stays inline
```

#### String Lists (Batch Logging)
```python
# Lists of strings trigger batch logging
messages = ["Message 1", "Message 2", "Message 3"]
logger.log(messages)
# Output:
# [timestamp]::INFO::Message 1
# [timestamp]::INFO::Message 2  
# [timestamp]::INFO::Message 3
```

#### Complex Objects (Vertical Formatting)
```python
# Long list triggers vertical formatting
long_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
logger.log(long_list)
# Output:
# [
#   1,
#   2,
#   3,
#   ...
# ]

# Complex nested structure
nested_data = {
    "users": [
        {"id": 1, "name": "Alice"},  # Short nested objects stay inline
        {"id": 2, "name": "Bob", "email": "bob@example.com", "roles": ["admin", "user"]}  # Long objects go vertical
    ],
    "config": {"theme": "dark", "lang": "en"}  # Short nested dict stays inline
}
logger.log(nested_data)
```

### Smart Formatting Rules
1. **String List Rule**: Lists containing only strings trigger batch logging
2. **50% Rule**: Main objects exceeding 50% of terminal width format vertically
3. **20% Rule**: Nested objects under 20% of terminal width stay inline
4. **Clean Brackets**: No type labels, just clean bracket notation
5. **Consistent Indentation**: 2-space indentation throughout

## File Logging

### Basic File Logging
```python
file_logger = Logger(write_to_file=True)
file_logger.log("This goes to console and file")
```

### Session-Based Logging
Creates unique log files with timestamps:
```python
session_logger = Logger(write_to_file=True, session=True)
# Creates: log_2024-01-15_14-30-25.txt
```

### Directory Organization
Store logs in a dedicated `/logs` directory:
```python
dir_logger = Logger(in_dir=True, write_to_file=True)
# Creates: ./logs/log.txt
```

### Batch Logging with Files
```python
file_logger = Logger(write_to_file=True)
batch_messages = [
    "Operation started",
    "Processing data",
    "Operation completed"
]
file_logger.log(batch_messages)
# Each message written to file separately with individual timestamps
```

### Log Retrieval
```python
# Get logs since last flush
recent_logs = logger.flush_logs()

# Get all logs from start
all_logs = logger.flush_logs(from_start=True)
```

## Configuration Options

### Logger Parameters
```python
Logger(
    write_to_file=False,  # Enable file logging
    in_dir=False,         # Store in /logs directory
    session=False,        # Create timestamped files
    prefix=""             # Add prefix to all messages
)
```

### Prefix Usage
```python
api_logger = Logger(prefix="[API] ")
api_logger.log("Request received")
# Output: [API] Request received

# Prefix works with batch logging too
api_logger.log([
    "Validating request",
    "Processing request", 
    "Sending response"
])
# Output:
# [API] Validating request
# [API] Processing request
# [API] Sending response
```

## Advanced Usage

### Mixed Content Logging
```python
logger = Logger()

# Regular strings
logger.log("Processing user data...")

# Batch messages
logger.log([
    "Step 1: Validation",
    "Step 2: Transformation",
    "Step 3: Storage"
])

# Objects when needed
user_data = {"id": 123, "name": "Alice", "permissions": ["read", "write"]}
logger.log(user_data)

# Back to strings
logger.log("Processing complete")
```

### Error Handling with Batch Logging
```python
try:
    # Some operation
    result = complex_operation()
except Exception as e:
    logger.error([
        f"Operation failed: {str(e)}",
        "Attempting recovery",
        "Please check system logs"
    ])
    
    error_context = {
        "error": str(e),
        "operation": "complex_operation",
        "timestamp": datetime.now().isoformat()
    }
    logger.error("Error context:")
    logger.error(error_context)
```

### Performance Considerations
- Batch logging processes each string individually for proper timestamps
- Object formatting is only triggered when objects exceed size thresholds
- Terminal width is detected automatically for optimal formatting
- File operations are optimized with proper file handle management
- Memory usage is managed through the flush system

### Best Practices
1. **Use batch logging for sequences**: When logging multiple related messages, use lists
2. **Use appropriate log levels**: `init()` for startup, `error()` for failures, `warn()` for issues, `log()` for general info
3. **Leverage object formatting**: Pass complex data structures directly instead of converting to strings
4. **Use prefixes for context**: Add prefixes to distinguish between different components
5. **Manage log files**: Use `flush_logs()` to retrieve and clear log history when needed
6. **Session logging for debugging**: Use session-based logging during development and debugging

### Terminal Compatibility
- Works with all major terminals (Windows Terminal, iTerm2, Terminal.app, etc.)
- Automatic width detection for optimal formatting
- Fallback to 80-character width if detection fails
- Rich color support with graceful degradation

### File Format
Log files use a structured format:
```
[2024-01-15 14:30:25]::INFO::Your message here
[2024-01-15 14:30:26]::ERROR::Error message
```

This format ensures logs are both human-readable and machine-parseable.
