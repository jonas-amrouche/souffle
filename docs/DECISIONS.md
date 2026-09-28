# Journal des décisions

Chaque idée d'interface a été testée par le porteur du projet. Ne pas réintroduire ce qui a été rejeté sans en discuter.

## Gardé

- **Voix → notes nettes**, avec l'expression vocale réinjectable (`expr`). Au début, tout sonnait « chanté » (souffle, micro-variations) : les notes sont devenues des objets propres, retouchables.
- **Analyse de type Melodyne** (centre de note, dérive, vibrato, transitions) plutôt que correction trame par trame : la gravité par trame faisait basculer le vibrato entre deux notes.
- **Accordage : Grille (12, calée sur le morceau) / Aimants (relationnel) / Libre.** Sans grille, il fallait l'oreille absolue. La grille n'est jamais imposée ; le calage suit le morceau.
- **Caler le temps (A) et caler les hauteurs (H)** : deux actions séparées, à force réglable (Maj = à moitié).
- **Pulsation globale** en BPM, mais fixée intuitivement (Taper, Déduire le BPM). Grille à 4 divisions par temps par défaut.
- **Friction = bord rouge.** Compris immédiatement.
- **Ancrage = saturation de la couleur** (vive / grisée).
- **Clic droit maintenu = accord** de toutes les notes de la fenêtre, **avec les vrais instruments** ; la molette élargit la fenêtre. Motivation : une mélodie est souvent un accord décomposé dans le temps.
- **Bibliothèque en carte à axes fixes et nommés** (sombre ↔ brillant, court ↔ long) plutôt qu'un regroupement automatique qui bouge à chaque ajout.
- **Bibliothèque** (c'est son nom) **en surimpression, ouverte et fermée par D, en fondu rapide** (Tab essayé : ne marche pas comme raccourci dans le navigateur du porteur) : fond sombre à demi transparent sur tout l'écran, panneau à marges lui aussi sombre et à demi transparent, le tout sous une **vignette rectangulaire** qui suit les bords de l'écran, de transparent aux bords jusqu'à l'opacité voulue, sans aucun bord net (le fond du panneau s'efface aussi ; une ellipse allongée et un panneau à bord net ont été rejetés) ; pas de fond coloré derrière les points ; navigable (molette = zoom, clic molette = déplacer) ; commandes en haut ; volume d'écoute réglable ; bouton dans l'îlot central de la barre du haut ; un clic sur le fond la ferme. Pendant qu'on emporte un son, elle devient presque invisible, puis réapparaît. Essayé avant : tiroir sous le morceau, colonne à gauche, panneau sous les couches (trop petits), panneau opaque avec fond coloré. Pas de carte de sélection ni de bouton « Instrument » : on glisse le son sur la liste.
- **Un son posé garde sa hauteur exacte** : le morceau est un seul espace où chaque son est à sa fréquence (on voit le spectre de la composition). Essayé puis rejeté : le transposer jusqu'à la hauteur du pointeur. **Tout son a une hauteur** : s'il n'en a pas de nette (frappe, bruit), c'est sa résonance la plus forte entre 40 et 1400 Hz (grosse caisse ≈ 50 Hz, caisse claire ≈ 170 Hz, cymbale ≈ 850 Hz). Rejeté : les poser à la hauteur du pointeur (pas de lien avec le son). Une moyenne du spectre (centroïde) a été écartée : c'est la brillance, souvent hors de la plage du morceau, et on ne l'entend pas comme une hauteur. L'aperçu en pointillés est exactement la prise à venir.
- **Plus de pied de page** : le message d'état (un mot) est dans la barre du haut, à côté du nom.
- **Couleur des sons = leur place sur la carte, en 2D** sur toute la roue des couleurs (teinte autour du centre, clarté selon la brillance) : repère mnémotechnique, « ce type de 808 est de cette couleur ». Rejeté : arc-en-ciel 1D selon la durée. Une couche ou un instrument créé depuis un son en prend la couleur.
- **Instruments en liste simple** (plus de familles en pastilles). Un son glissé de la bibliothèque sur la liste devient un instrument choisissable.
- **Type de couche : Instrument / Audio, en icônes** (trois notes en escalier / onde), sur les lignes de couches et dans le panneau. « Audio » = prises de voix brutes et sons posés tels quels.
- **Supprimer une couche = corbeille** (la petite croix était trop discrète).
- **Écoute brute dans la bibliothèque** : aucun traitement au survol, on juge le son tel qu'il est.
- **Panneaux ajustables** par des poignées discrètes (filet au survol), tailles mémorisées.
- **Maj + glisser = dupliquer** une note (ou la sélection) et placer la copie.
- **Curseurs à petite prise** (piste fine) partout ; sur les couches, le vumètre est sous le curseur, séparé.
- **Le placement (pan) suit le curseur en direct** pendant la lecture, sans la relancer.
- **Placement stéréo par note** (pas par couche : le nœud de panoramique par couche existe mais reste à 0).
- **Orbe** comme bouton central, qui respire avec la voix.
- **Couches en lignes** (pas de cartes).
- **Prises sonores entrant dans les relations** par leurs hauteurs stables.
- **Instruments échantillonnés** (Musyng Kite) : la synthèse maison était trop grossière.
- **Station de travail** : tout sur un écran, panneaux séparés, icônes pour les actions de fichier et d'historique.

## Rejeté (et pourquoi)

- **Modèles d'IA pour l'analyse** : non déterministes, frustrants quand ils échouent, sentiment d'être déconnecté de son art.
- **Déclencher des sons à la voix / kit à la voix / créer un son en l'imitant** : gadget, et la voix est continue alors que déclencher est discret.
- **Réglage de teinte** : simple habillage.
- **Vagues animées pour la friction** : lues comme un vibrato.
- **Notes pleines / creuses pour l'ancrage** : lues comme de l'intensité.
- **Hz en axe vertical** : lecture technique ; seulement dans l'inspecteur.
- **Lecture automatique au clic sur une note** : gênant. Clic silencieux ; on écoute avec le clic droit ou Ctrl + Espace.
- **Double-clic pour créer une note** : remplacé par le clic droit dans le vide.
- **Sons neutres (sinusoïdes) pour écouter les relations** : déroutant, on veut entendre son morceau.
- **Orbe avec dégradé brillant et reflet**, trop grand : jugé laid.
- **Icônes micro / bouton d'enregistrement classique** : l'orbe doit être « le moyen de faire », pas une fonction parmi d'autres.
- **Libellés vagues** (« Déduire », « Caler ») : maintenant « Déduire le BPM », « Caler le temps », « Caler les hauteurs ».
- **Marqueurs de style « vibecodé »** : cartes arrondies à bord coloré, titres en petites capitales espacées, explications partout, compteurs de notes, légende et liste de raccourcis en bas.
- **Mettre instruments et réglages de note dans le même panneau** : séparés en deux.
- **Placement stéréo par couche** : le porteur le voulait par note.
- **Kit** (un son par ligne de grille, joué au clavier) : retiré. Les anciens morceaux sont convertis en couches Audio.
- **Kit / voix mélangés dans une prise** : en mode clavier, la prise n'écoute que le clavier.

## Interprétations à confirmer

- « Chaque ligne de clavier = une note de la grille » a été compris comme : chaque **touche** est un cran, les rangées se suivent (pas de logique touches blanches / noires).
- « Réenregistrer sur la couche » = punch-in (remplace dans la zone chantée, garde le reste).
- Hauteur de repli (résonance la plus forte) pour les sons sans hauteur nette : à valider à l'oreille par le porteur.
- Un son glissé sur la liste d'instruments y est seulement ajouté, pas appliqué à la couche choisie ; « Audio » comme nom de type : non contesté, pas explicitement validé.
