import os
from datetime import datetime

from rich.console import Console


class Logger:
    """
    A versatile logging utility that provides console output with color formatting
    and optional file logging capabilities.

    This logger uses Rich for console output with color formatting and can
    simultaneously write logs to files. It supports different log levels
    (INFO, ERROR, WARN, INIT) and can maintain logs in memory for later retrieval.
    """

    def __init__(self, write_to_file: bool = False, in_dir: bool = False, session: bool = False, prefix: str = "", short_timestamp: bool = False):
        """
        Initialize a new Logger instance.

        Parameters:
            write_to_file (bool, optional): If True, writes logs to file in addition to
                                           console output. Defaults to False.
            in_dir (bool, optional): If True, logs will be stored in a '/logs' directory.
                                    Only takes effect when write_to_file is True.
                                    Defaults to False.
            session (bool, optional): If True, creates a unique log file for each session
                                     with timestamp in the filename. If False, uses a single
                                     'log.txt' file. Only takes effect when write_to_file is True.
                                     Defaults to False.
            prefix (str, optional): A prefix to add before each log message. Defaults to "".
            short_timestamp (bool, optional): If True, uses short timestamp format (HH:MM).
                                             If False, uses full timestamp format (YYYY-MM-DD HH:MM:SS).
                                             Defaults to False.
        """
        self.cls = Console()

        self.write_to_file = write_to_file
        self.prefix = prefix
        self.short_timestamp = short_timestamp

        self.in_dir = in_dir
        self.path_prefix = ""
        if self.in_dir:
            self.path_prefix = "/logs"
            if not os.path.isdir(f"{os.getcwd()}/logs"):
                if self.write_to_file:
                    os.mkdir(f"{os.getcwd()}/logs")

        self.session = session
        if self.session:
            self.log_file_path = (
                os.getcwd()
                + self.path_prefix
                + "/log_"
                + str(datetime.now()).replace(" ", "_").replace(":", "-")
                + ".txt"
            )
        else:
            self.log_file_path = os.getcwd() + self.path_prefix + "/log.txt"

        self.log_list = []
        self.log_list_to_send = []
        if self.write_to_file:
            log_file = self._open_log_file(mode="w+")
            log_file.write(
                f"-----------------------{self._make_timestamp_string()}-----------------------\n"
            )
            log_file.close()

    def _open_log_file(self, mode: str = "a+"):
        """
        Opens the log file with the specified mode.

        Parameters:
            mode (str, optional): The file opening mode. Defaults to "a+" (append and read).

        Returns:
            file: The opened file object.
        """
        file = open(self.log_file_path, mode, encoding="utf-8")
        return file

    def _make_timestamp_string(self) -> str:
        """
        Creates a formatted timestamp string for log entries.

        Returns:
            str: Current timestamp as a string. Format depends on short_timestamp setting:
                 - If short_timestamp is True: 'HH:MM'
                 - If short_timestamp is False: 'YYYY-MM-DD HH:MM:SS'
        """
        timestamp = str(datetime.now()).split(".")[0]
        if self.short_timestamp:
            time_part = timestamp.split(" ")[1]  # Get the time part (HH:MM:SS)
            return ":".join(time_part.split(":")[:2])  # Return only HH:MM
        return timestamp

    def _echo(self, msg: str, m_type: str) -> None:
        """
        Internal method to process and display log messages.

        This method handles both console output with appropriate color formatting
        and file writing if enabled.

        Parameters:
            msg (str): The message content to log.
            m_type (str): The message type/level (INFO, ERROR, WARN, INIT).

        Returns:
            None
        """
        if self.write_to_file:
            if self.prefix:
                bare_log_string = f"[{self._make_timestamp_string()}]::[{self.prefix}]::{m_type}::{msg}\n"
            else:
                bare_log_string = f"[{self._make_timestamp_string()}]::{m_type}::{msg}\n"

            log_file = self._open_log_file()
            log_file.write(bare_log_string)
            log_file.close()

            self.log_list.append(bare_log_string)
            self.log_list_to_send.append(bare_log_string)

        if m_type == "INFO":
            color_code = "blue bold"
        elif m_type == "ERROR":
            color_code = "red bold"
        elif m_type == "WARN":
            color_code = "yellow bold"
        elif m_type == "INIT":
            color_code = "purple bold"
        else:
            color_code = "white bold"

        if self.prefix:
            self.cls.print(
                f"[gray][{self._make_timestamp_string()}][/][red bold]::[/][green bold][{self.prefix}][/][red bold]::[/][{color_code}]{m_type}[/][red bold]::[/]{msg}"
            )
        else:
            self.cls.print(
                f"[gray][{self._make_timestamp_string()}][/][red bold]::[/][{color_code}]{m_type}[/][red bold]::[/]{msg}"
            )

    def log(self, msg: str):
        """
        Logs an informational message.

        Parameters:
            msg (str): The message to log.

        Returns:
            None
        """
        self._echo(msg, "INFO")

    def error(self, msg: str):
        """
        Logs an error message.

        Parameters:
            msg (str): The error message to log.

        Returns:
            None
        """
        self._echo(msg, "ERROR")

    def warn(self, msg: str):
        """
        Logs a warning message.

        Parameters:
            msg (str): The warning message to log.

        Returns:
            None
        """
        self._echo(msg, "WARN")

    def init(self, msg: str):
        """
        Logs an initialization message.

        Parameters:
            msg (str): The initialization message to log.

        Returns:
            None
        """
        self._echo(msg, "INIT")

    def flush_logs(self, from_start: bool = False) -> list:
        """
        Retrieves and clears the pending log messages.

        Parameters:
            from_start (bool, optional): If True, returns all logs since logger
                                        initialization. If False, returns only logs
                                        since the last flush. Defaults to False.

        Returns:
            list: A list of log message strings.
        """
        if from_start:
            self.log_list_to_send = self.log_list
        log_list = self.log_list_to_send.copy()
        self.log_list_to_send = []
        return log_list
