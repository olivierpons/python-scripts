# unzip_files_then_clean.py

## English

### ZIP Extraction and Directory Reorganization Tool

This advanced script automates the process of extracting ZIP files and cleaning up directory structures for better organization.

**Features:**
- Extracts all ZIP files in a directory to corresponding subdirectories
- Removes Apple system files (.DS_Store, .__MACOSX folders, etc.)
- Reorganizes directories by moving single-child directories up one level
- Eliminates unnecessary nesting in file hierarchies
- Detailed progress logging with configurable verbosity
- Beautiful tabular output (with fallback to basic formatting)
- Comprehensive statistics collection
- Modern Python typing and dataclasses
- Configurable confirmation prompts for overwriting existing content

**Usage:**
```bash
python unzip_files_then_clean.py directory [options]
```

**Arguments:**
- `directory`: Path to the directory containing files to process
- `--clean-only`: Only clean system files without extracting or reorganizing
- `--no-confirm`: Skip all confirmation prompts
- `--verbose`, `-v`: Show detailed operation logs

## Français

### Outil d'Extraction ZIP et de Réorganisation de Répertoires

Ce script avancé automatise le processus d'extraction des fichiers ZIP et de nettoyage des structures de répertoires pour une meilleure organisation.

**Fonctionnalités :**
- Extrait tous les fichiers ZIP d'un répertoire vers des sous-répertoires correspondants
- Supprime les fichiers système Apple (.DS_Store, dossiers .__MACOSX, etc.)
- Réorganise la structure des répertoires en remontant d'un niveau les répertoires à enfant unique
- Élimine l'imbrication inutile dans les hiérarchies de fichiers
- Journalisation détaillée des progrès avec niveau de verbosité configurable
- Affichage tabulaire élégant (avec repli sur un formatage basique)
- Collecte complète de statistiques
- Typages Python modernes et dataclasses
- Demandes de confirmation configurables pour l'écrasement du contenu existant

**Utilisation :**
```bash
python unzip_files_then_clean.py repertoire [options]
```

**Arguments :**
- `repertoire` : Chemin vers le répertoire contenant les fichiers à traiter
- `--clean-only` : Nettoyer uniquement les fichiers système sans extraire ni réorganiser
- `--no-confirm` : Ignorer toutes les demandes de confirmation
- `--verbose`, `-v` : Afficher les journaux d'opération détaillés

## 日本語

### ZIP抽出とディレクトリ再編成ツール

このスクリプトは、ZIPファイルの抽出とディレクトリ構造のクリーンアップを自動化して、より良い整理を実現する高度なツールです。

**機能：**
- ディレクトリ内のすべてのZIPファイルを対応するサブディレクトリに抽出
- Appleシステムファイル（.DS_Store、.__MACOSXフォルダなど）を削除
- 単一の子ディレクトリを持つディレクトリ構造を上の階層に移動して再編成
- ファイル階層における不要な入れ子構造を排除
- 設定可能な詳細レベルでの詳細な進行ログ
- 美しい表形式の出力（基本的な形式へのフォールバック付き）
- 包括的な統計収集
- モダンなPythonの型付けとデータクラス
- 既存のコンテンツを上書きするための設定可能な確認プロンプト

**使用法：**
```bash
python unzip_files_then_clean.py ディレクトリ [オプション]
```

**引数：**
- `ディレクトリ`：処理するファイルを含むディレクトリへのパス
- `--clean-only`：抽出や再編成なしでシステムファイルのみをクリーンアップ
- `--no-confirm`：すべての確認プロンプトをスキップ
- `--verbose`, `-v`：詳細な操作ログを表示

## 简体中文

### ZIP提取和目录重组工具

此高级脚本自动化了ZIP文件提取和目录结构清理的过程，以实现更好的组织。

**功能：**
- 将目录中的所有ZIP文件提取到相应的子目录中
- 删除Apple系统文件（.DS_Store、.__MACOSX文件夹等）
- 通过将单一子目录上移一级来重组目录结构
- 消除文件层次结构中不必要的嵌套
- 提供可配置详细级别的详细进度日志
- 美观的表格输出（具有基本格式的后备方案）
- 全面的统计数据收集
- 现代Python类型提示和数据类
- 针对覆盖现有内容的可配置确认提示

**使用方法：**
```bash
python unzip_files_then_clean.py 目录 [选项]
```

**参数：**
- `目录`：包含要处理文件的目录路径
- `--clean-only`：仅清理系统文件，不进行提取或重组
- `--no-confirm`：跳过所有确认提示
- `--verbose`, `-v`：显示详细操作日志

## 繁體中文

### ZIP提取和目錄重組工具

此高級腳本自動化了ZIP檔案提取和目錄結構清理的過程，以實現更好的組織。

**功能：**
- 將目錄中的所有ZIP檔案提取到相應的子目錄中
- 刪除Apple系統檔案（.DS_Store、.__MACOSX資料夾等）
- 通過將單一子目錄上移一級來重組目錄結構
- 消除檔案層次結構中不必要的嵌套
- 提供可配置詳細級別的詳細進度日誌
- 美觀的表格輸出（具有基本格式的後備方案）
- 全面的統計數據收集
- 現代Python類型提示和數據類
- 針對覆蓋現有內容的可配置確認提示

**使用方法：**
```bash
python unzip_files_then_clean.py 目錄 [選項]
```

**參數：**
- `目錄`：包含要處理檔案的目錄路徑
- `--clean-only`：僅清理系統檔案，不進行提取或重組
- `--no-confirm`：跳過所有確認提示
- `--verbose`, `-v`：顯示詳細操作日誌
