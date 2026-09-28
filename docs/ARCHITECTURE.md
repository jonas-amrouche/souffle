# Architecture technique

## Vue d'ensemble

`souffle.html` = CSS + HTML + deux balises `<script>` :
1. `<script id="samples" type="application/json">` : 231 échantillons MP3 mono 56 kbit/s en base64, un toutes les 3 demi-tons, 15 instruments de la banque **Musyng Kite** (CC BY-SA 3.0, via `gleitz/midi-js-soundfonts`). Régénérable avec `tools/fetch_instruments.py`.
2. Le script principal (~2300 lignes), une IIFE `'use strict'`. Pas de variables globales exposées (les tests passent par le DOM et les pixels des canvas, pas par l'état interne).

Disposition : grille CSS à 5 colonnes (couches, poignée, centre, poignée, réglages), chaque zone placée explicitement (`grid-area`). La bibliothèque (`#lib`) est hors grille, en `position:fixed` sur toute la fenêtre, au-dessus de tout : fond à demi transparent, panneau `.libpane` à marges, l'ensemble masqué par deux dégradés linéaires croisés (`mask-composite: intersect`) ; ouverture par la classe `open` (fondu d'opacité, `visibility` coupée après) ; tailles en variables CSS (`--w-l`, `--w-r` sur `.app`, `--h-sel` sur `#rcol`) posées par `applySizes()` et gardées dans `localStorage` (`souffle.sizes2`, lecture et écriture sous try/catch).

Toute l'application tourne sur un seul `AudioContext` (`S.ctx`), un canvas pour le morceau (`#score`) et un canvas pour la bibliothèque (`#libCanvas`). Boucle `tick()` sur `requestAnimationFrame` : analyse du micro, niveau de l'orbe, vumètres des couches, dessin.

## Sections du script (dans l'ordre)

Temps (pulsation) → Analyse du micro → De la voix aux notes (`analyzeFrames`) → Relations → Son (sortie, synthé, échantillons, prises sonores) → Enregistrement → Annuler/rétablir → Transposition des prises (WSOLA) → Couper au curseur → Retour en direct → Sauvegarder/ouvrir/exporter → Couches et sélection → Opérations d'édition → Pulsation (taper, déduire) → Vue (dessin) → Souris → Clavier → Panneaux → Démarrage → Bibliothèque de sons → Jouer au clavier → initialisation.

## État global `S` (extraits importants)

| Champ | Rôle |
|---|---|
| `ctx, an, tbuf, fbuf, lbuf` | contexte audio, analyseur du micro et tampons |
| `frames` | trames d'analyse du micro `{id, t (temps ctx), f (Hz ou 0), a (RMS), l (0..1 au-dessus du bruit), v (actif), o (attaque)}`, ~60/s |
| `layers` | les couches (voir plus bas) |
| `lsel` (Set), `active` | couches choisies (éditables), couche active |
| `sel` (Set), `focus` | éléments choisis (ids de notes et de prises), élément principal |
| `cur` | réglages de la « nouvelle couche » `{inst, x, y, expr, fx}` |
| `tune` | accordage des hauteurs : `'grid'` / `'mag'` (aimants) / `'free'` |
| `gridOff` | décalage de la grille de hauteur (cents), déduit du morceau |
| `tg` | grille du temps `{on, bpm, beats (par mesure), div (divisions par temps, défaut 4), off (phase, s)}` |
| `loop, loopOn` | zone de boucle `{a, b}` en secondes |
| `playing` | lecture en cours `{t0, from, until, rec, loop, only, hs[], segs[]}` : `segs` = passages `{t0 (ctx), a, b (morceau)}` |
| `rec` | prise en cours `{t0, comp, from, audio, keys, pl, target}` |
| `audio` | sons du morceau : `id → {buf (AudioBuffer mono), trace, name, sh (cache de transpositions)}` |
| `lg` | chaînes audio par couche (`layerGain`) |
| `undo, redo` | instantanés JSON (100 max) |
| `lib, keys, keyOn, keyRec` | bibliothèque et mode clavier |

## Modèle de données

**Hauteurs** : toujours en **cents relatifs au la 440** (`c`), convertis par `hz(c)` et `cents(f)`. Plage affichée : 40 Hz à 1400 Hz (`C_LO`, `C_HI`).

**Couche** :
```js
{ id, kind: 'notes' | 'audio', inst, name?, hue,
  x, y,            // matière : rond→mordant, sec/pur→ample/soufflé (0..1)
  expr,            // expression vocale réinjectée : 0 nette → 1 chantée
  gain, fx: { space, echo, dist }, mute, solo, hidden, fond?,
  notes: [], clips: [], alts: null | [[...]], take,   // prises multiples (boucle)
  sample?, base?,  // si inst === 'smp' : son de la bibliothèque joué comme instrument, base = hauteur d'origine (cents)
                   // (aussi dans S.cur ; la liste de ces instruments est S.uinst = [{ id, aid, base, col, name }])
}
// les anciens morceaux peuvent contenir des couches kind 'kit' (slots : ligne → son) : à l'ouverture, chaque coup devient une prise sonore d'une couche Audio
```
`inst` ∈ `INST` : piano, epiano, orgue, guitare, basse, violon, violoncelle, cordes, flute, clarinette, trompette, choeur, nappe, synth, marimba, vibraphone, audio (prise brute), smp (échantillon). `fam: null` = pas proposé dans la liste des instruments (audio, smp).

**Note** : `{ id, t, d, c, v (intensité 0..1), pan?, det? [[dt, cents]], dyn? [[dt, gain]] }`. `det`/`dyn` = courbes de la voix d'origine, réinjectées selon `expr`. Champs calculés non sauvegardés : `_fr` (friction), `_h` (ancrage).

**Prise sonore** (clip) : `{ id, t, off (décalage dans le son), d, buf (id dans S.audio), pitch? (cents, transposition), at? (cents : hauteur d'une prise sans hauteur nette, sa résonance ; prioritaire sur la trace dans `clipBox`), pan? }`.

**Trace** d'un son (pour le dessin et les relations) : `[{ t, c | null, l }]` à 60 points/s, calculée par `traceOf()` (YIN à 16 kHz).

## Chaîne audio

Sortie (`buildOutput`) : `bus → (dry, convolver) → compresseur → destination`. Réverbération par réponse impulsionnelle synthétique déterministe (bruit à graine fixe).

Par couche (`layerGain`) : `entrée (volume, muet, solo) → passe-bas (distance) → panoramique (0) → analyseur (vumètre)` puis `dry`, envoi réverbération (`space`), écho calé sur la pulsation (0,75 temps, avec contre-réaction filtrée). Persistante pour la session : volume, muet, solo et effets s'appliquent pendant la lecture.

Par note :
- `sampleNote` : échantillon le plus proche, `playbackRate` pour la hauteur ; passe-bas (dépend de l'intensité et de la matière), étagère aiguë, mélange propre/saturé (`WaveShaper`), panoramique par note, envoi réverbération (« ample »). Sons tenus (`kind: 'sus'`) : boucle de la partie stable (1,0 à 3,0 s) en fondus croisés de 0,25 s. Renvoie une poignée `{L, kill, release, retune, matter, pan}` : `matter()` applique la matière **en temps réel**.
- `contNote` : synthé (3 oscillateurs, filtre, souffle), même poignée.
- `clipPlay` : prise sonore (tampon transposé si `pitch`). Poignée `{kill, pan}`. `scheduleRange` note l'id de l'élément sur chaque poignée (`h.id`) : le curseur de placement agit ainsi en direct sur ce qui sonne.

Lecture (`playRange(from, until, {rec, loop, only})`) : programme des passages ; en boucle, une pompe (`setTimeout` 200 ms) ajoute le passage suivant 0,8 s avant la fin. `livePatch()` reprogramme depuis la position courante quand le morceau change pendant la lecture.

## Algorithmes (tous déterministes)

**Hauteur en direct** : YIN (fenêtre 1024, seuil 0,15, interpolation parabolique), médiane sur 3 trames, suivi du plancher de bruit (min qui remonte lentement), niveau `l` relatif à ce plancher, attaque = hausse de `l` > 0,2 sur 4 trames.

**De la voix aux notes** (`analyzeFrames`) : 1) lissage ~180 ms (médiane 5 + moyenne glissante ±90 ms) qui annule le vibrato ; 2) découpage par hystérésis (seuil `35 + 105×sens` cents pendant 45 ms), coupures aux attaques ; 3) fusion des fragments trop courts ou trop proches (0,7 × seuil) ; 4) frontière au croisement du milieu entre deux notes ; 5) centre = médiane de la partie stable (25 à 85 %) ; 6) reconstruction : centre corrigé + dérive + vibrato + transitions lissées. `framesToNotes` l'utilise sans correction, puis `placeNotes` pose chaque note selon l'accordage.

**Relations** :
- Friction : rugosité de Plomp-Levelt / Sethares entre les 6 premiers harmoniques (amplitude 1/n) de la note et de tout ce qui sonne en même temps (pondéré par recouvrement et intensité) ; `fric = 1 - exp(-D/0,35)`.
- Ancrage : densité (noyau gaussien σ ≈ 25 cents, à l'octave près) des hauteurs du morceau pondérées par durée × intensité, normalisée par le maximum (`hMax`).
- Paysage d'une note : `coût = friction - 0,6 × ancrage` pour chaque hauteur ; aimants = minima locaux. Les prises sonores y participent par leurs hauteurs stables (`clipNotes`).

**Grille de hauteur** : tempérament égal 12, décalage = moyenne circulaire (modulo 100 cents) des hauteurs du morceau pondérées par durée × intensité. Au départ, le fond (110 Hz) aligne la grille sur le la 440.

**Pulsation** : « Déduire » teste 50 à 200 bpm par pas de 0,25 ; score = |Σ v·e^(2πi t/T)| + 0,5 × |Σ à T/2|, pondéré par un a priori log-normal autour de 100 bpm ; la phase donne le calage. « Taper » : moyenne des intervalles.

**Alignement d'une prise brute** : corrélation croisée normalisée entre l'enveloppe RMS du son capturé (100 Hz) et l'amplitude mesurée en direct, décalage ±0,4 s. Capture par `ScriptProcessorNode` (4096).

**Compensation de latence** : notes chantées décalées de `baseLatency + outputLatency + 1024/sr + 8 ms` ; touches du clavier de `baseLatency + outputLatency`.

**Transposition des prises** : WSOLA (fenêtre 1024, pas 512, recherche ±256) puis rééchantillonnage : la hauteur change, la durée reste identique. Mis en cache par transposition.

**Bibliothèque** : enveloppe RMS 10 ms ; durée = jusqu'à 3 % du pic ; brillance = `sr/2π × √(E[Δx²]/E[x²])` (estimation du centroïde sans FFT) ; hauteur nette = même analyse que le morceau (`traceOf` sur les 3 premières secondes) : le son a une hauteur si au moins un quart des trames audibles en ont une (60 à 1150 Hz), c'est alors leur médiane (et la hauteur d'origine s'il devient instrument). Ainsi un son rond dans la bibliothèque montre toujours sa trace dans le morceau. Hauteur de repli (`domPitch`), pour un son sans hauteur nette : spectre moyen (FFT 8192, pas de 4096, fenêtre de Hann, 2 premières secondes, énergie cumulée), pic local le plus fort entre 40 et 1400 Hz, interpolation parabolique sur le logarithme ; `feat.clear` dit si la hauteur est nette (rond) ou de repli (carré). Carte : x = log(brillance) de 60 Hz à 12 kHz, y = log(durée) de 0,04 à 6 s. La couleur reste calculée de (durée, brillance) comme avant l'échange des axes. Vue zoomable `S.libZ = {k, u, v}` (zoom 1 à 60, coin bas-gauche visible en coordonnées de carte). Couleur d'un son = sa place (`libRGB`, en OKLab : la teinte tourne autour du centre de la carte, la saturation croît en s'en éloignant, la clarté suit la brillance), donnée aux couches créées depuis ce son et aux instruments de la liste. Rond = son avec une hauteur, carré = sans. L'écoute au survol (`libPreview`) va directement à `ctx.destination`, sans réverbération ni compresseur, au volume `S.libVol` (réglé dans la bibliothèque, gardé dans `localStorage`). Au départ, seuls les trois premiers sons de chaque dossier de la source sont téléchargés et analysés ; « Tout charger » met les autres en file (6 à la fois). Dépôt sur le morceau : `libPlace()` calcule la prise (temps au pointeur, hauteur = celle du son, sans transposition ; `at` = hauteur de repli pour un son sans hauteur nette) ; l'aperçu pendant le glisser est `clipBox()` de cette même prise. Une erreur de dépôt est signalée (« Son illisible ») et détaillée dans la console.

## Format de fichier `.souffle`

JSON : `{ app:'souffle', version:1, tg, tune, loop, loopOn, metro, cur, layers, uinst, audio: { id: { sr, pcm (int16 mono base64), name } }, ids: { nid, lid, aid } }`. Les traces sont recalculées à l'ouverture. Export audio : rendu hors temps réel (`OfflineAudioContext`, 44,1 kHz stéréo) en WAV 16 bits.

## Pièges connus

- Les fonctions ne sont pas toutes « pures » : `recomputeRel()` doit suivre tout changement de hauteur/durée ; `refresh()` le fait.
- `renderLayers()` reconstruit le DOM à chaque clic : un double-clic natif ne survit pas (le renommage détecte le double-clic à la main).
- Les poignées de notes gardent une référence à l'objet couche ; après `restore()` (annuler), `livePatch()` relance la lecture.
- Les `AudioBuffer` sont partagés entre le contexte temps réel et le contexte d'export ; les `PeriodicWave` et chaînes de couches sont recréées pour l'export.
- **Données d'un `AudioBuffer`** : ne jamais garder un tableau obtenu par `getChannelData` au-delà de l'instant. Quand le tampon est joué, Firefox (conformément à la norme, « acquire the content ») vide ces tableaux. La bibliothèque gardait `it.mono` ainsi : les sons mono déjà écoutés au survol ne pouvaient plus être posés. `monoOf()` renvoie donc toujours une copie.
- `file://` interdit les modules ES : si on découpe le code, il faut soit une étape d'assemblage, soit un petit serveur local.
