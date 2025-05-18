# scans_rename.py

## English

### Japanese Timestamp File Organizer

This script helps manage and organize scanned files with Japanese timestamps in their filenames. It was created out of necessity to deal with the limitations of the Canon ImageFORMULA driver written by developers that only works properly on Windows and lacks the ability to generate proper file formats.

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

## Français

### Organisateur de Fichiers avec Horodatage Japonais

Ce script aide à gérer et organiser les fichiers numérisés avec des horodatages japonais dans leurs noms de fichier. Il a été créé par nécessité pour faire face aux limitations du pilote Canon ImageFORMULA écrit par des développeurs, qui ne fonctionne correctement que sous Windows et n'a pas la possibilité de générer des formats de fichiers appropriés.

**Fonctionnalités :**
- Renomme les fichiers du format d'horodatage japonais (`YYYYMMDD-HH時MM分SS秒-XXX.jpg`) au format latin (`YYYYMMDD-HHhMMmSSs-XXX.jpg`)
- Organise les fichiers dans des dossiers basés sur leurs préfixes d'horodatage
- Crée des versions redimensionnées adaptées au web dans des sous-dossiers "petites"
- Organise les fichiers numérotés (ex. "1.jpg", "2.jpg") en utilisant le contenu du presse-papiers pour nommer les dossiers
- Inclut un mode simulation pour prévisualiser les changements sans modifier les fichiers
- Niveaux de verbosité configurables pour un retour détaillé des opérations

**Utilisation :**
```bash
python scans_rename.py --directory CHEMIN [--rename] [--organize] [--resize] \
  [--numbered] [--dry-run] [--verbose NIVEAU]
```

**Arguments :**
- `-d, --directory` : Répertoire contenant les fichiers à traiter (par défaut : répertoire courant)
- `-r, --dry-run` : Simuler les opérations sans changer aucun fichier
- `-n, --rename` : Activer l'étape de renommage des fichiers (japonais '時分秒' vers latin 'hms')
- `-o, --organize` : Activer l'étape d'organisation des fichiers (déplacer les fichiers dans des dossiers nommés selon l'horodatage)
- `-z, --resize` : Activer l'étape de redimensionnement d'images (créer des versions adaptées au web dans des sous-dossiers "petites")
- `-x, --numbered` : Activer l'organisation des fichiers numérotés en utilisant le contenu du presse-papiers
- `-m, --max-pixels` : Taille maximale en pixels pour les images redimensionnées (par défaut : 2000)
- `-q, --quality` : Qualité JPEG pour les images redimensionnées (70-100, par défaut : 80)
- `-v, --verbose` : Niveau de verbosité : 0=silencieux, 1=résumé, 2=détails (par défaut : 0)
- `-w, --overwrite` : Écraser les fichiers existants lors du déplacement ou du redimensionnement
- `-c, --current-dir` : Inclure les images dans le répertoire courant lors du redimensionnement

## 日本語

### 日本語タイムスタンプファイル整理ツール

このスクリプトは、ファイル名に日本語のタイムスタンプが付いたスキャンファイルの管理と整理を支援します。このスクリプトは、Canon ImageFORMULAドライバーの限界に対処するために作成されました。このドライバーは開発者によって作られ、Windowsでしか正常に動作せず、適切なファイル形式を生成する機能が欠けています。

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

## 简体中文

### 日语时间戳文件整理工具

此脚本有助于管理和整理文件名中带有日语时间戳的扫描文件。它是为了应对Canon ImageFORMULA驱动程序的局限性而创建的，这个由开发人员编写的驱动程序只能在Windows下正常工作，且缺乏生成适当文件格式的能力。

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

## 繁體中文

### 日語時間戳檔案整理工具

此腳本有助於管理和整理檔案名中帶有日語時間戳的掃描檔案。它是為了應對Canon ImageFORMULA驅動程序的局限性而創建的，這個由開發人員編寫的驅動程序只能在Windows下正常工作，且缺乏生成適當檔案格式的能力。

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
