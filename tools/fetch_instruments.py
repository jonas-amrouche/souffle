"""Télécharge les instruments échantillonnés (banque Musyng Kite, CC BY-SA 3.0, via gleitz/midi-js-soundfonts),
les compresse en MP3 mono 56 kbit/s (un échantillon toutes les 3 notes) et les injecte dans souffle.html,
dans <script id="samples" type="application/json">.

Prérequis : curl et ffmpeg.   Usage : python3 tools/fetch_instruments.py
Pour ajouter un instrument : l'ajouter à INST ci-dessous (nom General MIDI, note MIDI basse, note MIDI haute),
puis à INST dans souffle.html (libellé, famille, kind 'struck' ou 'sus', rel, gain).
"""
import subprocess, os, base64, json, re, pathlib, concurrent.futures as cf
ROOT = pathlib.Path(__file__).resolve().parent.parent
WORK = ROOT / 'tools' / '.cache'
NAMES = ['C','Db','D','Eb','E','F','Gb','G','Ab','A','Bb','B']
def nm(m): return f"{NAMES[m % 12]}{m // 12 - 1}"
INST = {
 'piano':('acoustic_grand_piano',24,96), 'epiano':('electric_piano_1',36,84), 'guitare':('acoustic_guitar_nylon',36,81),
 'basse':('acoustic_bass',24,60), 'violon':('violin',54,96), 'violoncelle':('cello',36,72), 'cordes':('string_ensemble_1',36,84),
 'trompette':('trumpet',54,84), 'flute':('flute',60,96), 'clarinette':('clarinet',51,84), 'orgue':('church_organ',36,84),
 'choeur':('choir_aahs',48,79), 'marimba':('marimba',36,96), 'vibraphone':('vibraphone',48,84), 'nappe':('pad_2_warm',36,84)}

def get(job):
    k, g, m = job
    src, dst = WORK / f'raw_{k}_{m}.mp3', WORK / f'enc_{k}_{m}.mp3'
    if not src.exists():
        url = f"https://raw.githubusercontent.com/gleitz/midi-js-soundfonts/gh-pages/MusyngKite/{g}-mp3/{nm(m)}.mp3"
        if subprocess.run(['curl', '-s', '-f', '-o', str(src), url]).returncode: return (k, m, None)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', str(src), '-ac', '1', '-b:a', '56k', str(dst)], check=True)
    return (k, m, dst)

def main():
    WORK.mkdir(parents=True, exist_ok=True)
    jobs = [(k, g, m) for k, (g, lo, hi) in INST.items() for m in range(lo, hi + 1) if m % 3 == 0]
    with cf.ThreadPoolExecutor(12) as ex: res = list(ex.map(get, jobs))
    out, miss = {}, []
    for k, m, p in res:
        if not p: miss.append((k, m)); continue
        out.setdefault(k, []).append([m, base64.b64encode(p.read_bytes()).decode()])
    for k in out: out[k].sort()
    html = (ROOT / 'souffle.html').read_text(encoding='utf-8')
    html, n = re.subn(r'(<script id="samples" type="application/json">).*?(</script>)', lambda mo: mo.group(1) + json.dumps(out) + mo.group(2), html, count=1, flags=re.S)
    assert n == 1, 'balise <script id="samples"> introuvable'
    (ROOT / 'souffle.html').write_text(html, encoding='utf-8')
    print(f"{sum(len(v) for v in out.values())} échantillons injectés, manquants : {miss}")

if __name__ == '__main__':
    main()
