#!/usr/bin/env python3
"""
Advanced ZIP Extraction and Directory Reorganization Tool.

This script performs three main operations with comprehensive logging and statistics:
1. Extracts all ZIP files in a directory into corresponding subdirectories
2. Removes Apple system files (.DS_Store, .__MACOSX folders, etc.)
3. Reorganizes directories by moving single-child directories up one level

Features:
- Detailed progress logging with verbosity levels (0=silent, 1=normal, 2=verbose)
- Beautiful tabular output (with fallback to basic formatting)
- Comprehensive statistics collection
- Modern Python typing and dataclasses
- Configurable confirmation prompts

Example usage:
    $ python unzip_files_then_clean.py /path/to/directory
    $ python unzip_files_then_clean.py /path/to/directory --clean-only
    $ python unzip_files_then_clean.py /path/to/directory --no-confirm -v
    $ python unzip_files_then_clean.py /path/to/directory -vv  # full verbose (default)

Detailed Examples:
    1. Basic extraction and reorganization:
       $ python unzip_files_then_clean.py ~/Downloads/archive
       # Extracts all ZIP files in ~/Downloads/archive
       # Removes Apple system files
       # Reorganizes single-child directories

    2. Clean only mode (skips extraction and reorganization):
       $ python unzip_files_then_clean.py ~/Projects --clean-only
       # Only removes Apple system files from ~/Projects and subdirectories
       # Useful for cleaning up directories without modifying structure

    3. No confirmation mode:
       $ python unzip_files_then_clean.py ~/Documents -v --no-confirm
       # Processes all files without asking for confirmation
       # Shows normal verbosity output (errors and warnings)
       # Useful for scripting and batch processing

    4. Different verbosity levels:
       $ python unzip_files_then_clean.py ~/Music -v     # Normal verbosity (errors and warnings)
       $ python unzip_files_then_clean.py ~/Music -vv    # Full verbosity (all operations)
       $ python unzip_files_then_clean.py ~/Music        # Same as -vv (default)
       $ python unzip_files_then_clean.py ~/Music -v 0   # Silent mode (no output)
"""

import argparse
import re
import shutil
import sys
import zipfile
from dataclasses import dataclass, field
from enum import Enum, auto
from pathlib import Path
from typing import Generator, List, Literal, Optional, Set, Tuple, Pattern

# Try to import tabulate, with fallback to basic printing if not available
try:
    from tabulate import tabulate

    HAS_TABULATE = True
except ImportError:
    HAS_TABULATE = False

    def tabulate(data, headers=None, *args, **kwargs):
        """Simple tabulate fallback when the package is not available."""
        if not data:
            return ""

        # Calculate column widths
        if headers:
            all_rows = [headers] + data
        else:
            all_rows = data

        col_widths = [
            max(len(str(row[i])) for row in all_rows) for i in range(len(all_rows[0]))
        ]

        # Build horizontal divider
        divider = "+" + "+".join("-" * (w + 2) for w in col_widths) + "+"

        # Build the table
        table = [divider]

        # Add headers if provided
        if headers:
            header_row = (
                "| "
                + " | ".join(
                    f"{str(header):<{width}}"
                    for header, width in zip(headers, col_widths)
                )
                + " |"
            )
            table.extend([header_row, divider])

        # Add data rows
        for row in data:
            row_str = (
                "| "
                + " | ".join(
                    f"{str(item):<{width}}" for item, width in zip(row, col_widths)
                )
                + " |"
            )
            table.append(row_str)

        table.append(divider)
        return "\n".join(table)


class LogLevel(Enum):
    """Enum for different log levels."""

    INFO = auto()
    WARNING = auto()
    ERROR = auto()
    SUCCESS = auto()
    OPERATION = auto()


@dataclass
class LogEntry:
    """Class representing a single log entry."""

    message: str
    level: LogLevel = LogLevel.INFO
    timestamp: Optional[float] = field(default=None, repr=False)
    path: Optional[Path] = None  # Added path field to track file operations


@dataclass
class OperationStats:
    """Statistics collector for all operations.

    Examples:
        >>> stats = OperationStats()
        >>> stats.add_log("Processing started", LogLevel.INFO)
        >>> stats.total_zips += 1
        >>> stats.successful_extractions += 1
        >>> output = stats.get_output(verbosity=2)  # Get complete output
        >>> print(output)  # Print the summary and logs
    """

    # Operation counters
    total_zips: int = 0
    successful_extractions: int = 0
    failed_extractions: int = 0
    files_removed: int = 0
    dirs_removed: int = 0
    dirs_examined: int = 0
    dirs_reorganized: int = 0
    dirs_ignored: int = 0

    # Detailed logging
    logs: List[LogEntry] = field(default_factory=list)

    # Store removed files for verbose output
    removed_files: List[Path] = field(default_factory=list)
    removed_dirs: List[Path] = field(default_factory=list)

    def add_log(
        self, message: str, level: LogLevel = LogLevel.INFO, path: Optional[Path] = None
    ) -> None:
        """Add a new log entry.

        Args:
            message: Log message to record
            level: Severity level of the log entry
            path: Path object associated with this log entry

        Examples:
            >>> stats = OperationStats()
            >>> stats.add_log("Extracted file.zip", LogLevel.SUCCESS)
            >>> f_path = Path("/tmp/file.txt")
            >>> stats.add_log(f"Failed to process {f_path}", LogLevel.ERROR, f_path)
        """
        self.logs.append(LogEntry(message, level, path=path))

        # Track removed files and directories for verbose output
        if level == LogLevel.INFO and path:
            if "Removed Apple file" in message:
                self.removed_files.append(path)
            elif "Removed Apple directory" in message:
                self.removed_dirs.append(path)

    def get_output(self, verbosity: int = 2) -> str:
        """Get all output as a single string with appropriate verbosity filtering.

        Args:
            verbosity: 0=silent, 1=normal (errors+warnings+summary), 2=verbose (all)

        Returns:
            Formatted string containing all output

        Examples:
            >>> stats = OperationStats()
            >>> stats.add_log("Processing complete", LogLevel.SUCCESS)
            >>> result_normal = stats.get_output(verbosity=1)  # Normal verbosity
            >>> print(result_normal)
            >>> result_verbose = stats.get_output(verbosity=2)  # Full verbosity
            >>> print(result_verbose)
        """
        if verbosity == 0:
            return ""

        output = []

        # Add summary
        summary = self._get_summary()
        output.append(summary)

        # Add logs if verbosity is full
        if verbosity >= 1:
            logs = self._get_logs(verbosity)
            if logs:
                output.append(logs)

        # Add removed files list in verbose mode
        if verbosity >= 2 and (self.removed_files or self.removed_dirs):
            output.append(self._get_removed_files_list())

        return "\n".join(output)

    def _get_summary(self) -> str:
        """Generate summary tables for operations."""
        # Prepare summary data
        summary_data = {
            "ZIP Processing": [
                ["Files Processed", self.total_zips],
                ["Successful", self.successful_extractions],
                ["Failed", self.failed_extractions],
                [
                    "Success Rate",
                    (
                        f"{self.successful_extractions / self.total_zips * 100:.1f}%"
                        if self.total_zips
                        else "N/A"
                    ),
                ],
            ],
            "Cleaning": [
                ["Files Removed", self.files_removed],
                ["Directories Removed", self.dirs_removed],
                ["Total Cleaned", self.files_removed + self.dirs_removed],
            ],
            "Reorganization": [
                ["Examined", self.dirs_examined],
                ["Reorganized", self.dirs_reorganized],
                ["Ignored", self.dirs_ignored],
                [
                    "Reorg Rate",
                    (
                        f"{self.dirs_reorganized / self.dirs_examined * 100:.1f}%"
                        if self.dirs_examined
                        else "N/A"
                    ),
                ],
            ],
        }

        # Build summary output
        output = ["=" * 80, "PROCESSING SUMMARY".center(80), "=" * 80]

        # Print each section
        for section, data in summary_data.items():
            output.append(f"\n{section.upper():^80}")
            output.append(tabulate(data, tablefmt="fancy"))

        # Print error summary if any
        error_logs = [log for log in self.logs if log.level == LogLevel.ERROR]
        if error_logs:
            output.append("\n" + "!" * 80)
            output.append(f"  {len(error_logs)} ERRORS ENCOUNTERED  ".center(80, "!"))
            output.append("!" * 80)

        return "\n".join(output)

    def _get_logs(self, verbosity: int = 2) -> str:
        """Generate log output with appropriate verbosity filtering."""
        if not self.logs:
            return ""

        output = ["\n" + "-" * 80, "DETAILED OPERATION LOGS".center(80), "-" * 80]

        for log in self.logs:
            if verbosity == 1 and log.level not in (LogLevel.ERROR, LogLevel.WARNING):
                continue

            prefix = {
                LogLevel.INFO: "[INFO]",
                LogLevel.WARNING: "[WARNING]",
                LogLevel.ERROR: "[ERROR]",
                LogLevel.SUCCESS: "[SUCCESS]",
                LogLevel.OPERATION: "→",
            }.get(log.level, "")

            output.append(f"{prefix} {log.message}")

        return "\n".join(output)

    def _get_removed_files_list(self) -> str:
        """Generate a list of removed files and directories (verbose mode only)."""
        output = []

        if self.removed_files or self.removed_dirs:
            output.append("\n" + "-" * 80)
            output.append("REMOVED ITEMS (VERBOSE MODE)".center(80))
            output.append("-" * 80)

            if self.removed_files:
                output.append("\nRemoved Files:")
                for file_path in sorted(self.removed_files):
                    output.append(f"  - {file_path}")

            if self.removed_dirs:
                output.append("\nRemoved Directories:")
                for dir_path in sorted(self.removed_dirs):
                    output.append(f"  - {dir_path}")

        return "\n".join(output)


# Constants for Apple system files to remove
APPLE_SYSTEM_FILES: Set[str | Pattern] = {
    ".DS_Store",
    "._.DS_Store",
    ".AppleDouble",
    ".LSOverride",
    # More specific pattern for AppleDouble files
    re.compile(r"^\._.*$"),  # Only files starting with ._
}

# Apple system directories
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
        filename: Name of the file to check

    Returns:
        True if the file is an Apple system file, False otherwise

    Examples:
        >>> is_apple_system_file(".DS_Store")
        True
        >>> is_apple_system_file("._config.json")
        True
        >>> is_apple_system_file("document.txt")
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


def remove_apple_system_files(
    directory: Path, stats: OperationStats
) -> Tuple[int, int]:
    """
    Recursively remove Apple system files and directories.

    Args:
        directory: Path to directory to clean
        stats: OperationStats for logging and stats

    Returns:
        Tuple of (files_removed, dirs_removed)

    Examples:
        >>> operation_stats = OperationStats()
        >>> files, dirs = remove_apple_system_files(
        >>>     Path("~/Downloads"), operation_stats
        >>> )
        >>> print(f"Removed {files} files and {dirs} directories")
    """
    files_removed, dirs_removed = 0, 0

    for path in sorted(
        directory.glob("**/*"), key=lambda p: len(p.parts), reverse=True
    ):
        if not path.exists():
            continue

        # Handle directories
        if path.is_dir() and path.name in APPLE_SYSTEM_DIRS:
            try:
                shutil.rmtree(path)
                dirs_removed += 1
                stats.add_log(f"Removed Apple directory: {path}", LogLevel.INFO, path)
            except OSError as e:
                stats.add_log(f"Error removing {path}: {e}", LogLevel.ERROR, path)

        # Handle files - ONLY ACTUAL APPLE FILES
        elif path.is_file() and is_apple_system_file(path.name):
            try:
                path.unlink()
                files_removed += 1
                stats.add_log(f"Removed Apple file: {path}", LogLevel.INFO, path)
            except OSError as e:
                stats.add_log(f"Error removing {path}: {e}", LogLevel.ERROR, path)

    return files_removed, dirs_removed


def extract_zip_files(
    source_dir: Path, stats: OperationStats, no_confirm: bool = False
) -> None:
    """
    Extract all ZIP files in directory to corresponding subdirectories.

    Args:
        source_dir: Directory containing ZIP files
        stats: OperationStats for logging and stats
        no_confirm: Skip confirmation prompts if True

    Examples:
        >>> operation_stats = OperationStats()
        >>> extract_zip_files(Path("~/Downloads"), operation_stats)
        >>> extract_zip_files(Path("~/Downloads"), operation_stats, no_confirm=True)
    """
    for zip_file in source_dir.glob("*.zip"):
        stats.total_zips += 1
        dest_dir = source_dir / zip_file.stem

        stats.add_log(f"Processing ZIP: {zip_file.name}", LogLevel.OPERATION)
        stats.add_log(f"Creating directory: {dest_dir}", LogLevel.INFO)

        # Handle existing directory
        if dest_dir.exists():
            stats.add_log("Destination directory exists", LogLevel.WARNING)

            if not no_confirm and not get_user_confirmation("Overwrite contents?"):
                stats.add_log("Skipped by user", LogLevel.INFO)
                stats.failed_extractions += 1
                continue

            stats.add_log("Clearing existing directory...", LogLevel.OPERATION)
            try:
                shutil.rmtree(dest_dir)
            except OSError as e:
                stats.add_log(f"Clear failed: {e}", LogLevel.ERROR)
                stats.failed_extractions += 1
                continue

        # Create destination and extract
        try:
            dest_dir.mkdir(exist_ok=True)

            with zipfile.ZipFile(zip_file, "r") as zip_ref:
                zip_ref.extractall(dest_dir)

            # Clean extracted files
            files_removed, dirs_removed = remove_apple_system_files(dest_dir, stats)
            stats.files_removed += files_removed
            stats.dirs_removed += dirs_removed

            # Verify and remove original
            if any(dest_dir.rglob("*")):
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

        except (zipfile.BadZipFile, OSError) as e:
            stats.add_log(f"Extraction failed: {e}", LogLevel.ERROR)
            stats.failed_extractions += 1


def find_single_child_dirs(root_dir: Path) -> Generator[Tuple[Path, Path], None, None]:
    """Find directories with exactly one subdirectory and no other items.

    Args:
        root_dir: Base directory to scan

    Yields:
        Tuples of (parent_directory, child_directory)

    Examples:
        >>> for parent, child in find_single_child_dirs(Path("~/Downloads")):
        ...     print(f"Parent: {parent}, Child: {child}")
    """
    for parent_dir in root_dir.iterdir():
        if parent_dir.is_dir():
            children = list(parent_dir.iterdir())
            dir_children = [c for c in children if c.is_dir()]

            if len(dir_children) == 1 and len(children) == 1:
                yield parent_dir, dir_children[0]


def reorganize_directories(
    source_dir: Path, stats: OperationStats, no_confirm: bool = False
) -> None:
    """
    Reorganize a directory structure by moving single-child directories up.

    Args:
        source_dir: Directory to reorganize
        stats: OperationStats for logging and stats
        no_confirm: Skip confirmation prompts if True

    Examples:
        >>> operation_stats = OperationStats()
        >>> reorganize_directories(Path("~/tmp"), operation_stats)
        >>> reorganize_directories(Path("~/tmp"), operation_stats, no_confirm=True)
    """
    for parent_dir, child_dir in find_single_child_dirs(source_dir):
        stats.dirs_examined += 1

        stats.add_log(f"Processing: {parent_dir.name}", LogLevel.OPERATION)

        # Clean before reorganization
        files_removed, dirs_removed = remove_apple_system_files(parent_dir, stats)
        stats.files_removed += files_removed
        stats.dirs_removed += dirs_removed

        target_path = source_dir / child_dir.name

        # Handle existing target
        if target_path.exists() and target_path != child_dir:
            stats.add_log(f"Target exists: {target_path}", LogLevel.WARNING)

            if not no_confirm and not get_user_confirmation("Overwrite target?"):
                stats.add_log("Skipped by user", LogLevel.INFO)
                stats.dirs_ignored += 1
                continue

            try:
                shutil.rmtree(target_path)
            except OSError as e:
                stats.add_log(f"Clear failed: {e}", LogLevel.ERROR)
                stats.dirs_ignored += 1
                continue

        # Perform move
        try:
            shutil.move(str(child_dir), str(source_dir))

            # Remove parent if empty
            if not any(parent_dir.iterdir()):
                parent_dir.rmdir()
                stats.dirs_reorganized += 1
                stats.add_log("Reorganization successful", LogLevel.SUCCESS)
            else:
                stats.add_log("Parent not empty after move", LogLevel.WARNING)
                stats.dirs_ignored += 1

        except OSError as e:
            stats.add_log(f"Move failed: {e}", LogLevel.ERROR)
            stats.dirs_ignored += 1


def get_user_confirmation(prompt: str, default: bool = False) -> bool:
    """
    Get confirmation from user with customizable defaults.

    Args:
        prompt: Question to ask
        default: Default if user just hits enter

    Returns:
        True if confirmed, False otherwise

    Examples:
        >>> if get_user_confirmation("Delete this file?"):
        ...     print("Deleting file...")
        >>> if get_user_confirmation("Proceed with operation?", default=True):
        ...     print("Operation confirmed")
    """
    suffix = " [Y/n]" if default else " [y/N]"
    response = input(prompt + suffix).strip().lower()

    if not response:
        return default
    return response.startswith("y")


def main() -> Literal[0, 1]:
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description="Advanced ZIP extraction and directory reorganization tool",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "directory",
        type=Path,
        help="Directory containing files to process",
    )
    parser.add_argument(
        "--clean-only",
        action="store_true",
        help="Only clean system files without extracting or reorganizing",
    )
    parser.add_argument(
        "--no-confirm",
        action="store_true",
        help="Skip all confirmation prompts",
    )
    parser.add_argument(
        "-v",
        action="count",
        default=2,
        help="Verbosity level (0=silent, 1=normal, 2=verbose)",
    )

    args = parser.parse_args()
    stats = OperationStats()

    # Validate directory
    if not args.directory.is_dir():
        print(f"Error: Directory not found: {args.directory}", file=sys.stderr)
        return 1

    # Clean-only mode
    if args.clean_only:
        stats.add_log(f"Starting clean-only mode in {args.directory}", LogLevel.INFO)
        files, dirs = remove_apple_system_files(args.directory, stats)
        stats.files_removed = files
        stats.dirs_removed = dirs
    else:
        # Full processing mode
        stats.add_log(f"Starting full processing in {args.directory}", LogLevel.INFO)

        # Extract ZIP files
        stats.add_log("Starting ZIP extraction", LogLevel.OPERATION)
        extract_zip_files(args.directory, stats, args.no_confirm)

        # Additional cleaning
        stats.add_log("Performing additional cleaning", LogLevel.OPERATION)
        files, dirs = remove_apple_system_files(args.directory, stats)
        stats.files_removed += files
        stats.dirs_removed += dirs

        # Reorganization
        stats.add_log("Starting directory reorganization", LogLevel.OPERATION)
        reorganize_directories(args.directory, stats, args.no_confirm)

    # Generate and print output based on verbosity
    if args.v > 0:
        output = stats.get_output(verbosity=args.v)
        if output:
            print(output)

    return 0


if __name__ == "__main__":
    sys.exit(main())
