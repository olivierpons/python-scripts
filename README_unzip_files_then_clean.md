# unzip_files_then_clean.py

## English

### Advanced ZIP Extraction and Directory Reorganization Tool

This script performs three main operations with comprehensive logging and statistics:

1. Extracts all ZIP files in a directory into corresponding subdirectories
2. Removes Apple system files (.DS_Store, .__MACOSX folders, etc.)
3. Reorganizes directories by moving single-child directories up one level

**Features:**

- Three verbosity levels (0=silent, 1=normal, 2=verbose)
- Centralized output through OperationStats class
- Comprehensive statistics collection
- Modern Python typing with pipe syntax
- Configurable confirmation prompts
- Detailed progress logging
- Beautiful tabular output using 'rich' library (with fallbacks to 'tabulate'
  or basic formatting)
- Extensive error handling and recovery
- File locking to prevent concurrent modifications
- Path safety checks for network paths and long filenames

**Example usage:**

```bash
# Default verbose mode (shows all operations)
$ python unzip_files_then_clean.py /path/to/directory

# Clean only mode with normal verbosity
$ python unzip_files_then_clean.py /path/to/directory --clean-only -v1

# Silent mode (only errors)
$ python unzip_files_then_clean.py /path/to/directory -v0

# No confirmation prompts with normal verbosity
$ python unzip_files_then_clean.py /path/to/directory --no-confirm -v1
```

**Arguments:**

- `-d`, `--directory`: Directory containing files to process
- `-c`, `--clean-only`: Only clean system files without extracting or
  reorganizing
- `-n`, `--no-confirm`: Skip all confirmation prompts
- `-v`, `--verbosity`: Verbosity level (0=silent, 1=normal, 2=verbose)
- `--max-size`: Maximum ZIP file size in bytes (default: 10GB)
- `--no-color`: Disable colored output

## Français

### Outil Avancé d'Extraction ZIP et de Réorganisation de Répertoires

Ce script effectue trois opérations principales avec une journalisation et des
statistiques complètes :

1. Extrait tous les fichiers ZIP d'un répertoire vers des sous-répertoires
   correspondants
2. Supprime les fichiers système Apple (.DS_Store, dossiers .__MACOSX, etc.)
3. Réorganise la structure des répertoires en remontant d'un niveau les
   répertoires à enfant unique

**Fonctionnalités :**

- Trois niveaux de verbosité (0=silencieux, 1=normal, 2=verbeux)
- Sortie centralisée via la classe OperationStats
- Collecte complète de statistiques
- Typages Python modernes avec syntaxe pipe
- Demandes de confirmation configurables
- Journalisation détaillée des progrès
- Affichage tabulaire élégant utilisant la bibliothèque 'rich' (avec repli sur
  'tabulate' ou un formatage basique)
- Gestion et récupération d'erreurs extensives
- Verrouillage de fichiers pour empêcher les modifications simultanées
- Vérifications de sécurité pour les chemins réseau et les noms de fichiers longs

**Exemples d'utilisation :**

```bash
# Mode verbeux par défaut (affiche toutes les opérations)
$ python unzip_files_then_clean.py /chemin/vers/repertoire

# Mode nettoyage uniquement avec verbosité normale
$ python unzip_files_then_clean.py /chemin/vers/repertoire --clean-only -v1

# Mode silencieux (seulement les erreurs)
$ python unzip_files_then_clean.py /chemin/vers/repertoire -v0

# Sans demandes de confirmation avec verbosité normale
$ python unzip_files_then_clean.py /chemin/vers/repertoire --no-confirm -v1
```

**Arguments :**

- `-d`, `--directory` : Répertoire contenant les fichiers à traiter
- `-c`, `--clean-only` : Nettoyer uniquement les fichiers système sans extraire
  ni réorganiser
- `-n`, `--no-confirm` : Ignorer toutes les demandes de confirmation
- `-v`, `--verbosity` : Niveau de verbosité (0=silencieux, 1=normal, 2=verbeux)
- `--max-size` : Taille maximale des fichiers ZIP en octets (par défaut : 10Go)
- `--no-color` : Désactiver la sortie colorée

## 日本語

### 高度なZIP抽出とディレクトリ再編成ツール

このスクリプトは、包括的なログ記録と統計を備えた3つの主要な操作を実行します：

1. ディレクトリ内のすべてのZIPファイルを対応するサブディレクトリに抽出
2. Appleシステムファイル（.DS_Store、.__MACOSXフォルダなど）を削除
3. 単一の子ディレクトリを持つディレクトリ構造を上の階層に移動して再編成

**機能：**

- 3つの詳細レベル（0=無音、1=通常、2=詳細）
- OperationStatsクラスを通じた一元化された出力
- 包括的な統計収集
- パイプ構文を使用した現代的なPythonタイピング
- 設定可能な確認プロンプト
- 詳細な進行ログ
- 'rich'ライブラリを使用した美しい表形式の出力（'tabulate'または基本的な形式
  へのフォールバック付き）
- 広範なエラー処理と回復
- 同時変更を防止するためのファイルロック
- ネットワークパスや長いファイル名のためのパス安全性チェック

**使用例：**

```bash
# デフォルトの詳細モード（すべての操作を表示）
$ python unzip_files_then_clean.py /path/to/directory

# 通常の詳細度でのクリーニングのみモード
$ python unzip_files_then_clean.py /path/to/directory --clean-only -v1

# サイレントモード（エラーのみ）
$ python unzip_files_then_clean.py /path/to/directory -v0

# 通常の詳細度での確認プロンプトなし
$ python unzip_files_then_clean.py /path/to/directory --no-confirm -v1
```

**引数：**

- `-d`, `--directory`：処理するファイルを含むディレクトリ
- `-c`, `--clean-only`：抽出や再編成なしでシステムファイルのみを清掃
- `-n`, `--no-confirm`：すべての確認プロンプトをスキップ
- `-v`, `--verbosity`：詳細レベル（0=無音、1=通常、2=詳細）
- `--max-size`：ZIPファイルの最大サイズ（バイト単位、デフォルト：10GB）
- `--no-color`：カラー出力を無効にする

## 简体中文

### 高级ZIP提取和目录重组工具

此脚本通过全面的日志记录和统计执行三项主要操作：

1. 将目录中的所有ZIP文件提取到相应的子目录中
2. 删除Apple系统文件（.DS_Store、.__MACOSX文件夹等）
3. 通过将单一子目录上移一级来重组目录结构

**功能：**

- 三个详细级别（0=静默，1=普通，2=详细）
- 通过OperationStats类实现集中化输出
- 全面的统计数据收集
- 具有管道语法的现代Python类型提示
- 可配置的确认提示
- 详细的进度日志
- 使用'rich'库的美观表格输出（后备为'tabulate'或基本格式）
- 广泛的错误处理和恢复
- 文件锁定以防止并发修改
- 网络路径和长文件名的路径安全检查

**使用示例：**

```bash
# 默认详细模式（显示所有操作）
$ python unzip_files_then_clean.py /path/to/directory

# 普通详细度的仅清理模式
$ python unzip_files_then_clean.py /path/to/directory --clean-only -v1

# 静默模式（仅显示错误）
$ python unzip_files_then_clean.py /path/to/directory -v0

# 普通详细度的无确认提示
$ python unzip_files_then_clean.py /path/to/directory --no-confirm -v1
```

**参数：**

- `-d`, `--directory`：包含要处理文件的目录
- `-c`, `--clean-only`：仅清理系统文件，不进行提取或重组
- `-n`, `--no-confirm`：跳过所有确认提示
- `-v`, `--verbosity`：详细级别（0=静默，1=普通，2=详细）
- `--max-size`：ZIP文件的最大大小（字节，默认：10GB）
- `--no-color`：禁用彩色输出

## Español

### Herramienta Avanzada de Extracción ZIP y Reorganización de Directorios

Este script realiza tres operaciones principales con registro y estadísticas
completas:

1. Extrae todos los archivos ZIP en un directorio a subdirectorios correspondientes
2. Elimina archivos del sistema Apple (.DS_Store, carpetas .__MACOSX, etc.)
3. Reorganiza directorios moviendo directorios de hijo único un nivel hacia arriba

**Características:**

- Tres niveles de verbosidad (0=silencioso, 1=normal, 2=detallado)
- Salida centralizada a través de la clase OperationStats
- Recopilación completa de estadísticas
- Tipado moderno de Python con sintaxis de pipe
- Mensajes de confirmación configurables
- Registro detallado del progreso
- Hermosa salida tabular usando la biblioteca 'rich' (con alternativas a
  'tabulate' o formato básico)
- Manejo y recuperación extensiva de errores
- Bloqueo de archivos para prevenir modificaciones concurrentes
- Comprobaciones de seguridad para rutas de red y nombres de archivo largos

**Ejemplos de uso:**

```bash
# Modo detallado predeterminado (muestra todas las operaciones)
$ python unzip_files_then_clean.py /ruta/al/directorio

# Modo solo limpieza con verbosidad normal
$ python unzip_files_then_clean.py /ruta/al/directorio --clean-only -v1

# Modo silencioso (solo errores)
$ python unzip_files_then_clean.py /ruta/al/directorio -v0

# Sin mensajes de confirmación con verbosidad normal
$ python unzip_files_then_clean.py /ruta/al/directorio --no-confirm -v1
```

**Argumentos:**

- `-d`, `--directory`: Directorio que contiene los archivos a procesar
- `-c`, `--clean-only`: Solo limpiar archivos del sistema sin extraer ni
  reorganizar
- `-n`, `--no-confirm`: Omitir todos los mensajes de confirmación
- `-v`, `--verbosity`: Nivel de verbosidad (0=silencioso, 1=normal, 2=detallado)
- `--max-size`: Tamaño máximo de archivo ZIP en bytes (predeterminado: 10GB)
- `--no-color`: Desactivar salida coloreada

## Italiano

### Strumento Avanzato di Estrazione ZIP e Riorganizzazione delle Directory

Questo script esegue tre operazioni principali con registrazione e statistiche
complete:

1. Estrae tutti i file ZIP in una directory nelle sottodirectory corrispondenti
2. Rimuove i file di sistema Apple (.DS_Store, cartelle .__MACOSX, ecc.)
3. Riorganizza le directory spostando le directory con un solo figlio un livello
   più in alto

**Funzionalità:**

- Tre livelli di verbosità (0=silenzioso, 1=normale, 2=dettagliato)
- Output centralizzato attraverso la classe OperationStats
- Raccolta completa di statistiche
- Tipizzazione Python moderna con sintassi pipe
- Richieste di conferma configurabili
- Registrazione dettagliata dei progressi
- Output tabulare elegante utilizzando la libreria 'rich' (con fallback a
  'tabulate' o formattazione base)
- Gestione e recupero estensivo degli errori
- Blocco dei file per prevenire modifiche concorrenti
- Controlli di sicurezza per percorsi di rete e nomi di file lunghi

**Esempi di utilizzo:**

```bash
# Modalità dettagliata predefinita (mostra tutte le operazioni)
$ python unzip_files_then_clean.py /percorso/alla/directory

# Modalità solo pulizia con verbosità normale
$ python unzip_files_then_clean.py /percorso/alla/directory --clean-only -v1

# Modalità silenziosa (solo errori)
$ python unzip_files_then_clean.py /percorso/alla/directory -v0

# Nessuna richiesta di conferma con verbosità normale
$ python unzip_files_then_clean.py /percorso/alla/directory --no-confirm -v1
```

**Argomenti:**

- `-d`, `--directory`: Directory contenente i file da elaborare
- `-c`, `--clean-only`: Pulisci solo i file di sistema senza estrarre o
  riorganizzare
- `-n`, `--no-confirm`: Salta tutte le richieste di conferma
- `-v`, `--verbosity`: Livello di verbosità (0=silenzioso, 1=normale,
  2=dettagliato)
- `--max-size`: Dimensione massima del file ZIP in byte (predefinito: 10GB)
- `--no-color`: Disabilita l'output colorato

## Deutsch

### Fortgeschrittenes ZIP-Extraktions- und Verzeichnis-Reorganisationstool

Dieses Skript führt drei Hauptoperationen mit umfassender Protokollierung und
Statistik durch:

1. Extrahiert alle ZIP-Dateien in einem Verzeichnis in entsprechende
   Unterverzeichnisse
2. Entfernt Apple-Systemdateien (.DS_Store, .__MACOSX-Ordner usw.)
3. Reorganisiert Verzeichnisse, indem Verzeichnisse mit einem einzelnen Kind eine
   Ebene nach oben verschoben werden

**Funktionen:**

- Drei Ausführlichkeitsstufen (0=stumm, 1=normal, 2=ausführlich)
- Zentralisierte Ausgabe durch die OperationStats-Klasse
- Umfassende Statistikerfassung
- Moderne Python-Typisierung mit Pipe-Syntax
- Konfigurierbare Bestätigungsaufforderungen
- Detaillierte Fortschrittsprotokollierung
- Schöne tabellarische Ausgabe mit der 'rich'-Bibliothek (mit Fallbacks zu
  'tabulate' oder Basisformatierung)
- Umfangreiche Fehlerbehandlung und -wiederherstellung
- Dateisperrung zur Verhinderung gleichzeitiger Änderungen
- Sicherheitsprüfungen für Netzwerkpfade und lange Dateinamen

**Verwendungsbeispiele:**

```bash
# Standardmäßiger ausführlicher Modus (zeigt alle Operationen)
$ python unzip_files_then_clean.py /pfad/zum/verzeichnis

# Nur-Bereinigungsmodus mit normaler Ausführlichkeit
$ python unzip_files_then_clean.py /pfad/zum/verzeichnis --clean-only -v1

# Stummer Modus (nur Fehler)
$ python unzip_files_then_clean.py /pfad/zum/verzeichnis -v0

# Keine Bestätigungsaufforderungen mit normaler Ausführlichkeit
$ python unzip_files_then_clean.py /pfad/zum/verzeichnis --no-confirm -v1
```

**Argumente:**

- `-d`, `--directory`: Verzeichnis mit zu verarbeitenden Dateien
- `-c`, `--clean-only`: Nur Systemdateien bereinigen ohne Extraktion oder
  Reorganisation
- `-n`, `--no-confirm`: Alle Bestätigungsaufforderungen überspringen
- `-v`, `--verbosity`: Ausführlichkeitsstufe (0=stumm, 1=normal, 2=ausführlich)
- `--max-size`: Maximale ZIP-Dateigröße in Bytes (Standard: 10GB)
- `--no-color`: Farbige Ausgabe deaktivieren