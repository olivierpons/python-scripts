# square_image_with_centered_cross_generator.py

## English

### Square Image with Centered Cross Generator

This script creates a square image with a perfectly centered cross. The image
size, colors, cross thickness, and output format are all customizable.

**Features:**

- Generates a square image of any specified odd size for perfect centering.
- Draws a perfectly centered cross on the image.
- Customizable colors for the cross and the background.
- Supports multiple color formats: RGB (`255,0,0`), HEX (`#ff0000`), and single
  integer for grayscale (`128`).
- Allows for custom cross thickness.
- Can save the output image as either PNG or WEBP.

**Usage:**

```bash
python square_image_with_centered_cross_generator.py \
    --size <SIZE> --cross-color <COLOR> --bg-color <COLOR> \
    [--format <FORMAT>] [--thickness <THICKNESS>]
```

**Arguments:**

- `-s, --size`: Image width/height (must be an odd number).
- `-c, --cross-color`: Color of the cross (e.g., '255,0,0', '#ff0000', '128').
- `-b, --bg-color`: Color of the background (same formats as cross-color).
- `-f, --format`: Output image format ('png' or 'webp', default: 'png').
- `-t, --thickness`: Thickness of the cross in pixels
  (default: auto-calculated).

## Français

### Générateur d'Image Carrée avec Croix Centrée

Ce script crée une image carrée avec une croix parfaitement centrée. La taille de
l'image, les couleurs, l'épaisseur de la croix et le format de sortie sont tous
personnalisables.

**Fonctionnalités :**

- Génère une image carrée de n'importe quelle taille impaire spécifiée pour un
  centrage parfait.
- Dessine une croix parfaitement centrée sur l'image.
- Couleurs personnalisables pour la croix et l'arrière-plan.
- Prend en charge plusieurs formats de couleur : RVB (`255,0,0`), HEX
  (`#ff0000`), et un entier unique pour les niveaux de gris (`128`).
- Permet de définir une épaisseur de croix personnalisée.
- Peut enregistrer l'image de sortie en format PNG ou WEBP.

**Utilisation :**

```bash
python square_image_with_centered_cross_generator.py \
    --size <TAILLE> --cross-color <COULEUR> --bg-color <COULEUR> \
    [--format <FORMAT>] [--thickness <ÉPAISSEUR>]
```

**Arguments :**

- `-s, --size` : Largeur/hauteur de l'image (doit être un nombre impair).
- `-c, --cross-color` : Couleur de la croix (ex. : '255,0,0', '#ff0000', '128').
- `-b, --bg-color` : Couleur de l'arrière-plan (mêmes formats que cross-color).
- `-f, --format` : Format de l'image de sortie ('png' ou 'webp', par défaut :
  'png').
- `-t, --thickness` : Épaisseur de la croix en pixels (par défaut : calculée
  automatiquement).

## 日本語

### 中央に十字がある正方形画像ジェネレーター

このスクリプトは、完全に中央に配置された十字を持つ正方形の画像を生成します。
画像のサイズ、色、十字の太さ、出力形式はすべてカスタマイズ可能です。

**機能：**

- 完璧なセンタリングのために、指定された奇数のサイズの正方形画像を生成します。
- 画像上に完全に中央に配置された十字を描画します。
- 十字と背景の色をカスタマイズできます。
- 複数のカラーフォーマットをサポート：RGB（`255,0,0`）、HEX（`#ff0000`）、
  およびグレースケール用の単一整数（`128`）。
- 十字の太さをカスタム設定できます。
- 出力画像をPNGまたはWEBPとして保存できます。

**使用法：**

```bash
python square_image_with_centered_cross_generator.py \
    --size <サイズ> --cross-color <色> --bg-color <色> \
    [--format <フォーマット>] [--thickness <太さ>]
```

**引数：**

- `-s, --size`：画像の幅/高さ（奇数である必要があります）。
- `-c, --cross-color`：十字の色（例：「255,0,0」、「#ff0000」、「128」）。
- `-b, --bg-color`：背景の色（十字の色と同じフォーマット）。
- `-f, --format`：出力画像フォーマット（「png」または「webp」、
  デフォルト：「png」）。
- `-t, --thickness`：十字の太さ（ピクセル単位、デフォルト：自動計算）。

## 简体中文

### 带居中十字的正方形图像生成器

此脚本创建一个带有完美居中十字的正方形图像。图像大小、颜色、十字厚度和输出
格式均可自定义。

**功能：**

- 生成任何指定的奇数尺寸的方形图像，以实现完美居中。
- 在图像上绘制一个完美居中的十字。
- 可自定义十字和背景的颜色。
- 支持多种颜色格式：RGB (`255,0,0`)、HEX (`#ff0000`) 和用于灰度的单个整数
  (`128`)。
- 允许自定义十字的厚度。
- 可以将输出图像保存为PNG或WEBP格式。

**使用方法：**

```bash
python square_image_with_centered_cross_generator.py \
    --size <尺寸> --cross-color <颜色> --bg-color <颜色> \
    [--format <格式>] [--thickness <厚度>]
```

**参数：**

- `-s, --size`: 图像的宽度/高度（必须是奇数）。
- `-c, --cross-color`: 十字的颜色（例如：'255,0,0', '#ff0000', '128'）。
- `-b, --bg-color`: 背景的颜色（格式与十字颜色相同）。
- `-f, --format`: 输出图像格式（'png' 或 'webp'，默认：'png'）。
- `-t, --thickness`: 十字的厚度（像素）（默认：自动计算）。

## 繁體中文

### 帶居中十字的正方形圖像生成器

此腳本創建一個帶有完美居中十字的正方形圖像。圖像大小、顏色、十字厚度和輸出
格式均可自訂。

**功能：**

- 生成任何指定的奇數尺寸的方形圖像，以實現完美居中。
- 在圖像上繪製一個完美居中的十字。
- 可自訂十字和背景的顏色。
- 支援多種顏色格式：RGB (`255,0,0`)、HEX (`#ff0000`) 和用於灰階的單個整數
  (`128`)。
- 允許自訂十字的厚度。
- 可以將輸出圖像儲存為PNG或WEBP格式。

**使用方法：**

```bash
python square_image_with_centered_cross_generator.py \
    --size <尺寸> --cross-color <顏色> --bg-color <顏色> \
    [--format <格式>] [--thickness <厚度>]
```

**參數：**

- `-s, --size`: 圖像的寬度/高度（必須是奇數）。
- `-c, --cross-color`: 十字的顏色（例如：'255,0,0', '#ff0000', '128'）。
- `-b, --bg-color`: 背景的顏色（格式與十字顏色相同）。
- `-f, --format`: 輸出圖像格式（'png' 或 'webp'，預設：'png'）。
- `-t, --thickness`: 十字的厚度（像素）（預設：自動計算）。

## Español

### Generador de Imágenes Cuadradas con Cruz Centrada

Este script crea una imagen cuadrada con una cruz perfectamente centrada. El
tamaño de la imagen, los colores, el grosor de la cruz y el formato de salida son
todos personalizables.

**Características:**

- Genera una imagen cuadrada de cualquier tamaño impar especificado para un
  centrado perfecto.
- Dibuja una cruz perfectamente centrada en la imagen.
- Colores personalizables para la cruz y el fondo.
- Soporta múltiples formatos de color: RGB (`255,0,0`), HEX (`#ff0000`), y un
  solo entero para escala de grises (`128`).
- Permite un grosor de cruz personalizado.
- Puede guardar la imagen de salida como PNG o WEBP.

**Uso:**

```bash
python square_image_with_centered_cross_generator.py \
    --size <TAMAÑO> --cross-color <COLOR> --bg-color <COLOR> \
    [--format <FORMATO>] [--thickness <GROSOR>]
```

**Argumentos:**

- `-s, --size`: Ancho/alto de la imagen (debe ser un número impar).
- `-c, --cross-color`: Color de la cruz (ej: '255,0,0', '#ff0000', '128').
- `-b, --bg-color`: Color del fondo (mismos formatos que el color de la cruz).
- `-f, --format`: Formato de imagen de salida ('png' o 'webp', por defecto:
  'png').
- `-t, --thickness`: Grosor de la cruz en píxeles (por defecto: calculado
  automáticamente).

## Italiano

### Generatore di Immagini Quadrate con Croce Centrale

Questo script crea un'immagine quadrata con una croce perfettamente centrata. Le
dimensioni dell'immagine, i colori, lo spessore della croce e il formato di
output sono tutti personalizzabili.

**Funzionalità:**

- Genera un'immagine quadrata di qualsiasi dimensione dispari specificata per un
  centraggio perfetto.
- Disegna una croce perfettamente centrata sull'immagine.
- Colori personalizzabili per la croce e lo sfondo.
- Supporta più formati di colore: RGB (`255,0,0`), HEX (`#ff0000`) e un singolo
  intero per la scala di grigi (`128`).
- Consente di impostare uno spessore della croce personalizzato.
- Può salvare l'immagine di output in formato PNG o WEBP.

**Utilizzo:**

```bash
python square_image_with_centered_cross_generator.py \
    --size <DIMENSIONE> --cross-color <COLORE> --bg-color <COLORE> \
    [--format <FORMATO>] [--thickness <SPESSORE>]
```

**Argomenti:**

- `-s, --size`: Larghezza/altezza dell'immagine (deve essere un numero dispari).
- `-c, --cross-color`: Colore della croce (es. '255,0,0', '#ff0000', '128').
- `-b, --bg-color`: Colore dello sfondo (stessi formati del colore della croce).
- `-f, --format`: Formato dell'immagine di output ('png' o 'webp', predefinito:
  'png').
- `-t, --thickness`: Spessore della croce in pixel (predefinito: calcolato
  automaticamente).

## Deutsch

### Generator für quadratische Bilder mit zentriertem Kreuz

Dieses Skript erstellt ein quadratisches Bild mit einem perfekt zentrierten Kreuz.
Bildgröße, Farben, Kreuzdicke und Ausgabeformat sind alle anpassbar.

**Funktionen:**

- Erzeugt ein quadratisches Bild jeder angegebenen ungeraden Größe für eine
  perfekte Zentrierung.
- Zeichnet ein perfekt zentriertes Kreuz auf das Bild.
- Anpassbare Farben für das Kreuz und den Hintergrund.
- Unterstützt mehrere Farbformate: RGB (`255,0,0`), HEX (`#ff0000`) und eine
  einzelne Ganzzahl für Graustufen (`128`).
- Ermöglicht eine benutzerdefinierte Kreuzdicke.
- Kann das Ausgabebild als PNG oder WEBP speichern.

**Verwendung:**

```bash
python square_image_with_centered_cross_generator.py \
    --size <GRÖSSE> --cross-color <FARBE> --bg-color <FARBE> \
    [--format <FORMAT>] [--thickness <DICKE>]
```

**Argumente:**

- `-s, --size`: Bildbreite/-höhe (muss eine ungerade Zahl sein).
- `-c, --cross-color`: Farbe des Kreuzes (z.B. '255,0,0', '#ff0000', '128').
- `-b, --bg-color`: Farbe des Hintergrunds (gleiche Formate wie Kreuzfarbe).
- `-f, --format`: Ausgabebildformat ('png' oder 'webp', Standard: 'png').
- `-t, --thickness`: Dicke des Kreuzes in Pixeln (Standard: automatisch
  berechnet).
