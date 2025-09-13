"""Seamless sphere texture generator for Blender and Godot.

This module generates and converts textures optimized for spherical mapping
in 3D applications, using equirectangular projection to avoid seams.

Features:
    - Convert flat textures to seamless sphere-ready format
    - Generate procedural textures (Earth-like, gas giants, marble)
    - Optimize for Blender and Godot engines
    - Apply pole distortion fixes for better sphere mapping
    - Support multiple output formats and resolutions

Supported Texture Types:
    earth: Realistic planet textures with continents, oceans, and mountains
    gas_giant: Banded gas giant textures with turbulent atmospheric effects
    marble: Elegant marble patterns with realistic veining

Usage Examples:
    Basic Earth texture generation with Jupiter palette:
        >>> from sphere_texture_generator import SphereTextureGenerator, TextureConfig
        >>> config = TextureConfig(width=2048, height=1024)
        >>> generator = SphereTextureGenerator(config)
        >>> generator.generate_procedural("earth", ocean_color=(255,165,0), land_color=(204,85,0), mountain_color=(153,101,21))

    Custom gas giant with Neptune palette:
        >>> generator.generate_procedural("gas_giant", base_colors=[(173,216,230),(0,255,255),(0,0,139),(106,90,205)])

    Marble with Europa palette:
        >>> generator.generate_procedural("marble", base_color=(255,255,255), vein_color=(202,225,255))

    Convert existing image:
        >>> from pathlib import Path
        >>> generator.convert_image(Path("my_texture.jpg"))

Command Line Examples:
    # Earth with Neptune palette
    python sphere_texture_generator.py -m procedural -t earth -r 1k -s 202 \
        --base-colors neptune -o earth_neptune_1k_seed202.png

    # Gas giant with Jupiter palette
    python sphere_texture_generator.py -m procedural -t gas_giant -r 1k -s 203 \
        --base-colors jupiter -o gas_giant_jupiter_1k_seed203.png

    # Marble with Venus palette
    python sphere_texture_generator.py -m procedural -t marble -r 1k -s 204 \
        --base-colors venus -o marble_venus_1k_seed204.png

    # Custom colors via JSON
    python sphere_texture_generator.py -m procedural -t gas_giant -r 1k -s 205 \
        --base-colors '[[0,201,87],[173,255,47],[255,255,0],[128,128,0]]' \
        -o gas_giant_custom_1k_seed205.png

Resolution Guidelines:
    256x128: Mobile preview (very fast, low detail)
    512x256: Mobile/testing (fast generation)
    1024x512: Preview/low-detail game objects
    2048x1024: Standard game quality
    4096x2048: High-quality cinematics
    8192x4096: Ultra-high detail (large file sizes)

Integration Notes:
    Blender: Import as Image Texture, set Projection to 'Sphere'
    Godot: Use as albedo texture on SphereMesh with UV mapping
    Unity: Apply to sphere primitive with UV Sphere mapping
"""

import argparse
import json
import logging
import math
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, TypeAlias

import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from noise import pnoise2

# Configure logging
logger: logging.Logger = logging.getLogger(__name__)

# Type definitions
ColorTuple: TypeAlias = tuple[int, int, int] | tuple[int, int, int, int]
NoiseFunction: type = Callable[[float, float], float]
TextureArray: type = np.ndarray

# Standard resolution presets
STANDARD_RESOLUTIONS: dict[str, tuple[int, int]] = {
    "128": (256, 128),
    "256": (512, 256),
    "512": (1024, 512),
    "1k": (2048, 1024),
    "2k": (4096, 2048),
    "4k": (8192, 4096),
    "8k": (16384, 8192),
}

# Predefined color palettes for all texture types
PREDEFINED_PALETTES: dict[str, list[ColorTuple]] = {
    "jupiter": [(255, 165, 0), (204, 85, 0), (153, 101, 21), (111, 78, 55)],
    "neptune": [(173, 216, 230), (0, 255, 255), (0, 0, 139), (106, 90, 205)],
    "saturn": [(153, 50, 204), (128, 0, 128), (230, 230, 250), (221, 160, 221)],
    "venus": [(0, 201, 87), (173, 255, 47), (255, 255, 0), (128, 128, 0)],
    "mars": [(178, 34, 34), (255, 127, 80), (165, 42, 42), (250, 128, 114)],
    "mercury": [(169, 169, 169), (192, 192, 192), (47, 79, 79), (211, 211, 211)],
    "uranus": [(64, 224, 208), (0, 128, 128), (0, 150, 136), (152, 251, 152)],
    "pluto": [(0, 0, 0), (69, 47, 32), (54, 54, 54), (139, 62, 47)],
    "titan": [(255, 215, 0), (218, 165, 32), (184, 134, 11), (250, 235, 215)],
    "europa": [(255, 255, 255), (202, 225, 255), (240, 248, 255), (176, 224, 230)],
    "marble_classic": [(245, 245, 220), (105, 105, 105)],
    "marble_onyx": [(30, 30, 30), (255, 215, 0)],
    "marble_emerald": [(240, 255, 240), (0, 100, 0)],
}


@dataclass
class TextureConfig:
    """Configuration for texture generation.

    Attributes:
        width: Texture width in pixels.
        height: Texture height in pixels.
        output_path: Path to save the generated texture.
        format: Output image format (PNG or JPEG).
        quality: JPEG quality (1-100) if the format is JPEG.
    """

    width: int = 2048
    height: int = 1024
    output_path: Path = field(default_factory=lambda: Path("output.png"))
    format: str = "PNG"
    quality: int = 95

    def __post_init__(self) -> None:
        """Validate configuration after initialization."""
        if self.width <= 0 or self.height <= 0:
            raise ValueError("Width and height must be positive")

        if self.width != 2 * self.height:
            logger.warning(
                f"Non-standard aspect ratio {self.width}:{self.height}. "
                "Equirectangular projection recommends 2:1 ratio."
            )


@dataclass
class NoiseConfig:
    """Configuration for procedural noise generation.

    Attributes:
        octaves: Number of noise octaves.
        persistence: Noise persistence (0 to 1).
        lacunarity: Noise lacunarity.
        scale: Noise scale factor.
        seed: Random seed for noise generation.
        coordinate_mode: Coordinate system for noise ('xy' or 'xz').
    """

    octaves: int = 6
    persistence: float = 0.5
    lacunarity: float = 2.0
    scale: float = 100.0
    seed: int = 42
    coordinate_mode: str = "xy"

    def __post_init__(self) -> None:
        """Validate noise parameters."""
        if self.octaves < 1:
            raise ValueError("Octaves must be at least 1")
        if not 0 < self.persistence < 1:
            raise ValueError("Persistence must be between 0 and 1")
        if self.scale <= 0:
            raise ValueError("Scale must be positive")
        if self.coordinate_mode not in ("xy", "xz"):
            raise ValueError("Coordinate mode must be 'xy' or 'xz'")


class EquirectangularConverter:
    """Convert images to equirectangular projection for seamless sphere mapping."""

    def __init__(self, config: TextureConfig) -> None:
        """Initialize converter with configuration.

        Args:
            config: Texture configuration object.
        """
        self.config: TextureConfig = config
        self.x_coords: np.ndarray
        self.y_coords: np.ndarray
        self.theta_grid: np.ndarray
        self.phi_grid: np.ndarray
        self._setup_coordinate_mappings()

    def _setup_coordinate_mappings(self) -> None:
        """Pre-calculate coordinate mappings for performance."""
        self.x_coords = np.linspace(0, 2 * np.pi, self.config.width, endpoint=False)
        self.y_coords = np.linspace(0, np.pi, self.config.height, endpoint=True)

        # Create meshgrid for vectorized operations
        self.theta_grid, self.phi_grid = np.meshgrid(self.x_coords, self.y_coords)

    def convert_image_to_equirectangular(self, input_path: Path) -> Image.Image:
        """Convert flat image to equirectangular projection.

        Args:
            input_path: Path to the input image.

        Returns:
            Equirectangular projected image.

        Raises:
            FileNotFoundError: If the input file does not exist.
            ValueError: If image loading fails.
        """
        if not input_path.exists():
            raise FileNotFoundError(f"Input file not found: {input_path}")

        try:
            source_img: Image.Image = Image.open(input_path).convert("RGB")
        except Exception as e:
            raise ValueError(f"Cannot load image {input_path}: {e}") from e

        logger.info(f"Converting {input_path} to equirectangular format")

        # Resize the source to square for easier spherical mapping
        size: int = min(source_img.size)
        source_img = source_img.resize((size, size), Image.Resampling.LANCZOS)
        return self._apply_spherical_projection(source_img)

    def _apply_spherical_projection(self, source_img: Image.Image) -> Image.Image:
        """Apply spherical projection to create seamless texture.

        Args:
            source_img: Input image to project.

        Returns:
            Projected image in equirectangular format.
        """
        result_array: TextureArray = np.zeros(
            (self.config.height, self.config.width, 3), dtype=np.uint8
        )
        source_array: np.ndarray = np.array(source_img)
        source_height, source_width = source_array.shape[:2]

        for y in range(self.config.height):
            for x in range(self.config.width):
                # Convert to spherical coordinates
                theta: float = float(self.theta_grid[y, x].item())
                phi: float = float(self.phi_grid[y, x].item())
                # Convert to 3D coordinates on a unit sphere
                sphere_x: float = math.sin(phi) * math.cos(theta)
                sphere_y: float = math.cos(phi)
                sphere_z: float = math.sin(phi) * math.sin(theta)
                # Project to plane coordinates
                plane_x: int = int(
                    (math.atan2(sphere_z, sphere_x) + math.pi)
                    / (2 * math.pi)
                    * source_width
                )
                plane_y: int = int((math.acos(sphere_y) / math.pi) * source_height)
                # Ensure coordinates are within bounds
                plane_x = max(0, min(plane_x, source_width - 1))
                plane_y = max(0, min(plane_y, source_height - 1))
                result_array[y, x] = source_array[plane_y, plane_x]

        return Image.fromarray(result_array)


class ProceduralTextureGenerator:
    """Generate procedural textures suitable for sphere mapping."""

    def __init__(self, config: TextureConfig, noise_config: NoiseConfig) -> None:
        """Initialize generator with configurations.

        Args:
            config: Texture configuration object.
            noise_config: Noise configuration object.
        """
        self.config: TextureConfig = config
        self.noise_config: NoiseConfig = noise_config
        np.random.seed(noise_config.seed)

    @staticmethod
    def _apply_color_variation(base_color: ColorTuple, variation: int) -> ColorTuple:
        """Apply variation to a color tuple, clamping values between 0 and 255.

        Args:
            base_color: Input RGB or RGBA color tuple.
            variation: Variation to apply to each color component.

        Returns:
            Color tuple with variation applied (RGB or RGBA).

        Raises:
            ValueError: If base_color has invalid length.
        """
        if len(base_color) not in (3, 4):
            raise ValueError("Color tuple must have 3 or 4 components")
        if len(base_color) == 3:
            return (
                max(0, min(255, base_color[0] + variation)),
                max(0, min(255, base_color[1] + variation)),
                max(0, min(255, base_color[2] + variation)),
            )
        return (
            max(0, min(255, base_color[0] + variation)),
            max(0, min(255, base_color[1] + variation)),
            max(0, min(255, base_color[2] + variation)),
            max(0, min(255, base_color[3] + variation)),
        )

    def generate_earth_like_texture(
        self,
        ocean_color: ColorTuple = (65, 105, 225),
        land_color: ColorTuple = (34, 139, 34),
        mountain_color: ColorTuple = (139, 69, 19),
    ) -> Image.Image:
        """Generate Earth-like texture with continents and oceans.

        Args:
            ocean_color: RGB color for oceans.
            land_color: RGB color for land.
            mountain_color: RGB color for mountains.

        Returns:
            Generated Earth-like texture image.

        Raises:
            ValueError: If color tuples have invalid lengths.
        """
        logger.info("Generating Earth-like procedural texture")
        texture_array: TextureArray = np.zeros(
            (self.config.height, self.config.width, 3), dtype=np.uint8
        )

        for color in (ocean_color, land_color, mountain_color):
            if len(color) not in (3, 4):
                raise ValueError("Color tuples must have 3 or 4 components")

        for y in range(self.config.height):
            for x in range(self.config.width):
                lon: float = (x / self.config.width) * 2 * math.pi
                lat: float = (y / self.config.height) * math.pi
                height: float = self._generate_height_value(lon, lat)
                color: ColorTuple
                if height < 0.3:
                    color = ocean_color
                elif height < 0.6:
                    color = land_color
                else:
                    color = mountain_color
                variation: int = int(self._generate_noise_value(lon * 4, lat * 4) * 30)
                final_color: ColorTuple = self._apply_color_variation(color, variation)
                texture_array[y, x] = final_color[:3]

        return Image.fromarray(texture_array)

    def generate_gas_giant_texture(
        self, base_colors: list[ColorTuple] | None = None
    ) -> Image.Image:
        """Generate gas giant style texture with bands and swirls.

        Args:
            base_colors: List of RGB colors for bands. Uses default if None.

        Returns:
            Generated gas giant texture image.

        Raises:
            ValueError: If base_colors is empty or contains invalid color tuples.
        """
        if base_colors is None:
            base_colors = [
                (255, 140, 0),  # Orange
                (255, 165, 0),  # Dark orange
                (139, 69, 19),  # Brown
                (160, 82, 45),  # Saddle brown
            ]

        if not base_colors:
            raise ValueError("base_colors cannot be empty")
        for color in base_colors:
            if len(color) not in (3, 4):
                raise ValueError("Color tuples must have 3 or 4 components")

        logger.info("Generating gas giant procedural texture")
        texture_array: TextureArray = np.zeros(
            (self.config.height, self.config.width, 3), dtype=np.uint8
        )

        for y in range(self.config.height):
            for x in range(self.config.width):
                lon: float = (x / self.config.width) * 2 * math.pi
                lat: float = (y / self.config.height) * math.pi
                band_factor: float = math.sin(lat * 6) * 0.5 + 0.5
                turbulence: float = self._generate_turbulence(lon, lat)
                band_factor = (band_factor + turbulence * 0.3) % 1.0
                color_index: int = int(band_factor * len(base_colors))
                color_index = max(0, min(color_index, len(base_colors) - 1))
                base_color: ColorTuple = base_colors[color_index]
                variation: int = int(self._generate_noise_value(lon * 2, lat * 2) * 40)
                final_color: ColorTuple = self._apply_color_variation(
                    base_color, variation
                )
                texture_array[y, x] = final_color[:3]

        return Image.fromarray(texture_array)

    def generate_marble_texture(
        self,
        base_color: ColorTuple = (240, 240, 240),
        vein_color: ColorTuple = (128, 128, 128),
    ) -> Image.Image:
        """Generate marble-like texture with veins.

        Args:
            base_color: RGB color for marble base.
            vein_color: RGB color for marble veins.

        Returns:
            Generated marble texture image.

        Raises:
            ValueError: If base_color or vein_color have invalid lengths.
        """
        logger.info("Generating marble procedural texture")
        texture_array: TextureArray = np.zeros(
            (self.config.height, self.config.width, 3), dtype=np.uint8
        )

        for color in (base_color, vein_color):
            if len(color) not in (3, 4):
                raise ValueError("Color tuples must have 3 or 4 components")

        for y in range(self.config.height):
            for x in range(self.config.width):
                lon: float = (x / self.config.width) * 2 * math.pi
                lat: float = (y / self.config.height) * math.pi
                marble_value: float = (
                    math.sin((lon + lat) * 4 + self._generate_turbulence(lon, lat) * 3)
                    * 0.5
                    + 0.5
                )
                final_color: ColorTuple = (
                    int(
                        base_color[0] * (1 - marble_value)
                        + vein_color[0] * marble_value
                    ),
                    int(
                        base_color[1] * (1 - marble_value)
                        + vein_color[1] * marble_value
                    ),
                    int(
                        base_color[2] * (1 - marble_value)
                        + vein_color[2] * marble_value
                    ),
                )
                texture_array[y, x] = final_color

        return Image.fromarray(texture_array)

    def _generate_height_value(self, lon: float, lat: float) -> float:
        """Generate height value using Perlin noise.

        Args:
            lon: Longitude in radians.
            lat: Latitude in radians.

        Returns:
            Normalized height value between 0 and 1.
        """
        coord1, coord2 = self._get_noise_coordinates(lon, lat)
        height: float = 0.0
        amplitude: float = 1.0
        frequency: float = self.noise_config.scale

        for _ in range(self.noise_config.octaves):
            height += (
                pnoise2(
                    coord1 * frequency,
                    coord2 * frequency,
                    octaves=1,
                    persistence=self.noise_config.persistence,
                    lacunarity=self.noise_config.lacunarity,
                    base=self.noise_config.seed,
                )
                * amplitude
            )
            amplitude *= self.noise_config.persistence
            frequency *= self.noise_config.lacunarity

        return max(0.0, min(1.0, (height + 1.0) * 0.5))

    def _generate_noise_value(self, lon: float, lat: float) -> float:
        """Generate simple noise value.

        Args:
            lon: Longitude in radians.
            lat: Latitude in radians.

        Returns:
            Noise value.
        """
        coord1, coord2 = self._get_noise_coordinates(lon, lat)
        return pnoise2(coord1, coord2, octaves=2, base=self.noise_config.seed)

    def _get_noise_coordinates(self, lon: float, lat: float) -> tuple[float, float]:
        """Convert spherical coordinates to noise coordinates based on mode.

        Args:
            lon: Longitude in radians.
            lat: Latitude in radians.

        Returns:
            Tuple of (coord1, coord2) for noise generation, based on coordinate_mode
            ('xy' or 'xz').
        """
        x: float = math.cos(lat) * math.cos(lon)
        y: float = math.cos(lat) * math.sin(lon)
        z: float = math.sin(lat)
        return (x, z) if self.noise_config.coordinate_mode == "xz" else (x, y)

    def _generate_turbulence(self, lon: float, lat: float) -> float:
        """Generate turbulence for gas giant effects.

        Args:
            lon: Longitude in radians.
            lat: Latitude in radians.

        Returns:
            Turbulence value.
        """
        coord1, coord2 = self._get_noise_coordinates(lon, lat)
        turbulence: float = 0.0
        scale: float = 1.0

        for _ in range(4):
            turbulence += (
                abs(
                    pnoise2(
                        coord1 * scale,
                        coord2 * scale,
                        base=self.noise_config.seed + 100,
                    )
                )
                / scale
            )
            scale *= 2.0

        return turbulence


class TextureOptimizer:
    """Optimize textures for game engine usage."""

    @staticmethod
    def apply_pole_fix(image: Image.Image) -> Image.Image:
        """Apply pole fixing to reduce polar distortion.

        Args:
            image: Input image to process.

        Returns:
            Image with fixed poles.
        """
        logger.info("Applying pole distortion fix")
        # Uniformize top and bottom rows to reduce polar distortion
        img_array: np.ndarray = np.array(image)
        for x in range(img_array.shape[1]):
            if x > 0:
                img_array[0, x] = img_array[0, 0]
                img_array[-1, x] = img_array[-1, 0]

        result: Image.Image = Image.fromarray(img_array)

        # Apply slight gaussian blur to poles
        mask: Image.Image = Image.new("L", result.size, 0)
        draw: ImageDraw.Draw = ImageDraw.Draw(mask)

        # Create gradient mask for poles
        height: int = result.size[1]
        pole_height: int = height // 10

        for y in range(pole_height):
            alpha: int = int(255 * (1 - y / pole_height))
            draw.rectangle([0, y, result.size[0], y + 1], fill=alpha)
            draw.rectangle([0, height - y - 1, result.size[0], height - y], fill=alpha)

        blurred: Image.Image = result.filter(ImageFilter.GaussianBlur(radius=1))
        return Image.composite(blurred, result, mask)

    @staticmethod
    def optimize_for_godot(
        image: Image.Image, target_format: str = "PNG"
    ) -> Image.Image:
        """Optimize image for Godot engine.

        Args:
            image: Input image to optimize.
            target_format: Output format ('PNG' or 'JPEG').

        Returns:
            Optimized image for Godot.
        """
        logger.info(f"Optimizing texture for Godot ({target_format} format)")
        width, height = image.size
        new_width: int = 2 ** math.ceil(math.log2(width))
        new_height: int = 2 ** math.ceil(math.log2(height))

        if new_width != width or new_height != height:
            logger.info(f"Resizing to power-of-two: {new_width}x{new_height}")
            image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)

        return image


class SphereTextureGenerator:
    """Main class for generating sphere textures."""

    def __init__(
        self, config: TextureConfig, noise_config: NoiseConfig | None = None
    ) -> None:
        """Initialize the texture generator.

        Args:
            config: Texture configuration object.
            noise_config: Noise configuration object. Uses default if None.
        """
        self.config: TextureConfig = config
        self.noise_config: NoiseConfig = noise_config or NoiseConfig()
        self.converter: EquirectangularConverter = EquirectangularConverter(config)
        self.procedural_gen: ProceduralTextureGenerator = ProceduralTextureGenerator(
            config, self.noise_config
        )

    def convert_image(self, input_path: Path) -> None:
        """Convert the existing image to sphere-ready texture.

        Args:
            input_path: Path to the input image.

        Raises:
            FileNotFoundError: If the input file does not exist.
            ValueError: If image loading fails.
        """
        logger.info(f"Converting image: {input_path}")
        result_image: Image.Image = self.converter.convert_image_to_equirectangular(
            input_path
        )
        result_image = TextureOptimizer.apply_pole_fix(result_image)
        result_image = TextureOptimizer.optimize_for_godot(
            result_image, self.config.format
        )
        self._save_image(result_image)

    def generate_procedural(self, texture_type: str, **kwargs: Any) -> None:
        """Generate procedural texture.

        Args:
            texture_type: Type of texture to generate ('earth', 'gas_giant', 'marble').
            **kwargs: Additional arguments for texture generation.

        Raises:
            ValueError: If the texture type is unsupported.
        """
        logger.info(f"Generating procedural texture: {texture_type}")
        generators: dict[str, Callable[..., Image.Image]] = {
            "earth": self.procedural_gen.generate_earth_like_texture,
            "gas_giant": self.procedural_gen.generate_gas_giant_texture,
            "marble": self.procedural_gen.generate_marble_texture,
        }

        if texture_type not in generators:
            raise ValueError(f"Unsupported texture type: {texture_type}")

        result_image: Image.Image = generators[texture_type](**kwargs)
        result_image = TextureOptimizer.apply_pole_fix(result_image)
        result_image = TextureOptimizer.optimize_for_godot(
            result_image, self.config.format
        )
        self._save_image(result_image)

    def _save_image(self, image: Image.Image) -> None:
        """Save image to the configured output path.

        Args:
            image: Image to save.

        Raises:
            OSError: If saving fails.
        """
        self.config.output_path.parent.mkdir(parents=True, exist_ok=True)
        save_kwargs: dict[str, Any] = {}
        if self.config.format.upper() == "JPEG":
            save_kwargs["quality"] = self.config.quality
            save_kwargs["optimize"] = True

        try:
            image.save(
                self.config.output_path, format=self.config.format, **save_kwargs
            )
            logger.info(f"Saved texture: {self.config.output_path}")
        except Exception as e:
            raise OSError(f"Failed to save image: {e}") from e


def create_cli_parser() -> argparse.ArgumentParser:
    """Create command-line interface parser.

    Returns:
        Configured argument parser.

    Example:
        ```bash
        # Generate marble texture with marble_classic palette
        python sphere_texture_generator.py -m procedural -t marble -r 512 -s 202 \
            --base-colors marble_classic -o marble_classic_512_seed202.png
        ```
    """
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description="Generate seamless sphere textures for Blender and Godot",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
Examples:
    # Convert an image to equirectangular projection (PNG, 1k resolution)
    python sphere_texture_generator.py -m convert -i input.jpg -r 1k  \
        -o sphere_texture.png

    # Convert an image with custom resolution and JPEG output
    python sphere_texture_generator.py -m convert -i input.jpg -w 4096 -g 2048 \
        -f JPEG -q 90 -o sphere_texture.jpg

    # Generate Earth-like texture with jupiter palette (512x256, PNG)
    python sphere_texture_generator.py -m procedural -t earth -r 512 -s 202  \
        -a 6 -c 100.0 --base-colors jupiter -o earth_jupiter_512_seed202.png

    # Generate Earth-like texture with custom colors (1k, PNG)
    python sphere_texture_generator.py -m procedural -t earth -r 1k -s 203  \
        -a 8 -c 150.0 --base-colors '[[0,105,225],[34,139,34],[139,69,19]]'  \
        -o earth_custom_1k_seed203.png

    # Generate gas giant texture with neptune palette (2k, JPEG)
    python sphere_texture_generator.py -m procedural -t gas_giant -r 2k -s 204  \
        -a 6 -c 100.0 --base-colors neptune -f JPEG -q 90  \
        -o gas_giant_neptune_2k_seed204.jpg

    # Generate gas giant with custom colors and xz coordinate mode (256x128, PNG)
    python sphere_texture_generator.py -m procedural -t gas_giant -r 128 -s 205  \
        -a 4 -c 200.0 -d xz --base-colors '[[255,140,0],[204,85,0],[153,101,21]]'  \
        -o gas_giant_custom_128_seed205.png

    # Generate marble texture with marble_classic palette (1k, PNG)
    python sphere_texture_generator.py -m procedural -t marble -r 1k -s 206  \
        -a 6 -c 100.0 --base-colors marble_classic -o marble_classic_1k_seed206.png

    # Generate marble texture with custom colors (512x256, JPEG)
    python sphere_texture_generator.py -m procedural -t marble -r 256 -s 207  \
        -a 8 -c 120.0 --base-colors '[[245,245,220],[105,105,105]]'  \
        -f JPEG -q 85 -o marble_custom_256_seed207.jpg

    # Generate marble with marble_emerald palette and verbose output (1k, PNG)
    python sphere_texture_generator.py -m procedural -t marble -r 1k -s 208  \
        -a 6 -c 100.0 --base-colors marble_emerald -v -o marble_emerald_1k_seed208.png

    # Batch generate all textures with planetary palettes (512x256, PNG)
    mkdir -p ok/512; i=0; 
    for TYPE in earth gas_giant; do 
        for PALETTE in jupiter neptune saturn venus mars mercury uranus pluto titan europa; do 
            export PALETTE=$PALETTE; 
            python sphere_texture_generator.py -m procedural -t $TYPE -r 512  \
                -s $((202 + i)) -a 6 -c 100.0 --base-colors $PALETTE  \
                -o "ok/512/${TYPE}_${PALETTE}_512_seed$((202 + i)).png"; 
            ((i++)); 
        done; 
    done; 
    for PALETTE in jupiter neptune saturn venus mars mercury uranus pluto titan europa marble_classic marble_onyx marble_emerald; do 
        export PALETTE=$PALETTE; 
        python sphere_texture_generator.py -m procedural -t marble -r 512  \
            -s $((202 + i)) -a 6 -c 100.0 --base-colors $PALETTE  \
            -o "ok/512/marble_${PALETTE}_512_seed$((202 + i)).png"; 
        ((i++)); 
    done

Notes:
    - Predefined palettes: jupiter, neptune, saturn, venus, mars, mercury, uranus, 
      pluto, titan, europa, marble_classic, marble_onyx, marble_emerald
    - For 'earth', use 3 colors (ocean, land, mountain)
    - For 'marble', use 2 colors (base, veins)
    - For 'gas_giant', use 2+ colors for bands
    - Use -v for verbose logging
    - Resolutions: 128 (256x128), 256 (512x256), 512 (1024x512), 1k (2048x1024), 2k (4096x2048), 
                   4k (8192x4096), 8k (16384x8192)
    - Custom resolutions with -w and -g (height defaults to width/2)
""",
    )

    parser.add_argument(
        "-m",
        "--mode",
        choices=["convert", "procedural"],
        required=True,
        help="Operation mode: convert existing image or generate procedural texture",
    )
    parser.add_argument(
        "-i",
        "--input",
        type=Path,
        help="Input image path (for convert mode)",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=Path("sphere_texture.png"),
        help="Output file path",
    )
    resolution_group: argparse._ArgumentGroup = parser.add_mutually_exclusive_group()
    resolution_group.add_argument(
        "-r",
        "--resolution",
        choices=list(STANDARD_RESOLUTIONS.keys()),
        help="Standard resolution preset",
    )
    resolution_group.add_argument(
        "-w",
        "--width",
        type=int,
        help="Custom width",
    )
    parser.add_argument(
        "-g",
        "--height",
        type=int,
        help="Custom height (defaults to width/2)",
    )
    parser.add_argument(
        "-f",
        "--format",
        choices=["PNG", "JPEG"],
        default="PNG",
        help="Output format",
    )
    parser.add_argument(
        "-q",
        "--quality",
        type=int,
        default=95,
        help="JPEG quality (1-100)",
    )
    parser.add_argument(
        "-t",
        "--type",
        choices=["earth", "gas_giant", "marble"],
        help="Procedural texture type",
    )
    parser.add_argument(
        "-a",
        "--octaves",
        type=int,
        default=6,
        help="Noise octaves",
    )
    parser.add_argument(
        "-s",
        "--seed",
        type=int,
        default=42,
        help="Random seed",
    )
    parser.add_argument(
        "-c",
        "--scale",
        type=float,
        default=100.0,
        help="Noise scale",
    )
    parser.add_argument(
        "--base-colors",
        type=str,
        help="Colors for texture: either a JSON list of RGB tuples "
        f"(e.g., '[[255,140,0],[204,85,0]]') or a predefined palette name: "
        f"{', '.join(PREDEFINED_PALETTES.keys())}. "
        "For 'earth', uses first 3 colors (ocean, land, mountain). "
        "For 'marble', uses first 2 colors (base, veins). "
        "For 'gas_giant', uses all colors for bands.",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Verbose output",
    )
    parser.add_argument(
        "-d",
        "--coordinate-mode",
        choices=["xy", "xz"],
        default="xy",
        help="Noise coordinate mode: 'xy' uses x,y; 'xz' uses x,z",
    )

    return parser


def main() -> int:
    """Main application entry point.

    Returns:
        Exit code (0 for success, 1 for error).

    Raises:
        ValueError: If arguments are invalid.
        OSError: If file operations fail.
    """
    parser: argparse.ArgumentParser = create_cli_parser()
    args: argparse.Namespace = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    try:
        # Determine resolution
        width: int
        height: int
        if args.resolution:
            width, height = STANDARD_RESOLUTIONS[args.resolution]
        elif args.width:
            width = args.width
            height = args.height or args.width // 2
        else:
            width, height = 2048, 1024

        # Create configuration
        texture_config: TextureConfig = TextureConfig(
            width=width,
            height=height,
            output_path=args.output,
            format=args.format,
            quality=args.quality,
        )

        noise_config: NoiseConfig = NoiseConfig(
            octaves=args.octaves,
            seed=args.seed,
            scale=args.scale,
            coordinate_mode=args.coordinate_mode,
        )

        # Parse base_colors
        kwargs: dict[str, Any] = {}
        if args.mode == "procedural" and args.base_colors:
            colors: list[ColorTuple]
            if args.base_colors in PREDEFINED_PALETTES:
                colors = PREDEFINED_PALETTES[args.base_colors]
            else:
                try:
                    parsed_colors: Any = json.loads(args.base_colors)
                    if not isinstance(parsed_colors, list):
                        raise ValueError(
                            "base-colors JSON must be a list of RGB tuples"
                        )
                    colors: list[ColorTuple] = []
                    for color in parsed_colors:
                        if not isinstance(color, list) or len(color) not in (3, 4):
                            raise ValueError(
                                "Each color must be a list of "
                                "3 or 4 integers (RGB/RGBA)"
                            )
                        if not all(isinstance(c, int) and 0 <= c <= 255 for c in color):
                            raise ValueError(
                                "RGB values must be integers between 0 and 255"
                            )
                        if len(color) == 3:
                            r, g, b = color
                            colors.append((r, g, b))
                        else:  # len(color) == 4
                            r, g, b, a = color
                            colors.append((r, g, b, a))
                except json.JSONDecodeError:
                    parser.error(f"Invalid JSON for --base-colors: {args.base_colors}")
                except ValueError as e:
                    parser.error(f"Error in --base-colors: {e}")

            if args.type == "earth":
                if len(colors) < 3:
                    parser.error(
                        "earth requires at least 3 colors (ocean, land, mountain)"
                    )
                kwargs = {
                    "ocean_color": colors[0],
                    "land_color": colors[1],
                    "mountain_color": colors[2],
                }
            elif args.type == "marble":
                if len(colors) < 2:
                    parser.error("marble requires at least 2 colors (base, veins)")
                kwargs = {"base_color": colors[0], "vein_color": colors[1]}
            elif args.type == "gas_giant":
                if len(colors) < 2:
                    parser.error("gas_giant requires at least 2 colors")
                kwargs = {"base_colors": colors}

        # Create generator
        generator: SphereTextureGenerator = SphereTextureGenerator(
            texture_config, noise_config
        )

        # Execute based on mode
        if args.mode == "convert":
            if not args.input:
                parser.error("--input is required for convert mode")
            generator.convert_image(args.input)
        elif args.mode == "procedural":
            if not args.type:
                parser.error("--type is required for procedural mode")
            generator.generate_procedural(args.type, **kwargs)

        logger.info("✅ Operation completed successfully.")
        print("\n" + "=" * 60)
        print("📊 Generation summary")
        print("=" * 60)
        print(f"✅ File saved: {texture_config.output_path}")
        print(f"📏 Final size: {texture_config.width}x{texture_config.height}")
        print(f"📦 Format: {texture_config.format}")
        print(f"💾 File size: {texture_config.output_path.stat().st_size // 1024}KB")
        if kwargs:
            print(f"🎨 Colors: {kwargs}")
        print("=" * 60)
        return 0

    except (ValueError, OSError) as e:
        logger.error(f"Error: {e}")
        return 1


if __name__ == "__main__":
    import sys

    sys.exit(main())
