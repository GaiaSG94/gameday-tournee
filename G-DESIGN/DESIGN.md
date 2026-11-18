# DESIGN — Tournée (journal)

> Journal des versions. Jamais écrasé : chaque version s'ajoute en dessous de la précédente.

## V1 — 2026-11-18 · 3 directions pour la page Jeu (en revue)

Compris du produit : un puzzle quotidien de tournée de livraison. Six arrêts sur un plan 8 × 8, un dépôt ; le joueur touche les arrêts dans l'ordre, la tournée (retour au dépôt compris) est comparée à la plus courte possible. Même tournée pour tous chaque jour, série si la tournée est parfaite.

Données de démo : la vraie tournée du **2026-11-18** générée par `src/shared/puzzle.ts` (Post 1,5 · Florist 4,0 · Library 6,1 · Atelier 4,2 · Bakery 1,0 · School 2,4 ; optimum 22 blocs). État dessiné : 4 arrêts placés (Bakery, Florist, Library, Atelier), 10 blocs parcourus, Send route verrouillé à 4/6.

Planches (`planches/v1/`), générées par `tools/design/build_planches_v1.py` pour garantir des données identiques :

| # | Direction | Palette | Typo | Motif |
|---|-----------|---------|------|-------|
| 01 | **Carte pliée** (direction de départ) | carte `#f1eada`, route `#3a6ea5`, arrêt/accent `#c8322b`, encre `#23303d` | sans de signalétique (marque en panneau), mono pour l'horloge et les distances | plan papier plié en six, tracé bleu au feutre |
| 02 | **Calque d'architecte** | calque `#fbfaf6`, encre unique `#c8322b`, texte `#2a2422` | grotesque fine, mono pour les cotes | filets, cotes de distance sur chaque tronçon, cartouche |
| 03 | **Dispatch de nuit** (écart) | asphalte `#121417`, îlot `#1c2025`, sodium/accent `#f2b33d` | sans neutre, mono dominant | îlots en tuiles, tournée allumée en jaune sodium, arrêts codés |

Notes :
- Polices : piles système dans les planches (aucune requête réseau). La police définitive sera embarquée dans l'app (CSP), à choisir sous licence libre au moment de `STYLE.md`.
- Questions produit ouvertes : voir `PAGES.md` (créneaux horaires absents du code, classement communautaire, nombre d'envois par jour).

Décision : en attente de la validation de Gaia.

**Retour de Gaia (2026-11-18)** : V1 rejetée, « trop slop IA ». Repartir de zéro, s'appuyer franchement sur les designs des refs, design de narratif jeu.

## V2 — 2026-11-18 · repartie de zéro, 3 directions ancrées dans les refs (en revue)

Ce qui faisait « slop » en V1 et a été retiré : légendes de nuancier et cartes de notes sur la planche, badges et pastilles arrondis génériques, composants de template (liste + deux boutons pilule), aucune idée empruntée aux refs au-delà de la couleur.

Méthode : refs réouvertes en profondeur (pages internes de PART, scroll complet de Baseten) ; chaque direction part d'une **mécanique** de ref, pas d'une palette. Récit commun : le van quitte le dépôt à 06:00, chaque bloc vaut 3 minutes, donc chaque livraison a une heure (06:03 Bakery, 06:12 Florist…). Mêmes données de démo qu'en V1 (tournée réelle du 2026-11-18, 4/6 arrêts placés, 10 blocs).

Planches (`planches/v2/`, générées par `tools/design/build_planches_v2.py`) :

| # | Direction | Ref | Principe | Palette | Typo |
|---|-----------|-----|----------|---------|------|
| A | **Maquette** | Baseten | ville en tuiles isométriques pastel, arrêts = petits immeubles extrudés qui passent au cobalt et portent leur numéro sur leur face ; étiquettes en pixels 5 × 5 ; journal de bord horodaté dans un panneau blanc découpé sur un fond pointillé | pastels + encre `#111` + accent cobalt `#1f5cff` | grotesque + mono |
| B | **Salle** | PART | le post est une pièce dessinée au filet (plafond tramé, murs, sol) ; la ville est au sol en perspective ; mur du fond = titre en lettres construites + récit + blocs parcourus ; infos de partie à la verticale sur les murs | encre unique `#e2432e` sur blanc | lettres construites (dessin maison, traits orthogonaux et 45°) + grotesque + mono |
| C | **Feuilleton** | Baseten + récit | ville en tuiles plates vue de haut, la tournée s'imprime case par case en noir ; arrêts = icônes pixel sur leur pastel ; la matinée s'écrit ligne par ligne et finit sur la question du moment (« School or Post first? ») | noir `#111` + un pastel par arrêt | grotesque grasse + mono |

À noter :
- L'horaire narratif (06:00 + 3 min par bloc) et les icônes d'arrêt sont des **propositions** : ce sont des habillages des distances existantes, pas de nouvelles règles. À valider (voir `PAGES.md`, question 1).
- Les lettres construites de B sont un dessin original (grille 4 × 6), pas la police de PART.

Décision (2026-11-18, Gaia) : **A · Maquette validée** pour la page Jeu. B et C abandonnées. Suite : `STYLE.md` puis déclinaison des pages restantes.

## V3 — 2026-11-18 · style verrouillé, déclinaison des 4 pages

**/lock demandé par Gaia** juste après la validation de A : fin des explorations. Le brief prévoit `/lock` une fois toutes les pages validées ; ici le style est verrouillé d'abord, et les pages 1, 3 et 4 restent **en revue** dans ce style.

- `STYLE.md` rédigé : palette (encre `#111`, cobalt `#1f5cff` seul accent, pastels réservés aux îlots), typo (Inter + JetBrains Mono à embarquer), grille, maquette iso, icônes pixel, composants, mouvement, états.
- Planches `planches/v3/`, générées par `tools/design/build_planches_v3.py`, qui réutilise tel quel le rendu de V2 · A :
  - `01-post.html` : vue feed. Maquette du jour sans tracé, panneau Round (colis, départ, chauffeurs du jour, série), bouton « Start the round ».
  - `02-jeu.html` : page validée, identique à V2 · A.
  - `03-fin.html` : tournée parfaite bouclée (22 blocs, retour 07:06), score 100 %, veille, série 7, part de chauffeurs, citation de partage sans spoiler, « Comment your round », compte à rebours.
  - `04-series.html` : calendrier iso de 4 semaines (hauteur = score), classement du jour (score puis horloge), répartition en barres de pixels.
- Données communautaires (chauffeurs du jour, %, rang, pseudos) = démo, à brancher côté serveur (voir `PAGES.md`, question 5).

Validation (2026-11-18, Gaia) : **les 4 pages sont validées** (Post, Jeu, Carte de fin, Séries & classement). Le design V3 est figé ; le verrou de style vaut désormais pour un jeu de pages complet. Restent ouvertes les questions produit de `PAGES.md` (créneaux horaires, horaire narratif, données communautaires côté serveur).
