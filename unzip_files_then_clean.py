#!/usr/bin/env python3
"""
Advanced ZIP Extraction and Directory Reorganization Tool.

This script performs three main operations with comprehensive logging and statistics:
1. Extracts all ZIP files in a directory into corresponding subdirectories
2. Removes Apple system files (.DS_Store, .__MACOSX folders, etc.)
3. Reorganizes directories by moving single-child directories up one level

Features:
- Detailed progress logging with --verbose option
- Beautiful tabular output (with fallback to basic formatting)
- Comprehensive statistics collection
- Modern Python typing and dataclasses
- Configurable confirmation prompts

Example usage:
    $ python unzip_files_then_clean.py /path/to/directory
    $ python unzip_files_then_clean.py /path/to/directory --clean-only
    $ python unzip_files_then_clean.py /path/to/directory --no-confirm --verbose

Returns:
    0: Success
    1: Error (directory not found or processing error)
"""

import argparse
import re
import shutil
import sys
import zipfile
from dataclasses import dataclass, field
from enum import Enum, auto
from pathlib import Path
from typing import Generator, List, Literal, Optional, Set, Tuple

# Try to import tabulate, with fallback to basic printing if not available
try:
    from tabulate import tabulate

    HAS_TABULATE = True
except ImportError:
    HAS_TABULATE = False

    # Define a simple tabulate function as a fallback
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

    print(
        "Note: For better output formatting, install 'tabulate' "
        "with: `pip install tabulate`"
    )


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


@dataclass
class OperationStats:
    """Statistics collector for all operations."""

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

    def add_log(self, message: str, level: LogLevel = LogLevel.INFO) -> None:
        """Add a new log entry."""
        self.logs.append(LogEntry(message, level))

    def print_summary(self) -> None:
        """Print a comprehensive summary of all operations."""
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

        # Print summary header
        print("\n" + "=" * 80)
        print("PROCESSING SUMMARY".center(80))
        print("=" * 80)

        # Print each section
        for section, data in summary_data.items():
            print(f"\n{section.upper():^80}")
            print(tabulate(data, tablefmt="fancy"))

        # Print error summary if any
        error_logs = [log for log in self.logs if log.level == LogLevel.ERROR]
        if error_logs:
            print("\n" + "!" * 80)
            print(f"  {len(error_logs)} ERRORS ENCOUNTERED  ".center(80, "!"))
            print("!" * 80)

    def print_logs(self, verbose: bool = False) -> None:
        """Print all collected logs with optional filtering."""
        if not self.logs:
            return

        print("\n" + "-" * 80)
        print("DETAILED OPERATION LOGS".center(80))
        print("-" * 80)

        for log in self.logs:
            if not verbose and log.level == LogLevel.INFO:
                continue

            prefix = {
                LogLevel.INFO: "[INFO]",
                LogLevel.WARNING: "[WARNING]",
                LogLevel.ERROR: "[ERROR]",
                LogLevel.SUCCESS: "[SUCCESS]",
                LogLevel.OPERATION: "→",
            }.get(log.level, "")

            print(f"{prefix} {log.message}")


# Constants for Apple system files to remove
APPLE_SYSTEM_FILES: Set[str] = {
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
    """Check if a filename matches known Apple system file patterns."""
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
                stats.add_log(f"Removed Apple directory: {path}", LogLevel.INFO)
            except OSError as e:
                stats.add_log(f"Error removing {path}: {e}", LogLevel.ERROR)

        # Handle files - ONLY ACTUAL APPLE FILES
        elif path.is_file() and is_apple_system_file(path.name):
            try:
                path.unlink()
                files_removed += 1
                stats.add_log(f"Removed Apple file: {path}", LogLevel.INFO)
            except OSError as e:
                stats.add_log(f"Error removing {path}: {e}", LogLevel.ERROR)

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
    """Find directories with exactly one subdirectory and no other items."""
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
    Reorganize directory structure by moving single-child directories up.

    Args:
        source_dir: Directory to reorganize
        stats: OperationStats for logging and stats
        no_confirm: Skip confirmation prompts if True
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
        "--verbose",
        "-v",
        action="store_true",
        help="Show detailed operation logs",
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

    # Print results
    stats.print_summary()
    if args.verbose:
        stats.print_logs(verbose=True)

    return 0


if __name__ == "__main__":
    sys.exit(main())
