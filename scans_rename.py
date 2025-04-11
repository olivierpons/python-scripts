import re
import argparse
import shutil
from pathlib import Path
from PIL import Image
from PIL.Image import Resampling

# Supported image file extensions
SUPPORTED_IMAGE_EXTENSIONS = [".jpg", ".jpeg", ".tif", ".png", ".psd", ".cr2"]


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


def resize_image(
    img_path: Path,
    output_path: Path,
    max_pixels: int = 2000,
    jpeg_quality: int = 80,
    dry_run: bool = False,
    overwrite: bool = False,
) -> tuple[bool, bool]:
    """Resizes a single image file for web use.

    Args:
        img_path: Path to the source image file.
        output_path: Path where the resized image should be saved.
        max_pixels: Maximum width/height in pixels for the resized image.
        jpeg_quality: Quality of the JPEG compression (0-100, higher is better).
        dry_run: If True, only simulate the resizing without actually changing files.
        overwrite: If True, replace existing resized images.

    Returns:
        Tuple of (operation_successful, skipped). Both are True/False values.
    """
    # Skip if file exists and we're not overwriting
    if output_path.exists() and not overwrite:
        return False, True

    try:
        if not dry_run:
            # Open the image
            with Image.open(img_path) as img:
                # Calculate scaling ratio to maintain aspect ratio
                width, height = img.size
                ratio = min(max_pixels / width, max_pixels / height)
                new_width = int(width * ratio)
                new_height = int(height * ratio)

                # Resize the image
                resized_img = img.resize((new_width, new_height), Resampling.BICUBIC)

                # Save the image with specified quality
                resized_img.save(output_path, "JPEG", quality=jpeg_quality)
        return True, False
    except Exception as e:
        print(f"Error processing {img_path}: {e}")
        return False, False


def resize_images_for_web(
    directory_path: Path,
    max_pixels: int = 2000,
    jpeg_quality: int = 80,
    dry_run: bool = False,
    overwrite: bool = False,
) -> tuple[dict[str, list[str]], dict[str, list[str]]]:
    """Resizes images for web use.

    For each folder in the directory, creates a 'petites' subfolder and processes
    all images within the folder, resizing them while maintaining aspect ratio.

    Args:
        directory_path: Path to the directory containing image folders.
        max_pixels: Maximum width/height in pixels for the resized images.
        jpeg_quality: Quality of the JPEG compression (0-100, higher is better).
        dry_run: If True, only simulate the resizing without actually changing files.
        overwrite: If True, replace existing resized images.

    Returns:
        Tuple of (resized_files, skipped_files) dictionaries mapping folder names to
        lists of files.
    """
    resized_files: dict[str, list[str]] = {}
    skipped_files: dict[str, list[str]] = {}

    # Get only directories in the specified path (after organization step)
    folders = [f for f in directory_path.iterdir() if f.is_dir()]

    # Process each folder
    for folder in folders:
        # Skip any 'petites' folders that might already exist
        if folder.name == "petites":
            continue

        # Get all supported image files in the folder
        image_files = [
            f
            for f in folder.iterdir()
            if f.is_file() and f.suffix.lower() in SUPPORTED_IMAGE_EXTENSIONS
        ]

        # Skip if no files to resize
        if not image_files:
            continue

        # Track files for this folder
        folder_files = []
        folder_skipped = []

        # Create 'petites' subfolder only if there are images to process
        petites_folder = folder / "petites"
        if not dry_run:
            petites_folder.mkdir(exist_ok=True)

        # Process each image file
        for img_path in image_files:
            # Extract filename without extension
            output_filename = img_path.stem + ".jpg"
            output_path = petites_folder / output_filename

            resized, skipped = resize_image(
                img_path, output_path, max_pixels, jpeg_quality, dry_run, overwrite
            )

            if resized:
                folder_files.append(output_filename)
            elif skipped:
                folder_skipped.append(output_filename)

        # Add to tracking dictionaries if any files were processed or skipped
        if folder_files:
            resized_files[folder.name] = folder_files
        if folder_skipped:
            skipped_files[folder.name] = folder_skipped

    return resized_files, skipped_files


def verify_and_complete_resizing(
    directory_path: Path,
    max_pixels: int = 2000,
    jpeg_quality: int = 80,
    dry_run: bool = False,
    overwrite: bool = False,
) -> tuple[dict[str, list[str]], dict[str, list[str]]]:
    """Verifies that all timestamp folders have properly resized images.

    Finds all folders matching the timestamp format (YYYYMMDD-HHhMMmSSs) and checks
    if each image in these folders has been converted to the "petites" subfolder.
    If not, it creates the necessary resized versions.

    Args:
        directory_path: Path to the directory containing timestamp folders.
        max_pixels: Maximum width/height in pixels for the resized images.
        jpeg_quality: Quality of the JPEG compression (0-100, higher is better).
        dry_run: If True, only simulate the resizing without actually changing files.
        overwrite: If True, replace existing resized images.

    Returns:
        Tuple of (newly_resized_files, skipped_files) dictionaries mapping folder
        names to lists of files.
    """
    # Regular expression to match timestamp format folders
    timestamp_pattern: re.Pattern[str] = re.compile(r"^\d{8}-\d{2}h\d{2}m\d{2}s$")

    newly_resized_files: dict[str, list[str]] = {}
    skipped_files: dict[str, list[str]] = {}

    # Find all directories in the specified path
    for folder in directory_path.iterdir():
        if not folder.is_dir():
            continue

        # Check if folder name matches timestamp pattern
        if timestamp_pattern.match(folder.name):
            # Get all supported image files in the timestamp folder
            image_files = [
                f
                for f in folder.iterdir()
                if f.is_file() and f.suffix.lower() in SUPPORTED_IMAGE_EXTENSIONS
            ]

            if not image_files:
                continue

            # Track files for this folder
            folder_files = []
            folder_skipped = []

            # Create 'petites' subfolder only if needed
            petites_folder = folder / "petites"
            if not dry_run and not petites_folder.exists() and image_files:
                petites_folder.mkdir(exist_ok=True)

            # Process each image file
            for img_path in image_files:
                # Extract filename without extension
                output_filename = img_path.stem + ".jpg"
                output_path = petites_folder / output_filename

                resized, skipped = resize_image(
                    img_path,
                    output_path,
                    max_pixels,
                    jpeg_quality,
                    dry_run,
                    overwrite,
                )

                if resized:
                    folder_files.append(output_filename)
                elif skipped:
                    folder_skipped.append(output_filename)

            # Add to tracking dictionaries if any files were processed or skipped
            if folder_files:
                newly_resized_files[folder.name] = folder_files
            if folder_skipped:
                skipped_files[folder.name] = folder_skipped

    return newly_resized_files, skipped_files


def dry_run_status(text: str) -> str:
    """Add dry run indicator to text.

    Args:
        text: The text to append the dry run indicator to

    Returns:
        Text with dry run indicator appended
    """
    return f"{text} (dry run)"


def print_file_operation(
    old_path: str, new_path: str, dry_run: bool, indent: int = 0
) -> None:
    """Print a file operation with consistent formatting.

    Args:
        old_path: The original file path
        new_path: The new file path
        dry_run: Whether this is a dry run
        indent: Number of spaces to indent (default: 0)
    """
    indentation = " " * indent
    operation = f"{indentation}{old_path} → {new_path}"
    if dry_run:
        operation = dry_run_status(operation)
    print(operation)


def main() -> None:
    """Parse command-line arguments and execute file operations.

    Handles parsing arguments for main operations:
    1. Rename: Convert Japanese timestamp characters to Latin characters
    2. Organize: Group files into folders based on timestamp prefix
    3. Resize: Resize images for web use and check for missing resized images

    Each operation can be enabled independently with command-line flags.
    """
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description=(
            "Rename Japanese timestamp files, organize them into folders, and "
            "resize for web. Three operations are available: rename, organize, "
            "and resize. Renaming changes '時分秒' to 'hms'. Organization groups files "
            "into folders by their timestamp prefix. Resize creates smaller versions "
            "of images for web use and checks existing timestamp folders for missing "
            "resized images."
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
        help="Enable the file organization step (move files into timestamp-named "
        "folders)",
    )
    parser.add_argument(
        "-z",
        "--resize",
        action="store_true",
        help="Enable the image resizing step (including checking for missing resizes)",
    )
    parser.add_argument(
        "-m",
        "--max-pixels",
        type=int,
        default=2000,
        help=f"Maximum size in pixels for the resized images (default: 2000)",
    )
    parser.add_argument(
        "-q",
        "--quality",
        type=int,
        default=80,
        choices=range(70, 101),
        help="JPEG quality for resized images (70-100, default: 80)",
    )
    parser.add_argument(
        "-w",
        "--overwrite",
        action="store_true",
        help="Overwrite existing resized images",
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
            "No operation specified. Please use --rename, --organize, or --resize "
            "(or any combination)."
        )
        # Show supported file extensions
        print(f"Supported image extensions: {', '.join(SUPPORTED_IMAGE_EXTENSIONS)}")
        parser.print_help()
        return

    # STEP 1: Rename files if requested
    if args.rename:
        renamed_files: list[tuple[str, str]] = rename_japanese_timestamp_files(
            args.directory, args.dry_run
        )
        if args.verbose >= 1:
            if renamed_files:
                operation_text = f"Successfully renamed {len(renamed_files)} files."
                if args.dry_run:
                    operation_text = (
                        f"Dry run: {len(renamed_files)} files would be renamed."
                    )
                print(operation_text)

                if args.verbose >= 2:
                    for old_name, new_name in renamed_files:
                        print_file_operation(old_name, new_name, args.dry_run, indent=2)
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
                operation_text = (
                    f"{'Dry run: ' if args.dry_run else ''}"
                    f"{'Would organize' if args.dry_run else 'Successfully organized'} "
                    f"{total_files} files into {len(organized_files)} folders."
                )
                print(operation_text)

                if args.verbose >= 2:
                    for folder_name, files in organized_files.items():
                        print(f"  Folder: {folder_name}")
                        for file_name in files:
                            print_file_operation(
                                file_name,
                                f"{folder_name}/{file_name}",
                                args.dry_run,
                                indent=4,
                            )
            else:
                print("No matching files found to organize.")

    # STEP 3: Resize images if requested
    if args.resize:
        # First resize newly organized images
        resize_result = resize_images_for_web(
            args.directory,
            args.max_pixels,
            args.quality,
            args.dry_run,
            args.overwrite,
        )
        resized_files, skipped_files = resize_result

        # Then check for and complete any missing resized images in timestamp folders
        verify_result = verify_and_complete_resizing(
            args.directory,
            args.max_pixels,
            args.quality,
            args.dry_run,
            args.overwrite,
        )
        newly_resized_files, newly_skipped_files = verify_result

        # Combine results for reporting
        total_resized_folders = len(resized_files) + len(newly_resized_files)
        total_resized_files = sum(len(files) for files in resized_files.values()) + sum(
            len(files) for files in newly_resized_files.values()
        )

        # Combine skipped files for reporting
        all_skipped_files = {}
        for folder, files in skipped_files.items():
            all_skipped_files[folder] = files
        for folder, files in newly_skipped_files.items():
            if folder in all_skipped_files:
                all_skipped_files[folder].extend(files)
            else:
                all_skipped_files[folder] = files

        total_skipped_folders = len(all_skipped_files)
        total_skipped_files = sum(len(files) for files in all_skipped_files.values())

        if args.verbose >= 1:
            if total_resized_files > 0:
                operation_text = (
                    f"{'Dry run: ' if args.dry_run else ''}"
                    f"{'Would resize' if args.dry_run else 'Successfully resized'} "
                    f"{total_resized_files} files in {total_resized_folders} folders."
                )
                print(operation_text)

                if args.verbose >= 2:
                    # Report on regular resize operations
                    for folder_name, files in resized_files.items():
                        print(f"  Folder: {folder_name}")
                        print(f"    {len(files)} files resized to 'petites' subfolder")
                        if args.verbose > 2:  # Extra verbose level for file details
                            for file_name in files:
                                print_file_operation(
                                    file_name,
                                    f"petites/{file_name}",
                                    args.dry_run,
                                    indent=6,
                                )

                    # Report on verification resize operations
                    for folder_name, files in newly_resized_files.items():
                        print(f"  Folder: {folder_name} (missing files)")
                        print(
                            f"    {len(files)} missing files resized to 'petites' "
                            f"subfolder"
                        )
                        if args.verbose > 2:  # Extra verbose level for file details
                            for file_name in files:
                                print_file_operation(
                                    file_name,
                                    f"petites/{file_name}",
                                    args.dry_run,
                                    indent=6,
                                )
            else:
                print("No files found to resize.")

            # Report skipped files
            if total_skipped_files > 0:
                skipped_text = (
                    f"Skipped {total_skipped_files} existing files in "
                    f"{total_skipped_folders} folders."
                )
                print(skipped_text)

                if args.verbose >= 2:
                    for folder_name, files in all_skipped_files.items():
                        print(f"  Folder: {folder_name}")
                        print(
                            f"    {len(files)} files already exist in 'petites' "
                            f"subfolder"
                        )
                        if args.verbose > 2:  # Extra verbose level for file details
                            for file_name in files:
                                print(f"      {file_name} (already exists)")
            elif not args.overwrite:
                print("No existing files found to skip.")


if __name__ == "__main__":
    main()
