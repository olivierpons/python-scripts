#!/usr/bin/env python3
"""
ZIP Extraction and Directory Reorganization Tool

This script performs two main operations:
1. Extracts all ZIP files in a directory into corresponding subdirectories
2. Reorganizes directories by moving single-child directories up one level

Example usage:
    $ python zip_reorganizer.py /path/to/directory
"""

import argparse
import os
import shutil
import stat
import zipfile
from pathlib import Path
from typing import Generator, Literal, Optional, Tuple


def extract_zip_files(source_dir: Path) -> Tuple[int, int, int]:
    """
    Extract all ZIP files in the source directory to corresponding subdirectories.

    Args:
        source_dir: Directory containing ZIP files to extract

    Returns:
        Tuple containing:
        - total_processed: Total ZIP files found
        - success_count: Successfully extracted ZIP files
        - failure_count: Failed extractions

    Example:
        >>> extract_zip_files(Path("/data/zips"))
        (10, 8, 2)  # Processed 10, 8 success, 2 failures
    """
    total_processed = 0
    success_count = 0
    failure_count = 0

    for zip_file in source_dir.glob("*.zip"):
        total_processed += 1
        dest_dir = source_dir / zip_file.stem

        print(f"Processing: {zip_file.name}")
        print(f"  → Creating directory: {dest_dir}")

        # Handle existing directory
        if dest_dir.exists():
            print("  ⚠️ Destination directory already exists.")
            response = input("     Overwrite contents? (y/n): ").lower()
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
            
            # Verify extraction
            extracted_files = sum(1 for _ in dest_dir.rglob("*") if _.is_file())
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
        root_dir: Directory to search for single-child directories

    Yields:
        Tuples of (parent_dir, child_dir) for each single-child directory found

    Example:
        >>> list(find_single_child_dirs(Path("/data")))
        [(Path("/data/dir1"), Path("/data/dir1/subdir"))]
    """
    for parent_dir in root_dir.iterdir():
        if not parent_dir.is_dir():
            continue

        children = list(parent_dir.iterdir())
        dir_children = [child for child in children if child.is_dir()]

        if len(dir_children) == 1 and len(children) == 1:
            yield parent_dir, dir_children[0]


def reorganize_directories(source_dir: Path) -> Tuple[int, int, int]:
    """
    Reorganize directory structure by moving single-child directories up one level.

    Args:
        source_dir: Directory to reorganize

    Returns:
        Tuple containing:
        - total_processed: Total directories examined
        - reorganized_count: Successfully reorganized directories
        - ignored_count: Directories left unchanged

    Example:
        >>> reorganize_directories(Path("/data"))
        (15, 8, 7)  # 15 examined, 8 reorganized, 7 ignored
    """
    total_processed = 0
    reorganized_count = 0
    ignored_count = 0

    for parent_dir in source_dir.iterdir():
        if not parent_dir.is_dir():
            continue

        total_processed += 1
        print(f"Examining directory: {parent_dir.name}")

        children = list(parent_dir.iterdir())
        dir_children = [child for child in children if child.is_dir()]

        print(f"  → Subdirectories: {len(dir_children)}")
        print(f"  → Total items: {len(children)}")

        if len(dir_children) == 1 and len(children) == 1:
            child_dir = dir_children[0]
            print(f"  ✓ Contains single subdirectory: {child_dir.name}")

            target_path = source_dir / child_dir.name

            # Handle existing directory
            if target_path.exists() and target_path != child_dir:
                print("  ⚠️ Directory with same name exists in target.")
                response = input("     Overwrite? (y/n): ").lower()
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
                remaining_items = list(parent_dir.iterdir())
                if not remaining_items:
                    try:
                        parent_dir.rmdir()
                        print("  ✅ Parent directory removed (empty).")
                        reorganized_count += 1
                    except OSError as e:
                        print(f"  ❌ Failed to remove parent directory: {e}")
                        ignored_count += 1
                else:
                    print(f"  ⚠️ Parent not empty ({len(remaining_items)} items remaining).")
                    ignored_count += 1
            except OSError as e:
                print(f"  ❌ Failed to move directory: {e}")
                ignored_count += 1
        else:
            print("  ℹ️ No single subdirectory found - ignoring.")
            ignored_count += 1

        print()

    return total_processed, reorganized_count, ignored_count


def main() -> Literal[0, 1]:
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description="Extract ZIP files and reorganize directory structure."
    )
    parser.add_argument(
        "directory",
        type=Path,
        help="Directory containing ZIP files to process"
    )
    args = parser.parse_args()

    if not args.directory.is_dir():
        print(f"Error: Directory '{args.directory}' does not exist.")
        return 1

    print(f"=== Processing ZIP files in '{args.directory}' ===")
    print()
    zip_total, zip_success, zip_fail = extract_zip_files(args.directory)
    print("=== ZIP Processing Summary ===")
    print(f"Files processed: {zip_total}")
    print(f"Successful extractions: {zip_success}")
    print(f"Failed extractions: {zip_fail}")
    print("=============================")
    print()

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
    raise SystemExit(main())
