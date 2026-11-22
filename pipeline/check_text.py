"""Check restated text against the game data, one unit at a time, and print the source for a writer.

Usage (in the site folder):
  uv run --with opencc-python-reimplemented python3 -I pipeline/check_text.py char-src <slug>     # source of one character, Traditional
  uv run --with opencc-python-reimplemented python3 -I pipeline/check_text.py char <slug> [...]   # check records/text/characters/<slug>.json
  uv run --with opencc-python-reimplemented python3 -I pipeline/check_text.py kibo-todo [i/n]     # keys without text, with their source (part i of n)
  uv run --with opencc-python-reimplemented python3 -I pipeline/check_text.py lingzi-todo | lingzi [name ...] | lingzi-file <file>   # 靈子 skills
  uv run --with opencc-python-reimplemented python3 -I pipeline/check_text.py kibo-file <file>    # check a batch file of the same shape as kibo-skills.json
  uv run --with opencc-python-reimplemented python3 -I pipeline/check_text.py kibo [key ...]      # check records/text/kibo-skills.json (all keys by default)

A check fails (exit 1) when:
  - a field is missing, or a character skill of the record has no text;
  - a percentage in the text is not a level-1 value of that skill in the source;
  - the text follows the source too closely (after conversion to Traditional, without markup,
    spaces and punctuation): one shared run of 20 or more characters, or more than half of the
    text in shared runs of 8 or more. Game terms and short formulas such as 消耗1枚風印記 may
    repeat; sentences may not;
  - the description is longer than 70 characters;
  - a pattern of pipeline/check_prose.py matches (source names, hedges, timed content, the site).
The source is cache/bwiki/ (not committed); the game data is from test builds.
"""
import json
import re
import sys
from difflib import SequenceMatcher
from pathlib import Path

from opencc import OpenCC

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'pipeline'))
from check_prose import PATTERNS  # noqa: E402
from build_records import skill_fingerprints, template  # noqa: E402

s2tw = OpenCC('s2tw')
COPY_RUN = 20
COPY_SHARE = 0.5
COPY_MIN = 8
PCT = re.compile(r'(\d+(?:\.\d+)?)\s*%')


def clean(text):
    text = re.sub(r'<br\s*/?>', '\n', text or '')
    text = re.sub(r'<[^>]+>', '', text)
    return s2tw.convert(text).strip()


def squash(text):
    return re.sub(r'[\s，。、；：「」『』（）()！？,.;:!?—-]+', '', text)


def copied(mine, source):
    """A message when `mine` follows `source` too closely, else ''."""
    a, b = squash(mine), squash(source)
    if not a or not b:
        return ''
    blocks = SequenceMatcher(None, a, b, autojunk=False).get_matching_blocks()
    longest = max(blocks, key=lambda m: m.size)
    if longest.size >= COPY_RUN:
        return f'copies the source: "{a[longest.a:longest.a + longest.size]}"'
    share = sum(m.size for m in blocks if m.size >= COPY_MIN) / len(a)
    if share > COPY_SHARE:
        return f'{share:.0%} of the text is in runs shared with the source'
    return ''


def prose_hits(text):
    hits = []
    for kind, pats in PATTERNS.items():
        for p in pats:
            if re.search(p, text):
                hits.append(f'{kind} /{p}/')
    return hits


def load(category):
    data = json.loads((ROOT / 'cache' / 'bwiki' / f'{category}.json').read_text(encoding='utf-8'))
    tpl = {'角色': '角色图鉴', '奇波': '奇波图鉴', '灵子': '灵子图鉴'}[category]
    return {name: template(page['wikitext'], tpl) for name, page in data.items()}


def char_source(c):
    f = load('角色')[c['name_cn']]
    skills = {}
    for n in range(1, 7):
        # The written text of some characters carries another level's values; the template
        # filled with the first level's values is level 1. Both are kept for the check.
        desc = f.get(f'技能{n}描述') or ''
        if f.get(f'技能{n}模板'):
            first = (f.get(f'技能{n}属性值') or '').split('/')[0].split(',')
            filled = f[f'技能{n}模板']
            for i, v in enumerate(first):
                filled = filled.replace('{' + str(i) + '}', v)
            desc = desc + ('\n' + filled if desc and filled != desc else filled if not desc else '')
        name = f.get(f'技能{n}名')
        skills[str(n)] = {'name': clean(name) if name and name != '0' else '—', 'desc': clean(desc)}
    return {'intro': clean(f.get('介绍')), 'words': clean(f.get('描述')), 'skills': skills}


def check_char(slug):
    chars = {c['slug']: c for c in json.loads((ROOT / 'records' / 'characters.json').read_text(encoding='utf-8'))}
    c = chars[slug]
    path = ROOT / 'records' / 'text' / 'characters' / f'{slug}.json'
    if not path.exists():
        return [f'{slug}: no {path.relative_to(ROOT)}']
    t = json.loads(path.read_text(encoding='utf-8'))
    src = char_source(c)
    errs = []
    for key in ('description', 'applies', 'caveat', 'lead', 'skills_intro', 'skills'):
        if not t.get(key):
            errs.append(f'missing "{key}"')
    if len(t.get('description', '')) > 70:
        errs.append(f'description has {len(t["description"])} characters (at most 70)')
    for key in ('description', 'caveat', 'lead', 'skills_intro'):
        for h in prose_hits(t.get(key, '')):
            errs.append(f'{key}: {h}')
    msg = copied(t.get('lead', ''), src['intro'] + src['words'])
    if msg:
        errs.append(f'lead {msg}')
    for s in c['skills']:
        n = str(s['n'])
        mine = (t.get('skills') or {}).get(n)
        if not mine:
            errs.append(f'skill {n} ({s["name_tw"]}): no text')
            continue
        source = src['skills'].get(n, {}).get('desc', '')
        allowed = set(PCT.findall(source))
        for v in PCT.findall(mine.get('effect', '')):
            if v not in allowed:
                errs.append(f'skill {n}: {v}% is not a level-1 value of the source ({", ".join(sorted(allowed)) or "none"})')
        msg = copied(mine.get('effect', ''), source)
        if msg:
            errs.append(f'skill {n}: {msg}')
        for h in prose_hits(mine.get('effect', '')):
            errs.append(f'skill {n}: {h}')
    return [f'{slug}: {e}' for e in errs]


def kibo_sources():
    """key -> level-1 source text; the key is `name`, or `name@fingerprint` where one name has several texts."""
    pairs = [('固定技能', '固定技能描述1')] + [(f'技能{i}', f'技能{i}描述1') for i in (1, 2, 3, 4)] + [('合击技能', '合击技能描述1')] + [(f'特性{i}', f'特性{i}描述') for i in (1, 2, 3)]
    by_name = {}
    for f in load('奇波').values():
        fps = skill_fingerprints(f)
        for nk, dk in pairs:
            if f.get(nk):
                name = s2tw.convert(f[nk])
                by_name.setdefault(name, {})[fps[name]] = (clean(f.get(dk)), nk.startswith('特性'), f.get('名称'))
    out = {}
    for name, texts in by_name.items():
        for fp, (text, trait, owner) in texts.items():
            key = name if len(texts) == 1 else f'{name}@{fp}'
            out[key] = {'source': text, 'kind': '特性' if trait else '技能', 'kibo': s2tw.convert(owner or '')}
    return out


def check_kibo(keys, file=None):
    texts = json.loads(Path(file or ROOT / 'records' / 'text' / 'kibo-skills.json').read_text(encoding='utf-8'))
    sources = kibo_sources()
    errs = []
    for key in keys or list(texts):
        mine = texts.get(key)
        if mine is None:
            errs.append(f'{key}: no text')
            continue
        if key not in sources:
            errs.append(f'{key}: no skill or trait of this key in the game data')
            continue
        source = sources[key]['source']
        allowed = set(PCT.findall(source))
        for v in PCT.findall(mine):
            if v not in allowed:
                errs.append(f'{key}: {v}% is not in the level-1 source ({", ".join(sorted(allowed)) or "none"})')
        msg = copied(mine, source)
        if msg:
            errs.append(f'{key}: {msg}')
        for h in prose_hits(mine):
            errs.append(f'{key}: {h}')
    return errs


def lingzi_sources():
    """靈子 name (Traditional) -> its skill text at one star and at full stars."""
    out = {}
    for f in load('灵子').values():
        if not f:
            continue
        out[s2tw.convert(f['名称'])] = {'source': clean(f.get('技能描述')), 'source_full': clean(f.get('满星技能描述')), 'skill': s2tw.convert(f.get('技能', ''))}
    return out


def check_lingzi(keys, file=None):
    texts = json.loads(Path(file or ROOT / 'records' / 'text' / 'lingzi-skills.json').read_text(encoding='utf-8'))
    sources = lingzi_sources()
    errs = []
    for key in keys or list(texts):
        mine = texts.get(key)
        if mine is None:
            errs.append(f'{key}: no text')
            continue
        if key not in sources:
            errs.append(f'{key}: no 靈子 of this name in the game data')
            continue
        src = sources[key]
        allowed = set(PCT.findall(src['source'])) | set(PCT.findall(src['source_full']))
        allowed |= {re.sub(r'\.?0+$', '', v) for v in allowed if '.' in v}  # 6.50% may be written 6.5%
        for v in PCT.findall(mine):
            if v not in allowed:
                errs.append(f'{key}: {v}% is not in the source ({", ".join(sorted(allowed)) or "none"})')
        msg = copied(mine, src['source'])
        if msg:
            errs.append(f'{key}: {msg}')
        for h in prose_hits(mine):
            errs.append(f'{key}: {h}')
    return errs


def main(argv):
    if not argv:
        print(__doc__)
        return 2
    cmd, args = argv[0], argv[1:]
    if cmd == 'char-src':
        chars = {c['slug']: c for c in json.loads((ROOT / 'records' / 'characters.json').read_text(encoding='utf-8'))}
        c = chars[args[0]]
        out = {'record': {k: c[k] for k in c if k not in ('skills', 'source')},
               'skills_record': [{k: s[k] for k in ('n', 'name_tw', 'kind', 'value_names', 'cooldown', 'energy')} | {'level1': s['values_by_level'][0] if s['values_by_level'] else [], 'level12': s['values_by_level'][-1] if s['values_by_level'] else []} for s in c['skills']],
               'source': char_source(c)}
        print(json.dumps(out, ensure_ascii=False, indent=1))
        return 0
    if cmd == 'kibo-todo':
        texts = json.loads((ROOT / 'records' / 'text' / 'kibo-skills.json').read_text(encoding='utf-8'))
        todo = {k: v for k, v in kibo_sources().items() if k not in texts and k.split('@')[0] not in texts}
        if args:  # part i of n, e.g. 2/4: a fixed split of the sorted keys
            i, n = map(int, args[0].split('/'))
            keys = sorted(todo)
            todo = {k: todo[k] for k in keys[(i - 1) * len(keys) // n:i * len(keys) // n]}
        print(json.dumps(todo, ensure_ascii=False, indent=1))
        print(f'{len(todo)} keys without text', file=sys.stderr)
        return 0
    if cmd == 'lingzi-todo':
        path = ROOT / 'records' / 'text' / 'lingzi-skills.json'
        texts = json.loads(path.read_text(encoding='utf-8')) if path.exists() else {}
        todo = {k: v for k, v in lingzi_sources().items() if k not in texts}
        print(json.dumps(todo, ensure_ascii=False, indent=1))
        print(f'{len(todo)} keys without text', file=sys.stderr)
        return 0
    errs = []
    if cmd == 'lingzi':
        errs = check_lingzi(args)
    elif cmd == 'lingzi-file':
        errs = check_lingzi([], args[0])
    elif cmd == 'char':
        for slug in args:
            errs += check_char(slug)
    elif cmd == 'kibo':
        errs = check_kibo(args)
    elif cmd == 'kibo-file':  # check every key of a batch file
        errs = check_kibo([], args[0])
    else:
        print(__doc__)
        return 2
    for e in errs:
        print(e)
    print('OK' if not errs else f'{len(errs)} problem(s)', file=sys.stderr)
    return 1 if errs else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
