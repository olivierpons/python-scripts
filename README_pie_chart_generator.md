# pie_chart_generator.py

## English

### Professional Pie Chart Series Generator

This script generates a comprehensive series of pie charts showing the progression of two colors from 0% to 100% in customizable increments. Built with modern Python 3.13+ features, it offers extensive customization options, robust error handling, and professional-grade file operations.

**Features:**

- Generates pie chart series with customizable percentage ranges and steps
- Supports multiple output formats (PNG, JPG, JPEG, PDF, SVG, WEBP, TIFF)
- Advanced command-line interface with short and long argument formats
- Comprehensive validation using PurePath for cross-platform compatibility
- Atomic file writes with backup support to prevent corruption
- Colorful terminal progress bars and status messages without icons
- Optional animated GIF creation from generated images
- Configuration file support (JSON) for saving and loading settings
- Extensive error handling with custom exception hierarchy
- Modern Python 3.13+ features: dataclasses, enums, pattern matching, union types

**Usage:**

```bash
python pie_chart_generator.py [options]

# Basic usage
python pie_chart_generator.py -o charts -c "#FF0000,#00FF00"

# Advanced usage with custom range and format
python pie_chart_generator.py --output-dir results --colors "#123456,#ABCDEF" \
    --start 10 --end 90 --step 5 --format webp --dpi 300 --gif

# Load/save configuration
python pie_chart_generator.py --config settings.json --save-config my_config.json
```

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
- `--no-percentage`: Hide percentage text in center

**GIF Options:**
- `--gif`: Generate animated GIF
- `--gif-duration`: GIF frame duration in milliseconds
- `--gif-loop`: GIF loop count (0=infinite)

**Progress Options:**
- `--progress-width`: Progress bar width in characters
- `--quiet, -q`: Suppress progress output
- `--verbose, -v`: Enable verbose output

**Configuration:**
- `--config`: Load configuration from JSON file
- `--save-config`: Save current configuration to JSON file

## Français

### Générateur Professionnel de Séries de Camemberts

Ce script génère une série complète de camemberts montrant la progression de deux couleurs de 0% à 100% par incréments personnalisables. Construit avec les fonctionnalités modernes de Python 3.13+, il offre de nombreuses options de personnalisation, une gestion d'erreurs robuste et des opérations de fichiers de qualité professionnelle.

**Fonctionnalités :**

- Génère des séries de camemberts avec des plages de pourcentages et des pas personnalisables
- Supporte plusieurs formats de sortie (PNG, JPG, JPEG, PDF, SVG, WEBP, TIFF)
- Interface en ligne de commande avancée avec formats d'arguments courts et longs
- Validation complète utilisant PurePath pour la compatibilité multiplateforme
- Écritures atomiques de fichiers avec support de sauvegarde pour éviter la corruption
- Barres de progression et messages d'état colorés dans le terminal sans icônes
- Création optionnelle de GIF animés à partir des images générées
- Support de fichiers de configuration (JSON) pour sauvegarder et charger les paramètres
- Gestion d'erreurs extensive avec hiérarchie d'exceptions personnalisée
- Fonctionnalités modernes Python 3.13+ : dataclasses, enums, pattern matching, types union

**Utilisation :**

```bash
python pie_chart_generator.py [options]

# Utilisation basique
python pie_chart_generator.py -o graphiques -c "#FF0000,#00FF00"

# Utilisation avancée avec plage et format personnalisés
python pie_chart_generator.py --output-dir resultats --colors "#123456,#ABCDEF" \
    --start 10 --end 90 --step 5 --format webp --dpi 300 --gif

# Charger/sauvegarder la configuration
python pie_chart_generator.py --config parametres.json --save-config ma_config.json
```

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
- `--no-percentage` : Masquer le texte de pourcentage au centre

**Options GIF :**
- `--gif` : Générer un GIF animé
- `--gif-duration` : Durée de frame GIF en millisecondes
- `--gif-loop` : Nombre de boucles GIF (0=infini)

**Options de Progression :**
- `--progress-width` : Largeur de la barre de progression en caractères
- `--quiet, -q` : Supprimer la sortie de progression
- `--verbose, -v` : Activer la sortie détaillée

**Configuration :**
- `--config` : Charger la configuration depuis un fichier JSON
- `--save-config` : Sauvegarder la configuration actuelle dans un fichier JSON

## 日本語

### プロフェッショナル円グラフシリーズジェネレーター

このスクリプトは、2つの色の0%から100%への進行を示す包括的な円グラフシリーズを、カスタマイズ可能な増分で生成します。Python 3.13+の最新機能で構築され、豊富なカスタマイズオプション、堅牢なエラー処理、プロフェッショナル品質のファイル操作を提供します。

**機能：**

- カスタマイズ可能なパーセンテージ範囲とステップで円グラフシリーズを生成
- 複数の出力形式をサポート（PNG、JPG、JPEG、PDF、SVG、WEBP、TIFF）
- 短縮形と長形式の引数形式を持つ高度なコマンドライン インターフェース
- クロスプラットフォーム互換性のためのPurePathを使用した包括的検証
- 破損を防ぐバックアップサポート付きアトミックファイル書き込み
- アイコンなしのカラフルなターミナル進行状況バーとステータスメッセージ
- 生成された画像からのオプションのアニメーションGIF作成
- 設定の保存と読み込みのための設定ファイルサポート（JSON）
- カスタム例外階層による広範なエラー処理
- 最新のPython 3.13+機能：データクラス、列挙型、パターンマッチング、ユニオン型

**使用方法：**

```bash
python pie_chart_generator.py [オプション]

# 基本的な使用法
python pie_chart_generator.py -o charts -c "#FF0000,#00FF00"

# カスタム範囲と形式での高度な使用法
python pie_chart_generator.py --output-dir results --colors "#123456,#ABCDEF" \
    --start 10 --end 90 --step 5 --format webp --dpi 300 --gif

# 設定の読み込み/保存
python pie_chart_generator.py --config settings.json --save-config my_config.json
```

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
- `--no-percentage`：中央のパーセンテージテキストを非表示

**GIFオプション：**
- `--gif`：アニメーションGIFを生成
- `--gif-duration`：ミリ秒単位のGIFフレーム時間
- `--gif-loop`：GIFループ回数（0=無限）

**進行状況オプション：**
- `--progress-width`：文字数での進行状況バー幅
- `--quiet, -q`：進行状況出力を抑制
- `--verbose, -v`：詳細出力を有効化

**設定：**
- `--config`：JSONファイルから設定を読み込み
- `--save-config`：現在の設定をJSONファイルに保存

## 简体中文

### 专业饼图系列生成器

此脚本生成全面的饼图系列，显示两种颜色从0%到100%的进展，具有可自定义的增量。使用现代Python 3.13+功能构建，提供广泛的自定义选项、强大的错误处理和专业级文件操作。

**功能：**

- 生成具有可自定义百分比范围和步长的饼图系列
- 支持多种输出格式（PNG、JPG、JPEG、PDF、SVG、WEBP、TIFF）
- 具有短格式和长格式参数的高级命令行界面
- 使用PurePath进行跨平台兼容性的全面验证
- 具有备份支持的原子文件写入以防止损坏
- 无图标的彩色终端进度条和状态消息
- 从生成的图像可选创建动画GIF
- 配置文件支持（JSON）用于保存和加载设置
- 具有自定义异常层次结构的广泛错误处理
- 现代Python 3.13+功能：数据类、枚举、模式匹配、联合类型

**使用方法：**

```bash
python pie_chart_generator.py [选项]

# 基本用法
python pie_chart_generator.py -o charts -c "#FF0000,#00FF00"

# 具有自定义范围和格式的高级用法
python pie_chart_generator.py --output-dir results --colors "#123456,#ABCDEF" \
    --start 10 --end 90 --step 5 --format webp --dpi 300 --gif

# 加载/保存配置
python pie_chart_generator.py --config settings.json --save-config my_config.json
```

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
- `--no-percentage`：隐藏中心百分比文本

**GIF选项：**
- `--gif`：生成动画GIF
- `--gif-duration`：毫秒为单位的GIF帧持续时间
- `--gif-loop`：GIF循环次数（0=无限）

**进度选项：**
- `--progress-width`：字符为单位的进度条宽度
- `--quiet, -q`：抑制进度输出
- `--verbose, -v`：启用详细输出

**配置：**
- `--config`：从JSON文件加载配置
- `--save-config`：将当前配置保存到JSON文件

## 繁體中文

### 專業圓餅圖系列產生器

此腳本生成全面的圓餅圖系列，顯示兩種顏色從0%到100%的進展，具有可自訂的增量。使用現代Python 3.13+功能構建，提供廣泛的自訂選項、強大的錯誤處理和專業級檔案操作。

**功能：**

- 生成具有可自訂百分比範圍和步長的圓餅圖系列
- 支援多種輸出格式（PNG、JPG、JPEG、PDF、SVG、WEBP、TIFF）
- 具有短格式和長格式參數的進階命令列介面
- 使用PurePath進行跨平台相容性的全面驗證
- 具有備份支援的原子檔案寫入以防止損壞
- 無圖標的彩色終端進度條和狀態訊息
- 從生成的圖像可選創建動畫GIF
- 組態檔案支援（JSON）用於保存和載入設定
- 具有自訂例外階層的廣泛錯誤處理
- 現代Python 3.13+功能：資料類、列舉、模式匹配、聯合類型

**使用方法：**

```bash
python pie_chart_generator.py [選項]

# 基本用法
python pie_chart_generator.py -o charts -c "#FF0000,#00FF00"

# 具有自訂範圍和格式的進階用法
python pie_chart_generator.py --output-dir results --colors "#123456,#ABCDEF" \
    --start 10 --end 90 --step 5 --format webp --dpi 300 --gif

# 載入/保存設定
python pie_chart_generator.py --config settings.json --save-config my_config.json
```

**參數：**

**輸出選項：**
- `-o, --output-dir`：生成圖像的輸出目錄
- `-f, --format`：輸出圖像格式（png、jpg、jpeg、pdf、svg、webp、tiff）
- `--dpi`：DPI圖像解析度（50-1000）
- `--atomic-writes`：使用原子檔案寫入防止損壞
- `--backup`：創建現有檔案的備份

**視覺選項：**
- `-c, --colors`：用逗號分隔的兩種十六進制顏色
- `-w, --width`：英寸為單位的圖形寬度
- `--height`：英寸為單位的圖形高度

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
- `--no-percentage`：隱藏中心百分比文字

**GIF選項：**
- `--gif`：生成動畫GIF
- `--gif-duration`：毫秒為單位的GIF幀持續時間
- `--gif-loop`：GIF循環次數（0=無限）

**進度選項：**
- `--progress-width`：字元為單位的進度條寬度
- `--quiet, -q`：抑制進度輸出
- `--verbose, -v`：啟用詳細輸出

**組態：**
- `--config`：從JSON檔案載入組態
- `--save-config`：將目前組態保存到JSON檔案

## Español

### Generador Profesional de Series de Gráficos Circulares

Este script genera una serie completa de gráficos circulares que muestran la progresión de dos colores del 0% al 100% en incrementos personalizables. Construido con características modernas de Python 3.13+, ofrece amplias opciones de personalización, manejo robusto de errores y operaciones de archivos de calidad profesional.

**Características:**

- Genera series de gráficos circulares con rangos de porcentaje y pasos personalizables
- Soporta múltiples formatos de salida (PNG, JPG, JPEG, PDF, SVG, WEBP, TIFF)
- Interfaz de línea de comandos avanzada con formatos de argumentos cortos y largos
- Validación exhaustiva usando PurePath para compatibilidad multiplataforma
- Escrituras atómicas de archivos con soporte de respaldo para prevenir corrupción
- Barras de progreso y mensajes de estado coloridos en terminal sin iconos
- Creación opcional de GIF animado a partir de imágenes generadas
- Soporte de archivos de configuración (JSON) para guardar y cargar ajustes
- Manejo extensivo de errores con jerarquía de excepciones personalizada
- Características modernas de Python 3.13+: dataclasses, enums, pattern matching, union types

**Uso:**

```bash
python pie_chart_generator.py [opciones]

# Uso básico
python pie_chart_generator.py -o graficos -c "#FF0000,#00FF00"

# Uso avanzado con rango y formato personalizado
python pie_chart_generator.py --output-dir resultados --colors "#123456,#ABCDEF" \
    --start 10 --end 90 --step 5 --format webp --dpi 300 --gif

# Cargar/guardar configuración
python pie_chart_generator.py --config ajustes.json --save-config mi_config.json
```

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
- `--no-percentage`: Ocultar texto de porcentaje en el centro

**Opciones GIF:**
- `--gif`: Generar GIF animado
- `--gif-duration`: Duración de frame GIF en milisegundos
- `--gif-loop`: Número de bucles GIF (0=infinito)

**Opciones de Progreso:**
- `--progress-width`: Ancho de barra de progreso en caracteres
- `--quiet, -q`: Suprimir salida de progreso
- `--verbose, -v`: Habilitar salida detallada

**Configuración:**
- `--config`: Cargar configuración desde archivo JSON
- `--save-config`: Guardar configuración actual en archivo JSON

## Italiano

### Generatore Professionale di Serie di Grafici a Torta

Questo script genera una serie completa di grafici a torta che mostrano la progressione di due colori dallo 0% al 100% in incrementi personalizzabili. Costruito con funzionalità moderne di Python 3.13+, offre ampie opzioni di personalizzazione, gestione robusta degli errori e operazioni sui file di qualità professionale.

**Funzionalità:**

- Genera serie di grafici a torta con intervalli percentuali e passi personalizzabili
- Supporta formati di output multipli (PNG, JPG, JPEG, PDF, SVG, WEBP, TIFF)
- Interfaccia a riga di comando avanzata con formati di argomenti corti e lunghi
- Validazione completa utilizzando PurePath per compatibilità multipiattaforma
- Scritture atomiche di file con supporto backup per prevenire corruzione
- Barre di progresso e messaggi di stato colorati nel terminale senza icone
- Creazione opzionale di GIF animata dalle immagini generate
- Supporto file di configurazione (JSON) per salvare e caricare impostazioni
- Gestione estensiva degli errori con gerarchia di eccezioni personalizzata
- Funzionalità moderne Python 3.13+: dataclasses, enums, pattern matching, union types

**Utilizzo:**

```bash
python pie_chart_generator.py [opzioni]

# Uso base
python pie_chart_generator.py -o grafici -c "#FF0000,#00FF00"

# Uso avanzato con intervallo e formato personalizzato
python pie_chart_generator.py --output-dir risultati --colors "#123456,#ABCDEF" \
    --start 10 --end 90 --step 5 --format webp --dpi 300 --gif

# Caricare/salvare configurazione
python pie_chart_generator.py --config impostazioni.json --save-config mia_config.json
```

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
- `--no-percentage`: Nascondere testo percentuale al centro

**Opzioni GIF:**
- `--gif`: Generare GIF animata
- `--gif-duration`: Durata frame GIF in millisecondi
- `--gif-loop`: Numero di cicli GIF (0=infinito)

**Opzioni Progresso:**
- `--progress-width`: Larghezza barra progresso in caratteri
- `--quiet, -q`: Sopprimere output progresso
- `--verbose, -v`: Abilitare output dettagliato

**Configurazione:**
- `--config`: Caricare configurazione da file JSON
- `--save-config`: Salvare configurazione corrente in file JSON

## Deutsch

### Professioneller Kreisdiagramm-Serien-Generator

Dieses Skript generiert eine umfassende Serie von Kreisdiagrammen, die den Fortschritt zweier Farben von 0% bis 100% in anpassbaren Schritten zeigt. Mit modernen Python 3.13+ Funktionen erstellt, bietet es umfangreiche Anpassungsoptionen, robuste Fehlerbehandlung und professionelle Dateioperationen.

**Funktionen:**

- Generiert Kreisdiagramm-Serien mit anpassbaren Prozentbereichen und Schritten
- Unterstützt mehrere Ausgabeformate (PNG, JPG, JPEG, PDF, SVG, WEBP, TIFF)
- Erweiterte Befehlszeilenschnittstelle mit kurzen und langen Argumentformaten
- Umfassende Validierung mit PurePath für plattformübergreifende Kompatibilität
- Atomare Dateischreibungen mit Backup-Unterstützung zur Korruptionsvermeidung
- Farbige Terminal-Fortschrittsbalken und Statusmeldungen ohne Symbole
- Optionale animierte GIF-Erstellung aus generierten Bildern
- Konfigurationsdatei-Unterstützung (JSON) zum Speichern und Laden von Einstellungen
- Umfangreiche Fehlerbehandlung mit benutzerdefinierten Ausnahmehierarchien
- Moderne Python 3.13+ Funktionen: dataclasses, enums, pattern matching, union types

**Verwendung:**

```bash
python pie_chart_generator.py [optionen]

# Grundlegende Verwendung
python pie_chart_generator.py -o diagramme -c "#FF0000,#00FF00"

# Erweiterte Verwendung mit benutzerdefiniertem Bereich und Format
python pie_chart_generator.py --output-dir ergebnisse --colors "#123456,#ABCDEF" \
    --start 10 --end 90 --step 5 --format webp --dpi 300 --gif

# Konfiguration laden/speichern
python pie_chart_generator.py --config einstellungen.json --save-config meine_config.json
```

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
- `--no-percentage`: Prozenttext in der Mitte ausblenden

**GIF-Optionen:**
- `--gif`: Animierte GIF generieren
- `--gif-duration`: GIF-Frame-Dauer in Millisekunden
- `--gif-loop`: GIF-Wiederholungsanzahl (0=unendlich)

**Fortschritts-Optionen:**
- `--progress-width`: Fortschrittsbalkenbreite in Zeichen
- `--quiet, -q`: Fortschrittsausgabe unterdrücken
- `--verbose, -v`: Detaillierte Ausgabe aktivieren

**Konfiguration:**
- `--config`: Konfiguration aus JSON-Datei laden
- `--save-config`: Aktuelle Konfiguration in JSON-Datei speichern