# sphere_texture_generator.py

## English

### Seamless Sphere Texture Generator

This script generates seamless sphere textures optimized for Blender and Godot using 
equirectangular projection. Creates procedural textures (Earth-like planets, gas giants,
marble patterns) or converts existing images to sphere-ready formats with automatic 
pole distortion correction, power-of-2 optimization, and comprehensive noise 
configuration.

**Features:**

- Generates seamless sphere textures using equirectangular projection (2:1 ratio)
- Creates procedural textures: Earth-like planets, gas giants, marble patterns
- Converts existing images to sphere-compatible format with spherical coordinate mapping
- Optimized for Blender UV mapping and Godot SphereMesh with automatic compatibility checks
- Advanced pole correction using Gaussian blur masking and pixel consolidation
- Flexible resolutions: standard presets (512, 1K, 2K, 4K, 8K) plus custom dimensions
- Comprehensive noise configuration with octave controls and coordinate modes
- Refactored coordinate generation to eliminate code duplication for improved maintainability
- Robust type hints using `TypeAlias` for better mypy compatibility and modern Python 3.13+ features
- Professional output with JPEG quality control and PNG optimization
- Detailed processing summaries and validation
- Modern Python 3.13+ features with dataclasses and union types

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

# High-quality JPEG output with custom quality
python sphere_texture_generator.py -m procedural -t earth -f JPEG -q 98 -o earth_hq.jpg

# Batch generate all textures with planetary and marble palettes (512x256, PNG)
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

Ce script génère des textures sphériques seamless optimisées pour Blender et Godot en 
utilisant la projection équirectangulaire. Crée des textures procédurales (planètes 
terrestres, géantes gazeuses, motifs marbre) ou convertit des images existantes 
en formats prêts pour les sphères avec correction automatique des distorsions 
polaires, optimisation `power-of-2`, et configuration complète du bruit.

**Fonctionnalités :**

- Génère des textures sphériques seamless utilisant la projection équirectangulaire (ratio 2:1)
- Crée des textures procédurales : planètes terrestres, géantes gazeuses, motifs marbre
- Convertit des images existantes en format compatible sphérique avec mapping coordonnées sphériques
- Optimisé pour le mapping UV Blender et SphereMesh Godot avec vérifications compatibilité automatiques
- Correction polaire avancée utilisant masquage flou gaussien et consolidation pixels
- Résolutions flexibles : préréglages standard (512, 1K, 2K, 4K, 8K) plus dimensions personnalisées
- Configuration complète du bruit avec contrôles octaves et modes coordonnées
- Factorisation de la génération des coordonnées pour éliminer la duplication de code et améliorer la maintenabilité
- Typage robuste avec `TypeAlias` pour une meilleure compatibilité mypy et fonctionnalités Python 3.13+ modernes
- Sortie professionnelle avec contrôle qualité JPEG et optimisation PNG
- Résumés traitement détaillés et validation
- Fonctionnalités Python 3.13+ modernes avec dataclasses et types union

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

# Sortie JPEG haute qualité avec qualité personnalisée
python sphere_texture_generator.py -m procedural -t earth -f JPEG -q 98 -o terre_hq.jpg

# Générer en lot toutes les textures avec palettes planétaires et marbre (512x256, PNG)
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

このスクリプトは、正距円筒図法を使用してBlenderとGodot用に最適化されたシームレス球体テクスチャを生成します。手続き的テクスチャ（地球風惑星、ガス惑星、大理石パターン）を作成するか、既存の画像を球体対応フォーマットに変換し、自動極点歪み補正、2の冪乗最適化、包括的なノイズ設定を備えています。

**機能：**

- 正距円筒図法（2:1比率）を使用してシームレス球体テクスチャを生成
- 手続き的テクスチャを作成：地球風惑星、ガス惑星、大理石パターン
- 球面座標マッピングで既存画像を球体互換フォーマットに変換
- BlenderのUVマッピングとGodotのSphereMesh用に最適化、自動互換性チェック付き
- ガウシアンブラーマスキングとピクセル統合による高度な極点補正
- 柔軟な解像度：標準プリセット（512、1K、2K、4K、8K）およびカスタム寸法
- オクターブ制御と座標モードを備えた包括的ノイズ設定
- コード重複を排除する座標生成のリファクタリングでメンテナンス性を向上
- `TypeAlias`を使用した堅牢な型ヒントにより、mypy互換性とPython 3.13+の現代的機能を向上
- JPEG品質制御とPNG最適化によるプロフェッショナル出力
- 詳細な処理サマリーと検証
- dataclassesとユニオン型を使用した現代的Python 3.13+機能

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

# カスタム品質の高品質JPEG出力
python sphere_texture_generator.py -m procedural -t earth -f JPEG -q 98 -o earth_hq.jpg

# 惑星および大理石パレットで全テクスチャをバッチ生成（512x256、PNG）
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

此脚本使用等距圆柱投影生成针对Blender和Godot优化的无缝球体纹理。创建程序化纹理（类地行星、气态巨行星、大理石图案）或将现有图像转换为球体就绪格式，具有自动极点畸变校正、2的幂优化和全面的噪声配置。

**功能：**

- 使用等距圆柱投影（2:1比例）生成无缝球体纹理
- 创建程序化纹理：类地行星、气态巨行星、大理石图案
- 通过球面坐标映射将现有图像转换为球体兼容格式
- 为Blender UV映射和Godot SphereMesh优化，带自动兼容性检查
- 使用高斯模糊遮罩和像素合并的高级极点校正
- 灵活分辨率：标准预设（512、1K、2K、4K、8K）加自定义尺寸
- 具有倍频程控制和坐标模式的全面噪声配置
- 重构坐标生成以消除代码重复，提高可维护性
- 使用`TypeAlias`的健壮类型提示，提升mypy兼容性和Python 3.13+现代功能
- JPEG质量控制和PNG优化的专业输出
- 详细的处理摘要和验证
- 具有数据类和联合类型的现代Python 3.13+功能

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

# 自定义质量的高质量JPEG输出
python sphere_texture_generator.py -m procedural -t earth -f JPEG -q 98 -o earth_hq.jpg

# 批量生成所有带有行星和大理石调色板的纹理（512x256，PNG）
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

此腳本使用等距圓柱投影生成針對Blender和Godot優化的無縫球體紋理。創建程序化紋理（類地行星、氣態巨行星、大理石圖案）或將現有圖像轉換為球體就緒格式，具有自動極點畸變校正、2的冪優化和全面的噪聲配置。

**功能：**

- 使用等距圓柱投影（2:1比例）生成無縫球體紋理
- 創建程序化紋理：類地行星、氣態巨行星、大理石圖案
- 通過球面座標映射將現有圖像轉換為球體兼容格式
- 為Blender UV映射和Godot SphereMesh優化，帶自動兼容性檢查
- 使用高斯模糊遮罩和像素合併的高級極點校正
- 靈活分辨率：標準預設（512、1K、2K、4K、8K）加自訂尺寸
- 具有倍頻程控制和座標模式的全面噪聲配置
- 重構座標生成以消除代碼重複，提高可維護性
- 使用`TypeAlias`的健壯類型提示，提升mypy兼容性和Python 3.13+現代功能
- JPEG品質控制和PNG優化的專業輸出
- 詳細的處理摘要和驗證
- 具有資料類和聯合類型的現代Python 3.13+功能

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

# 自訂品質的高品質JPEG輸出
python sphere_texture_generator.py -m procedural -t earth -f JPEG -q 98 -o earth_hq.jpg

# 批量生成所有帶有行星和大理石調色板的紋理（512x256，PNG）
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

Este script genera texturas esféricas sin costuras optimizadas para Blender y Godot usando proyección equirectangular. Crea texturas procedimentales (planetas terrestres, gigantes gaseosos, patrones de mármol) o convierte imágenes existentes a formatos listos para esferas con corrección automática de distorsión polar, optimización power-of-2, y configuración completa de ruido.

**Características:**

- Genera texturas esféricas sin costuras usando proyección equirectangular (proporción 2:1)
- Crea texturas procedimentales: planetas terrestres, gigantes gaseosos, patrones mármol
- Convierte imágenes existentes a formato compatible con esferas usando mapeo coordenadas esféricas
- Optimizado para mapeo UV Blender y SphereMesh Godot con verificaciones compatibilidad automáticas
- Corrección polar avanzada usando enmascarado difuminado gaussiano y consolidación píxeles
- Resoluciones flexibles: preajustes estándar (512, 1K, 2K, 4K, 8K) más dimensiones personalizadas
- Configuración completa de ruido con controles octavas y modos coordenadas
- Refactorización de generación de coordenadas para eliminar duplicación de código y mejorar mantenibilidad
- Tipos robustos con `TypeAlias` para mejor compatibilidad con mypy y características modernas de Python 3.13+
- Salida profesional con control calidad JPEG y optimización PNG
- Resúmenes procesamiento detallados y validación
- Características modernas Python 3.13+ con dataclasses y tipos union

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

# Salida JPEG alta calidad con calidad personalizada
python sphere_texture_generator.py -m procedural -t earth -f JPEG -q 98 -o earth_hq.jpg

# Generar en lote todas las texturas con paletas planetarias y de mármol (512x256, PNG)
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

Questo script genera texture sferiche senza giunture ottimizzate per Blender e Godot utilizzando proiezione equirettangolare. Crea texture procedurali (pianeti terrestri, giganti gassosi, pattern marmorei) o converte immagini esistenti in formati pronti per sfere con correzione automatica distorsione polare, ottimizzazione power-of-2, e configurazione completa rumore.

**Funzionalità:**

- Genera texture sferiche senza giunture utilizzando proiezione equirettangolare (rapporto 2:1)
- Crea texture procedurali: pianeti terrestri, giganti gassosi, pattern marmorei
- Converte immagini esistenti in formato compatibile sfere utilizzando mappatura coordinate sferiche
- Ottimizzato per mappatura UV Blender e SphereMesh Godot con verifiche compatibilità automatiche
- Correzione polare avanzata utilizzando mascheratura sfocatura gaussiana e consolidamento pixel
- Risoluzioni flessibili: preimpostazioni standard (512, 1K, 2K, 4K, 8K) più dimensioni personalizzate
- Configurazione completa rumore con controlli ottave e modalità coordinate
- Refactoring della generazione di coordinate per eliminare duplicazione codice e migliorare manutenibilità
- Tipi robusti con `TypeAlias` per migliore compatibilità mypy e funzionalità moderne Python 3.13+
- Output professionale con controllo qualità JPEG e ottimizzazione PNG
- Riassunti elaborazione dettagliati e validazione
- Funzionalità moderne Python 3.13+ con dataclasses e tipi union

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

# Output JPEG alta qualità con qualità personalizzata
python sphere_texture_generator.py -m procedural -t earth -f JPEG -q 98 -o earth_hq.jpg

# Generare in batch tutte le texture con palette planetarie e marmoree (512x256, PNG)
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

Dieses Skript generiert nahtlose Sphären-Texturen optimiert für Blender und Godot mit äquirektangulärer Projektion. Erstellt prozedurale Texturen (erdähnliche Planeten, Gasriesen, Marmormuster) oder konvertiert bestehende Bilder in sphärentaugliche Formate mit automatischer Polverzerrungskorrektur, Power-of-2-Optimierung und umfassender Rauschkonfiguration.

**Funktionen:**

- Generiert nahtlose Sphären-Texturen mit äquirektangulärer Projektion (2:1-Verhältnis)
- Erstellt prozedurale Texturen: erdähnliche Planeten, Gasriesen, Marmormuster
- Konvertiert bestehende Bilder in sphärenkompatibles Format mit sphärischer Koordinatenmappierung
- Optimiert für Blender UV-Mapping und Godot SphereMesh mit automatischen Kompatibilitätsprüfungen
- Erweiterte Polkorrektur mit Gaußsche Unschärfe-Maskierung und Pixelkonsolidierung
- Flexible Auflösungen: Standard-Voreinstellungen (512, 1K, 2K, 4K, 8K) plus benutzerdefinierte Dimensionen
- Umfassende Rauschkonfiguration mit Oktav-Kontrollen und Koordinatenmodi
- Refaktorisierte Koordinatengenerierung zur Beseitigung von Code-Duplikation und Verbesserung der Wartbarkeit
- Robuste Typ-Hinweise mit `TypeAlias` für bessere mypy-Kompatibilität und moderne Python 3.13+ Funktionen
- Professionelle Ausgabe mit JPEG-Qualitätskontrolle und PNG-Optimierung
- Detaillierte Verarbeitungszusammenfassungen und Validierung
- Moderne Python 3.13+ Funktionen mit Dataclasses und Union-Typen

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

# Hochqualitative JPEG-Ausgabe mit benutzerdefinierter Qualität
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
