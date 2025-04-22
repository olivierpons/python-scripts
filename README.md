# Python Utility Scripts / Scripts Utilitaires Python / Python ユーティリティスクリプト / Python 实用脚本 / Python 實用腳本

## Quick Overview / Aperçu Rapide / 概要 / 概述

### English

This repository contains a collection of small Python utility scripts designed to automate common tasks and solve
specific problems. Currently available:

- [**eliminate_dups_in_csv.py**](#eliminate_dups_en): Processes CSV files to remove duplicates and saves them separately.
- [**extract_first_column_of_csv.py**](#extract_first_column_en): Extracts the first column from a CSV file.
- [**scans_rename.py**](#scans_rename_en): Renames and organizes files with Japanese timestamps in their filenames.
- [**csv_transformer.py**](#csv_transformer_en): Transforms, filters, and processes CSV data with various operations.
[More details below](#english-details)

### Français
Ce dépôt contient une collection de petits scripts utilitaires Python conçus pour
automatiser des tâches courantes et résoudre des problèmes spécifiques. Actuellement 
disponible :
- [**eliminate_dups_in_csv.py**](#eliminate_dups_fr) : Traite les fichiers CSV pour supprimer les doublons et les enregistre séparément.
- [**extract_first_column_of_csv.py**](#extract_first_column_fr) : Extrait la première colonne d'un fichier CSV.
- [**scans_rename.py**](#scans_rename_fr) : Renomme et organise les fichiers avec des horodatages japonais dans leurs noms.
- [**csv_transformer.py**](#csv_transformer_fr) : Transforme, filtre et traite les données CSV avec diverses opérations.
[Plus de détails ci-dessous](#french-details)

### 日本語
このリポジトリには、一般的なタスクを自動化し、特定の問題を解決するために設計された小さなPythonユーティリティスクリプトのコレクションが含まれています。現在利用可能：
- [**eliminate_dups_in_csv.py**](#eliminate_dups_jp)：CSVファイルを処理して重複を削除し、別々に保存します。
- [**extract_first_column_of_csv.py**](#extract_first_column_jp)：CSVファイルの最初の列を抽出します。
- [**scans_rename.py**](#scans_rename_jp)：ファイル名の日本語タイムスタンプを持つファイルの名前変更と整理を行います。
- [**csv_transformer.py**](#csv_transformer_jp)：様々な操作でCSVデータを変換、フィルタリング、処理します。
[詳細は以下をご覧ください](#japanese-details)

### 简体中文

本仓库包含一系列小型Python实用脚本，旨在自动化常见任务并解决特定问题。目前可用：

- [**eliminate_dups_in_csv.py**](#eliminate_dups_zh_cn)：处理CSV文件以删除重复项并将其单独保存。
- [**extract_first_column_of_csv.py**](#extract_first_column_zh_cn)：从CSV文件中提取第一列。
- [**scans_rename.py**](#scans_rename_zh_cn)：重命名并整理文件名中带有日语时间戳的文件。
- [**csv_transformer.py**](#csv_transformer_zh_cn)：通过各种操作转换、过滤和处理CSV数据。

[更多详情见下文](#chinese-simplified-details)

### 繁體中文

本倉庫包含一系列小型Python實用腳本，旨在自動化常見任務並解決特定問題。目前可用：

- [**eliminate_dups_in_csv.py**](#eliminate_dups_zh_tw)：處理CSV檔案以刪除重複項並將其單獨保存。
- [**extract_first_column_of_csv.py**](#extract_first_column_zh_tw)：從CSV檔案中提取第一列。
- [**scans_rename.py**](#scans_rename_zh_tw)：重新命名並整理檔案名中帶有日語時間戳的檔案。
- [**csv_transformer.py**](#csv_transformer_zh_tw)：通過各種操作轉換、過濾和處理CSV數據。

[更多詳情見下文](#chinese-traditional-details)

---

<a id="english-details"></a>
## English Details

### Project Overview

This repository contains a collection of small Python utility scripts designed to automate common tasks and solve
specific problems. Each script is self-contained and focuses on a single functionality, making them easy to use and
modify.

### Current Scripts

<a id="eliminate_dups_en"></a>
#### 1. `eliminate_dups_in_csv.py` - CSV Duplicate Remover

This script processes CSV files to identify and remove duplicate entries, saving them into separate files for review.

**Features:**
- Identifies and removes duplicate entries from CSV files
- Works with any CSV file regardless of its content or number of columns
- Creates a clean output file without duplicates
- Saves identified duplicates to a separate file
- Provides a comprehensive summary of the operation
- Customizable encoding, delimiter, and table display format

**Usage:**
```bash
python eliminate_dups_in_csv.py input_file.csv output_file.csv duplicates_file.csv [options]
```

**Arguments:**
- `input_file`: Path to the input CSV file
- `output_file`: Path to save the CSV file without duplicates
- `duplicates_file`: Path to save the CSV file containing only duplicates
- `--encoding`: CSV file encoding (default: utf-8)
- `--delimiter`: CSV file delimiter (default: ,)
- `--table-format`: Format for summary table (default: fancy_grid)

<a id="extract_first_column_en"></a>
#### 2. `extract_first_column_of_csv.py` - CSV First Column Extractor

This script extracts the content of the first column from a CSV file and outputs the values as a comma-separated list with each value surrounded by quotes.

**Features:**
- Extracts the first column from any CSV file
- Outputs values in a formatted comma-separated list with quotes
- Handles file opening errors gracefully
- Simple and focused functionality

**Usage:**
```bash
python extract_first_column_of_csv.py -i input_file.csv
```

**Arguments:**
- `-i, --input`: Path to the input CSV file (required)

<a id="scans_rename_en"></a>
#### 3. `scans_rename.py` - Japanese Timestamp File Organizer

This script helps manage and organize scanned files with Japanese timestamps in their filenames. It was created out
of necessity to deal with the... limitations of the 💩 Canon ImageFORMULA driver written by 🤬 🧠💀 developers that
only works properly on Windows and lacks the ability to generate proper file formats.

**Features:**
- Renames files from Japanese timestamp format (`YYYYMMDD-HH時MM分SS秒-XXX.jpg`) to Latin format (`YYYYMMDD-HHhMMmSSs-XXX.jpg`)
- Organizes files into folders based on their timestamp prefixes
- Creates web-friendly resized versions of images in "petites" subfolders
- Organizes numbered files (e.g., "1.jpg", "2.jpg") using clipboard content for folder naming
- Includes a dry-run mode to preview changes without modifying files
- Configurable verbosity levels for detailed operation feedback

**Usage:**
```bash
python scans_rename.py --directory PATH [--rename] [--organize] [--resize] \
    [--numbered] [--dry-run] [--verbose LEVEL]
```

**Arguments:**
- `-d, --directory`: Directory containing files to process (defaults to current directory)
- `-r, --dry-run`: Simulate operations without changing any files
- `-n, --rename`: Enable the file renaming step (Japanese '時分秒' to Latin 'hms')
- `-o, --organize`: Enable the file organization step (move files into timestamp-named folders)
- `-z, --resize`: Enable the image resizing step (creating web-friendly versions in "petites" subfolders)
- `-x, --numbered`: Enable organizing numbered files using clipboard content
- `-m, --max-pixels`: Maximum size in pixels for resized images (default: 2000)
- `-q, --quality`: JPEG quality for resized images (70-100, default: 80)
- `-v, --verbose`: Verbosity level: 0=quiet, 1=summary, 2=details (default: 0)
- `-w, --overwrite`: Overwrite existing files when moving or resizing
- `-c, --current-dir`: Include images in the current directory itself when resizing

<a id="csv_transformer_en"></a>
#### 4. `csv_transformer.py` - CSV Transformation Utility

This script provides comprehensive CSV transformation capabilities for data processing workflows.

**Features:**
- Column selection, renaming, and reordering
- Row filtering based on conditions
- Data transformation with custom functions
- Aggregation and grouping operations
- Statistical analysis and summary generation
- Supports multiple input and output encoding formats
- Batch processing of multiple CSV files

**Usage:**
```bash
python csv_transformer.py --input input.csv --output transformed.csv [options]
```

**Arguments:**
- `--input`: Path to the input CSV file
- `--output`: Path to save the transformed CSV file
- `--select`: Select specific columns (comma-separated)
- `--rename`: Rename columns (format: old_name:new_name,old_name2:new_name2)
- `--filter`: Filter rows using a Python expression
- `--transform`: Apply transformations to columns
- `--encoding`: Input/output encoding (default: utf-8)
- `--delimiter`: CSV delimiter character (default: ,)
- `--group-by`: Group data by specified columns
- `--aggregate`: Aggregate function to apply to groups

### Future Plans
More Python utility scripts will be added to this repository over time, each focused
on solving specific tasks efficiently.

[Back to top](#python-utility-scripts--scripts-utilitaires-python--python-ユーティリティスクリプト--python-实用脚本--python-實用腳本)

---

<a id="french-details"></a>
## Détails en Français

### Aperçu du Projet
Ce dépôt contient une collection de petits scripts utilitaires Python conçus pour automatiser des tâches courantes et résoudre des problèmes spécifiques. Chaque script est autonome et se concentre sur une fonctionnalité unique, ce qui les rend faciles à utiliser et à modifier.

### Scripts Actuels

<a id="eliminate_dups_fr"></a>
#### 1. `eliminate_dups_in_csv.py` - Suppresseur de doublons CSV

Ce script traite les fichiers CSV pour identifier et supprimer les entrées en double, en les enregistrant dans des fichiers séparés pour examen.

**Fonctionnalités :**
- Identifie et supprime les entrées en double des fichiers CSV
- Fonctionne avec n'importe quel fichier CSV, quel que soit son contenu ou son nombre de colonnes
- Crée un fichier de sortie propre sans doublons
- Enregistre les doublons identifiés dans un fichier séparé
- Fournit un résumé complet de l'opération
- Format d'encodage, délimiteur et affichage de tableau personnalisables

**Utilisation :**
```bash
python eliminate_dups_in_csv.py fichier_entree.csv fichier_sortie.csv fichier_doublons.csv [options]
```

**Arguments :**
- `fichier_entree` : Chemin vers le fichier CSV d'entrée
- `fichier_sortie` : Chemin pour enregistrer le fichier CSV sans doublons
- `fichier_doublons` : Chemin pour enregistrer le fichier CSV contenant uniquement les doublons
- `--encoding` : Encodage du fichier CSV (par défaut : utf-8)
- `--delimiter` : Délimiteur du fichier CSV (par défaut : ,)
- `--table-format` : Format pour le tableau récapitulatif (par défaut : fancy_grid)

<a id="extract_first_column_fr"></a>
#### 2. `extract_first_column_of_csv.py` - Extracteur de Première Colonne CSV

Ce script extrait le contenu de la première colonne d'un fichier CSV et génère les valeurs sous forme de liste séparée par des virgules, chaque valeur étant entourée de guillemets.

**Fonctionnalités :**
- Extrait la première colonne de n'importe quel fichier CSV
- Génère des valeurs dans une liste formatée séparée par des virgules avec des guillemets
- Gère les erreurs d'ouverture de fichier avec élégance
- Fonctionnalité simple et ciblée

**Utilisation :**
```bash
python extract_first_column_of_csv.py -i fichier_entree.csv
```

**Arguments :**
- `-i, --input` : Chemin vers le fichier CSV d'entrée (requis)

<a id="scans_rename_fr"></a>
#### 3. `scans_rename.py` - Organisateur de Fichiers avec Horodatage Japonais
Ce script aide à gérer et organiser les fichiers numérisés avec des horodatages japonais
dans leurs noms de fichier. Il a été créé par nécessité pour faire face aux... 
limitations du pilote 💩 Canon ImageFORMULA écrit par des 🤬 🧠💀 de développeurs, 
ne fonctionne correctement que sous Windows et n'a pas la possibilité de générer des 
formats de fichiers appropriés.

**Fonctionnalités :**
- Renomme les fichiers du format d'horodatage japonais (`YYYYMMDD-HH時MM分SS秒-XXX.jpg`)
  au format latin (`YYYYMMDD-HHhMMmSSs-XXX.jpg`)
- Organise les fichiers dans des dossiers basés sur leurs préfixes d'horodatage
- Crée des versions redimensionnées adaptées au web dans des sous-dossiers "petites"
- Organise les fichiers numérotés (ex. "1.jpg", "2.jpg") en utilisant le contenu du 
  presse-papiers pour nommer les dossiers
- Inclut un mode simulation pour prévisualiser les changements sans modifier les 
  fichiers
- Niveaux de verbosité configurables pour un retour détaillé des opérations

**Utilisation :**
```bash
python scans_rename.py --directory CHEMIN [--rename] [--organize] [--resize] \
  [--numbered] [--dry-run] [--verbose NIVEAU]
```

**Arguments :**
- `-d, --directory` : Répertoire contenant les fichiers à traiter (par défaut :
  répertoire courant)
- `-r, --dry-run` : Simuler les opérations sans changer aucun fichier
- `-n, --rename` : Activer l'étape de renommage des fichiers (japonais '時分秒' vers 
  latin 'hms')
- `-o, --organize` : Activer l'étape d'organisation des fichiers (déplacer les fichiers
  dans des dossiers nommés selon l'horodatage)
- `-z, --resize` : Activer l'étape de redimensionnement d'images (créer des versions
  adaptées au web dans des sous-dossiers "petites")
- `-x, --numbered` : Activer l'organisation des fichiers numérotés en utilisant le
  contenu du presse-papiers
- `-m, --max-pixels` : Taille maximale en pixels pour les images redimensionnées (par
  défaut : 2000)
- `-q, --quality` : Qualité JPEG pour les images redimensionnées (70-100, 
  par défaut : 80)
- `-v, --verbose` : Niveau de verbosité : 0=silencieux, 1=résumé, 2=détails
  (par défaut : 0)
- `-w, --overwrite` : Écraser les fichiers existants lors du déplacement ou du 
  redimensionnement
- `-c, --current-dir` : Inclure les images dans le répertoire courant lors du redimensionnement

<a id="csv_transformer_fr"></a>
#### 4. `csv_transformer.py` - Utilitaire de Transformation CSV

Ce script fournit des capacités complètes de transformation CSV pour les flux de traitement de données.

**Fonctionnalités :**
- Sélection, renommage et réorganisation des colonnes
- Filtrage des lignes basé sur des conditions
- Transformation de données avec des fonctions personnalisées
- Opérations d'agrégation et de regroupement
- Analyse statistique et génération de résumés
- Prend en charge plusieurs formats d'encodage d'entrée et de sortie
- Traitement par lots de plusieurs fichiers CSV

**Utilisation :**
```bash
python csv_transformer.py --input input.csv --output transforme.csv [options]
```

**Arguments :**
- `--input` : Chemin vers le fichier CSV d'entrée
- `--output` : Chemin pour enregistrer le fichier CSV transformé
- `--select` : Sélectionner des colonnes spécifiques (séparées par des virgules)
- `--rename` : Renommer les colonnes (format : ancien_nom:nouveau_nom,ancien_nom2:nouveau_nom2)
- `--filter` : Filtrer les lignes en utilisant une expression Python
- `--transform` : Appliquer des transformations aux colonnes
- `--encoding` : Encodage d'entrée/sortie (par défaut : utf-8)
- `--delimiter` : Caractère délimiteur CSV (par défaut : ,)
- `--group-by` : Regrouper les données par colonnes spécifiées
- `--aggregate` : Fonction d'agrégation à appliquer aux groupes

### Plans Futurs
D'autres scripts utilitaires Python seront ajoutés à ce dépôt au fil du temps, chacun se
concentrant sur la résolution efficace de tâches spécifiques.

[Retour en haut](#python-utility-scripts--scripts-utilitaires-python--python-ユーティリティスクリプト--python-实用脚本--python-實用腳本)

---

<a id="japanese-details"></a>
## 日本語の詳細

### プロジェクト概要
このリポジトリには、一般的なタスクを自動化し、特定の問題を解決するために設計された小さなPythonユーティリティスクリプトのコレクションが含まれています。各スクリプトは独立しており、単一の機能に焦点を当てているため、使用や修正が容易です。

### 現在のスクリプト

<a id="eliminate_dups_jp"></a>
#### 1. `eliminate_dups_in_csv.py` - CSV重複除去ツール

このスクリプトはCSVファイルを処理して重複エントリを特定し、削除して、レビュー用に別のファイルに保存します。

**機能：**
- CSVファイルから重複エントリを特定して削除
- コンテンツや列数に関係なく、あらゆるCSVファイルに対応
- 重複のないクリーンな出力ファイルを作成
- 特定された重複を別のファイルに保存
- 操作の包括的な概要を提供
- エンコーディング、区切り文字、テーブル表示形式のカスタマイズ可能

**使用法：**
```bash
python eliminate_dups_in_csv.py 入力ファイル.csv 出力ファイル.csv 重複ファイル.csv [オプション]
```

**引数：**
- `入力ファイル`：入力CSVファイルへのパス
- `出力ファイル`：重複のないCSVファイルを保存するパス
- `重複ファイル`：重複のみを含むCSVファイルを保存するパス
- `--encoding`：CSVファイルのエンコーディング（デフォルト：utf-8）
- `--delimiter`：CSVファイルの区切り文字（デフォルト：,）
- `--table-format`：概要テーブルの形式（デフォルト：fancy_grid）

<a id="extract_first_column_jp"></a>
#### 2. `extract_first_column_of_csv.py` - CSV最初の列抽出ツール

このスクリプトはCSVファイルの最初の列のコンテンツを抽出し、各値を引用符で囲んだコンマ区切りのリストとして出力します。

**機能：**
- 任意のCSVファイルから最初の列を抽出
- 引用符で囲まれたフォーマット済みのコンマ区切りリストとして値を出力
- ファイルオープンエラーを適切に処理
- シンプルで焦点を絞った機能性

**使用法：**
```bash
python extract_first_column_of_csv.py -i 入力ファイル.csv
```

**引数：**
- `-i, --input`：入力CSVファイルへのパス（必須）

<a id="scans_rename_jp"></a>
#### 3. `scans_rename.py` - 日本語タイムスタンプファイル整理ツール
このスクリプトは、ファイル名に日本語のタイムスタンプが付いたスキャンファイルの管理と整理を支援します。このスクリプトは、Canon ImageFORMULAドライバー（💩）の限界に対処するために作成されました。このドライバーは能力のない開発者（🤬 🧠💀）によって作られ、Windowsでしか正常に動作せず、適切なファイル形式を生成する機能が欠けています。

**機能：**
- ファイル名を日本語タイムスタンプ形式（`YYYYMMDD-HH時MM分SS秒-XXX.jpg`）からラテン形式（`YYYYMMDD-HHhMMmSSs-XXX.jpg`）に変更
- タイムスタンプのプレフィックスに基づいてファイルをフォルダに整理
- "petites"サブフォルダにウェブ用にリサイズされた画像バージョンを作成
- クリップボードの内容を使用して番号付きファイル（例：「1.jpg」、「2.jpg」）を整理
- ファイルを変更せずに変更をプレビューするドライランモードを含む
- 詳細な操作フィードバックのための設定可能な詳細レベル

**使用法：**
```bash
python scans_rename.py --directory パス [--rename] [--organize] [--resize] \
  [--numbered] [--dry-run] [--verbose レベル]
```

**引数：**
- `-d, --directory`：処理するファイルを含むディレクトリ（デフォルトは現在のディレクトリ）
- `-r, --dry-run`：ファイルを変更せずに操作をシミュレート
- `-n, --rename`：ファイル名変更ステップを有効にする（日本語の'時分秒'をラテン文字の'hms'に）
- `-o, --organize`：ファイル整理ステップを有効にする（タイムスタンプ名のフォルダにファイルを移動）
- `-z, --resize`：画像リサイズステップを有効にする（"petites"サブフォルダにウェブ用バージョンを作成）
- `-x, --numbered`：クリップボードの内容を使用して番号付きファイルの整理を有効にする
- `-m, --max-pixels`：リサイズされた画像の最大サイズ（ピクセル単位、デフォルト：2000）
- `-q, --quality`：リサイズされた画像のJPEG品質（70-100、デフォルト：80）
- `-v, --verbose`：詳細レベル：0=静か、1=要約、2=詳細（デフォルト：0）
- `-w, --overwrite`：移動またはリサイズ時に既存のファイルを上書きする
- `-c, --current-dir`：リサイズ時に現在のディレクトリ内の画像も含める

<a id="csv_transformer_jp"></a>
#### 4. `csv_transformer.py` - CSV変換ユーティリティ

このスクリプトは、データ処理ワークフローのための包括的なCSV変換機能を提供します。

**機能：**
- 列の選択、名前変更、並べ替え
- 条件に基づく行のフィルタリング
- カスタム関数によるデータ変換
- 集計とグループ化操作
- 統計分析と要約の生成
- 複数の入出力エンコーディング形式をサポート
- 複数のCSVファイルのバッチ処理

**使用法：**
```bash
python csv_transformer.py --input 入力.csv --output 変換済.csv [オプション]
```

**引数：**
- `--input`：入力CSVファイルへのパス
- `--output`：変換されたCSVファイルを保存するパス
- `--select`：特定の列を選択（カンマ区切り）
- `--rename`：列の名前を変更（形式：旧名:新名,旧名2:新名2）
- `--filter`：Python式を使用して行をフィルタリング
- `--transform`：列に変換を適用
- `--encoding`：入力/出力エンコーディング（デフォルト：utf-8）
- `--delimiter`：CSV区切り文字（デフォルト：,）
- `--group-by`：指定された列でデータをグループ化
- `--aggregate`：グループに適用する集計関数

### 将来の計画
今後、他のPythonユーティリティスクリプトがこのリポジトリに追加される予定で、それぞれが特定のタスクを効率的に解決することに焦点を当てています。

[トップに戻る](#python-utility-scripts--scripts-utilitaires-python--python-ユーティリティスクリプト--python-实用脚本--python-實用腳本)

---

<a id="chinese-simplified-details"></a>
## 简体中文详情

### 项目概述
本仓库包含一系列小型Python实用脚本，旨在自动化常见任务并解决特定问题。每个脚本都是独立的，专注于单一功能，使其易于使用和修改。

### 当前脚本

<a id="eliminate_dups_zh_cn"></a>
#### 1. `eliminate_dups_in_csv.py` - CSV重复项删除器

此脚本处理CSV文件以识别并删除重复条目，将它们保存到单独的文件中以供审查。

**功能：**
- 识别并删除CSV文件中的重复条目
- 适用于任何CSV文件，无论其内容或列数
- 创建不含重复项的干净输出文件
- 将已识别的重复项保存到单独的文件中
- 提供全面的操作摘要
- 可自定义编码、分隔符和表格显示格式

**使用方法：**
```bash
python eliminate_dups_in_csv.py 输入文件.csv 输出文件.csv 重复项文件.csv [选项]
```

**参数：**
- `输入文件`：输入CSV文件的路径
- `输出文件`：保存无重复项CSV文件的路径
- `重复项文件`：保存仅包含重复项的CSV文件的路径
- `--encoding`：CSV文件编码（默认：utf-8）
- `--delimiter`：CSV文件分隔符（默认：,）
- `--table-format`：摘要表格的格式（默认：fancy_grid）

<a id="extract_first_column_zh_cn"></a>
#### 2. `extract_first_column_of_csv.py` - CSV第一列提取器

此脚本从CSV文件中提取第一列内容，并将值作为逗号分隔的列表输出，每个值都由引号包围。

**功能：**
- 从任何CSV文件中提取第一列
- 以带引号的格式化逗号分隔列表形式输出值
- 优雅处理文件打开错误
- 简单而专注的功能

**使用方法：**
```bash
python extract_first_column_of_csv.py -i 输入文件.csv
```

**参数：**
- `-i, --input`：输入CSV文件的路径（必需）

<a id="scans_rename_zh_cn"></a>
#### 3. `scans_rename.py` - 日语时间戳文件整理工具
此脚本有助于管理和整理文件名中带有日语时间戳的扫描文件。它是为了应对Canon ImageFORMULA驱动程序（💩）的局限性而创建的，这个由无能的开发人员（🤬 🧠💀）编写的驱动程序只能在Windows下正常工作，且缺乏生成适当文件格式的能力。

**功能：**
- 将文件从日语时间戳格式（`YYYYMMDD-HH時MM分SS秒-XXX.jpg`）重命名为拉丁格式（`YYYYMMDD-HHhMMmSSs-XXX.jpg`）
- 根据时间戳前缀将文件整理到文件夹中
- 在"petites"子文件夹中创建适合网页使用的调整大小版本图像
- 使用剪贴板内容整理编号文件（例如："1.jpg"、"2.jpg"）
- 包含预览模式，可在不修改文件的情况下预览更改
- 可配置的详细级别，提供详细的操作反馈

**使用方法：**
```bash
python scans_rename.py --directory 路径 [--rename] [--organize] [--resize] \
  [--numbered] [--dry-run] [--verbose 级别]
```

**参数：**
- `-d, --directory`：包含要处理文件的目录（默认为当前目录）
- `-r, --dry-run`：模拟操作而不更改任何文件
- `-n, --rename`：启用文件重命名步骤（日语'時分秒'转为拉丁'hms'）
- `-o, --organize`：启用文件整理步骤（将文件移动到以时间戳命名的文件夹中）
- `-z, --resize`：启用图像调整大小步骤（在"petites"子文件夹中创建网页友好版本）
- `-x, --numbered`：启用使用剪贴板内容整理编号文件
- `-m, --max-pixels`：调整大小图像的最大尺寸（像素，默认：2000）
- `-q, --quality`：调整大小图像的JPEG质量（70-100，默认：80）
- `-v, --verbose`：详细级别：0=安静，1=摘要，2=详细（默认：0）
- `-w, --overwrite`：移动或调整大小时覆盖现有文件
- `-c, --current-dir`：在调整大小时包括当前目录中的图像

<a id="csv_transformer_zh_cn"></a>
#### 4. `csv_transformer.py` - CSV转换工具

此脚本为数据处理工作流提供全面的CSV转换功能。

**功能：**
- 列选择、重命名和重新排序
- 基于条件的行过滤
- 使用自定义函数进行数据转换
- 聚合和分组操作
- 统计分析和摘要生成
- 支持多种输入和输出编码格式
- 批处理多个CSV文件

**使用方法：**
```bash
python csv_transformer.py --input 输入.csv --output 转换后.csv [选项]
```

**参数：**
- `--input`：输入CSV文件的路径
- `--output`：保存转换后CSV文件的路径
- `--select`：选择特定列（逗号分隔）
- `--rename`：重命名列（格式：旧名称:新名称,旧名称2:新名称2）
- `--filter`：使用Python表达式过滤行
- `--transform`：对列应用转换
- `--encoding`：输入/输出编码（默认：utf-8）
- `--delimiter`：CSV分隔符（默认：,）
- `--group-by`：按指定列对数据进行分组
- `--aggregate`：应用于组的聚合函数

### 未来计划
随着时间的推移，更多的Python实用脚本将添加到此仓库中，每个脚本都专注于有效解决特定任务。

[返回顶部](#python-utility-scripts--scripts-utilitaires-python--python-ユーティリティスクリプト--python-实用脚本--python-實用腳本)

---

<a id="chinese-traditional-details"></a>
## 繁體中文詳情

### 專案概述
本倉庫包含一系列小型Python實用腳本，旨在自動化常見任務並解決特定問題。每個腳本都是獨立的，專注於單一功能，使其易於使用和修改。

### 當前腳本

<a id="eliminate_dups_zh_tw"></a>
#### 1. `eliminate_dups_in_csv.py` - CSV重複項刪除器

此腳本處理CSV檔案以識別並刪除重複條目，將它們保存到單獨的檔案中以供審查。

**功能：**
- 識別並刪除CSV檔案中的重複條目
- 適用於任何CSV檔案，無論其內容或列數
- 創建不含重複項的乾淨輸出檔案
- 將已識別的重複項保存到單獨的檔案中
- 提供全面的操作摘要
- 可自定義編碼、分隔符和表格顯示格式

**使用方法：**
```bash
python eliminate_dups_in_csv.py 輸入檔案.csv 輸出檔案.csv 重複項檔案.csv [選項]
```

**參數：**
- `輸入檔案`：輸入CSV檔案的路徑
- `輸出檔案`：保存無重複項CSV檔案的路徑
- `重複項檔案`：保存僅包含重複項的CSV檔案的路徑
- `--encoding`：CSV檔案編碼（默認：utf-8）
- `--delimiter`：CSV檔案分隔符（默認：,）
- `--table-format`：摘要表格的格式（默認：fancy_grid）

<a id="extract_first_column_zh_tw"></a>
#### 2. `extract_first_column_of_csv.py` - CSV第一列提取器

此腳本從CSV檔案中提取第一列內容，並將值作為逗號分隔的列表輸出，每個值都由引號包圍。

**功能：**
- 從任何CSV檔案中提取第一列
- 以帶引號的格式化逗號分隔列表形式輸出值
- 優雅處理檔案開啟錯誤
- 簡單而專注的功能

**使用方法：**
```bash
python extract_first_column_of_csv.py -i 輸入檔案.csv
```

**參數：**
- `-i, --input`：輸入CSV檔案的路徑（必需）

<a id="scans_rename_zh_tw"></a>
#### 3. `scans_rename.py` - 日語時間戳檔案整理工具
此腳本有助於管理和整理檔案名中帶有日語時間戳的掃描檔案。它是為了應對Canon ImageFORMULA驅動程序（💩）的局限性而創建的，這個由無能的開發人員（🤬 🧠💀）編寫的驅動程序只能在Windows下正常工作，且缺乏生成適當檔案格式的能力。

**功能：**
- 將檔案從日語時間戳格式（`YYYYMMDD-HH時MM分SS秒-XXX.jpg`）重新命名為拉丁格式（`YYYYMMDD-HHhMMmSSs-XXX.jpg`）
- 根據時間戳前綴將檔案整理到資料夾中
- 在"petites"子資料夾中創建適合網頁使用的調整大小版本圖像
- 使用剪貼簿內容整理編號檔案（例如："1.jpg"、"2.jpg"）
- 包含預覽模式，可在不修改檔案的情況下預覽更改
- 可配置的詳細級別，提供詳細的操作反饋

**使用方法：**
```bash
python scans_rename.py --directory 路徑 [--rename] [--organize] [--resize] \
  [--numbered] [--dry-run] [--verbose 級別]
```

**參數：**
- `-d, --directory`：包含要處理檔案的目錄（默認為當前目錄）
- `-r, --dry-run`：模擬操作而不更改任何檔案
- `-n, --rename`：啟用檔案重命名步驟（日語'時分秒'轉為拉丁'hms'）
- `-o, --organize`：啟用檔案整理步驟（將檔案移動到以時間戳命名的資料夾中）
- `-z, --resize`：啟用圖像調整大小步驟（在"petites"子資料夾中創建網頁友好版本）
- `-x, --numbered`：啟用使用剪貼簿內容整理編號檔案
- `-m, --max-pixels`：調整大小圖像的最大尺寸（像素，默認：2000）
- `-q, --quality`：調整大小圖像的JPEG質量（70-100，默認：80）
- `-v, --verbose`：詳細級別：0=安靜，1=摘要，2=詳細（默認：0）
- `-w, --overwrite`：移動或調整大小時覆蓋現有檔案
- `-c, --current-dir`：在調整大小時包括當前目錄中的圖像

<a id="csv_transformer_zh_tw"></a>
#### 4. `csv_transformer.py` - CSV轉換工具

此腳本為數據處理工作流提供全面的CSV轉換功能。

**功能：**
- 列選擇、重命名和重新排序
- 基於條件的行過濾
- 使用自定義函數進行數據轉換
- 聚合和分組操作
- 統計分析和摘要生成
- 支持多種輸入和輸出編碼格式
- 批處理多個CSV檔案

**使用方法：**
```bash
python csv_transformer.py --input 輸入.csv --output 轉換後.csv [選項]
```

**參數：**
- `--input`：輸入CSV檔案的路徑
- `--output`：保存轉換後CSV檔案的路徑
- `--select`：選擇特定列（逗號分隔）
- `--rename`：重命名列（格式：舊名稱:新名稱,舊名稱2:新名稱2）
- `--filter`：使用Python表達式過濾行
- `--transform`：對列應用轉換
- `--encoding`：輸入/輸出編碼（默認：utf-8）
- `--delimiter`：CSV分隔符（默認：,）
- `--group-by`：按指定列對數據進行分組
- `--aggregate`：應用於組的聚合函數

### 未來計劃
隨著時間的推移，更多的Python實用腳本將添加到此倉庫中，每個腳本都專注於有效解決特定任務。

[返回頂部](#python-utility-scripts--scripts-utilitaires-python--python-ユーティリティスクリプト--python-实用脚本--python-實用腳本)