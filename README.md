# Python Utility Scripts / Scripts Utilitaires Python / Python ユーティリティスクリプト / Python 实用脚本 / Python 實用腳本

## Quick Overview / Aperçu Rapide / 概要 / 概述

### English

This repository contains a collection of small Python utility scripts designed to automate common tasks and solve
specific problems. Currently available:

- [**scans_rename.py**](#scans_rename_en): Renames and organizes files with Japanese timestamps in their filenames.

[More details below](#english-details)

### Français

Ce dépôt contient une collection de petits scripts utilitaires Python conçus pour automatiser des tâches courantes et 
résoudre des problèmes spécifiques. Actuellement disponible :

- [**scans_rename.py**](#scans_rename_fr) : Renomme et organise les fichiers avec des horodatages japonais dans leurs noms.

[Plus de détails ci-dessous](#french-details)

### 日本語

このリポジトリには、一般的なタスクを自動化し、特定の問題を解決するために設計された小さなPythonユーティリティスクリプトのコレクションが含まれています。現在利用可能：

- [**scans_rename.py**](#scans_rename_jp)：ファイル名の日本語タイムスタンプを持つファイルの名前変更と整理を行います。

[詳細は以下をご覧ください](#japanese-details)

### 简体中文

本仓库包含一系列小型Python实用脚本，旨在自动化常见任务并解决特定问题。目前可用：

- [**scans_rename.py**](#scans_rename_zh_cn)：重命名并整理文件名中带有日语时间戳的文件。

[更多详情见下文](#chinese-simplified-details)

### 繁體中文

本倉庫包含一系列小型Python實用腳本，旨在自動化常見任務並解決特定問題。目前可用：

- [**scans_rename.py**](#scans_rename_zh_tw)：重新命名並整理檔案名中帶有日語時間戳的檔案。

[更多詳情見下文](#chinese-traditional-details)

---

<a id="english-details"></a>
## English Details

### Project Overview

This repository contains a collection of small Python utility scripts designed to automate common tasks and solve
specific problems. Each script is self-contained and focuses on a single functionality, making them easy to use and
modify.

### Current Scripts

<a id="scans_rename_en"></a>
#### 1. `scans_rename.py` - Japanese Timestamp File Organizer

This script helps manage and organize scanned files with Japanese timestamps in their filenames. It was created out
of necessity to deal with the... limitations of the 💩 Canon ImageFORMULA driver written by 🤬 🧠💀 developers that
only works properly on Windows and lacks the ability to generate proper file formats.

**Features:**
- Renames files from Japanese timestamp format (`YYYYMMDD-HH時MM分SS秒-XXX.jpg`) to Latin format (`YYYYMMDD-HHhMMmSSs-XXX.jpg`)
- Organizes files into folders based on their timestamp prefixes
- Includes a dry-run mode to preview changes without modifying files
- Configurable verbosity levels for detailed operation feedback

**Usage:**
```bash
python scans_rename.py --directory PATH [--rename] [--organize] [--dry-run] [--verbose LEVEL]
```

**Arguments:**
- `-d, --directory`: Directory containing files to process (defaults to current directory)
- `-r, --dry-run`: Simulate operations without changing any files
- `-n, --rename`: Enable the file renaming step (Japanese '時分秒' to Latin 'hms')
- `-o, --organize`: Enable the file organization step (move files into timestamp-named folders)
- `-v, --verbose`: Verbosity level: 0=quiet, 1=summary, 2=details (default: 0)

### Future Plans

More Python utility scripts will be added to this repository over time, each focused on solving specific tasks 
efficiently.

[Back to top](#python-utility-scripts--scripts-utilitaires-python--python-ユーティリティスクリプト--python-实用脚本--python-實用腳本)

---

<a id="french-details"></a>
## Détails en Français

### Aperçu du Projet

Ce dépôt contient une collection de petits scripts utilitaires Python conçus pour automatiser des tâches courantes 
et résoudre des problèmes spécifiques. Chaque script est autonome et se concentre sur une fonctionnalité unique, 
ce qui les rend faciles à utiliser et à modifier.

### Scripts Actuels

<a id="scans_rename_fr"></a>
#### 1. `scans_rename.py` - Organisateur de Fichiers avec Horodatage Japonais

Ce script aide à gérer et organiser les fichiers numérisés avec des horodatages japonais dans leurs noms de fichier. 
Il a été créé par nécessité pour faire face aux... limitations du pilote 💩 Canon ImageFORMULA écrit par des 
🤬 🧠💀 de développeurs, ne fonctionne correctement que sous Windows et n'a pas la possibilité de générer des 
formats de fichiers appropriés.

**Fonctionnalités :**
- Renomme les fichiers du format d'horodatage japonais (`YYYYMMDD-HH時MM分SS秒-XXX.jpg`) au format 
  latin (`YYYYMMDD-HHhMMmSSs-XXX.jpg`)
- Organise les fichiers dans des dossiers basés sur leurs préfixes d'horodatage
- Inclut un mode simulation pour prévisualiser les changements sans modifier les fichiers
- Niveaux de verbosité configurables pour un retour détaillé des opérations

**Utilisation :**
```bash
python scans_rename.py --directory CHEMIN [--rename] [--organize] [--dry-run] [--verbose NIVEAU]
```

**Arguments :**
- `-d, --directory` : Répertoire contenant les fichiers à traiter (par défaut : répertoire courant)
- `-r, --dry-run` : Simuler les opérations sans changer aucun fichier
- `-n, --rename` : Activer l'étape de renommage des fichiers (japonais '時分秒' vers latin 'hms')
- `-o, --organize` : Activer l'étape d'organisation des fichiers (déplacer les fichiers dans des dossiers nommés selon l'horodatage)
- `-v, --verbose` : Niveau de verbosité : 0=silencieux, 1=résumé, 2=détails (par défaut : 0)

### Plans Futurs

D'autres scripts utilitaires Python seront ajoutés à ce dépôt au fil du temps, chacun se concentrant sur la résolution efficace de tâches spécifiques.

[Retour en haut](#python-utility-scripts--scripts-utilitaires-python--python-ユーティリティスクリプト--python-实用脚本--python-實用腳本)

---

<a id="japanese-details"></a>
## 日本語の詳細

### プロジェクト概要

このリポジトリには、一般的なタスクを自動化し、特定の問題を解決するために設計された小さなPythonユーティリティスクリプトのコレクションが含まれています。各スクリプトは独立しており、単一の機能に焦点を当てているため、使用や修正が容易です。

### 現在のスクリプト

<a id="scans_rename_jp"></a>
#### 1. `scans_rename.py` - 日本語タイムスタンプファイル整理ツール

このスクリプトは、ファイル名に日本語のタイムスタンプが付いたスキャンファイルの管理と整理を支援します。このスクリプトは、Canon ImageFORMULAドライバー（💩）の限界に対処するために作成されました。このドライバーは能力のない開発者（🤬 🧠💀）によって作られ、Windowsでしか正常に動作せず、適切なファイル形式を生成する機能が欠けています。

**機能：**
- ファイル名を日本語タイムスタンプ形式（`YYYYMMDD-HH時MM分SS秒-XXX.jpg`）からラテン形式（`YYYYMMDD-HHhMMmSSs-XXX.jpg`）に変更
- タイムスタンプのプレフィックスに基づいてファイルをフォルダに整理
- ファイルを変更せずに変更をプレビューするドライランモードを含む
- 詳細な操作フィードバックのための設定可能な詳細レベル

**使用法：**
```bash
python scans_rename.py --directory パス [--rename] [--organize] [--dry-run] [--verbose レベル]
```

**引数：**
- `-d, --directory`：処理するファイルを含むディレクトリ（デフォルトは現在のディレクトリ）
- `-r, --dry-run`：ファイルを変更せずに操作をシミュレート
- `-n, --rename`：ファイル名変更ステップを有効にする（日本語の'時分秒'をラテン文字の'hms'に）
- `-o, --organize`：ファイル整理ステップを有効にする（タイムスタンプ名のフォルダにファイルを移動）
- `-v, --verbose`：詳細レベル：0=静か、1=要約、2=詳細（デフォルト：0）

### 将来の計画

今後、他のPythonユーティリティスクリプトがこのリポジトリに追加される予定で、それぞれが特定のタスクを効率的に解決することに焦点を当てています。

[トップに戻る](#python-utility-scripts--scripts-utilitaires-python--python-ユーティリティスクリプト--python-实用脚本--python-實用腳本)

---

<a id="chinese-simplified-details"></a>
## 简体中文详情

### 项目概述

本仓库包含一系列小型Python实用脚本，旨在自动化常见任务并解决特定问题。每个脚本都是独立的，专注于单一功能，使其易于使用和修改。

### 当前脚本

<a id="scans_rename_zh_cn"></a>
#### 1. `scans_rename.py` - 日语时间戳文件整理工具

此脚本有助于管理和整理文件名中带有日语时间戳的扫描文件。它是为了应对Canon ImageFORMULA驱动程序（💩）的局限性而创建的，这个由无能的开发人员（🤬 🧠💀）编写的驱动程序只能在Windows下正常工作，且缺乏生成适当文件格式的能力。

**功能：**
- 将文件从日语时间戳格式（`YYYYMMDD-HH時MM分SS秒-XXX.jpg`）重命名为拉丁格式（`YYYYMMDD-HHhMMmSSs-XXX.jpg`）
- 根据时间戳前缀将文件整理到文件夹中
- 包含预览模式，可在不修改文件的情况下预览更改
- 可配置的详细级别，提供详细的操作反馈

**使用方法：**
```bash
python scans_rename.py --directory 路径 [--rename] [--organize] [--dry-run] [--verbose 级别]
```

**参数：**
- `-d, --directory`：包含要处理文件的目录（默认为当前目录）
- `-r, --dry-run`：模拟操作而不更改任何文件
- `-n, --rename`：启用文件重命名步骤（日语'時分秒'转为拉丁'hms'）
- `-o, --organize`：启用文件整理步骤（将文件移动到以时间戳命名的文件夹中）
- `-v, --verbose`：详细级别：0=安静，1=摘要，2=详细（默认：0）

### 未来计划

随着时间的推移，更多的Python实用脚本将添加到此仓库中，每个脚本都专注于有效解决特定任务。

[返回顶部](#python-utility-scripts--scripts-utilitaires-python--python-ユーティリティスクリプト--python-实用脚本--python-實用腳本)

---

<a id="chinese-traditional-details"></a>
## 繁體中文詳情

### 專案概述

本倉庫包含一系列小型Python實用腳本，旨在自動化常見任務並解決特定問題。每個腳本都是獨立的，專注於單一功能，使其易於使用和修改。

### 當前腳本

<a id="scans_rename_zh_tw"></a>
#### 1. `scans_rename.py` - 日語時間戳檔案整理工具

此腳本有助於管理和整理檔案名中帶有日語時間戳的掃描檔案。它是為了應對Canon ImageFORMULA驅動程序（💩）的局限性而創建的，這個由無能的開發人員（🤬 🧠💀）編寫的驅動程序只能在Windows下正常工作，且缺乏生成適當檔案格式的能力。

**功能：**
- 將檔案從日語時間戳格式（`YYYYMMDD-HH時MM分SS秒-XXX.jpg`）重新命名為拉丁格式（`YYYYMMDD-HHhMMmSSs-XXX.jpg`）
- 根據時間戳前綴將檔案整理到資料夾中
- 包含預覽模式，可在不修改檔案的情況下預覽更改
- 可配置的詳細級別，提供詳細的操作反饋

**使用方法：**
```bash
python scans_rename.py --directory 路徑 [--rename] [--organize] [--dry-run] [--verbose 級別]
```

**參數：**
- `-d, --directory`：包含要處理檔案的目錄（默認為當前目錄）
- `-r, --dry-run`：模擬操作而不更改任何檔案
- `-n, --rename`：啟用檔案重命名步驟（日語'時分秒'轉為拉丁'hms'）
- `-o, --organize`：啟用檔案整理步驟（將檔案移動到以時間戳命名的資料夾中）
- `-v, --verbose`：詳細級別：0=安靜，1=摘要，2=詳細（默認：0）

### 未來計劃

隨著時間的推移，更多的Python實用腳本將添加到此倉庫中，每個腳本都專注於有效解決特定任務。

[返回頂部](#python-utility-scripts--scripts-utilitaires-python--python-ユーティリティスクリプト--python-实用脚本--python-實用腳本)