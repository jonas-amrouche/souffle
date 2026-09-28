Lance les tests de fumée dans un vrai navigateur, puis corrige ce qui casse.

1. Vérifie la syntaxe du script principal :
   `python3 -c "import re;s=open('souffle.html').read();open('/tmp/souffle.js','w').write(re.findall(r'<script>(.*?)</script>',s,re.S)[-1])" && node --check /tmp/souffle.js`
2. Lance `python3 tests/smoke.py` (Playwright ; si besoin : `pip install playwright && python3 -m playwright install chromium`).
3. Si un test échoue, trouve la cause dans `souffle.html` (pas dans le test, sauf si l'interface a légitimement changé), corrige, relance.
4. Résume en une ou deux phrases ce qui a été vérifié et ce qui a été corrigé.

$ARGUMENTS
