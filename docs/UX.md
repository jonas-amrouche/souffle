# Interface, interactions et raccourcis

## Disposition (au-dessus de 1000 px, sans défilement)

- **Barre du haut** : nom à gauche ; au centre : retour en direct (casque), mode clavier, **l'orbe** (enregistrer, universel), lecture/stop, temps, tempo (− bpm +), Taper, métronome ; à droite : ouvrir, enregistrer, exporter, annuler, rétablir (icônes).
- **Colonne gauche** : les couches, en lignes (pastille de couleur, icône du type — trois notes en escalier = Instrument, onde = Audio —, nom, S / M / masquer, corbeille au survol, volume puis vumètre juste en dessous ; en tête, « Nouvelle couche · instrument » = aucune couche choisie). Le nom d'une couche est celui de son instrument, ou « Audio » ; le type n'est plus écrit, l'icône le dit.
- **Centre** : barre d'outils (Hauteur : Grille / Aimants / Libre, Caler les hauteurs ; Temps : Grille, Déduire le BPM, découpage, Boucle, Couper au curseur, Caler le temps), puis le morceau (canvas).
- **Bibliothèque** (D, ou le bouton à points dans l'îlot central de la barre du haut) : apparaît et disparaît en fondu rapide, au-dessus de tout, barre du haut comprise. Un fond sombre à demi transparent couvre tout l'écran ; par-dessus, avec des marges, un panneau sombre lui aussi à demi transparent porte les sons (des points, à la couleur de leur place ; pas de fond coloré). L'ensemble s'efface en vignette rectangulaire vers les bords de l'écran ; le fond du panneau s'efface lui aussi vers ses côtés (aucun bord net). Commandes en haut du panneau : titre, filtre, source (bouton lien : champ de source + Charger), « Tout charger » tant qu'il reste des sons non chargés, volume de l'écoute. Le chargement se voit comme un filet au-dessus de la carte. On en sort par D, Échap, ou un clic sur le fond autour du panneau. Dès qu'on emporte un son, elle devient presque invisible (son nom suit le pointeur, un cadre en pointillés montre exactement où tombera la prise) ; au lâcher, elle réapparaît.
- **Tous les panneaux s'ajustent** : poignées entre les colonnes et entre les deux panneaux de droite, un filet apparaît au survol. Double-clic : taille d'origine ; au clavier, flèches (Maj : pas plus grand). Tailles gardées d'une séance à l'autre (stockage du navigateur). Le morceau garde toujours au moins 320 px.
- **Colonne droite, deux panneaux** : en haut la couche (type en icônes : Instrument / Audio, choisi pour une nouvelle couche, affiché pour une couche existante ; liste simple des instruments sur deux colonnes, puis les instruments venus de la bibliothèque, avec leur couleur ; matière, expression, registre, effets, prises) ; en bas la sélection (relation de la note, fusion, ancrage, intensité, placement, écouter, supprimer).

## L'orbe

Bouton principal, plus grand que les autres mais dans la barre. Couleur pleine rose-violet sans reflet. Icône = 5 petites barres qui suivent le niveau du micro en permanence (points au repos). Rouge et pulsation douce pendant une prise. **Universel** : enregistre la voix, ou le clavier si le mode clavier est actif (jamais les deux dans la même prise, pour éviter que le bruit des touches devienne des notes).

## Lire une note

- Épaisseur = intensité.
- Couleur vive = « chez elle » dans le morceau ; grisée = loin de ses hauteurs habituelles.
- Bord rouge (plus épais si plus fort) = frotte avec ce qui sonne en même temps.
- Note choisie : cadre clair. Quand une seule note est choisie, sa colonne montre le paysage : vert = s'y fondrait, rouge = frotterait ; repères à gauche = crans de la grille (colorés) ou aimants.
- Notes des couches non choisies : estompées (pelure d'oignon), non éditables.
- Bandes d'octave discrètes calées sur la hauteur « chez soi ».

## Prises sonores

Cadre aux bornes de la prise ; trait = hauteur quand il y en a une ; grains = texture sans hauteur ; bande d'intensité en bas du cadre = tout ce qui sonne. Déplacer, rogner par les bords, transposer en glissant verticalement.

## Souris

| Geste | Effet |
|---|---|
| Clic sur une note | la choisir (silencieux) |
| Maj / Ctrl + clic | ajouter ou retirer de la sélection |
| Maj + glisser une note | la dupliquer et placer la copie (toute la sélection si la note en fait partie) ; Maj + clic sans bouger = ajouter / retirer |
| Glisser une note | déplacer la sélection (temps et hauteur, accrochés selon les modes ; on entend la note et ses voisines) |
| Glisser le bord droit | durée |
| Alt pendant un glisser | sans accrochage |
| Glisser dans le vide | lasso |
| Alt + clic ou Alt + lasso | choisir des notes de n'importe quelle couche (et leurs couches) |
| Clic droit dans le vide | ajouter une note |
| Clic droit maintenu sur une note | toutes les notes de sa fenêtre sonnent ensemble, tenues, avec leurs vrais instruments (couches choisies seulement) ; la molette élargit ou resserre la fenêtre |
| Règle : clic ou glisser | curseur, totalement libre |
| Règle : clic droit glissé | définir la boucle (bords accrochés à la grille ; Alt = libre) ; sur un bord : le déplacer ; clic droit simple : activer/couper |
| Molette | défiler dans le temps |
| Ctrl + molette | zoom horizontal (pas de zoom vertical) |
| Clic molette maintenu | faire glisser le morceau |
| Placement (panneau Sélection) | suit le curseur en direct pendant la lecture |
| Couches : clic sur le nom | choisir (Ctrl/Maj : plusieurs) ; double-clic : renommer |
| Couches : pastille | clic = couleur suivante, glisser = réordonner |
| Bibliothèque : molette | zoom autour du pointeur |
| Bibliothèque : clic molette maintenu, ou glisser dans le vide de la carte | se déplacer dans la carte ; double-clic dans le vide : tout voir ; clic sur le fond autour du panneau : fermer |
| Bibliothèque : glisser un son sur la liste des instruments | il devient un instrument de la liste (joué à toutes les hauteurs) ; la liste reste visible pendant le glisser, même si une couche Audio est choisie ; croix au survol pour le retirer |
| Bibliothèque : survol | écouter le son brut (sans réverbération ni compresseur) ; clic = choisir ; glisser vers le morceau = poser au pointeur dans le temps, **à sa hauteur exacte** (le morceau est un seul espace de fréquences) ; un son sans hauteur nette (frappe, bruit) est posé à sa résonance la plus forte ; sur la couche Audio choisie, sinon une nouvelle ; le cadre en pointillés montre exactement la prise à venir |
| Déposer des fichiers/dossiers sur la bibliothèque | les ajouter |

## Clavier

| Touche | Effet |
|---|---|
| Espace | lecture / stop (en boucle si la boucle est active) |
| Entrée | enregistrer / terminer |
| Ctrl + Espace | jouer seulement la sélection |
| Ctrl + Z, Ctrl + Maj + Z, Ctrl + Y | annuler, rétablir |
| Ctrl + A / C / X / V / D | tout choisir, copier, couper, coller au curseur, dupliquer après |
| Ctrl + S (Maj : sous un autre nom), Ctrl + O, Ctrl + E | enregistrer, ouvrir, exporter en WAV |
| Suppr / Retour arrière | supprimer la sélection |
| D | ouvrir / fermer la bibliothèque (pas en mode clavier : D y joue une note) |
| Échap | fermer la bibliothèque si elle est ouverte, sinon tout désélectionner |
| ↑ ↓ | hauteur suivante (cran de grille, aimant, ou 10 cents en libre) ; Maj ou Ctrl : octave ; Alt : 5 cents |
| ← → | déplacer d'une division ; Maj : durée ; Ctrl : une mesure ; Alt : 50 ms |
| A (Maj + A) | caler le temps (à moitié) |
| H (Maj + H) | caler les hauteurs (à moitié) |
| S | couper au curseur |
| R | retour en direct |
| L | boucle |
| T | taper le tempo |
| F | tout voir |
| Début | curseur au début |
| ² ou ` | mode clavier : les touches jouent des notes (les raccourcis en lettres sont alors désactivés) |

Mode clavier : chaque touche = un cran de la grille, dans l'ordre physique (codes `KeyZ…Slash`, puis `KeyA…Quote`, `KeyQ…BracketRight`, `Digit1…Equal`), à partir d'un do grave. Indépendant de la disposition (AZERTY / QWERTY), car basé sur `event.code`.

## Comportements à préserver

- Aucun bouton ne garde le focus après un clic de souris (sinon Espace/Entrée le réactivent). Les listes et curseurs se désactivent après usage.
- Sélection de texte désactivée dans l'application (sauf champs de saisie).
- Une prise avec une couche choisie réenregistre **sur cette couche** (punch-in : remplace ce qui commençait dans la zone chantée). Sans couche choisie : nouvelle couche.
- En boucle, chaque passage devient une prise ; on choisit la meilleure dans le panneau de la couche.
- Après une prise, toutes ses notes sont choisies (prêtes pour A ou H).
- La lecture suit les modifications en direct.
