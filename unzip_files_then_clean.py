#!/usr/bin/env python3
"""
ZIP Extraction and Directory Reorganization Tool.

This script performs three main operations:
1. Extracts all ZIP files in a directory into corresponding subdirectories
2. Removes Apple system files (.DS_Store, .__MACOSX folders, etc.)
3. Reorganizes directories by moving single-child directories up one level

Example usage:
    $ python unzip_files_then_clean.py /path/to/directory
    $ python unzip_files_then_clean.py /path/to/directory --clean-only
    $ python unzip_files_then_clean.py /path/to/directory --no-confirm

Returns:
    0: Success
    1: Error (directory not found)
"""

import argparse
import re
import shutil
import sys
import zipfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Generator, List, Literal, Optional, Set, Tuple

# Try to import tabulate, with fallback to basic printing if not available
try:
    from tabulate import tabulate

    HAS_TABULATE = True
except ImportError:
    HAS_TABULATE = False

    # Define a simple tabulate function as a fallback
    def tabulate(data):
        """Simple tabulate fallback when the package is not available."""
        result = []
        for row in data:
            result.append("| " + " | ".join(str(cell) for cell in row) + " |")
        return "\n".join(result)

    print(
        "Warning: 'tabulate' package not found. Install with 'pip install tabulate' for better output formatting."
    )
    print()


@dataclass
class OperationStats:
    """Statistics for different operations in the script."""

    # ZIP extraction stats
    total_zips: int = 0
    successful_extractions: int = 0
    failed_extractions: int = 0

    # Cleaning stats
    total_files_removed: int = 0
    total_dirs_removed: int = 0

    # Reorganization stats
    dirs_examined: int = 0
    dirs_reorganized: int = 0
    dirs_ignored: int = 0

    # Detailed logs
    logs: List[str] = field(default_factory=list)

    def add_log(self, message: str) -> None:
        """Add a log message to the log's list."""
        self.logs.append(message)

    def print_summary(self) -> None:
        """Print a summary of all operations."""
        if HAS_TABULATE:
            # Create table data
            tables = []

            # ZIP extraction table
            zip_data = [
                ["Total ZIP files", self.total_zips],
                ["Successful extractions", self.successful_extractions],
                ["Failed extractions", self.failed_extractions],
            ]
            tables.append(("ZIP Processing Summary", zip_data))

            # Cleaning table
            clean_data = [
                ["Files removed", self.total_files_removed],
                ["Directories removed", self.total_dirs_removed],
            ]
            tables.append(("Cleaning Summary", clean_data))

            # Reorganization table
            reorg_data = [
                ["Directories examined", self.dirs_examined],
                ["Directories reorganized", self.dirs_reorganized],
                ["Directories ignored", self.dirs_ignored],
            ]
            tables.append(("Reorganization Summary", reorg_data))

            # Print each table
            print("\n=== OPERATION SUMMARY ===\n")
            for title, data in tables:
                print(f"--- {title} ---")
                print(tabulate(data))
                print()

            # Print overall statistics
            overall_data = [
                ["Total files cleaned", self.total_files_removed],
                ["Total directories cleaned", self.total_dirs_removed],
                [
                    "Success rate (ZIP extraction)",
                    (
                        f"{self.successful_extractions/self.total_zips*100:.1f}%"
                        if self.total_zips > 0
                        else "N/A"
                    ),
                ],
                [
                    "Success rate (reorganization)",
                    (
                        f"{self.dirs_reorganized/self.dirs_examined*100:.1f}%"
                        if self.dirs_examined > 0
                        else "N/A"
                    ),
                ],
            ]
            print("--- Overall Statistics ---")
            print(tabulate(overall_data))
            print()
        else:
            # Fallback to basic printing if tabulate is not available
            print("\n=== OPERATION SUMMARY ===\n")

            print("--- ZIP Processing Summary ---")
            print(f"Total ZIP files: {self.total_zips}")
            print(f"Successful extractions: {self.successful_extractions}")
            print(f"Failed extractions: {self.failed_extractions}")
            print()

            print("--- Cleaning Summary ---")
            print(f"Files removed: {self.total_files_removed}")
            print(f"Directories removed: {self.total_dirs_removed}")
            print()

            print("--- Reorganization Summary ---")
            print(f"Directories examined: {self.dirs_examined}")
            print(f"Directories reorganized: {self.dirs_reorganized}")
            print(f"Directories ignored: {self.dirs_ignored}")
            print()

            print("--- Overall Statistics ---")
            print(f"Total files cleaned: {self.total_files_removed}")
            print(f"Total directories cleaned: {self.total_dirs_removed}")
            if self.total_zips > 0:
                print(
                    f"Success rate (ZIP extraction): {self.successful_extractions/self.total_zips*100:.1f}%"
                )
            if self.dirs_examined > 0:
                print(
                    f"Success rate (reorganization): {self.dirs_reorganized/self.dirs_examined*100:.1f}%"
                )
            print()

    def print_logs(self, verbose: bool = False) -> None:
        """Print all logs collected during operations."""
        if verbose and self.logs:
            print("\n=== DETAILED LOGS ===\n")
            for log in self.logs:
                print(log)
            print()


# Constants for Apple system files to remove
APPLE_SYSTEM_FILES: Set[str] = {
    ".DS_Store",
    "._.DS_Store",
    ".AppleDouble",
    ".LSOverride",
}

# Constants for Apple system directories to remove
APPLE_SYSTEM_DIRS: Set[str] = {
    "__MACOSX",
    ".__MACOSX",
    ".Spotlight-V100",
    ".Trashes",
    ".fseventsd",
}


def remove_apple_system_files(
    directory: Path, stats: Optional[OperationStats] = None
) -> Tuple[int, int]:
    """
    Recursively remove Apple system files and directories from the given directory.

    Args:
        directory: Directory to clean.
        stats: Optional OperationStats object to collect logs and statistics.

    Returns:
        A tuple containing (files_removed, dirs_removed).
        files_removed: Number of files removed.
        dirs_removed: Number of directories removed.

    Examples:
        >>> remove_apple_system_files(Path("/data/extracted"))
        (12, 3)  # 12 files and 3 directories removed

        >>> # No system files found
        >>> remove_apple_system_files(Path("/clean/directory"))
        (0, 0)
    """
    files_removed: int = 0
    dirs_removed: int = 0

    # Process all files and directories
    for path in sorted(
        directory.glob("**/*"), reverse=True
    ):  # Reverse to process deeper paths first
        # Skip if the path no longer exists (might have been in a removed directory)
        if not path.exists():
            continue

        path_name: str = path.name

        # Check if this is a directory to remove
        if path.is_dir():
            if path_name in APPLE_SYSTEM_DIRS:
                log_message = (
                    f"Removing Apple system directory: {path.relative_to(directory)}"
                )
                if stats:
                    stats.add_log(log_message)
                try:
                    shutil.rmtree(path)
                    dirs_removed += 1
                except OSError as e:
                    error_message = f"Failed to remove directory {path}: {e}"
                    if stats:
                        stats.add_log(error_message)

        # Check if this is a file to remove
        elif path.is_file():
            # Direct match with file patterns
            is_system_file: bool = path_name in APPLE_SYSTEM_FILES

            # Check patterns with wildcards
            if not is_system_file:
                for pattern in APPLE_SYSTEM_FILES:
                    if "*" in pattern and re.match(
                        f"^{pattern.replace('*', '.*')}$", path_name
                    ):
                        is_system_file = True
                        break

            if is_system_file:
                log_message = (
                    f"Removing Apple system file: {path.relative_to(directory)}"
                )
                if stats:
                    stats.add_log(log_message)
                try:
                    path.unlink()
                    files_removed += 1
                except OSError as e:
                    error_message = f"Failed to remove file {path}: {e}"
                    if stats:
                        stats.add_log(error_message)

    return files_removed, dirs_removed


def extract_zip_files(
    source_dir: Path, no_confirm: bool = False, stats: Optional[OperationStats] = None
) -> Tuple[int, int, int]:
    """
    Extract all ZIP files in the source directory to corresponding subdirectories.

    This function iterates through all ZIP files in the source directory,
    creates a subdirectory with the same name (minus the .zip extension),
    and extracts the contents into that subdirectory. It also cleans up
    Apple system files during the extraction process.

    Args:
        source_dir: Directory containing ZIP files to extract.
        no_confirm: If True, overwrite existing directories without confirmation.
        stats: Optional OperationStats object to collect logs and statistics.

    Returns:
        A tuple containing (total_processed, success_count, failure_count).
        total_processed: Total ZIP files found.
        success_count: Successfully extracted ZIP files.
        failure_count: Failed extractions.

    Examples:
        >>> extract_zip_files(Path("/data/zips"))
        (10, 8, 2)  # Processed 10, 8 successes, 2 failures

        >>> # Directory with no ZIP files
        >>> extract_zip_files(Path("/empty/directory"))
        (0, 0, 0)
    """
    total_processed: int = 0
    success_count: int = 0
    failure_count: int = 0

    for zip_file in source_dir.glob("*.zip"):
        total_processed += 1
        dest_dir: Path = source_dir / zip_file.stem

        log_message = f"Processing: {zip_file.name}"
        if stats:
            stats.add_log(log_message)
            stats.add_log(f"Creating directory: {dest_dir}")

        # Handle existing directory
        if dest_dir.exists():
            if stats:
                stats.add_log("Destination directory already exists.")
            if not no_confirm:
                response: str = input("Overwrite contents? (y/n): ").lower()
                if response != "y":
                    if stats:
                        stats.add_log("Operation cancelled for this file.")
                    failure_count += 1
                    continue
            else:
                if stats:
                    stats.add_log("Overwriting as --no-confirm flag is set...")

            # Clear the existing directory
            if stats:
                stats.add_log("Clearing existing directory...")
            try:
                shutil.rmtree(dest_dir)
            except OSError as e:
                error_message = f"Failed to clear directory: {e}"
                if stats:
                    stats.add_log(error_message)
                failure_count += 1
                continue

        # Create a destination directory
        try:
            dest_dir.mkdir(exist_ok=True)
        except OSError as e:
            error_message = f"Failed to create directory: {e}"
            if stats:
                stats.add_log(error_message)
            failure_count += 1
            continue

        # Extract ZIP file
        if stats:
            stats.add_log("Extracting ZIP file...")
        try:
            with zipfile.ZipFile(zip_file, "r") as zip_ref:
                zip_ref.extractall(dest_dir)

            # Clean up any Apple system files that might have been extracted
            if stats:
                stats.add_log("Cleaning up Apple system files...")
            files_removed, dirs_removed = remove_apple_system_files(dest_dir, stats)
            if files_removed > 0 or dirs_removed > 0 and stats:
                stats.add_log(
                    f"Removed {files_removed} system files and {dirs_removed} system directories"
                )

            # Verify extraction
            extracted_files: int = sum(1 for _ in dest_dir.rglob("*") if _.is_file())
            if extracted_files > 0:
                if stats:
                    stats.add_log(f"{extracted_files} file(s) extracted.")
                    stats.add_log("Removing original ZIP file...")
                try:
                    zip_file.unlink()
                    if stats:
                        stats.add_log("ZIP file removed successfully.")
                    success_count += 1
                except OSError as e:
                    error_message = f"Failed to remove ZIP file: {e}"
                    if stats:
                        stats.add_log(error_message)
                    failure_count += 1
            else:
                if stats:
                    stats.add_log("No files extracted (empty or corrupt ZIP).")
                failure_count += 1
        except (zipfile.BadZipFile, OSError) as e:
            error_message = f"Extraction failed: {e}"
            if stats:
                stats.add_log(error_message)
            failure_count += 1

    return total_processed, success_count, failure_count


def find_single_child_dirs(root_dir: Path) -> Generator[Tuple[Path, Path], None, None]:
    """
    Find directories that contain exactly one subdirectory and no other items.

    Args:
        root_dir: Directory to search for single-child directories.

    Yields:
        Tuples of (parent_dir, child_dir) for each single-child directory found.

    Examples:
        >>> list(find_single_child_dirs(Path("/data")))
        [(Path("/data/dir1"), Path("/data/dir1/subdir"))]

        >>> # Directory with multiple subdirectories in each parent
        >>> list(find_single_child_dirs(Path("/data/complex")))
        []
    """
    for parent_dir in root_dir.iterdir():
        if not parent_dir.is_dir():
            continue

        children: List[Path] = list(parent_dir.iterdir())
        dir_children: List[Path] = [child for child in children if child.is_dir()]

        if len(dir_children) == 1 and len(children) == 1:
            yield parent_dir, dir_children[0]


def reorganize_directories(
    source_dir: Path, no_confirm: bool = False, stats: Optional[OperationStats] = None
) -> Tuple[int, int, int]:
    """
    Reorganize the directory structure by moving single-child directories up one level.

    This function identifies directories that contain exactly one subdirectory
    and no other files, then moves that subdirectory up to the parent level
    and removes the now-empty parent directory.

    Args:
        source_dir: Directory to reorganize.
        no_confirm: If True, overwrite existing directories without confirmation.
        stats: Optional OperationStats object to collect logs and statistics.

    Returns:
        A tuple containing (total_processed, reorganized_count, ignored_count).
        total_processed: Total directories examined.
        reorganized_count: Successfully reorganized directories.
        ignored_count: Directories left unchanged.

    Examples:
        >>> reorganize_directories(Path("/data"))
        (15, 8, 7)  # 15 examined, 8 reorganized, 7 ignored

        >>> # Directory with no subdirectories
        >>> reorganize_directories(Path("/flat/directory"))
        (0, 0, 0)
    """
    total_processed: int = 0
    reorganized_count: int = 0
    ignored_count: int = 0

    for parent_dir in source_dir.iterdir():
        if not parent_dir.is_dir():
            continue

        total_processed += 1
        if stats:
            stats.add_log(f"Examining directory: {parent_dir.name}")

        # First, clean any Apple system files in this directory
        files_removed, dirs_removed = remove_apple_system_files(parent_dir, stats)
        if files_removed > 0 or dirs_removed > 0 and stats:
            stats.add_log(
                f"Removed {files_removed} system files and {dirs_removed} system directories"
            )

        # Now check for single child directories
        children: List[Path] = list(parent_dir.iterdir())
        dir_children: List[Path] = [child for child in children if child.is_dir()]

        if stats:
            stats.add_log(f"Subdirectories: {len(dir_children)}")
            stats.add_log(f"Total items: {len(children)}")

        if len(dir_children) == 1 and len(children) == 1:
            child_dir: Path = dir_children[0]
            if stats:
                stats.add_log(f"Contains single subdirectory: {child_dir.name}")

            target_path: Path = source_dir / child_dir.name

            # Handle existing directory
            if target_path.exists() and target_path != child_dir:
                if stats:
                    stats.add_log("Directory with same name exists in target.")
                if not no_confirm:
                    response: str = input("Overwrite? (y/n): ").lower()
                    if response != "y":
                        if stats:
                            stats.add_log("Operation cancelled for this directory.")
                        ignored_count += 1
                        continue
                else:
                    if stats:
                        stats.add_log("Overwriting as --no-confirm flag is set...")

                if stats:
                    stats.add_log("Removing existing directory...")
                try:
                    shutil.rmtree(target_path)
                except OSError as e:
                    error_message = f"Failed to remove existing directory: {e}"
                    if stats:
                        stats.add_log(error_message)
                    ignored_count += 1
                    continue

            # Move the directory
            if stats:
                stats.add_log(f"Moving {child_dir.name} to parent directory...")
            try:
                shutil.move(str(child_dir), str(source_dir))
                if stats:
                    stats.add_log("Directory moved successfully.")

                # Remove parent if empty
                remaining_items: List[Path] = list(parent_dir.iterdir())
                if not remaining_items:
                    try:
                        parent_dir.rmdir()
                        if stats:
                            stats.add_log("Parent directory removed (empty).")
                        reorganized_count += 1
                    except OSError as e:
                        error_message = f"Failed to remove parent directory: {e}"
                        if stats:
                            stats.add_log(error_message)
                        ignored_count += 1
                else:
                    if stats:
                        stats.add_log(
                            f"Parent not empty ({len(remaining_items)} items remaining)."
                        )
                    ignored_count += 1
            except OSError as e:
                error_message = f"Failed to move directory: {e}"
                if stats:
                    stats.add_log(error_message)
                ignored_count += 1
        else:
            if stats:
                stats.add_log("No single subdirectory found - ignoring.")
            ignored_count += 1

    return total_processed, reorganized_count, ignored_count


def clean_directory(
    directory: Path, stats: Optional[OperationStats] = None
) -> Tuple[int, int]:
    """
    Clean Apple system files from a directory recursively.

    Args:
        directory: Directory to clean.
        stats: Optional OperationStats object to collect logs and statistics.

    Returns:
        A tuple containing (files_removed, dirs_removed).
        files_removed: Number of files removed.
        dirs_removed: Number of directories removed.

    Examples:
        >>> clean_directory(Path("/data/messy"))
        (25, 5)  # 25 files and 5 directories removed

        >>> # Already clean directory
        >>> clean_directory(Path("/data/clean"))
        (0, 0)
    """
    if stats:
        stats.add_log(f"Cleaning Apple system files in '{directory}'")

    files_removed, dirs_removed = remove_apple_system_files(directory, stats)

    return files_removed, dirs_removed


def get_user_confirmation(prompt: str, default: bool = False) -> bool:
    """
    Get confirmation from the user via the command line.

    Args:
        prompt: Question to present to the user.
        default: Default value if the user just presses Enter.

    Returns:
        True if the user confirmed, False otherwise.

    Examples:
        >>> get_user_confirmation("Delete this file?")
        Delete this file? (y/n): y
        True

        >>> get_user_confirmation("Proceed with operation?", default=True)
        Proceed with operation? (Y/n):
        True
    """
    default_text: str = "Y/n" if default else "y/N"
    response: str = input(f"{prompt} ({default_text}): ").lower()

    if not response:
        return default

    return response.startswith("y")


def main() -> Literal[0, 1]:
    """
    Main entry point for the script.

    Parses command line arguments and executes the appropriate functions
    based on user input.

    Returns:
        0 on success, 1 on error.

    Examples:
        >>> # Success case
        >>> main()  # when valid arguments are provided
        0

        >>> # Error case
        >>> main()  # when the directory doesn't exist
        1
    """
    parser = argparse.ArgumentParser(
        description="Extract ZIP files, clean Apple system files, and reorganize directory structure."
    )
    parser.add_argument(
        "directory", type=Path, help="Directory containing ZIP files to process"
    )
    parser.add_argument(
        "--clean-only",
        action="store_true",
        help="Only clean Apple system files without extracting ZIPs or reorganizing",
    )
    parser.add_argument(
        "--no-confirm",
        action="store_true",
        help="Do not ask for confirmation before overwriting files",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Print detailed logs of all operations",
    )
    args = parser.parse_args()

    # Create stat's object to collect information
    stats = OperationStats()

    # Check if the directory exists
    if not args.directory.is_dir():
        print(f"Error: Directory '{args.directory}' does not exist.")
        return 1

    # Run in clean-only mode if requested
    if args.clean_only:
        files_removed, dirs_removed = clean_directory(args.directory, stats)
        stats.total_files_removed += files_removed
        stats.total_dirs_removed += dirs_removed
        stats.print_summary()
        if args.verbose:
            stats.print_logs(args.verbose)
        return 0

    # Process ZIP files
    stats.add_log(f"Processing ZIP files in '{args.directory}'")

    zip_total, zip_success, zip_fail = extract_zip_files(
        args.directory, args.no_confirm, stats
    )
    stats.total_zips = zip_total
    stats.successful_extractions = zip_success
    stats.failed_extractions = zip_fail

    # Apply standalone cleaning after ZIP extraction
    clean_result: Tuple[int, int] = clean_directory(args.directory, stats)
    files_cleaned, dirs_cleaned = clean_result
    stats.total_files_removed += files_cleaned
    stats.total_dirs_removed += dirs_cleaned

    # Reorganize directories
    stats.add_log(f"Reorganizing directories in '{args.directory}'")

    dir_total, dir_reorg, dir_ignored = reorganize_directories(
        args.directory, args.no_confirm, stats
    )
    stats.dirs_examined = dir_total
    stats.dirs_reorganized = dir_reorg
    stats.dirs_ignored = dir_ignored

    # Print summary
    stats.print_summary()
    if args.verbose:
        stats.print_logs(args.verbose)

    return 0


if __name__ == "__main__":
    sys.exit(main())
