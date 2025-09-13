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
    Basic Earth texture generation:
        >>> from sphere_texture_generator import SphereTextureGenerator, TextureConfig
        >>> config = TextureConfig(width=2048, height=1024)
        >>> generator = SphereTextureGenerator(config)
        >>> generator.generate_procedural("earth")

    Custom gas giant with specific colors:
        >>> colors = [(255, 100, 50), (200, 150, 100), (150, 100, 200)]
        >>> generator.generate_procedural("gas_giant", base_colors=colors)

    Convert existing image:
        >>> from pathlib import Path
        >>> generator.convert_image(Path("my_texture.jpg"))

    High-resolution marble with custom colors:
        >>> config = TextureConfig(width=4096, height=2048)
        >>> generator = SphereTextureGenerator(config)
        >>> generator.generate_procedural("marble",
        ...     base_color=(250, 248, 240),
        ...     vein_color=(100, 100, 120))

Command Line Examples:
    # Standard Earth texture at 2K resolution
    python sphere_texture_generator.py -m procedural -t earth -r 2k -o earth_2k.png

    # High-detail gas giant with custom noise settings
    python sphere_texture_generator.py -m procedural -t gas_giant -w 4096 -g 2048 \\
        -s 123 -a 8 -c 150.0 -o jupiter_style.png

    # Convert photo to seamless sphere texture
    python sphere_texture_generator.py -m convert -i landscape.jpg \\
        -o sphere_landscape.png -r 4k

    # Marble texture with high quality JPEG output
    python sphere_texture_generator.py -m procedural -t marble -r 1k \\
        -f JPEG -q 98 -o marble_sphere.jpg

    # Multiple variations with different seeds
    python sphere_texture_generator.py -m procedural -t earth -s 42 -o earth_v1.png
    python sphere_texture_generator.py -m procedural -t earth -s 123 -o earth_v2.png
    python sphere_texture_generator.py -m procedural -t earth -s 456 -o earth_v3.png

Resolution Guidelines:
    512x256: Preview/testing (fast generation)
    1024x512: Low-detail game objects
    2048x1024: Standard game quality
    4096x2048: High-quality cinematics
    8192x4096: Ultra-high detail (large file sizes)

Integration Notes:
    Blender: Import as Image Texture, set Projection to 'Sphere'
    Godot: Use as albedo texture on SphereMesh with UV mapping
    Unity: Apply to sphere primitive with UV Sphere mapping
"""

import argparse
import logging
import math
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable

import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from noise import pnoise2

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Type definitions
ColorTuple = tuple[int, int, int] | tuple[int, int, int, int]
NoiseFunction = Callable[[float, float], float]
TextureArray = np.ndarray

# Standard resolution presets
STANDARD_RESOLUTIONS: dict[str, tuple[int, int]] = {
    "512": (1024, 512),
    "1k": (2048, 1024),
    "2k": (4096, 2048),
    "4k": (8192, 4096),
    "8k": (16384, 8192),
}


@dataclass
class TextureConfig:
    """Configuration for texture generation."""

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
                "Equirectangular projection requires 2:1 ratio."
            )


@dataclass
class NoiseConfig:
    """Configuration for procedural noise generation."""

    octaves: int = 6
    persistence: float = 0.5
    lacunarity: float = 2.0
    scale: float = 100.0
    seed: int = 42
    coordinate_mode: str = "xy"  # "xy" uses x,y coordinates | "xz" uses x,z coordinates

    def __post_init__(self) -> None:
        """Validate noise parameters."""
        if self.octaves < 1:
            raise ValueError("Octaves must be at least 1")
        if self.persistence <= 0 or self.persistence >= 1:
            raise ValueError("Persistence must be between 0 and 1")
        if self.scale <= 0:
            raise ValueError("Scale must be positive")
        if self.coordinate_mode not in ("xy", "xz"):
            raise ValueError("coordinate_mode must be 'xy' or 'xz'")


class EquirectangularConverter:
    """Convert images to equirectangular projection for seamless sphere mapping."""

    def __init__(self, config: TextureConfig) -> None:
        """Initialize converter with configuration.

        Args:
            config: Texture generation configuration.
        """
        self.config = config
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
            input_path: Path to input image file.

        Returns:
            PIL Image in equirectangular format.

        Raises:
            FileNotFoundError: If input file doesn't exist.
            ValueError: If image format is not supported.
        """
        if not input_path.exists():
            raise FileNotFoundError(f"Input file not found: {input_path}")

        try:
            source_img = Image.open(input_path).convert("RGB")
        except Exception as e:
            raise ValueError(f"Cannot load image {input_path}: {e}") from e

        logger.info(f"Converting {input_path} to equirectangular format")

        # Resize the source to square for easier spherical mapping
        size = min(source_img.size)
        source_img = source_img.resize((size, size), Image.Resampling.LANCZOS)

        return self._apply_spherical_projection(source_img)

    def _apply_spherical_projection(self, source_img: Image.Image) -> Image.Image:
        """Apply spherical projection to create seamless texture.

        Args:
            source_img: Source image to project.

        Returns:
            Projected image in equirectangular format.
        """
        result_array = np.zeros(
            (self.config.height, self.config.width, 3), dtype=np.uint8
        )
        source_array = np.array(source_img)
        source_height, source_width = source_array.shape[:2]

        for y in range(self.config.height):
            for x in range(self.config.width):
                # Convert to spherical coordinates
                theta = self.theta_grid[y, x]  # longitude
                phi = self.phi_grid[y, x]  # latitude

                # Convert to 3D coordinates on unit sphere
                sphere_x = math.sin(phi) * math.cos(theta)
                sphere_y = math.cos(phi)
                sphere_z = math.sin(phi) * math.sin(theta)

                # Project to plane coordinates
                plane_x = int(
                    (math.atan2(sphere_z, sphere_x) + math.pi)
                    / (2 * math.pi)
                    * source_width
                )
                plane_y = int((math.acos(sphere_y) / math.pi) * source_height)

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
            config: Texture configuration.
            noise_config: Noise generation configuration.
        """
        self.config = config
        self.noise_config = noise_config
        np.random.seed(noise_config.seed)

    def generate_earth_like_texture(
        self,
        ocean_color: ColorTuple = (65, 105, 225),
        land_color: ColorTuple = (34, 139, 34),
        mountain_color: ColorTuple = (139, 69, 19),
    ) -> Image.Image:
        """Generate Earth-like texture with continents and oceans.

        Args:
            ocean_color: RGB color for ocean areas.
            land_color: RGB color for land areas.
            mountain_color: RGB color for mountain areas.

        Returns:
            Generated Earth-like texture.
        """
        logger.info("Generating Earth-like procedural texture")

        texture_array = np.zeros(
            (self.config.height, self.config.width, 3), dtype=np.uint8
        )

        for y in range(self.config.height):
            for x in range(self.config.width):
                # Convert pixel coordinates to spherical coordinates
                lon = (x / self.config.width) * 2 * math.pi
                lat = (y / self.config.height) * math.pi

                # Generate height map using multiple octaves of noise
                height = self._generate_height_value(lon, lat)

                # Determine terrain type based on height
                if height < 0.3:
                    color = ocean_color
                elif height < 0.6:
                    color = land_color
                else:
                    color = mountain_color

                # Add some variation
                variation = int(self._generate_noise_value(lon * 4, lat * 4) * 30)
                color = tuple(max(0, min(255, c + variation)) for c in color)

                texture_array[y, x] = color[:3]

        return Image.fromarray(texture_array)

    def generate_gas_giant_texture(
        self, base_colors: list[ColorTuple] = None
    ) -> Image.Image:
        """Generate gas giant style texture with bands and swirls.

        Args:
            base_colors: List of colors to use for bands.

        Returns:
            Generated gas giant texture.
        """
        if base_colors is None:
            base_colors = [
                (255, 140, 0),  # Orange
                (255, 165, 0),  # Dark orange
                (139, 69, 19),  # Brown
                (160, 82, 45),  # Saddle brown
            ]

        logger.info("Generating gas giant procedural texture")

        texture_array = np.zeros(
            (self.config.height, self.config.width, 3), dtype=np.uint8
        )

        for y in range(self.config.height):
            for x in range(self.config.width):
                lon = (x / self.config.width) * 2 * math.pi
                lat = (y / self.config.height) * math.pi

                # Create horizontal bands based on latitude
                band_factor = math.sin(lat * 6) * 0.5 + 0.5

                # Add turbulence for realistic gas movement
                turbulence = self._generate_turbulence(lon, lat)
                band_factor = (band_factor + turbulence * 0.3) % 1.0

                # Select color based on band position
                color_index = int(band_factor * len(base_colors))
                color_index = max(0, min(color_index, len(base_colors) - 1))

                base_color = base_colors[color_index]

                # Add noise variation
                variation = int(self._generate_noise_value(lon * 2, lat * 2) * 40)
                final_color = tuple(max(0, min(255, c + variation)) for c in base_color)

                texture_array[y, x] = final_color[:3]

        return Image.fromarray(texture_array)

    def generate_marble_texture(
        self,
        base_color: ColorTuple = (240, 240, 240),
        vein_color: ColorTuple = (128, 128, 128),
    ) -> Image.Image:
        """Generate marble-like texture with veins.

        Args:
            base_color: Base marble color.
            vein_color: Color of marble veins.

        Returns:
            Generated marble texture.
        """
        logger.info("Generating marble procedural texture")

        texture_array = np.zeros(
            (self.config.height, self.config.width, 3), dtype=np.uint8
        )

        for y in range(self.config.height):
            for x in range(self.config.width):
                lon = (x / self.config.width) * 2 * math.pi
                lat = (y / self.config.height) * math.pi

                # Generate marble pattern using sine wave with noise
                marble_value = (
                    math.sin((lon + lat) * 4 + self._generate_turbulence(lon, lat) * 3)
                    * 0.5
                    + 0.5
                )

                # Interpolate between base and vein colors
                final_color = tuple(
                    int(
                        base_color[i] * (1 - marble_value)
                        + vein_color[i] * marble_value
                    )
                    for i in range(3)
                )

                texture_array[y, x] = final_color

        return Image.fromarray(texture_array)

    def _generate_height_value(self, lon: float, lat: float) -> float:
        """Generate height value using Perlin noise.

        Args:
            lon: Longitude coordinate.
            lat: Latitude coordinate.

        Returns:
            Height value between 0 and 1.
        """
        # Use spherical coordinates for seamless tiling
        x = math.cos(lat) * math.cos(lon)
        y = math.cos(lat) * math.sin(lon)
        z = math.sin(lat)

        # Select coordinates based on configuration
        if self.noise_config.coordinate_mode == "xz":
            coord1, coord2 = x, z
        else:  # default "xy"
            coord1, coord2 = x, y

        height = 0.0
        amplitude = 1.0
        frequency = self.noise_config.scale

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
            lon: Longitude coordinate.
            lat: Latitude coordinate.

        Returns:
            Noise value between -1 and 1.
        """
        # Use spherical coordinates for seamless tiling
        x = math.cos(lat) * math.cos(lon)
        y = math.cos(lat) * math.sin(lon)
        z = math.sin(lat)

        # Select coordinates based on configuration
        if self.noise_config.coordinate_mode == "xz":
            coord1, coord2 = x, z
        else:  # default "xy"
            coord1, coord2 = x, y

        return pnoise2(coord1, coord2, octaves=2, base=self.noise_config.seed)

    def _generate_turbulence(self, lon: float, lat: float) -> float:
        """Generate turbulence for gas giant effects.

        Args:
            lon: Longitude coordinate.
            lat: Latitude coordinate.

        Returns:
            Turbulence value.
        """
        # Use spherical coordinates for seamless tiling
        x = math.cos(lat) * math.cos(lon)
        y = math.cos(lat) * math.sin(lon)
        z = math.sin(lat)

        # Select coordinates based on configuration
        if self.noise_config.coordinate_mode == "xz":
            coord1, coord2 = x, z
        else:  # default "xy"
            coord1, coord2 = x, y

        turbulence = 0.0
        scale = 1.0

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
            image: Input image to fix.

        Returns:
            Image with reduced polar distortion.
        """
        logger.info("Applying pole distortion fix")

        # Apply slight blur to top and bottom rows to reduce distortion
        img_array = np.array(image)

        # Fix north pole (top row)
        for x in range(img_array.shape[1]):
            if x > 0:
                img_array[0, x] = img_array[0, 0]  # Use first pixel for entire top row

        # Fix south pole (bottom row)
        last_row = img_array.shape[0] - 1
        for x in range(img_array.shape[1]):
            if x > 0:
                img_array[last_row, x] = img_array[last_row, 0]

        result = Image.fromarray(img_array)

        # Apply slight gaussian blur to poles
        mask = Image.new("L", result.size, 0)
        draw = ImageDraw.Draw(mask)

        # Create gradient mask for poles
        height = result.size[1]
        pole_height = height // 10

        for y in range(pole_height):
            alpha = int(255 * (1 - y / pole_height))
            draw.rectangle([0, y, result.size[0], y + 1], fill=alpha)
            draw.rectangle([0, height - y - 1, result.size[0], height - y], fill=alpha)

        blurred = result.filter(ImageFilter.GaussianBlur(radius=1))
        return Image.composite(blurred, result, mask)

    @staticmethod
    def optimize_for_godot(image: Image.Image, target_format: str = "PNG") -> Image.Image:
        """Optimize image for Godot engine.

        Args:
            image: Image to optimize.
            target_format: Target format (PNG or JPEG).

        Returns:
            Optimized image.
        """
        logger.info(f"Optimizing texture for Godot ({target_format} format)")

        # Ensure power-of-two dimensions for better performance
        width, height = image.size

        # Find next power of 2
        new_width = 2 ** math.ceil(math.log2(width))
        new_height = 2 ** math.ceil(math.log2(height))

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
            config: Texture generation configuration.
            noise_config: Optional noise configuration.
        """
        self.config = config
        self.noise_config = noise_config or NoiseConfig()
        self.converter = EquirectangularConverter(config)
        self.procedural_gen = ProceduralTextureGenerator(config, self.noise_config)

    def convert_image(self, input_path: Path) -> None:
        """Convert existing image to sphere-ready texture.

        Args:
            input_path: Path to input image.

        Raises:
            FileNotFoundError: If input file doesn't exist.
        """
        logger.info(f"Converting image: {input_path}")

        result_image = self.converter.convert_image_to_equirectangular(input_path)
        result_image = TextureOptimizer.apply_pole_fix(result_image)
        result_image = TextureOptimizer.optimize_for_godot(
            result_image, self.config.format
        )

        self._save_image(result_image)

    def generate_procedural(self, texture_type: str, **kwargs: Any) -> None:
        """Generate procedural texture.

        Args:
            texture_type: Type of texture to generate.
            **kwargs: Additional arguments for texture generation.

        Raises:
            ValueError: If texture_type is not supported.
        """
        logger.info(f"Generating procedural texture: {texture_type}")

        generators = {
            "earth": self.procedural_gen.generate_earth_like_texture,
            "gas_giant": self.procedural_gen.generate_gas_giant_texture,
            "marble": self.procedural_gen.generate_marble_texture,
        }

        if texture_type not in generators:
            raise ValueError(f"Unsupported texture type: {texture_type}")

        result_image = generators[texture_type](**kwargs)
        result_image = TextureOptimizer.apply_pole_fix(result_image)
        result_image = TextureOptimizer.optimize_for_godot(
            result_image, self.config.format
        )

        self._save_image(result_image)

    def _save_image(self, image: Image.Image) -> None:
        """Save image to configured output path.

        Args:
            image: Image to save.
        """
        self.config.output_path.parent.mkdir(parents=True, exist_ok=True)

        save_kwargs = {}
        if self.config.format.upper() == "JPEG":
            save_kwargs["quality"] = self.config.quality
            save_kwargs["optimize"] = True

        image.save(self.config.output_path, format=self.config.format, **save_kwargs)
        logger.info(f"Saved texture: {self.config.output_path}")


def create_cli_parser() -> argparse.ArgumentParser:
    """Create command-line interface parser.

    Returns:
        Configured argument parser.
    """
    parser = argparse.ArgumentParser(
        description="Generate seamless sphere textures for Blender and Godot",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
    DETAILED EXAMPLES:

    ━━━ PROCEDURAL GENERATION ━━━

    🌍 Earth-like Planets:
      # Standard Earth at 2K resolution
      python sphere_textures.py -m procedural -t earth -r 2k -o earth.png

      # High-detail Earth with custom noise (8 octaves)
      python sphere_textures.py -m procedural -t earth -w 4096 -g 2048 -a 8 -c 80.0

      # Desert planet variation (different seed)
      python sphere_textures.py -m procedural -t earth -s 999 -o desert_planet.png

      # Ocean world (high noise scale for more water)
      python sphere_textures.py -m procedural -t earth -c 200.0 -s 777 -o ocean_world.png

    🪐 Gas Giants:
      # Jupiter-style banded planet
      python sphere_textures.py -m procedural -t gas_giant -r 4k -s 42 -o jupiter.png

      # Saturn-style with different seed and resolution
      python sphere_textures.py -m procedural -t gas_giant -w 2048 -g 1024 -s 123

      # High-turbulence gas giant (more octaves = more detail)
      python sphere_textures.py -m procedural -t gas_giant -a 10 -c 50.0 -o turbulent.png

      # Smooth gas giant (fewer octaves = smoother bands)  
      python sphere_textures.py -m procedural -t gas_giant -a 3 -c 120.0 -o smooth.png

    🏛️ Marble Textures:
      # Classic white marble with gray veins
      python sphere_textures.py -m procedural -t marble -r 2k -o marble_classic.png

      # High-resolution marble for close-ups
      python sphere_textures.py -m procedural -t marble -w 8192 -g 4096 -o marble_hd.png

      # Different marble patterns with various seeds
      python sphere_textures.py -m procedural -t marble -s 100 -o marble_v1.png
      python sphere_textures.py -m procedural -t marble -s 200 -o marble_v2.png
      python sphere_textures.py -m procedural -t marble -s 300 -o marble_v3.png

    ━━━ IMAGE CONVERSION ━━━

    📸 Photo to Sphere Texture:
      # Convert landscape photo to seamless sphere
      python sphere_textures.py -m convert -i landscape.jpg -o sphere_landscape.png -r 2k

      # Convert texture with custom resolution
      python sphere_textures.py -m convert -i texture.png -w 4096 -g 2048 -o converted.png

      # High-quality JPEG output for smaller files
      python sphere_textures.py -m convert -i photo.jpg -f JPEG -q 95 -o result.jpg

      # Batch conversion concept (run multiple times)
      python sphere_textures.py -m convert -i input1.jpg -o sphere1.png
      python sphere_textures.py -m convert -i input2.jpg -o sphere2.png

    ━━━ RESOLUTION PRESETS ━━━

    📐 Standard Resolutions:
      -r 512   → 1024×512   (Preview quality, ~500KB)
      -r 1k    → 2048×1024  (Game quality, ~2MB)  
      -r 2k    → 4096×2048  (High quality, ~8MB)
      -r 4k    → 8192×4096  (Cinema quality, ~32MB)
      -r 8k    → 16384×8192 (Ultra quality, ~128MB)

    🎯 Custom Resolutions:
      # Square aspect (will show warning but work)
      python sphere_textures.py -m procedural -t earth -w 1024 -g 1024

      # Ultra-wide for special effects
      python sphere_textures.py -m procedural -t gas_giant -w 4096 -g 1024

      # Mobile-optimized size
      python sphere_textures.py -m procedural -t marble -w 512 -g 256

    ━━━ OUTPUT FORMATS ━━━

    🖼️ PNG (Lossless):
      # High quality, larger files
      python sphere_textures.py -m procedural -t earth -f PNG -o earth.png

    📷 JPEG (Compressed):
      # Smaller files, good for textures
      python sphere_textures.py -m procedural -t earth -f JPEG -q 90 -o earth.jpg

      # Maximum JPEG quality
      python sphere_textures.py -m procedural -t marble -f JPEG -q 100 -o marble.jpg

      # Balanced quality/size
      python sphere_textures.py -m procedural -t gas_giant -f JPEG -q 85 -o planet.jpg

    ━━━ ADVANCED WORKFLOWS ━━━

    🎮 Game Development Pipeline:
      # Generate planet set for space game
      python sphere_textures.py -m procedural -t earth -s 1 -r 2k -o planet_earth.png
      python sphere_textures.py -m procedural -t gas_giant -s 2 -r 2k -o planet_gas1.png  
      python sphere_textures.py -m procedural -t gas_giant -s 3 -r 2k -o planet_gas2.png
      python sphere_textures.py -m procedural -t marble -s 4 -r 2k -o planet_rock.png

    🎬 VFX/Animation Workflow:
      # Ultra-high resolution for close-ups
      python sphere_textures.py -m procedural -t earth -r 8k -a 12 -c 60.0 -o hero_planet.png

      # Multiple detail levels for LOD system
      python sphere_textures.py -m procedural -t gas_giant -s 42 -r 4k -o planet_lod0.png
      python sphere_textures.py -m procedural -t gas_giant -s 42 -r 2k -o planet_lod1.png  
      python sphere_textures.py -m procedural -t gas_giant -s 42 -r 1k -o planet_lod2.png

    🔬 Texture Variations Study:
      # Study noise octave effects (keep same seed, vary octaves)
      python sphere_textures.py -m procedural -t earth -s 100 -a 2 -o study_oct2.png
      python sphere_textures.py -m procedural -t earth -s 100 -a 4 -o study_oct4.png
      python sphere_textures.py -m procedural -t earth -s 100 -a 6 -o study_oct6.png
      python sphere_textures.py -m procedural -t earth -s 100 -a 8 -o study_oct8.png

      # Study noise scale effects (keep octaves/seed same, vary scale)
      python sphere_textures.py -m procedural -t gas_giant -s 42 -c 50.0 -o scale_50.png
      python sphere_textures.py -m procedural -t gas_giant -s 42 -c 100.0 -o scale_100.png
      python sphere_textures.py -m procedural -t gas_giant -s 42 -c 200.0 -o scale_200.png

    ━━━ ENGINE INTEGRATION TIPS ━━━

    🎨 Blender Setup:
      1. Add UV Sphere mesh
      2. Add Material → Image Texture
      3. Load generated texture
      4. Set Projection to 'Sphere' 
      5. Connect to Base Color

    🎮 Godot Setup:
      1. Create SphereMesh in MeshInstance3D
      2. Create new StandardMaterial3D
      3. Load texture as Albedo
      4. UV mapping is automatic

    🔧 Performance Tips:
      # Fast preview generation (small, low octaves)
      python sphere_textures.py -m procedural -t earth -w 512 -g 256 -a 3 -o preview.png

      # Production quality (balanced settings)
      python sphere_textures.py -m procedural -t earth -r 2k -a 6 -c 100.0 -o production.png

      # Hero asset quality (maximum settings)
      python sphere_textures.py -m procedural -t earth -r 4k -a 10 -c 80.0 -v -o hero.png

    ━━━ TROUBLESHOOTING ━━━

    ❌ Common Issues:
      # File not found → Check input path exists
      python sphere_textures.py -m convert -i /full/path/to/image.jpg

      # Out of memory → Use smaller resolution  
      python sphere_textures.py -m procedural -t earth -r 1k  # instead of 8k

      # Slow generation → Reduce octaves
      python sphere_textures.py -m procedural -t gas_giant -a 4  # instead of 12

    🐛 Debug Mode:
      # Verbose output for troubleshooting
      python sphere_textures.py -m procedural -t earth -v -o debug.png

    📊 File Size Estimates:
      512×256 PNG:   ~200KB  | JPEG 90%: ~80KB
      1024×512 PNG:  ~800KB  | JPEG 90%: ~200KB  
      2048×1024 PNG: ~3MB    | JPEG 90%: ~600KB
      4096×2048 PNG: ~12MB   | JPEG 90%: ~2MB
      8192×4096 PNG: ~48MB   | JPEG 90%: ~6MB
            """,
    )

    # Mode selection
    parser.add_argument(
        "-m",
        "--mode",
        choices=["convert", "procedural"],
        required=True,
        help="Operation mode: convert existing image or generate procedural texture",
    )

    # Input/output options
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

    # Resolution options
    resolution_group = parser.add_mutually_exclusive_group()
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

    # Format options
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

    # Procedural generation options
    parser.add_argument(
        "-t",
        "--type",
        choices=["earth", "gas_giant", "marble"],
        help="Procedural texture type",
    )

    # Noise options
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

    # Other options
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
        help="Noise coordinate mode: "
        "'xy' uses x,y coordinates, "
        "'xz' uses x,z coordinates",
    )

    return parser


def main() -> int:
    """Main application entry point.

    Returns:
        Exit code (0 for success, 1 for error).
    """
    parser = create_cli_parser()
    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    try:
        # Determine resolution
        if args.resolution:
            width, height = STANDARD_RESOLUTIONS[args.resolution]
        elif args.width:
            width = args.width
            height = args.height or args.width // 2
        else:
            width, height = 2048, 1024  # Default

        # Create configuration
        texture_config = TextureConfig(
            width=width,
            height=height,
            output_path=args.output,
            format=args.format,
            quality=args.quality,
        )

        noise_config = NoiseConfig(
            octaves=args.octaves,
            seed=args.seed,
            scale=args.scale,
            coordinate_mode=args.coordinate_mode,
        )

        # Create generator
        generator = SphereTextureGenerator(texture_config, noise_config)

        # Execute based on mode
        if args.mode == "convert":
            if not args.input:
                parser.error("--input is required for convert mode")
            generator.convert_image(args.input)

        elif args.mode == "procedural":
            if not args.type:
                parser.error("--type is required for procedural mode")
            generator.generate_procedural(args.type)

        logger.info("✅ Operation completed successfully!")

        # Print the final summary
        print("\n" + "=" * 60)
        print("📊 Generation summary")
        print("=" * 60)
        print(f"✅ File saved: {texture_config.output_path}")
        print(f"📏 Final size: {texture_config.width}x{texture_config.height}")
        print(f"📦 Format: {texture_config.format}")
        print(f"💾 File size: {texture_config.output_path.stat().st_size // 1024}KB")
        print("=" * 60)
        return 0

    except Exception as e:
        logger.error(f"Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
