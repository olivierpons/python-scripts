#!/usr/bin/env python3
"""
File Content Cutter Script

This script removes content from the beginning of a file up to a specified
cutoff time in MM:SS format. It's useful for trimming log files, transcripts,
or any time-stamped text files.

Usage:
    python file_cutter.py <filename> <cutoff_time>

Example:
    python file_cutter.py transcript.txt 05:30
"""

import argparse
import logging
import os
import re
import shutil
import sys
import tempfile
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator, List, Optional, Tuple, Union

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


class FileCutterError(Exception):
    """Base exception class for file cutter operations."""
    pass


class TimeFormatError(FileCutterError):
    """Exception raised for invalid time format."""
    pass


class FileOperationError(FileCutterError):
    """Exception raised for file operation errors."""
    pass


class TimestampNotFoundError(FileCutterError):
    """Exception raised when cutoff timestamp is not found in file."""
    pass


class InsufficientPermissionsError(FileCutterError):
    """Exception raised for permission-related errors."""
    pass


class DiskSpaceError(FileCutterError):
    """Exception raised when insufficient disk space is available."""
    pass


@contextmanager
def safe_file_operation(file_path: Union[str, Path], operation: str) -> Iterator[None]:
    """Context manager for safe file operations with comprehensive error handling.

    Args:
        file_path: Path to the file being operated on
        operation: Description of the operation being performed

    Yields:
        None

    Raises:
        FileOperationError: For various file operation failures
        InsufficientPermissionsError: For permission-related errors
        DiskSpaceError: For disk space issues
    """
    file_path = Path(file_path)

    try:
        yield
    except PermissionError as e:
        raise InsufficientPermissionsError(
            f"Permission denied during {operation} on '{file_path}': {e}"
        ) from e
    except OSError as e:
        if e.errno == 28:  # No space left on device
            raise DiskSpaceError(
                f"Insufficient disk space during {operation} on '{file_path}'"
            ) from e
        elif e.errno == 2:  # No such file or directory
            raise FileOperationError(
                f"File not found during {operation}: '{file_path}'"
            ) from e
        elif e.errno == 13:  # Permission denied
            raise InsufficientPermissionsError(
                f"Access denied during {operation} on '{file_path}'"
            ) from e
        elif e.errno == 21:  # Is a directory
            raise FileOperationError(
                f"Expected file but found directory: '{file_path}'"
            ) from e
        elif e.errno == 26:  # Text file busy
            raise FileOperationError(
                f"File is currently in use: '{file_path}'"
            ) from e
        else:
            raise FileOperationError(
                f"OS error during {operation} on '{file_path}': {e}"
            ) from e
    except IOError as e:
        raise FileOperationError(
            f"I/O error during {operation} on '{file_path}': {e}"
        ) from e
    except UnicodeDecodeError as e:
        raise FileOperationError(
            f"Encoding error during {operation} on '{file_path}': {e}"
        ) from e
    except UnicodeEncodeError as e:
        raise FileOperationError(
            f"Encoding error during {operation} on '{file_path}': {e}"
        ) from e
    except MemoryError as e:
        raise FileOperationError(
            f"Insufficient memory during {operation} on '{file_path}': {e}"
        ) from e


def validate_file_access(file_path: Path, operation: str) -> None:
    """Validate file access permissions and existence.

    Args:
        file_path: Path to validate
        operation: Type of operation (read/write) for error messages

    Raises:
        FileOperationError: If file validation fails
        InsufficientPermissionsError: If permissions are insufficient
    """
    try:
        if not file_path.exists():
            raise FileOperationError(f"File does not exist: '{file_path}'")

        if not file_path.is_file():
            if file_path.is_dir():
                raise FileOperationError(f"Path is a directory, not a file: '{file_path}'")
            elif file_path.is_symlink():
                raise FileOperationError(f"Path is a symbolic link: '{file_path}'")
            else:
                raise FileOperationError(f"Path is not a regular file: '{file_path}'")

        if operation == "read" and not os.access(file_path, os.R_OK):
            raise InsufficientPermissionsError(f"No read permission for file: '{file_path}'")

        if operation == "write" and not os.access(file_path, os.W_OK):
            raise InsufficientPermissionsError(f"No write permission for file: '{file_path}'")

        # Check if file is empty
        if file_path.stat().st_size == 0:
            raise FileOperationError(f"File is empty: '{file_path}'")

    except OSError as e:
        raise FileOperationError(f"Error accessing file '{file_path}': {e}") from e


def check_disk_space(file_path: Path, required_bytes: int) -> None:
    """Check if sufficient disk space is available.

    Args:
        file_path: Path where file will be written
        required_bytes: Minimum bytes required

    Raises:
        DiskSpaceError: If insufficient disk space is available
    """
    try:
        stat = shutil.disk_usage(file_path.parent)
        available_bytes = stat.free

        # Add 10% buffer for safety
        required_with_buffer = int(required_bytes * 1.1)

        if available_bytes < required_with_buffer:
            raise DiskSpaceError(
                f"Insufficient disk space. Required: {required_with_buffer} bytes, "
                f"Available: {available_bytes} bytes"
            )
    except OSError as e:
        logger.warning(f"Could not check disk space: {e}")


def parse_time_format(time_str: str) -> Tuple[int, int]:
    """Parse time string in MM:SS format to minutes and seconds.

    Args:
        time_str: Time string in format MM:SS (e.g., "05:30")

    Returns:
        Tuple containing (minutes, seconds)

    Raises:
        TimeFormatError: If time format is invalid

    Examples:
        >>> parse_time_format("05:30")
        (5, 30)
        >>> parse_time_format("12:45")
        (12, 45)
    """
    if not isinstance(time_str, str):
        raise TimeFormatError(f"Time must be a string, got {type(time_str).__name__}")

    time_str = time_str.strip()

    if not time_str:
        raise TimeFormatError("Time string cannot be empty")

    # Check for valid MM:SS format
    pattern = r'^(\d{1,3}):(\d{2})$'
    match = re.match(pattern, time_str)

    if not match:
        raise TimeFormatError(
            f"Invalid time format: '{time_str}'. Expected MM:SS format (e.g., '05:30')"
        )

    try:
        minutes = int(match.group(1))
        seconds = int(match.group(2))
    except (ValueError, OverflowError) as e:
        raise TimeFormatError(f"Invalid numeric values in time string '{time_str}': {e}") from e

    # Validate ranges
    if minutes < 0:
        raise TimeFormatError(f"Minutes cannot be negative: {minutes}")

    if minutes > 999:
        raise TimeFormatError(f"Minutes too large (max 999): {minutes}")

    if seconds < 0 or seconds >= 60:
        raise TimeFormatError(f"Seconds must be between 0-59, got: {seconds}")

    return minutes, seconds


def detect_file_encoding(file_path: Path) -> str:
    """Detect file encoding with fallback options.

    Args:
        file_path: Path to the file

    Returns:
        Detected encoding string

    Raises:
        FileOperationError: If encoding cannot be determined
    """
    encodings_to_try = ['utf-8', 'utf-8-sig', 'latin1', 'cp1252', 'iso-8859-1']

    for encoding in encodings_to_try:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                # Try to read first 1KB to test encoding
                f.read(1024)
                return encoding
        except (UnicodeDecodeError, UnicodeError):
            continue
        except Exception as e:
            logger.warning(f"Error testing encoding {encoding}: {e}")
            continue

    raise FileOperationError(
        f"Could not determine encoding for file '{file_path}'. "
        f"Tried encodings: {', '.join(encodings_to_try)}"
    )


def safe_read_file(file_path: Path) -> Tuple[List[str], str]:
    """Safely read file content with encoding detection and error handling.

    Args:
        file_path: Path to the file to read

    Returns:
        Tuple of (lines_list, detected_encoding)

    Raises:
        FileOperationError: For various file reading errors
        MemoryError: If file is too large to fit in memory
    """
    validate_file_access(file_path, "read")

    # Check file size to prevent memory issues
    try:
        file_size = file_path.stat().st_size
        max_size = 1024 * 1024 * 1024  # 1GB limit

        if file_size > max_size:
            raise FileOperationError(
                f"File too large to process: {file_size} bytes (max {max_size} bytes)"
            )
    except OSError as e:
        raise FileOperationError(f"Could not get file size: {e}") from e

    encoding = detect_file_encoding(file_path)

    with safe_file_operation(file_path, "reading"):
        try:
            with open(file_path, 'r', encoding=encoding, newline=None) as file:
                lines = file.readlines()
        except MemoryError as e:
            raise MemoryError(f"File too large to fit in memory: '{file_path}'") from e

    if not lines:
        raise FileOperationError(f"File is empty or contains no readable content: '{file_path}'")

    logger.info(f"Successfully read {len(lines)} lines from '{file_path}' using {encoding} encoding")
    return lines, encoding


def find_cutoff_line(lines: List[str], cutoff_minutes: int, cutoff_seconds: int) -> Optional[int]:
    """Find the line index where the cutoff time is reached or exceeded.

    Args:
        lines: List of lines from the file
        cutoff_minutes: Target minutes for cutoff
        cutoff_seconds: Target seconds for cutoff

    Returns:
        Line index where cutoff occurs, or None if not found

    Note:
        This function looks for timestamps in various common formats:
        - MM:SS (e.g., "05:30")
        - [MM:SS] (e.g., "[05:30]")
        - HH:MM:SS (e.g., "01:05:30")
        - MM:SS.mmm (e.g., "05:30.123")
    """
    if not lines:
        return None

    if not isinstance(lines, list):
        raise TypeError("Lines must be a list")

    cutoff_total_seconds = cutoff_minutes * 60 + cutoff_seconds

    # Enhanced timestamp patterns with more comprehensive matching
    patterns = [
        r'(?:^|\s)(\d{1,2}):(\d{2})(?:\.(\d{1,3}))?(?:\s|$)',  # MM:SS or MM:SS.mmm
        r'\[(\d{1,2}):(\d{2})(?:\.(\d{1,3}))?\]',  # [MM:SS] or [MM:SS.mmm]
        r'(?:^|\s)(\d{1,2}):(\d{1,2}):(\d{2})(?:\.(\d{1,3}))?(?:\s|$)',  # HH:MM:SS or HH:MM:SS.mmm
        r'(\d{1,2}):(\d{2})\s*-\s*',  # MM:SS followed by dash (common in transcripts)
        r'(?:Time|Timestamp):\s*(\d{1,2}):(\d{2})',  # "Time: MM:SS" format
    ]

    found_any_timestamp = False

    try:
        for line_idx, line in enumerate(lines):
            if not isinstance(line, str):
                continue

            for pattern in patterns:
                try:
                    matches = re.findall(pattern, line, re.IGNORECASE)

                    for match in matches:
                        if not match:
                            continue

                        found_any_timestamp = True

                        try:
                            # Handle different match group structures
                            if len(match) >= 4 and match[2]:  # HH:MM:SS format
                                hours = int(match[0])
                                minutes = int(match[1])
                                seconds = int(match[2])

                                # Validate ranges
                                if hours > 23 or minutes > 59 or seconds > 59:
                                    continue

                                total_seconds = hours * 3600 + minutes * 60 + seconds
                            else:  # MM:SS format
                                minutes = int(match[0])
                                seconds = int(match[1])

                                # Validate ranges
                                if minutes < 0 or minutes > 999 or seconds < 0 or seconds > 59:
                                    continue

                                total_seconds = minutes * 60 + seconds

                            if total_seconds >= cutoff_total_seconds:
                                logger.info(
                                    f"Found cutoff at line {line_idx + 1}: "
                                    f"{total_seconds // 60:02d}:{total_seconds % 60:02d}"
                                )
                                return line_idx

                        except (ValueError, IndexError, OverflowError) as e:
                            logger.debug(f"Error parsing timestamp in line {line_idx + 1}: {e}")
                            continue

                except re.error as e:
                    logger.warning(f"Regex error with pattern '{pattern}': {e}")
                    continue
                except Exception as e:
                    logger.debug(f"Unexpected error processing line {line_idx + 1}: {e}")
                    continue

    except Exception as e:
        raise FileOperationError(f"Error while searching for timestamps: {e}") from e

    if not found_any_timestamp:
        logger.warning("No timestamps found in file with any recognized format")

    return None


def create_backup(file_path: Path) -> Path:
    """Create a backup of the original file.

    Args:
        file_path: Path to the file to backup

    Returns:
        Path to the backup file

    Raises:
        FileOperationError: If backup creation fails
        DiskSpaceError: If insufficient disk space
    """
    backup_path = file_path.with_suffix(file_path.suffix + '.backup')
    counter = 1

    # Find unique backup name
    while backup_path.exists():
        backup_path = file_path.with_suffix(f'{file_path.suffix}.backup.{counter}')
        counter += 1
        if counter > 1000:  # Prevent infinite loop
            raise FileOperationError("Could not create unique backup filename")

    try:
        file_size = file_path.stat().st_size
        check_disk_space(backup_path, file_size)

        with safe_file_operation(backup_path, "creating backup"):
            shutil.copy2(file_path, backup_path)

        logger.info(f"Backup created: '{backup_path}'")
        return backup_path

    except shutil.Error as e:
        raise FileOperationError(f"Failed to create backup: {e}") from e


def atomic_write_file(file_path: Path, content: List[str], encoding: str) -> None:
    """Atomically write content to file using temporary file.

    Args:
        file_path: Target file path
        content: Lines to write
        encoding: Encoding to use

    Raises:
        FileOperationError: If write operation fails
        DiskSpaceError: If insufficient disk space
    """
    if not content:
        raise FileOperationError("Cannot write empty content")

    # Estimate content size
    estimated_size = sum(len(line.encode(encoding, errors='replace')) for line in content)
    check_disk_space(file_path, estimated_size)

    # Create temporary file in same directory for atomic operation
    temp_fd = None
    temp_path = None

    try:
        temp_fd, temp_path = tempfile.mkstemp(
            dir=file_path.parent,
            prefix=f'.{file_path.name}.tmp',
            suffix='.tmp'
        )
        temp_path = Path(temp_path)

        with safe_file_operation(temp_path, "writing temporary file"):
            with open(temp_fd, 'w', encoding=encoding, newline='') as temp_file:
                temp_file.writelines(content)
            temp_fd = None  # File is closed

        # Atomic move
        with safe_file_operation(file_path, "atomic file replacement"):
            if sys.platform == "win32":
                # Windows doesn't support atomic replace if target exists
                if file_path.exists():
                    file_path.unlink()
            temp_path.replace(file_path)

        logger.info(f"Successfully wrote {len(content)} lines to '{file_path}'")

    except Exception as e:
        # Cleanup temporary file
        if temp_fd is not None:
            try:
                os.close(temp_fd)
            except OSError:
                pass

        if temp_path and temp_path.exists():
            try:
                temp_path.unlink()
            except OSError as cleanup_error:
                logger.warning(f"Could not cleanup temporary file '{temp_path}': {cleanup_error}")

        raise FileOperationError(f"Failed to write file '{file_path}': {e}") from e


def cut_file_content(filename: str, cutoff_time: str, output_filename: Optional[str] = None) -> bool:
    """Cut file content from beginning up to the specified cutoff time.

    Args:
        filename: Path to the input file
        cutoff_time: Cutoff time in MM:SS format
        output_filename: Optional output filename. If None, overwrites input file

    Returns:
        True if operation was successful, False otherwise

    Raises:
        TimeFormatError: If cutoff time format is invalid
        FileOperationError: For file operation errors
        TimestampNotFoundError: If cutoff timestamp not found
        InsufficientPermissionsError: If file permissions are insufficient
        DiskSpaceError: If insufficient disk space
    """
    try:
        input_path = Path(filename).resolve()

        # Parse cutoff time with comprehensive error handling
        try:
            cutoff_minutes, cutoff_seconds = parse_time_format(cutoff_time)
        except TimeFormatError:
            raise
        except Exception as e:
            raise TimeFormatError(f"Unexpected error parsing time '{cutoff_time}': {e}") from e

        # Read file content with encoding detection
        try:
            lines, detected_encoding = safe_read_file(input_path)
        except (FileOperationError, MemoryError):
            raise
        except Exception as e:
            raise FileOperationError(f"Unexpected error reading file '{filename}': {e}") from e

        # Find cutoff line
        try:
            cutoff_line_idx = find_cutoff_line(lines, cutoff_minutes, cutoff_seconds)
        except Exception as e:
            raise FileOperationError(f"Error searching for timestamps: {e}") from e

        if cutoff_line_idx is None:
            raise TimestampNotFoundError(
                f"Cutoff time {cutoff_time} not found in file '{filename}'. "
                f"Make sure the file contains timestamps in MM:SS, [MM:SS], or HH:MM:SS format."
            )

        if cutoff_line_idx == 0:
            logger.warning(f"Cutoff time {cutoff_time} found at first line - no content will be removed")
            return False

        # Keep content from cutoff line onwards
        remaining_lines = lines[cutoff_line_idx:]

        if not remaining_lines:
            logger.warning("No content remains after cutoff - output would be empty")
            return False

        # Determine output file
        output_path = Path(output_filename).resolve() if output_filename else input_path

        # Validate output path
        if output_filename:
            # Check if output directory exists and is writable
            if not output_path.parent.exists():
                raise FileOperationError(f"Output directory does not exist: '{output_path.parent}'")

            if not os.access(output_path.parent, os.W_OK):
                raise InsufficientPermissionsError(
                    f"No write permission for output directory: '{output_path.parent}'"
                )
        else:
            # Validate write permission for input file
            validate_file_access(input_path, "write")

        # Write the cut content atomically
        try:
            atomic_write_file(output_path, remaining_lines, detected_encoding)
        except (FileOperationError, DiskSpaceError):
            raise
        except Exception as e:
            raise FileOperationError(f"Unexpected error writing output file: {e}") from e

        # Report results
        lines_removed = cutoff_line_idx
        lines_remaining = len(remaining_lines)

        logger.info(f"File cutting completed successfully:")
        logger.info(f"  Input file: '{filename}'")
        logger.info(f"  Output file: '{output_path}'")
        logger.info(f"  Cutoff time: {cutoff_time}")
        logger.info(f"  Lines removed: {lines_removed}")
        logger.info(f"  Lines remaining: {lines_remaining}")
        logger.info(f"  Encoding used: {detected_encoding}")

        return True

    except (TimeFormatError, FileOperationError, TimestampNotFoundError,
            InsufficientPermissionsError, DiskSpaceError):
        raise
    except KeyboardInterrupt:
        raise
    except Exception as e:
        raise FileOperationError(f"Unexpected error during file cutting: {e}") from e


def show_complete_help() -> None:
    """Display comprehensive help with examples and explanations."""
    help_text = """
FILE CONTENT CUTTER - Complete Usage Guide
==========================================

WHAT IT DOES:
This script removes content from the beginning of a file up to a specified cutoff time.
The cutoff_time parameter specifies WHERE to start keeping content.
Everything BEFORE this timestamp will be REMOVED from the file.
Everything AT or AFTER this timestamp will be KEPT.

USAGE:
    python file_cutter.py <filename> <cutoff_time> [options]

ARGUMENTS:
    filename      - Path to the input file to process
    cutoff_time   - Time in MM:SS format where to start keeping content
                   (e.g., "05:30" means keep everything from 5:30 onwards)

OPTIONS:
    -o, --output FILE    - Save result to different file (default: overwrite input)
    --backup            - Create backup before modifying file
    --dry-run           - Preview changes without modifying files
    -v, --verbose       - Show detailed logging information
    --force             - Force operation even with warnings

CUTOFF_TIME EXPLANATION:
========================
The cutoff_time is the timestamp WHERE you want to START keeping content.

Example with cutoff_time "05:30":
  Original file content:
    00:15 This line will be REMOVED
    02:45 This line will be REMOVED
    04:20 This line will be REMOVED
    05:30 This line will be KEPT ← cutoff point
    08:20 This line will be KEPT
    12:00 This line will be KEPT

  After cutting:
    05:30 This line will be KEPT
    08:20 This line will be KEPT
    12:00 This line will be KEPT

SUPPORTED TIMESTAMP FORMATS:
============================
Your file can contain timestamps in any of these formats:
  - MM:SS           (e.g., "05:30")
  - [MM:SS]         (e.g., "[05:30]")
  - HH:MM:SS        (e.g., "01:05:30")
  - MM:SS.mmm       (e.g., "05:30.123")
  - Time: MM:SS     (e.g., "Time: 05:30")
  - MM:SS -         (e.g., "05:30 - Some text")

USAGE EXAMPLES:
===============
Basic usage:
    python file_cutter.py transcript.txt 05:30
    → Removes everything before 5:30 from transcript.txt

Save to different file:
    python file_cutter.py log.txt 12:45 -o trimmed_log.txt
    → Removes everything before 12:45, saves result to trimmed_log.txt

Create backup first:
    python file_cutter.py data.txt 02:15 --backup
    → Creates data.txt.backup, then removes everything before 2:15

Preview without changes:
    python file_cutter.py file.txt 08:30 --dry-run
    → Shows what would be removed without actually changing the file

Verbose output:
    python file_cutter.py file.txt 03:45 --verbose
    → Shows detailed information during processing

COMMON USE CASES:
=================
• Trim audio/video transcripts from a specific time
• Remove early entries from timestamped log files  
• Cut meeting notes to start from a particular time
• Process time-coded data files

TROUBLESHOOTING:
================
If you get "timestamp not found" errors:
• Check that your file contains timestamps in supported formats
• Verify the cutoff_time format is MM:SS (e.g., "05:30")
• Use --dry-run to see what timestamps were detected
• Use --verbose for detailed processing information

For permission errors:
• Check file read/write permissions
• Ensure output directory exists and is writable
• Try running with --backup to preserve original

"""
    print(help_text)


def main() -> int:
    """Main function to handle command line arguments and execute file cutting.

    Returns:
        Exit code (0 for success, 1 for error, 2 for user interruption)
    """
    parser = argparse.ArgumentParser(
        description="Remove content from beginning of file up to specified cutoff time",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        add_help=False  # We'll handle help ourselves
    )

    parser.add_argument(
        'filename',
        nargs='?',  # Make optional to handle help cases
        type=str,
        help='Input filename to process'
    )

    parser.add_argument(
        'cutoff_time',
        nargs='?',  # Make optional to handle help cases
        type=str,
        help='Cutoff time in MM:SS format (e.g., 05:30)'
    )

    parser.add_argument(
        '-h', '--help',
        action='store_true',
        help='Show complete help with examples'
    )

    parser.add_argument(
        '-o', '--output',
        type=str,
        default=None,
        help='Output filename (default: overwrite input file)'
    )

    parser.add_argument(
        '--backup',
        action='store_true',
        help='Create backup of original file before cutting'
    )

    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be cut without actually modifying files'
    )

    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )

    parser.add_argument(
        '--force',
        action='store_true',
        help='Force operation even with warnings'
    )

    try:
        args = parser.parse_args()

        # Handle help or insufficient arguments
        if args.help or not args.filename or not args.cutoff_time:
            show_complete_help()
            return 1

        # Configure logging level
        if args.verbose:
            logging.getLogger().setLevel(logging.DEBUG)

        # Validate inputs with simple error messages
        if not args.filename.strip():
            logger.error("Filename cannot be empty")
            return 1

        if not args.cutoff_time.strip():
            logger.error("Cutoff time cannot be empty")
            return 1

        input_path = Path(args.filename.strip())

        # Pre-validation checks
        try:
            if not input_path.exists():
                logger.error(f"File '{args.filename}' not found")
                return 1

            validate_file_access(input_path, "read")

            if not args.output:
                validate_file_access(input_path, "write")

        except (FileOperationError, InsufficientPermissionsError) as e:
            logger.error(str(e))
            return 1

        # Validate cutoff time format early
        try:
            cutoff_minutes, cutoff_seconds = parse_time_format(args.cutoff_time.strip())
            logger.debug(f"Parsed cutoff time: {cutoff_minutes:02d}:{cutoff_seconds:02d}")
        except TimeFormatError as e:
            logger.error(str(e))
            return 1

        # Create backup if requested (before dry run to test permissions)
        backup_path = None
        if args.backup and not args.dry_run:
            try:
                backup_path = create_backup(input_path)
            except (FileOperationError, DiskSpaceError, InsufficientPermissionsError) as e:
                logger.error(f"Failed to create backup: {e}")
                return 1

        # Dry run mode
        if args.dry_run:
            try:
                logger.info("Performing dry run...")
                lines, encoding = safe_read_file(input_path)
                cutoff_line_idx = find_cutoff_line(lines, cutoff_minutes, cutoff_seconds)

                if cutoff_line_idx is None:
                    logger.warning(f"Dry run: Cutoff time {args.cutoff_time} not found in file")
                    logger.info("Dry run completed - no changes would be made")
                else:
                    logger.info(f"Dry run results:")
                    logger.info(f"  Would remove {cutoff_line_idx} lines from beginning")
                    logger.info(f"  Would keep {len(lines) - cutoff_line_idx} lines")
                    logger.info(f"  File encoding: {encoding}")
                    if cutoff_line_idx > 0:
                        logger.info(f"  First removed line: {repr(lines[0][:100])}")
                        logger.info(f"  First kept line: {repr(lines[cutoff_line_idx][:100])}")

                return 0

            except (FileOperationError, TimeFormatError, MemoryError) as e:
                logger.error(f"Dry run failed: {e}")
                return 1

        # Execute the cut operation
        try:
            success = cut_file_content(args.filename.strip(), args.cutoff_time.strip(), args.output)

            if success:
                logger.info("Operation completed successfully")
                return 0
            else:
                logger.warning("Operation completed with warnings")
                return 0

        except TimestampNotFoundError as e:
            logger.error(str(e))
            logger.info("Use --help for examples and supported timestamp formats")
            return 1
        except (TimeFormatError, FileOperationError, InsufficientPermissionsError, DiskSpaceError) as e:
            logger.error(str(e))

            # Cleanup backup if operation failed
            if backup_path and backup_path.exists():
                try:
                    backup_path.unlink()
                    logger.info(f"Cleaned up backup file: {backup_path}")
                except OSError as cleanup_error:
                    logger.warning(f"Could not cleanup backup file: {cleanup_error}")

            return 1

    except KeyboardInterrupt:
        logger.info("Operation cancelled by user")
        return 2
    except SystemExit:
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        logger.debug("Full traceback:", exc_info=True)
        return 1


if __name__ == '__main__':
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        logger.info("Program interrupted by user")
        sys.exit(2)
    except SystemExit:
        raise
    except Exception as e:
        logger.critical(f"Critical error: {e}")
        sys.exit(1)