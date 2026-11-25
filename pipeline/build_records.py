"""Build records/characters.json and records/kibo.json from the BWIKI cache.

Facts only: ids, names, element, rarity, numbers, work types, evolution links. Description
text is not copied; restated text lives in records/text/ and is written by a writer.

Names: the Taiwan service name where the Taiwan official site gives one (records/names_tw.json),
otherwise the mainland name converted character by character (OpenCC s2tw), marked
`name_tw_source: "converted"` so that the pass after launch can replace it.

Usage: uv run --with opencc-python-reimplemented --with pypinyin python3 -I pipeline/build_records.py
"""

import hashlib
import json
import re
from pathlib import Path

from opencc import OpenCC
from pypinyin import lazy_pinyin, load_phrases_dict

# Readings pypinyin gets wrong in Kibo names.
load_phrases_dict({'长尾': [['cháng'], ['wěi']]})

ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / 'cache' / 'bwiki'
RECORDS = ROOT / 'records'
s2tw = OpenCC('s2tw')

ELEMENTS = ['火', '水', '風', '雷', '冰', '木', '地', '光', '暗', '無']
# Element of a page as the game names it (mainland text) -> Traditional.
ELEMENT_TW = {'火': '火', '水': '水', '风': '風', '雷': '雷', '冰': '冰', '木': '木', '地': '地', '光': '光', '暗': '暗', '无': '無'}
# Test names in the mainland community (BWIKI 实装版本) -> how pages write them.
BUILD = {'一测': '第一次測試', '二测': '第二次測試', '三测': '第三次測試（星至測試）', '四测': '第四次測試（恆序測試）', '1.0': '公測 1.0'}


def template(wikitext, name):
    """Fields of the first {{name ...}} template as a dict (values stripped, HTML kept)."""
    m = re.search(r'\{\{' + re.escape(name) + r'\s*\n(.*?)\n\}\}', wikitext, re.S)
    if not m:
        return None
    fields, key = {}, None
    for line in m.group(1).split('\n'):
        if line.startswith('|') and '=' in line:
            key, _, value = line[1:].partition('=')
            key = key.strip()
            fields[key] = value.strip()
        elif key:
            fields[key] += '\n' + line
    return fields


def split(value, sep='、'):
    return [v.strip() for v in re.split(sep, value or '') if v.strip()]


def elements(value):
    """One element or several (`地、火`), in Traditional characters, joined with 、."""
    return '、'.join(ELEMENT_TW.get(e, e) for e in split(value))


def skill_fingerprints(f):
    pairs = [('固定技能', '固定技能描述1')] + [(f'技能{i}', f'技能{i}描述1') for i in (1, 2, 3, 4)] + [('合击技能', '合击技能描述1')] + [(f'特性{i}', f'特性{i}描述') for i in (1, 2, 3)]
    out = {}
    for name_key, desc_key in pairs:
        if f.get(name_key):
            out[s2tw.convert(f[name_key])] = hashlib.sha1((f.get(desc_key) or '').encode()).hexdigest()[:8]
    return out


def slug_latin(name):
    return re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')


def slug_pinyin(name):
    base = re.sub(r'（.*?）', '', name)
    return ''.join(lazy_pinyin(base)).lower().replace('ü', 'v')


def load(category):
    file = CACHE / f'{category}.json'
    return json.loads(file.read_text(encoding='utf-8')) if file.exists() else {}


def characters(names_tw):
    out = []
    for title, page in load('角色').items():
        f = template(page['wikitext'], '角色图鉴')
        if not f:
            continue
        cn = re.sub(r'\s+', '', f['名称'])
        official = names_tw.get(cn)
        # Romanization: the Taiwan official site's, else the game's English name as BWIKI gives it.
        romaji = (official or {}).get('romaji') or (f.get('英文名') or '').strip().title() or None
        skills = []
        for i in range(1, 10):
            name = f.get(f'技能{i}名')
            if not name and not f.get(f'技能{i}模板'):
                continue
            name = None if name in (None, '', '0') else name
            values = [v.split(',') for v in split(f.get(f'技能{i}属性值', ''), '/')]
            skills.append({
                'n': i,
                'name_cn': name,
                'name_tw': s2tw.convert(name) if name else None,
                'kind': (re.match(r'【(.+?)】', f.get(f'技能{i}描述') or f.get(f'技能{i}模板') or '') or [None, None])[1],
                'value_names': split(s2tw.convert(f.get(f'技能{i}属性名', '')), ','),
                'values_by_level': values,
                'cooldown': f.get(f'技能{i}冷却'),
                'energy': f.get(f'技能{i}能量消耗'),
            })
        out.append({
            'id': f.get('id'),
            'slug': slug_latin(romaji) if romaji else slug_pinyin(cn),
            'name_cn': cn,
            'name_tw': (official or {}).get('name') or s2tw.convert(cn),
            'name_tw_source': 'official-tw' if official else 'converted',
            'romaji': romaji,
            'romaji_source': 'official-tw' if official else 'bwiki-english',
            'rarity': f.get('稀有度'),
            'class': s2tw.convert(f.get('职业', '')),
            'element': elements(f.get('元素')),
            'weapon': s2tw.convert(f.get('武器', '')),
            'faction': s2tw.convert(f.get('阵营', '')),
            'race': s2tw.convert(f.get('种族', '')),
            'role': split(s2tw.convert(f.get('战斗定位', ''))),
            'type': s2tw.convert(f.get('角色类型', '')),
            'release_version': f.get('实装版本'),
            'release_date': f.get('实装日期'),
            'cv_ja': f.get('日语CV') or None,
            'cv_zh': f.get('汉语CV') or None,
            'skills': skills,
            'source': {'title': title, 'revid': page['revid'], 'timestamp': page['timestamp']},
        })
    return sorted(out, key=lambda c: (c['rarity'] or '', c['name_tw']), reverse=False)


def saddles():
    """Kibo name (Simplified) -> saddles for riding it. A saddle names its Kibo in its description
    (为骑行<Kibo>准备的鞍具); a Kibo with a saddle can be ridden."""
    out = {}
    if not (CACHE / '鞍具.json').exists():
        return None
    for title, page in load('鞍具').items():
        f = template(page['wikitext'], '鞍具图鉴')
        m = re.search(r'为骑行(.+?)准备', (f or {}).get('描述', ''))
        if m:
            out.setdefault(m.group(1), []).append({'name_tw': s2tw.convert(f['名称']), 'rarity': f.get('稀有度'), 'build': f.get('实装版本'),
                                                   'source': {'title': title, 'revid': page['revid'], 'timestamp': page['timestamp']}})
    return out


def kibo(names_tw):
    ride = saddles() or {}
    en = {k: v for k, v in json.loads((RECORDS / 'kibo_en.json').read_text(encoding='utf-8')).items() if not k.startswith('_')}
    out = []
    for title, page in load('奇波').items():
        f = template(page['wikitext'], '奇波图鉴')
        if not f:
            continue
        cn = f['名称']
        # The story's own copy of a Kibo carries （特殊） only in the page title, not in 名称.
        if '（特殊）' in title and '（特殊）' not in cn:
            cn += '（特殊）'
        official = names_tw.get(cn)
        out.append({
            'id': f.get('id'),
            'slug': (slug_latin(en[cn]) if cn in en else slug_pinyin(cn)) + ('-special' if '（特殊）' in cn else ''),
            'name_en': en.get(cn),
            'name_cn': cn,
            'name_tw': (official or {}).get('name') or s2tw.convert(cn),
            'name_tw_source': 'official-tw' if official else 'converted',
            'element': elements(f.get('元素')),
            'race': s2tw.convert(f.get('种族', '')),
            'stage': s2tw.convert(f.get('阶段', '')),
            'tag': s2tw.convert(f.get('标签', '')),
            'height': f.get('身高'),
            'size': s2tw.convert(f.get('体型', '')),
            'trait': split(s2tw.convert(f.get('特征', ''))),
            'work': split(s2tw.convert(f.get('家园工种', ''))),
            'drops': split(s2tw.convert(f.get('掉落素材', ''))),
            'shiny': f.get('异色') == '1',
            'build': f.get('实装版本'),
            'passives': [{'name_tw': s2tw.convert(f[f'特性{i}']), 'name_cn': f[f'特性{i}']} for i in (1, 2, 3) if f.get(f'特性{i}')],
            # Fingerprint of each skill's level-1 text: the game text in records/gametext.json
            # is keyed by name, and a name whose text differs between Kibo gets one entry per
            # fingerprint (`name@fp`).
            'skill_fp': skill_fingerprints(f),
            'fixed_skill': s2tw.convert(f.get('固定技能', '')) or None,
            'skills': [s2tw.convert(f[f'技能{i}']) for i in (1, 2, 3, 4) if f.get(f'技能{i}')],
            'combo_skill': s2tw.convert(f.get('合击技能', '')) or None,
            'line': s2tw.convert(f.get('进化系列', '')) or None,
            'evolves_from': s2tw.convert(f.get('进化上级', '')) or None,
            'evolves_to': s2tw.convert(f.get('进化下级', '')) or None,
            'evolve_level': f.get('进化下级等级') or None,
            'saddles': ride.get(cn, []),
            'page': True,
            'source': {'title': title, 'revid': page['revid'], 'timestamp': page['timestamp']},
        })
    seen = {}
    for k in out:
        seen.setdefault(k['slug'], []).append(k)
    for slug, group in seen.items():
        if len(group) > 1:
            for k in group:
                k['slug'] = f"{slug}-{k['id']}"
    order = {e: i for i, e in enumerate(ELEMENTS)}
    return sorted(out, key=lambda k: (order.get(k['element'].split('、')[0], 99), k['slug']))


RARITY = {}  # R, SR, SSR as the game writes them


def lingzi():
    """靈子 (equipment cards). Their skill text is in records/gametext.json, keyed by name."""
    if not (CACHE / '灵子.json').exists():
        return None
    out = []
    for title, page in load('灵子').items():
        f = template(page['wikitext'], '灵子图鉴')
        if not f:
            continue
        cn = f['名称']
        out.append({
            'id': f.get('id'),
            'slug': slug_pinyin(cn),
            'name_cn': cn,
            'name_tw': s2tw.convert(cn),
            'rarity': RARITY.get(f.get('稀有度'), f.get('稀有度')),
            'class': s2tw.convert(f.get('职业', '')) or None,
            'stat': s2tw.convert(f.get('属性', '')),
            'stat_1': f.get('属性值'), 'stat_100': f.get('100属性值'),
            'hp_1': f.get('基础生命'), 'atk_1': f.get('基础攻击'), 'def_1': f.get('基础防御'),
            'hp_100': f.get('100基础生命'), 'atk_100': f.get('100基础攻击'), 'def_100': f.get('100基础防御'),
            'skill': s2tw.convert(f.get('技能', '')),
            'skill_fp': hashlib.sha1(((f.get('技能描述') or '') + (f.get('满星技能描述') or '')).encode()).hexdigest()[:8],
            'build': f.get('实装版本'),
            'source': {'title': title, 'revid': page['revid'], 'timestamp': page['timestamp']},
        })
    order = {'SSR': 0, 'SR': 1, 'R': 2}
    return sorted(out, key=lambda x: (order.get(x['rarity'], 9), x['slug']))


def main():
    names_tw = {k: v for k, v in json.loads((RECORDS / 'names_tw.json').read_text(encoding="utf-8")).items() if not k.startswith("_")}
    RECORDS.mkdir(exist_ok=True)
    rows_kibo = kibo(names_tw)
    if not rows_kibo and (RECORDS / 'kibo.json').exists():
        rows_kibo = None  # no cache: keep the records as they are
    for name, rows in (('characters', characters(names_tw)), ('kibo', rows_kibo), ('lingzi', lingzi())):
        if rows is None:
            continue
        (RECORDS / f'{name}.json').write_text(json.dumps(rows, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
        print(name, len(rows), 'official TW names:', sum(r.get('name_tw_source') == 'official-tw' for r in rows))


if __name__ == '__main__':
    main()
