#!/usr/bin/env python3
"""
Advanced ZIP Extraction and Directory Reorganization Tool.

This script performs three main operations with comprehensive logging and statistics:
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
import re
import shutil
import sys
import zipfile
from dataclasses import dataclass, field
from enum import Enum, auto
from pathlib import Path
from typing import Generator, List, Set, Tuple, Literal

try:
    from colorama import init, Fore, Back, Style

    init(autoreset=True)
    HAS_COLORAMA = True
except ImportError:
    HAS_COLORAMA = False

    def init(*args, **kwargs):
        """Stub function for Colorama import fallback."""
        pass

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
except ImportError:
    HAS_RICH = False
    # Tabulate fallback:
    try:
        from tabulate import tabulate

        HAS_TABULATE = True
    except ImportError:
        HAS_TABULATE = False

        def tabulate(data, headers=None, *args, **kwargs):
            """Simple tabulate fallback when the package is not available."""
            if not data:
                return ""
            # Calculate column widths for each column across all rows
            col_widths = []
            for i in range(len(data[0])):
                max_width = max(len(str(row[i])) for row in data)
                if headers:
                    max_width = max(max_width, len(str(headers[i])))
                col_widths.append(max_width)

            divider = "+" + "+".join("-" * (w + 2) for w in col_widths) + "+"
            table = [divider]
            if headers:
                table.extend(
                    [
                        "| "
                        + " | ".join(
                            f"{str(h):<{w}}" for h, w in zip(headers, col_widths)
                        )
                        + " |",
                        divider,
                    ]
                )
            for row in data:
                table.append(
                    "| "
                    + " | ".join(f"{str(i):<{w}}" for i, w in zip(row, col_widths))
                    + " |"
                )
            table.append(divider)
            return "\n".join(table)


class LogLevel(Enum):
    """Enum for different log levels."""

    INFO = auto()
    WARNING = auto()
    ERROR = auto()
    SUCCESS = auto()
    OPERATION = auto()

    def get_color(self) -> str:
        """Return the appropriate color for each log level."""
        if not HAS_COLORAMA:
            return ""
        return {
            LogLevel.INFO: Fore.CYAN,
            LogLevel.WARNING: Fore.YELLOW,
            LogLevel.ERROR: Fore.RED,
            LogLevel.SUCCESS: Fore.GREEN,
            LogLevel.OPERATION: Fore.MAGENTA,
        }.get(self, "")


@dataclass
class LogEntry:
    """Class representing a single log entry.

    Attributes:
        message (str): The log message content.
        level (LogLevel): Severity level of the message.
        timestamp (float|None): Optional timestamp for the log entry.
    """

    message: str
    level: LogLevel = LogLevel.INFO
    timestamp: float | None = field(default=None, repr=False)


@dataclass
class OperationStats:
    """Statistics collector for all operations with centralized output.

    Attributes:
        total_zips (int): Total ZIP files processed.
        successful_extractions (int): Successfully extracted ZIPs.
        failed_extractions (int): Failed extractions.
        files_removed (int): Apple system files removed.
        dirs_removed (int): Apple system directories removed.
        dirs_examined (int): Directories examined for reorganization.
        dirs_reorganized (int): Directories successfully reorganized.
        dirs_ignored (int): Directories skipped during reorganization.
        logs (List[LogEntry]): Collection of all log entries.
        removed_files_details (List[str]): Detailed list of removed files (for verbosity=2).
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

    def add_log(self, message: str, level: LogLevel = LogLevel.INFO) -> None:
        """Add a new log entry.

        Args:
            message: The log message to add.
            level: Severity level of the message.

        Example:
            >>> stats = OperationStats()
            >>> stats.add_log("Processing started", LogLevel.INFO)
        """
        self.logs.append(LogEntry(message, level))

    def add_removed_file_detail(self, path: str) -> None:
        """Add details of a removed file for verbose output.

        Args:
            path: Path of the removed file/directory.

        Example:
            >>> stats = OperationStats()
            >>> stats.add_removed_file_detail("/path/to/.DS_Store")
        """
        self.removed_files_details.append(path)

    def print_summary(self, verbosity: int = 2) -> None:
        """Print a comprehensive summary in a unified tabular format with category separators."""
        if verbosity == 0:
            return

        if HAS_RICH:
            console = Console()
            summary_table = Table(
                title="[bold]PROCESSING SUMMARY[/bold]",
                box=box.ROUNDED,
                show_header=True,
                header_style="bold magenta",
                title_style="bold green",
                row_styles=["", "", ""],
            )

            summary_table.add_column("Category", style="cyan", no_wrap=True)
            summary_table.add_column("Metric", style="yellow")
            summary_table.add_column("Value", style="green", justify="right")

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
            summary_table.add_row("", "Reorg Rate", reorg_rate)

            console.print(summary_table)

        else:
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

        # Error summary if any errors (show even in verbosity=1)
        error_logs = [log for log in self.logs if log.level == LogLevel.ERROR]
        if error_logs:
            print("\n" + f" {len(error_logs)} ERRORS ENCOUNTERED ".center(80, "!"))

    def print_logs(self, verbosity: int = 2) -> None:
        """Print logs in a separate table when in verbose mode."""
        if verbosity == 2 and self.logs:
            if HAS_RICH:
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
                    }.get(log.level, "")

                    log_table.add_row(level_style, log.message)

                console.print(log_table)
            else:
                # tabulate fallback:
                log_data = []
                for log in self.logs:
                    prefix = {
                        LogLevel.INFO: "[INFO]",
                        LogLevel.WARNING: "[WARN]",
                        LogLevel.ERROR: "[ERR]",
                        LogLevel.SUCCESS: "[OK]",
                        LogLevel.OPERATION: "→",
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


# Constants for Apple system files to remove
APPLE_SYSTEM_FILES: Set[str] = {
    ".DS_Store",
    "._.DS_Store",
    ".AppleDouble",
    ".LSOverride",
    re.compile(r"^\._.*$"),  # Only files starting with ._
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
        filename: The filename to check.

    Returns:
        True if the file is an Apple system file, False otherwise.

    Examples:
        >>> is_apple_system_file(".DS_Store")
        True
        >>> is_apple_system_file("normal_file.txt")
        False
        >>> is_apple_system_file("._hidden_file")
        True
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
    """Recursively remove Apple system files and directories.

    Args:
        directory: Path to directory to clean.
        stats: OperationStats instance for logging.

    Returns:
        Tuple of (files_removed, dirs_removed) counts.

    Examples:
        >>> my_stats = OperationStats()
        >>> remove_apple_system_files(Path("/tmp"), my_stats)
        (3, 1)  # Example return value
    """
    files_removed, dirs_removed = 0, 0

    for path in sorted(
        directory.glob("**/*"), key=lambda p: len(p.parts), reverse=True
    ):
        if not path.exists():
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

    return files_removed, dirs_removed


def extract_zip_files(
    source_dir: Path, stats: OperationStats, no_confirm: bool = False
) -> None:
    """Extract all ZIP files in the directory to corresponding subdirectories.

    Args:
        source_dir: Directory containing ZIP files.
        stats: OperationStats instance for logging.
        no_confirm: Skip confirmation prompts if True.

    Examples:
        >>> my_stats = OperationStats()
        >>> extract_zip_files(Path("/tmp/zips"), my_stats, no_confirm=True)
        # Processes all ZIP files in /tmp/zips without confirmation prompts
    """
    for zip_file in source_dir.glob("*.zip"):
        stats.total_zips += 1
        dest_dir = source_dir / zip_file.stem

        stats.add_log(f"Processing ZIP: {zip_file.name}", LogLevel.OPERATION)
        stats.add_log(f"Creating directory: {dest_dir}", LogLevel.INFO)

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

        try:
            dest_dir.mkdir(exist_ok=True)
            with zipfile.ZipFile(zip_file, "r") as zip_ref:
                zip_ref.extractall(dest_dir)

            files_removed, dirs_removed = remove_apple_system_files(dest_dir, stats)
            stats.files_removed += files_removed
            stats.dirs_removed += dirs_removed

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
        root_dir: Directory to search for single-child directories.

    Yields:
        Tuples of (parent_dir, child_dir) pairs.

    Examples:
        >>> for parent, child in find_single_child_dirs(Path("/tmp")):
        ...     print(f"Found: {parent} -> {child}")
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
    """Reorganize a directory structure by moving single-child directories up.

    Args:
        source_dir: Directory to reorganize.
        stats: OperationStats instance for logging.
        no_confirm: Skip confirmation prompts if True.

    Examples:
        >>> my_stats = OperationStats()
        >>> reorganize_directories(Path("/tmp"), my_stats, no_confirm=True)
        # Reorganizes directories without confirmation prompts
    """
    for parent_dir, child_dir in find_single_child_dirs(source_dir):
        stats.dirs_examined += 1
        stats.add_log(f"Processing: {parent_dir.name}", LogLevel.OPERATION)

        files_removed, dirs_removed = remove_apple_system_files(parent_dir, stats)
        stats.files_removed += files_removed
        stats.dirs_removed += dirs_removed

        target_path = source_dir / child_dir.name

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

        try:
            shutil.move(str(child_dir), str(source_dir))

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
    """Get confirmation from user with customizable defaults.

    Args:
        prompt: Question to ask the user.
        default: Default response if user just hits enter.

    Returns:
        True if user confirmed, False otherwise.

    Examples:
        >>> get_user_confirmation("Continue?", default=True)
        Continue? [Y/n] y
        True
        >>> get_user_confirmation("Delete files?", default=False)
        Delete files? [y/N] n
        False
    """
    suffix = " [Y/n]" if default else " [y/N]"
    response = input(prompt + suffix).strip().lower()
    return response.startswith("y") if response else default


def main() -> Literal[0, 1]:
    """Main entry point for the script.

    Returns:
        0 on success, 1 on error.
    """
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
        default=2,
        help="Verbosity level (0=silent, 1=normal, 2=verbose)",
    )

    args = parser.parse_args()
    args.directory = Path(args.directory).expanduser()
    stats = OperationStats()

    if not HAS_COLORAMA:
        stats.add_log(
            "Note: For better output, install 'colorama' "
            "with: `pip install colorama`",
            LogLevel.INFO,
        )
    if not HAS_RICH:
        stats.add_log(
            "Note: For better output formatting, install 'rich' "
            "with: `pip install rich`",
            LogLevel.INFO,
        )
        if not HAS_TABULATE:
            stats.add_log(
                "Note: For better output formatting, install 'tabulate' "
                "with: `pip install tabulate`",
                LogLevel.INFO,
            )

    if not args.directory.is_dir():
        stats.add_log(f"Directory not found: {args.directory}", LogLevel.ERROR)
        stats.print_logs(verbosity=1)  # Always show errors
        return 1

    if args.clean_only:
        stats.add_log(f"Starting clean-only mode in {args.directory}", LogLevel.INFO)
        files, dirs = remove_apple_system_files(args.directory, stats)
        stats.files_removed = files
        stats.dirs_removed = dirs
    else:
        stats.add_log(f"Starting full processing in {args.directory}", LogLevel.INFO)
        extract_zip_files(args.directory, stats, args.no_confirm)
        files, dirs = remove_apple_system_files(args.directory, stats)
        stats.files_removed += files
        stats.dirs_removed += dirs
        reorganize_directories(args.directory, stats, args.no_confirm)

    stats.print_logs(verbosity=args.verbosity)
    stats.print_summary(verbosity=args.verbosity)

    return 0 if not any(log.level == LogLevel.ERROR for log in stats.logs) else 1


if __name__ == "__main__":
    sys.exit(main())
