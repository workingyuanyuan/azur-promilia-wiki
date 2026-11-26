"""Write the generated pages (Traditional Chinese, the root language) from records/.

Pages: characters/index, characters/<slug> (for characters with restated text in
records/text/characters/<slug>.json), kibo/index, kibo/work, kibo/elements, kibo/<slug>.
Simplified Chinese is written from these by scripts/to-zh-cn.py; never edit either by hand.

Usage: uv run --with opencc-python-reimplemented python3 -I pipeline/build_pages.py
"""

import json
import urllib.parse
import re
from pathlib import Path
from urllib.parse import quote

from opencc import OpenCC

tw2s = OpenCC('tw2s')

ROOT = Path(__file__).resolve().parent.parent
RECORDS = ROOT / 'records'
DOCS = ROOT / 'src' / 'content' / 'docs'
TODAY = '2026-11-22'
BWIKI = 'https://wiki.biligame.com/ap/'
TW_SITE = 'https://azurpromilia.com/zh-tw/home/'
ART = json.loads((ROOT / 'records' / 'art.json').read_text(encoding='utf-8'))
# The game's own skill and trait text, as BWIKI gives it, converted to Traditional characters
# (pipeline/gametext.py). Shown as it is, never restated.
NAMES_JA = json.loads((ROOT / 'records' / 'names_ja.json').read_text(encoding='utf-8'))
GAMETEXT = json.loads((ROOT / 'records' / 'gametext.json').read_text(encoding='utf-8'))


def game_text(s):
    """The game's text on one line: its line breaks become spaces."""
    return ' '.join(line.strip() for line in s.split('\n') if line.strip())
# BWIKI's names for the tests -> how pages write them.
BUILD = {'一测': '第一次測試', '二测': '第二次測試', '三测': '第三次測試', '四测': '第四次測試', '1.0': '公測 1.0'}
ELEMENTS = ['火', '水', '風', '雷', '冰', '木', '地', '光', '暗', '無']


def load(name):
    return json.loads((RECORDS / name).read_text(encoding='utf-8'))


def yaml_str(s):
    return json.dumps(s, ensure_ascii=False)


def bwiki_source(rec):
    src = rec['source']
    return {'title': f"BWIKI：{src['title']}（修訂 {src['revid']}，{src['timestamp'][:10]}）",
            'url': f"{BWIKI}index.php?title={quote(src['title'])}&oldid={src['revid']}"}


def front(title, description, applies, caveat, sources, aliases=(), effective=None, art=None, verified=None):
    lines = ['---', f'title: {yaml_str(title)}', f'description: {yaml_str(description)}', f'appliesTo: {yaml_str(applies)}',
             f'caveat: {yaml_str(caveat)}', f'lastVerified: {verified or TODAY}']
    if effective:
        lines.append(f'effectiveDate: {effective}')
    # The Simplified title is an alias of every page: scripts/to-zh-cn.py makes it the title there.
    aliases = [a for a in dict.fromkeys([*aliases, tw2s.convert(title)]) if a and a != title]
    if aliases:
        lines.append('aliases:')
        lines += [f'  - {yaml_str(a)}' for a in aliases]
    if art:
        lines += ['art:']
        for a in (art if isinstance(art, list) else [art]):
            lines += [f"  - title: {yaml_str(a['title'])}", f"    url: {a['url']}"]
    lines.append('sources:')
    for s in sources:
        lines += [f"  - title: {yaml_str(s['title'])}", f"    url: {s['url']}"]
    lines.append('---')
    return '\n'.join(lines) + '\n'


def write(path, text):
    out = DOCS / path
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text, encoding='utf-8')


def cell(s):
    return str(s if s not in (None, '') else '—').replace('|', '／').replace('\n', ' ')


def table(head, rows):
    out = ['| ' + ' | '.join(head) + ' |', '| ' + ' | '.join('---' for _ in head) + ' |']
    out += ['| ' + ' | '.join(cell(c) for c in r) + ' |' for r in rows]
    return '\n'.join(out) + '\n'


def stars(r):
    return {'5星': '五星', '4星': '四星', '3星': '三星'}.get(r, r or '—')


KIBO_PAGES = set()


def kibo_link(k):
    return f"[{k['name_tw']}](/kibo/{k['slug']}/)" if k['slug'] in KIBO_PAGES else k['name_tw']


# ---------------------------------------------------------------- characters

def character_page(c, text, kibo_by_cn):
    skills = []
    for s in c['skills']:
        g = GAMETEXT['characters'].get(c['slug'], {}).get(str(s['n']))
        if not g:  # a slot the game data leaves empty (no name, no text)
            continue
        kind = text['skills'].get(str(s['n']), {}).get('kind', s['kind'])
        lv12 = '、'.join(f'{n} {v}' for n, v in zip(s['value_names'], s['values_by_level'][-1])) if len(s['values_by_level']) > 1 and s['value_names'] else ''
        cost = []
        if s['cooldown'] and float(s['cooldown']) > 0:
            cost.append(f"冷卻 {float(s['cooldown']):g} 秒")
        if s['energy'] and float(s['energy']) > 0:
            cost.append(f"能量 {float(s['energy']):g}")
        skills.append([g['name'], kind, game_text(g['text']), lv12, '、'.join(cost)])
    facts = [
        ['稀有度', stars(c['rarity'])], ['屬性', c['element']], ['職業', c['class']], ['武器', c['weapon']],
        ['日服名稱', NAMES_JA.get(c['slug'], {}).get('name_ja')], ['戰鬥定位', '、'.join(c['role'])], ['類型', c['type']], ['陣營', c['faction']], ['種族', c['race']],
        ['日文配音', text.get('cv_ja') or c['cv_ja']], ['加入版本', BUILD.get(c['release_version'], c['release_version'])],
    ]
    facts = [f for f in facts if f[1] and f[1] != '未知']  # the game data's 未知 tells the reader nothing
    # Two kinds of picture (records/art.json): our cutout of an official illustration of the
    # Taiwan site (pipeline/cut_art.py), which links to the original; or the game's own card
    # art as wikiru hosts it, shown unchanged but resized, which links to the wikiru page.
    entry = ART.get(c['slug'], {})
    art = ROOT / 'public' / 'art' / 'characters' / f"{c['slug']}.webp"
    has_art = art.exists() and entry.get('original')
    wikiru = entry.get('source') == 'wikiru'
    if has_art:
        alt, link = (f"{c['name_tw']}，遊戲立繪", entry['page']) if wikiru else (f"{c['name_tw']}，官方立繪", entry['original'])
        body = [f"[![{alt}](/art/characters/{c['slug']}.webp)]({link})", '']
        credits = ([{'title': f"アズールプロミリア有志Wiki（{urllib.parse.unquote(entry['page'].split('?', 1)[1])}）", 'url': entry['page']},
                    {'title': f"立繪原檔：{entry['file_title']}（讀取於 {entry['read']}）", 'url': entry['original']}] if wikiru else
                   [{'title': '台港澳官方網站（角色）', 'url': TW_SITE},
                    {'title': f"{c['name_tw']}立繪原圖（去背前）", 'url': entry['original']}])
    else:
        body, credits = [], None
    body += ['## 人物與打法', '', text['lead'], '', '## 基本資料', '', table(['項目', '內容'], facts)]
    body += ['## 技能', '', text.get('skills_intro', ''), '', table(['技能', '種類', '效果（技能等級 1）', '技能等級 12 的倍率', '冷卻與消耗'], skills)]
    if text.get('kibo'):
        body += ['## 奇波', '', text['kibo'], '']
    sources = [bwiki_source(c)]
    ja = NAMES_JA.get(c['slug'])
    if ja:
        sources.append({'title': f"アズールプロミリア有志Wiki：{ja['name_ja']}（日服名稱，2026-11-25 讀取）", 'url': ja['page']})
    if c['name_tw_source'] == 'official-tw':
        sources.append({'title': '藍色星原：旅謠 台港澳官方網站（角色）', 'url': TW_SITE})
    head = front(c['name_tw'], text['description'], text['applies'], text['caveat'], sources,
                 aliases=[c['name_cn'], c.get('romaji'), ja and ja['name_ja']],
                 art=credits)
    return head + '\n' + '\n'.join(body).replace('\n\n\n', '\n\n')


def released(c):
    """Characters the game data dates to a later version (`1.x`, `2027年xx月`) are left out."""
    return 'x' not in (c['release_version'] or '') + (c['release_date'] or '')


def characters_index(chars, written):
    chars = [c for c in chars if released(c)]
    rows = []
    for c in sorted(chars, key=lambda c: (-int((c['rarity'] or '0')[0]), ELEMENTS.index(c['element']) if c['element'] in ELEMENTS else 99, c['name_tw'])):
        name = f"[{c['name_tw']}](/characters/{c['slug']}/)" if c['slug'] in written else c['name_tw']
        rows.append([name, c['name_cn'], c.get('romaji'), stars(c['rarity']), c['element'], c['class'], c['weapon'], c['type']])
    rows.sort(key=lambda r: 0 if r[0].startswith('[') else 1)
    n5 = sum(c['rarity'] == '5星' for c in chars)
    head = front('角色列表', f'《藍色星原：旅謠》的 {len(chars)} 名可用角色，其中 {n5} 名是 5 星。',
                 'BWIKI 整理的遊戲資料，2026-11-22 讀取', '名稱以台港澳服官網為準；官網未列出的角色，繁體名稱由簡體名稱逐字轉寫。',
                 [{'title': 'BWIKI：角色分類', 'url': BWIKI + quote('Category:角色')}, {'title': '藍色星原：旅謠 台港澳官方網站', 'url': TW_SITE}],
                 aliases=['角色一覽', '角色图鉴', 'Azur Promilia characters'])
    n5 = sum(c['rarity'] == '5星' for c in chars)
    lead = f"其餘 {len(chars) - n5} 名是四星；名單含玩家操作的主角「星臨者」。"
    return head + '\n## 角色\n\n' + lead + '\n\n' + table(['名稱', '簡體', '英文名', '稀有度', '屬性', '職業', '武器', '類型'], rows)


# ---------------------------------------------------------------- Kibo

def text_for(k, name, skill_text):
    """The game's text of a Kibo's skill or trait: `name@fingerprint` first, then `name`."""
    s = skill_text.get(f"{name}@{k['skill_fp'].get(name)}") or skill_text.get(name)
    return game_text(s) if s else s


def kibo_page(k, by_tw, skill_text):
    def link(name):
        other = by_tw.get(name)
        return kibo_link(other) if other else name
    facts = [
        ['屬性', k['element']], ['種族', k['race']], ['成長階段', k['stage']], ['定位', k['tag']],
        ['身高', k['height']], ['體型', k['size']], ['特徵', '、'.join(k['trait'])],
        ['家園工作', '、'.join(f'[{w}](/kibo/work/#{w})' for w in k['work'])], ['掉落素材', '、'.join(k['drops'])],
        ['星彩（異色）', '有' if k['shiny'] else '無'], ['首次出現', BUILD.get(k['build'], k['build'])],
    ]
    if k.get('saddles'):
        facts.insert(8, ['騎乘', '可騎乘，鞍具：' + '、'.join(f"[{x['name_tw']}](/kibo/riding/)" for x in k['saddles'])])
    rows = []
    for kind, name in [('固定技能', k['fixed_skill'])] + [('技能', s) for s in k['skills']] + [('合擊技能', k['combo_skill'])]:
        if name:
            rows.append([name, kind, text_for(k, name, skill_text)])
    evo = []
    parents = [o for o in by_tw.values() if o['evolves_to'] == k['name_tw']]
    if parents:
        evo.append(['進化自', '、'.join(link(o['name_tw']) + (f"（等級 {o['evolve_level']}）" if o['evolve_level'] else '') for o in parents)])
    if k['evolves_to']:
        evo.append(['進化為', link(k['evolves_to']) + (f"（等級 {k['evolve_level']} 起）" if k['evolve_level'] else '')])
    if k['line']:
        evo.insert(0, ['系列', k['line']])
    work = '、'.join(k['work']) or '無'
    desc = f"{k['name_tw']}是《藍色星原：旅謠》的{k['element']}屬性奇波，{k['stage']}，家園工作：{work}。"
    body = ['## 基本資料', '', table(['項目', '內容'], facts)]
    if k['passives']:
        body += ['## 特性', '', table(['特性', '效果'], [[p['name_tw'], text_for(k, p['name_tw'], skill_text)] for p in k['passives']])]
    body += ['## 技能', '', table(['技能', '種類', '效果（等級 1）'], rows)]
    if evo:
        body += ['## 進化', '', table(['項目', '內容'], evo)]
    head = front(k['name_tw'], desc, f"公測前測試版的遊戲資料；此奇波自{BUILD.get(k['build'], k['build'])}起出現",
                 '進化後是另一隻奇波，有自己的技能、特性與家園工作；技能倍率為技能等級 1 的數值。',
                 [bwiki_source(k)], aliases=[k['name_cn'], k.get('name_en')])
    return head + '\n' + '\n'.join(body)


def kibo_index(kibo):
    rows = [[kibo_link(k), k['element'], k['stage'], k['tag'], '、'.join(k['work']), '有' if k['shiny'] else ''] for k in kibo]
    head = front('奇波列表', f'《藍色星原：旅謠》的 {len(kibo)} 隻奇波，分屬火、水、風、雷、冰、木、地、光、暗九種屬性。',
                 'BWIKI 整理的遊戲資料，2026-11-22 讀取', '同一系列的幼年期與成熟期是不同的奇波，各有自己的技能與家園工作；「（特殊）」是劇情用的另一個版本。',
                 [{'title': 'BWIKI：奇波分類', 'url': BWIKI + quote('Category:奇波')}],
                 aliases=['奇波一覽', '奇波图鉴', 'Kibo list'])
    return head + '\n## 奇波\n\n' + table(['奇波', '屬性', '階段', '定位', '家園工作', '星彩'], rows)


def kibo_work(kibo):
    jobs = {}
    for k in kibo:
        for w in k['work']:
            jobs.setdefault(w, []).append(k)
    order = sorted(jobs, key=lambda w: -len(jobs[w]))
    head = front('家園工作查詢', '《藍色星原：旅謠》奇波的家園工作：耕作、澆水、照料、採礦、伐木等，每隻奇波能做的工作不同。',
                 'BWIKI 整理的遊戲資料，2026-11-22 讀取', '一隻奇波可做多種工作；同一系列進化前後的工作可能不同。',
                 [{'title': 'BWIKI：奇波分類', 'url': BWIKI + quote('Category:奇波')}],
                 aliases=['家园工种', '奇波 家園 工作', '哪隻奇波會澆水'])
    summary = table(['工作', '奇波數'], [[f'[{w}](#{w})', len(jobs[w])] for w in order])
    parts = [head, '\n## 各工作的奇波數', '', summary]
    for w in order:
        rows = [[kibo_link(k), k['element'], k['stage'], '、'.join(x for x in k['work'] if x != w)] for k in jobs[w]]
        parts += [f'## {w}', '', table(['奇波', '屬性', '階段', '其他工作'], rows)]
    return '\n'.join(parts)


def kibo_riding(kibo):
    ride = [k for k in kibo if k.get('saddles')]
    head = front('騎乘查詢', f'《藍色星原：旅謠》有 {len(ride)} 隻奇波可以騎乘，每隻要用牠專用的鞍具。',
                 'BWIKI 整理的遊戲資料（鞍具 44 種），2026-11-22 與 2026-11-25 讀取；二測與三測加入的鞍具',
                 '騎乘一隻奇波要先捕捉到牠，再做出牠專用的鞍具；鞍具只對應一隻奇波，進化前後也不通用。',
                 [{'title': 'BWIKI：鞍具分類', 'url': BWIKI + quote('Category:鞍具')}],
                 aliases=['奇波 騎乘', '坐騎', '坐骑', '鞍具', '哪些奇波可以騎'], verified='2026-11-25')
    rows = [[kibo_link(k), k['element'], k['size'], k['stage'], '、'.join(f"{x['name_tw']}（{x['rarity'].replace('5星', '五星')}）" for x in k['saddles'])] for k in ride]
    two = [k['name_tw'] for k in ride if len(k['saddles']) > 1]
    lead = f"{'、'.join(two)}有兩種鞍具，其他奇波各一種。" if two else '每隻奇波各有一種鞍具。'
    return head + '\n## 可騎乘的奇波\n\n' + lead + '\n\n' + table(['奇波', '屬性', '體型', '階段', '鞍具'], rows)


ELEMENT_SLUG = {'火': 'fire', '水': 'water', '風': 'wind', '雷': 'thunder', '冰': 'ice', '木': 'wood', '地': 'earth', '光': 'light', '暗': 'dark', '無': 'none'}


def kibo_by_element(kibo):
    """Element -> Kibo; a Kibo of two elements is listed under each."""
    by = {}
    for k in kibo:
        for e in k['element'].split('、'):
            by.setdefault(e, []).append(k)
    return {e: by[e] for e in ELEMENTS if e in by}


def kibo_elements(kibo):
    """The summary page: how many Kibo per element, each linking its element page."""
    by = kibo_by_element(kibo)
    head = front('屬性查詢', '《藍色星原：旅謠》的奇波分九種屬性：火、水、風、雷、冰、木、地、光、暗，部分奇波兼有兩種。',
                 'BWIKI 整理的遊戲資料，2026-11-22 讀取', '一隻奇波可以有兩種屬性，因此各屬性的奇波數相加多於奇波總數；奇波的屬性決定牠技能的傷害屬性，與角色的屬性分開計算。',
                 [{'title': 'BWIKI：奇波分類', 'url': BWIKI + quote('Category:奇波')}],
                 aliases=['奇波 属性', '奇波 元素'])
    rows = [[f'[{e}屬性奇波](/kibo/elements/{ELEMENT_SLUG[e]}/)', len(by[e])] for e in by]
    return head + '\n' + table(['屬性', '奇波數'], rows)


def kibo_element_page(e, ks):
    head = front(f'{e}屬性奇波', f"《藍色星原：旅謠》的 {len(ks)} 隻{e}屬性奇波，其中 {sum(bool(k.get('saddles')) for k in ks)} 隻可以騎乘。",
                 'BWIKI 整理的遊戲資料，2026-11-22 讀取', '部分奇波兼有兩種屬性；同一系列進化前後是不同的奇波，各有自己的技能與家園工作。',
                 [{'title': 'BWIKI：奇波分類', 'url': BWIKI + quote('Category:奇波')}],
                 aliases=[f'{e}屬性奇波', tw2s.convert(f'{e}屬性奇波'), f'{e}系奇波'])
    rows = [[kibo_link(k), k['element'], k['stage'], k['tag'], '、'.join(k['work']), '可' if k.get('saddles') else ''] for k in ks]
    return head + '\n' + f'## {e}屬性奇波\n\n' + table(['奇波', '屬性', '階段', '定位', '家園工作', '騎乘'], rows)


def lingzi_page(items, texts, intro):
    rows = [[x['name_tw'], x['class'] or '', f"{x['stat']} {x['stat_1']} → {x['stat_100']}",
             f"{x['hp_100']} / {x['atk_100']} / {x['def_100']}",
             f"**{texts[x['name_tw']]['skill']}** 一星：{game_text(texts[x['name_tw']]['one'])} 滿星：{game_text(texts[x['name_tw']]['full'])}"] for x in items]
    head = front('靈子', intro['description'], f"BWIKI 整理的遊戲資料（三測），2026-11-22 讀取；共 {len(items)} 種靈子",
                 intro['caveat'], [{'title': 'BWIKI：靈子分類', 'url': BWIKI + quote('Category:灵子')},
                                   {'title': '《藍色星原：旅謠》「恆序觀測」玩法機率公告（台港澳官方網站，2026-11-26）：靈子的台服名稱',
                                    'url': 'https://azurpromilia.jimi-global.com/home/news/detail/912439441941991424'}],
                 aliases=['灵子', '靈子 是什麼', '靈子列表', '靈子 專武'])
    parts = [head, '\n## 數值與取得', '', intro['lead'], '']
    for r in ('SSR', 'SR', 'R'):
        group = [row for row, x in zip(rows, items) if x['rarity'] == r]
        if group:
            parts += [f'## {r} 靈子', '', f'共 {len(group)} 種。', '',
                      table(['靈子', '職業', '副屬性（等級 1 → 100）', '生命 / 攻擊 / 防禦（等級 100）', '技能（一星，滿星）'], group)]
    return '\n'.join(parts)


# ---------------------------------------------------------------- element advantage

def elements_page():
    e = load('elements.json')
    order = e['order']

    def rate(atk, enemy):
        return 25 if enemy in e['strong'][atk] else -25 if enemy in e['weak'][atk] else 0
    single = [[a, '、'.join(e['strong'][a]) or '—', '、'.join(e['weak'][a]) or '—'] for a in order + ['無']]
    pairs = [(x, y) for i, x in enumerate(order) for y in order[i + 1:]]
    dual = [[f'{x}、{y}'] + [f'{100 + rate(a, x) + rate(a, y)}%' for a in order] for x, y in pairs]
    head = front('屬性克制', '《藍色星原：旅謠》的屬性克制：七種屬性各克制兩種、被兩種克制，光與暗互相克制，無屬性不克制也不被克制。',
                 '公測前測試版的遊戲資料，2026-11-25 讀取；BWIKI 與日服 wikiru 的表相同',
                 '克制時傷害 +25%、被克時 −25%；敵人有兩種屬性時兩者分別計算後相加，範圍是 50% 到 150%。',
                 e['sources'], aliases=['屬性相剋', '元素克制', '属性相性表', 'element weakness'], verified='2026-11-25')
    body = ['## 單一屬性', '', table(['攻擊屬性', '傷害 125% 的敵人屬性', '傷害 75% 的敵人屬性'], single),
            '## 雙屬性敵人', '', table(['敵人屬性'] + [f'{a}攻擊' for a in order], dual)]
    return head + '\n' + '\n'.join(body)


def main():
    chars = load('characters.json')
    kibo = load('kibo.json')
    text_dir = RECORDS / 'text' / 'characters'
    written = set()
    kibo_by_cn = {k['name_cn']: k for k in kibo}
    for c in filter(released, chars):
        f = text_dir / f"{c['slug']}.json"
        if f.exists():
            write(f"characters/{c['slug']}.md", character_page(c, json.loads(f.read_text(encoding='utf-8')), kibo_by_cn))
            written.add(c['slug'])
    write('characters/index.md', characters_index(chars, written))
    skill_text = GAMETEXT['kibo']
    by_tw = {k['name_tw']: k for k in kibo}
    # A skill name whose level-1 text differs between Kibo must be keyed `name@fingerprint`.
    fps = {}
    for k in kibo:
        for name, fp in k.get('skill_fp', {}).items():
            fps.setdefault(name, set()).add(fp)
    for name, text in list(skill_text.items()):
        if '@' not in name and len(fps.get(name, ())) > 1:
            raise SystemExit(f'gametext.json: "{name}" has {len(fps[name])} different texts in the game data; key it as {name}@<fingerprint>')
    pages = 0
    for k in kibo:
        names = [k['fixed_skill'], k['combo_skill'], *k['skills'], *[p['name_tw'] for p in k['passives']]]
        # A page only once every skill and trait has text.
        if all(text_for(k, n, skill_text) for n in names if n):
            KIBO_PAGES.add(k['slug'])
    by_tw.update({k['name_tw']: k for k in kibo})
    for k in kibo:
        if k['slug'] in KIBO_PAGES:
            write(f"kibo/{k['slug']}.md", kibo_page(k, by_tw, skill_text))
            pages += 1
    write('kibo/index.md', kibo_index(kibo))
    write('kibo/work.md', kibo_work(kibo))
    write('kibo/elements.md', kibo_elements(kibo))
    for e, ks in kibo_by_element(kibo).items():
        write(f'kibo/elements/{ELEMENT_SLUG[e]}.md', kibo_element_page(e, ks))
    write('kibo/riding.md', kibo_riding(kibo))
    # 靈子: one page, written only once every 靈子 of the records has text.
    lz_path = RECORDS / 'lingzi.json'
    if lz_path.exists():
        items, texts = load('lingzi.json'), GAMETEXT['lingzi']
        intro = json.loads((RECORDS / 'text' / 'lingzi.json').read_text(encoding='utf-8'))
        if all(x['name_tw'] in texts for x in items):
            write('systems/lingzi.md', lingzi_page(items, texts, intro))
    write('systems/elements.md', elements_page())
    print('characters with pages:', len(written), 'kibo pages:', pages)


if __name__ == '__main__':
    main()
