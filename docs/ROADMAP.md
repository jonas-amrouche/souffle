# Feuille de route

## Dette technique (à traiter tôt)

1. **Découper `souffle.html`.** 2300 lignes de script + 6,9 Mo d'échantillons dans un seul fichier. Proposition : `src/*.js` (une section = un fichier) + `samples/` (fichiers MP3), et un petit script d'assemblage sans dépendance qui produit `dist/souffle.html` autonome. Attention : `file://` interdit les modules ES ; soit on assemble, soit on sert en local (`python -m http.server`). Garder un livrable en un seul fichier, qui fonctionne en double-cliquant.
2. **Remplacer `ScriptProcessorNode`** (obsolète) par un `AudioWorklet` pour la capture brute, et y déplacer l'analyse YIN : latence du retour en direct plus faible (aujourd'hui ~50-80 ms).
3. **Stéréo** : les prises et les sons de la bibliothèque passent en mono (analyse, transposition, sauvegarde). Garder la stéréo pour la lecture.
4. **Tests** : `tests/smoke.py` couvre les parcours principaux (dont bibliothèque, Maj + glisser, poignées, types de couche) ; **le porteur utilise Firefox** : ajouter un passage Firefox (Playwright Firefox ne démarre pas sur le poste de développement actuel : « spawn UNKNOWN ») ; ajouter des tests unitaires des algorithmes (analyse voix → notes, rugosité, WSOLA, déduction du tempo), faciles en Node une fois le code découpé.

## Pilier pas encore construit : le temps relationnel

La friction et l'ancrage ne regardent que la **verticale** (ce qui sonne en même temps). Il manque la dimension temporelle, discutée dès le début :
- surprise / attente d'une note selon ce qui précède (modèle statistique déterministe appris sur le morceau lui-même, dans l'esprit d'IDyOM) ;
- tension au fil du temps (« rubans de tension » de Herremans et Chew) ;
- une note qui « attend » une résolution pourrait pencher visuellement vers là où elle veut aller.

## Prochaines fonctions demandées ou proposées

- **Bibliothèque v2** : hauteur de repli à affiner (bornée à 40-1400 Hz : les sons très aigus, charlestons, s'alignent en haut) ; chargement de toute la source en tâche de fond plutôt que « Tout charger » ; recherche en imitant un son à la voix (plus proche voisin sur les descripteurs, pour pointer dans la carte, pas pour créer un son) ; navigation par dossiers ; favoris ; analyse en tâche de fond plus fine.
- **Composer une prise à partir de plusieurs** (garder la mesure 1 de la prise 2 et la mesure 2 de la prise 4).
- **Effets** : rester perceptif (espace, écho, distance existent). Pistes : « chaleur », « flou », « grain ». Pas de chaîne de plugins.
- **Automation par geste** : enregistrer un mouvement du pad de matière ou de la voix pendant la lecture, plutôt que dessiner des courbes.
- **Clavier** : changer d'octave ; entrée MIDI.
- **Placement stéréo** : le montrer visuellement sur les notes.
- **Exports** : pistes séparées.
- **Zoom vertical** : explicitement refusé pour l'instant.

## Limites connues

- Pas de sauvegarde automatique (Ctrl + S uniquement).
- Après une prise, la lecture repart d'elle-même : le premier Espace l'arrête au lieu de la lancer (comportement existant, à confirmer avec le porteur).
- Au départ, la bibliothèque ne charge que les trois premiers sons de chaque dossier de la source (« Tout charger » pour le reste).
- **Ctrl + O** : certains Chromium refusent d'ouvrir le sélecteur de fichier depuis ce raccourci (c'est aussi le raccourci d'ouverture du navigateur, et il n'est pas toujours compté comme geste de l'utilisateur). Le bouton « Ouvrir » fonctionne toujours. À vérifier dans le Firefox du porteur ; piste : un `<input type="file">` permanent dans la page, ou `showOpenFilePicker` quand il existe.
- `showSaveFilePicker` absent sous Firefox : téléchargement classique à la place.
- Dans la page publiée sur claude.ai (bac à sable), la bibliothèque ne peut pas télécharger depuis GitHub ; en local, pas de problème.
- Quatre fichiers de la banque Strudel ne se décodent pas (ignorés).
- Le mode Aimants en direct utilise la grille (simplification).
