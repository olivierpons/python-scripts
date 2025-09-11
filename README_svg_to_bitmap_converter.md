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
- 自动格式转换（BMP的RGBA到RGB）

**要求：**
- Python 3.13+
- Pillow (PIL)

**使用方法：**

```bash
# 基本转换
python svg_to_bitmap_converter.py 输入.svg 输出.png

# 详细模式
python svg_to_bitmap_converter.py 输入.svg 输出.bmp --verbose

# 安静模式
python svg_to_bitmap_converter.py 输入.svg 输出.jpg --quiet

# 无彩色输出
python svg_to_bitmap_converter.py 输入.svg 输出.png --no-color
```

**参数：**

- `source`：源SVG文件的路径
- `destination`：目标位图文件的路径
- `--verbose, -v`：启用详细输出与详细信息
- `--quiet, -q`：安静模式 - 只显示错误
- `--no-color`：禁用彩色输出

## 繁體中文

### SVG轉點陣圖轉換器

此腳本將僅包含矩形的簡單SVG檔案轉換為點陣圖影像格式（PNG、BMP、JPEG、TIFF等）。它具有集成的輸出處理功能，包含彩色進度訊息和全面的錯誤處理。

**功能：**

- 將基於矩形的SVG檔案轉換為各種點陣圖格式
- 支援PNG、BMP、JPEG、TIFF和其他影像格式
- 具有驗證功能的全面SVG解析
- 帶有彩色終端訊息的集成輸出處理器
- 三個詳細級別（安靜、正常、詳細）
- 執行緒安全的輸出處理
- 詳細的錯誤報告和日誌記錄
- 相容格式的透明背景支援
- 自動格式轉換（BMP的RGBA到RGB）

**要求：**
- Python 3.13+
- Pillow (PIL)

**使用方法：**

```bash
# 基本轉換
python svg_to_bitmap_converter.py 輸入.svg 輸出.png

# 詳細模式
python svg_to_bitmap_converter.py 輸入.svg 輸出.bmp --verbose

# 安靜模式
python svg_to_bitmap_converter.py 輸入.svg 輸出.jpg --quiet

# 無彩色輸出
python svg_to_bitmap_converter.py 輸入.svg 輸出.png --no-color
```

**參數：**

- `source`：源SVG檔案的路徑
- `destination`：目標點陣圖檔案的路徑
- `--verbose, -v`：啟用詳細輸出與詳細資訊
- `--quiet, -q`：安靜模式 - 只顯示錯誤
- `--no-color`：禁用彩色輸出

## Español

### Convertidor SVG a Bitmap

Este script convierte archivos SVG simples que contienen solo rectángulos a formatos de imagen bitmap (PNG, BMP, JPEG, TIFF, etc.). Incluye manejo de salida integrado con mensajes de progreso coloreados y manejo completo de errores.

**Características:**

- Convierte archivos SVG basados en rectángulos a varios formatos bitmap
- Soporta PNG, BMP, JPEG, TIFF y otros formatos de imagen
- Análisis SVG completo con validación
- Manejador de salida integrado con mensajes coloridos del terminal
- Tres niveles de verbosidad (silencioso, normal, detallado)
- Manejo de salida thread-safe
- Informes de errores detallados y registro
- Soporte de fondo transparente para formatos compatibles
- Conversión automática de formato (RGBA a RGB para BMP)

**Requisitos:**
- Python 3.13+
- Pillow (PIL)

**Uso:**

```bash
# Conversión básica
python svg_to_bitmap_converter.py entrada.svg salida.png

# Modo detallado
python svg_to_bitmap_converter.py entrada.svg salida.bmp --verbose

# Modo silencioso
python svg_to_bitmap_converter.py entrada.svg salida.jpg --quiet

# Sin salida coloreada
python svg_to_bitmap_converter.py entrada.svg salida.png --no-color
```

**Argumentos:**

- `source`: Ruta al archivo SVG fuente
- `destination`: Ruta al archivo bitmap de destino
- `--verbose, -v`: Habilitar salida detallada con información detallada
- `--quiet, -q`: Modo silencioso - solo mostrar errores
- `--no-color`: Deshabilitar salida coloreada

## Italiano

### Convertitore SVG a Bitmap

Questo script converte file SVG semplici contenenti solo rettangoli in formati di immagine bitmap (PNG, BMP, JPEG, TIFF, ecc.). Include gestione dell'output integrata con messaggi di progresso colorati e gestione completa degli errori.

**Funzionalità:**

- Converte file SVG basati su rettangoli in vari formati bitmap
- Supporta PNG, BMP, JPEG, TIFF e altri formati di immagine
- Analisi SVG completa con validazione
- Gestore di output integrato con messaggi colorati del terminale
- Tre livelli di verbosità (silenzioso, normale, dettagliato)
- Gestione dell'output thread-safe
- Report di errori dettagliati e registrazione
- Supporto dello sfondo trasparente per formati compatibili
- Conversione automatica del formato (RGBA a RGB per BMP)

**Requisiti:**
- Python 3.13+
- Pillow (PIL)

**Utilizzo:**

```bash
# Conversione di base
python svg_to_bitmap_converter.py input.svg output.png

# Modalità dettagliata
python svg_to_bitmap_converter.py input.svg output.bmp --verbose

# Modalità silenziosa
python svg_to_bitmap_converter.py input.svg output.jpg --quiet

# Nessun output colorato
python svg_to_bitmap_converter.py input.svg output.png --no-color
```

**Argomenti:**

- `source`: Percorso al file SVG sorgente
- `destination`: Percorso al file bitmap di destinazione
- `--verbose, -v`: Abilitare output dettagliato con informazioni dettagliate
- `--quiet, -q`: Modalità silenziosa - mostrare solo errori
- `--no-color`: Disabilitare output colorato

## Deutsch

### SVG zu Bitmap Konverter

Dieses Skript konvertiert einfache SVG-Dateien, die nur Rechtecke enthalten, zu Bitmap-Bildformaten (PNG, BMP, JPEG, TIFF, etc.). Es verfügt über integrierte Ausgabeverarbeitung mit farbigen Fortschrittsmeldungen und umfassende Fehlerbehandlung.

**Funktionen:**

- Konvertiert rechteckbasierte SVG-Dateien in verschiedene Bitmap-Formate
- Unterstützt PNG, BMP, JPEG, TIFF und andere Bildformate
- Umfassende SVG-Analyse mit Validierung
- Integrierter Ausgabe-Handler mit farbigen Terminal-Nachrichten
- Drei Verbosity-Level (still, normal, ausführlich)
- Thread-sichere Ausgabeverarbeitung
- Detaillierte Fehlerberichte und Protokollierung
- Unterstützung für transparenten Hintergrund für kompatible Formate
- Automatische Formatkonvertierung (RGBA zu RGB für BMP)

**Anforderungen:**
- Python 3.13+
- Pillow (PIL)

**Verwendung:**

```bash
# Grundlegende Konvertierung
python svg_to_bitmap_converter.py eingabe.svg ausgabe.png

# Ausführlicher Modus
python svg_to_bitmap_converter.py eingabe.svg ausgabe.bmp --verbose

# Stiller Modus
python svg_to_bitmap_converter.py eingabe.svg ausgabe.jpg --quiet

# Keine farbige Ausgabe
python svg_to_bitmap_converter.py eingabe.svg ausgabe.png --no-color
```

**Argumente:**

- `source`: Pfad zur Quell-SVG-Datei
- `destination`: Pfad zur Ziel-Bitmap-Datei
- `--verbose, -v`: Ausführliche Ausgabe mit detaillierten Informationen aktivieren
- `--quiet, -q`: Stiller Modus - nur Fehler anzeigen
- `--no-color`: Farbige Ausgabe deaktivieren