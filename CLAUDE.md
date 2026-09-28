# Souffle

Station de travail musicale (DAW) où l'on compose d'abord **avec sa voix**, puis on retouche. L'objectif : que l'utilisateur apprenne la musique, pas le logiciel. Aucune théorie musicale requise, même pour atteindre les limites de l'outil.

Le porteur du projet est développeur, francophone, et fait tourner l'application **en local** (fichier HTML ouvert dans le navigateur). Toute l'interface est **en français**, et la conversation aussi.

@docs/VISION.md

## État actuel

- Tout tient dans **un seul fichier** : `souffle.html` (~7 Mo, dont ~6,9 Mo d'échantillons d'instruments encodés en base64 dans `<script id="samples" type="application/json">`).
- Aucune dépendance, aucune étape de construction, aucun modèle d'IA. Web Audio API + Canvas 2D + JavaScript simple, dans une IIFE en mode strict.
- Le code est découpé en sections repérées par des commentaires `/* ================= Titre ================= */`.

Lire selon le besoin (pas chargés automatiquement) :
- `docs/ARCHITECTURE.md` : modèle de données, moteur audio, algorithmes, format de fichier. **À lire avant de toucher au code.**
- `docs/UX.md` : toutes les interactions et tous les raccourcis.
- `docs/DECISIONS.md` : ce qui a été essayé, gardé, rejeté, et pourquoi. **À lire avant de proposer une idée d'interface**, beaucoup ont déjà été testées et écartées.
- `docs/ROADMAP.md` : prochaines étapes, limites connues, dette technique.

## Règles non négociables

1. **Déterministe.** Pas d'apprentissage automatique pour l'analyse (le porteur l'a explicitement refusé : il veut un outil qu'on apprend à maîtriser, qui se comporte toujours pareil). Traitement du signal classique uniquement : YIN, énergie, enveloppes, rugosité psychoacoustique, etc.
2. **Pas de tutoriel nécessaire.** Pas de textes d'aide, de légendes explicatives, de listes de raccourcis en bas d'écran. Les seuls textes admis : la description d'une note parmi ses voisines (dans l'inspecteur), les raccourcis affichés sur les boutons (`<kbd>`), les infobulles `title`. Messages d'état : un mot ou rien.
3. **Pas de « style vibecodé ».** Proscrits : cartes arrondies avec bordure colorée sur le côté, titres en petites capitales espacées, dégradés brillants avec reflet, pastilles partout, compteurs inutiles, emojis. Préférer des lignes, des filets, des aplats sobres.
4. **Vocabulaire de sensation, pas de jargon.** « rond / mordant », « sec / ample », « proche / lointain », « se fond / frotte ». Jamais de noms de notes, d'accords, de gammes, de « cents » dans l'interface (les Hz ne sont montrés que dans l'inspecteur d'une note).
5. **Tout s'entend en contexte.** Une note n'est jamais montrée ou jouée comme si elle était seule quand on juge une relation.
6. **Station de travail, pas démo.** Tout tient dans un écran sans défilement (au-dessus de 1000 px de large), zones bien séparées, raccourcis clavier partout, aucun bouton ne garde le focus après un clic de souris.
7. **Accessibilité** : `aria-label` sur les boutons-icônes, `aria-pressed` sur les bascules, respect de `prefers-reduced-motion`, thèmes clair et sombre via des variables CSS sur `:root`.

## Façon de travailler

- Avant d'écrire, relire la section concernée de `souffle.html` : beaucoup de fonctions sont couplées (sélection, relations, lecture à chaud).
- Après toute modification : vérifier la syntaxe du script principal et **tester dans un vrai navigateur**, voir `tests/smoke.py` (Playwright, micro factice). Commande `/test`.
- Tout changement de données doit passer par `pushUndo()` avant la modification, puis `refresh()` après (qui recalcule les relations, redessine les panneaux et met à jour la lecture en cours via `livePatch()`).
- Tout changement d'interface doit être revu contre les règles ci-dessus. Commande `/design-review`.
- En fin de session, mettre à jour `docs/DECISIONS.md` et `docs/ROADMAP.md`. Commande `/session-end`.
- Commentaires de code en français, courts, qui disent le *pourquoi*.

## Lancer

Ouvrir `souffle.html` dans Firefox, Chrome ou Edge. **Le porteur utilise Firefox** : penser à ses différences (pas d'« Enregistrer sous » natif, tableaux `getChannelData` vidés quand un tampon est joué ; voir les pièges dans `docs/ARCHITECTURE.md`). Cliquer « Commencer », autoriser le micro, mettre un casque. La bibliothèque de sons télécharge depuis `raw.githubusercontent.com` : elle ne marche qu'en local ou servie par un serveur, pas dans un bac à sable qui bloque le réseau.
