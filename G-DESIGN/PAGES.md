# PAGES — Tournée

> Statuts : à dessiner / en revue / validée. **Style verrouillé le 2026-11-18 (/lock) : « Maquette » (V2 · A), voir `STYLE.md`.**
> Chaque planche montre le jeu dans son cadre : desktop 1440 × 900 et mobile 390 × 844 côte à côte (§6 du brief).

| # | Page | Rôle | Contenu clé | Statut |
|---|------|------|-------------|--------|
| 1 | **Post** | Vue dans le feed (splash inline) : donner envie d'ouvrir la tournée du jour | En-tête du post, date de la tournée, aperçu du plan (6 arrêts, sans tracé), série du joueur, bouton « Start the round » | **validée** · `planches/v3/01-post.html` |
| 2 | **Jeu** | Écran principal, une seule règle : « Visit all 6 stops, back to the depot. Shortest round wins. » | Plan 8 × 8, dépôt, 6 arrêts nommés, tracé en cours, manifeste (ordre, tronçon, cumul), horloge, série, Undo, Send route (verrouillé avant 6/6) | **validée** · `planches/v3/02-jeu.html` (= V2 · A) |
| 3 | **Carte de fin** | Résultat + boucle quotidienne + accroche commentaire | Score en % de l'optimum, longueur jouée vs meilleure possible, temps, série, bouton commenter (sans spoiler), prochaine tournée dans HH:MM | **validée** · `planches/v3/03-fin.html` |
| 4 | **Séries & classement** | Montrer la communauté et la série | Série perso, classement du jour (score puis temps), répartition des scores de la communauté | **validée** · `planches/v3/04-series.html` |

États transverses à dessiner dans la déclinaison : chargement (« Loading the van… » existe déjà), erreur, partie déjà jouée aujourd'hui.

## Questions produit ouvertes (non tranchées)

0. **Horaire narratif (V2).** Les planches V2 racontent la tournée : départ du dépôt à 06:00, 3 minutes par bloc, donc une heure par livraison. C'est un habillage des distances, sans nouvelle règle. À garder ? Il pourrait aussi devenir la base des créneaux horaires de la question 1.

1. **Créneaux horaires.** `IDEE.md` annonce « distances et créneaux horaires », mais le jeu actuel (`src/shared/puzzle.ts`) n'a que des distances de Manhattan sur une grille 8 × 8, sans créneaux. Les planches dessinent **le jeu tel qu'il existe** (distances seules, horloge de partie en mono). Faut-il ajouter des créneaux (ex. « Bakery 08:00–08:30 ») ? Si oui, ils iraient dans le manifeste et en étiquette sur la carte.
2. **Classement communautaire.** (Dessiné en page 4 avec des pseudos de démo.) `IDEE.md` parle de « community scores » mais le serveur ne stocke aujourd'hui que la série par joueur. La page 4 suppose un classement du jour (score puis temps) : à confirmer.
3. **Après l'envoi** : un seul envoi par jour (comme aujourd'hui côté serveur ?) ou des essais multiples avec meilleur score retenu ? La carte de fin en dépend.
4. **« Beat yesterday's score »** (`IDEE.md`) : faut-il afficher le score de la veille sur la carte de fin ?

5. **Données communautaires dessinées mais absentes du serveur** : nombre de chauffeurs du jour, % ayant trouvé l'optimum, rang, meilleure série, score de la veille. Les planches les montrent ; il faut les stocker (Redis) pour les afficher.
