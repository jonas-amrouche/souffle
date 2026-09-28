# Vision et piliers de conception

## L'intuition de départ

Beaucoup de gens ont une musicalité réelle (sens du rythme, oreille, capacité à fredonner une mélodie) mais ne peuvent pas créer, parce que les outils imposent soit la mémoire musculaire d'un instrument, soit des DAW techniques où l'on cherche des sons par leurs noms et où l'on crée « à tâtons » au lieu de se diriger vers une vision.

Le problème de fond : les outils représentent la musique du point de vue de sa **fabrication** (hauteur, grille, nom de fichier) et non de sa **perception** (tension, fusion, couleur, attente). Les musiciens autodidactes ont intériorisé la structure par l'oreille ; l'outil doit rendre cette intuition visible au lieu d'exiger de la théorie.

Le porteur du projet chante bien, ne joue pas d'instrument (et ne veut pas être limité à un timbre ou à un accordage), a essayé les DAW et Strudel (rapide mais enfermé dans les motifs qui se répètent).

## La phrase qui résume tout

> Ce qu'on apprend doit être la musique, pas le logiciel.

Critère pour chaque fonctionnalité : **est-ce qu'elle demande de comprendre le logiciel, ou seulement d'écouter ?** Si un réglage a besoin d'une explication, c'est le réglage qui est mal conçu.

Liberté et maîtrise : « la liberté seule, dans un monde dont on ne maîtrise pas les codes, c'est être enfermé. » 80 % des utilisateurs doivent arriver dans un monde qu'ils maîtrisent déjà, parce que ses moyens d'expression (la voix, le geste, les mots de sensation) sont ceux qu'ils utilisent déjà.

## Piliers

1. **La voix comme interface principale.** C'est l'instrument que presque tout le monde maîtrise. Elle sert à créer des notes, des prises sonores, et elle est au centre de l'interface (l'orbe). Mais on ne fait pas de « transcription gadget » : la voix crée des notes **nettes** qu'on peut ensuite retoucher, avec une expression vocale dosable.
2. **Performer, puis éditer.** La boucle de travail est : chanter (ou jouer au clavier), puis reprendre. Les deux doivent être excellents. La reprise en particulier : caler le temps, caler les hauteurs, couper, copier, déplacer, sans friction.
3. **La musique est relationnelle et temporelle.** Une note ne sonne qu'en fonction de ses voisines. L'interface le montre sans le dire : chaque note affiche sa relation au reste (fusion ou friction avec ce qui sonne en même temps, ancrage dans le morceau), et quand on déplace une note, on voit et on entend où elle se fondrait ou frotterait.
4. **Voir comment ça sonne, pas ce que c'est.** La hauteur et le volume ne disent pas si ça sonne bien. On calcule des modèles partiels de l'écoute (rugosité de Plomp-Levelt / Sethares, ancrage par densité de hauteurs) et on les rend visibles. L'oreille reste le juge final ; le visuel guide l'écoute.
5. **Déterministe.** Traitement du signal classique, jamais de modèle d'IA pour l'analyse : un comportement qu'on apprend et qui ne surprend pas.
6. **Vocabulaire de sensation.** Mots que tout le monde possède (proche, lointain, rond, mordant, se fond, frotte), paires d'opposés, verbes plutôt que noms. Le jargon peut exister caché, jamais requis.
7. **Profondeur progressive.** Niveau 1 : on chante, c'est déjà beau. Niveau 2 : on choisit à l'oreille. Niveau 3 : on modèle avec des mots de sensation. Niveau 4 : réglages fins. Personne n'est obligé de descendre.
8. **Pas de page blanche.** Le morceau commence avec un fond grave tenu : il est plus facile de chanter *avec* quelque chose.
9. **Station de travail agréable.** Un outil où l'on a envie de passer du temps : zones rangées, tout accessible sans défilement, raccourcis partout, utilisable en direct.

## Ce qu'il faut éviter (pour ne pas redevenir un DAW classique)

- Chaînes d'effets à dizaines de paramètres techniques (préférer 2-3 réglages perceptifs par couche : espace, écho, distance).
- Courbes d'automation dessinées à la souris (préférer enregistrer un geste, comme une performance).
- Tables de mixage avec égaliseurs à bandes et vumètres partout.
- Édition de paramètres MIDI note par note.
- Tout ce qui demande d'apprendre le logiciel plutôt que la musique.

## La question de fond (discutée)

La musique n'a jamais été « décrite » autrement que comme recette (partition) ou comme physique (spectrogramme), parce que son sens est relationnel, temporel et se passe dans l'auditeur. Une description complète est impossible, mais on dispose aujourd'hui de modèles partiels de l'écoute (rugosité, fusion, attente) : on peut dessiner non pas ce qu'il faut jouer, mais ce qu'un auditeur ressentira probablement. Le visuel ne remplace pas l'écoute, il la guide.
