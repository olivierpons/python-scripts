# -*- coding: utf-8 -*-
"""
Generates an SVG pattern for a foldable, straight-walled vase with a triangular base.

This script produces a single-page SVG file that can be printed and cut out
to create a physical paper or cardboard model. The pattern consists of a central
triangular base, three rectangular walls, and rounded corners that allow the
flat pattern to be folded into a 3D shape.

The generated SVG distinguishes between cut lines (solid black) and fold lines
(dashed gray).
"""

import math
from typing import Tuple

import svgwrite

# --- Type Alias for Clarity ---
Vector2D = Tuple[float, float]

# --- Constants ---
PAGE_WIDTH_MM = 210  # A4 paper width
PAGE_HEIGHT_MM = 297  # A4 paper height


# --- Vector Geometry Helper Functions ---


def add_vectors(v1: Vector2D, v2: Vector2D) -> Vector2D:
    """Adds two 2D vectors component-wise.

    Args:
        v1: The first vector (x1, y1).
        v2: The second vector (x2, y2).

    Returns:
        The resulting vector from the addition (x1+x2, y1+y2).

    Example:
        >>> add_vectors((1, 2), (3, 4))
        (4, 6)
    """
    return v1[0] + v2[0], v1[1] + v2[1]


def subtract_vectors(v1: Vector2D, v2: Vector2D) -> Vector2D:
    """Subtracts the second 2D vector from the first.

    Args:
        v1: The vector to subtract from (x1, y1).
        v2: The vector to subtract (x2, y2).

    Returns:
        The resulting vector from the subtraction (x1-x2, y1-y2).

    Example:
        >>> subtract_vectors((5, 5), (1, 2))
        (4, 3)
    """
    return v1[0] - v2[0], v1[1] - v2[1]


def scale_vector(v: Vector2D, s: float) -> Vector2D:
    """Scales a 2D vector by a scalar factor.

    Args:
        v: The vector to scale (x, y).
        s: The scalar multiplier.

    Returns:
        The scaled vector (x*s, y*s).

    Example:
        >>> scale_vector((3, -4), 1.5)
        (4.5, -6.0)
    """
    return v[0] * s, v[1] * s


def normalize_vector(v: Vector2D) -> Vector2D:
    """Normalizes a 2D vector to a unit length of 1.

    Args:
        v: The vector to normalize (x, y).

    Returns:
        The normalized unit vector. Returns (0, 0) for a zero vector.

    Example:
        >>> normalize_vector((3, 4))
        (0.6, 0.8)
    """
    magnitude = math.sqrt(v[0] ** 2 + v[1] ** 2)
    if magnitude == 0:
        return 0.0, 0.0
    return v[0] / magnitude, v[1] / magnitude


def get_perpendicular_vector(v: Vector2D) -> Vector2D:
    """Calculates a vector that is perpendicular (rotated 90 degrees counter-clockwise).

    Args:
        v: The input vector (x, y).

    Returns:
        The perpendicular vector (-y, x).

    Example:
        >>> get_perpendicular_vector((2, 3))
        (-3, 2)
    """
    return -v[1], v[0]


def generate_straight_vase_pattern(
    base_edge_mm: float = 80.0,
    wall_height_mm: float = 120.0,
    filename: str = "vase_pattern.svg",
) -> None:
    """
    Generates an SVG pattern for a vase with a triangular base and straight walls.

    The function creates an A4-sized SVG file centered on the page. The pattern
    includes a central equilateral triangle (the base) marked with fold lines,
    and an outer boundary marked with cut lines. When cut and folded, this
    pattern forms a 3D vase.

    Args:
        base_edge_mm: The length of one edge of the equilateral triangle base in mm.
        wall_height_mm: The final height of the vase's walls in mm.
        filename: The name of the SVG file to create.
    """
    # --- SVG Document Setup ---
    dwg = svgwrite.Drawing(
        filename,
        size=(f"{PAGE_WIDTH_MM}mm", f"{PAGE_HEIGHT_MM}mm"),
        profile="tiny",
    )
    dwg.viewbox(0, 0, PAGE_WIDTH_MM, PAGE_HEIGHT_MM)

    # --- Page Center Calculation ---
    center_x: float = PAGE_WIDTH_MM / 2
    center_y: float = PAGE_HEIGHT_MM / 2

    # --- Base Triangle Geometry ---
    s: float = base_edge_mm
    triangle_height: float = s * math.sqrt(3) / 2

    # Vertices of the base triangle, centered on the page
    v1: Vector2D = (center_x, center_y - (2 / 3) * triangle_height)
    v2: Vector2D = (center_x + s / 2, center_y + (1 / 3) * triangle_height)
    v3: Vector2D = (center_x - s / 2, center_y + (1 / 3) * triangle_height)

    # --- Pattern Drawing ---

    # 1. Base Triangle (Fold Lines)
    fold_line_triangle = dwg.polygon(
        points=[v1, v2, v3],
        fill="none",
        stroke="gray",
        stroke_width=0.5,
        stroke_dasharray="4 2",
    )
    dwg.add(fold_line_triangle)

    # 2. Outer Contour (Cut Lines)
    # This contour is composed of three straight wall tops and three corner arcs.

    # Calculate side vectors and their outward-pointing perpendicular normals
    side_vec_12 = subtract_vectors(v2, v1)
    side_vec_23 = subtract_vectors(v3, v2)
    side_vec_31 = subtract_vectors(v1, v3)

    normal_vec_12 = normalize_vector(get_perpendicular_vector(side_vec_12))
    normal_vec_23 = normalize_vector(get_perpendicular_vector(side_vec_23))
    normal_vec_31 = normalize_vector(get_perpendicular_vector(side_vec_31))

    # Calculate the corner points of the unfolded outer walls
    # For each vertex (v1, v2, v3), there are two outer points that define the arc
    wall_corner_1a = add_vectors(v1, scale_vector(normal_vec_31, wall_height_mm))
    wall_corner_1b = add_vectors(v1, scale_vector(normal_vec_12, wall_height_mm))

    wall_corner_2a = add_vectors(v2, scale_vector(normal_vec_12, wall_height_mm))
    wall_corner_2b = add_vectors(v2, scale_vector(normal_vec_23, wall_height_mm))

    wall_corner_3a = add_vectors(v3, scale_vector(normal_vec_23, wall_height_mm))
    wall_corner_3b = add_vectors(v3, scale_vector(normal_vec_31, wall_height_mm))

    # Construct the SVG path string for the outer cutting line
    cut_path_str = (
        f"M {wall_corner_1a[0]},{wall_corner_1a[1]} "
        f"A {wall_height_mm},{wall_height_mm} 0 0 1 {wall_corner_1b[0]},{wall_corner_1b[1]} "
        f"L {wall_corner_2a[0]},{wall_corner_2a[1]} "
        f"A {wall_height_mm},{wall_height_mm} 0 0 1 {wall_corner_2b[0]},{wall_corner_2b[1]} "
        f"L {wall_corner_3a[0]},{wall_corner_3a[1]} "
        f"A {wall_height_mm},{wall_height_mm} 0 0 1 {wall_corner_3b[0]},{wall_corner_3b[1]} "
        f"L {wall_corner_1a[0]},{wall_corner_1a[1]} "
        "Z"
    )

    cut_path = dwg.path(d=cut_path_str, fill="none", stroke="black", stroke_width=0.5)
    dwg.add(cut_path)

    # # --- Add Informational Text ---
    # info_text = dwg.text(
    #     f"Straight Vase Pattern - Base: {s}mm, Height: {wall_height_mm}mm",
    #     insert=(10, PAGE_HEIGHT_MM - 10),
    #     fill="black",
    #     font_size="10px",
    #     font_family="Arial",
    # )
    # instruction_text = dwg.text(
    #     "Solid Line = Cut | Dashed Line = Fold",
    #     insert=(10, PAGE_HEIGHT_MM - 20),
    #     fill="black",
    #     font_size="10px",
    #     font_family="Arial",
    # )
    # dwg.add(info_text)
    # dwg.add(instruction_text)

    # --- Save the File ---
    dwg.save()
    print(f"Pattern successfully generated in file: '{filename}'")


# --- Script Execution ---
if __name__ == "__main__":
    # --- Customize your dimensions here ---

    # The edge length of the triangle base in millimeters (e.g., 8 cm = 80 mm)
    BASE_EDGE_LENGTH_MM: float = 80.0

    # The final height of the vase's walls in millimeters (e.g., 12 cm = 120 mm)
    # This can be made much larger than the base for a tall, narrow vase.
    WALL_HEIGHT_MM: float = 120.0

    # The output filename for the SVG pattern.
    OUTPUT_FILENAME: str = (
        f"vase_pattern_{int(BASE_EDGE_LENGTH_MM)}x{int(WALL_HEIGHT_MM)}.svg"
    )

    # --- Generate the pattern ---
    print("Generating vase pattern...")
    generate_straight_vase_pattern(
        base_edge_mm=BASE_EDGE_LENGTH_MM,
        wall_height_mm=WALL_HEIGHT_MM,
        filename=OUTPUT_FILENAME,
    )
