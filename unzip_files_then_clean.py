#!/usr/bin/env python3
"""
Advanced ZIP Extraction and Directory Reorganization Tool.

This script performs three main operations with comprehensive logging, statistics,
and error handling:
1. Extracts all ZIP files in a directory into corresponding subdirectories
2. Removes Apple system files (.DS_Store, .__MACOSX folders, etc.)
3. Reorganizes directories by moving single-child directories up one level

Features:
- Three verbosity levels (0=silent, 1=normal, 2=verbose)
- Centralized output through OperationStats class
- Comprehensive statistics collection
- Modern Python typing with pipe syntax
- Configurable confirmation prompts
- Detailed Google-style documentation with examples

Example usage:
    # Default verbose mode (shows all operations)
    $ python unzip_files_then_clean.py /path/to/directory

    # Clean only mode with normal verbosity
    $ python unzip_files_then_clean.py /path/to/directory --clean-only -v1

    # Silent mode (only errors)
    $ python unzip_files_then_clean.py /path/to/directory -v0

    # No confirmation prompts with normal verbosity
    $ python unzip_files_then_clean.py /path/to/directory --no-confirm -v1
"""

import argparse
import fcntl
import os
import re
import shutil
import sys
import zipfile
from dataclasses import dataclass, field
from enum import Enum, auto
from pathlib import Path
from typing import Generator, List, Set, Tuple, Literal, Optional

# Constants
MAX_ZIP_SIZE = 10 * 1024 * 1024 * 1024  # 10GB
MAX_RECURSION_DEPTH = 10
DEFAULT_VERBOSITY = 2

# Try to import optional dependencies for enhanced output
try:
    from colorama import init, Fore, Back, Style

    init(autoreset=True)
    HAS_COLORAMA = True
except ImportError:
    HAS_COLORAMA = False

    def init(*args, **kwargs):
        """Stub function for Colorama import fallback."""
        pass

    # Fallback color definitions if colorama is not available
    class Fore:
        BLACK = RED = GREEN = YELLOW = BLUE = MAGENTA = CYAN = WHITE = RESET = ""

    class Back:
        BLACK = RED = GREEN = YELLOW = BLUE = MAGENTA = CYAN = WHITE = RESET = ""

    class Style:
        DIM = NORMAL = BRIGHT = RESET_ALL = ""


try:
    from rich.console import Console
    from rich.table import Table
    from rich import box

    HAS_RICH = True
    HAS_TABULATE = False
except ImportError:
    HAS_RICH = False
    # Fallback to 'tabulate' if 'rich' is not available
    try:
        from tabulate import tabulate

        HAS_TABULATE = True
    except ImportError:
        HAS_TABULATE = False

        def tabulate(data, headers=None, *args, **kwargs):
            """Simple tabulate fallback when neither rich nor tabulate is available."""
            if not data:
                return ""

            # Calculate column widths
            col_widths = []
            for i in range(len(data[0])):
                max_width = max(len(str(row[i])) for row in data)
                if headers:
                    max_width = max(max_width, len(str(headers[i])))
                col_widths.append(max_width)

            # Create an ASCII table
            divider = "+" + "+".join("-" * (w + 2) for w in col_widths) + "+"
            table = [divider]

            if headers:
                header_row = (
                    "| "
                    + " | ".join(f"{str(h):<{w}}" for h, w in zip(headers, col_widths))
                    + " |"
                )
                table.extend([header_row, divider])

            for row in data:
                table.append(
                    "| "
                    + " | ".join(f"{str(i):<{w}}" for i, w in zip(row, col_widths))
                    + " |"
                )
            table.append(divider)
            return "\n".join(table)


class LogLevel(Enum):
    """Enumeration of log levels with associated colors.

    Attributes:
        INFO: General informational messages
        WARNING: Potential issues that don't prevent execution
        ERROR: Critical errors that may affect results
        SUCCESS: Successful operations
        OPERATION: Main operation indicators
    """

    INFO = auto()
    WARNING = auto()
    ERROR = auto()
    SUCCESS = auto()
    OPERATION = auto()
    DEBUG = auto()

    def get_color(self) -> str:
        """Return the appropriate color for each log level.

        Returns:
            ANSI color code string or empty string if colorama not available.
        """
        if not HAS_COLORAMA:
            return ""
        return {
            LogLevel.INFO: Fore.CYAN,
            LogLevel.WARNING: Fore.YELLOW,
            LogLevel.ERROR: Fore.RED,
            LogLevel.SUCCESS: Fore.GREEN,
            LogLevel.OPERATION: Fore.MAGENTA,
            LogLevel.DEBUG: Fore.BLUE,
        }.get(self, "")


@dataclass
class LogEntry:
    """Represents a single log entry with metadata.

    Attributes:
        message: The log message content
        level: Severity level of the message
        timestamp: Optional timestamp (not currently used)
    """

    message: str
    level: LogLevel = LogLevel.INFO
    timestamp: float | None = field(default=None, repr=False)


@dataclass
class OperationStats:
    """Collects and reports statistics for all operations.

    Tracks count for various operations and stores detailed logs.
    Provides formatted output for both console and rich displays.

    Attributes:
        total_zips: Total ZIP files processed
        successful_extractions: Successfully extracted ZIPs
        failed_extractions: Failed extractions
        files_removed: Apple system files removed
        dirs_removed: Apple system directories removed
        dirs_examined: Directories examined for reorganization
        dirs_reorganized: Directories successfully reorganized
        dirs_ignored: Directories skipped during reorganization
        logs: Collection of all log entries
        removed_files_details: Detailed list of removed files/dirs
    """

    total_zips: int = 0
    successful_extractions: int = 0
    failed_extractions: int = 0
    files_removed: int = 0
    dirs_removed: int = 0
    dirs_examined: int = 0
    dirs_reorganized: int = 0
    dirs_ignored: int = 0
    logs: List[LogEntry] = field(default_factory=list)
    removed_files_details: List[str] = field(default_factory=list)
    warnings: int = 0
    errors: int = 0

    def add_log(self, message: str, level: LogLevel = LogLevel.INFO) -> None:
        """Add a new log entry to the collection.

        Args:
            message: The log message to add
            level: Severity level of the message
        """
        if level == LogLevel.WARNING:
            self.warnings += 1
        elif level == LogLevel.ERROR:
            self.errors += 1
        self.logs.append(LogEntry(message, level))

    def add_removed_file_detail(self, path: str) -> None:
        """Add details of a removed file/directory for verbose output.

        Args:
            path: Path of the removed file/directory
        """
        self.removed_files_details.append(path)

    def print_summary(self, verbosity: int = DEFAULT_VERBOSITY) -> None:
        """Print a comprehensive summary of all operations.

        Uses rich for display if available, falls back to tabulate or ASCII.

        Args:
            verbosity: Controls output detail (0-2)
        """
        if verbosity == 0:
            return

        if HAS_RICH:
            self._print_rich_summary()
        else:
            self._print_basic_summary()

    def _print_rich_summary(self) -> None:
        """Generate and print a rich formatted summary table."""
        console = Console()
        summary_table = Table(
            title="[bold]PROCESSING SUMMARY[/bold]",
            box=box.ROUNDED,
            show_header=True,
            header_style="bold magenta",
            title_style="bold green",
        )

        summary_table.add_column("Category", style="cyan", no_wrap=True)
        summary_table.add_column("Metric", style="yellow")
        summary_table.add_column("Value", style="green", justify="right")

        # ZIP Processing section
        summary_table.add_row(
            "[bold]ZIP Processing[/bold]",
            "[bold]Files Processed[/bold]",
            str(self.total_zips),
        )
        summary_table.add_row("", "Successful", str(self.successful_extractions))
        summary_table.add_row("", "Failed", str(self.failed_extractions))
        success_rate = (
            f"[green]{self.successful_extractions / self.total_zips * 100:.1f}%[/green]"
            if self.total_zips
            else "N/A"
        )
        summary_table.add_row("", "Success Rate", success_rate, end_section=True)

        # Cleaning section
        summary_table.add_row(
            "[bold]Cleaning[/bold]",
            "[bold]Files Removed[/bold]",
            str(self.files_removed),
        )
        summary_table.add_row("", "Directories Removed", str(self.dirs_removed))
        summary_table.add_row(
            "",
            "Total Cleaned",
            str(self.files_removed + self.dirs_removed),
            end_section=True,
        )

        # Reorganization section
        summary_table.add_row(
            "[bold]Reorganization[/bold]",
            "[bold]Examined[/bold]",
            str(self.dirs_examined),
        )
        summary_table.add_row("", "Reorganized", str(self.dirs_reorganized))
        summary_table.add_row("", "Ignored", str(self.dirs_ignored))
        reorg_rate = (
            f"[green]{self.dirs_reorganized / self.dirs_examined * 100:.1f}%[/green]"
            if self.dirs_examined
            else "N/A"
        )
        summary_table.add_row("", "Reorg Rate", reorg_rate, end_section=True)

        # Error/Warning section
        warnings_color = "green" if self.warnings == 0 else "yellow"
        errors_color = "green" if self.errors == 0 else "red"
        summary_table.add_row(
            "[bold]Issues[/bold]",
            "[bold]Warnings[/bold]",
            f"[{warnings_color}]{self.warnings}[/{warnings_color}]",
        )
        summary_table.add_row(
            "", "[bold]Errors[/bold]", f"[{errors_color}]{self.errors}[/{errors_color}]"
        )

        console.print(summary_table)

    def _print_basic_summary(self) -> None:
        """Generate and print a basic ASCII-formatted summary table."""
        summary_data = [
            ["ZIP Processing", "Files Processed", self.total_zips],
            ["", "Successful", self.successful_extractions],
            ["", "Failed", self.failed_extractions],
            [
                "",
                "Success Rate",
                (
                    f"{self.successful_extractions / self.total_zips * 100:.1f}%"
                    if self.total_zips
                    else "N/A"
                ),
            ],
            ["Cleaning", "Files Removed", self.files_removed],
            ["", "Directories Removed", self.dirs_removed],
            ["", "Total Cleaned", self.files_removed + self.dirs_removed],
            ["Reorganization", "Examined", self.dirs_examined],
            ["", "Reorganized", self.dirs_reorganized],
            ["", "Ignored", self.dirs_ignored],
            [
                "",
                "Reorg Rate",
                (
                    f"{self.dirs_reorganized / self.dirs_examined * 100:.1f}%"
                    if self.dirs_examined
                    else "N/A"
                ),
            ],
            ["Issues", "Warnings", self.warnings],
            ["", "Errors", self.errors],
        ]

        print(
            "\n"
            + tabulate(
                summary_data,
                headers=["Category", "Metric", "Value"],
                tablefmt="fancy_grid",
                colalign=("left", "left", "right"),
                stralign="center",
            )
        )

    def print_logs(self, verbosity: int = DEFAULT_VERBOSITY) -> None:
        """Print all collected logs in formatted output.

        Args:
            verbosity: Controls output detail (0-2)
        """
        if verbosity < 2 or not self.logs:
            return

        if HAS_RICH:
            self._print_rich_logs()
        else:
            self._print_basic_logs()

    def _print_rich_logs(self) -> None:
        """Print logs using rich formatting."""
        console = Console()
        log_table = Table(
            title="[bold]PROCESS LOGS[/bold]",
            box=box.SIMPLE_HEAVY,
            show_header=True,
            header_style="bold blue",
        )

        log_table.add_column("Level", style="cyan", width=8)
        log_table.add_column("Message", style="white")

        for log in self.logs:
            level_style = {
                LogLevel.INFO: "[cyan]INFO[/cyan]",
                LogLevel.WARNING: "[yellow]WARN[/yellow]",
                LogLevel.ERROR: "[red]ERROR[/red]",
                LogLevel.SUCCESS: "[green]SUCCESS[/green]",
                LogLevel.OPERATION: "[magenta]→[/magenta]",
                LogLevel.DEBUG: "[blue]DEBUG[/blue]",
            }.get(log.level, "")
            log_table.add_row(level_style, log.message)

        console.print(log_table)

    def _print_basic_logs(self) -> None:
        """Print logs using basic ASCII formatting."""
        log_data = []
        for log in self.logs:
            prefix = {
                LogLevel.INFO: "[INFO]",
                LogLevel.WARNING: "[WARN]",
                LogLevel.ERROR: "[ERR]",
                LogLevel.SUCCESS: "[OK]",
                LogLevel.OPERATION: "→",
                LogLevel.DEBUG: "[DBG]",
            }.get(log.level, "")
            log_data.append([prefix, log.message])

        print(
            tabulate(
                log_data,
                headers=["Level", "Message"],
                tablefmt="fancy_outline",
                colalign=("center", "left"),
            )
        )


# Constants for Apple system files/directories to remove
APPLE_SYSTEM_FILES: Set[str] = {
    ".DS_Store",
    "._.DS_Store",
    ".AppleDouble",
    ".LSOverride",
    re.compile(r"^\._.*$"),  # Files starting with ._
}

APPLE_SYSTEM_DIRS: Set[str] = {
    "__MACOSX",
    ".__MACOSX",
    ".Spotlight-V100",
    ".Trashes",
    ".fseventsd",
}


def is_apple_system_file(filename: str) -> bool:
    """Check if a filename matches known Apple system file patterns.

    Args:
        filename: The filename to check

    Returns:
        True if the file is an Apple system file, False otherwise

    Examples:
        >>> is_apple_system_file(".DS_Store")
        True
        >>> is_apple_system_file("._hidden_file")
        True
        >>> is_apple_system_file("normal_file.txt")
        False
    """
    if filename in APPLE_SYSTEM_FILES:
        return True

    for pattern in APPLE_SYSTEM_FILES:
        if isinstance(pattern, re.Pattern):
            if pattern.match(filename):
                return True
        elif filename.startswith(pattern.replace("*", "")):
            return True

    return False


def check_readable(path: Path, stats: OperationStats) -> bool:
    """Check if a path is readable with detailed error handling.

    Args:
        path: Path object to check
        stats: OperationStats instance for logging

    Returns:
        bool: True if readable, False otherwise with detailed error logging
    """
    try:
        # Check basic readability
        if not os.access(path, os.R_OK):
            stats.add_log(f"Path not readable (no R_OK): {path}", LogLevel.DEBUG)
            return False

        # For directories, we also need execute permission
        if path.is_dir() and not os.access(path, os.X_OK):
            stats.add_log(f"Directory not executable (no X_OK): {path}", LogLevel.DEBUG)
            return False

        return True

    except PermissionError as e:
        stats.add_log(
            f"Permission denied checking readability: {path} - {str(e)}",
            LogLevel.WARNING,
        )
        return False
    except FileNotFoundError:
        stats.add_log(
            f"Path not found when checking readability: {path}", LogLevel.ERROR
        )
        return False
    except OSError as e:
        stats.add_log(
            f"OS error checking readability: {path} - {str(e)}", LogLevel.ERROR
        )
        return False
    except Exception as e:
        stats.add_log(
            f"Unexpected error checking readability: {path} - {str(e)}", LogLevel.ERROR
        )
        return False


def check_writable(path: Path, stats: OperationStats) -> bool:
    """Check if a path is writable with comprehensive error handling.

    Args:
        path: Path object to check
        stats: OperationStats instance for logging

    Returns:
        bool: True if writable, False otherwise with error details
    """
    try:
        # First check parent directory if file doesn't exist
        if not path.exists():
            parent = path.parent
            if not os.access(parent, os.W_OK):
                stats.add_log(
                    f"Parent directory not writable: {parent}", LogLevel.DEBUG
                )
                return False
            return True

        if not os.access(path, os.W_OK):
            stats.add_log(f"Path not writable: {path}", LogLevel.DEBUG)
            return False
        return True

    except PermissionError as e:
        stats.add_log(
            f"Permission denied checking writability: {path} - {str(e)}",
            LogLevel.WARNING,
        )
        return False
    except FileNotFoundError:
        stats.add_log(
            f"Parent directory not found when checking writability: {path}",
            LogLevel.ERROR,
        )
        return False
    except OSError as e:
        stats.add_log(
            f"OS error checking writability: {path} - {str(e)}", LogLevel.ERROR
        )
        return False
    except Exception as e:
        stats.add_log(
            f"Unexpected error checking writability: {path} - {str(e)}", LogLevel.ERROR
        )
        return False


def safe_path(path: Path, stats: OperationStats) -> Path:
    """Ensure a path name uses safe encoding with proper error recovery.

    Args:
        path: Original path to sanitize
        stats: OperationStats instance for logging

    Returns:
        Path: Safe version of the path with ASCII fallback if needed
    """
    try:
        # First try UTF-8 encoding
        path_str = str(path)
        path_str.encode("utf-8")  # Test encoding
        return path

    except UnicodeEncodeError:
        try:
            # Fallback to ASCII with replacement
            new_name = path.name.encode("ascii", errors="replace").decode("ascii")
            stats.add_log(
                f"Converted problematic filename: {path.name} -> {new_name}",
                LogLevel.INFO,
            )
            return path.with_name(new_name)
        except Exception as e:
            stats.add_log(
                f"Critical error in safe_path fallback: {str(e)}", LogLevel.ERROR
            )
            return path  # Return original as last resort
    except Exception as e:
        stats.add_log(f"Unexpected error in safe_path: {str(e)}", LogLevel.ERROR)
        return path  # Return original on unexpected errors


def is_network_path(path: Path, stats: OperationStats) -> bool:
    """Check if a path is on a network location with robust error handling.

    Args:
        path: Path to check
        stats: OperationStats instance for logging

    Returns:
        bool: True if network path, False otherwise with error details
    """
    try:
        # First try modern Path method
        if hasattr(path, "is_mount"):
            is_mount = path.is_mount()
            if is_mount:
                stats.add_log(
                    f"Network path detected (is_mount=True): {path}", LogLevel.DEBUG
                )
            return is_mount

        # Fallback for older Python versions
        path_str = str(path)
        if any(part.startswith("\\\\") for part in path.parts):
            stats.add_log(f"Network path detected (UNC path): {path}", LogLevel.DEBUG)
            return True
        return False

    except AttributeError:
        stats.add_log(
            "Path.is_mount() not available - using string detection", LogLevel.DEBUG
        )
        try:
            if any(part.startswith("\\\\") for part in path.parts):
                stats.add_log(
                    f"Network path detected (fallback): {path}", LogLevel.DEBUG
                )
                return True
            return False
        except Exception as e:
            stats.add_log(
                f"Error in network path fallback detection: {str(e)}", LogLevel.ERROR
            )
            return False
    except Exception as e:
        stats.add_log(
            f"Unexpected error checking network path: {str(e)}", LogLevel.ERROR
        )
        return False


def is_path_too_long(path: Path, stats: OperationStats) -> bool:
    """Check if a path exceeds system limits with platform-specific handling.

    Args:
        path: Path to check
        stats: OperationStats instance for logging

    Returns:
        bool: True if the path is too long, False otherwise
    """
    try:
        path_str = str(path)

        # Windows-specific checks
        if os.name == "nt":
            # 260 characters including null terminator
            if len(path_str) > 259:
                stats.add_log(
                    f"Windows path too long: {len(path_str)} characters",
                    LogLevel.WARNING,
                )
                return True

            # Additional Windows path length rules
            if "~" in path_str:  # Check for 8.3 compatibility
                try:
                    long_path = path.resolve()
                    if len(str(long_path)) > 259:
                        stats.add_log(
                            f"Windows 8.3 path too long: {len(str(long_path))} characters",
                            LogLevel.WARNING,
                        )
                        return True
                except Exception as e:
                    stats.add_log(f"Error resolving 8.3 path: {str(e)}", LogLevel.DEBUG)
                    pass

        # Unix systems generally don't have length limits
        return False

    except OSError as e:
        stats.add_log(f"OS error checking path length: {str(e)}", LogLevel.ERROR)
        return False
    except Exception as e:
        stats.add_log(
            f"Unexpected error checking path length: {str(e)}", LogLevel.ERROR
        )
        return False


def acquire_lock(filepath: Path) -> Optional[int]:
    """Acquire a file lock to prevent concurrent modifications."""
    try:
        if os.name == "posix":
            lock_file = filepath.with_suffix(".lock")
            lock_fd = os.open(lock_file, os.O_CREAT | os.O_WRONLY)
            fcntl.flock(lock_fd, fcntl.LOCK_EX)
            return lock_fd
        elif os.name == "nt":
            import msvcrt

            lock_file = filepath.with_suffix(".lock")
            lock_fd = os.open(lock_file, os.O_CREAT | os.O_WRONLY)
            msvcrt.locking(lock_fd, msvcrt.LK_LOCK, 1)
            return lock_fd
    except Exception:
        return None


def release_lock(lock_fd: int | None, stats: OperationStats) -> None:
    """Release a previously acquired file lock.

    Args:
        lock_fd: File descriptor of the lock file or None
        stats: OperationStats instance for logging
    """
    if lock_fd is None:
        return

    try:
        if os.name == "posix":
            fcntl.flock(lock_fd, fcntl.LOCK_UN)
            os.close(lock_fd)
        elif os.name == "nt":
            import msvcrt

            msvcrt.locking(lock_fd, msvcrt.LK_UNLCK, 1)
            os.close(lock_fd)
    except (OSError, AttributeError) as e:
        # AttributeError in case msvcrt import failed on Windows
        stats.add_log(f"Error releasing lock: {e}", LogLevel.WARNING)


def remove_apple_system_files(
    directory: Path, stats: OperationStats, verbosity: int = DEFAULT_VERBOSITY
) -> Tuple[int, int]:
    """Recursively remove Apple system files and directories.

    Walks through a directory tree and removes any files/directories
    that match known Apple system file patterns.

    Args:
        directory: Root directory to clean
        stats: OperationStats instance for logging

    Returns:
        Tuple of (files_removed, dirs_removed) counts

    Examples:
        >>> my_stats = OperationStats()
        >>> remove_apple_system_files(Path("/tmp"), my_stats)
        (3, 1)  # Example return values
    """
    files_removed, dirs_removed = 0, 0

    try:
        for path in sorted(
            directory.glob("**/*"), key=lambda p: len(p.parts), reverse=True
        ):
            try:
                if not path.exists():
                    continue

                # Skip special files and links
                if path.is_symlink():
                    if verbosity >= 2:
                        stats.add_log(f"Skipping symbolic link: {path}", LogLevel.DEBUG)
                    continue

                if (
                    path.is_socket()
                    or path.is_fifo()
                    or path.is_char_device()
                    or path.is_block_device()
                ):
                    if verbosity >= 2:
                        stats.add_log(f"Skipping special file: {path}", LogLevel.DEBUG)
                    continue

                if path.is_dir() and path.name in APPLE_SYSTEM_DIRS:
                    try:
                        shutil.rmtree(path)
                        dirs_removed += 1
                        stats.add_removed_file_detail(str(path))
                        stats.add_log(f"Removed Apple directory: {path}", LogLevel.INFO)
                    except OSError as e:
                        stats.add_log(f"Error removing {path}: {e}", LogLevel.ERROR)

                elif path.is_file() and is_apple_system_file(path.name):
                    try:
                        path.unlink()
                        files_removed += 1
                        stats.add_removed_file_detail(str(path))
                        stats.add_log(f"Removed Apple file: {path}", LogLevel.INFO)
                    except OSError as e:
                        stats.add_log(f"Error removing {path}: {e}", LogLevel.ERROR)

            except OSError as e:
                stats.add_log(f"Error processing {path}: {e}", LogLevel.ERROR)

    except Exception as e:
        stats.add_log(f"Unexpected error during cleanup: {e}", LogLevel.ERROR)

    return files_removed, dirs_removed


def extract_zip_files(
    source_dir: Path,
    stats: OperationStats,
    no_confirm: bool = False,
    verbosity: int = DEFAULT_VERBOSITY,
) -> None:
    """Extract all ZIP files in the directory to corresponding subdirectories.

    For each ZIP file found:
    1. Creates a subdirectory with the ZIP's basename
    2. Extracts contents into the subdirectory
    3. Removes Apple system files from extracted contents
    4. Deletes the original ZIP if extraction succeeds

    Args:
        source_dir: Directory containing ZIP files
        stats: OperationStats instance for logging
        no_confirm: Skip confirmation prompts if True
        verbosity: Controls output detail (0-2)

    Examples:
        >>> my_stats = OperationStats()
        >>> extract_zip_files(Path("/tmp/zips"), my_stats, no_confirm=True)
    """
    for i, zip_file in enumerate(source_dir.glob("*.zip")):
        stats.total_zips += 1
        dest_dir = source_dir / zip_file.stem

        stats.add_log(f"Processing ZIP: {zip_file.name}", LogLevel.OPERATION)
        stats.add_log(f"Creating directory: {dest_dir}", LogLevel.INFO)

        # Check for path length issues (Windows)
        if is_path_too_long(dest_dir, stats):
            stats.add_log(f"Path too long for Windows: {dest_dir}", LogLevel.ERROR)
            stats.failed_extractions += 1
            continue

        # Check ZIP file size
        try:
            zip_size = zip_file.stat().st_size
            if zip_size > MAX_ZIP_SIZE:
                stats.add_log(
                    f"ZIP file too large ({zip_size/1024/1024:.2f} MB): {zip_file}",
                    LogLevel.WARNING,
                )
                if not no_confirm and not get_user_confirmation(
                    "Proceed with large file?", default=False, stats=stats
                ):
                    stats.add_log("Skipped large ZIP file", LogLevel.INFO)
                    stats.failed_extractions += 1
                    continue
        except OSError as e:
            stats.add_log(f"Error checking ZIP size: {e}", LogLevel.ERROR)
            stats.failed_extractions += 1
            continue

        # Check if the destination exists
        if dest_dir.exists():
            stats.add_log("Destination directory exists", LogLevel.WARNING)
            if not no_confirm and not get_user_confirmation(
                "Overwrite contents?", default=False, stats=stats
            ):
                stats.add_log("Skipped by user", LogLevel.INFO)
                stats.failed_extractions += 1
                continue

            try:
                shutil.rmtree(dest_dir)
                stats.add_log("Cleared existing directory", LogLevel.OPERATION)
            except OSError as e:
                stats.add_log(f"Clear failed: {e}", LogLevel.ERROR)
                stats.failed_extractions += 1
                continue

        # Create the destination directory
        try:
            dest_dir.mkdir(exist_ok=True)
        except OSError as e:
            stats.add_log(f"Failed to create directory: {e}", LogLevel.ERROR)
            stats.failed_extractions += 1
            continue

        # Extract ZIP contents
        try:
            with zipfile.ZipFile(zip_file, "r") as zip_ref:
                # Check for corrupted files
                corrupted = zip_ref.testzip()
                if corrupted:
                    stats.add_log(f"Corrupted file in ZIP: {corrupted}", LogLevel.ERROR)
                    stats.failed_extractions += 1
                    continue

                # Check for encrypted files
                if any(f.flag_bits & 0x1 for f in zip_ref.infolist()):
                    stats.add_log(
                        f"Password-protected ZIP detected: {zip_file}",
                        LogLevel.WARNING,
                    )
                    if not no_confirm and not get_user_confirmation(
                        "Attempt extraction without password?",
                        default=False,
                        stats=stats,
                    ):
                        stats.add_log("Skipped password-protected ZIP", LogLevel.INFO)
                        stats.failed_extractions += 1
                        continue

                # Check for unsafe paths
                for info in zip_ref.infolist():
                    if os.path.isabs(info.filename) or "../" in info.filename:
                        stats.add_log(
                            f"ZIP contains unsafe paths: {info.filename}",
                            LogLevel.ERROR,
                        )
                        stats.failed_extractions += 1
                        raise zipfile.BadZipFile("Unsafe path detected")

                # Perform extraction
                zip_ref.extractall(dest_dir)

            # Clean Apple system files from extracted contents
            files_removed, dirs_removed = remove_apple_system_files(
                dest_dir, stats, verbosity
            )
            stats.files_removed += files_removed
            stats.dirs_removed += dirs_removed

            # Check if extraction produced any content
            if any(dest_dir.iterdir()):
                try:
                    zip_file.unlink()
                    stats.successful_extractions += 1
                    stats.add_log("Extraction successful", LogLevel.SUCCESS)
                except OSError as e:
                    stats.add_log(f"Failed to remove ZIP: {e}", LogLevel.ERROR)
                    stats.failed_extractions += 1
            else:
                stats.add_log("Empty ZIP file", LogLevel.ERROR)
                stats.failed_extractions += 1

        except zipfile.BadZipFile as e:
            stats.add_log(f"Bad ZIP file: {e}", LogLevel.ERROR)
            stats.failed_extractions += 1
            try:
                shutil.rmtree(dest_dir)
            except OSError as e:
                stats.add_log(
                    f"Failed to remove directory {dest_dir}: {e}", LogLevel.WARNING
                )
        except Exception as e:
            stats.add_log(f"Unexpected error during extraction: {e}", LogLevel.ERROR)
            stats.failed_extractions += 1
            try:
                shutil.rmtree(dest_dir)
            except OSError as e:
                stats.add_log(
                    f"Failed to remove directory {dest_dir}: {e}", LogLevel.WARNING
                )


def find_single_child_dirs(root_dir: Path) -> Generator[Tuple[Path, Path], None, None]:
    """Find directories containing exactly one subdirectory and no other items."""
    for parent_dir in root_dir.iterdir():
        if parent_dir.is_dir():
            try:
                children = list(parent_dir.iterdir())
                dir_children = [c for c in children if c.is_dir()]

                if len(dir_children) == 1 and len(children) == 1:
                    yield parent_dir, dir_children[0]
            except OSError as e:
                continue


def reorganize_directories(
    source_dir: Path,
    stats: OperationStats,
    no_confirm: bool = False,
    verbosity: int = DEFAULT_VERBOSITY,
) -> None:
    """Reorganize a directory structure by moving single-child directories up.

    For each directory containing exactly one subdirectory:
    1. Moves the child directory up one level
    2. Removes the now-empty parent directory (which is now empty)

    Args:
        source_dir: Directory to reorganize
        stats: OperationStats instance for logging
        no_confirm: Skip confirmation prompts if True
        verbosity: Controls output detail (0-2)

    Examples:
        >>> my_stats = OperationStats()
        >>> reorganize_directories(Path("/tmp"), my_stats, no_confirm=True)
    """
    for parent_dir, child_dir in find_single_child_dirs(source_dir):
        stats.dirs_examined += 1
        stats.add_log(f"Processing: {parent_dir.name}", LogLevel.OPERATION)

        # Clean Apple system files before reorganization
        files_removed, dirs_removed = remove_apple_system_files(
            parent_dir, stats, verbosity
        )
        stats.files_removed += files_removed
        stats.dirs_removed += dirs_removed

        target_path = source_dir / child_dir.name

        # Check for path length issues (Windows)
        if is_path_too_long(target_path, stats):
            stats.add_log(f"Path too long for Windows: {target_path}", LogLevel.ERROR)
            stats.dirs_ignored += 1
            continue

        if target_path.exists() and target_path != child_dir:
            stats.add_log(f"Target exists: {target_path}", LogLevel.WARNING)
            if not no_confirm and not get_user_confirmation(
                "Overwrite target?", default=False, stats=stats
            ):
                stats.add_log("Skipped by user", LogLevel.INFO)
                stats.dirs_ignored += 1
                continue

            stats.add_log(f"Removing directory: '{target_path}'...", LogLevel.INFO)
            try:
                shutil.rmtree(target_path)
            except OSError as e:
                stats.add_log(f"Clear failed: {e}", LogLevel.ERROR)
                stats.dirs_ignored += 1
                continue

        stats.add_log(
            f"Moving directory: '{child_dir.name}' to parent...", LogLevel.INFO
        )
        try:
            shutil.move(str(child_dir), str(source_dir))
        except (OSError, shutil.Error) as e:
            stats.add_log(f"Failed to move directory: {e}", LogLevel.ERROR)
            stats.dirs_ignored += 1
            continue

        try:
            # Check if the parent is now empty
            if not any(parent_dir.iterdir()):
                parent_dir.rmdir()
                stats.dirs_reorganized += 1
                stats.add_log("Reorganization successful", LogLevel.SUCCESS)
            else:
                stats.add_log("Parent not empty after move", LogLevel.WARNING)
                stats.dirs_ignored += 1
        except OSError as e:
            stats.add_log(f"Failed to remove parent directory: {e}", LogLevel.ERROR)
            stats.dirs_ignored += 1


def get_user_confirmation(
    prompt: str, default: bool = False, stats: Optional[OperationStats] = None
) -> bool:
    """Get yes/no confirmation from user with customizable default.

    Args:
        prompt: Question to present to user
        default: Default response if user just hits enter

    Returns:
        True if user confirmed, False otherwise

    Examples:
        >>> get_user_confirmation("Continue?", default=True)
        Continue? [Y/n] y
        True
        >>> get_user_confirmation("Delete files?", default=False)
        Delete files? [y/N] n
        False
    """
    if not sys.stdin.isatty():
        if stats:
            stats.add_log(
                "No interactive terminal, using default response", LogLevel.WARNING
            )
        return default

    suffix = " [Y/n]" if default else " [y/N]"
    while True:
        try:
            response = input(prompt + suffix).strip().lower()
            if not response:
                return default
            if response in ("y", "yes"):
                return True
            if response in ("n", "no"):
                return False
            print("Please enter 'y' or 'n'")
        except (EOFError, KeyboardInterrupt):
            print()
            return default


def main() -> Literal[0, 1]:
    """Main entry point for the script.

    Handles argument parsing and coordinates all operations.

    Returns:
        0 on success, 1 on error
    """
    global MAX_ZIP_SIZE

    parser = argparse.ArgumentParser(
        description="Advanced ZIP extraction and directory reorganization tool",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "-d",
        "--directory",
        type=Path,
        help="Directory containing files to process",
    )
    parser.add_argument(
        "-c",
        "--clean-only",
        action="store_true",
        help="Only clean system files without extracting or reorganizing",
    )
    parser.add_argument(
        "-n",
        "--no-confirm",
        action="store_true",
        help="Skip all confirmation prompts",
    )
    parser.add_argument(
        "-v",
        "--verbosity",
        type=int,
        choices=[0, 1, 2],
        default=DEFAULT_VERBOSITY,
        help="Verbosity level (0=silent, 1=normal, 2=verbose)",
    )
    parser.add_argument(
        "--max-size",
        type=int,
        default=MAX_ZIP_SIZE,
        help=f"Maximum ZIP file size in bytes (default: {MAX_ZIP_SIZE})",
    )
    parser.add_argument(
        "--no-color",
        action="store_true",
        help="Disable colored output",
    )

    args = parser.parse_args()
    MAX_ZIP_SIZE = args.max_size

    try:
        args.directory = Path(args.directory).expanduser().resolve()
    except Exception as e:
        print(f"Error resolving directory path: {e}", file=sys.stderr)
        return 1

    stats = OperationStats()

    # Notify about optional dependencies
    if not HAS_COLORAMA and not args.no_color:
        stats.add_log(
            "Note: For colored output, install 'colorama' with: `pip install colorama`",
            LogLevel.INFO,
        )
    if not HAS_RICH:
        stats.add_log(
            "Note: For better output formatting, install 'rich' with: `pip install rich`",
            LogLevel.INFO,
        )
        if not HAS_TABULATE:
            stats.add_log(
                "Note: For better output formatting, install 'tabulate' with: `pip install tabulate`",
                LogLevel.INFO,
            )

    # Validate directory
    if not args.directory.exists():
        stats.add_log(f"Directory not found: {args.directory}", LogLevel.ERROR)
        stats.print_logs(verbosity=1)
        return 1

    if not args.directory.is_dir():
        stats.add_log(f"Path is not a directory: {args.directory}", LogLevel.ERROR)
        stats.print_logs(verbosity=1)
        return 1

    if not check_readable(args.directory, stats):
        stats.add_log(
            f"No read permission for directory: {args.directory}", LogLevel.ERROR
        )
        stats.print_logs(verbosity=1)
        return 1

    if not check_writable(args.directory, stats):
        stats.add_log(
            f"No write permission for directory: {args.directory}", LogLevel.ERROR
        )
        stats.print_logs(verbosity=1)
        return 1

    if is_network_path(args.directory, stats):
        stats.add_log("Network path detected - operations may be slower", LogLevel.INFO)

    # Acquire directory lock
    lock_fd = acquire_lock(args.directory)
    if lock_fd is None and not args.no_confirm:
        stats.add_log("Warning: Could not acquire directory lock", LogLevel.WARNING)
        if not get_user_confirmation(
            "Continue without lock?", default=False, stats=stats
        ):
            return 1

    try:
        # Execute requested operations
        if args.clean_only:
            stats.add_log(
                f"Starting clean-only mode in {args.directory}", LogLevel.INFO
            )
            files, dirs = remove_apple_system_files(
                args.directory, stats, args.verbosity
            )
            stats.files_removed = files
            stats.dirs_removed = dirs
        else:
            stats.add_log(
                f"Starting full processing in {args.directory}", LogLevel.INFO
            )
            extract_zip_files(args.directory, stats, args.no_confirm, args.verbosity)
            files, dirs = remove_apple_system_files(
                args.directory, stats, args.verbosity
            )
            stats.files_removed += files
            stats.dirs_removed += dirs
            reorganize_directories(
                args.directory, stats, args.no_confirm, args.verbosity
            )

        # Output results
        stats.print_logs(verbosity=args.verbosity)
        stats.print_summary(verbosity=args.verbosity)

        return 0 if stats.errors == 0 else 1

    except Exception as e:
        stats.add_log(f"Unexpected error: {e}", LogLevel.ERROR)
        if args.verbosity >= 1:
            import traceback

            stats.add_log(traceback.format_exc(), LogLevel.DEBUG)
        stats.print_logs(verbosity=args.verbosity)
        return 1

    finally:
        release_lock(lock_fd, stats)


if __name__ == "__main__":
    sys.exit(main())
