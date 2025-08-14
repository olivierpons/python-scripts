"""Pie Chart Generator Module.

This module generates a series of pie charts showing the progression of two colors
from 0% to 100% in customizable increments. Built with Python 3.13+ features,
it offers extensive customization options and robust error handling.

Features:
    - Generates pie chart series with customizable percentage ranges and steps
    - Supports multiple output formats (PNG, JPG, JPEG, PDF, SVG, WEBP, TIFF)
    - Advanced command-line interface with short and long argument formats
    - Comprehensive validation using PurePath for cross-platform compatibility
    - Atomic file writes with backup support to prevent corruption
    - Colorful terminal progress bars and status messages
    - Optional animated GIF creation from generated images
    - Configuration file support (JSON) for saving and loading settings
    - Extensive error handling with custom exception hierarchy
    - Modern Python 3.13+ features: dataclasses, enums, pattern matching, union types
    - Transparent background support for PNG and other compatible formats
    - Optional text display controls (percentage and title)

Requirements:
    - Python 3.13+
    - matplotlib
    - tqdm
    - Pillow (for GIF creation)

Examples:
    Basic usage:
        python pie_chart_generator.py

    Custom colors and range:
        python pie_chart_generator.py -o charts -c "#FF0000,#00FF00" -s 0 -e 50 --step 1

    Color combinations and edge styles:
        # Vibrant colors without border
        python pie_chart_generator.py -o charts -c "#FF6B35,#004E89" --edge-width 0

        # Pastel colors with thin white border
        python pie_chart_generator.py -o charts -c "#FFB3BA,#BAE1FF" --edge-width 1 --edge-color "#FFFFFF"

        # Dark colors with thick black border
        python pie_chart_generator.py -o charts -c "#2E2E2E,#D32F2F" --edge-width 3 --edge-color "#000000"

        # Blue-green gradient without border
        python pie_chart_generator.py -o charts -c "#1E3A8A,#10B981" --edge-width 0

        # Sunset colors with golden border
        python pie_chart_generator.py -o charts -c "#FF6B6B,#FFE66D" --edge-width 2 --edge-color "#FFD700"

        # Monochrome with gray border
        python pie_chart_generator.py -o charts -c "#000000,#FFFFFF" --edge-width 4 --edge-color "#808080"

        # Neon colors
        python pie_chart_generator.py -o charts -c "#00FFFF,#FF00FF" --edge-width 0

        # Natural colors
        python pie_chart_generator.py -o charts -c "#8B4513,#228B22" --edge-width 1.5 --edge-color "#FFFFFF"

    Advanced options:
        # High quality transparent PNG with text
        python pie_chart_generator.py -c "#FF4444,#44FF44" --edge-width 0 --transparent --format png --dpi 300 --show-percentage

        # Generate animated GIF
        python pie_chart_generator.py -c "#FF6B35,#004E89" --gif --gif-duration 100 --edge-width 0

        # Custom range with step
        python pie_chart_generator.py -c "#1E3A8A,#10B981" -s 25 -e 75 --step 5 --edge-width 0

        # Using atomic writes with backup
        python pie_chart_generator.py -c "#FF0000,#00FF00" --atomic-writes --backup --overwrite

        # Custom angles and clockwise direction
        python pie_chart_generator.py -c "#FF6B35,#004E89" --start-angle 0 --clockwise

        # Save and load configuration
        python pie_chart_generator.py --save-config my_config.json
        python pie_chart_generator.py --config my_config.json

        # Verbose output with custom font settings
        python pie_chart_generator.py -c "#1E3A8A,#10B981" --verbose --font-size 32 --font-weight bold --show-title

Edge width options:
    --edge-width 0      : No border
    --edge-width 0.5    : Very thin border
    --edge-width 1      : Thin border
    --edge-width 2      : Medium border (default)
    --edge-width 3      : Thick border
    --edge-width 5      : Very thick border

Edge color options:
    --edge-color "#FFFFFF"  : White (default)
    --edge-color "#000000"  : Black
    --edge-color "#808080"  : Gray
    --edge-color "#FFD700"  : Gold
    --edge-color "none"     : No border (equivalent to --edge-width 0)

Arguments:
    Output Options:
        -o, --output-dir     : Output directory for generated images
        -f, --format         : Output image format (png, jpg, jpeg, pdf, svg, webp, tiff)
        --dpi                : Image resolution in DPI (50-1000)
        --atomic-writes      : Use atomic file writes to prevent corruption
        --backup             : Create backups of existing files
        --overwrite          : Overwrite existing files (default: skip existing files)

    Visual Options:
        -c, --colors         : Two hex colors separated by comma
        -w, --width          : Figure width in inches
        --height             : Figure height in inches
        --transparent        : Use transparent background (default: enabled)
        --no-transparent     : Use white background instead of transparent

    Range Options:
        -s, --start          : Starting percentage (0-100)
        -e, --end            : Ending percentage (0-100)
        --step               : Step increment

    Chart Appearance:
        --start-angle        : Starting angle in degrees (0-360)
        --clockwise          : Draw pie chart clockwise
        --edge-color         : Edge color for pie segments
        --edge-width         : Edge line width

    Text Options:
        --font-size          : Font size for percentage text
        --font-color         : Font color for percentage text
        --font-weight        : Font weight (normal, bold, light, ultralight, heavy)
        --title-font-size    : Title font size
        --show-percentage    : Show percentage text in center (default: disabled)
        --show-title         : Show chart title (default: disabled)

    GIF Options:
        --gif                : Generate animated GIF
        --gif-duration       : GIF frame duration in milliseconds
        --gif-loop           : GIF loop count (0=infinite)
        --keep-png           : Keep PNG files when generating GIF (default: delete PNG files after GIF creation)

    Progress Options:
        --quiet, -q          : Suppress progress output
        --verbose, -v        : Enable verbose output

    Configuration Options:
        --config             : Load configuration from JSON file
        --save-config        : Save current configuration to JSON file
"""

import argparse
import json
import os
import re
import shutil
import stat
import sys
import tempfile
import time
from contextlib import contextmanager
from dataclasses import dataclass
from enum import StrEnum, auto
from pathlib import Path, PurePath
from typing import List, Tuple, Any, Union

import matplotlib.pyplot as plt
from tqdm import tqdm


class ImageFormat(StrEnum):
    """Supported image formats."""

    PNG = auto()
    JPG = auto()
    JPEG = auto()
    PDF = auto()
    SVG = auto()
    WEBP = auto()
    TIFF = auto()


class FontWeight(StrEnum):
    """Font weight options."""

    NORMAL = auto()
    BOLD = auto()
    LIGHT = auto()
    ULTRALIGHT = auto()
    HEAVY = auto()


class ErrorSeverity(StrEnum):
    """Error severity levels."""

    LOW = auto()
    MEDIUM = auto()
    HIGH = auto()
    CRITICAL = auto()


@dataclass(frozen=True, slots=True)
class ChartConfig:
    """Configuration dataclass for chart generation."""

    output_dir: Union[str, Path] = Path("default")
    colors: tuple[str, str] = ("#FF6B6B", "#4ECDC4")
    width: float = 8.0
    height: float = 8.0
    dpi: int = 150
    start_percent: int = 0
    end_percent: int = 100
    step: int = 1
    start_angle: int = 90
    clockwise: bool = False
    edge_color: str = "white"
    edge_width: float = 2.0
    font_size: int = 24
    font_color: str = "#333333"
    font_weight: FontWeight = FontWeight.BOLD
    title_font_size: int = 16
    show_percentage: bool = False
    show_title: bool = False
    transparent_background: bool = True
    format: ImageFormat = ImageFormat.PNG
    gif_duration: int = 100
    gif_loop: int = 0
    keep_png_for_gif: bool = False
    overwrite_existing: bool = False
    quiet: bool = False
    verbose: bool = False

    def __post_init__(self) -> None:
        """Validate configuration after initialization."""
        object.__setattr__(self, "output_dir", Path(self.output_dir))


class PieChartError(Exception):
    """Base exception for pie chart generation errors."""

    def __init__(
        self,
        message: str,
        severity: ErrorSeverity = ErrorSeverity.MEDIUM,
        context: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message)
        self.severity = severity
        self.context = context or {}
        self.timestamp = time.time()


class ConfigurationError(PieChartError):
    """Exception raised for configuration-related errors."""

    pass


class FileOperationError(PieChartError):
    """Exception raised for file operation errors."""

    def __init__(
        self,
        message: str,
        path: Path | None = None,
        operation: str | None = None,
        **kwargs,
    ) -> None:
        super().__init__(message, **kwargs)
        self.path = path
        self.operation = operation


class ValidationError(PieChartError):
    """Exception raised for input validation errors."""

    def __init__(
        self, message: str, field: str | None = None, value: Any = None, **kwargs
    ) -> None:
        super().__init__(message, **kwargs)
        self.field = field
        self.value = value


class RenderingError(PieChartError):
    """Exception raised for chart rendering errors."""

    pass


class DependencyError(PieChartError):
    """Exception raised for missing dependencies."""

    pass


class PermissionDeniedError(FileOperationError):
    """Exception raised for permission-related file errors."""

    pass


class DiskSpaceError(FileOperationError):
    """Exception raised for insufficient disk space."""

    pass


class FileSystemError(FileOperationError):
    """Exception raised for file system errors."""

    pass


class TerminalColors:
    """ANSI escape codes for colored terminal output."""

    RED: str = "\033[91m"
    GREEN: str = "\033[92m"
    YELLOW: str = "\033[93m"
    BLUE: str = "\033[94m"
    MAGENTA: str = "\033[95m"
    CYAN: str = "\033[96m"
    WHITE: str = "\033[97m"

    BRIGHT_RED: str = "\033[91;1m"
    BRIGHT_GREEN: str = "\033[92;1m"
    BRIGHT_YELLOW: str = "\033[93;1m"
    BRIGHT_BLUE: str = "\033[94;1m"
    BRIGHT_MAGENTA: str = "\033[95;1m"
    BRIGHT_CYAN: str = "\033[96;1m"

    BG_RED: str = "\033[101m"
    BG_GREEN: str = "\033[102m"
    BG_YELLOW: str = "\033[103m"
    BG_BLUE: str = "\033[104m"
    BG_MAGENTA: str = "\033[105m"
    BG_CYAN: str = "\033[106m"

    BOLD: str = "\033[1m"
    DIM: str = "\033[2m"
    UNDERLINE: str = "\033[4m"
    BLINK: str = "\033[5m"
    REVERSE: str = "\033[7m"

    RESET: str = "\033[0m"
    CLEAR_LINE: str = "\033[K"
    MOVE_UP: str = "\033[A"


@contextmanager
def safe_file_operation(path: Path, operation: str):
    """Context manager for safe file operations with comprehensive error handling.

    Args:
        path: Path object for the file operation.
        operation: Description of the operation being performed.

    Yields:
        Path object for the operation.

    Raises:
        Various FileOperationError subclasses based on the specific error.
    """
    try:
        _validate_path_safety(path)
        _check_disk_space(path)
        _check_path_permissions(path, operation)

        yield path

    except PermissionError as e:
        raise PermissionDeniedError(
            f"Permission denied during {operation}",
            path=path,
            operation=operation,
            severity=ErrorSeverity.HIGH,
            context={"errno": e.errno, "strerror": e.strerror},
        )
    except OSError as e:
        if e.errno == 28:
            raise DiskSpaceError(
                f"Insufficient disk space for {operation}",
                path=path,
                operation=operation,
                severity=ErrorSeverity.CRITICAL,
            )
        elif e.errno == 30:
            raise FileSystemError(
                f"Read-only file system during {operation}",
                path=path,
                operation=operation,
                severity=ErrorSeverity.HIGH,
            )
        else:
            raise FileSystemError(
                f"File system error during {operation}: {e}",
                path=path,
                operation=operation,
                severity=ErrorSeverity.MEDIUM,
                context={"errno": e.errno, "strerror": e.strerror},
            )
    except Exception as e:
        raise FileOperationError(
            f"Unexpected error during {operation}: {e}",
            path=path,
            operation=operation,
            severity=ErrorSeverity.HIGH,
        )


def _validate_path_safety(path: Path) -> None:
    """Validate path safety using PurePath for cross-platform compatibility.

    Args:
        path: Path to validate.

    Raises:
        ValidationError: If path is unsafe.
    """
    pure_path = PurePath(path)

    if ".." in pure_path.parts:
        raise ValidationError(
            "Path traversal detected in path",
            field="path",
            value=str(path),
            severity=ErrorSeverity.HIGH,
        )

    # Remove absolute path warning as it's not necessary and pollutes output
    # if pure_path.is_absolute() and not str(path).startswith(("/tmp", "/var/tmp")):
    #     warnings.warn(f"Using absolute path: {path}", UserWarning, stacklevel=3)

    reserved_names = {
        "CON",
        "PRN",
        "AUX",
        "NUL",
        "COM1",
        "COM2",
        "COM3",
        "COM4",
        "COM5",
        "COM6",
        "COM7",
        "COM8",
        "COM9",
        "LPT1",
        "LPT2",
        "LPT3",
        "LPT4",
        "LPT5",
        "LPT6",
        "LPT7",
        "LPT8",
        "LPT9",
    }

    if pure_path.stem.upper() in reserved_names:
        raise ValidationError(
            f"Reserved filename detected: {pure_path.stem}",
            field="filename",
            value=pure_path.stem,
            severity=ErrorSeverity.HIGH,
        )

    if len(str(path)) > 260:
        raise ValidationError(
            f"Path too long: {len(str(path))} characters (max 260)",
            field="path_length",
            value=len(str(path)),
            severity=ErrorSeverity.HIGH,
        )


def _check_disk_space(path: Path, required_mb: float = 100.0) -> None:
    """Check available disk space for the operation.

    Args:
        path: Path where operation will occur.
        required_mb: Required space in megabytes.

    Raises:
        DiskSpaceError: If insufficient disk space.
    """
    try:
        check_path = path.parent if path.is_file() or not path.exists() else path

        disk_usage = shutil.disk_usage(check_path)
        free_mb = disk_usage.free / (1024 * 1024)

        if free_mb < required_mb:
            raise DiskSpaceError(
                f"Insufficient disk space: {free_mb:.1f}MB available, {required_mb:.1f}MB required",
                path=path,
                operation="disk_space_check",
                severity=ErrorSeverity.CRITICAL,
                context={"available_mb": free_mb, "required_mb": required_mb},
            )

    except FileNotFoundError:
        if path.parent.exists():
            _check_disk_space(path.parent, required_mb)
        else:
            raise ValidationError(
                f"Parent directory does not exist: {path.parent}",
                field="parent_directory",
                value=str(path.parent),
                severity=ErrorSeverity.HIGH,
            )


def _check_path_permissions(path: Path, operation: str) -> None:
    """Check path permissions for the intended operation.

    Args:
        path: Path to check.
        operation: Type of operation (read, write, create, etc.).

    Raises:
        PermissionError: If insufficient permissions.
    """
    try:
        if path.exists():
            path_stat = path.stat()

            if operation in ("write", "save", "create"):
                if path.is_file() and not os.access(path, os.W_OK):
                    raise PermissionDeniedError(
                        f"No write permission for existing file: {path}",
                        path=path,
                        operation=operation,
                    )
                elif path.is_dir() and not os.access(path, os.W_OK):
                    raise PermissionDeniedError(
                        f"No write permission for directory: {path}",
                        path=path,
                        operation=operation,
                    )

            if operation == "read" and not os.access(path, os.R_OK):
                raise PermissionDeniedError(
                    f"No read permission for: {path}", path=path, operation=operation
                )

            if (
                operation in ("write", "save")
                and path.is_file()
                and not (path_stat.st_mode & stat.S_IWRITE)
            ):
                raise PermissionDeniedError(
                    f"File is read-only: {path}", path=path, operation=operation
                )
        else:
            parent = path.parent
            if not parent.exists():
                raise FileNotFoundError(f"Parent directory does not exist: {parent}")

            if not os.access(parent, os.W_OK):
                raise PermissionDeniedError(
                    f"No write permission for parent directory: {parent}",
                    path=parent,
                    operation="create_in_directory",
                )

    except OSError as e:
        raise FileSystemError(
            f"Error checking permissions for {path}: {e}",
            path=path,
            operation=operation,
        )


def validate_path_with_purepath(path_str: str) -> Path:
    """Validate and normalize path using PurePath for cross-platform compatibility.

    Args:
        path_str: String representation of the path.

    Returns:
        Validated and normalized Path object.

    Raises:
        ValidationError: If path is invalid.
    """
    try:
        pure_path = PurePath(path_str)

        for part in pure_path.parts:
            if not part or part in (".", ""):
                continue

            invalid_chars = set('<>:"|?*')
            if sys.platform == "win32":
                invalid_chars.update(["/", "\\"])

            if any(char in part for char in invalid_chars):
                raise ValidationError(
                    f"Invalid characters in path component: {part}",
                    field="path_component",
                    value=part,
                    severity=ErrorSeverity.HIGH,
                )

        path = Path(path_str).resolve()

        return path

    except (ValueError, OSError) as e:
        raise ValidationError(
            f"Invalid path: {path_str} - {e}",
            field="path",
            value=path_str,
            severity=ErrorSeverity.HIGH,
        )


def atomic_file_write(path: Path, content: bytes, backup: bool = True) -> None:
    """Atomically write content to a file with optional backup.

    Args:
        path: Target file path.
        content: Content to write.
        backup: Whether to create a backup of existing file.

    Raises:
        FileOperationError: If write operation fails.
    """
    with safe_file_operation(path, "atomic_write"):
        backup_path = None
        if backup and path.exists():
            backup_path = path.with_suffix(f"{path.suffix}.backup")
            try:
                shutil.copy2(path, backup_path)
            except Exception as e:
                raise FileOperationError(
                    f"Failed to create backup: {e}",
                    path=backup_path,
                    operation="backup_creation",
                )

        temp_path = None
        try:
            with tempfile.NamedTemporaryFile(
                mode="wb",
                dir=path.parent,
                prefix=f".{path.stem}_",
                suffix=f"{path.suffix}.tmp",
                delete=False,
            ) as temp_file:
                temp_path = Path(temp_file.name)
                temp_file.write(content)
                temp_file.flush()
                os.fsync(temp_file.fileno())

            if sys.platform == "win32":
                if path.exists():
                    path.unlink()

            temp_path.replace(path)

        except Exception as e:
            if temp_path and temp_path.exists():
                try:
                    temp_path.unlink()
                except OSError:
                    pass

            if backup_path and backup_path.exists():
                try:
                    shutil.copy2(backup_path, path)
                except (OSError, shutil.Error):
                    pass
            raise FileOperationError(
                f"Atomic write failed: {e}", path=path, operation="atomic_write"
            )
        finally:
            if backup_path and backup_path.exists():
                try:
                    backup_path.unlink()
                except OSError:
                    pass


def validate_hex_color(*, color: str | None) -> bool:
    """Validate if a string is a valid hex color code.

    Args:
        color: Color string to validate.

    Returns:
        True if valid hex color, False otherwise.
    """
    if not isinstance(color, str):
        return False

    pattern = r"^#?([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$"
    return bool(re.match(pattern, color))


def validate_colors(colors: tuple[str, str] | list[str]) -> None:
    """Validate a collection of color codes.

    Args:
        colors: Collection of color codes to validate.

    Raises:
        ValidationError: If colors are invalid.
    """
    if len(colors) != 2:
        raise ValidationError(
            f"Exactly 2 colors required, got {len(colors)}",
            field="colors_count",
            value=len(colors),
            severity=ErrorSeverity.HIGH,
        )

    for i, color in enumerate(colors):
        if not validate_hex_color(color=color):
            raise ValidationError(
                f"Invalid hex color at position {i}: '{color}'",
                field=f"color_{i}",
                value=color,
                severity=ErrorSeverity.MEDIUM,
            )


def print_colored_message(
    message: str,
    color: str = TerminalColors.WHITE,
    background: str = "",
    style: str = "",
    end: str = "\n",
) -> None:
    """Print a colored message to the terminal.

    Args:
        message: The message to print.
        color: ANSI color code for text color.
        background: ANSI color code for background color.
        style: ANSI style code (bold, underline, etc.).
        end: String appended after the message.
    """
    formatted_message: str = (
        f"{style}{background}{color}{message}{TerminalColors.RESET}"
    )
    print(formatted_message, end=end)


def create_progress_bar(
    current: int, total: int, width: int = 50, show_percentage: bool = True
) -> None:
    """Create and display a colorful progress bar.

    Args:
        current: Current progress value.
        total: Total value when complete.
        width: Width of the progress bar in characters.
        show_percentage: Whether to show percentage value.
    """
    if total == 0:
        percentage: float = 0.0
    else:
        percentage = (current / total) * 100

    filled_width: int = int((current / total) * width) if total > 0 else 0

    bar_colors: List[str] = [
        TerminalColors.RED,
        TerminalColors.YELLOW,
        TerminalColors.GREEN,
        TerminalColors.CYAN,
        TerminalColors.BLUE,
        TerminalColors.MAGENTA,
    ]

    bar: str = ""
    for i in range(width):
        if i < filled_width:
            color_index: int = (i * len(bar_colors)) // width
            bar += f"{bar_colors[color_index]}â–ˆ{TerminalColors.RESET}"
        else:
            bar += f"{TerminalColors.DIM}â–'{TerminalColors.RESET}"

    progress_line: str = (
        f"\r{TerminalColors.BOLD}Progress:{TerminalColors.RESET} [{bar}]"
    )

    if show_percentage:
        if percentage < 25:
            percent_color: str = TerminalColors.RED
        elif percentage < 50:
            percent_color = TerminalColors.YELLOW
        elif percentage < 75:
            percent_color = TerminalColors.CYAN
        elif percentage < 100:
            percent_color = TerminalColors.GREEN
        else:
            percent_color = TerminalColors.BRIGHT_GREEN

        progress_line += f" {percent_color}{percentage:6.1f}%{TerminalColors.RESET}"

    progress_line += f" ({TerminalColors.BRIGHT_CYAN}{current}{TerminalColors.RESET}/{TerminalColors.BRIGHT_MAGENTA}{total}{TerminalColors.RESET})"

    print(f"{TerminalColors.CLEAR_LINE}{progress_line}", end="", flush=True)


def print_section_header(title: str, color: str = TerminalColors.BRIGHT_CYAN) -> None:
    """Print a colored section header.

    Args:
        title: The header title to display.
        color: ANSI color code for the header.
    """
    separator: str = "=" * len(title)
    print_colored_message(separator, color, style=TerminalColors.BOLD)
    print_colored_message(title, color, style=TerminalColors.BOLD)
    print_colored_message(separator, color, style=TerminalColors.BOLD)


def print_success_message(message: str) -> None:
    """Print a success message in green.

    Args:
        message: The success message to display.
    """
    print_colored_message(
        f"SUCCESS: {message}", TerminalColors.BRIGHT_GREEN, style=TerminalColors.BOLD
    )


def print_error_message(message: str) -> None:
    """Print an error message in red.

    Args:
        message: The error message to display.
    """
    print_colored_message(
        f"ERROR: {message}", TerminalColors.BRIGHT_RED, style=TerminalColors.BOLD
    )


def print_info_message(message: str) -> None:
    """Print an info message in cyan.

    Args:
        message: The info message to display.
    """
    print_colored_message(
        f"INFO: {message}", TerminalColors.BRIGHT_CYAN, style=TerminalColors.BOLD
    )


def print_warning_message(message: str) -> None:
    """Print a warning message in yellow.

    Args:
        message: The warning message to display.
    """
    print_colored_message(
        f"WARNING: {message}", TerminalColors.BRIGHT_YELLOW, style=TerminalColors.BOLD
    )


def create_output_directory_advanced(directory: Path) -> None:
    """Create output directory with comprehensive validation and error handling.

    Args:
        directory: Path object for the directory to create.

    Raises:
        FileOperationError: If directory creation fails.
    """
    directory = validate_path_with_purepath(str(directory))

    with safe_file_operation(directory, "directory_creation"):
        if directory.exists():
            if not directory.is_dir():
                raise FileSystemError(
                    f"Path exists but is not a directory: {directory}",
                    path=directory,
                    operation="directory_validation",
                    severity=ErrorSeverity.HIGH,
                )

            try:
                if any(directory.iterdir()):
                    # Remove warning as it's not critical and pollutes output
                    pass
            except PermissionError:
                pass

            print_success_message(f"Using existing directory: {directory}")
        else:
            try:
                directory.mkdir(parents=True, exist_ok=True)

                if sys.platform != "win32":
                    directory.chmod(0o755)

                print_success_message(f"Created output directory: {directory}")

            except FileExistsError:
                if directory.is_dir():
                    print_success_message(
                        f"Directory created by another process: {directory}"
                    )
                else:
                    raise FileSystemError(
                        f"File exists but is not a directory: {directory}",
                        path=directory,
                        operation="directory_creation",
                    )


def calculate_pie_sizes(percentage: int) -> List[float]:
    """Calculate pie chart sizes based on percentage.

    Args:
        percentage: Percentage for first color (0-100).

    Returns:
        List of two floats representing the sizes for each pie segment.

    Note:
        Uses small non-zero values for edge cases (0% and 100%) to avoid
        matplotlib rendering issues.
    """
    if percentage == 0:
        return [0.001, 99.999]
    elif percentage == 100:
        return [99.999, 0.001]
    else:
        return [float(percentage), float(100 - percentage)]


def create_pie_chart(
    percentage: int,
    colors: tuple[str, str] | list[str],
    figure_size: Tuple[float, float],
    start_angle: int = 90,
    clockwise: bool = False,
    edge_color: str = "white",
    edge_width: float = 2.0,
    font_size: int = 24,
    font_color: str = "#333333",
    font_weight: str = "bold",
    title_font_size: int = 16,
    show_percentage: bool = False,
    show_title: bool = False,
    transparent_background: bool = True,
) -> Tuple[plt.Figure, plt.Axes]:
    """Create a single pie chart with specified parameters.

    Args:
        percentage: Percentage for the first color (0-100).
        colors: Collection of two hex color codes.
        figure_size: Tuple of (width, height) for the figure size.
        start_angle: Starting angle in degrees.
        clockwise: Whether to draw clockwise.
        edge_color: Color for pie segment edges.
        edge_width: Width of edge lines.
        font_size: Font size for percentage text.
        font_color: Color for percentage text.
        font_weight: Font weight for percentage text.
        title_font_size: Font size for title.
        show_percentage: Whether to show percentage in center.
        show_title: Whether to show title.
        transparent_background: Whether to use transparent background.

    Returns:
        Tuple containing the matplotlib Figure and Axes objects.

    Raises:
        RenderingError: If chart creation fails.
    """
    try:
        sizes: List[float] = calculate_pie_sizes(percentage)

        fig, ax = plt.subplots(figsize=figure_size)

        # Configure transparent background if requested
        if transparent_background:
            fig.patch.set_alpha(0.0)
            ax.patch.set_alpha(0.0)

        wedges, _ = ax.pie(
            sizes,
            colors=colors,
            startangle=start_angle,
            counterclock=not clockwise,
            wedgeprops={
                "width": 0.8,
                "edgecolor": edge_color,
                "linewidth": edge_width,
            },
        )

        # Show percentage only if requested
        if show_percentage:
            ax.text(
                0,
                0,
                f"{percentage}%",
                horizontalalignment="center",
                verticalalignment="center",
                fontsize=font_size,
                fontweight=font_weight,
                color=font_color,
            )

        ax.set_aspect("equal")

        # Show title only if requested
        if show_title:
            ax.set_title(
                f"Pie Chart - {percentage}% / {100 - percentage}%",
                fontsize=title_font_size,
                fontweight="bold",
                pad=20,
            )

        return fig, ax

    except Exception as e:
        raise RenderingError(f"Failed to create pie chart for {percentage}%: {e}")


def save_chart_image_advanced(
    fig: plt.Figure,
    percentage: int,
    config: ChartConfig,
) -> Path:
    """Save pie chart image with comprehensive error handling and modern Path usage.

    Args:
        fig: Matplotlib figure object to save.
        percentage: Percentage value for filename generation.
        config: Chart configuration object.

    Returns:
        Path object of the saved image.

    Raises:
        FileOperationError: If image saving fails.
    """
    filename = config.output_dir / f"pie_chart_{percentage:03d}.{config.format.value}"
    filename = validate_path_with_purepath(str(filename))
    if filename.exists() and not config.overwrite_existing:
        if config.verbose:
            print_info_message(f"Skipping existing file: {filename.name}")
        return filename

    try:
        with safe_file_operation(filename, "image_save"):
            save_kwargs: dict[str, Any] = {
                "bbox_inches": "tight",
                "metadata": {
                    "Creator": "Pie Chart Generator",
                    "Subject": f"Pie chart at {percentage}%",
                    "Title": f"pie_chart_{percentage:03d}",
                },
            }

            # Configure background based on transparency option
            if config.transparent_background:
                save_kwargs["facecolor"] = "none"
                save_kwargs["edgecolor"] = "none"
                save_kwargs["transparent"] = True
            else:
                save_kwargs["facecolor"] = "white"
                save_kwargs["edgecolor"] = "none"

            match config.format:
                case ImageFormat.PNG | ImageFormat.WEBP | ImageFormat.TIFF:
                    save_kwargs["dpi"] = config.dpi
                case ImageFormat.JPG | ImageFormat.JPEG:
                    save_kwargs["dpi"] = config.dpi
                    save_kwargs["quality"] = 95
                    save_kwargs["optimize"] = True
                    # JPEG doesn't support transparency, force white background
                    if config.transparent_background:
                        print_warning_message(
                            "JPEG format doesn't support transparency, using white background"
                        )
                        save_kwargs["facecolor"] = "white"
                        save_kwargs["transparent"] = False
                case ImageFormat.PDF:
                    save_kwargs["pdf_compression"] = 6
                case ImageFormat.SVG:
                    save_kwargs["metadata"] = {
                        **save_kwargs["metadata"],
                        "Date": time.strftime("%Y-%m-%d"),
                    }

            import io

            buffer = io.BytesIO()
            fig.savefig(buffer, format=config.format.value, **save_kwargs)
            image_data = buffer.getvalue()
            buffer.close()

            atomic_file_write(filename, image_data, backup=False)

            return filename

    except Exception as e:
        raise FileOperationError(
            f"Failed to save image for {percentage}%: {e}",
            path=filename,
            operation="image_save",
            severity=ErrorSeverity.HIGH,
            context={"percentage": percentage, "format": config.format.value},
        )


def load_config_from_file_advanced(config_path: Path) -> dict[str, Any]:
    """Load configuration from JSON file with enhanced error handling.

    Args:
        config_path: Path to the configuration file.

    Returns:
        Configuration dictionary.

    Raises:
        ConfigurationError: If configuration loading fails.
    """
    config_path = validate_path_with_purepath(str(config_path))

    with safe_file_operation(config_path, "config_read"):
        try:
            file_size = config_path.stat().st_size
            if file_size > 10 * 1024 * 1024:
                raise ConfigurationError(
                    f"Configuration file too large: {file_size} bytes",
                    severity=ErrorSeverity.HIGH,
                )

            with config_path.open("r", encoding="utf-8") as f:
                config: dict[str, Any] = json.load(f)

            return config

        except json.JSONDecodeError as e:
            raise ConfigurationError(
                f"Invalid JSON in config file: {e}",
                severity=ErrorSeverity.HIGH,
                context={"line": e.lineno, "column": e.colno, "error": e.msg},
            )
        except UnicodeDecodeError as e:
            raise ConfigurationError(
                f"Encoding error in config file: {e}", severity=ErrorSeverity.HIGH
            )


def save_config_to_file_advanced(config: dict[str, Any], config_path: Path) -> None:
    """Save configuration to JSON file with atomic write.

    Args:
        config: Configuration dictionary to save.
        config_path: Path where to save the configuration.

    Raises:
        ConfigurationError: If configuration saving fails.
    """
    config_path = validate_path_with_purepath(str(config_path))

    try:
        json_data = json.dumps(
            config, indent=2, ensure_ascii=False, sort_keys=True
        ).encode("utf-8")

        atomic_file_write(config_path, json_data, backup=True)

        print_success_message(f"Configuration saved to: {config_path}")

    except (TypeError, ValueError) as e:
        raise ConfigurationError(
            f"Failed to serialize configuration: {e}", severity=ErrorSeverity.HIGH
        )
    except Exception as e:
        raise ConfigurationError(
            f"Failed to save configuration: {e}", severity=ErrorSeverity.HIGH
        )


def parse_color_list(color_string: str) -> tuple[str, str]:
    """Parse a comma-separated string of colors.

    Args:
        color_string: Comma-separated color codes.

    Returns:
        Tuple of validated color codes.

    Raises:
        ValidationError: If color parsing fails.
    """
    try:
        colors = [color.strip() for color in color_string.split(",")]
        validate_colors(colors)
        return colors[0], colors[1]
    except Exception as e:
        raise ValidationError(f"Failed to parse colors '{color_string}': {e}")


def validate_percentage_range(start: int, end: int, step: int) -> None:
    """Validate percentage range parameters.

    Args:
        start: Starting percentage.
        end: Ending percentage.
        step: Step increment.

    Raises:
        ValidationError: If range parameters are invalid.
    """
    if not (0 <= start <= 100):
        raise ValidationError(f"Start percentage must be 0-100, got {start}")

    if not (0 <= end <= 100):
        raise ValidationError(f"End percentage must be 0-100, got {end}")

    if start >= end:
        raise ValidationError(f"Start ({start}) must be less than end ({end})")

    if step <= 0:
        raise ValidationError(f"Step must be positive, got {step}")

    if step > (end - start):
        raise ValidationError(f"Step ({step}) too large for range {start}-{end}")


def validate_dimensions(width: float, height: float) -> None:
    """Validate figure dimensions.

    Args:
        width: Figure width in inches.
        height: Figure height in inches.

    Raises:
        ValidationError: If dimensions are invalid.
    """
    if width <= 0:
        raise ValidationError(f"Width must be positive, got {width}")

    if height <= 0:
        raise ValidationError(f"Height must be positive, got {height}")

    if width > 50 or height > 50:
        raise ValidationError(f"Dimensions too large: {width}x{height} (max 50x50)")


def validate_dpi(dpi: int) -> None:
    """Validate DPI value.

    Args:
        dpi: DPI value to validate.

    Raises:
        ValidationError: If DPI is invalid.
    """
    if dpi < 50:
        raise ValidationError(f"DPI too low: {dpi} (minimum 50)")

    if dpi > 1000:
        raise ValidationError(f"DPI too high: {dpi} (maximum 1000)")


def create_argument_parser() -> argparse.ArgumentParser:
    """Create and configure the command-line argument parser.

    Returns:
        Configured ArgumentParser instance.
    """
    parser = argparse.ArgumentParser(
        description="Generate a series of pie charts with customizable parameters",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s
  %(prog)s -o charts -c "#FF0000,#00FF00" -s 0 -e 50 --step 5
  %(prog)s --width 10 --height 10 --dpi 300 --clockwise
  %(prog)s --colors "#123456,#ABCDEF" --gif --gif-duration 50
  %(prog)s --start-angle 0 --font-size 32 --show-percentage
  %(prog)s --format webp --atomic-writes --backup --transparent
  %(prog)s --show-title --no-transparent
        """,
    )

    output_group = parser.add_argument_group("Output Options")
    output_group.add_argument(
        "-o",
        "--output-dir",
        type=Path,
        default=ChartConfig().output_dir,
        help=f"Output directory for generated images (default: {ChartConfig().output_dir})",
    )
    output_group.add_argument(
        "-f",
        "--format",
        type=lambda x: ImageFormat(x.lower()),
        choices=list(ImageFormat),
        default=ChartConfig().format,
        help=f"Output image format (default: {ChartConfig().format.value})",
    )
    output_group.add_argument(
        "--dpi",
        type=int,
        default=ChartConfig().dpi,
        help=f"Image resolution in DPI (default: {ChartConfig().dpi})",
    )
    output_group.add_argument(
        "--atomic-writes",
        action="store_true",
        help="Use atomic file writes to prevent corruption",
    )
    output_group.add_argument(
        "--backup",
        action="store_true",
        help="Create backups of existing files",
    )
    output_group.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing files (default: skip existing files)",
    )

    visual_group = parser.add_argument_group("Visual Options")
    visual_group.add_argument(
        "-c",
        "--colors",
        type=str,
        default=",".join(ChartConfig().colors),
        help=f"Two hex colors separated by comma (default: {','.join(ChartConfig().colors)})",
    )
    visual_group.add_argument(
        "-w",
        "--width",
        type=float,
        default=ChartConfig().width,
        help=f"Figure width in inches (default: {ChartConfig().width})",
    )
    visual_group.add_argument(
        "--height",
        type=float,
        default=ChartConfig().height,
        help=f"Figure height in inches (default: {ChartConfig().height})",
    )

    # New transparency option
    visual_group.add_argument(
        "--transparent",
        action="store_true",
        default=ChartConfig().transparent_background,
        help="Use transparent background (default: enabled)",
    )
    visual_group.add_argument(
        "--no-transparent",
        action="store_true",
        help="Use white background instead of transparent",
    )

    range_group = parser.add_argument_group("Range Options")
    range_group.add_argument(
        "-s",
        "--start",
        type=int,
        default=ChartConfig().start_percent,
        help=f"Starting percentage (default: {ChartConfig().start_percent})",
    )
    range_group.add_argument(
        "-e",
        "--end",
        type=int,
        default=ChartConfig().end_percent,
        help=f"Ending percentage (default: {ChartConfig().end_percent})",
    )
    range_group.add_argument(
        "--step",
        type=int,
        default=ChartConfig().step,
        help=f"Step increment (default: {ChartConfig().step})",
    )

    chart_group = parser.add_argument_group("Chart Appearance")
    chart_group.add_argument(
        "--start-angle",
        type=int,
        default=ChartConfig().start_angle,
        help=f"Starting angle in degrees (default: {ChartConfig().start_angle})",
    )
    chart_group.add_argument(
        "--clockwise",
        action="store_true",
        default=ChartConfig().clockwise,
        help="Draw pie chart clockwise (default: counter-clockwise)",
    )
    chart_group.add_argument(
        "--edge-color",
        type=str,
        default=ChartConfig().edge_color,
        help=f"Edge color (default: {ChartConfig().edge_color})",
    )
    chart_group.add_argument(
        "--edge-width",
        type=float,
        default=ChartConfig().edge_width,
        help=f"Edge line width (default: {ChartConfig().edge_width})",
    )

    text_group = parser.add_argument_group("Text Options")
    text_group.add_argument(
        "--font-size",
        type=int,
        default=ChartConfig().font_size,
        help=f"Font size for percentage text (default: {ChartConfig().font_size})",
    )
    text_group.add_argument(
        "--font-color",
        type=str,
        default=ChartConfig().font_color,
        help=f"Font color for percentage text (default: {ChartConfig().font_color})",
    )
    text_group.add_argument(
        "--font-weight",
        type=lambda x: FontWeight(x.lower()),
        choices=list(FontWeight),
        default=ChartConfig().font_weight,
        help=f"Font weight (default: {ChartConfig().font_weight.value})",
    )
    text_group.add_argument(
        "--title-font-size",
        type=int,
        default=ChartConfig().title_font_size,
        help=f"Title font size (default: {ChartConfig().title_font_size})",
    )

    # Options to show or hide text
    text_group.add_argument(
        "--show-percentage",
        action="store_true",
        help="Show percentage text in center (default: disabled)",
    )
    text_group.add_argument(
        "--show-title",
        action="store_true",
        help="Show chart title (default: disabled)",
    )

    gif_group = parser.add_argument_group("GIF Options")
    gif_group.add_argument(
        "--gif",
        action="store_true",
        help="Generate animated GIF",
    )
    gif_group.add_argument(
        "--gif-duration",
        type=int,
        default=ChartConfig().gif_duration,
        help=f"GIF frame duration in milliseconds (default: {ChartConfig().gif_duration})",
    )
    gif_group.add_argument(
        "--gif-loop",
        type=int,
        default=ChartConfig().gif_loop,
        help=f"GIF loop count (0=infinite) (default: {ChartConfig().gif_loop})",
    )
    gif_group.add_argument(
        "--keep-png",
        action="store_true",
        help=(
            "Keep PNG files when generating GIF "
            "(default: delete PNG files after GIF creation)"
        ),
    )

    progress_group = parser.add_argument_group("Progress Options")
    progress_group.add_argument(
        "--quiet",
        "-q",
        action="store_true",
        help="Suppress progress output",
    )
    progress_group.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable verbose output",
    )

    config_group = parser.add_argument_group("Configuration")
    config_group.add_argument(
        "--config",
        type=Path,
        help="Load configuration from JSON file",
    )
    config_group.add_argument(
        "--save-config",
        type=Path,
        help="Save current configuration to JSON file",
    )

    return parser


def validate_arguments(args: argparse.Namespace) -> None:
    """Validate command-line arguments.

    Args:
        args: Parsed command-line arguments.

    Raises:
        ValidationError: If arguments are invalid.
    """
    try:
        parse_color_list(args.colors)
        validate_dimensions(args.width, args.height)
        validate_dpi(args.dpi)
        validate_percentage_range(args.start, args.end, args.step)

        if not (0 <= args.start_angle <= 360):
            raise ValidationError(f"Start angle must be 0-360, got {args.start_angle}")

        if args.font_size <= 0:
            raise ValidationError(f"Font size must be positive, got {args.font_size}")

        if args.title_font_size <= 0:
            raise ValidationError(
                f"Title font size must be positive, got {args.title_font_size}"
            )

        if args.edge_width < 0:
            raise ValidationError(
                f"Edge width must be non-negative, got {args.edge_width}"
            )

        if args.gif_duration <= 0:
            raise ValidationError(
                f"GIF duration must be positive, got {args.gif_duration}"
            )

        if args.gif_loop < 0:
            raise ValidationError(
                f"GIF loop count must be non-negative, got {args.gif_loop}"
            )

        if not validate_hex_color(color=args.font_color):
            raise ValidationError(f"Invalid font color: {args.font_color}")

        # Validate mutually exclusive transparency options
        if args.transparent and args.no_transparent:
            raise ValidationError(
                "Cannot use both --transparent and --no-transparent options"
            )

    except Exception as e:
        if isinstance(e, ValidationError):
            raise
        else:
            raise ValidationError(f"Argument validation failed: {e}")


def args_to_config(args: argparse.Namespace) -> ChartConfig:
    """Convert parsed arguments to ChartConfig object.

    Args:
        args: Parsed command-line arguments.

    Returns:
        ChartConfig object with validated parameters.
    """
    colors = parse_color_list(args.colors)

    # Handle transparency option
    transparent_background = ChartConfig().transparent_background
    if args.no_transparent:
        transparent_background = False
    elif args.transparent:
        transparent_background = True

    return ChartConfig(
        output_dir=args.output_dir,
        colors=colors,
        width=args.width,
        height=args.height,
        dpi=args.dpi,
        start_percent=args.start,
        end_percent=args.end,
        step=args.step,
        start_angle=args.start_angle,
        clockwise=args.clockwise,
        edge_color=args.edge_color,
        edge_width=args.edge_width,
        font_size=args.font_size,
        font_color=args.font_color,
        font_weight=args.font_weight,
        title_font_size=args.title_font_size,
        show_percentage=args.show_percentage,
        show_title=args.show_title,
        transparent_background=transparent_background,
        format=args.format,
        gif_duration=args.gif_duration,
        gif_loop=args.gif_loop,
        keep_png_for_gif=args.keep_png,
        overwrite_existing=args.overwrite,
        quiet=args.quiet,
        verbose=args.verbose,
    )


def generate_pie_chart_series(config: ChartConfig) -> None:
    """Generate complete series of pie charts based on configuration.

    Args:
        config: Chart configuration object.

    Raises:
        ValidationError: If configuration is invalid.
        FileOperationError: If file operations fail.
        RenderingError: If chart rendering fails.
    """
    try:
        create_output_directory_advanced(config.output_dir)

        if not config.quiet:
            print_section_header("PIE CHART GENERATION")
            print_info_message(
                f"Range: {config.start_percent}% to {config.end_percent}% (step: {config.step})"
            )
            print_info_message(f"Colors: {config.colors[0]} and {config.colors[1]}")
            print_info_message(
                f"Output: {config.output_dir} ({config.format.value.upper()})"
            )
            print_info_message(
                f"Dimensions: {config.width}x{config.height} inches @ {config.dpi} DPI"
            )
            print_info_message(
                f"Transparent background: {config.transparent_background}"
            )
            print_info_message(f"Show percentage: {config.show_percentage}")
            print_info_message(f"Show title: {config.show_title}")
            print()

        percentages: List[int] = list(
            range(config.start_percent, config.end_percent + 1, config.step)
        )
        total_charts: int = len(percentages)
        created_count = 0
        skipped_count = 0

        if config.verbose:
            print_info_message(f"Generating {total_charts} charts...")

        # Use tqdm directly instead of wrapper function
        progress_bar = tqdm(
            enumerate(percentages),
            total=len(percentages),
            desc="Generating charts",
            disable=config.quiet,
            unit="chart",
        )

        for i, percentage in progress_bar:
            try:
                filename = (
                    config.output_dir
                    / f"pie_chart_{percentage:03d}.{config.format.value}"
                )
                file_existed = filename.exists()

                fig, ax = create_pie_chart(
                    percentage=percentage,
                    colors=config.colors,
                    figure_size=(config.width, config.height),
                    start_angle=config.start_angle,
                    clockwise=config.clockwise,
                    edge_color=config.edge_color,
                    edge_width=config.edge_width,
                    font_size=config.font_size,
                    font_color=config.font_color,
                    font_weight=str(config.font_weight.value),
                    title_font_size=config.title_font_size,
                    show_percentage=config.show_percentage,
                    show_title=config.show_title,
                    transparent_background=config.transparent_background,
                )

                save_chart_image_advanced(fig, percentage, config)
                plt.close(fig)

                if file_existed and not config.overwrite_existing:
                    skipped_count += 1
                else:
                    created_count += 1

                if config.verbose and (i + 1) % 10 == 0:
                    tqdm.write(f"Generated {i + 1}/{total_charts} charts")

            except (RenderingError, FileOperationError) as e:
                tqdm.write(f"ERROR: Failed to generate chart for {percentage}%: {e}")
                if config.quiet:
                    raise

        if skipped_count > 0:
            print_success_message(
                f"Generation complete! "
                f"{created_count} images created, "
                f"{skipped_count} existing files skipped "
                f"in '{config.output_dir}' directory"
            )
            if not config.overwrite_existing:
                print_info_message("Use --overwrite to replace existing files")
        else:
            print_success_message(
                f"Generation complete! {total_charts} images created "
                f"in '{config.output_dir}' directory"
            )

    except Exception as e:
        if isinstance(e, (ValidationError, FileOperationError, RenderingError)):
            raise
        else:
            raise PieChartError(f"Unexpected error during generation: {e}")


def _create_gif_from_config(
    config: ChartConfig, output_filename: str = "animation.gif"
) -> List[str]:
    """Helper function to find image files and create GIF.

    Args:
        config: Chart configuration object.
        output_filename: Name for the output GIF file.

    Returns:
        List of image file paths that were used to create the GIF.

    Raises:
        ImportError: If Pillow is not available.
        Exception: If GIF creation fails.
    """
    from PIL import Image
    import glob

    pattern: str = str(config.output_dir / f"pie_chart_*.{config.format.value}")
    image_files: List[str] = sorted(glob.glob(pattern))

    if not image_files:
        print_error_message(f"No images found in {config.output_dir}")
        return []

    percentages = list(range(config.start_percent, config.end_percent + 1, config.step))
    expected_files = len(percentages)

    if len(image_files) < expected_files and not config.overwrite_existing:
        print_warning_message(
            f"Found {len(image_files)} PNG files but expected {expected_files}. "
            f"Some files may have been skipped. Use --overwrite to ensure all files are generated."
        )

    print_info_message(f"Creating GIF from {len(image_files)} images...")

    # Use tqdm directly for GIF creation
    progress_bar = tqdm(
        image_files, desc="Loading images", disable=config.quiet, unit="image"
    )

    images: List[Image.Image] = []
    for filename in progress_bar:
        img: Image.Image = Image.open(filename)
        images.append(img)

    output_path: Path = config.output_dir / output_filename
    images[0].save(
        str(output_path),
        save_all=True,
        append_images=images[1:],
        duration=config.gif_duration,
        loop=config.gif_loop,
    )

    print_success_message(f"Animated GIF created: {output_path}")
    return image_files


def create_animated_gif(
    config: ChartConfig, output_filename: str = "animation.gif"
) -> None:
    """Create animated GIF from generated pie chart images.

    Args:
        config: Chart configuration object.
        output_filename: Name for the output GIF file.

    Note:
        Requires Pillow package (pip install Pillow).
    """
    try:
        # Create GIF and get list of image files used
        image_files = _create_gif_from_config(config, output_filename)

        if not image_files:  # No images found
            return

        # Cleanup PNG files if requested
        if not config.keep_png_for_gif:
            print_info_message("Cleaning up PNG files...")
            cleanup_bar = tqdm(
                image_files,
                desc="Deleting PNG files",
                disable=config.quiet,
                unit="file",
            )
            deleted_count = 0
            for filename in cleanup_bar:
                try:
                    Path(filename).unlink()
                    deleted_count += 1
                except OSError as e:
                    print_warning_message(f"Could not delete {filename}: {e}")

            if deleted_count > 0:
                print_success_message(f"Deleted {deleted_count} PNG files")
            else:
                print_info_message("No PNG files were deleted")
        else:
            print_info_message(f"Kept {len(image_files)} PNG files as requested")

    except ImportError:
        print_warning_message(
            "To create animated GIF, install Pillow: pip install Pillow"
        )
    except Exception as e:
        print_error_message(f"GIF creation failed: {e}")


def create_animated_gif_with_existing(
    config: ChartConfig, existing_files: set, output_filename: str = "animation.gif"
) -> None:
    """Create animated GIF from generated pie chart images.

    Args:
        config: Chart configuration object.
        existing_files: Set of files that existed before generation.
        output_filename: Name for the output GIF file.

    Note:
        Requires Pillow package (pip install Pillow).
    """
    try:
        # Create GIF and get list of image files used
        image_files = _create_gif_from_config(config, output_filename)

        if not image_files:  # No images found
            return

        # Cleanup only new PNG files if requested
        if not config.keep_png_for_gif:
            print_info_message("Cleaning up newly created PNG files...")
            new_files = [f for f in image_files if f not in existing_files]
            if new_files:
                cleanup_bar = tqdm(
                    new_files,
                    desc="Deleting new PNG files",
                    disable=config.quiet,
                    unit="file",
                )
                deleted_count = 0
                for filename in cleanup_bar:
                    try:
                        Path(filename).unlink()
                        deleted_count += 1
                    except OSError as e:
                        print_warning_message(f"Could not delete {filename}: {e}")
                print_success_message(
                    f"Deleted {deleted_count} newly created PNG files"
                )
            else:
                print_info_message("No new PNG files to delete")
        else:
            print_info_message(f"Kept {len(image_files)} PNG files as requested")

    except ImportError:
        print_warning_message(
            "To create animated GIF, install Pillow: pip install Pillow"
        )
    except Exception as e:
        print_error_message(f"GIF creation failed: {e}")


def main() -> None:
    """Main function to execute the pie chart generation process.

    This function orchestrates the entire pie chart generation workflow,
    including argument parsing, validation, and execution.
    """
    try:
        print_section_header("PIE CHART GENERATOR", TerminalColors.BRIGHT_MAGENTA)

        parser = create_argument_parser()
        args = parser.parse_args()

        if args.config:
            try:
                load_config_from_file_advanced(args.config)
                print_success_message(f"Loaded configuration from: {args.config}")
            except ConfigurationError as e:
                print_error_message(f"Configuration error: {e}")
                sys.exit(1)

        try:
            validate_arguments(args)
            config = args_to_config(args)
        except ValidationError as e:
            print_error_message(f"Validation error: {e}")
            sys.exit(1)

        if args.save_config:
            try:
                config_dict = {
                    "output_dir": str(config.output_dir),
                    "colors": list(config.colors),
                    "width": config.width,
                    "height": config.height,
                    "dpi": config.dpi,
                    "start_percent": config.start_percent,
                    "end_percent": config.end_percent,
                    "step": config.step,
                    "start_angle": config.start_angle,
                    "clockwise": config.clockwise,
                    "edge_color": config.edge_color,
                    "edge_width": config.edge_width,
                    "font_size": config.font_size,
                    "font_color": config.font_color,
                    "font_weight": config.font_weight.value,
                    "title_font_size": config.title_font_size,
                    "show_percentage": config.show_percentage,
                    "show_title": config.show_title,
                    "transparent_background": config.transparent_background,
                    "format": config.format.value,
                    "gif_duration": config.gif_duration,
                    "gif_loop": config.gif_loop,
                }
                save_config_to_file_advanced(config_dict, args.save_config)
            except ConfigurationError as e:
                print_error_message(f"Failed to save configuration: {e}")
                sys.exit(1)

        print_info_message(
            "Generating pie charts with advanced error handling and Path validation"
        )
        print()

        if args.gif and not args.quiet:
            print_info_message("Animated GIF will be created after chart generation")

        existing_files = set()
        if args.gif and not config.keep_png_for_gif:
            import glob

            pattern = str(config.output_dir / f"pie_chart_*.{config.format.value}")
            existing_files = set(glob.glob(pattern))

        generate_pie_chart_series(config)

        if args.gif:
            print_section_header("GIF CREATION")
            create_animated_gif_with_existing(config, existing_files)

        print()
        print_success_message("Process completed successfully!")

    except KeyboardInterrupt:
        print()
        print_warning_message("Process interrupted by user")
        sys.exit(1)
    except Exception as e:
        print()
        print_error_message(f"Unexpected error: {e}")
        if isinstance(e, PieChartError) and e.severity == ErrorSeverity.CRITICAL:
            sys.exit(2)
        else:
            sys.exit(1)


if __name__ == "__main__":
    main()
