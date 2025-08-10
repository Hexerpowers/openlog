# OpenLog

A versatile Python logging utility designed to enhance logging capabilities with rich console output and optional file
logging.

## Features

- 🎨 **Rich Console Output**: Color-coded messages with beautiful formatting
- 📁 **Flexible File Logging**: Optional file output with session support
- 🔧 **Smart Object Formatting**: Intelligent vertical formatting for complex data structures
- 📊 **Multiple Log Levels**: INFO, ERROR, WARN, and INIT with distinct styling
- 💾 **In-Memory Storage**: Retrieve and manage logs programmatically
- 🎯 **Prefix Support**: Add context to your log messages
- 📐 **Terminal-Aware**: Automatic width detection for optimal formatting

## Installation

```bash
pip install openlog
```

## Quick Start

### Basic Console Logging

```python
from openlog import Logger

logger = Logger()
logger.log("This is an info message")
logger.error("Something went wrong")
logger.warn("This is a warning")
logger.init("System initialized")
```
### Batch Logging

```python
# Add multiple messages

logger.batch.add_message("Processing started")
logger.batch.add_message("Loading configuration")
logger.batch.add_message("Connecting to database")

# Log all messages in the batch
logger.flush_batch()
```

### File Logging

```python
# Basic file logging
file_logger = Logger(write_to_file=True)
file_logger.log("This message goes to console and file")

# Session-based logging (timestamped files)
session_logger = Logger(write_to_file=True, session=True)
session_logger.log("Logged with timestamp in filename")

# Organized in /logs directory
dir_logger = Logger(in_dir=True, write_to_file=True)
dir_logger.log("Logs stored in /logs directory")
```

### Smart Object Formatting

```python
# Simple objects stay inline
logger.log({"user": "Alice", "id": 123})

# Complex objects format vertically
complex_data = {
    "users": [
        {"id": 1, "name": "Alice", "roles": ["admin", "user"]},
        {"id": 2, "name": "Bob", "roles": ["user", "viewer"]},
    ],
    "settings": {
        "theme": "dark",
        "notifications": {"email": True, "push": False}
    }
}
logger.log("User data:")
logger.log(complex_data)
```

### Retrieve Logs Programmatically

```python
# Get recent logs
logs = logger.flush_logs()

# Get all logs from start
all_logs = logger.flush_logs(from_start=True)
```

## Documentation

For detailed information about all features, configuration options, and advanced usage, see [FEATURES.md](FEATURES.md).

## Configuration

| Parameter       | Type | Default | Description                     |
|-----------------|------|---------|---------------------------------|
| `write_to_file` | bool | False   | Enable file logging             |
| `in_dir`        | bool | False   | Store logs in `/logs` directory |
| `session`       | bool | False   | Create timestamped log files    |
| `prefix`        | str  | ""      | Add prefix to all messages      |

## Log Levels

- `log()` - General information (blue)
- `error()` - Error messages (red)
- `warn()` - Warning messages (yellow)
- `init()` - Initialization messages (purple)

## Requirements

- Python 3.9+
- Rich library (automatically installed)

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Links

- [GitHub Repository](https://github.com/Hexerpowers/openlog)
- [Detailed Features Documentation](FEATURES.md)
