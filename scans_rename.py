import re
import argparse
import shutil
from pathlib import Path
from typing import List, Tuple, Dict


def rename_japanese_timestamp_files(
    directory_path: Path, dry_run: bool = False
) -> List[Tuple[str, str]]:
    """
    Renames files in the specified directory that match the pattern
    'YYYYMMDD-HH時MM分SS秒-XXX.jpg' to 'YYYYMMDD-HHhMMmSSs-XXX.jpg'.

    Args:
        directory_path: Path to the directory containing files to rename
        dry_run: If True, only simulate the renaming without actually changing files

    Returns:
        List of tuples containing (original_name, new_name) of renamed files
    """
    # Regular expression to match the file format
    pattern = re.compile(r"^(\d{8}-\d{2})時(\d{2})分(\d{2})秒(-\d+\.jpg)$")

    renamed_files: List[Tuple[str, str]] = []

    # Process only files directly in the root directory (non-recursively)
    for file_path in directory_path.iterdir():
        # Skip directories and only process files
        if file_path.is_dir():
            continue

        # Check if the file matches our pattern
        match = pattern.match(file_path.name)
        if match:
            # Extract components
            date_hour = match.group(1)
            minutes = match.group(2)
            seconds = match.group(3)
            suffix = match.group(4)

            # Create the new filename
            new_filename = f"{date_hour}h{minutes}m{seconds}s{suffix}"
            new_file_path = file_path.with_name(new_filename)

            # Rename the file only if not in dry-run mode
            if not dry_run:
                file_path.rename(new_file_path)

            renamed_files.append((file_path.name, new_filename))

    return renamed_files


def organize_files_into_folders(
    directory_path: Path, dry_run: bool = False
) -> Dict[str, List[str]]:
    """
    For each file matching the pattern 'YYYYMMDD-HHhMMmSSs-XXX.jpg', creates a folder
    with the name 'YYYYMMDD-HHhMMmSSs' and moves the file into that folder.

    Args:
        directory_path: Path to the directory containing files to organize
        dry_run: If True, only simulate the organization without actually moving files

    Returns:
        Dictionary mapping folder names to lists of files moved into them
    """
    # Regular expression to match both original and renamed format
    pattern = re.compile(r"^(\d{8}-\d{2}[h時]\d{2}[m分]\d{2}[s秒])(-\d+\.jpg)$")

    # Keep track of which files go into which folders
    organized_files: Dict[str, List[str]] = {}

    # Process only files directly in the root directory (non-recursively)
    for file_path in directory_path.iterdir():
        # Skip directories and only process files
        if file_path.is_dir():
            continue

        # Check if the file matches our pattern
        match = pattern.match(file_path.name)
        if match:
            # Extract the prefix that will be the folder name
            folder_name = match.group(1)
            folder_path = directory_path / folder_name

            # Add file to tracking
            if folder_name not in organized_files:
                organized_files[folder_name] = []
            organized_files[folder_name].append(file_path.name)

            # Create folder and move file only if not in dry-run mode
            if not dry_run:
                # Create the folder if it doesn't exist
                folder_path.mkdir(exist_ok=True)

                # Move the file to the folder
                destination = folder_path / file_path.name
                shutil.move(str(file_path), str(destination))

    return organized_files


def main() -> None:
    """Parse arguments and execute file renaming and organization."""
    parser = argparse.ArgumentParser(
        description=(
            "Rename Japanese timestamp files and organize them into folders. "
            "Two operations are available: rename and organize. "
            "Renaming changes '時分秒' to 'hms'. Organization groups files into folders by their timestamp prefix."
        )
    )
    parser.add_argument(
        "-d", "--directory", type=Path, help="Directory containing files to process"
    )
    parser.add_argument(
        "-v",
        "--verbose",
        type=int,
        default=0,
        choices=[0, 1, 2],
        help="Verbosity level: 0=quiet, 1=summary, 2=details",
    )
    parser.add_argument(
        "-r",
        "--dry-run",
        action="store_true",
        help="Simulate operations without actually changing any files",
    )
    parser.add_argument(
        "-n",
        "--rename",
        action="store_true",
        help="Enable the file renaming step (Japanese '時分秒' to Latin 'hms')",
    )
    parser.add_argument(
        "-o",
        "--organize",
        action="store_true",
        help="Enable the file organization step (move files into timestamp-named folders)",
    )

    args = parser.parse_args()

    # If no directory is provided, use the current working directory
    if args.directory is None:
        args.directory = Path.cwd()
        if args.verbose >= 1:
            print(f"No directory specified, using current directory: {args.directory}")

    if not args.directory.is_dir():
        parser.error(f"'{args.directory}' is not a valid directory")

    # If no operation is specified, print help and exit
    if not (args.rename or args.organize):
        print("No operation specified. Please use --rename or --organize (or both).")
        parser.print_help()
        return

    # STEP 1: Rename files if requested
    if args.rename:
        renamed_files = rename_japanese_timestamp_files(args.directory, args.dry_run)

        if args.verbose >= 1:
            if renamed_files:
                if args.dry_run:
                    print(f"Dry run: {len(renamed_files)} files would be renamed.")
                else:
                    print(f"Successfully renamed {len(renamed_files)} files.")

                if args.verbose >= 2:
                    for old_name, new_name in renamed_files:
                        if args.dry_run:
                            print(f"  {old_name} → {new_name} (dry run)")
                        else:
                            print(f"  {old_name} → {new_name}")
            else:
                print("No matching files found to rename.")

    # STEP 2: Organize files into folders if requested
    if args.organize:
        organized_files = organize_files_into_folders(args.directory, args.dry_run)

        if args.verbose >= 1:
            if organized_files:
                total_files = sum(len(files) for files in organized_files.values())
                if args.dry_run:
                    print(
                        f"Dry run: {total_files} files would be organized into {len(organized_files)} folders."
                    )
                else:
                    print(
                        f"Successfully organized {total_files} files into {len(organized_files)} folders."
                    )

                if args.verbose >= 2:
                    for folder_name, files in organized_files.items():
                        print(f"  Folder: {folder_name}")
                        for file_name in files:
                            if args.dry_run:
                                print(
                                    f"    {file_name} → {folder_name}/{file_name} (dry run)"
                                )
                            else:
                                print(f"    {file_name} → {folder_name}/{file_name}")
            else:
                print("No matching files found to organize.")


if __name__ == "__main__":
    main()
