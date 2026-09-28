"""Tests de fumée de Souffle dans un vrai navigateur (Playwright + Chromium, micro factice).

Usage :
    pip install playwright && python3 -m playwright install chromium
    python3 tests/smoke.py                # parcours principaux
    python3 tests/smoke.py --lib          # + bibliothèque (réseau vers raw.githubusercontent.com requis)

Variable d'environnement facultative : CHROMIUM_PATH (chemin d'un Chromium déjà installé).
Le micro factice de Chromium émet un bip intermittent : il produit des notes, ce qui suffit à tester les prises.
L'état interne de l'application n'est pas exposé : on passe par le DOM et par les pixels des canvas.
"""
import asyncio, os, sys, pathlib, tempfile, wave, math, struct
from playwright.async_api import async_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGE = (ROOT / 'souffle.html').as_uri()
failures = []
FIND_DOT = '''() => { const c = document.querySelector('#libCanvas'), g = c.getContext('2d'), d = devicePixelRatio || 1;
    const im = g.getImageData(0, 0, c.width, c.height).data, top = document.querySelector('.libtop').getBoundingClientRect().bottom*d + 24*d;
    for (let y = Math.round(top); y < c.height*0.87; y += 2) for (let x = Math.round(c.width*0.16); x < c.width*0.84; x += 2){
      const o = (y*c.width + x)*4; if (im[o+3] > 200 && Math.max(im[o], im[o+1], im[o+2]) > 150) return [x/d, y/d]; }
    return null; }'''

def make_wav(path, f=220, dur=1.5, sr=22050):
    with wave.open(str(path), 'wb') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
        w.writeframes(b''.join(struct.pack('<h', int(12000*math.sin(2*math.pi*f*i/sr)*min(1, (sr*dur - i)/(sr*0.2)))) for i in range(int(sr*dur))))

def check(cond, label):
    print(('  ok   ' if cond else '  ÉCHEC ') + label)
    if not cond: failures.append(label)

async def main(with_lib):
    async with async_playwright() as p:
        kw = {'args': ['--use-fake-ui-for-media-stream', '--use-fake-device-for-media-stream', '--autoplay-policy=no-user-gesture-required']}
        if os.environ.get('CHROMIUM_PATH'): kw['executable_path'] = os.environ['CHROMIUM_PATH']
        b = await p.chromium.launch(**kw)
        ctx = await b.new_context(viewport={'width': 1440, 'height': 860}, accept_downloads=True)
        pg = await ctx.new_page()
        await pg.add_init_script("delete window.showSaveFilePicker; delete window.showOpenFilePicker;")
        errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        tracks = lambda: pg.locator('.track .tname .tn').all_text_contents()
        play = lambda: pg.get_attribute('#playBtn', 'aria-label')

        await pg.goto(PAGE)
        await pg.click('#startBtn'); await pg.wait_for_timeout(2000)
        check(not await pg.is_visible('#gate'), 'le voile de démarrage disparaît')
        check(not await pg.evaluate('document.documentElement.scrollHeight > innerHeight'), 'aucun défilement de page')

        # prise à la voix
        await pg.click('#recBtn'); await pg.wait_for_timeout(2800); await pg.click('#recBtn'); await pg.wait_for_timeout(900)
        t = await tracks()
        check(len(t) == 2, f'une prise crée une couche ({t})')
        await pg.keyboard.press('Space'); await pg.wait_for_timeout(100); await pg.keyboard.press('Space'); await pg.wait_for_timeout(300)
        check('Arrêter' in (await play() or ''), "Espace lance la lecture après un clic sur l'orbe (pas de focus résiduel)")
        await pg.keyboard.press('Space')

        # édition
        sb = await pg.locator('#score').bounding_box()
        await pg.mouse.click(sb['x'] + sb['width'] * 0.6, sb['y'] + sb['height'] * 0.4, button='right'); await pg.wait_for_timeout(200)
        check('Sélection · 1' in (await pg.text_content('#selTitle')), 'clic droit dans le vide ajoute une note choisie')
        check(await pg.is_visible('#noteMeter'), 'les jauges fusion / ancrage sont visibles')
        await pg.keyboard.press('a'); await pg.keyboard.press('h'); await pg.keyboard.press('ArrowUp'); await pg.keyboard.press('Control+ArrowUp')
        await pg.keyboard.press('Control+a'); await pg.keyboard.press('Control+c'); await pg.keyboard.press('Control+d'); await pg.wait_for_timeout(150)
        await pg.keyboard.press('Control+z'); await pg.wait_for_timeout(150)
        check(await pg.is_enabled('#redoBtn'), 'annuler puis rétablir disponible')

        # accord au clic droit maintenu
        await pg.mouse.move(sb['x'] + sb['width'] * 0.6 + 3, sb['y'] + sb['height'] * 0.4)
        await pg.mouse.down(button='right'); await pg.wait_for_timeout(300); await pg.mouse.up(button='right')

        # Maj + glisser une note : la duplique
        async def count_all():
            await pg.keyboard.press('Control+a'); await pg.wait_for_timeout(100)
            t = await pg.text_content('#selTitle'); await pg.keyboard.press('Escape')
            return int(t.split('·')[1]) if '·' in t else 0
        nx, ny = sb['x'] + sb['width'] * 0.85, sb['y'] + sb['height'] * 0.25
        await pg.mouse.click(nx, ny, button='right'); await pg.wait_for_timeout(200)
        n0 = await count_all()
        await pg.keyboard.down('Shift'); await pg.mouse.move(nx + 10, ny); await pg.mouse.down()
        await pg.mouse.move(nx + 130, ny - 40, steps=6); await pg.mouse.up(); await pg.keyboard.up('Shift'); await pg.wait_for_timeout(150)
        check(await count_all() == n0 + 1, 'Maj + glisser duplique la note')

        # panneaux ajustables
        lay = pg.locator('aside[aria-label="Couches"]')
        w0 = (await lay.bounding_box())['width']; gb = await pg.locator('.gut[data-k="l"]').bounding_box()
        await pg.mouse.move(gb['x'] + 4, gb['y'] + 200); await pg.mouse.down(); await pg.mouse.move(gb['x'] + 64, gb['y'] + 200, steps=4); await pg.mouse.up()
        check(abs((await lay.bounding_box())['width'] - w0 - 60) < 3, 'la poignée élargit la colonne des couches')
        h0 = (await pg.locator('aside[aria-label="Sélection"]').bounding_box())['height']; gh = await pg.locator('.gut[data-k="sel"]').bounding_box()
        await pg.mouse.move(gh['x'] + 60, gh['y'] + 4); await pg.mouse.down(); await pg.mouse.move(gh['x'] + 60, gh['y'] - 36, steps=4); await pg.mouse.up()
        check(abs((await pg.locator('aside[aria-label="Sélection"]').bounding_box())['height'] - h0 - 40) < 3, 'la poignée agrandit le panneau de sélection')

        # type de couche et liste d'instruments
        await pg.click('.tnext'); await pg.wait_for_timeout(100)
        await pg.click('#typeSeg [data-type="audio"]')
        check(not await pg.is_visible('#insts'), "type Audio : pas de liste d'instruments")
        await pg.click('#typeSeg [data-type="notes"]')
        await pg.click('#insts .iname:has-text("Marimba")')
        check('Marimba' in (await pg.text_content('.tnext')), "la liste choisit l'instrument de la prochaine couche")
        await pg.keyboard.press('d'); await pg.wait_for_timeout(300)
        check(await pg.is_visible('#libCanvas'), 'D ouvre la bibliothèque')
        lb = await pg.locator('#libCanvas').bounding_box()
        ob = await pg.locator('#lib').bounding_box()
        check(ob['width'] >= 1440 and ob['y'] == 0, 'la bibliothèque passe au-dessus de tout')
        check(abs((await pg.locator('#score').bounding_box())['y'] - sb['y']) < 1, "la bibliothèque ne déplace rien sous elle")
        await pg.mouse.move(lb['x'] + lb['width']/2, lb['y'] + lb['height']/2); await pg.mouse.wheel(0, -400); await pg.wait_for_timeout(100)
        await pg.mouse.down(button='middle'); await pg.mouse.move(lb['x'] + lb['width']/2 + 30, lb['y'] + lb['height']/2 + 20, steps=3); await pg.mouse.up(button='middle')
        await pg.keyboard.press('d'); await pg.wait_for_timeout(300)
        check(not await pg.is_visible('#libCanvas'), 'D referme la bibliothèque')
        await pg.click('#libBtn'); await pg.wait_for_timeout(300)
        await pg.mouse.click(20, 430); await pg.wait_for_timeout(300)
        check(not await pg.is_visible('#libCanvas'), 'un clic sur le fond autour du panneau ferme la bibliothèque')
        check(not await pg.evaluate('document.documentElement.scrollHeight > innerHeight'), 'toujours aucun défilement')
        sb = await pg.locator('#score').bounding_box()

        # boucle : clic droit glissé sur la règle
        await pg.mouse.move(sb['x'] + 80, sb['y'] + 12); await pg.mouse.down(button='right')
        await pg.mouse.move(sb['x'] + 380, sb['y'] + 12, steps=5); await pg.mouse.up(button='right')
        check(await pg.get_attribute('#loopBtn', 'aria-pressed') == 'true', 'clic droit glissé sur la règle crée une boucle')
        await pg.keyboard.press('l')

        # mode clavier sur la couche choisie
        await pg.click('#keysBtn'); await pg.keyboard.press('Enter'); await pg.wait_for_timeout(500)
        for k in ['z', 'x', 'c']:
            await pg.keyboard.down(k); await pg.wait_for_timeout(120); await pg.keyboard.up(k); await pg.wait_for_timeout(120)
        await pg.keyboard.press('Enter'); await pg.wait_for_timeout(600); await pg.click('#keysBtn')

        # importer ses propres sons : une bibliothèque « Mes sons », filtrable
        tmp = pathlib.Path(tempfile.mkdtemp()); make_wav(tmp / 'la grave.wav', f=1800)
        await pg.set_input_files('#libFileIn', str(tmp / 'la grave.wav')); await pg.wait_for_timeout(300)
        sets = lambda: pg.locator('#libSets .lsn').all_text_contents()
        check('Mes sons' in await sets(), f'importer un son crée la bibliothèque « Mes sons » ({await sets()})')
        await pg.keyboard.press('d'); await pg.wait_for_timeout(200)
        mine = pg.locator('#libSets .lsn', has_text='Mes sons')
        await mine.click(); await mine.click(); await pg.wait_for_timeout(200)
        pressed = lambda: pg.evaluate("[...document.querySelectorAll('#libSets .lsn')].map(b => b.textContent + ':' + b.getAttribute('aria-pressed'))")
        check(await pressed() == ['Mes sons:true'] or all(x.endswith(':false') for x in (await pressed()) if not x.startswith('Mes sons')), f'double-clic : seulement cette bibliothèque ({await pressed()})')
        dot = None
        for _ in range(20):
            await pg.wait_for_timeout(300); dot = await pg.evaluate(FIND_DOT)
            if dot: break
        check(dot is not None, 'le son importé apparaît sur la carte')
        await pg.wait_for_timeout(500); await mine.click(); await pg.wait_for_timeout(200)
        check(await pg.evaluate(FIND_DOT) is None, 'cacher la bibliothèque cache ses sons')
        await mine.click(); await pg.wait_for_timeout(200)
        await pg.keyboard.press('Escape'); await pg.wait_for_timeout(200)
        lw = (await pg.locator('aside[aria-label="Couches"]').bounding_box())['width']

        # fichiers
        async with pg.expect_download() as d1: await pg.keyboard.press('Control+s')
        saved = await (await d1.value).path()
        check(os.path.getsize(saved) > 1000, 'Ctrl+S enregistre un fichier .souffle')
        async with pg.expect_download(timeout=60000) as d2: await pg.keyboard.press('Control+e')
        wav = await (await d2.value).path()
        check(open(wav, 'rb').read(4) == b'RIFF', 'Ctrl+E exporte un WAV')
        before = await tracks()
        await pg.reload(); await pg.click('#startBtn'); await pg.wait_for_timeout(1200)
        # Ctrl+O peut être refusé comme geste utilisateur par certains Chromium (voir docs/ROADMAP.md) : on passe par le bouton
        async with pg.expect_file_chooser() as fc: await pg.click('#openBtn')
        await (await fc.value).set_files(saved); await pg.wait_for_timeout(1200)
        check(await tracks() == before, f'Ouvrir restitue les mêmes couches ({before})')
        # le morceau garde aussi les bibliothèques, leurs sons importés et la disposition, même sur un autre poste
        await pg.evaluate('localStorage.clear()'); await pg.reload(); await pg.click('#startBtn'); await pg.wait_for_timeout(1200)
        async with pg.expect_file_chooser() as fc: await pg.click('#openBtn')
        await (await fc.value).set_files(saved); await pg.wait_for_timeout(1500)
        check(abs((await pg.locator('aside[aria-label="Couches"]').bounding_box())['width'] - lw) < 3, 'Ouvrir restitue la largeur des panneaux')
        check('Mes sons:true' in await pressed(), f'Ouvrir restitue les bibliothèques et leur filtre ({await pressed()})')
        await pg.keyboard.press('d'); dot = None
        for _ in range(20):
            await pg.wait_for_timeout(300); dot = await pg.evaluate(FIND_DOT)
            if dot: break
        check(dot is not None, 'les sons importés voyagent dans le fichier du morceau')
        await pg.keyboard.press('Escape')

        if with_lib:
            await pg.keyboard.press('d'); await pg.wait_for_timeout(300)
            # attendre que des sons soient analysés : des points bien lumineux apparaissent sur la carte
            find_dot = FIND_DOT
            dot = None
            for _ in range(60):
                await pg.wait_for_timeout(1000)
                dot = await pg.evaluate(find_dot)
                if dot: break
            check(dot is not None, 'la bibliothèque charge et analyse des sons')
            if dot:
                lb = await pg.locator('#libCanvas').bounding_box()
                dot = await pg.evaluate(find_dot)
                n0 = await pg.locator('#insts .idel').count()
                ib = await pg.locator('#insts').bounding_box()
                await pg.mouse.move(lb['x'] + dot[0], lb['y'] + dot[1]); await pg.mouse.down()
                await pg.mouse.move(ib['x'] + 40, ib['y'] + 20, steps=8); await pg.mouse.up(); await pg.wait_for_timeout(200)
                check(await pg.locator('#insts .idel').count() == n0 + 1, 'glisser un son sur la liste en fait un instrument')
                t0 = len(await tracks())
                await pg.mouse.move(lb['x'] + dot[0], lb['y'] + dot[1]); await pg.mouse.down()
                await pg.mouse.move(sb['x'] + sb['width'] * 0.5, sb['y'] + sb['height'] * 0.5, steps=8)
                check(await pg.evaluate("document.querySelector('#lib').classList.contains('dragging')"), 'la bibliothèque s’efface pendant le glisser')
                await pg.mouse.up(); await pg.wait_for_timeout(200)
                check(len(await tracks()) == t0 + 1 and await pg.is_visible('#libCanvas'), 'glisser un son sur le morceau le pose, puis la bibliothèque revient')

        # copie de secours : un Ctrl+R ne perd rien
        await pg.keyboard.press('Escape')
        before = await tracks(); sets0 = await pressed()
        await pg.wait_for_timeout(6500)
        await pg.reload(); await pg.click('#startBtn'); await pg.wait_for_timeout(1500)
        check(await tracks() == before, f'après Ctrl+R, le morceau est repris ({await tracks()})')
        check(await pressed() == sets0, f'après Ctrl+R, les bibliothèques sont reprises ({await pressed()})')
        # nouveau morceau, et retour au précédent
        await pg.click('#newBtn'); await pg.wait_for_timeout(200)
        check(await tracks() == ['Fond'], f'Nouveau morceau : le fond seul ({await tracks()})')
        await pg.keyboard.press('Control+z'); await pg.wait_for_timeout(200)
        check(await tracks() == before, 'Ctrl+Z retrouve le morceau précédent')

        check(not errs, f'aucune erreur JavaScript ({errs[:3]})')
        await b.close()

asyncio.run(main('--lib' in sys.argv))
print('\n' + ('TOUT EST BON' if not failures else f'{len(failures)} ÉCHEC(S)'))
sys.exit(1 if failures else 0)
