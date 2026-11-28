"""Write records/gear.json from BWIKI's gear pages (category 装备, template 装备图鉴) in cache/bwiki/.

Usage (in the site folder):
  python3 -I pipeline/fetch_bwiki.py 装备      # fill cache/bwiki/装备.json (resumable)
  uv run -q --with opencc-python-reimplemented python3 -I pipeline/build_gear.py

Facts only: slot, rarity, set, the class tag (适配职业), enhancement cap, main stats at level 0 and
at the cap, how to obtain it. The set effects and the effect of each affix (词条) are the game's
own text: kept as BWIKI gives it, converted to Traditional characters by OpenCC s2tw and nothing
else, as for skill text (owner decision, 2026-11-25). The flavour text (描述) is left out. The
data is the third test's (实装版本 三测); the page says so and gives the launch values of the
sets from players' sources in a section of its own.
"""
import json
import re
from pathlib import Path

from opencc import OpenCC

ROOT = Path(__file__).resolve().parent.parent
s2tw = OpenCC('s2tw')
SLOTS = ['武器', '上装', '下装', '耳环', '戒指']


def conv(s):
    # The Taiwan service writes 台; OpenCC writes 臺.
    return s2tw.convert(s).replace('臺', '台')


def fields(wikitext):
    m = re.search(r'\{\{装备图鉴(.*)\}\}', wikitext, re.S)
    out = {}
    for line in re.split(r'\n\|', m.group(1)):
        if '=' in line:
            k, v = line.split('=', 1)
            out[k.strip()] = v.strip()
    return out


def main():
    cache = json.loads((ROOT / 'cache' / 'bwiki' / '装备.json').read_text(encoding='utf-8'))
    items, sets = [], {}
    for title, page in sorted(cache.items(), key=lambda x: x[0]):
        f = fields(page['wikitext'])
        if f.get('类型') not in SLOTS:
            raise SystemExit(f'{title}: unknown slot {f.get("类型")!r}')
        stats = []
        for n in (1, 2):
            if f.get(f'主属性{n}'):
                stats.append({'stat': conv(f[f'主属性{n}']), 'lv0': f[f'主属性{n}初始'], 'max': f[f'主属性{n}满级']})
        affixes = []
        for n in range(10):
            if f.get(f'词条{n}名'):
                affixes.append({'name': conv(f[f'词条{n}名']), 'level': int(f[f'词条{n}等级']), 'text': conv(f[f'词条{n}数值'])})
        set_cn = f.get('套装', '')
        if set_cn:
            s = sets.setdefault(set_cn, {'name_cn': set_cn, 'name_tw': conv(set_cn), 'two': '', 'four': ''})
            for key, field in (('two', '套装2件'), ('four', '套装4件')):
                text = conv(f.get(field, ''))
                if text and s[key] and s[key] != text:
                    raise SystemExit(f'{title}: {field} differs from another piece of {set_cn}')
                s[key] = s[key] or text
        items.append({
            'id': f['id'], 'name_cn': title, 'name_tw': conv(title), 'slot': conv(f['类型']), 'rarity': f['稀有度'],
            'set': conv(set_cn), 'class': conv(f.get('适配职业', '')), 'max_level': int(f['最高强化']),
            'stats': stats, 'affixes': affixes,
            'obtain': [conv(x) for x in f.get('获取方式', '').split('、') if x],
            'build': f.get('实装版本', ''),
            'source': {'title': title, 'revid': page['revid'], 'timestamp': page['timestamp']},
        })
    out = {
        '_about': 'Gear (装备): one record per piece, from the BWIKI pages of category 装备 (template 装备图鉴, third test), '
                  'read 2026-11-28 by pipeline/build_gear.py. Names, set effects and affix effects are the game text converted '
                  'by OpenCC s2tw; the flavour text is left out.',
        'sets': sorted(sets.values(), key=lambda s: s['name_cn']),
        'items': items,
    }
    (ROOT / 'records' / 'gear.json').write_text(json.dumps(out, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    print('items', len(items), 'sets', len(sets))


if __name__ == '__main__':
    main()
