"""SVG to bitmap converter with integrated output handling."""

import argparse
import logging
import sys
import threading
import xml.etree.ElementTree as ElT
from pathlib import Path

try:
    from PIL import Image, ImageDraw
except ImportError:
    Image = ImageDraw = None
    print("[Error: Pillow is required. Install with: pip install Pillow]")
    sys.exit(1)

logger = logging.getLogger(__name__)


class OutputHandler:
    """Integrated output handler for command-line applications.

    Provides thread-safe output with different styling options and verbosity levels.
    """

    def __init__(self, verbosity_level: int = 1, no_color: bool = False) -> None:
        """Initialize output handler.

        Args:
            verbosity_level: Output verbosity (0=quiet, 1=normal, 2=verbose).
            no_color: Disable color output.
        """
        self._output_lock = threading.RLock()
        self.verbosity_level = verbosity_level
        self.no_color = no_color
        self.stderr = sys.stderr
        self.stdout = sys.stdout

        # Color codes for different message types
        self._colors = (
            {
                "success": "\033[92m",  # Green
                "warning": "\033[93m",  # Yellow
                "error": "\033[91m",  # Red
                "info": "\033[94m",  # Blue
                "reset": "\033[0m",  # Reset
            }
            if not no_color
            else {key: "" for key in ["success", "warning", "error", "info", "reset"]}
        )

    def _colorize(self, message: str, color_type: str) -> str:
        """Apply color to message.

        Args:
            message: Message to colorize.
            color_type: Type of color to apply.

        Returns:
            Colorized message.
        """
        if self.no_color:
            return message
        return f"{self._colors[color_type]}{message}{self._colors['reset']}"

    def out(self, message: str, level: int = 1, msg_type: str = "info") -> None:
        """Output message with specified verbosity level and type.

        Args:
            message: Message to output.
            level: Required verbosity level (0=always, 1=normal, 2=verbose).
            msg_type: Message type for styling ('info', 'success', 'warning', 'error').
        """
        if self.verbosity_level < level:
            return

        with self._output_lock:
            colored_message = self._colorize(message, msg_type)
            if msg_type == "error":
                self.stderr.write(f"{colored_message}\n")
                self.stderr.flush()
            else:
                self.stdout.write(f"{colored_message}\n")
                self.stdout.flush()

    def out_success(self, message: str, level: int = 1) -> None:
        """Output success message.

        Args:
            message: Success message.
            level: Required verbosity level.
        """
        self.out(f"[SUCCESS] {message}", level, "success")

    def out_warning(self, message: str, level: int = 1) -> None:
        """Output warning message.

        Args:
            message: Warning message.
            level: Required verbosity level.
        """
        self.out(f"[WARNING] {message}", level, "warning")

    def out_error(self, message: str, level: int = 0) -> None:
        """Output error message.

        Args:
            message: Error message.
            level: Required verbosity level.
        """
        self.out(f"[ERROR] {message}", level, "error")

    def out_info(self, message: str, level: int = 1) -> None:
        """Output info message.

        Args:
            message: Info message.
            level: Required verbosity level.
        """
        self.out(f"[INFO] {message}", level, "info")

    def out_verbose(self, message: str) -> None:
        """Output verbose message (level 2).

        Args:
            message: Verbose message.
        """
        self.out(f"[VERBOSE] {message}", 2, "info")


class ConversionError(Exception):
    """Exception raised when SVG conversion fails."""


class SVGParser:
    """Parser for simple rectangle-based SVG files."""

    def __init__(self, svg_path: Path, output_handler: OutputHandler) -> None:
        """Initialize SVG parser.

        Args:
            svg_path: Path to the SVG file.
            output_handler: Output handler for messages.
        """
        self.svg_path = svg_path
        self.out = output_handler
        self.width: int = 0
        self.height: int = 0
        self.rectangles: list[dict[str, str | int]] = []

    def parse(self) -> None:
        """Parse SVG file and extract rectangle information.

        Raises:
            ConversionError
        """
        self.out.out_verbose(f"Starting SVG parsing for file: {self.svg_path}")

        try:
            tree = ElT.parse(self.svg_path)
            root = tree.getroot()
            self.out.out_verbose("Successfully loaded XML tree")
        except ElT.ParseError as e:
            error_msg = f"Invalid SVG format: {e}"
            self.out.out_error(error_msg)
            raise ConversionError(error_msg) from e
        except FileNotFoundError as e:
            error_msg = f"SVG file not found: {e}"
            self.out.out_error(error_msg)
            raise ConversionError(error_msg) from e
        except PermissionError as e:
            error_msg = f"Permission denied reading SVG file: {e}"
            self.out.out_error(error_msg)
            raise ConversionError(error_msg) from e
        except Exception as e:
            error_msg = f"Unexpected error reading SVG file: {e}"
            self.out.out_error(error_msg)
            raise ConversionError(error_msg) from e

        # Extract viewBox or width/height
        try:
            view_box = root.get("viewBox")
            if view_box:
                self.out.out_verbose(f"Found viewBox: {view_box}")
                try:
                    _, _, width_str, height_str = view_box.split()
                    self.width = int(float(width_str))
                    self.height = int(float(height_str))
                except (ValueError, TypeError) as e:
                    raise ConversionError(f"Invalid viewBox format: {e}") from e
            else:
                self.out.out_verbose("No viewBox found, using width/height attributes")
                width_attr = root.get("width", "0")
                height_attr = root.get("height", "0")
                try:
                    self.width = int(float(width_attr.replace("px", "")))
                    self.height = int(float(height_attr.replace("px", "")))
                except (ValueError, TypeError) as e:
                    raise ConversionError(
                        f"Invalid width/height attributes: {e}"
                    ) from e

            if self.width <= 0 or self.height <= 0:
                raise ConversionError(
                    f"Invalid SVG dimensions: {self.width}x{self.height}"
                )

            self.out.out_verbose(f"SVG dimensions: {self.width}x{self.height}")

        except ConversionError:
            raise
        except Exception as e:
            error_msg = f"Error extracting SVG dimensions: {e}"
            self.out.out_error(error_msg)
            raise ConversionError(error_msg) from e

        # Find all rectangles
        try:
            namespace = {"": "http://www.w3.org/2000/svg"}
            rectangles = root.findall(".//rect", namespace) or root.findall(".//rect")

            if not rectangles:
                self.out.out_warning("No rectangles found in SVG")
            else:
                self.out.out_verbose(f"Found {len(rectangles)} rectangles")

        except Exception as e:
            error_msg = f"Error finding rectangles in SVG: {e}"
            self.out.out_error(error_msg)
            raise ConversionError(error_msg) from e

        # Check for unsupported elements
        try:
            all_elements = list(root.iter())
            unsupported_elements = []
            for elem in all_elements:
                try:
                    tag = elem.tag.split("}")[-1] if "}" in elem.tag else elem.tag
                    if tag not in ["svg", "rect"]:
                        unsupported_elements.append(tag)
                except (AttributeError, IndexError) as e:
                    self.out.out_warning(f"Error processing element tag: {e}")

            if unsupported_elements:
                unique_unsupported = list(set(unsupported_elements))
                error_msg = (
                    f"SVG contains unsupported elements: "
                    f"{', '.join(unique_unsupported)}. Only rectangles are supported."
                )
                self.out.out_error(error_msg)
                raise ConversionError(error_msg)

        except ConversionError:
            raise
        except Exception as e:
            error_msg = f"Error checking for unsupported elements: {e}"
            self.out.out_error(error_msg)
            raise ConversionError(error_msg) from e

        # Extract rectangle data
        try:
            for i, rect in enumerate(rectangles):
                try:
                    rect_data = {
                        "x": int(float(rect.get("x", "0"))),
                        "y": int(float(rect.get("y", "0"))),
                        "width": int(float(rect.get("width", "0"))),
                        "height": int(float(rect.get("height", "0"))),
                        "fill": rect.get("fill", "#000000"),
                    }
                    self.rectangles.append(rect_data)

                    self.out.out_verbose(
                        f"Rectangle {i + 1}: x={rect_data['x']}, y={rect_data['y']}, "
                        f"w={rect_data['width']}, h={rect_data['height']}, "
                        f"fill={rect_data['fill']}"
                    )

                except (ValueError, TypeError) as e:
                    error_msg = f"Invalid rectangle {i + 1} attributes: {e}"
                    self.out.out_error(error_msg)
                    raise ConversionError(error_msg) from e

        except ConversionError:
            raise
        except Exception as e:
            error_msg = f"Error extracting rectangle data: {e}"
            self.out.out_error(error_msg)
            raise ConversionError(error_msg) from e

        self.out.out_verbose(f"Successfully parsed {len(self.rectangles)} rectangles")


class BitmapConverter:
    """Converter for creating bitmap images from parsed SVG data."""

    def __init__(self, width: int, height: int, output_handler: OutputHandler) -> None:
        """Initialize bitmap converter.

        Args:
            width: Image width in pixels.
            height: Image height in pixels.
            output_handler: Output handler for messages.
        """
        self.width = width
        self.height = height
        self.out = output_handler

    def convert(
        self, rectangles: list[dict[str, str | int]], output_path: Path
    ) -> None:
        """Convert rectangle data to bitmap image.

        Args:
            rectangles: List of rectangle data dictionaries.
            output_path: Path where to save the bitmap image.

        Raises:
            ConversionError: If conversion fails.
        """
        self.out.out_verbose(f"Starting bitmap conversion to: {output_path}")
        self.out.out_verbose(f"Image dimensions: {self.width}x{self.height}")

        try:
            # Create an image with a transparent background
            try:
                image = Image.new("RGBA", (self.width, self.height), (0, 0, 0, 0))
                draw = ImageDraw.Draw(image)
                self.out.out_verbose("Created RGBA image canvas")
            except Exception as e:
                error_msg = f"Failed to create image canvas: {e}"
                self.out.out_error(error_msg)
                raise ConversionError(error_msg) from e

            # Draw each rectangle
            try:
                for i, rect in enumerate(rectangles):
                    try:
                        x = rect["x"]
                        y = rect["y"]
                        width = rect["width"]
                        height = rect["height"]
                        fill_color = self._parse_color(rect["fill"])

                        # Draw rectangle
                        draw.rectangle([x, y, x + width, y + height], fill=fill_color)

                        self.out.out_verbose(
                            f"Drew rectangle {i + 1} at ({x},{y}) "
                            f"size {width}x{height} color {fill_color}"
                        )

                    except (KeyError, TypeError, ValueError) as e:
                        error_msg = f"Error drawing rectangle {i + 1}: {e}"
                        self.out.out_error(error_msg)
                        raise ConversionError(error_msg) from e

            except ConversionError:
                raise
            except Exception as e:
                error_msg = f"Error during rectangle drawing: {e}"
                self.out.out_error(error_msg)
                raise ConversionError(error_msg) from e

            # Save image
            try:
                output_path.parent.mkdir(parents=True, exist_ok=True)

                if output_path.suffix.lower() == ".bmp":
                    self.out.out_verbose("Converting to RGB for BMP format")
                    # Convert to RGB for BMP format (no transparency)
                    rgb_image = Image.new("RGB", image.size, (255, 255, 255))
                    rgb_image.paste(image, mask=image.split()[-1])  # Use alpha as mask
                    rgb_image.save(output_path, "BMP")
                else:
                    image.save(output_path)

                self.out.out_verbose("Image saved successfully")
                self.out.out_success(f"Successfully converted to {output_path}")

            except PermissionError as e:
                error_msg = f"Permission denied saving to {output_path}: {e}"
                self.out.out_error(error_msg)
                raise ConversionError(error_msg) from e
            except OSError as e:
                error_msg = f"OS error saving image: {e}"
                self.out.out_error(error_msg)
                raise ConversionError(error_msg) from e
            except Exception as e:
                error_msg = f"Failed to save image: {e}"
                self.out.out_error(error_msg)
                raise ConversionError(error_msg) from e

        except ConversionError:
            raise
        except Exception as e:
            error_msg = f"Failed to create bitmap: {e}"
            self.out.out_error(error_msg)
            raise ConversionError(error_msg) from e

    def _parse_color(self, color_str: str | int) -> tuple[int, int, int, int]:
        """Parse color string to RGBA tuple.

        Args:
            color_str: Color in hex format (#RRGGBB) or color name.

        Returns:
            RGBA color tuple.

        Raises:
            ConversionError: If the color format is invalid.
        """
        try:
            if isinstance(color_str, int):
                return 0, 0, 0, 255

            color_str = str(color_str).strip()

            if color_str.startswith("#"):
                # Hex color
                hex_color = color_str[1:]
                if len(hex_color) == 6:
                    try:
                        r = int(hex_color[0:2], 16)
                        g = int(hex_color[2:4], 16)
                        b = int(hex_color[4:6], 16)
                        return r, g, b, 255
                    except ValueError as e:
                        raise ConversionError(
                            f"Invalid hex color format: {color_str}"
                        ) from e
                else:
                    raise ConversionError(
                        f"Hex color must be 6 characters: {color_str}"
                    )

            # Named colors (basic set)
            color_map = {
                "black": (0, 0, 0, 255),
                "white": (255, 255, 255, 255),
                "red": (255, 0, 0, 255),
                "green": (0, 255, 0, 255),
                "blue": (0, 0, 255, 255),
                "transparent": (0, 0, 0, 0),
            }

            result = color_map.get(color_str.lower(), (0, 0, 0, 255))
            if color_str.lower() not in color_map:
                self.out.out_warning(f"Unknown color '{color_str}', using black")

            return result

        except ConversionError:
            raise
        except Exception as e:
            error_msg = f"Error parsing color: {e}"
            self.out.out_error(error_msg)
            raise ConversionError(error_msg) from e


def convert_svg_to_bitmap(
    source_path: Path, destination_path: Path, output_handler: OutputHandler
) -> None:
    """Convert an SVG file to bitmap format.

    Args:
        source_path: Path to the source SVG file.
        destination_path: Path to destination bitmap file.
        output_handler: Output handler for messages.

    Raises:
        ConversionError: If conversion fails.
        FileNotFoundError: If the source file doesn't exist.
    """
    output_handler.out_verbose(
        f"Starting conversion from {source_path} to {destination_path}"
    )

    try:
        if not source_path.exists():
            error_msg = f"Source file not found: {source_path}"
            output_handler.out_error(error_msg)
            raise FileNotFoundError(error_msg)

        if not source_path.suffix.lower() == ".svg":
            error_msg = f"Source file must be an SVG file, got: {source_path.suffix}"
            output_handler.out_error(error_msg)
            raise ConversionError(error_msg)

        # Parse SVG
        try:
            parser = SVGParser(source_path, output_handler)
            parser.parse()
        except Exception as e:
            error_msg = f"SVG parsing failed: {e}"
            output_handler.out_error(error_msg)
            raise ConversionError(error_msg) from e

        # Convert to bitmap
        try:
            converter = BitmapConverter(parser.width, parser.height, output_handler)
            converter.convert(parser.rectangles, destination_path)
        except Exception as e:
            error_msg = f"Bitmap conversion failed: {e}"
            output_handler.out_error(error_msg)
            raise ConversionError(error_msg) from e

        output_handler.out_verbose("Conversion completed successfully")

    except (ConversionError, FileNotFoundError):
        raise
    except Exception as e:
        error_msg = f"Unexpected error during conversion: {e}"
        output_handler.out_error(error_msg)
        raise ConversionError(error_msg) from e


def setup_logging(verbosity_level: int) -> None:
    """Setup logging configuration based on verbosity level.

    Args:
        verbosity_level: Logging verbosity (0=quiet, 1=normal, 2=verbose).
    """
    try:
        if verbosity_level == 0:
            log_level = logging.ERROR
            log_format = "%(levelname)s: %(message)s"
        elif verbosity_level == 2:
            log_level = logging.INFO
            log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        else:
            log_level = logging.WARNING
            log_format = "%(levelname)s: %(message)s"

        logging.basicConfig(
            level=log_level, format=log_format, datefmt="%Y-%m-%d %H:%M:%S"
        )

    except Exception as e:
        print(f"[Error setting up logging: {e}]")


def main() -> None:
    """Main entry point for the SVG to bitmap converter."""
    try:
        parser = argparse.ArgumentParser(
            description="Convert simple SVG files (rectangles only) to bitmap format",
            epilog="Supported output formats: BMP, PNG, JPEG, TIFF, etc.",
            formatter_class=argparse.RawDescriptionHelpFormatter,
        )

        parser.add_argument("source", type=Path, help="Source SVG file path")

        parser.add_argument(
            "destination",
            type=Path,
            help="Destination bitmap file path (supports BMP, PNG, etc.)",
        )

        parser.add_argument(
            "--verbose",
            "-v",
            action="store_true",
            help="Enable verbose output with detailed information",
        )

        parser.add_argument(
            "--quiet", "-q", action="store_true", help="Quiet mode - only show errors"
        )

        parser.add_argument(
            "--no-color", action="store_true", help="Disable colored output"
        )

        args = parser.parse_args()

        # Validate mutually exclusive options
        if args.verbose and args.quiet:
            print("Error: --verbose and --quiet options are mutually exclusive")
            sys.exit(1)

        # Determine verbosity level
        if args.quiet:
            verbosity_level = 0
        elif args.verbose:
            verbosity_level = 2
        else:
            verbosity_level = 1

        # Setup logging and output handler
        setup_logging(verbosity_level)
        output_handler = OutputHandler(verbosity_level, args.no_color)

        if verbosity_level == 2:
            output_handler.out_info("Verbose mode enabled")
        elif verbosity_level == 0:
            output_handler.out_error("Quiet mode enabled - only errors will be shown")

        # Perform conversion
        try:
            convert_svg_to_bitmap(args.source, args.destination, output_handler)
            if verbosity_level > 0:
                output_handler.out_success(
                    f"Successfully converted {args.source} to {args.destination}"
                )
        except (ConversionError, FileNotFoundError) as e:
            output_handler.out_error(f"Conversion failed: {e}")
            sys.exit(1)
        except KeyboardInterrupt:
            output_handler.out_error("Conversion interrupted by user")
            sys.exit(130)
        except Exception as e:
            output_handler.out_error(f"Unexpected error: {e}")
            if verbosity_level == 2:
                import traceback

                output_handler.out_error(f"Traceback: {traceback.format_exc()}")
            sys.exit(1)

    except KeyboardInterrupt:
        print("Program interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"Fatal error during startup: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
