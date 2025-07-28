import math
from PIL import Image, ImageDraw

# --- PARAMÈTRES ---
# Vous pouvez modifier ces valeurs si besoin

# Dimensions physiques
LONGUEUR_ARETE_CM = 9.0  # 9 cm pour l'arête du triangle
ECART_MM = 5.0  # 5 mm d'écart horizontal entre les colonnes

# Qualité de l'image pour l'impression (300 DPI est une bonne qualité standard)
DPI = 300

# Nombre de triangles à dessiner par ligne
NOMBRE_DE_TRIANGLES_PAR_LIGNE = 6

# Style du patron
COULEUR_FOND = "white"
COULEUR_TRAIT = "black"
EPAISSEUR_TRAIT_PX = 2  # Épaisseur du trait en pixels (2 ou 3 est bien visible)

# Nom du fichier de sortie
NOM_FICHIER_SORTIE = "patron_triangles_double.png"

# --- CALCULS DE CONVERSION ---

# 1 pouce = 2.54 cm
pouces_par_cm = 1 / 2.54

# Conversion des dimensions physiques en pixels
arete_px = (LONGUEUR_ARETE_CM * pouces_par_cm) * DPI
ecart_px = ((ECART_MM / 10) * pouces_par_cm) * DPI

# Calcul de la hauteur d'un triangle équilatéral
hauteur_px = (math.sqrt(3) / 2) * arete_px

# Marge autour du dessin (en pixels)
marge_px = 30

# --- CALCUL DE LA TAILLE DE L'IMAGE ---

# La largeur est calculée comme avant, en fonction du nombre de triangles par ligne
largeur_image = (marge_px * 2) + ((NOMBRE_DE_TRIANGLES_PAR_LIGNE - 1) * (arete_px / 2 + ecart_px)) + arete_px

# La hauteur doit maintenant accommoder DEUX rangées de triangles
hauteur_image = (marge_px * 2) + (2 * hauteur_px)

# Création de l'image vierge
image = Image.new('RGB', (int(largeur_image), int(hauteur_image)), COULEUR_FOND)
dessin = ImageDraw.Draw(image)

# --- DESSIN DES TRIANGLES ---

# Position de départ sur l'axe X
x_curseur = marge_px

# Coordonnées Y pour les 3 lignes horizontales du patron
y_ligne_haute = marge_px
y_ligne_milieu = marge_px + hauteur_px
y_ligne_basse = marge_px + (2 * hauteur_px)

print(f"Début du dessin de 2 lignes de {NOMBRE_DE_TRIANGLES_PAR_LIGNE} triangles...")

for i in range(NOMBRE_DE_TRIANGLES_PAR_LIGNE):

    # --- LIGNE 1 (HAUT) ---
    # Le premier triangle (i=0) pointe vers le bas, comme demandé
    if i % 2 == 0:  # Pointe vers le bas
        p1 = (x_curseur, y_ligne_haute)
        p2 = (x_curseur + arete_px, y_ligne_haute)
        p3 = (x_curseur + arete_px / 2, y_ligne_milieu)
    else:  # Pointe vers le haut
        p1 = (x_curseur, y_ligne_milieu)
        p2 = (x_curseur + arete_px, y_ligne_milieu)
        p3 = (x_curseur + arete_px / 2, y_ligne_haute)

    dessin.polygon([p1, p2, p3], outline=COULEUR_TRAIT, width=EPAISSEUR_TRAIT_PX)

    # --- LIGNE 2 (BAS) - EN MIROIR ---
    # Le premier triangle (i=0) pointe vers le haut (l'inverse de la ligne 1)
    if i % 2 == 0:  # Pointe vers le haut
        p1_m = (x_curseur, y_ligne_basse)
        p2_m = (x_curseur + arete_px, y_ligne_basse)
        p3_m = (x_curseur + arete_px / 2, y_ligne_milieu)
    else:  # Pointe vers le bas
        p1_m = (x_curseur, y_ligne_milieu)
        p2_m = (x_curseur + arete_px, y_ligne_milieu)
        p3_m = (x_curseur + arete_px / 2, y_ligne_basse)

    dessin.polygon([p1_m, p2_m, p3_m], outline=COULEUR_TRAIT, width=EPAISSEUR_TRAIT_PX)

    # Met à jour la position du curseur pour la prochaine COLONNE de triangles
    x_curseur += arete_px / 2 + ecart_px

    print(f"  - Colonne de triangles {i + 1} dessinée.")

# --- SAUVEGARDE DE L'IMAGE ---

image.save(NOM_FICHIER_SORTIE, dpi=(DPI, DPI))

print("-" * 20)
print(f"Patron double '{NOM_FICHIER_SORTIE}' créé avec succès !")
print(f"Ouvrez ce fichier dans Photoshop pour l'imprimer à la bonne taille.")
