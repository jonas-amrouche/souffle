Relis les modifications en cours (`git diff`, ou les derniers changements de `souffle.html`) contre les règles de conception du projet : `CLAUDE.md`, `docs/VISION.md` et la partie « Rejeté » de `docs/DECISIONS.md`.

Vérifie en particulier :
- Aucun texte d'aide, aucune légende explicative, aucune liste de raccourcis ajoutés à l'écran ; messages d'état d'un mot au plus.
- Aucun marqueur de style « vibecodé » : carte arrondie avec bordure colorée sur le côté, titres en petites capitales espacées, dégradés brillants, compteurs inutiles, emojis.
- Vocabulaire de sensation, pas de jargon (pas de noms de notes, d'accords, de cents dans l'interface).
- Déterminisme : aucun modèle d'IA, aucune dépendance au hasard non initialisé.
- Accessibilité : `aria-label`, `aria-pressed`, `prefers-reduced-motion`, thèmes clair et sombre.
- Tout tient sans défilement ; aucun bouton ne garde le focus ; `pushUndo()` avant chaque modification de données.
- Aucune idée déjà rejetée n'est réintroduite.

Liste les écarts trouvés, du plus grave au moins grave, avec une correction proposée pour chacun.

$ARGUMENTS
