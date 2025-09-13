# Python Utility Scripts

(Scripts Utilitaires Python / Python ユーティリティスクリプト / Python 实用脚本 /
Scripts de Utilidad Python / Script di Utilità Python /
Python-Dienstprogrammskripte / Python 實用腳本)

## Quick Overview

(Aperçu Rapide / 概要 / 概述 / Vista Rápida / Panoramica / Kurzübersicht / 概述)

### English

This repository contains a collection of small Python utility scripts designed to
automate common tasks and solve specific problems. Each script is documented in
its own README file with detailed information:

- [**eliminate_dups_in_csv.py**](README_eliminate_dups_in_csv.md): Processes CSV
  files to remove duplicates and saves them separately.
- [**extract_first_column_of_csv.py**](README_extract_first_column_of_csv.md):
  Extracts the first column from a CSV file.
- [**pie_chart_generator.py**](README_pie_chart_generator.md): Generates a professional
  series of pie charts showing color progression from 0% to 100% with extensive
  customization options and modern Python 3.13+ features.
- [**scans_rename.py**](README_scans_rename.md): Renames and organizes files
  with Japanese timestamps in their filenames.
- [**sphere_texture_generator.py**](README_sphere_texture_generator.md): Generates seamless sphere textures optimized for Blender and Godot using equirectangular projection. Creates procedural textures (Earth-like, gas giant, marble) or converts existing images to sphere-ready formats with automatic pole distortion fixes.
- [**square_image_with_centered_cross_generator.py**](README_square_image_with_centered_cross_generator.md):
  Generates a square image with a centered cross, with customizable size and
  colors.
- [**svg_pattern_for_vase.py**](README_svg_pattern_for_vase.md): Generates a foldable SVG pattern for a vase with a triangular base.
- [**svg_to_bitmap_converter.py**](README_svg_to_bitmap_converter.md): Converts simple rectangle-based SVG files to bitmap formats (PNG, BMP, JPEG, etc.) with comprehensive error handling and logging.
- [**triangles.py**](README_triangles.md): Creates a PNG image with a double row of triangles, for use as a printable pattern.
- [**unzip_files_then_clean.py**](README_unzip_files_then_clean.md): Extracts all
  ZIP files in a directory and reorganizes folder structure.
- [**video_content_cutter.py**](README_video_content_cutter.md): Removes content from the beginning of a time-stamped file up to a specified MM:SS cutoff time.
- [**wordpress_scraper.py**](README_wordpress_scraper.md): Fetches a protected
  web page after authenticating with a complex login form (supports CSRF).

### Français

Ce dépôt contient une collection de petits scripts utilitaires Python conçus pour
automatiser des tâches courantes et résoudre des problèmes spécifiques. Chaque
script est documenté dans son propre fichier README avec des informations
détaillées :

- [**eliminate_dups_in_csv.py**](README_eliminate_dups_in_csv.md) : Traite les
  fichiers CSV pour supprimer les doublons et les enregistre séparément.
- [**extract_first_column_of_csv.py**](README_extract_first_column_of_csv.md) :
  Extrait la première colonne d'un fichier CSV.
- [**pie_chart_generator.py**](README_pie_chart_generator.md) : Génère une série
  professionnelle de camemberts montrant la progression des couleurs de 0% à 100%
  avec de nombreuses options de personnalisation et les fonctionnalités modernes de Python 3.13+.
- [**scans_rename.py**](README_scans_rename.md) : Renomme et organise les
  fichiers avec des horodatages japonais dans leurs noms.
- [**sphere_texture_generator.py**](README_sphere_texture_generator.md) : Génère des textures sphériques seamless optimisées pour Blender et Godot en utilisant la projection équirectangulaire. Crée des textures procédurales (terrestres, géantes gazeuses, marbre) ou convertit des images existantes en formats prêts pour les sphères avec correction automatique des distorsions polaires.
- [**square_image_with_centered_cross_generator.py**](README_square_image_with_centered_cross_generator.md):
  Génère une image carrée avec une croix centrée, avec une taille et des
  couleurs personnalisables.
- [**svg_pattern_for_vase.py**](README_svg_pattern_for_vase.md) : Génère un patron SVG pliable pour un vase à base triangulaire.
- [**svg_to_bitmap_converter.py**](README_svg_to_bitmap_converter.md) : Convertit des fichiers SVG simples (rectangles uniquement) vers des formats bitmap (PNG, BMP, JPEG, etc.) avec gestion d'erreurs complète et journalisation.
- [**triangles.py**](README_triangles.md) : Crée une image PNG avec une double rangée de triangles, à utiliser comme patron imprimable.
- [**unzip_files_then_clean.py**](README_unzip_files_then_clean.md) : Extrait
  tous les fichiers ZIP d'un répertoire et réorganise la structure des
  dossiers.
- [**video_content_cutter.py**](README_video_content_cutter.md) : Supprime le contenu du début d'un fichier horodaté jusqu'à un temps de coupe spécifié au format MM:SS.
- [**wordpress_scraper.py**](README_wordpress_scraper.md): Récupère une page web
  protégée après s'être authentifié via un formulaire de connexion complexe
  (supporte CSRF).

### 日本語

このリポジトリには、一般的なタスクを自動化し、特定の問題を解決するために設計された
小さなPythonユーティリティスクリプトのコレクションが含まれています。各スクリプトは
独自のREADMEファイルに詳細情報とともに文書化されています：

- [**eliminate_dups_in_csv.py**](README_eliminate_dups_in_csv.md)：CSVファイルを
  処理して重複を削除し、別々に保存します。
- [**extract_first_column_of_csv.py**](README_extract_first_column_of_csv.md)：
  CSVファイルの最初の列を抽出します。
- [**pie_chart_generator.py**](README_pie_chart_generator.md)：0%から100%までの
  色の進行を示すプロフェッショナルな円グラフシリーズを、豊富なカスタマイズオプションと
  Python 3.13+の最新機能で生成します。
- [**scans_rename.py**](README_scans_rename.md)：ファイル名の日本語タイムスタンプを
  持つファイルの名前変更と整理を行います。
- [**sphere_texture_generator.py**](README_sphere_texture_generator.md)：正距円筒図法を使用してBlenderとGodot用に最適化されたシームレスな球体テクスチャを生成します。手続き的テクスチャ（地球風、ガス惑星、大理石）を作成するか、既存の画像を球体対応フォーマットに自動極歪み修正付きで変換します。
- [**square_image_with_centered_cross_generator.py**](README_square_image_with_centered_cross_generator.md):
  中央に十字が描かれた正方形の画像を、カスタマイズ可能なサイズと色で生成します。
- [**svg_pattern_for_vase.py**](README_svg_pattern_for_vase.md): 三角形の底面を持つ折りたたみ可能な花瓶のSVGパターンを生成します。
- [**svg_to_bitmap_converter.py**](README_svg_to_bitmap_converter.md): シンプルな長方形ベースのSVGファイルをビットマップ形式（PNG、BMP、JPEGなど）に変換し、包括的なエラー処理とログ記録を提供します。
- [**triangles.py**](README_triangles.md): 印刷可能なパターンとして使用するために、二重の三角形の列を持つPNG画像を生成します。
- [**unzip_files_then_clean.py**](README_unzip_files_then_clean.md)：
  ディレクトリ内のすべてのZIPファイルを抽出し、フォルダ構造を再編成します。
- [**video_content_cutter.py**](README_video_content_cutter.md): タイムスタンプ付きファイルの先頭から指定されたMM:SS形式のカットオフ時間までのコンテンツを削除します。
- [**wordpress_scraper.py**](README_wordpress_scraper.md):
  複雑なログインフォーム（CSRF対応）で認証後、保護されたウェブページを取得します。

### 简体中文

本仓库包含一系列小型Python实用脚本，旨在自动化常见任务并解决特定问题。
每个脚本都在其自己的README文件中有详细说明：

- [**eliminate_dups_in_csv.py**](README_eliminate_dups_in_csv.md)：处理CSV文件以
  删除重复项并将其单独保存。
- [**extract_first_column_of_csv.py**](README_extract_first_column_of_csv.md)：
  从CSV文件中提取第一列。
- [**pie_chart_generator.py**](README_pie_chart_generator.md)：生成专业的饼图系列，
  显示从0%到100%的颜色进展，具有丰富的自定义选项和Python 3.13+的现代功能。
- [**scans_rename.py**](README_scans_rename.md)：重命名并整理文件名中带有日语
  时间戳的文件。
- [**sphere_texture_generator.py**](README_sphere_texture_generator.md)：使用等距圆柱投影生成为Blender和Godot优化的无缝球体纹理。创建程序化纹理（类地行星、气态巨行星、大理石）或将现有图像转换为具有自动极点畸变修正的球体就绪格式。
- [**square_image_with_centered_cross_generator.py**](README_square_image_with_centered_cross_generator.md):
  生成一个带有居中十字的正方形图像，尺寸和颜色可自定义。
- [**svg_pattern_for_vase.py**](README_svg_pattern_for_vase.md): 为三角形底座的可折叠花瓶生成SVG图案。
- [**svg_to_bitmap_converter.py**](README_svg_to_bitmap_converter.md): 将简单的基于矩形的SVG文件转换为位图格式（PNG、BMP、JPEG等），提供全面的错误处理和日志记录。
- [**triangles.py**](README_triangles.md): 创建一个带有双排三角形的PNG图像，用作可打印的图案。
- [**unzip_files_then_clean.py**](README_unzip_files_then_clean.md)：提取目录中
  的所有ZIP文件并重组文件夹结构。
- [**video_content_cutter.py**](README_video_content_cutter.md): 从带时间戳文件的开头删除内容，直到指定的MM:SS格式的截止时间。
- [**wordpress_scraper.py**](README_wordpress_scraper.md):
  在通过复杂的登录表单（支持CSRF）进行身份验证后，获取受保护的网页。

### 繁體中文

本倉庫包含一系列小型Python實用腳本，旨在自動化常見任務並解決特定問題。
每個腳本都在其自己的README文件中有詳細說明：

- [**eliminate_dups_in_csv.py**](README_eliminate_dups_in_csv.md)：處理CSV檔案以
  刪除重複項並將其單獨保存。
- [**extract_first_column_of_csv.py**](README_extract_first_column_of_csv.md)：
  從CSV檔案中提取第一列。
- [**pie_chart_generator.py**](README_pie_chart_generator.md)：生成專業的圓餅圖系列，
  顯示從0%到100%的顏色進展，具有豐富的自訂選項和Python 3.13+的現代功能。
- [**scans_rename.py**](README_scans_rename.md)：重新命名並整理檔案名中帶有
  日語時間戳的檔案。
- [**sphere_texture_generator.py**](README_sphere_texture_generator.md)：使用等距圓柱投影生成為Blender和Godot優化的無縫球體紋理。創建程序化紋理（類地行星、氣態巨行星、大理石）或將現有圖像轉換為具有自動極點畸變修正的球體就緒格式。
- [**square_image_with_centered_cross_generator.py**](README_square_image_with_centered_cross_generator.md):
  生成一個帶有居中十字的正方形圖像，尺寸和顏色可自訂。
- [**svg_pattern_for_vase.py**](README_svg_pattern_for_vase.md): 為三角形底座的可摺疊花瓶生成SVG圖案。
- [**svg_to_bitmap_converter.py**](README_svg_to_bitmap_converter.md): 將簡單的基於矩形的SVG檔案轉換為點陣圖格式（PNG、BMP、JPEG等），提供全面的錯誤處理和日誌記錄。
- [**triangles.py**](README_triangles.md): 創建一個帶有雙排三角形的PNG圖像，用作可打印的圖案。
- [**unzip_files_then_clean.py**](README_unzip_files_then_clean.md)：提取目錄中
  的所有ZIP檔案並重組資料夾結構。
- [**video_content_cutter.py**](README_video_content_cutter.md): 從帶時間戳檔案的開頭刪除內容，直到指定的MM:SS格式的截止時間。
- [**wordpress_scraper.py**](README_wordpress_scraper.md):
  在通過複雜的登錄表單（支援CSRF）進行身份驗證後，獲取受保護的網頁。

### Español

Este repositorio contiene una colección de pequeños scripts de utilidad en Python
diseñados para automatizar tareas comunes y resolver problemas específicos. Cada
script está documentado en su propio archivo README con información detallada:

- [**eliminate_dups_in_csv.py**](README_eliminate_dups_in_csv.md): Procesa
  archivos CSV para eliminar duplicados y los guarda por separado.
- [**extract_first_column_of_csv.py**](README_extract_first_column_of_csv.md):
  Extrae la primera columna de un archivo CSV.
- [**pie_chart_generator.py**](README_pie_chart_generator.md): Genera una serie
  profesional de gráficos circulares mostrando la progresión de colores del 0% al 100%
  con amplias opciones de personalización y características modernas de Python 3.13+.
- [**scans_rename.py**](README_scans_rename.md): Renombra y organiza archivos con
  marcas de tiempo japonesas en sus nombres.
- [**sphere_texture_generator.py**](README_sphere_texture_generator.md): Genera texturas esféricas sin costuras optimizadas para Blender y Godot usando proyección equirectangular. Crea texturas procedurales (similares a la Tierra, gigante gaseoso, mármol) o convierte imágenes existentes a formatos listos para esferas con corrección automática de distorsión en los polos.
- [**square_image_with_centered_cross_generator.py**](README_square_image_with_centered_cross_generator.md):
  Genera una imagen cuadrada con una cruz centrada, con tamaño y colores
  personalizables.
- [**svg_pattern_for_vase.py**](README_svg_pattern_for_vase.md): Genera un patrón SVG plegable para un jarrón con base triangular.
- [**svg_to_bitmap_converter.py**](README_svg_to_bitmap_converter.md): Convierte archivos SVG simples basados en rectángulos a formatos bitmap (PNG, BMP, JPEG, etc.) con manejo completo de errores y registro.
- [**triangles.py**](README_triangles.md): Crea una imagen PNG con una doble fila de triángulos, para usar como patrón imprimible.
- [**unzip_files_then_clean.py**](README_unzip_files_then_clean.md): Extrae todos
  los archivos ZIP en un directorio y reorganiza la estructura de carpetas.
- [**video_content_cutter.py**](README_video_content_cutter.md): Elimina el contenido desde el principio de un archivo con marca de tiempo hasta un tiempo de corte especificado en formato MM:SS.
- [**wordpress_scraper.py**](README_wordpress_scraper.md): Obtiene una página
  web protegida después de autenticarse con un formulario de inicio de sesión
  complejo (compatible con CSRF).

### Italiano

Questo repository contiene una collezione di piccoli script di utilità Python
progettati per automatizzare attività comuni e risolvere problemi specifici.
Ogni script è documentato nel proprio file README con informazioni dettagliate:

- [**eliminate_dups_in_csv.py**](README_eliminate_dups_in_csv.md): Elabora file
  CSV per rimuovere duplicati e li salva separatamente.
- [**extract_first_column_of_csv.py**](README_extract_first_column_of_csv.md):
  Estrae la prima colonna da un file CSV.
- [**pie_chart_generator.py**](README_pie_chart_generator.md): Genera una serie
  professionale di grafici a torta mostrando la progressione dei colori dallo 0% al 100%
  con ampie opzioni di personalizzazione e funzionalità moderne di Python 3.13+.
- [**scans_rename.py**](README_scans_rename.md): Rinomina e organizza file con
  timestamp giapponesi nei loro nomi.
- [**sphere_texture_generator.py**](README_sphere_texture_generator.md): Genera texture sferiche senza giunture ottimizzate per Blender e Godot utilizzando la proiezione equirettangolare. Crea texture procedurali (simili alla Terra, gigante gassoso, marmo) o converte immagini esistenti in formati pronti per le sfere con correzione automatica della distorsione ai poli.
- [**square_image_with_centered_cross_generator.py**](README_square_image_with_centered_cross_generator.md):
  Genera un'immagine quadrata con una croce centrata, con dimensioni e colori
  personalizzabili.
- [**svg_pattern_for_vase.py**](README_svg_pattern_for_vase.md): Genera un modello SVG pieghevole per un vaso con base triangolare.
- [**svg_to_bitmap_converter.py**](README_svg_to_bitmap_converter.md): Converte file SVG semplici basati su rettangoli in formati bitmap (PNG, BMP, JPEG, ecc.) con gestione completa degli errori e registrazione.
- [**triangles.py**](README_triangles.md): Crea un'immagine PNG con una doppia fila di triangoli, da utilizzare come modello stampabile.
- [**unzip_files_then_clean.py**](README_unzip_files_then_clean.md): Estrae tutti
  i file ZIP in una directory e riorganizza la struttura delle cartelle.
- [**video_content_cutter.py**](README_video_content_cutter.md): Rimuove il contenuto dall'inizio di un file con timestamp fino a un tempo di taglio specificato in formato MM:SS.
- [**wordpress_scraper.py**](README_wordpress_scraper.md): Recupera una pagina
  web protetta dopo l'autenticazione con un modulo di login complesso
  (supporta CSRF).

### Deutsch

Dieses Repository enthält eine Sammlung kleiner Python-Dienstprogrammskripte, die
entwickelt wurden, um häufige Aufgaben zu automatisieren und spezifische
Probleme zu lösen. Jedes Skript ist in seiner eigenen README-Datei mit
detaillierten Informationen dokumentiert:

- [**eliminate_dups_in_csv.py**](README_eliminate_dups_in_csv.md): Verarbeitet
  CSV-Dateien, um Duplikate zu entfernen und speichert sie separat.
- [**extract_first_column_of_csv.py**](README_extract_first_column_of_csv.md):
  Extrahiert die erste Spalte aus einer CSV-Datei.
- [**pie_chart_generator.py**](README_pie_chart_generator.md): Generiert eine
  professionelle Serie von Kreisdiagrammen, die den Farbfortschritt von 0% bis 100%
  zeigen, mit umfangreichen Anpassungsoptionen und modernen Python 3.13+ Funktionen.
- [**scans_rename.py**](README_scans_rename.md): Benennt und organisiert Dateien
  mit japanischen Zeitstempeln in ihren Dateinamen.
- [**sphere_texture_generator.py**](README_sphere_texture_generator.md): Generiert nahtlose Sphären-Texturen optimiert für Blender und Godot mit äquirektangulärer Projektion. Erstellt prozedurale Texturen (erdähnlich, Gasriese, Marmor) oder konvertiert bestehende Bilder in sphärentaugliche Formate mit automatischer Polverzerrungskorrektur.
- [**square_image_with_centered_cross_generator.py**](README_square_image_with_centered_cross_generator.md):
  Erzeugt ein quadratisches Bild mit einem zentrierten Kreuz, dessen Größe und
  Farben anpassbar sind.
- [**svg_pattern_for_vase.py**](README_svg_pattern_for_vase.md): Erzeugt ein faltbares SVG-Muster für eine Vase mit dreieckigem Boden.
- [**svg_to_bitmap_converter.py**](README_svg_to_bitmap_converter.md): Konvertiert einfache rechteckbasierte SVG-Dateien in Bitmap-Formate (PNG, BMP, JPEG, etc.) mit umfassender Fehlerbehandlung und Protokollierung.
- [**triangles.py**](README_triangles.md): Erstellt ein PNG-Bild mit einer doppelten Reihe von Dreiecken zur Verwendung als druckbares Muster.
- [**unzip_files_then_clean.py**](README_unzip_files_then_clean.md): Extrahiert
  alle ZIP-Dateien in einem Verzeichnis und reorganisiert die Ordnerstruktur.
- [**video_content_cutter.py**](README_video_content_cutter.md): Entfernt Inhalte vom Anfang einer zeitgestempelten Datei bis zu einer angegebenen MM:SS-Schnittzeit.
- [**wordpress_scraper.py**](README_wordpress_scraper.md): Ruft eine geschützte
  Webseite ab, nachdem eine Authentifizierung über ein komplexes Anmeldeformular
  (unterstützt CSRF) erfolgt ist.

## Plans

- **English**: More Python utility scripts will be added to this repository
  over time, each focused on solving specific tasks efficiently.
- **Français**: D'autres scripts utilitaires Python seront ajoutés à ce dépôt au
  fil du temps, chacun se concentrant sur la résolution efficace de tâches
  spécifiques.
- **日本語**: 今後、他のPythonユーティリティスクリプトがこのリポジトリに追加される予定で、
  それぞれが特定のタスクを効率的に解決することに焦点を当てています。
- **简体中文**: 随着时间的推移，更多的Python实用脚本将添加到此仓库中，每个脚本都专注于
  有效解决特定任务。
- **繁體中文**: 隨著時間的推移，更多的Python實用腳本將添加到此倉庫中，每個腳本都專注於
  有效解決特定任務。
- **Español**: Con el tiempo, se añadirán más scripts de utilidad Python a este
  repositorio, cada uno enfocado en resolver tareas específicas de manera
  eficiente.
- **Italiano**: Nel corso del tempo, verranno aggiunti a questo repository
  altri script di utilità Python, ognuno focalizzato sulla risoluzione
  efficiente di compiti specifici.
- **Deutsch**: Im Laufe der Zeit werden diesem Repository weitere
  Python-Dienstprogrammskripte hinzugefügt, die jeweils auf die effiziente
  Lösung spezifischer Aufgaben ausgerichtet sind.