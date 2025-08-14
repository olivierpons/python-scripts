# pie_chart_generator.py

## English

### Pie Chart Series Generator

This script generates a series of pie charts showing the progression of two colors from 0% to 100% in customizable increments. Built with Python 3.13+ features, it offers extensive customization options and robust error handling.

**Features:**

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

**Basic Usage:**

```bash
# Simple generation with default settings
python pie_chart_generator.py

# Custom colors and output directory
python pie_chart_generator.py -o charts -c "#FF0000,#00FF00" -s 0 -e 50 --step 1
```

**Color Combinations and Edge Styles:**

```bash
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
```

**Advanced Options:**

```bash
# High quality transparent PNG with text
python pie_chart_generator.py -c "#FF4444,#44FF44" --edge-width 0 --transparent --format png --dpi 300 --show-percentage

# Generate animated GIF
python pie_chart_generator.py -c "#FF6B35,#004E89" --gif --gif-duration 100 --edge-width 0

# Custom range with step
python pie_chart_generator.py -c "#1E3A8A,#10B981" -s 25 -e 75 --step 5 --edge-width 0
```

**Edge Width Options:**
- `--edge-width 0`: No border
- `--edge-width 0.5`: Very thin border
- `--edge-width 1`: Thin border
- `--edge-width 2`: Medium border (default)
- `--edge-width 3`: Thick border
- `--edge-width 5`: Very thick border

**Edge Color Options:**
- `--edge-color "#FFFFFF"`: White (default)
- `--edge-color "#000000"`: Black
- `--edge-color "#808080"`: Gray
- `--edge-color "#FFD700"`: Gold
- `--edge-color "none"`: No border (equivalent to --edge-width 0)

**Arguments:**

**Output Options:**
- `-o, --output-dir`: Output directory for generated images
- `-f, --format`: Output image format (png, jpg, jpeg, pdf, svg, webp, tiff)
- `--dpi`: Image resolution in DPI (50-1000)
- `--atomic-writes`: Use atomic file writes to prevent corruption
- `--backup`: Create backups of existing files

**Visual Options:**
- `-c, --colors`: Two hex colors separated by comma
- `-w, --width`: Figure width in inches
- `--height`: Figure height in inches
- `--transparent`: Use transparent background (default: enabled)
- `--no-transparent`: Use white background instead of transparent

**Range Options:**
- `-s, --start`: Starting percentage (0-100)
- `-e, --end`: Ending percentage (0-100)
- `--step`: Step increment

**Chart Appearance:**
- `--start-angle`: Starting angle in degrees (0-360)
- `--clockwise`: Draw pie chart clockwise
- `--edge-color`: Edge color for pie segments
- `--edge-width`: Edge line width

**Text Options:**
- `--font-size`: Font size for percentage text
- `--font-color`: Font color for percentage text
- `--font-weight`: Font weight (normal, bold, light, ultralight, heavy)
- `--title-font-size`: Title font size
- `--show-percentage`: Show percentage text in center (default: disabled)
- `--show-title`: Show chart title (default: disabled)

**GIF Options:**
- `--gif`: Generate animated GIF
- `--gif-duration`: GIF frame duration in milliseconds
- `--gif-loop`: GIF loop count (0=infinite)

**Progress Options:**
- `--quiet, -q`: Suppress progress output
- `--verbose, -v`: Enable verbose output

**Configuration:**
- `--config`: Load configuration from JSON file
- `--save-config`: Save current configuration to JSON file

## Français

### Générateur de Séries de Camemberts

Ce script génère une série de camemberts montrant la progression de deux couleurs de 0% à 100% par incréments personnalisables. Construit avec les fonctionnalités de Python 3.13+, il offre de nombreuses options de personnalisation et une gestion d'erreurs robuste.

**Fonctionnalités :**

- Génère des séries de camemberts avec des plages de pourcentages et des pas personnalisables
- Supporte plusieurs formats de sortie (PNG, JPG, JPEG, PDF, SVG, WEBP, TIFF)
- Interface en ligne de commande avancée avec formats d'arguments courts et longs
- Validation complète utilisant PurePath pour la compatibilité multiplateforme
- Écritures atomiques de fichiers avec support de sauvegarde pour éviter la corruption
- Barres de progression et messages d'état colorés dans le terminal
- Création optionnelle de GIF animés à partir des images générées
- Support de fichiers de configuration (JSON) pour sauvegarder et charger les paramètres
- Gestion d'erreurs extensive avec hiérarchie d'exceptions personnalisée
- Fonctionnalités modernes Python 3.13+ : dataclasses, enums, pattern matching, types union
- Support d'arrière-plan transparent pour PNG et autres formats compatibles
- Contrôles optionnels d'affichage du texte (pourcentage et titre)

**Utilisation Basique :**

```bash
# Génération simple avec paramètres par défaut
python pie_chart_generator.py

# Couleurs personnalisées et répertoire de sortie
python pie_chart_generator.py -o graphiques -c "#FF0000,#00FF00" -s 0 -e 50 --step 1
```

**Combinaisons de Couleurs et Styles de Bordure :**

```bash
# Couleurs vibrantes sans bordure
python pie_chart_generator.py -o graphiques -c "#FF6B35,#004E89" --edge-width 0

# Couleurs pastel avec bordure blanche fine
python pie_chart_generator.py -o graphiques -c "#FFB3BA,#BAE1FF" --edge-width 1 --edge-color "#FFFFFF"

# Couleurs sombres avec bordure noire épaisse
python pie_chart_generator.py -o graphiques -c "#2E2E2E,#D32F2F" --edge-width 3 --edge-color "#000000"

# Dégradé bleu-vert sans bordure
python pie_chart_generator.py -o graphiques -c "#1E3A8A,#10B981" --edge-width 0

# Couleurs coucher de soleil avec bordure dorée
python pie_chart_generator.py -o graphiques -c "#FF6B6B,#FFE66D" --edge-width 2 --edge-color "#FFD700"

# Monochrome avec bordure grise
python pie_chart_generator.py -o graphiques -c "#000000,#FFFFFF" --edge-width 4 --edge-color "#808080"

# Couleurs néon
python pie_chart_generator.py -o graphiques -c "#00FFFF,#FF00FF" --edge-width 0

# Couleurs naturelles
python pie_chart_generator.py -o graphiques -c "#8B4513,#228B22" --edge-width 1.5 --edge-color "#FFFFFF"
```

**Options Avancées :**

```bash
# PNG transparent haute qualité avec texte
python pie_chart_generator.py -c "#FF4444,#44FF44" --edge-width 0 --transparent --format png --dpi 300 --show-percentage

# Générer un GIF animé
python pie_chart_generator.py -c "#FF6B35,#004E89" --gif --gif-duration 100 --edge-width 0

# Plage personnalisée avec pas
python pie_chart_generator.py -c "#1E3A8A,#10B981" -s 25 -e 75 --step 5 --edge-width 0
```

**Options de Largeur de Bordure :**
- `--edge-width 0` : Pas de bordure
- `--edge-width 0.5` : Bordure très fine
- `--edge-width 1` : Bordure fine
- `--edge-width 2` : Bordure moyenne (par défaut)
- `--edge-width 3` : Bordure épaisse
- `--edge-width 5` : Bordure très épaisse

**Options de Couleur de Bordure :**
- `--edge-color "#FFFFFF"` : Blanc (par défaut)
- `--edge-color "#000000"` : Noir
- `--edge-color "#808080"` : Gris
- `--edge-color "#FFD700"` : Or
- `--edge-color "none"` : Pas de bordure (équivalent à --edge-width 0)

**Arguments :**

**Options de Sortie :**
- `-o, --output-dir` : Répertoire de sortie pour les images générées
- `-f, --format` : Format d'image de sortie (png, jpg, jpeg, pdf, svg, webp, tiff)
- `--dpi` : Résolution d'image en DPI (50-1000)
- `--atomic-writes` : Utiliser des écritures atomiques pour éviter la corruption
- `--backup` : Créer des sauvegardes des fichiers existants

**Options Visuelles :**
- `-c, --colors` : Deux couleurs hex séparées par une virgule
- `-w, --width` : Largeur de la figure en pouces
- `--height` : Hauteur de la figure en pouces
- `--transparent` : Utiliser un arrière-plan transparent (par défaut : activé)
- `--no-transparent` : Utiliser un arrière-plan blanc au lieu de transparent

**Options de Plage :**
- `-s, --start` : Pourcentage de départ (0-100)
- `-e, --end` : Pourcentage de fin (0-100)
- `--step` : Incrément de pas

**Apparence du Graphique :**
- `--start-angle` : Angle de départ en degrés (0-360)
- `--clockwise` : Dessiner le camembert dans le sens horaire
- `--edge-color` : Couleur de bordure pour les segments
- `--edge-width` : Largeur des lignes de bordure

**Options de Texte :**
- `--font-size` : Taille de police pour le texte de pourcentage
- `--font-color` : Couleur de police pour le texte de pourcentage
- `--font-weight` : Poids de police (normal, bold, light, ultralight, heavy)
- `--title-font-size` : Taille de police du titre
- `--show-percentage` : Afficher le texte de pourcentage au centre (par défaut : désactivé)
- `--show-title` : Afficher le titre du graphique (par défaut : désactivé)

**Options GIF :**
- `--gif` : Générer un GIF animé
- `--gif-duration` : Durée de frame GIF en millisecondes
- `--gif-loop` : Nombre de boucles GIF (0=infini)

**Options de Progression :**
- `--quiet, -q` : Supprimer la sortie de progression
- `--verbose, -v` : Activer la sortie détaillée

**Configuration :**
- `--config` : Charger la configuration depuis un fichier JSON
- `--save-config` : Sauvegarder la configuration actuelle dans un fichier JSON

## 日本語

### 円グラフシリーズジェネレーター

このスクリプトは、2つの色の0%から100%への進行を示す円グラフシリーズを、カスタマイズ可能な増分で生成します。Python 3.13+の機能で構築され、豊富なカスタマイズオプションと堅牢なエラー処理を提供します。

**機能：**

- カスタマイズ可能なパーセンテージ範囲とステップで円グラフシリーズを生成
- 複数の出力形式をサポート（PNG、JPG、JPEG、PDF、SVG、WEBP、TIFF）
- 短縮形と長形式の引数形式を持つ高度なコマンドライン インターフェース
- クロスプラットフォーム互換性のためのPurePathを使用した包括的検証
- 破損を防ぐバックアップサポート付きアトミックファイル書き込み
- カラフルなターミナル進行状況バーとステータスメッセージ
- 生成された画像からのオプションのアニメーションGIF作成
- 設定の保存と読み込みのための設定ファイルサポート（JSON）
- カスタム例外階層による広範なエラー処理
- 最新のPython 3.13+機能：データクラス、列挙型、パターンマッチング、ユニオン型
- PNGおよび他の互換形式用の透明背景サポート
- オプションのテキスト表示制御（パーセンテージとタイトル）

**基本的な使用法：**

```bash
# デフォルト設定での簡単な生成
python pie_chart_generator.py

# カスタム色と出力ディレクトリ
python pie_chart_generator.py -o charts -c "#FF0000,#00FF00" -s 0 -e 50 --step 1
```

**色の組み合わせとエッジスタイル：**

```bash
# 境界線なしの鮮やかな色
python pie_chart_generator.py -o charts -c "#FF6B35,#004E89" --edge-width 0

# 細い白い境界線付きのパステルカラー
python pie_chart_generator.py -o charts -c "#FFB3BA,#BAE1FF" --edge-width 1 --edge-color "#FFFFFF"

# 太い黒い境界線付きのダークカラー
python pie_chart_generator.py -o charts -c "#2E2E2E,#D32F2F" --edge-width 3 --edge-color "#000000"

# 境界線なしの青緑グラデーション
python pie_chart_generator.py -o charts -c "#1E3A8A,#10B981" --edge-width 0

# 金色の境界線付きサンセットカラー
python pie_chart_generator.py -o charts -c "#FF6B6B,#FFE66D" --edge-width 2 --edge-color "#FFD700"

# グレーの境界線付きモノクローム
python pie_chart_generator.py -o charts -c "#000000,#FFFFFF" --edge-width 4 --edge-color "#808080"

# ネオンカラー
python pie_chart_generator.py -o charts -c "#00FFFF,#FF00FF" --edge-width 0

# ナチュラルカラー
python pie_chart_generator.py -o charts -c "#8B4513,#228B22" --edge-width 1.5 --edge-color "#FFFFFF"
```

**高度なオプション：**

```bash
# テキスト付き高品質透明PNG
python pie_chart_generator.py -c "#FF4444,#44FF44" --edge-width 0 --transparent --format png --dpi 300 --show-percentage

# アニメーションGIF生成
python pie_chart_generator.py -c "#FF6B35,#004E89" --gif --gif-duration 100 --edge-width 0

# ステップ付きカスタム範囲
python pie_chart_generator.py -c "#1E3A8A,#10B981" -s 25 -e 75 --step 5 --edge-width 0
```

**エッジ幅オプション：**
- `--edge-width 0`：境界線なし
- `--edge-width 0.5`：非常に細い境界線
- `--edge-width 1`：細い境界線
- `--edge-width 2`：中程度の境界線（デフォルト）
- `--edge-width 3`：太い境界線
- `--edge-width 5`：非常に太い境界線

**エッジ色オプション：**
- `--edge-color "#FFFFFF"`：白（デフォルト）
- `--edge-color "#000000"`：黒
- `--edge-color "#808080"`：グレー
- `--edge-color "#FFD700"`：金
- `--edge-color "none"`：境界線なし（--edge-width 0と同等）

**引数：**

**出力オプション：**
- `-o, --output-dir`：生成された画像の出力ディレクトリ
- `-f, --format`：出力画像形式（png、jpg、jpeg、pdf、svg、webp、tiff）
- `--dpi`：DPIでの画像解像度（50-1000）
- `--atomic-writes`：破損を防ぐためのアトミックファイル書き込みを使用
- `--backup`：既存ファイルのバックアップを作成

**視覚オプション：**
- `-c, --colors`：コンマで区切られた2つのヘックス色
- `-w, --width`：インチ単位の図の幅
- `--height`：インチ単位の図の高さ
- `--transparent`：透明背景を使用（デフォルト：有効）
- `--no-transparent`：透明の代わりに白い背景を使用

**範囲オプション：**
- `-s, --start`：開始パーセンテージ（0-100）
- `-e, --end`：終了パーセンテージ（0-100）
- `--step`：ステップ増分

**グラフの外観：**
- `--start-angle`：度単位での開始角度（0-360）
- `--clockwise`：円グラフを時計回りに描画
- `--edge-color`：円セグメントのエッジ色
- `--edge-width`：エッジライン幅

**テキストオプション：**
- `--font-size`：パーセンテージテキストのフォントサイズ
- `--font-color`：パーセンテージテキストのフォント色
- `--font-weight`：フォントウェイト（normal、bold、light、ultralight、heavy）
- `--title-font-size`：タイトルフォントサイズ
- `--show-percentage`：中央にパーセンテージテキストを表示（デフォルト：無効）
- `--show-title`：グラフタイトルを表示（デフォルト：無効）

**GIFオプション：**
- `--gif`：アニメーションGIFを生成
- `--gif-duration`：ミリ秒単位のGIFフレーム時間
- `--gif-loop`：GIFループ回数（0=無限）

**進行状況オプション：**
- `--quiet, -q`：進行状況出力を抑制
- `--verbose, -v`：詳細出力を有効化

**設定：**
- `--config`：JSONファイルから設定を読み込み
- `--save-config`：現在の設定をJSONファイルに保存

## 简体中文

### 饼图系列生成器

此脚本生成饼图系列，显示两种颜色从0%到100%的进展，具有可自定义的增量。使用Python 3.13+功能构建，提供广泛的自定义选项和强大的错误处理。

**功能：**

- 生成具有可自定义百分比范围和步长的饼图系列
- 支持多种输出格式（PNG、JPG、JPEG、PDF、SVG、WEBP、TIFF）
- 具有短格式和长格式参数的高级命令行界面
- 使用PurePath进行跨平台兼容性的全面验证
- 具有备份支持的原子文件写入以防止损坏
- 彩色终端进度条和状态消息
- 从生成的图像可选创建动画GIF
- 配置文件支持（JSON）用于保存和加载设置
- 具有自定义异常层次结构的广泛错误处理
- 现代Python 3.13+功能：数据类、枚举、模式匹配、联合类型
- PNG和其他兼容格式的透明背景支持
- 可选文本显示控制（百分比和标题）

**基本用法：**

```bash
# 使用默认设置的简单生成
python pie_chart_generator.py

# 自定义颜色和输出目录
python pie_chart_generator.py -o charts -c "#FF0000,#00FF00" -s 0 -e 50 --step 1
```

**颜色组合和边缘样式：**

```bash
# 无边框的鲜艳颜色
python pie_chart_generator.py -o charts -c "#FF6B35,#004E89" --edge-width 0

# 带细白边框的柔和颜色
python pie_chart_generator.py -o charts -c "#FFB3BA,#BAE1FF" --edge-width 1 --edge-color "#FFFFFF"

# 带粗黑边框的深色
python pie_chart_generator.py -o charts -c "#2E2E2E,#D32F2F" --edge-width 3 --edge-color "#000000"

# 无边框的蓝绿渐变
python pie_chart_generator.py -o charts -c "#1E3A8A,#10B981" --edge-width 0

# 带金色边框的日落色
python pie_chart_generator.py -o charts -c "#FF6B6B,#FFE66D" --edge-width 2 --edge-color "#FFD700"

# 带灰色边框的单色
python pie_chart_generator.py -o charts -c "#000000,#FFFFFF" --edge-width 4 --edge-color "#808080"

# 霓虹色
python pie_chart_generator.py -o charts -c "#00FFFF,#FF00FF" --edge-width 0

# 自然色
python pie_chart_generator.py -o charts -c "#8B4513,#228B22" --edge-width 1.5 --edge-color "#FFFFFF"
```

**高级选项：**

```bash
# 带文本的高质量透明PNG
python pie_chart_generator.py -c "#FF4444,#44FF44" --edge-width 0 --transparent --format png --dpi 300 --show-percentage

# 生成动画GIF
python pie_chart_generator.py -c "#FF6B35,#004E89" --gif --gif-duration 100 --edge-width 0

# 带步长的自定义范围
python pie_chart_generator.py -c "#1E3A8A,#10B981" -s 25 -e 75 --step 5 --edge-width 0
```

**边缘宽度选项：**
- `--edge-width 0`：无边框
- `--edge-width 0.5`：极细边框
- `--edge-width 1`：细边框
- `--edge-width 2`：中等边框（默认）
- `--edge-width 3`：粗边框
- `--edge-width 5`：极粗边框

**边缘颜色选项：**
- `--edge-color "#FFFFFF"`：白色（默认）
- `--edge-color "#000000"`：黑色
- `--edge-color "#808080"`：灰色
- `--edge-color "#FFD700"`：金色
- `--edge-color "none"`：无边框（等同于--edge-width 0）

**参数：**

**输出选项：**
- `-o, --output-dir`：生成图像的输出目录
- `-f, --format`：输出图像格式（png、jpg、jpeg、pdf、svg、webp、tiff）
- `--dpi`：DPI图像分辨率（50-1000）
- `--atomic-writes`：使用原子文件写入防止损坏
- `--backup`：创建现有文件的备份

**视觉选项：**
- `-c, --colors`：用逗号分隔的两种十六进制颜色
- `-w, --width`：英寸为单位的图形宽度
- `--height`：英寸为单位的图形高度
- `--transparent`：使用透明背景（默认：启用）
- `--no-transparent`：使用白色背景而不是透明

**范围选项：**
- `-s, --start`：起始百分比（0-100）
- `-e, --end`：结束百分比（0-100）
- `--step`：步长增量

**图表外观：**
- `--start-angle`：度数为单位的起始角度（0-360）
- `--clockwise`：顺时针绘制饼图
- `--edge-color`：饼图段的边缘颜色
- `--edge-width`：边缘线宽度

**文本选项：**
- `--font-size`：百分比文本的字体大小
- `--font-color`：百分比文本的字体颜色
- `--font-weight`：字体粗细（normal、bold、light、ultralight、heavy）
- `--title-font-size`：标题字体大小
- `--show-percentage`：在中心显示百分比文本（默认：禁用）
- `--show-title`：显示图表标题（默认：禁用）

**GIF选项：**
- `--gif`：生成动画GIF
- `--gif-duration`：毫秒为单位的GIF帧持续时间
- `--gif-loop`：GIF循环次数（0=无限）

**进度选项：**
- `--quiet, -q`：抑制进度输出
- `--verbose, -v`：启用详细输出

**配置：**
- `--config`：从JSON文件加载配置
- `--save-config`：将当前配置保存到JSON文件

## 繁體中文

### 圓餅圖系列產生器

此腳本產生圓餅圖系列，顯示兩種顏色從0%到100%的進展，具有可自訂的增量。使用Python 3.13+功能構建，提供廣泛的自訂選項和強大的錯誤處理。

**功能：**

- 產生具有可自訂百分比範圍和步長的圓餅圖系列
- 支援多種輸出格式（PNG、JPG、JPEG、PDF、SVG、WEBP、TIFF）
- 具有短格式和長格式參數的進階命令列介面
- 使用PurePath進行跨平台相容性的全面驗證
- 具有備份支援的原子檔案寫入以防止損壞
- 彩色終端進度條和狀態訊息
- 從產生的圖像可選創建動畫GIF
- 組態檔案支援（JSON）用於保存和載入設定
- 具有自訂例外階層的廣泛錯誤處理
- 現代Python 3.13+功能：資料類、列舉、模式匹配、聯合類型
- PNG和其他相容格式的透明背景支援
- 可選文字顯示控制（百分比和標題）

**基本用法：**

```bash
# 使用預設設定的簡單產生
python pie_chart_generator.py

# 自訂顏色和輸出目錄
python pie_chart_generator.py -o charts -c "#FF0000,#00FF00" -s 0 -e 50 --step 1
```

**顏色組合和邊緣樣式：**

```bash
# 無邊框的鮮豔顏色
python pie_chart_generator.py -o charts -c "#FF6B35,#004E89" --edge-width 0

# 帶細白邊框的柔和顏色
python pie_chart_generator.py -o charts -c "#FFB3BA,#BAE1FF" --edge-width 1 --edge-color "#FFFFFF"

# 帶粗黑邊框的深色
python pie_chart_generator.py -o charts -c "#2E2E2E,#D32F2F" --edge-width 3 --edge-color "#000000"

# 無邊框的藍綠漸變
python pie_chart_generator.py -o charts -c "#1E3A8A,#10B981" --edge-width 0

# 帶金色邊框的日落色
python pie_chart_generator.py -o charts -c "#FF6B6B,#FFE66D" --edge-width 2 --edge-color "#FFD700"

# 帶灰色邊框的單色
python pie_chart_generator.py -o charts -c "#000000,#FFFFFF" --edge-width 4 --edge-color "#808080"

# 霓虹色
python pie_chart_generator.py -o charts -c "#00FFFF,#FF00FF" --edge-width 0

# 自然色
python pie_chart_generator.py -o charts -c "#8B4513,#228B22" --edge-width 1.5 --edge-color "#FFFFFF"
```

**進階選項：**

```bash
# 帶文字的高品質透明PNG
python pie_chart_generator.py -c "#FF4444,#44FF44" --edge-width 0 --transparent --format png --dpi 300 --show-percentage

# 產生動畫GIF
python pie_chart_generator.py -c "#FF6B35,#004E89" --gif --gif-duration 100 --edge-width 0

# 帶步長的自訂範圍
python pie_chart_generator.py -c "#1E3A8A,#10B981" -s 25 -e 75 --step 5 --edge-width 0
```

**邊緣寬度選項：**
- `--edge-width 0`：無邊框
- `--edge-width 0.5`：極細邊框
- `--edge-width 1`：細邊框
- `--edge-width 2`：中等邊框（預設）
- `--edge-width 3`：粗邊框
- `--edge-width 5`：極粗邊框

**邊緣顏色選項：**
- `--edge-color "#FFFFFF"`：白色（預設）
- `--edge-color "#000000"`：黑色
- `--edge-color "#808080"`：灰色
- `--edge-color "#FFD700"`：金色
- `--edge-color "none"`：無邊框（等同於--edge-width 0）

**參數：**

**輸出選項：**
- `-o, --output-dir`：產生圖像的輸出目錄
- `-f, --format`：輸出圖像格式（png、jpg、jpeg、pdf、svg、webp、tiff）
- `--dpi`：DPI圖像解析度（50-1000）
- `--atomic-writes`：使用原子檔案寫入防止損壞
- `--backup`：創建現有檔案的備份

**視覺選項：**
- `-c, --colors`：用逗號分隔的兩種十六進制顏色
- `-w, --width`：英寸為單位的圖形寬度
- `--height`：英寸為單位的圖形高度
- `--transparent`：使用透明背景（預設：啟用）
- `--no-transparent`：使用白色背景而不是透明

**範圍選項：**
- `-s, --start`：起始百分比（0-100）
- `-e, --end`：結束百分比（0-100）
- `--step`：步長增量

**圖表外觀：**
- `--start-angle`：度數為單位的起始角度（0-360）
- `--clockwise`：順時針繪製圓餅圖
- `--edge-color`：圓餅圖段的邊緣顏色
- `--edge-width`：邊緣線寬度

**文字選項：**
- `--font-size`：百分比文字的字體大小
- `--font-color`：百分比文字的字體顏色
- `--font-weight`：字體粗細（normal、bold、light、ultralight、heavy）
- `--title-font-size`：標題字體大小
- `--show-percentage`：在中心顯示百分比文字（預設：停用）
- `--show-title`：顯示圖表標題（預設：停用）

**GIF選項：**
- `--gif`：產生動畫GIF
- `--gif-duration`：毫秒為單位的GIF幀持續時間
- `--gif-loop`：GIF循環次數（0=無限）

**進度選項：**
- `--quiet, -q`：抑制進度輸出
- `--verbose, -v`：啟用詳細輸出

**組態：**
- `--config`：從JSON檔案載入組態
- `--save-config`：將目前組態保存到JSON檔案

## Español

### Generador de Series de Gráficos Circulares

Este script genera una serie de gráficos circulares que muestran la progresión de dos colores del 0% al 100% en incrementos personalizables. Construido con características de Python 3.13+, ofrece amplias opciones de personalización y manejo robusto de errores.

**Características:**

- Genera series de gráficos circulares con rangos de porcentaje y pasos personalizables
- Soporta múltiples formatos de salida (PNG, JPG, JPEG, PDF, SVG, WEBP, TIFF)
- Interfaz de línea de comandos avanzada con formatos de argumentos cortos y largos
- Validación exhaustiva usando PurePath para compatibilidad multiplataforma
- Escrituras atómicas de archivos con soporte de respaldo para prevenir corrupción
- Barras de progreso y mensajes de estado coloridos en terminal
- Creación opcional de GIF animado a partir de imágenes generadas
- Soporte de archivos de configuración (JSON) para guardar y cargar ajustes
- Manejo extensivo de errores con jerarquía de excepciones personalizada
- Características modernas de Python 3.13+: dataclasses, enums, pattern matching, union types
- Soporte de fondo transparente para PNG y otros formatos compatibles
- Controles opcionales de visualización de texto (porcentaje y título)

**Uso Básico:**

```bash
# Generación simple con configuración predeterminada
python pie_chart_generator.py

# Colores personalizados y directorio de salida
python pie_chart_generator.py -o graficos -c "#FF0000,#00FF00" -s 0 -e 50 --step 1
```

**Combinaciones de Colores y Estilos de Borde:**

```bash
# Colores vibrantes sin borde
python pie_chart_generator.py -o graficos -c "#FF6B35,#004E89" --edge-width 0

# Colores pastel con borde blanco fino
python pie_chart_generator.py -o graficos -c "#FFB3BA,#BAE1FF" --edge-width 1 --edge-color "#FFFFFF"

# Colores oscuros con borde negro grueso
python pie_chart_generator.py -o graficos -c "#2E2E2E,#D32F2F" --edge-width 3 --edge-color "#000000"

# Gradiente azul-verde sin borde
python pie_chart_generator.py -o graficos -c "#1E3A8A,#10B981" --edge-width 0

# Colores atardecer con borde dorado
python pie_chart_generator.py -o graficos -c "#FF6B6B,#FFE66D" --edge-width 2 --edge-color "#FFD700"

# Monocromo con borde gris
python pie_chart_generator.py -o graficos -c "#000000,#FFFFFF" --edge-width 4 --edge-color "#808080"

# Colores neón
python pie_chart_generator.py -o graficos -c "#00FFFF,#FF00FF" --edge-width 0

# Colores naturales
python pie_chart_generator.py -o graficos -c "#8B4513,#228B22" --edge-width 1.5 --edge-color "#FFFFFF"
```

**Opciones Avanzadas:**

```bash
# PNG transparente de alta calidad con texto
python pie_chart_generator.py -c "#FF4444,#44FF44" --edge-width 0 --transparent --format png --dpi 300 --show-percentage

# Generar GIF animado
python pie_chart_generator.py -c "#FF6B35,#004E89" --gif --gif-duration 100 --edge-width 0

# Rango personalizado con paso
python pie_chart_generator.py -c "#1E3A8A,#10B981" -s 25 -e 75 --step 5 --edge-width 0
```

**Opciones de Ancho de Borde:**
- `--edge-width 0`: Sin borde
- `--edge-width 0.5`: Borde muy fino
- `--edge-width 1`: Borde fino
- `--edge-width 2`: Borde medio (predeterminado)
- `--edge-width 3`: Borde grueso
- `--edge-width 5`: Borde muy grueso

**Opciones de Color de Borde:**
- `--edge-color "#FFFFFF"`: Blanco (predeterminado)
- `--edge-color "#000000"`: Negro
- `--edge-color "#808080"`: Gris
- `--edge-color "#FFD700"`: Oro
- `--edge-color "none"`: Sin borde (equivalente a --edge-width 0)

**Argumentos:**

**Opciones de Salida:**
- `-o, --output-dir`: Directorio de salida para imágenes generadas
- `-f, --format`: Formato de imagen de salida (png, jpg, jpeg, pdf, svg, webp, tiff)
- `--dpi`: Resolución de imagen en DPI (50-1000)
- `--atomic-writes`: Usar escrituras atómicas para prevenir corrupción
- `--backup`: Crear respaldos de archivos existentes

**Opciones Visuales:**
- `-c, --colors`: Dos colores hex separados por coma
- `-w, --width`: Ancho de figura en pulgadas
- `--height`: Alto de figura en pulgadas
- `--transparent`: Usar fondo transparente (por defecto: habilitado)
- `--no-transparent`: Usar fondo blanco en lugar de transparente

**Opciones de Rango:**
- `-s, --start`: Porcentaje inicial (0-100)
- `-e, --end`: Porcentaje final (0-100)
- `--step`: Incremento de paso

**Apariencia del Gráfico:**
- `--start-angle`: Ángulo inicial en grados (0-360)
- `--clockwise`: Dibujar gráfico circular en sentido horario
- `--edge-color`: Color de borde para segmentos del gráfico
- `--edge-width`: Ancho de línea de borde

**Opciones de Texto:**
- `--font-size`: Tamaño de fuente para texto de porcentaje
- `--font-color`: Color de fuente para texto de porcentaje
- `--font-weight`: Peso de fuente (normal, bold, light, ultralight, heavy)
- `--title-font-size`: Tamaño de fuente del título
- `--show-percentage`: Mostrar texto de porcentaje en el centro (por defecto: deshabilitado)
- `--show-title`: Mostrar título del gráfico (por defecto: deshabilitado)

**Opciones GIF:**
- `--gif`: Generar GIF animado
- `--gif-duration`: Duración de frame GIF en milisegundos
- `--gif-loop`: Número de bucles GIF (0=infinito)

**Opciones de Progreso:**
- `--quiet, -q`: Suprimir salida de progreso
- `--verbose, -v`: Habilitar salida detallada

**Configuración:**
- `--config`: Cargar configuración desde archivo JSON
- `--save-config`: Guardar configuración actual en archivo JSON

## Italiano

### Generatore di Serie di Grafici a Torta

Questo script genera una serie di grafici a torta che mostrano la progressione di due colori dallo 0% al 100% in incrementi personalizzabili. Costruito con funzionalità di Python 3.13+, offre ampie opzioni di personalizzazione e gestione robusta degli errori.

**Funzionalità:**

- Genera serie di grafici a torta con intervalli percentuali e passi personalizzabili
- Supporta formati di output multipli (PNG, JPG, JPEG, PDF, SVG, WEBP, TIFF)
- Interfaccia a riga di comando avanzata con formati di argomenti corti e lunghi
- Validazione completa utilizzando PurePath per compatibilità multipiattaforma
- Scritture atomiche di file con supporto backup per prevenire corruzione
- Barre di progresso e messaggi di stato colorati nel terminale
- Creazione opzionale di GIF animata dalle immagini generate
- Supporto file di configurazione (JSON) per salvare e caricare impostazioni
- Gestione estensiva degli errori con gerarchia di eccezioni personalizzata
- Funzionalità moderne Python 3.13+: dataclasses, enums, pattern matching, union types
- Supporto sfondo trasparente per PNG e altri formati compatibili
- Controlli opzionali di visualizzazione del testo (percentuale e titolo)

**Utilizzo Base:**

```bash
# Generazione semplice con impostazioni predefinite
python pie_chart_generator.py

# Colori personalizzati e directory di output
python pie_chart_generator.py -o grafici -c "#FF0000,#00FF00" -s 0 -e 50 --step 1
```

**Combinazioni di Colori e Stili di Bordo:**

```bash
# Colori vibranti senza bordo
python pie_chart_generator.py -o grafici -c "#FF6B35,#004E89" --edge-width 0

# Colori pastello con bordo bianco sottile
python pie_chart_generator.py -o grafici -c "#FFB3BA,#BAE1FF" --edge-width 1 --edge-color "#FFFFFF"

# Colori scuri con bordo nero spesso
python pie_chart_generator.py -o grafici -c "#2E2E2E,#D32F2F" --edge-width 3 --edge-color "#000000"

# Gradiente blu-verde senza bordo
python pie_chart_generator.py -o grafici -c "#1E3A8A,#10B981" --edge-width 0

# Colori tramonto con bordo dorato
python pie_chart_generator.py -o grafici -c "#FF6B6B,#FFE66D" --edge-width 2 --edge-color "#FFD700"

# Monocromo con bordo grigio
python pie_chart_generator.py -o grafici -c "#000000,#FFFFFF" --edge-width 4 --edge-color "#808080"

# Colori neon
python pie_chart_generator.py -o grafici -c "#00FFFF,#FF00FF" --edge-width 0

# Colori naturali
python pie_chart_generator.py -o grafici -c "#8B4513,#228B22" --edge-width 1.5 --edge-color "#FFFFFF"
```

**Opzioni Avanzate:**

```bash
# PNG trasparente ad alta qualità con testo
python pie_chart_generator.py -c "#FF4444,#44FF44" --edge-width 0 --transparent --format png --dpi 300 --show-percentage

# Generare GIF animata
python pie_chart_generator.py -c "#FF6B35,#004E89" --gif --gif-duration 100 --edge-width 0

# Intervallo personalizzato con passo
python pie_chart_generator.py -c "#1E3A8A,#10B981" -s 25 -e 75 --step 5 --edge-width 0
```

**Opzioni Larghezza Bordo:**
- `--edge-width 0`: Nessun bordo
- `--edge-width 0.5`: Bordo molto sottile
- `--edge-width 1`: Bordo sottile
- `--edge-width 2`: Bordo medio (predefinito)
- `--edge-width 3`: Bordo spesso
- `--edge-width 5`: Bordo molto spesso

**Opzioni Colore Bordo:**
- `--edge-color "#FFFFFF"`: Bianco (predefinito)
- `--edge-color "#000000"`: Nero
- `--edge-color "#808080"`: Grigio
- `--edge-color "#FFD700"`: Oro
- `--edge-color "none"`: Nessun bordo (equivalente a --edge-width 0)

**Argomenti:**

**Opzioni di Output:**
- `-o, --output-dir`: Directory di output per immagini generate
- `-f, --format`: Formato immagine di output (png, jpg, jpeg, pdf, svg, webp, tiff)
- `--dpi`: Risoluzione immagine in DPI (50-1000)
- `--atomic-writes`: Usare scritture atomiche per prevenire corruzione
- `--backup`: Creare backup di file esistenti

**Opzioni Visive:**
- `-c, --colors`: Due colori hex separati da virgola
- `-w, --width`: Larghezza figura in pollici
- `--height`: Altezza figura in pollici
- `--transparent`: Usare sfondo trasparente (predefinito: abilitato)
- `--no-transparent`: Usare sfondo bianco invece di trasparente

**Opzioni di Intervallo:**
- `-s, --start`: Percentuale iniziale (0-100)
- `-e, --end`: Percentuale finale (0-100)
- `--step`: Incremento del passo

**Aspetto del Grafico:**
- `--start-angle`: Angolo iniziale in gradi (0-360)
- `--clockwise`: Disegnare grafico a torta in senso orario
- `--edge-color`: Colore bordo per segmenti del grafico
- `--edge-width`: Larghezza linea bordo

**Opzioni Testo:**
- `--font-size`: Dimensione font per testo percentuale
- `--font-color`: Colore font per testo percentuale
- `--font-weight`: Peso font (normal, bold, light, ultralight, heavy)
- `--title-font-size`: Dimensione font del titolo
- `--show-percentage`: Mostrare testo percentuale al centro (predefinito: disabilitato)
- `--show-title`: Mostrare titolo del grafico (predefinito: disabilitato)

**Opzioni GIF:**
- `--gif`: Generare GIF animata
- `--gif-duration`: Durata frame GIF in millisecondi
- `--gif-loop`: Numero di cicli GIF (0=infinito)

**Opzioni Progresso:**
- `--quiet, -q`: Sopprimere output progresso
- `--verbose, -v`: Abilitare output dettagliato

**Configurazione:**
- `--config`: Caricare configurazione da file JSON
- `--save-config`: Salvare configurazione corrente in file JSON

## Deutsch

### Kreisdiagramm-Serien-Generator

Dieses Skript generiert eine Serie von Kreisdiagrammen, die den Fortschritt zweier Farben von 0% bis 100% in anpassbaren Schritten zeigt. Mit Python 3.13+ Funktionen erstellt, bietet es umfangreiche Anpassungsoptionen und robuste Fehlerbehandlung.

**Funktionen:**

- Generiert Kreisdiagramm-Serien mit anpassbaren Prozentbereichen und Schritten
- Unterstützt mehrere Ausgabeformate (PNG, JPG, JPEG, PDF, SVG, WEBP, TIFF)
- Erweiterte Befehlszeilenschnittstelle mit kurzen und langen Argumentformaten
- Umfassende Validierung mit PurePath für plattformübergreifende Kompatibilität
- Atomare Dateischreibungen mit Backup-Unterstützung zur Korruptionsvermeidung
- Farbige Terminal-Fortschrittsbalken und Statusmeldungen
- Optionale animierte GIF-Erstellung aus generierten Bildern
- Konfigurationsdatei-Unterstützung (JSON) zum Speichern und Laden von Einstellungen
- Umfangreiche Fehlerbehandlung mit benutzerdefinierten Ausnahmehierarchien
- Moderne Python 3.13+ Funktionen: dataclasses, enums, pattern matching, union types
- Transparenter Hintergrund-Support für PNG und andere kompatible Formate
- Optionale Textanzeigesteuerung (Prozentsatz und Titel)

**Grundlegende Verwendung:**

```bash
# Einfache Generierung mit Standardeinstellungen
python pie_chart_generator.py

# Benutzerdefinierte Farben und Ausgabeverzeichnis
python pie_chart_generator.py -o diagramme -c "#FF0000,#00FF00" -s 0 -e 50 --step 1
```

**Farbkombinationen und Randstile:**

```bash
# Lebendige Farben ohne Rand
python pie_chart_generator.py -o diagramme -c "#FF6B35,#004E89" --edge-width 0

# Pastellfarben mit dünnem weißen Rand
python pie_chart_generator.py -o diagramme -c "#FFB3BA,#BAE1FF" --edge-width 1 --edge-color "#FFFFFF"

# Dunkle Farben mit dickem schwarzen Rand
python pie_chart_generator.py -o diagramme -c "#2E2E2E,#D32F2F" --edge-width 3 --edge-color "#000000"

# Blau-grüner Verlauf ohne Rand
python pie_chart_generator.py -o diagramme -c "#1E3A8A,#10B981" --edge-width 0

# Sonnenuntergangsfarben mit goldenem Rand
python pie_chart_generator.py -o diagramme -c "#FF6B6B,#FFE66D" --edge-width 2 --edge-color "#FFD700"

# Monochrom mit grauem Rand
python pie_chart_generator.py -o diagramme -c "#000000,#FFFFFF" --edge-width 4 --edge-color "#808080"

# Neonfarben
python pie_chart_generator.py -o diagramme -c "#00FFFF,#FF00FF" --edge-width 0

# Natürliche Farben
python pie_chart_generator.py -o diagramme -c "#8B4513,#228B22" --edge-width 1.5 --edge-color "#FFFFFF"
```

**Erweiterte Optionen:**

```bash
# Hochwertiges transparentes PNG mit Text
python pie_chart_generator.py -c "#FF4444,#44FF44" --edge-width 0 --transparent --format png --dpi 300 --show-percentage

# Animierte GIF generieren
python pie_chart_generator.py -c "#FF6B35,#004E89" --gif --gif-duration 100 --edge-width 0

# Benutzerdefinierter Bereich mit Schritt
python pie_chart_generator.py -c "#1E3A8A,#10B981" -s 25 -e 75 --step 5 --edge-width 0
```

**Randbreiten-Optionen:**
- `--edge-width 0`: Kein Rand
- `--edge-width 0.5`: Sehr dünner Rand
- `--edge-width 1`: Dünner Rand
- `--edge-width 2`: Mittlerer Rand (Standard)
- `--edge-width 3`: Dicker Rand
- `--edge-width 5`: Sehr dicker Rand

**Randfarben-Optionen:**
- `--edge-color "#FFFFFF"`: Weiß (Standard)
- `--edge-color "#000000"`: Schwarz
- `--edge-color "#808080"`: Grau
- `--edge-color "#FFD700"`: Gold
- `--edge-color "none"`: Kein Rand (äquivalent zu --edge-width 0)

**Argumente:**

**Ausgabe-Optionen:**
- `-o, --output-dir`: Ausgabeverzeichnis für generierte Bilder
- `-f, --format`: Bildausgabeformat (png, jpg, jpeg, pdf, svg, webp, tiff)
- `--dpi`: Bildauflösung in DPI (50-1000)
- `--atomic-writes`: Atomare Dateischreibungen zur Korruptionsvermeidung verwenden
- `--backup`: Backups bestehender Dateien erstellen

**Visuelle Optionen:**
- `-c, --colors`: Zwei durch Komma getrennte Hex-Farben
- `-w, --width`: Figurbreite in Zoll
- `--height`: Figurhöhe in Zoll
- `--transparent`: Transparenten Hintergrund verwenden (Standard: aktiviert)
- `--no-transparent`: Weißen Hintergrund statt transparent verwenden

**Bereichs-Optionen:**
- `-s, --start`: Startprozentsatz (0-100)
- `-e, --end`: Endprozentsatz (0-100)
- `--step`: Schrittinkrement

**Diagramm-Erscheinungsbild:**
- `--start-angle`: Startwinkel in Grad (0-360)
- `--clockwise`: Kreisdiagramm im Uhrzeigersinn zeichnen
- `--edge-color`: Randfarbe für Diagrammsegmente
- `--edge-width`: Randlinienbreite

**Text-Optionen:**
- `--font-size`: Schriftgröße für Prozenttext
- `--font-color`: Schriftfarbe für Prozenttext
- `--font-weight`: Schriftgewicht (normal, bold, light, ultralight, heavy)
- `--title-font-size`: Titel-Schriftgröße
- `--show-percentage`: Prozenttext in der Mitte anzeigen (Standard: deaktiviert)
- `--show-title`: Diagrammtitel anzeigen (Standard: deaktiviert)

**GIF-Optionen:**
- `--gif`: Animierte GIF generieren
- `--gif-duration`: GIF-Frame-Dauer in Millisekunden
- `--gif-loop`: GIF-Wiederholungsanzahl (0=unendlich)

**Fortschritts-Optionen:**
- `--quiet, -q`: Fortschrittsausgabe unterdrücken
- `--verbose, -v`: Detaillierte Ausgabe aktivieren

**Konfiguration:**
- `--config`: Konfiguration aus JSON-Datei laden
- `--save-config`: Aktuelle Konfiguration in JSON-Datei speichern