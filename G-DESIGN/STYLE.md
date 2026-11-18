# STYLE — Tournée · « Maquette »

> **Style verrouillé le 2026-11-18 (/lock, Gaia).** Direction V2 · A. Plus d'exploration : toute nouvelle planche suit ce document.
> Référence d'implémentation : `tools/design/build_planches_v3.py` (rendu iso, glyphes pixel, composants), planches `planches/v3/`.

## 1. Idée

La ville du jour est une **maquette isométrique** posée sur une table pointillée. Chaque arrêt est un petit immeuble ; livré, il passe au cobalt et porte son numéro sur sa face. Tout le texte vit dans des **panneaux blancs à filet noir** qui mordent sur la maquette. La partie se raconte comme un **journal de bord horodaté** (départ 06:00, 3 minutes par bloc).

Ancrage : Baseten (champ de tuiles iso pastel, blocs porteurs de données, icônes pixel 5 × 5, boutons noirs ▸). Voir `REFS.md`.

## 2. Palette

| Rôle | Hex | Usage |
|------|-----|-------|
| Encre | `#111111` | texte, filets de panneaux, bouton primaire, dépôt |
| Fond table | `#fafaf7` + points `#d9dad4` (1 px, pas 9 px) | fond du post |
| Panneau | `#ffffff` | tous les blocs de texte |
| Filet secondaire | `#d6d8d2` | séparateurs de lignes |
| Texte secondaire | `#7b7d78` | libellés, heures passées |
| **Accent cobalt** | `#1f5cff` | **seule couleur saturée** : arrêts livrés, route, dernier arrêt, score, série, « vous » |
| Cobalt faces | dessus `#6f95ff` · gauche `#1f5cff` · droite `#1746c9` · arête `#0b2a86` | immeubles livrés |
| Fond accent léger | `#eef3ff` | ligne active (« Tap your next stop », votre rang) |
| Pastels d'îlots | `#e4f2df` `#ece7f8` `#e0eaf8` `#f7eadb` `#f1f1ec` | tuiles de ville uniquement, jamais d'UI |
| Faces d'îlots | dessus = pastel · gauche × 0.93 · droite × 0.86 · arête `#c5cbc2` | |
| Désactivé | fond `#ecece7` · texte `#9b9d96` | Send route avant 6/6 |

Règle : les pastels **catégorisent** (îlots, puces d'arrêt dans le journal), le cobalt **signale**. Aucun dégradé, aucune ombre portée.

## 3. Typographie

- **Grotesque** (titres, texte) : Inter (OFL), à embarquer dans l'app ; les planches utilisent Helvetica Neue / Arial en substitut.
- **Mono** (heures, chiffres, distances, scores) : JetBrains Mono (OFL), à embarquer ; substitut `ui-monospace`.

| Rôle | Police | Taille / graisse |
|------|--------|------------------|
| Marque « Tournée » | grotesque | 17 / 600, précédée du van pixel 18 px |
| Lede (phrase de récit) | grotesque | 13 / 400, gras 600 pour l'accroche |
| Libellés (SHIFT LOG, ROUND…) | grotesque | 10 / 400, capitales, interlettrage .1em, gris |
| Lignes de panneau | grotesque | 13 / 400–600 |
| Heures, distances, valeurs | mono | 12–13 / 500–600 |
| Chiffres héros (blocs, horloge) | mono | 16–22 / 600 |
| Score de fin | mono | 44 / 600 cobalt (36 sur mobile) |
| Étiquettes de maquette | grotesque | capitales 600, équivalent ~11 px |

## 4. Grille et cadre

- Post desktop : zone de jeu 740 px de large, marges 18 px. Deux colonnes : maquette (≈ 450 px) + panneau 252 px, le panneau descend de 42 px pour mordre sur la maquette.
- Post mobile : 390 px, marges 12 px, une colonne : en-tête, lede, maquette pleine largeur, panneau. **Tout le jeu tient dans le viewport** sans défilement interne.
- Panneaux : filet 1 px `#111`, angles droits, aucun arrondi. En-tête + lede sont collés (le lede n'a pas de filet haut).
- Lignes de panneau : 32 px desktop, 26–27 px mobile.

## 5. Maquette isométrique

- Projection 2:1 : `X = x − y`, `Y = (x + y) / 2 − z`. Grille 8 × 8 d'intersections, 7 × 7 îlots.
- Îlots : joint de 0.13, hauteurs 0 / .12 / .22 / .36 (pseudo-aléatoire stable par case), teintes pastel.
- Route : polyligne cobalt 0.14 sur gaine blanche 0.30, angles arrondis, suit les rues (horizontal puis vertical).
- Arrêt à livrer : prisme blanc 0.48 × 0.48, hauteur 1.05, arête noire.
- Arrêt livré : même prisme en cobalt, numéro d'ordre en mono blanc sur la face droite.
- Dernier arrêt posé : losange pointillé cobalt au sol (c'est celui qu'Undo retire).
- Dépôt : prisme noir bas (0.55).
- Étiquettes : rectangle blanc à filet noir, icône pixel + nom en capitales, reliées au sommet de l'immeuble par un trait de 1 px. Côté et hauteur fixés par arrêt pour éviter les chevauchements (à calculer automatiquement en prod : gauche si `X < 0`).
- Calendrier de série : même projection, 7 colonnes × 4 semaines ; hauteur = score (100 % = 0.62, cobalt) ; jour manqué = tuile plate pointillée ; jours futurs = tuile plate claire.

## 6. Icônes pixel 5 × 5

Dessinées sur grille 5 × 5, une couleur, `shape-rendering: crispEdges`. Jeu actuel : van, house (dépôt), bread (Bakery), flower (Florist), book (Library), needle (Atelier), mail (Post), bell (School). Chaque nouveau type d'arrêt reçoit sa propre icône dans la même grille.
Dans le journal : icône noire sur la puce pastel de l'arrêt (22 px). Sur la maquette : noire si à livrer, cobalt si livré.

## 7. Composants

| Composant | Règle |
|-----------|-------|
| En-tête | barre blanche à filet : marque à gauche, cases horloge / série à droite (valeur mono + libellé capitales). Série en cobalt quand elle vient d'augmenter. |
| Lede | une phrase de récit, jamais d'instruction technique. |
| Journal de bord | `heure · puce · arrêt · +blocs`. Ligne active fond `#eef3ff`, texte cobalt. Lignes futures : heure `--:--`, puce vide pointillée. |
| Ligne clé / valeur | libellé gris à gauche, valeur mono à droite. |
| Bouton primaire | noir plein, texte blanc 600, chevron ▸ à droite, angles droits, hauteur 44. |
| Bouton secondaire | blanc, séparé du primaire par un filet vertical, même hauteur. |
| Barres de répartition | 20 carrés (1 = 5 %), noirs ; la ligne 100 % en cobalt. |
| Citation de partage | encadré pointillé mono : `Tournée · date · blocs · % · horloge`. Ne révèle jamais l'ordre. |

## 8. Mouvement

- Toucher un arrêt : l'immeuble « monte » (hauteur 0 → 1.05, 180 ms, ease-out) puis passe au cobalt ; la route s'allonge du tronçon (trait qui se dessine, 220 ms).
- Undo : animation inverse, 140 ms.
- Envoi parfait : les six immeubles clignent une fois en cascade dans l'ordre de livraison (60 ms d'écart), puis le score compte de 0 à 100.
- Pas de rebond, pas de particules, pas de confettis.

## 9. États

| État | Rendu |
|------|-------|
| Chargement | maquette vide (îlots seuls) + lede « Loading the van… » ; panneau en lignes grises. |
| Erreur | lede en encre : message court + bouton secondaire « Try again ». |
| Déjà joué aujourd'hui | le post ouvre directement la carte de fin (lecture seule) avec le compte à rebours. |
| Envoi verrouillé | Send route désactivé tant que < 6/6, le compteur reste visible. |
| Tournée non parfaite | score en encre (pas cobalt), ligne « Best possible » mise en avant, série remise à 0 en gris. |
