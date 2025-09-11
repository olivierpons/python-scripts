# svg_to_bitmap_converter.py

## English

### SVG to Bitmap Converter

This script converts simple SVG files containing only rectangles to bitmap image formats (PNG, BMP, JPEG, TIFF, etc.). It features integrated output handling with colored progress messages and comprehensive error handling.

**Features:**

- Converts rectangle-based SVG files to various bitmap formats
- Supports PNG, BMP, JPEG, TIFF, and other image formats
- Comprehensive SVG parsing with validation
- Integrated output handler with colored terminal messages
- Three verbosity levels (quiet, normal, verbose)
- Thread-safe output handling
- Detailed error reporting and logging
- Transparent background support for compatible formats
- Automatic format conversion (RGBA to RGB for BMP)

**Requirements:**
- Python 3.13+
- Pillow (PIL)

**Usage:**

```bash
# Basic conversion
python svg_to_bitmap_converter.py input.svg output.png

# Verbose mode
python svg_to_bitmap_converter.py input.svg output.bmp --verbose

# Quiet mode
python svg_to_bitmap_converter.py input.svg output.jpg --quiet

# No colored output
python svg_to_bitmap_converter.py input.svg output.png --no-color
```

**Arguments:**

- `source`: Path to the source SVG file
- `destination`: Path to the destination bitmap file
- `--verbose, -v`: Enable verbose output with detailed information
- `--quiet, -q`: Quiet mode - only show errors
- `--no-color`: Disable colored output

## Français

### Convertisseur SVG vers Bitmap

Ce script convertit des fichiers SVG simples contenant uniquement des rectangles vers des formats d'image bitmap (PNG, BMP, JPEG, TIFF, etc.). Il dispose d'une gestion de sortie intégrée avec des messages de progression colorés et une gestion d'erreurs complète.

**Fonctionnalités :**

- Convertit les fichiers SVG basés sur des rectangles vers divers formats bitmap
- Supporte PNG, BMP, JPEG, TIFF et autres formats d'image
- Analyse SVG complète avec validation
- Gestionnaire de sortie intégré avec messages colorés du terminal
- Trois niveaux de verbosité (silencieux, normal, verbeux)
- Gestion de sortie thread-safe
- Rapports d'erreurs détaillés et journalisation
- Support d'arrière-plan transparent pour les formats compatibles
- Conversion automatique de format (RGBA vers RGB pour BMP)

**Prérequis :**
- Python 3.13+
- Pillow (PIL)

**Utilisation :**

```bash
# Conversion basique
python svg_to_bitmap_converter.py entree.svg sortie.png

# Mode verbeux
python svg_to_bitmap_converter.py entree.svg sortie.bmp --verbose

# Mode silencieux
python svg_to_bitmap_converter.py entree.svg sortie.jpg --quiet

# Pas de sortie colorée
python svg_to_bitmap_converter.py entree.svg sortie.png --no-color
```

**Arguments :**

- `source` : Chemin vers le fichier SVG source
- `destination` : Chemin vers le fichier bitmap de destination
- `--verbose, -v` : Activer la sortie verbeuse avec des informations détaillées
- `--quiet, -q` : Mode silencieux - afficher seulement les erreurs
- `--no-color` : Désactiver la sortie colorée

## 日本語

### SVGからビットマップコンバーター

このスクリプトは、長方形のみを含むシンプルなSVGファイルをビットマップ画像形式（PNG、BMP、JPEG、TIFFなど）に変換します。カラー進行メッセージと包括的なエラー処理を備えた統合出力処理機能を持ちます。

**機能：**

- 長方形ベースのSVGファイルを様々なビットマップ形式に変換
- PNG、BMP、JPEG、TIFFおよび他の画像形式をサポート
- 検証機能付きの包括的なSVG解析
- カラーターミナルメッセージ付きの統合出力ハンドラー
- 3つの詳細レベル（静か、通常、詳細）
- スレッドセーフな出力処理
- 詳細なエラー報告とログ記録
- 互換形式での透明背景サポート
- 自動形式変換（BMPのためのRGBAからRGBへ）

**必要条件：**
- Python 3.13+
- Pillow (PIL)

**使用法：**

```bash
# 基本的な変換
python svg_to_bitmap_converter.py 入力.svg 出力.png

# 詳細モード
python svg_to_bitmap_converter.py 入力.svg 出力.bmp --verbose

# 静かモード
python svg_to_bitmap_converter.py 入力.svg 出力.jpg --quiet

# カラー出力なし
python svg_to_bitmap_converter.py 入力.svg 出力.png --no-color
```

**引数：**

- `source`：ソースSVGファイルへのパス
- `destination`：宛先ビットマップファイルへのパス
- `--verbose, -v`：詳細情報付きの詳細出力を有効にする
- `--quiet, -q`：静かモード - エラーのみを表示
- `--no-color`：カラー出力を無効にする

## 简体中文

### SVG转位图转换器

此脚本将仅包含矩形的简单SVG文件转换为位图图像格式（PNG、BMP、JPEG、TIFF等）。它具有集成的输出处理功能，包含彩色进度消息和全面的错误处理。

**功能：**

- 将基于矩形的SVG文件转换为各种位图格式
- 支持PNG、BMP、JPEG、TIFF和其他图像格式
- 具有验证功能的全面SVG解析
- 带有彩色终端消息的集成输出处理器
- 三个详细级别（安静、正常、详细）
- 线程安全的输出处理
- 详细的错误报告和日志记录
- 兼容格式的透明背景支持
- 