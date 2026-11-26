"""Write records/gametext.json: the game's own skill and trait text, as BWIKI gives it, converted
from Simplified to Traditional Chinese character by character (OpenCC s2tw) and nothing else.

Usage (in the site folder):
  uv run -q --with opencc-python-reimplemented --with pypinyin python3 -I pipeline/gametext.py

The text is the game's expression, so the pages show it as the source gives it and never in our
own words (owner decision, 2026-11-25). Changes made here, and only these: markup removed, line
breaks kept (the page joins them with a space), names of characters that the Taiwan official
site spells otherwise replaced by that spelling, and a 靈子's skill name (which is the 靈子's
name) spelled as the Taiwan service spells the 靈子 (records/names_tw_lingzi.json). Values are those of level 1; a character skill
whose written text carries another level's values is taken from its template filled with level 1.

Output keys:
  characters[slug][n] = {"name", "text"}            skill n of the character record
  kibo[key] = text                                  key as in pipeline/check_text.py kibo_sources()
  lingzi[name_tw] = {"skill", "one", "full"}        skill name, text at one star and at full stars
The source is cache/bwiki/ (not committed); the game data is from test builds.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'pipeline'))
from check_text import clean, kibo_sources, lingzi_sources, load, s2tw  # noqa: E402

RECORDS = ROOT / 'records'


def official_names():
    """Converted name -> Taiwan official name, where the two differ."""
    out = {}
    for c in json.loads((RECORDS / 'characters.json').read_text(encoding='utf-8')):
        conv = s2tw.convert(c['name_cn'])
        if c.get('name_tw_source') == 'official-tw' and c['name_tw'] != conv:
            out[conv] = c['name_tw']
    return out


def rename(text, names):
    for a, b in sorted(names.items(), key=lambda x: -len(x[0])):
        text = text.replace(a, b)
    return text


def character_skills(c, f, names):
    out = {}
    for n in range(1, 7):
        name = f.get(f'技能{n}名')
        if not name or name == '0':
            continue
        text = f.get(f'技能{n}描述') or ''
        if f.get(f'技能{n}模板'):
            first = (f.get(f'技能{n}属性值') or '').split('/')[0].split(',')
            filled = f[f'技能{n}模板']
            for i, v in enumerate(first):
                filled = filled.replace('{' + str(i) + '}', v)
            # A template with a slot left (no value, or a slot such as {{2}}) is not used;
            # the written text stands, and its level is reported.
            if '{' in filled or not all(first):
                print(f"{c['slug']} skill {n}: template not filled; written text used", file=sys.stderr)
            else:
                text = filled
        text = clean(text)
        if text:
            out[str(n)] = {'name': clean(name), 'text': rename(text, names)}
    return out


def main():
    names = official_names()
    chars = json.loads((RECORDS / 'characters.json').read_text(encoding='utf-8'))
    src = load('角色')
    out = {'characters': {}, 'kibo': {}, 'lingzi': {}}
    for c in chars:
        if c['name_cn'] in src:
            out['characters'][c['slug']] = character_skills(c, src[c['name_cn']], names)
    for key, v in sorted(kibo_sources().items()):
        out['kibo'][key] = rename(v['source'], names)
    for name, v in sorted(lingzi_sources().items()):
        out['lingzi'][name] = {'skill': v['skill'], 'one': rename(v['source'], names), 'full': rename(v['source_full'], names)}
    (RECORDS / 'gametext.json').write_text(json.dumps(out, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    print('characters', len(out['characters']), 'kibo texts', len(out['kibo']), 'lingzi', len(out['lingzi']))


if __name__ == '__main__':
    main()
