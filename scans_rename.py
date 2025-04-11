import re
import argparse
import shutil
from pathlib import Path
from PIL import Image


def rename_japanese_timestamp_files(
    directory_path: Path, dry_run: bool = False
) -> list[tuple[str, str]]:
    """Renames files with Japanese timestamps to use Latin characters.

    Renames files in the specified directory that match the pattern
    'YYYYMMDD-HH時MM分SS秒-XXX.jpg' to 'YYYYMMDD-HHhMMmSSs-XXX.jpg'.

    Args:
        directory_path: Path to the directory containing files to rename.
        dry_run: If True, only simulate the renaming without actually changing files.

    Returns:
        List of tuples containing (original_name, new_name) of renamed files.
    """
    # Regular expression to match the file format
    pattern: re.Pattern[str] = re.compile(
        r"^(\d{8}-\d{2})時(\d{2})分(\d{2})秒(-\d+\.jpg)$"
    )
    renamed_files: list[tuple[str, str]] = []

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
) -> dict[str, list[str]]:
    """Organizes timestamp-named files into corresponding folders.

    For each file matching the pattern 'YYYYMMDD-HHhMMmSSs-XXX.jpg', creates a folder
    with the name 'YYYYMMDD-HHhMMmSSs' and moves the file into that folder.

    Args:
        directory_path: Path to the directory containing files to organize.
        dry_run: If True, only simulate the organization without actually moving files.

    Returns:
        Dictionary mapping folder names to lists of files moved into them.
    """
    # Regular expression to match both original and renamed format
    pattern: re.Pattern[str] = re.compile(
        r"^(\d{8}-\d{2}[h時]\d{2}[m分]\d{2}[s秒])(-\d+\.jpg)$"
    )

    # Keep track of which files go into which folders
    organized_files: dict[str, list[str]] = {}

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


def resize_images_for_web(
    directory_path: Path,
    max_pixels: int = 400,
    jpeg_quality: int = 80,
    dry_run: bool = False,
) -> dict[str, list[str]]:
    """Resizes images for web use.

    For each folder in the directory, creates a 'petites' subfolder and processes
    all images within the folder, resizing them while maintaining aspect ratio.

    Args:
        directory_path: Path to the directory containing image folders.
        max_pixels: Maximum width/height in pixels for the resized images.
        jpeg_quality: Quality of the JPEG compression (0-100, higher is better).
        dry_run: If True, only simulate the resizing without actually changing files.

    Returns:
        Dictionary mapping folder names to lists of resized files.
    """
    resized_files: dict[str, list[str]] = {}

    # Get only directories in the specified path (after organization step)
    folders = [f for f in directory_path.iterdir() if f.is_dir()]

    # Process each folder
    for folder in folders:
        # Skip any 'petites' folders that might already exist
        if folder.name == "petites":
            continue

        # Create 'petites' subfolder
        petites_folder = folder / "petites"
        if not dry_run:
            petites_folder.mkdir(exist_ok=True)

        # Track files for this folder
        folder_files = []

        # Get all supported image files in the folder
        image_files = [
            f
            for f in folder.iterdir()
            if f.is_file()
            and f.suffix.lower() in [".jpg", ".jpeg", ".tif", ".png", ".psd", ".cr2"]
        ]

        # Process each image file
        for img_path in image_files:
            try:
                # Extract filename without extension
                output_filename = img_path.stem + ".jpg"
                output_path = petites_folder / output_filename

                if not dry_run:
                    # Open the image
                    with Image.open(img_path) as img:
                        # Calculate scaling ratio to maintain aspect ratio
                        width, height = img.size
                        ratio = min(max_pixels / width, max_pixels / height)
                        new_width = int(width * ratio)
                        new_height = int(height * ratio)

                        # Resize the image
                        resized_img = img.resize((new_width, new_height), Image.BICUBIC)

                        # Save the image with specified quality
                        resized_img.save(output_path, "JPEG", quality=jpeg_quality)

                # Track the resized file
                folder_files.append(output_filename)

            except Exception as e:
                print(f"Error processing {img_path}: {e}")
                continue

        # Add to tracking dictionary if any files were processed
        if folder_files:
            resized_files[folder.name] = folder_files

    return resized_files


def main() -> None:
    """Parse command-line arguments and execute file operations.

    Handles parsing arguments for three main operations:
    1. Rename: Convert Japanese timestamp characters to Latin characters
    2. Organize: Group files into folders based on timestamp prefix
    3. Resize: Resize images for web use

    Each operation can be enabled independently with command-line flags.
    """
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description=(
            "Rename Japanese timestamp files, organize them into folders, and resize for web. "
            "Three operations are available: rename, organize, and resize. "
            "Renaming changes '時分秒' to 'hms'. Organization groups files into folders by their timestamp prefix. "
            "Resize creates smaller versions of images for web use."
        )
    )
    parser.add_argument(
        "-d",
        "--directory",
        type=Path,
        help="Directory containing files to process",
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
    parser.add_argument(
        "-z",
        "--resize",
        action="store_true",
        help="Enable the image resizing step",
    )
    parser.add_argument(
        "-m",
        "--max-pixels",
        type=int,
        default=400,
        help="Maximum size in pixels for the resized images (default: 400)",
    )
    parser.add_argument(
        "-q",
        "--quality",
        type=int,
        default=80,
        choices=range(70, 101),
        help="JPEG quality for resized images (1-100, default: 80)",
    )

    args: argparse.Namespace = parser.parse_args()

    # If no directory is provided, use the current working directory
    if args.directory is None:
        args.directory = Path.cwd()
        if args.verbose >= 1:
            print(f"No directory specified, using current directory: {args.directory}")

    if not args.directory.is_dir():
        parser.error(f"'{args.directory}' is not a valid directory")

    # If no operation is specified, print help and exit
    if not (args.rename or args.organize or args.resize):
        print(
            "No operation specified. Please use --rename, --organize, or --resize (or any combination)."
        )
        parser.print_help()
        return

    # STEP 1: Rename files if requested
    if args.rename:
        renamed_files: list[tuple[str, str]] = rename_japanese_timestamp_files(
            args.directory, args.dry_run
        )
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
        organized_files: dict[str, list[str]] = organize_files_into_folders(
            args.directory, args.dry_run
        )
        if args.verbose >= 1:
            if organized_files:
                total_files: int = sum(len(files) for files in organized_files.values())
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

    # STEP 3: Resize images if requested
    if args.resize:
        resized_files: dict[str, list[str]] = resize_images_for_web(
            args.directory, args.max_pixels, args.quality, args.dry_run
        )
        if args.verbose >= 1:
            if resized_files:
                total_files: int = sum(len(files) for files in resized_files.values())
                if args.dry_run:
                    print(
                        f"Dry run: {total_files} files would be resized in {len(resized_files)} folders."
                    )
                else:
                    print(
                        f"Successfully resized {total_files} files in {len(resized_files)} folders."
                    )
                if args.verbose >= 2:
                    for folder_name, files in resized_files.items():
                        print(f"  Folder: {folder_name}")
                        print(f"    {len(files)} files resized to 'petites' subfolder")
                        if args.verbose > 2:  # Extra verbose level for file details
                            for file_name in files:
                                if args.dry_run:
                                    print(
                                        f"      {file_name} → petites/{file_name} (dry run)"
                                    )
                                else:
                                    print(f"      {file_name} → petites/{file_name}")
            else:
                print("No matching files found to resize.")


if __name__ == "__main__":
    main()
