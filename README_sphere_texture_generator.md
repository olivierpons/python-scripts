# sphere_texture_generator.py

## English

### Seamless Sphere Texture Generator

This script generates seamless sphere textures for Blender and Godot using equirectangular projection. It creates procedural textures or converts existing images to sphere-ready formats.

**Features:**
- Generates seamless sphere textures with equirectangular projection (2:1 ratio)
- Creates procedural textures: Earth-like planets, gas giants, marble patterns
- Converts images to sphere-compatible format using spherical coordinate mapping
- Applies pole distortion correction with Gaussian blur masking
- Supports resolutions: 512 (1024x512), 1K (2048x1024), 2K (4096x2048), 4K (8192x4096), 
  8K (16384x8192), or custom
- Configures noise with octaves, scale, and coordinate modes
- Optimizes textures for Blender UV mapping and Godot SphereMesh
- Outputs PNG or JPEG with adjustable JPEG quality
- Provides processing summaries

**Requirements:**
- Python 3.13+
- Pillow (≥10.0.0)
- numpy (≥1.24.0)
- noise (≥1.2.2)

**Usage:**

```bash
# Generate Earth-like texture at 2K resolution
python sphere_texture_generator.py -m procedural -t earth -r 2k -o earth_2k.png

# Generate gas giant at 4K with custom seed
python sphere_texture_generator.py -m procedural -t gas_giant -r 4k -s 123 -o jupiter.png

# Convert existing image to seamless sphere texture
python sphere_texture_generator.py -m convert -i landscape.jpg -o sphere_landscape.png -r 2k

# JPEG output with custom quality
python sphere_texture_generator.py -m procedural -t earth -f JPEG -q 98 -o earth_hq.jpg

# Batch generate textures with planetary and marble palettes (512x256, PNG)
mkdir -p ok/512; i=0; 
for TYPE in earth gas_giant; do 
    for PALETTE in jupiter neptune saturn venus mars mercury uranus pluto titan europa; do 
        export PALETTE=$PALETTE; 
        python sphere_texture_generator.py -m procedural -t $TYPE -r 512 -s $((202 + i)) -a 6 -c 100.0 --base-colors $PALETTE -o "ok/512/${TYPE}_${PALETTE}_512_seed$((202 + i)).png"; 
        ((i++)); 
    done; 
done; 
for PALETTE in jupiter neptune saturn venus mars mercury uranus pluto titan europa marble_classic marble_onyx marble_emerald; do 
    export PALETTE=$PALETTE; 
    python sphere_texture_generator.py -m procedural -t marble -r 512 -s $((202 + i)) -a 6 -c 100.0 --base-colors $PALETTE -o "ok/512/marble_${PALETTE}_512_seed$((202 + i)).png"; 
    ((i++)); 
done
```

**Arguments:**

- `-m, --mode`: Generation mode ('procedural' or 'convert')
- `-t, --texture-type`: Procedural texture type ('earth', 'gas_giant', 'marble')
- `-i, --input`: Input image file for conversion mode
- `-o, --output`: Output texture file path
- `-r, --resolution`: Resolution preset ('512', '1k', '2k', '4k', '8k')
- `-w, --width`: Custom texture width in pixels
- `-g, --height`: Custom texture height in pixels
- `-s, --seed`: Random seed for procedural generation
- `-f, --format`: Output format ('PNG', 'JPEG')
- `-q, --quality`: JPEG quality (70-100, default: 90)
- `--base-colors`: Colors for texture (JSON list of RGB tuples or predefined palette name)
- `-a, --octaves`: Noise octaves (default: 6)
- `-c, --scale`: Noise scale (default: 100.0)
- `-d, --coordinate-mode`: Noise coordinate mode ('xy' or 'xz', default: 'xy')

## Français

### Générateur de Textures Sphériques Seamless

Ce script génère des textures sphériques seamless pour Blender et Godot en utilisant la projection équirectangulaire. Il crée des textures procédurales ou convertit des images existantes en formats prêts pour les sphères.

**Fonctionnalités :**
- Génère des textures sphériques seamless avec projection équirectangulaire (ratio 2:1)
- Crée des textures procédurales : planètes terrestres, géantes gazeuses, motifs marbre
- Convertit des images en format compatible sphérique avec mapping coordonnées sphériques
- Applique une correction des distorsions polaires avec flou gaussien
- Supporte les résolutions : 512 (1024x512), 1K (2048x1024), 2K (4096x2048),
  4K (8192x4096), 8K (16384x8192), ou personnalisées
- Configure le bruit avec octaves, échelle et modes de coordonnées
- Optimise les textures pour le mapping UV Blender et SphereMesh Godot
- Sortie en PNG ou JPEG avec qualité JPEG ajustable
- Fournit des résumés de traitement

**Prérequis :**
- Python 3.13+
- Pillow (≥10.0.0)
- numpy (≥1.24.0)
- noise (≥1.2.2)

**Utilisation :**

```bash
# Générer texture terrestre en résolution 2K
python sphere_texture_generator.py -m procedural -t earth -r 2k -o terre_2k.png

# Générer géante gazeuse en 4K avec graine personnalisée
python sphere_texture_generator.py -m procedural -t gas_giant -r 4k -s 123 -o jupiter.png

# Convertir image existante en texture sphère seamless
python sphere_texture_generator.py -m convert -i paysage.jpg -o sphere_paysage.png -r 2k

# Sortie JPEG avec qualité personnalisée
python sphere_texture_generator.py -m procedural -t earth -f JPEG -q 98 -o terre_hq.jpg

# Générer en lot les textures avec palettes planétaires et marbre (512x256, PNG)
mkdir -p ok/512; i=0; 
for TYPE in earth gas_giant; do 
    for PALETTE in jupiter neptune saturn venus mars mercury uranus pluto titan europa; do 
        export PALETTE=$PALETTE; 
        python sphere_texture_generator.py -m procedural -t $TYPE -r 512 -s $((202 + i)) -a 6 -c 100.0 --base-colors $PALETTE -o "ok/512/${TYPE}_${PALETTE}_512_seed$((202 + i)).png"; 
        ((i++)); 
    done; 
done; 
for PALETTE in jupiter neptune saturn venus mars mercury uranus pluto titan europa marble_classic marble_onyx marble_emerald; do 
    export PALETTE=$PALETTE; 
    python sphere_texture_generator.py -m procedural -t marble -r 512 -s $((202 + i)) -a 6 -c 100.0 --base-colors $PALETTE -o "ok/512/marble_${PALETTE}_512_seed$((202 + i)).png"; 
    ((i++)); 
done
```

**Arguments :**

- `-m, --mode` : Mode de génération ('procedural' ou 'convert')
- `-t, --texture-type` : Type de texture procédurale ('earth', 'gas_giant', 'marble')
- `-i, --input` : Fichier image d'entrée pour le mode conversion
- `-o, --output` : Chemin du fichier texture de sortie
- `-r, --resolution` : Préréglage résolution ('512', '1k', '2k', '4k', '8k')
- `-w, --width` : Largeur texture personnalisée en pixels
- `-g, --height` : Hauteur texture personnalisée en pixels
- `-s, --seed` : Graine aléatoire pour génération procédurale
- `-f, --format` : Format de sortie ('PNG', 'JPEG')
- `-q, --quality` : Qualité JPEG (70-100, défaut : 90)
- `--base-colors` : Couleurs pour la texture (liste JSON de tuples RGB ou nom de palette prédéfinie)
- `-a, --octaves` : Octaves de bruit (défaut : 6)
- `-c, --scale` : Échelle de bruit (défaut : 100.0)
- `-d, --coordinate-mode` : Mode de coordonnées de bruit ('xy' ou 'xz', défaut : 'xy')

## 日本語

### シームレス球体テクスチャジェネレーター

このスクリプトは、正距円筒図法を使用してBlenderとGodot用にシームレス球体テクスチャを生成します。手続き的テクスチャを作成するか、既存の画像を球体対応フォーマットに変換します。

**機能：**
- 正距円筒図法（2:1比率）でシームレス球体テクスチャを生成
- 手続き的テクスチャを作成：地球風惑星、ガス惑星、大理石パターン
- 球面座標マッピングで画像を球体互換フォーマットに変換
- ガウシアンブラーマスキングで極点歪みを補正
- 解像度をサポート：512 (1024x512)、1K (2048x1024)、2K (4096x2048)、4K (8192x4096)、8K (16384x8192)、またはカスタム
- オクターブ、スケール、座標モードでノイズを設定
- BlenderのUVマッピングとGodotのSphereMesh用に最適化
- PNGまたはJPEG出力、JPEG品質調整可能
- 処理サマリーを提供

**必要条件：**
- Python 3.13+
- Pillow (≥10.0.0)
- numpy (≥1.24.0)
- noise (≥1.2.2)

**使用法：**

```bash
# 2K解像度で地球風テクスチャ生成
python sphere_texture_generator.py -m procedural -t earth -r 2k -o earth_2k.png

# カスタムシードで4K解像度のガス惑星生成
python sphere_texture_generator.py -m procedural -t gas_giant -r 4k -s 123 -o jupiter.png

# 既存画像をシームレス球体テクスチャに変換
python sphere_texture_generator.py -m convert -i landscape.jpg -o sphere_landscape.png -r 2k

# JPEG出力、カスタム品質
python sphere_texture_generator.py -m procedural -t earth -f JPEG -q 98 -o earth_hq.jpg

# 惑星および大理石パレットでテクスチャをバッチ生成（512x256、PNG）
mkdir -p ok/512; i=0; 
for TYPE in earth gas_giant; do 
    for PALETTE in jupiter neptune saturn venus mars mercury uranus pluto titan europa; do 
        export PALETTE=$PALETTE; 
        python sphere_texture_generator.py -m procedural -t $TYPE -r 512 -s $((202 + i)) -a 6 -c 100.0 --base-colors $PALETTE -o "ok/512/${TYPE}_${PALETTE}_512_seed$((202 + i)).png"; 
        ((i++)); 
    done; 
done; 
for PALETTE in jupiter neptune saturn venus mars mercury uranus pluto titan europa marble_classic marble_onyx marble_emerald; do 
    export PALETTE=$PALETTE; 
    python sphere_texture_generator.py -m procedural -t marble -r 512 -s $((202 + i)) -a 6 -c 100.0 --base-colors $PALETTE -o "ok/512/marble_${PALETTE}_512_seed$((202 + i)).png"; 
    ((i++)); 
done
```

**引数：**

- `-m, --mode`：生成モード（'procedural'または'convert'）
- `-t, --texture-type`：手続き的テクスチャタイプ（'earth'、'gas_giant'、'marble'）
- `-i, --input`：変換モード用の入力画像ファイル
- `-o, --output`：出力テクスチャファイルパス
- `-r, --resolution`：解像度プリセット（'512'、'1k'、'2k'、'4k'、'8k'）
- `-w, --width`：カスタムテクスチャ幅（ピクセル）
- `-g, --height`：カスタムテクスチャ高さ（ピクセル）
- `-s, --seed`：手続き的生成用のランダムシード
- `-f, --format`：出力フォーマット（'PNG'、'JPEG'）
- `-q, --quality`：JPEG品質（70-100、デフォルト：90）
- `--base-colors`：テクスチャの色（RGBタプルのJSONリストまたは定義済みパレット名）
- `-a, --octaves`：ノイズのオクターブ（デフォルト：6）
- `-c, --scale`：ノイズスケール（デフォルト：100.0）
- `-d, --coordinate-mode`：ノイズ座標モード（'xy'または'xz'、デフォルト：'xy'）

## 简体中文

### 无缝球体纹理生成器

此脚本使用等距圆柱投影为Blender和Godot生成无缝球体纹理。创建程序化纹理或将现有图像转换为球体就绪格式。

**功能：**
- 使用等距圆柱投影（2:1比例）生成无缝球体纹理
- 创建程序化纹理：类地行星、气态巨行星、大理石图案
- 使用球面坐标映射将图像转换为球体兼容格式
- 使用高斯模糊遮罩校正极点畸变
- 支持分辨率：512 (1024x512)、1K (2048x1024)、2K (4096x2048)、4K (8192x4096)、8K (16384x8192)，或自定义
- 使用倍频程、尺度、坐标模式配置噪声
- 为Blender UV映射和Godot SphereMesh优化
- 输出PNG或JPEG，可调整JPEG质量
- 提供处理摘要

**要求：**
- Python 3.13+
- Pillow (≥10.0.0)
- numpy (≥1.24.0)
- noise (≥1.2.2)

**使用方法：**

```bash
# 生成2K分辨率类地纹理
python sphere_texture_generator.py -m procedural -t earth -r 2k -o earth_2k.png

# 用自定义种子生成4K分辨率气态巨行星
python sphere_texture_generator.py -m procedural -t gas_giant -r 4k -s 123 -o jupiter.png

# 将现有图像转换为无缝球体纹理
python sphere_texture_generator.py -m convert -i landscape.jpg -o sphere_landscape.png -r 2k

# JPEG输出，自定义质量
python sphere_texture_generator.py -m procedural -t earth -f JPEG -q 98 -o earth_hq.jpg

# 批量生成带有行星和大理石调色板的纹理（512x256，PNG）
mkdir -p ok/512; i=0; 
for TYPE in earth gas_giant; do 
    for PALETTE in jupiter neptune saturn venus mars mercury uranus pluto titan europa; do 
        export PALETTE=$PALETTE; 
        python sphere_texture_generator.py -m procedural -t $TYPE -r 512 -s $((202 + i)) -a 6 -c 100.0 --base-colors $PALETTE -o "ok/512/${TYPE}_${PALETTE}_512_seed$((202 + i)).png"; 
        ((i++)); 
    done; 
done; 
for PALETTE in jupiter neptune saturn venus mars mercury uranus pluto titan europa marble_classic marble_onyx marble_emerald; do 
    export PALETTE=$PALETTE; 
    python sphere_texture_generator.py -m procedural -t marble -r 512 -s $((202 + i)) -a 6 -c 100.0 --base-colors $PALETTE -o "ok/512/marble_${PALETTE}_512_seed$((202 + i)).png"; 
    ((i++)); 
done
```

**参数：**

- `-m, --mode`：生成模式（'procedural'或'convert'）
- `-t, --texture-type`：程序化纹理类型（'earth'、'gas_giant'、'marble'）
- `-i, --input`：转换模式的输入图像文件
- `-o, --output`：输出纹理文件路径
- `-r, --resolution`：分辨率预设（'512'、'1k'、'2k'、'4k'、'8k'）
- `-w, --width`：自定义纹理宽度（像素）
- `-g, --height`：自定义纹理高度（像素）
- `-s, --seed`：程序化生成的随机种子
- `-f, --format`：输出格式（'PNG'、'JPEG'）
- `-q, --quality`：JPEG质量（70-100，默认：90）
- `--base-colors`：纹理颜色（RGB元组的JSON列表或预定义调色板名称）
- `-a, --octaves`：噪声倍频程（默认：6）
- `-c, --scale`：噪声尺度（默认：100.0）
- `-d, --coordinate-mode`：噪声坐标模式（'xy'或'xz'，默认：'xy'）

## 繁體中文

### 無縫球體紋理生成器

此腳本使用等距圓柱投影為Blender和Godot生成無縫球體紋理。創建程序化紋理或將現有圖像轉換為球體就緒格式。

**功能：**
- 使用等距圓柱投影（2:1比例）生成無縫球體紋理
- 創建程序化紋理：類地行星、氣態巨行星、大理石圖案
- 使用球面座標映射將圖像轉換為球體兼容格式
- 使用高斯模糊遮罩校正極點畸變
- 支持分辨率：512 (1024x512)、1K (2048x1024)、2K (4096x2048)、4K (8192x4096)、8K (16384x8192)，或自訂
- 使用倍頻程、尺度、座標模式配置噪聲
- 為Blender UV映射和Godot SphereMesh優化
- 輸出PNG或JPEG，可調整JPEG品質
- 提供處理摘要

**要求：**
- Python 3.13+
- Pillow (≥10.0.0)
- numpy (≥1.24.0)
- noise (≥1.2.2)

**使用方法：**

```bash
# 生成2K分辨率類地紋理
python sphere_texture_generator.py -m procedural -t earth -r 2k -o earth_2k.png

# 用自訂種子生成4K分辨率氣態巨行星
python sphere_texture_generator.py -m procedural -t gas_giant -r 4k -s 123 -o jupiter.png

# 將現有圖像轉換為無縫球體紋理
python sphere_texture_generator.py -m convert -i landscape.jpg -o sphere_landscape.png -r 2k

# JPEG輸出，自訂品質
python sphere_texture_generator.py -m procedural -t earth -f JPEG -q 98 -o earth_hq.jpg

# 批量生成帶有行星和大理石調色板的紋理（512x256，PNG）
mkdir -p ok/512; i=0; 
for TYPE in earth gas_giant; do 
    for PALETTE in jupiter neptune saturn venus mars mercury uranus pluto titan europa; do 
        export PALETTE=$PALETTE; 
        python sphere_texture_generator.py -m procedural -t $TYPE -r 512 -s $((202 + i)) -a 6 -c 100.0 --base-colors $PALETTE -o "ok/512/${TYPE}_${PALETTE}_512_seed$((202 + i)).png"; 
        ((i++)); 
    done; 
done; 
for PALETTE in jupiter neptune saturn venus mars mercury uranus pluto titan europa marble_classic marble_onyx marble_emerald; do 
    export PALETTE=$PALETTE; 
    python sphere_texture_generator.py -m procedural -t marble -r 512 -s $((202 + i)) -a 6 -c 100.0 --base-colors $PALETTE -o "ok/512/marble_${PALETTE}_512_seed$((202 + i)).png"; 
    ((i++)); 
done
```

**參數：**

- `-m, --mode`：生成模式（'procedural'或'convert'）
- `-t, --texture-type`：程序化紋理類型（'earth'、'gas_giant'、'marble'）
- `-i, --input`：轉換模式的輸入圖像檔案
- `-o, --output`：輸出紋理檔案路徑
- `-r, --resolution`：分辨率預設（'512'、'1k'、'2k'、'4k'、'8k'）
- `-w, --width`：自訂紋理寬度（像素）
- `-g, --height`：自訂紋理高度（像素）
- `-s, --seed`：程序化生成的隨機種子
- `-f, --format`：輸出格式（'PNG'、'JPEG'）
- `-q, --quality`：JPEG品質（70-100，默認：90）
- `--base-colors`：紋理顏色（RGB元組的JSON列表或預定義調色板名稱）
- `-a, --octaves`：噪聲倍頻程（默認：6）
- `-c, --scale`：噪聲尺度（默認：100.0）
- `-d, --coordinate-mode`：噪聲座標模式（'xy'或'xz'，默認：'xy'）

## Español

### Generador de Texturas Esféricas Sin Costuras

Este script genera texturas esféricas sin costuras para Blender y Godot usando proyección equirectangular. Crea texturas procedimentales o convierte imágenes existentes a formatos listos para esferas.

**Características:**
- Genera texturas esféricas sin costuras con proyección equirectangular (proporción 2:1)
- Crea texturas procedimentales: planetas terrestres, gigantes gaseosos, patrones mármol
- Convierte imágenes a formato compatible con esferas usando mapeo coordenadas esféricas
- Aplica corrección de distorsión polar con difuminado gaussiano
- Soporta resoluciones: 512 (1024x512), 1K (2048x1024), 2K (4096x2048), 4K (8192x4096), 8K (16384x8192), o personalizadas
- Configura ruido con octavas, escala y modos de coordenadas
- Optimiza texturas para mapeo UV Blender y SphereMesh Godot
- Salida en PNG o JPEG con calidad JPEG ajustable
- Proporciona resúmenes de procesamiento

**Requisitos:**
- Python 3.13+
- Pillow (≥10.0.0)
- numpy (≥1.24.0)
- noise (≥1.2.2)

**Uso:**

```bash
# Generar textura terrestre en resolución 2K
python sphere_texture_generator.py -m procedural -t earth -r 2k -o earth_2k.png

# Generar gigante gaseoso en 4K con semilla personalizada
python sphere_texture_generator.py -m procedural -t gas_giant -r 4k -s 123 -o jupiter.png

# Convertir imagen existente a textura esfera sin costuras
python sphere_texture_generator.py -m convert -i paisaje.jpg -o sphere_paisaje.png -r 2k

# Salida JPEG con calidad personalizada
python sphere_texture_generator.py -m procedural -t earth -f JPEG -q 98 -o earth_hq.jpg

# Generar en lote texturas con paletas planetarias y de mármol (512x256, PNG)
mkdir -p ok/512; i=0; 
for TYPE in earth gas_giant; do 
    for PALETTE in jupiter neptune saturn venus mars mercury uranus pluto titan europa; do 
        export PALETTE=$PALETTE; 
        python sphere_texture_generator.py -m procedural -t $TYPE -r 512 -s $((202 + i)) -a 6 -c 100.0 --base-colors $PALETTE -o "ok/512/${TYPE}_${PALETTE}_512_seed$((202 + i)).png"; 
        ((i++)); 
    done; 
done; 
for PALETTE in jupiter neptune saturn venus mars mercury uranus pluto titan europa marble_classic marble_onyx marble_emerald; do 
    export PALETTE=$PALETTE; 
    python sphere_texture_generator.py -m procedural -t marble -r 512 -s $((202 + i)) -a 6 -c 100.0 --base-colors $PALETTE -o "ok/512/marble_${PALETTE}_512_seed$((202 + i)).png"; 
    ((i++)); 
done
```

**Argumentos:**

- `-m, --mode`: Modo de generación ('procedural' o 'convert')
- `-t, --texture-type`: Tipo de textura procedimental ('earth', 'gas_giant', 'marble')
- `-i, --input`: Archivo imagen entrada para modo conversión
- `-o, --output`: Ruta archivo textura salida
- `-r, --resolution`: Preajuste resolución ('512', '1k', '2k', '4k', '8k')
- `-w, --width`: Ancho textura personalizada en píxeles
- `-g, --height`: Alto textura personalizada en píxeles
- `-s, --seed`: Semilla aleatoria para generación procedimental
- `-f, --format`: Formato salida ('PNG', 'JPEG')
- `-q, --quality`: Calidad JPEG (70-100, predeterminado: 90)
- `--base-colors`: Colores para textura (lista JSON de tuplas RGB o nombre de paleta predefinida)
- `-a, --octaves`: Octavas de ruido (predeterminado: 6)
- `-c, --scale`: Escala de ruido (predeterminado: 100.0)
- `-d, --coordinate-mode`: Modo de coordenadas de ruido ('xy' o 'xz', predeterminado: 'xy')

## Italiano

### Generatore di Texture Sferiche Senza Giunture

Questo script genera texture sferiche senza giunture per Blender e Godot utilizzando proiezione equirettangolare. Crea texture procedurali o converte immagini esistenti in formati pronti per sfere.

**Funzionalità:**
- Genera texture sferiche senza giunture con proiezione equirettangolare (rapporto 2:1)
- Crea texture procedurali: pianeti terrestri, giganti gassosi, pattern marmorei
- Converte immagini in formato compatibile sfere con mappatura coordinate sferiche
- Applica correzione distorsione polare con sfocatura gaussiana
- Supporta risoluzioni: 512 (1024x512), 1K (2048x1024), 2K (4096x2048), 4K (8192x4096), 8K (16384x8192), o personalizzate
- Configura rumore con ottave, scala e modalità coordinate
- Ottimizza texture per mappatura UV Blender e SphereMesh Godot
- Output in PNG o JPEG con qualità JPEG regolabile
- Fornisce riassunti di elaborazione

**Requisiti:**
- Python 3.13+
- Pillow (≥10.0.0)
- numpy (≥1.24.0)
- noise (≥1.2.2)

**Utilizzo:**

```bash
# Generare texture terrestre a risoluzione 2K
python sphere_texture_generator.py -m procedural -t earth -r 2k -o earth_2k.png

# Generare gigante gassoso a 4K con seme personalizzato
python sphere_texture_generator.py -m procedural -t gas_giant -r 4k -s 123 -o jupiter.png

# Convertire immagine esistente a texture sfera senza giunture
python sphere_texture_generator.py -m convert -i paesaggio.jpg -o sphere_paesaggio.png -r 2k

# Output JPEG con qualità personalizzata
python sphere_texture_generator.py -m procedural -t earth -f JPEG -q 98 -o earth_hq.jpg

# Generare in batch texture con palette planetarie e marmoree (512x256, PNG)
mkdir -p ok/512; i=0; 
for TYPE in earth gas_giant; do 
    for PALETTE in jupiter neptune saturn venus mars mercury uranus pluto titan europa; do 
        export PALETTE=$PALETTE; 
        python sphere_texture_generator.py -m procedural -t $TYPE -r 512 -s $((202 + i)) -a 6 -c 100.0 --base-colors $PALETTE -o "ok/512/${TYPE}_${PALETTE}_512_seed$((202 + i)).png"; 
        ((i++)); 
    done; 
done; 
for PALETTE in jupiter neptune saturn venus mars mercury uranus pluto titan europa marble_classic marble_onyx marble_emerald; do 
    export PALETTE=$PALETTE; 
    python sphere_texture_generator.py -m procedural -t marble -r 512 -s $((202 + i)) -a 6 -c 100.0 --base-colors $PALETTE -o "ok/512/marble_${PALETTE}_512_seed$((202 + i)).png"; 
    ((i++)); 
done
```

**Argomenti:**

- `-m, --mode`: Modalità generazione ('procedural' o 'convert')
- `-t, --texture-type`: Tipo texture procedurale ('earth', 'gas_giant', 'marble')
- `-i, --input`: File immagine input per modalità conversione
- `-o, --output`: Percorso file texture output
- `-r, --resolution`: Preimpostazione risoluzione ('512', '1k', '2k', '4k', '8k')
- `-w, --width`: Larghezza texture personalizzata in pixel
- `-g, --height`: Altezza texture personalizzata in pixel
- `-s, --seed`: Seme casuale per generazione procedurale
- `-f, --format`: Formato output ('PNG', 'JPEG')
- `-q, --quality`: Qualità JPEG (70-100, predefinito: 90)
- `--base-colors`: Colori per texture (lista JSON di tuple RGB o nome palette predefinita)
- `-a, --octaves`: Ottave di rumore (predefinito: 6)
- `-c, --scale`: Scala di rumore (predefinito: 100.0)
- `-d, --coordinate-mode`: Modalità coordinate rumore ('xy' o 'xz', predefinito: 'xy')

## Deutsch

### Nahtloser Sphären-Textur-Generator

Dieses Skript generiert nahtlose Sphären-Texturen für Blender und Godot mit äquirektangulärer Projektion. Es erstellt prozedurale Texturen oder konvertiert bestehende Bilder in sphärentaugliche Formate.

**Funktionen:**
- Generiert nahtlose Sphären-Texturen mit äquirektangulärer Projektion (2:1-Verhältnis)
- Erstellt prozedurale Texturen: erdähnliche Planeten, Gasriesen, Marmormuster
- Konvertiert Bilder in sphärenkompatibles Format mit sphärischer Koordinatenmappierung
- Wendet Polverzerrungskorrektur mit Gaußscher Unschärfe an
- Unterstützt Auflösungen: 512 (1024x512), 1K (2048x1024), 2K (4096x2048), 4K (8192x4096), 8K (16384x8192), oder benutzerdefiniert
- Konfiguriert Rausch mit Oktaven, Skala und Koordinatenmodi
- Optimiert Texturen für Blender UV-Mapping und Godot SphereMesh
- Ausgabe in PNG oder JPEG mit einstellbarer JPEG-Qualität
- Liefert Verarbeitungszusammenfassungen

**Anforderungen:**
- Python 3.13+
- Pillow (≥10.0.0)
- numpy (≥1.24.0)
- noise (≥1.2.2)

**Verwendung:**

```bash
# Erdähnliche Textur in 2K-Auflösung generieren
python sphere_texture_generator.py -m procedural -t earth -r 2k -o earth_2k.png

# Gasriese in 4K mit benutzerdefiniertem Seed generieren
python sphere_texture_generator.py -m procedural -t gas_giant -r 4k -s 123 -o jupiter.png

# Vorhandenes Bild in nahtlose Sphären-Textur konvertieren
python sphere_texture_generator.py -m convert -i landschaft.jpg -o sphere_landschaft.png -r 2k

# JPEG-Ausgabe mit benutzerdefinierter Qualität
python sphere_texture_generator.py -m procedural -t earth -f JPEG -q 98 -o earth_hq.jpg

# Alle Texturen mit planetaren und Marmorpaletten im Batch generieren (512x256, PNG)
mkdir -p ok/512; i=0; 
for TYPE in earth gas_giant; do 
    for PALETTE in jupiter neptune saturn venus mars mercury uranus pluto titan europa; do 
        export PALETTE=$PALETTE; 
        python sphere_texture_generator.py -m procedural -t $TYPE -r 512 -s $((202 + i)) -a 6 -c 100.0 --base-colors $PALETTE -o "ok/512/${TYPE}_${PALETTE}_512_seed$((202 + i)).png"; 
        ((i++)); 
    done; 
done; 
for PALETTE in jupiter neptune saturn venus mars mercury uranus pluto titan europa marble_classic marble_onyx marble_emerald; do 
    export PALETTE=$PALETTE; 
    python sphere_texture_generator.py -m procedural -t marble -r 512 -s $((202 + i)) -a 6 -c 100.0 --base-colors $PALETTE -o "ok/512/marble_${PALETTE}_512_seed$((202 + i)).png"; 
    ((i++)); 
done
```

**Argumente:**

- `-m, --mode`: Generierungsmodus ('procedural' oder 'convert')
- `-t, --texture-type`: Prozeduraler Texturtyp ('earth', 'gas_giant', 'marble')
- `-i, --input`: Eingabe-Bilddatei für Konvertierungsmodus
- `-o, --output`: Ausgabe-Texturdateipfad
- `-r, --resolution`: Auflösungsvoreinstellung ('512', '1k', '2k', '4k', '8k')
- `-w, --width`: Benutzerdefinierte Texturbreite in Pixeln
- `-g, --height`: Benutzerdefinierte Texturhöhe in Pixeln
- `-s, --seed`: Zufallsseed für prozedurale Generierung
- `-f, --format`: Ausgabeformat ('PNG', 'JPEG')
- `-q, --quality`: JPEG-Qualität (70-100, Standard: 90)
- `--base-colors`: Farben für Textur (JSON-Liste von RGB-Tupeln oder vordefinierter Palettenname)
- `-a, --octaves`: Rausch-Oktaven (Standard: 6)
- `-c, --scale`: Rausch-Skala (Standard: 100.0)
- `-d, --coordinate-mode`: Rausch-Koordinatenmodus ('xy' oder 'xz', Standard: 'xy')
