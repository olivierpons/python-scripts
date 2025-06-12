# eliminate_dups_in_csv.py

## English

### CSV Duplicate Remover

This script processes CSV files to identify and remove duplicate entries, saving
them into separate files for review.

**Features:**

- Identifies and removes duplicate entries from CSV files
- Works with any CSV file regardless of its content or number of columns
- Creates a clean output file without duplicates
- Saves identified duplicates to a separate file
- Provides a comprehensive summary of the operation
- Customizable encoding, delimiter, and table display format

**Usage:**

```bash
python eliminate_dups_in_csv.py input_file.csv output_file.csv \
    duplicates_file.csv [options]
```

**Arguments:**

- `input_file`: Path to the input CSV file
- `output_file`: Path to save the CSV file without duplicates
- `duplicates_file`: Path to save the CSV file containing only duplicates
- `--encoding`: CSV file encoding (default: utf-8)
- `--delimiter`: CSV file delimiter (default: ,)
- `--table-format`: Format for summary table (default: fancy_grid)

## Français

### Suppresseur de doublons CSV

Ce script traite les fichiers CSV pour identifier et supprimer les entrées
en double, en les enregistrant dans des fichiers séparés pour examen.

**Fonctionnalités :**

- Identifie et supprime les entrées en double des fichiers CSV
- Fonctionne avec n'importe quel fichier CSV, quel que soit son contenu ou son
  nombre de colonnes
- Crée un fichier de sortie propre sans doublons
- Enregistre les doublons identifiés dans un fichier séparé
- Fournit un résumé complet de l'opération
- Format d'encodage, délimiteur et affichage de tableau personnalisables

**Utilisation :**

```bash
python eliminate_dups_in_csv.py fichier_entree.csv fichier_sortie.csv \
    fichier_doublons.csv [options]
```

**Arguments :**

- `fichier_entree` : Chemin vers le fichier CSV d'entrée
- `fichier_sortie` : Chemin pour enregistrer le fichier CSV sans doublons
- `fichier_doublons` : Chemin pour enregistrer le fichier CSV contenant uniquement
  les doublons
- `--encoding` : Encodage du fichier CSV (par défaut : utf-8)
- `--delimiter` : Délimiteur du fichier CSV (par défaut : ,)
- `--table-format` : Format pour le tableau récapitulatif (par défaut : fancy_grid)

## 日本語

### CSV重複除去ツール

このスクリプトはCSVファイルを処理して重複エントリを特定し、削除して、
レビュー用に別のファイルに保存します。

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

## 简体中文

### CSV重复项删除器

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

## 繁體中文

### CSV重複項刪除器

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

## Español

### Eliminador de Duplicados CSV

Este script procesa archivos CSV para identificar y eliminar entradas duplicadas,
guardándolas en archivos separados para su revisión.

**Características:**

- Identifica y elimina entradas duplicadas de archivos CSV
- Funciona con cualquier archivo CSV independientemente de su contenido o número
  de columnas
- Crea un archivo de salida limpio sin duplicados
- Guarda los duplicados identificados en un archivo separado
- Proporciona un resumen completo de la operación
- Codificación, delimitador y formato de visualización de tabla personalizables

**Uso:**

```bash
python eliminate_dups_in_csv.py archivo_entrada.csv archivo_salida.csv \
    archivo_duplicados.csv [opciones]
```

**Argumentos:**

- `archivo_entrada`: Ruta al archivo CSV de entrada
- `archivo_salida`: Ruta para guardar el archivo CSV sin duplicados
- `archivo_duplicados`: Ruta para guardar el archivo CSV que contiene solo
  duplicados
- `--encoding`: Codificación del archivo CSV (predeterminado: utf-8)
- `--delimiter`: Delimitador del archivo CSV (predeterminado: ,)
- `--table-format`: Formato para la tabla de resumen (predeterminado: fancy_grid)

## Italiano

### Rimozione Duplicati CSV

Questo script elabora file CSV per identificare e rimuovere voci duplicate,
salvandole in file separati per la revisione.

**Funzionalità:**

- Identifica e rimuove voci duplicate dai file CSV
- Funziona con qualsiasi file CSV indipendentemente dal suo contenuto o numero di
  colonne
- Crea un file di output pulito senza duplicati
- Salva i duplicati identificati in un file separato
- Fornisce un riepilogo completo dell'operazione
- Codifica, delimitatore e formato di visualizzazione della tabella personalizzabili

**Utilizzo:**

```bash
python eliminate_dups_in_csv.py file_input.csv file_output.csv \
    file_duplicati.csv [opzioni]
```

**Argomenti:**

- `file_input`: Percorso del file CSV di input
- `file_output`: Percorso per salvare il file CSV senza duplicati
- `file_duplicati`: Percorso per salvare il file CSV contenente solo duplicati
- `--encoding`: Codifica del file CSV (predefinito: utf-8)
- `--delimiter`: Delimitatore del file CSV (predefinito: ,)
- `--table-format`: Formato per la tabella di riepilogo (predefinito: fancy_grid)

## Deutsch

### CSV-Duplikatentferner

Dieses Skript verarbeitet CSV-Dateien, um doppelte Einträge zu identifizieren
und zu entfernen, wobei diese zur Überprüfung in separaten Dateien gespeichert
werden.

**Funktionen:**

- Identifiziert und entfernt doppelte Einträge aus CSV-Dateien
- Funktioniert mit jeder CSV-Datei unabhängig von ihrem Inhalt oder ihrer
  Spaltenanzahl
- Erstellt eine bereinigte Ausgabedatei ohne Duplikate
- Speichert identifizierte Duplikate in einer separaten Datei
- Bietet eine umfassende Zusammenfassung der Operation
- Anpassbare Kodierung, Trennzeichen und Tabellenanzeigeformat

**Verwendung:**

```bash
python eliminate_dups_in_csv.py eingabedatei.csv ausgabedatei.csv \
    duplikate_datei.csv [optionen]
```

**Argumente:**

- `eingabedatei`: Pfad zur CSV-Eingabedatei
- `ausgabedatei`: Pfad zum Speichern der CSV-Datei ohne Duplikate
- `duplikate_datei`: Pfad zum Speichern der CSV-Datei, die nur Duplikate enthält
- `--encoding`: CSV-Dateikodierung (Standard: utf-8)
- `--delimiter`: CSV-Dateitrennzeichen (Standard: ,)
- `--table-format`: Format für die Zusammenfassungstabelle (Standard: fancy_grid)
