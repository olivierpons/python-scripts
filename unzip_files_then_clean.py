#!/usr/bin/env python3
"""
ZIP Extraction and Directory Reorganization Tool.

This script performs three main operations:
1. Extracts all ZIP files in a directory into corresponding subdirectories
2. Removes Apple system files (.DS_Store, .__MACOSX folders, etc.)
3. Reorganizes directories by moving single-child directories up one level

Example usage:
    $ python zip_reorganizer.py /path/to/directory
    $ python zip_reorganizer.py /path/to/directory --clean-only

Returns:
    0: Success
    1: Error (directory not found)
"""

import argparse
import os
import re
import shutil
import sys
import zipfile
from pathlib import Path
from typing import Dict, Generator, List, Literal, Optional, Set, Tuple, Union

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


def remove_apple_system_files(directory: Path) -> Tuple[int, int]:
    """
    Recursively remove Apple system files and directories from the given directory.

    Args:
        directory: Directory to clean.

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
                print(
                    f"  → Removing Apple system directory: {path.relative_to(directory)}"
                )
                try:
                    shutil.rmtree(path)
                    dirs_removed += 1
                except OSError as e:
                    print(f"  ⚠️ Failed to remove directory {path}: {e}")

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
                print(f"  → Removing Apple system file: {path.relative_to(directory)}")
                try:
                    path.unlink()
                    files_removed += 1
                except OSError as e:
                    print(f"  ⚠️ Failed to remove file {path}: {e}")

    return files_removed, dirs_removed


def extract_zip_files(source_dir: Path) -> Tuple[int, int, int]:
    """
    Extract all ZIP files in the source directory to corresponding subdirectories.

    This function iterates through all ZIP files in the source directory,
    creates a subdirectory with the same name (minus the .zip extension),
    and extracts the contents into that subdirectory. It also cleans up
    Apple system files during the extraction process.

    Args:
        source_dir: Directory containing ZIP files to extract.

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

        print(f"Processing: {zip_file.name}")
        print(f"  → Creating directory: {dest_dir}")

        # Handle existing directory
        if dest_dir.exists():
            print("  ⚠️ Destination directory already exists.")
            response: str = input("     Overwrite contents? (y/n): ").lower()
            if response != "y":
                print("  ❌ Operation cancelled for this file.")
                failure_count += 1
                print()
                continue

            # Clear existing directory
            print("  → Clearing existing directory...")
            try:
                shutil.rmtree(dest_dir)
            except OSError as e:
                print(f"  ❌ Failed to clear directory: {e}")
                failure_count += 1
                print()
                continue

        # Create destination directory
        try:
            dest_dir.mkdir(exist_ok=True)
        except OSError as e:
            print(f"  ❌ Failed to create directory: {e}")
            failure_count += 1
            print()
            continue

        # Extract ZIP file
        print("  → Extracting ZIP file...")
        try:
            with zipfile.ZipFile(zip_file, "r") as zip_ref:
                zip_ref.extractall(dest_dir)

            # Clean up any Apple system files that might have been extracted
            print("  → Cleaning up Apple system files...")
            files_removed, dirs_removed = remove_apple_system_files(dest_dir)
            if files_removed > 0 or dirs_removed > 0:
                print(
                    f"  ✓ Removed {files_removed} system files "
                    f"and {dirs_removed} system directories"
                )

            # Verify extraction
            extracted_files: int = sum(1 for _ in dest_dir.rglob("*") if _.is_file())
            if extracted_files > 0:
                print(f"  ✓ {extracted_files} file(s) extracted.")
                print("  → Removing original ZIP file...")
                try:
                    zip_file.unlink()
                    print("  ✅ ZIP file removed successfully.")
                    success_count += 1
                except OSError as e:
                    print(f"  ⚠️ Failed to remove ZIP file: {e}")
                    failure_count += 1
            else:
                print("  ❌ No files extracted (empty or corrupt ZIP).")
                failure_count += 1
        except (zipfile.BadZipFile, OSError) as e:
            print(f"  ❌ Extraction failed: {e}")
            failure_count += 1

        print()

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


def reorganize_directories(source_dir: Path) -> Tuple[int, int, int]:
    """
    Reorganize the directory structure by moving single-child directories up one level.

    This function identifies directories that contain exactly one subdirectory
    and no other files, then moves that subdirectory up to the parent level
    and removes the now-empty parent directory.

    Args:
        source_dir: Directory to reorganize.

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
        print(f"Examining directory: {parent_dir.name}")

        # First, clean any Apple system files in this directory
        files_removed, dirs_removed = remove_apple_system_files(parent_dir)
        if files_removed > 0 or dirs_removed > 0:
            print(
                f"  ✓ Removed {files_removed} system files and {dirs_removed} system directories"
            )

        # Now check for single child directories
        children: List[Path] = list(parent_dir.iterdir())
        dir_children: List[Path] = [child for child in children if child.is_dir()]

        print(f"  → Subdirectories: {len(dir_children)}")
        print(f"  → Total items: {len(children)}")

        if len(dir_children) == 1 and len(children) == 1:
            child_dir: Path = dir_children[0]
            print(f"  ✓ Contains single subdirectory: {child_dir.name}")

            target_path: Path = source_dir / child_dir.name

            # Handle existing directory
            if target_path.exists() and target_path != child_dir:
                print("  ⚠️ Directory with same name exists in target.")
                response: str = input("     Overwrite? (y/n): ").lower()
                if response != "y":
                    print("  ❌ Operation cancelled for this directory.")
                    ignored_count += 1
                    print()
                    continue

                print("  → Removing existing directory...")
                try:
                    shutil.rmtree(target_path)
                except OSError as e:
                    print(f"  ❌ Failed to remove existing directory: {e}")
                    ignored_count += 1
                    print()
                    continue

            # Move the directory
            print(f"  → Moving {child_dir.name} to parent directory...")
            try:
                shutil.move(str(child_dir), str(source_dir))
                print("  ✅ Directory moved successfully.")

                # Remove parent if empty
                remaining_items: List[Path] = list(parent_dir.iterdir())
                if not remaining_items:
                    try:
                        parent_dir.rmdir()
                        print("  ✅ Parent directory removed (empty).")
                        reorganized_count += 1
                    except OSError as e:
                        print(f"  ❌ Failed to remove parent directory: {e}")
                        ignored_count += 1
                else:
                    print(
                        f"  ⚠️ Parent not empty ({len(remaining_items)} items remaining)."
                    )
                    ignored_count += 1
            except OSError as e:
                print(f"  ❌ Failed to move directory: {e}")
                ignored_count += 1
        else:
            print("  ℹ️ No single subdirectory found - ignoring.")
            ignored_count += 1

        print()

    return total_processed, reorganized_count, ignored_count


def clean_directory(directory: Path) -> Tuple[int, int]:
    """
    Clean Apple system files from a directory recursively.

    Args:
        directory: Directory to clean.

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
    print(f"=== Cleaning Apple system files in '{directory}' ===")
    print()

    files_removed, dirs_removed = remove_apple_system_files(directory)

    print("=== Cleaning Summary ===")
    print(f"Files removed: {files_removed}")
    print(f"Directories removed: {dirs_removed}")
    print("=======================")
    print()

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
    default_text = "Y/n" if default else "y/N"
    response = input(f"{prompt} ({default_text}): ").lower()

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
    args = parser.parse_args()

    # Check if the directory exists
    if not args.directory.is_dir():
        print(f"Error: Directory '{args.directory}' does not exist.")
        return 1

    # Run in clean-only mode if requested
    if args.clean_only:
        clean_directory(args.directory)
        return 0

    # Process ZIP files
    print(f"=== Processing ZIP files in '{args.directory}' ===")
    print()
    zip_total, zip_success, zip_fail = extract_zip_files(args.directory)
    print("=== ZIP Processing Summary ===")
    print(f"Files processed: {zip_total}")
    print(f"Successful extractions: {zip_success}")
    print(f"Failed extractions: {zip_fail}")
    print("=============================")
    print()

    # Apply standalone cleaning after ZIP extraction
    files_removed, dirs_removed = clean_directory(args.directory)

    # Reorganize directories
    print(f"=== Reorganizing directories in '{args.directory}' ===")
    print()
    dir_total, dir_reorg, dir_ignored = reorganize_directories(args.directory)
    print("=== Reorganization Summary ===")
    print(f"Directories examined: {dir_total}")
    print(f"Reorganized: {dir_reorg}")
    print(f"Ignored: {dir_ignored}")
    print("=============================")

    return 0


if __name__ == "__main__":
    sys.exit(main())
