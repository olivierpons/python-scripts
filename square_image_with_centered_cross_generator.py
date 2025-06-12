#!/usr/bin/env python3
"""
Square image generator with centered cross.

This script creates a square image with a perfectly centered cross.
The size must be odd to ensure perfect centering.
"""

import argparse
import sys
from pathlib import Path
from typing import Tuple, Optional
from PIL import Image, ImageDraw


def parse_color(color_str: str) -> Tuple[int, int, int]:
    """Parse color from RGB, HEX, or INT format.

    Args:
        color_str: String representing the color (e.g., "255,0,0", "#ff0000", "128")

    Returns:
        RGB tuple (red, green, blue) with values between 0-255.

    Raises:
        ValueError: If the color format is invalid.

    Examples:
        >>> parse_color("255,0,0")
        (255, 0, 0)
        >>> parse_color("#ff0000")
        (255, 0, 0)
        >>> parse_color("128")
        (128, 128, 128)
    """
    try:
        # Try the hexadecimal format (ff00ff or #ff00ff)
        if color_str.startswith("#"):
            hex_str = color_str[1:]
        else:
            hex_str = color_str

        if len(hex_str) == 6:
            return (
                int(hex_str[0:2], 16),
                int(hex_str[2:4], 16),
                int(hex_str[4:6], 16),
            )

        # Try RGB format (255,0,255)
        if "," in color_str:
            parts = [int(x.strip()) for x in color_str.split(",")]
            if len(parts) == 3 and all(0 <= x <= 255 for x in parts):
                return tuple(parts)  # type: ignore

        # Try single INT value (grayscale)
        color_int = int(color_str)
        if 0 <= color_int <= 255:
            return color_int, color_int, color_int

    except ValueError as e:
        raise ValueError(
            f"Invalid color format: {color_str}\n"
            "Accepted formats:\n"
            "- RGB: '255,0,255' or '128,128,128'\n"
            "- HEX: 'ff00ff' or '#ff00ff'\n"
            "- INT: '128' (grayscale)"
        ) from e

    raise ValueError(f"Unrecognized color format: {color_str}")


def generate_cross_image(
    size: int,
    cross_color: Tuple[int, int, int],
    bg_color: Tuple[int, int, int],
    output_format: str = "png",
    cross_thickness: Optional[int] = None,
) -> None:
    """Generate square image with centered cross.

    Args:
        size: Image width/height (must be odd).
        cross_color: Cross color as RGB tuple.
        bg_color: Background color as an RGB tuple.
        output_format: Output format ('png' or 'webp').
        cross_thickness: Optional thickness of cross (default: size//20).

    Raises:
        ValueError: If size is even or format unsupported.
    """
    # Argument validation
    if size % 2 == 0:
        raise ValueError("Size must be odd to center the cross properly.")

    output_format = output_format.lower()
    if output_format not in ("png", "webp"):
        raise ValueError("Unsupported output format. Choose 'png' or 'webp'.")

    # Calculate cross-thickness
    thickness = cross_thickness if cross_thickness is not None else max(1, size // 20)
    if thickness <= 0:
        raise ValueError("Cross thickness must be positive")

    # Create a new image
    image = Image.new("RGB", (size, size), bg_color)
    draw = ImageDraw.Draw(image)

    # Calculate center position
    center = size // 2

    # Draw a horizontal line
    draw.rectangle(
        [(center - thickness, 0), (center + thickness, size)],
        fill=cross_color,
    )

    # Draw a vertical line
    draw.rectangle(
        [(0, center - thickness), (size, center + thickness)],
        fill=cross_color,
    )

    # Save image with format handling
    filename = f"cross_{size}_thick{thickness}.{output_format}"

    try:
        image.save(filename, format=output_format)
        print(f"✓ Image generated: {filename}")
    except ValueError:
        if output_format == "webp":
            print("⚠ WEBP format not available, using PNG instead.")
            filename = f"cross_{size}_thick{thickness}.png"
            image.save(filename, format="png")
            print(f"✓ Image generated: {filename}")
        else:
            raise


def main() -> None:
    """Main entry point for the script."""
    script_name = Path(sys.argv[0]).name
    parser = argparse.ArgumentParser(
        description="Square image generator with centered cross.",
        epilog="Usage examples:\n"
        f"  ./{script_name} -s 501 -c 255,0,0 -b ffffff\n"
        f"  ./{script_name} -s 301 -c #0000ff -b 128 -f webp -t 10\n"
        f"  ./{script_name} --size 201 --cross-color 0,255,0 --bg-color 0 --thickness 5",
        formatter_class=argparse.RawTextHelpFormatter,
    )

    # Required arguments
    parser.add_argument(
        "-s",
        "--size",
        type=int,
        required=True,
        help="Image width/height (must be odd)",
    )

    parser.add_argument(
        "-c",
        "--cross-color",
        type=str,
        required=True,
        help="Cross color (RGB: '255,0,0', HEX: 'ff0000' or INT: '128')",
    )

    parser.add_argument(
        "-b",
        "--bg-color",
        type=str,
        required=True,
        help="Background color (same formats as --cross-color)",
    )

    # Optional arguments
    parser.add_argument(
        "-f",
        "--format",
        type=str,
        choices=["png", "webp"],
        default="png",
        help="Output format (default: png)",
    )

    parser.add_argument(
        "-t",
        "--thickness",
        type=int,
        default=None,
        help="Custom cross thickness (default: auto-calculated as size//20)",
    )

    try:
        args = parser.parse_args()

        # Convert colors
        cross_color = parse_color(args.cross_color)
        bg_color = parse_color(args.bg_color)

        # Generate image
        generate_cross_image(
            size=args.size,
            cross_color=cross_color,
            bg_color=bg_color,
            output_format=args.format,
            cross_thickness=args.thickness,
        )

    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
