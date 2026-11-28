"""Write the community section (社群攻略, /community/) from records/community/.

Pages: community/index, community/tier-list, community/teams, community/damage, community/housing, community/builds. Every rating, team
and damage figure names its creator; each section links each source once (once_per_section): the
video, or the creator's comment under it (a chart posted as a picture, an answer to a viewer). The site never merges ratings: each
source keeps its own tiers, and rows follow the order of the character list, not a rank.
A comparison is written only where at least two sources say the same thing.
Called from pipeline/build_pages.py; Simplified Chinese is written by scripts/to-zh-cn.py.
"""

import json
import re
from pathlib import Path

from opencc import OpenCC

tw2s = OpenCC('tw2s')

ROOT = Path(__file__).resolve().parent.parent
RECORDS = ROOT / 'records'
DOCS = ROOT / 'src' / 'content' / 'docs'


def load(rel):
    return json.loads((RECORDS / rel).read_text(encoding='utf-8'))


def yaml_str(s):
    return json.dumps(s, ensure_ascii=False)


def front(title, description, applies, caveat, sources, aliases):
    lines = ['---', f'title: {yaml_str(title)}', f'description: {yaml_str(description)}', f'appliesTo: {yaml_str(applies)}',
             f'caveat: {yaml_str(caveat)}', f"lastVerified: {max(s['read'] for s in sources)}"]
    # The Simplified title is an alias of every page: scripts/to-zh-cn.py makes it the title there.
    aliases = [a for a in dict.fromkeys([*aliases, tw2s.convert(title)]) if a and a != title]
    if aliases:
        lines += ['aliases:', *[f'  - {yaml_str(a)}' for a in aliases]]
    lines.append('sources:')
    for s in sources:
        lines += [f"  - title: {yaml_str(source_title(s))}", f"    url: {s['url']}"]
    return '\n'.join(lines + ['---']) + '\n'


def source_title(s):
    return f"{s['title']}（{s['platform']}，{s['creator']}，{s['published']}）"


def table(head, rows):
    out = ['| ' + ' | '.join(head) + ' |', '| ' + ' | '.join('---' for _ in head) + ' |']
    out += ['| ' + ' | '.join(str(c).replace('|', '／') for c in r) + ' |' for r in rows]
    return '\n'.join(out) + '\n'


def at(s, claim):
    """Where a claim is shown: the video at the second (Bilibili takes `?t=` in seconds), or the
    creator's comment under the video (Bilibili opens `#reply<id>` at that comment)."""
    if 'reply' in claim:
        return f"{s['url']}#reply{claim['reply']}"
    return f"{s['url']}?t={claim['at']}"


def cite(s, claim, text=None):
    return f"[{text or s['creator']}]({at(s, claim)})"


ELEMENTS = ['火', '水', '風', '雷', '冰', '木', '地', '光', '暗', '無']
# Claims about the home (家園) and the works of its Kibo, in the order of the source's chart.
HOME = ('facility', 'job', 'advice')
# Claims about how a character is built: gear, the order of raising its slots, 定弦 to pull for.
BUILD = ('gear', 'gear_order', 'dingxian')
GEAR_SLOTS = ['上裝', '下裝', '耳環', '戒指', '武器']
JOBS = ['伐木', '採礦', '元素', '照料', '燃火', '手工', '澆水', '耕作', '鍛造']


def character_order(chars):
    """The order of the character list (pipeline/build_pages.py, characters_index)."""
    return sorted(chars, key=lambda c: (-int((c['rarity'] or '0')[0]), ELEMENTS.index(c['element']) if c['element'] in ELEMENTS else 99, c['name_tw']))


def main():
    sources = {s['id']: s for s in load('community/sources.json')['sources']}
    claims = load('community/claims.json')['claims']
    chars = {c['slug']: c for c in load('characters.json')}
    kibo = {k['slug']: k for k in load('kibo.json')}
    lingzi = {l['slug']: l for l in load('lingzi.json')}
    pages = {p.stem for p in (DOCS / 'characters').glob('*.md')}
    kibo_pages = {p.stem for p in (DOCS / 'kibo').glob('*.md')}
    facilities = {f['id']: f for f in load('housing.json')['facilities']}
    gear_records = load('gear.json')
    gear = {(i['name_tw'], i['slot']) for i in gear_records['items']}
    gear_sets = {x['name_tw'] for x in gear_records['sets']}
    for c in claims:  # every name resolves against the site's name records
        for slug in [*([c['subject']] if c['kind'] not in HOME else []), *c.get('second', []), *c.get('third', []), *c.get('team', [])]:
            if slug not in chars:
                raise SystemExit(f'records/community/claims.json: unknown character {slug}')
        if c.get('facility') and c['facility'] not in facilities:
            raise SystemExit(f"records/community/claims.json: unknown home facility {c['facility']}")
        if c.get('job') and c['job'] not in JOBS:
            raise SystemExit(f"records/community/claims.json: unknown work {c['job']}")
        for slug in [*c.get('kibo', []), *c.get('early', []), *c.get('late', []), *(k for ks in c.get('member_kibo', []) for k in ks)]:
            if slug not in kibo:
                raise SystemExit(f'records/community/claims.json: unknown Kibo {slug}')
        for slot, piece in c.get('pieces', {}).items():
            if (piece, slot) not in gear:
                raise SystemExit(f'records/community/claims.json: unknown gear {piece} ({slot})')
        if c.get('set') and c['set'] not in gear_sets:
            raise SystemExit(f"records/community/claims.json: unknown gear set {c['set']}")
        if c.get('lingzi') and c['lingzi'] not in lingzi:
            raise SystemExit(f"records/community/claims.json: unknown 靈子 {c['lingzi']}")
        if c['source'] not in sources:
            raise SystemExit(f"records/community/claims.json: unknown source {c['source']}")
        if ('at' in c) == ('reply' in c):
            raise SystemExit(f'records/community/claims.json: a claim needs one of at, reply: {c}')

    def name(slug):
        c = chars[slug]
        return f"[{c['name_tw']}](/characters/{slug}/)" if slug in pages else c['name_tw']

    def kibo_name(slug):
        k = kibo[slug]
        return f"[{k['name_tw']}](/kibo/{slug}/)" if slug in kibo_pages else k['name_tw']

    tier_sources = [s for s in sources.values() if any(c['source'] == s['id'] and c['kind'] == 'tier' for c in claims)]
    team_sources = [s for s in sources.values() if any(c['source'] == s['id'] and c['kind'] == 'team' for c in claims)]
    damage_sources = [s for s in sources.values() if any(c['source'] == s['id'] and c['kind'] in ('damage', 'lingzi') for c in claims)]
    write('community/tier-list.md', tier_page(tier_sources, claims, chars, name))
    write('community/teams.md', teams_page(team_sources, claims, chars, name, kibo_name))
    home_sources = [s for s in sources.values() if any(c['source'] == s['id'] and c['kind'] in HOME for c in claims)]
    write('community/damage.md', damage_page(damage_sources, claims, chars, lingzi, name, kibo_name))
    write('community/housing.md', housing_page(home_sources, claims, facilities, kibo_name))
    build_sources = [s for s in sources.values() if any(c['source'] == s['id'] and c['kind'] in BUILD for c in claims)]
    write('community/builds.md', builds_page(build_sources, claims, chars, name))
    write('community/index.md', index_page(sources, tier_sources, team_sources, damage_sources, home_sources, build_sources, claims, chars))


def once_per_section(text):
    """Each h2 section links each of its sources once, at its first mention (COMMUNITY.md): to the
    creator's comment when every link of the section to that video goes to that comment, else to
    the video. Later mentions keep the creator's name without a link; the records keep each
    claim's second or comment."""
    head, sep, body = text.partition('\n---\n')
    link = re.compile(r'\[([^\]]+)\]\((https?://[^)\s]+)\)')
    base = lambda u: u.split('#')[0].split('?')[0]
    out = []
    for part in re.split(r'(?m)^(?=## )', body):
        targets = {}
        for _, u in link.findall(part):
            targets.setdefault(base(u), set()).add(u)
        done = set()

        def one(m):
            b = base(m.group(2))
            if b in done:
                return m.group(1)
            done.add(b)
            us = targets[b]
            u = us.pop() if len(us) == 1 and '#reply' in next(iter(us)) else b
            return f'[{m.group(1)}]({u})'
        out.append(link.sub(one, part))
    return head + sep + ''.join(out)


def write(path, text):
    text = once_per_section(text)
    out = DOCS / path
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text, encoding='utf-8')


def creators(srcs):
    return '、'.join(dict.fromkeys(s['creator'] for s in srcs))


def applies(srcs):
    versions = sorted({s['version'] for s in srcs})
    dates = sorted({s['published'] for s in srcs})
    return f"{'、'.join(versions)}；{len(srcs)} 部 Bilibili 影片（{dates[0]}{' 至 ' + dates[-1] if len(dates) > 1 else ''} 發布，{'、'.join(sorted({s['read'] for s in srcs}))} 讀取）"


# ---------------------------------------------------------------- tier lists

def tier_page(srcs, claims, chars, name):
    tier = {(c['source'], c['subject']): c for c in claims if c['kind'] == 'tier'}
    subjects = [c for c in character_order(chars.values()) if any((s['id'], c['slug']) in tier for s in srcs)]
    lists = [[cite(s, tier[next(k for k in tier if k[0] == s['id'])]), s['conditions'], '、'.join(s['scale'])] for s in srcs]
    rows = []
    for c in subjects:
        row = [name(c['slug']), c['class']]
        for s in srcs:
            t = tier.get((s['id'], c['slug']))
            row.append(t['value'] if t else '—')
        rows.append(row)
    # Comparisons: the same end of the scale on two lists or more, whatever the tiers are called.
    agree = []
    for end, label in ((0, '最高一級'), (-1, '最低一級')):
        for c in subjects:
            on = [s for s in srcs if (s['id'], c['slug']) in tier and tier[(s['id'], c['slug'])]['value'] == s['scale'][end]]
            if len(on) >= 2:
                where = '、'.join(f"{cite(s, tier[(s['id'], c['slug'])])} {tier[(s['id'], c['slug'])]['value']}" for s in on)
                others = [s for s in srcs if s not in on and (s['id'], c['slug']) in tier]
                rest = ''.join(f"；{cite(s, tier[(s['id'], c['slug'])])}排在 {tier[(s['id'], c['slug'])]['value']}" for s in others)
                agree.append(f"- {name(c['slug'])}：{len(on)} 份榜排在{label}（{where}）{rest}。")
    n = len(srcs)
    head = front('強度榜', f"《藍色星原：旅謠》公測 1.0 的 {n} 份玩家強度榜：{creators(srcs)}為 {len(subjects)} 名角色排的梯度。",
                 applies(srcs),
                 '梯度只在各自的榜內有意義：' + '；'.join(f"{s['creator']}分 {len(s['scale'])} 級（{s['scale'][0]} 到 {s['scale'][-1]}）" for s in srcs) + '。各榜的評估條件也不同。',
                 srcs, ['强度榜', '角色強度榜', '節奏榜', 'tier list', 'Azur Promilia tier list'])
    body = ['## 各角色的梯度', '', table(['角色', '職業', *[cite(s, tier[next(k for k in tier if k[0] == s['id'])]) for s in srcs]], rows),
            '## 幾份榜的共同處', '', *agree, '',
            '## 各榜的評估條件', '', table(['創作者', '評估條件', '梯度（高到低）'], lists)]
    return head + '\n' + '\n'.join(body)


# ---------------------------------------------------------------- teams

def lineups(c):
    return {frozenset((a, b)) for a in c['second'] for b in c['third']}


def teams_page(srcs, claims, chars, name, kibo_name):
    teams = [c for c in claims if c['kind'] == 'team' and any(c['source'] == s['id'] for s in srcs)]
    mains = [c for c in character_order(chars.values()) if any(t['subject'] == c['slug'] for t in teams)]
    # A lineup two sources or more both list, main damage dealer and both teammates the same.
    both = []
    for m in mains:
        by_source = {}  # by creator: two videos of one creator count as one source
        creator_of = {s['id']: s['creator'] for s in srcs}
        for t in teams:
            if t['subject'] == m['slug']:
                by_source.setdefault(creator_of[t['source']], set()).update(lineups(t))
        common = {pair for pair in set().union(*by_source.values()) if sum(pair in v for v in by_source.values()) >= 2}
        for pair in sorted(common, key=lambda p: sorted(chars[x]['name_tw'] for x in p)):
            # Second teammate first, as the first source to list the pair has them.
            first = next(t for t in teams if t['subject'] == m['slug'] and pair in lineups(t))
            a = next(x for x in pair if x in first['second'])
            b = next(x for x in pair if x != a)
            both.append([name(m['slug']), f"{name(a)}、{name(b)}", '、'.join(sources_of(srcs, teams, m['slug'], pair))])
    body = ['## 兩份以上都列出的隊伍', '', table(['主力', '隊友', '列出的創作者'], both)]
    for m in mains:
        rows = []
        mine = [t for t in teams if t['subject'] == m['slug']]
        with_kibo = any(t.get('member_kibo') for t in mine)
        for s in srcs:
            for t in (t for t in mine if t['source'] == s['id']):
                who = cite(s, t) + (f"（{t['label']}）" if t.get('label') else '')
                row = [who, '、'.join(name(x) for x in t['second']), '、'.join(name(x) for x in t['third'])]
                if with_kibo:
                    row.append('；'.join('或'.join(kibo_name(k) for k in ks) for ks in t['member_kibo']) if t.get('member_kibo') else '—')
                rows.append(row)
        head_row = ['創作者', '2 號隊友', '3 號隊友（擇一）'] + (['奇波（主力；2 號；3 號）'] if with_kibo else [])
        body += [f"## {m['name_tw']}", '', table(head_row, rows)]
    body += ['## 各來源的條件', '', table(['創作者', '評估條件'],
                                    [[f"[{s['creator']}]({s['url']})", s['conditions']] for s in srcs])]
    head = front('配隊', f"《藍色星原：旅謠》公測 1.0 的玩家配隊：{creators(srcs)}為 {len(mains)} 名主力排的三人隊伍。",
                 applies(srcs),
                 '一列的 3 號隊友是擇一，不是同時上場；各來源的條件不同：' + '，'.join(f"{s['creator']}看{s['focus']}" for s in srcs) + '。',
                 srcs, ['配队', '隊伍搭配', '配隊推薦', 'team comp', 'Azur Promilia teams'])
    return head + '\n' + '\n'.join(body)


def sources_of(srcs, teams, main, pair):
    out, seen = [], set()
    for s in srcs:
        hit = next((t for t in teams if t['source'] == s['id'] and t['subject'] == main and pair in lineups(t)), None)
        if hit and s['creator'] not in seen:
            seen.add(s['creator'])
            out.append(cite(s, hit))
    return out


# ---------------------------------------------------------------- damage calculations

def damage_page(srcs, claims, chars, lingzi, name, kibo_name):
    ours = [c for c in claims if any(c['source'] == s['id'] for s in srcs)]
    dmg = [c for c in ours if c['kind'] == 'damage']
    mains = [c for c in character_order(chars.values()) if any(d['subject'] == c['slug'] for d in dmg)]
    by_id = {s['id']: s for s in srcs}
    rows = []
    for m in mains:
        for d in (d for d in dmg if d['subject'] == m['slug']):
            team = '、'.join(f"{name(x)}（{kibo_name(k)}）" for x, k in zip(d['team'], d['kibo'])) if d['kibo'] else '、'.join(name(x) for x in d['team'])
            who = cite(by_id[d['source']], d) + (f"（{d['note']}）" if d.get('note') else '')
            rows.append([team, d['seconds'], d['total'], d['dps'], who])
    notes = [f"- {name(k['subject'])}：{cite(by_id[k['source']], k)}寫明{k['note']}可把奇波換成{'、'.join(kibo_name(x) for x in k['kibo'])}。"
             for k in ours if k['kind'] == 'kibo']
    body = ['## 隊伍傷害', '', table(['隊伍與奇波（主力在前）', '軸長（秒）', '總傷害', '軸內 DPS', '來源'], rows)]
    if notes:
        body += [*notes, '']
    for m in mains:
        lz_all = [c for c in ours if c['kind'] == 'lingzi' and c['subject'] == m['slug']]
        if not lz_all:
            continue
        body += [f"## {m['name_tw']}的靈子", '']
        for s in (s for s in srcs if any(c['source'] == s['id'] for c in lz_all)):
            lz = [c for c in lz_all if c['source'] == s['id']]
            base = next((c for c in lz if c['ratio'] in ('100%', '100.0%')), lz[0])
            base_name = f"{lingzi[base['lingzi']]['name_tw']} {base['step']} 階"
            if base.get('team'):
                team = '、'.join(name(x) for x in base['team'])
                body += [f"- {cite(s, base)}在{team}的隊伍中比較主力的靈子，以{base_name}的隊伍傷害為 100%。", '',
                         table(['靈子', '稀有度', '階', f"隊伍傷害比（{cite(s, base)}）", '軸內 DPS'],
                               [[lingzi[c['lingzi']]['name_tw'], lingzi[c['lingzi']]['rarity'], c['step'], c['ratio'], c['dps']] for c in lz])]
            else:
                body += [f"- {cite(s, base)}比較{m['name_tw']}帶各靈子的傷害，以{base_name}為 100%。", '',
                         table(['靈子', '稀有度', '階', f"傷害比（{cite(s, base)}）"],
                               [[lingzi[c['lingzi']]['name_tw'], lingzi[c['lingzi']]['rarity'], c['step'], c['ratio']] for c in lz])]
    body += ['## 各來源的條件', '', table(['創作者', '評估條件'], [[f"[{s['creator']}]({s['url']})", s['conditions']] for s in srcs])]
    head = front('傷害計算', f"《藍色星原：旅謠》公測 1.0 的玩家傷害計算：{creators(srcs)}為 {len(mains)} 名主力的隊伍算出的總傷害、DPS 與靈子差距。",
                 applies(srcs),
                 'DPS 只在同一來源的條件內可比：' + '；'.join(f"{s['creator']}算的是{s['focus']}，{s['damage_note']}" for s in srcs) + '。',
                 srcs, ['伤害计算', '配隊傷害', 'DPS', '靈子對比', '灵子对比', 'Azur Promilia damage calculation'])
    return head + '\n' + '\n'.join(body)


# ---------------------------------------------------------------- section index

def housing_page(srcs, claims, facilities, kibo_name):
    ours = [c for c in claims if c['kind'] in HOME and any(c['source'] == s['id'] for s in srcs)]
    by_id = {s['id']: s for s in srcs}
    # Advice in the order of the fact page: gathering, then processing, then the rest.
    order = ['採集設施', *[k for k, f in facilities.items() if f['group'] == '採集'],
             '加工設施', *[k for k, f in facilities.items() if f['group'] == '加工'], '大地圖的設施']
    section = {'kuangchang': '礦場', 'muchang': '牧場', 'nongchang': '農場'}

    def kibos(c, when):
        return '、'.join(kibo_name(k) + ('及其進化型' if k in c.get('evolutions', []) else '') for k in c[when])

    def fac(fid):
        f = facilities[fid]
        return f"[{f['name_tw']}](/systems/housing/#{section.get(fid) or f['group'] + '設施'})"
    body = []
    for s in srcs:
        mine = [c for c in ours if c['source'] == s['id']]
        tiers = [c for c in mine if c['kind'] == 'facility']
        jobs = [c for c in mine if c['kind'] == 'job']
        if tiers:
            body += ['## 設施的建設先後', '',
                     f"- {cite(s, tiers[0])}把家園設施分 {len(s['scale'])} 級（{'、'.join(s['scale'])}），排的是建設先後，不是重要程度。", '',
                     table(['類別', '設施', f"建設先後（{cite(s, tiers[0])}）", '圖上的建議'],
                           [[c['group'], fac(c['facility']), c['tier'], c.get('note', '—')] for c in tiers])]
        if jobs:
            body += ['## 各工作的奇波', '',
                     f"- {cite(s, jobs[0])}的奇波推薦只看數值，比的是效率，不是工種評分；前期指 25 級前，後期指開全圖後。", '',
                     table(['工作', f"前期（{cite(s, jobs[0])}）", '後期'],
                           [[f"[{c['job']}](/kibo/work/#{c['job']})", kibos(c, 'early'), kibos(c, 'late')]
                            for c in sorted(jobs, key=lambda c: JOBS.index(c['job']))])]
    advice = [c for c in ours if c['kind'] == 'advice']
    advice.sort(key=lambda c: (order.index(c.get('facility') or c['topic']), c.get('at', 0)))
    if advice:
        body += ['## 各設施的建議', '']
        body += [f"- {fac(c['facility']) if c.get('facility') else c['topic']}：{cite(by_id[c['source']], c)}建議{c['text']}。" for c in advice]
        body.append('')
    body += ['## 來源的條件', '', table(['創作者', '條件'], [[f"[{s['creator']}]({s['url']})", s['conditions']] for s in srcs])]
    head = front('家園配置', f"《藍色星原：旅謠》公測 1.0 的玩家家園攻略：{creators(srcs)}排的設施建設先後與各工作推薦的奇波。",
                 applies(srcs),
                 '設施的 T0 到 T2 是建設先後，不是重要程度；奇波推薦比的是效率，不是工種評分。',
                 srcs, ['家园配置', '家園攻略', '家园攻略', '家園 優先級', '家园设施优先级', '家園 奇波推薦', '家园奇波推荐'])
    return head + '\n' + '\n'.join(body)


def builds_page(srcs, claims, chars, name):
    ours = [c for c in claims if c['kind'] in BUILD and any(c['source'] == s['id'] for s in srcs)]
    by_id = {s['id']: s for s in srcs}
    body = []
    for c in character_order(chars.values()):
        mine = [x for x in ours if x['subject'] == c['slug']]
        if not mine:
            continue
        body += [f"## {c['name_tw']}", '']
        gear = [x for x in mine if x['kind'] == 'gear']
        if gear:
            body.append(table(['來源', '套裝', *GEAR_SLOTS],
                              [[cite(by_id[x['source']], x, f"{by_id[x['source']]['creator']}（{x['stage']}）"),
                                f"[{x['set']}](/systems/gear/#套裝) 4 件", *[x['pieces'].get(slot, '—') for slot in GEAR_SLOTS]] for x in gear]))
        for x in mine:
            s = by_id[x['source']]
            if x['kind'] == 'gear_order':
                word = lambda slot: f"{slot}（{x['words'][slot]}）" if slot in x.get('words', {}) else slot
                body.append(f"- {cite(s, x)}的培養順序：{' > '.join(' = '.join(word(slot) for slot in group) for group in x['order'])}。")
            elif x['kind'] == 'dingxian':
                body.append(f"- {cite(s, x)}推薦抽的定弦：{'、'.join(str(n) for n in x['picks'])}。")
        body.append('')
    body += ['## 來源的條件', '', table(['創作者', '條件'], [[f"[{s['creator']}]({s['url']})", s['conditions']] for s in srcs])]
    head = front('角色養成', f"《藍色星原：旅謠》公測 1.0 的玩家養成攻略：{creators(srcs)}為主力角色選的套裝、武器、培養順序與定弦。",
                 applies(srcs),
                 '裝備名稱與部位依第三次測試的遊戲資料；公測 1.0 改了多數套裝的效果數值。',
                 srcs, ['角色养成', '裝備推薦', '装备推荐', '配裝', '配装', '定弦推薦', '定弦推荐', '畢業裝備', '毕业装备'])
    return head + '\n' + '\n'.join(body)


def index_page(sources, tier_sources, team_sources, damage_sources, home_sources, build_sources, claims, chars):
    srcs = list(sources.values())
    n_tier = len({c['subject'] for c in claims if c['kind'] == 'tier'})
    n_team = len({c['subject'] for c in claims if c['kind'] == 'team'})
    n_damage = len({c['subject'] for c in claims if c['kind'] == 'damage'})
    topics = table(['主題', '內容'], [
        ['[強度榜](/community/tier-list/)', f"{creators(tier_sources)}的 {len(tier_sources)} 份公測 1.0 強度榜，{n_tier} 名角色在各榜的梯度"],
        ['[配隊](/community/teams/)', f"{creators(team_sources)}為 {n_team} 名主力排的三人隊伍"],
        ['[傷害計算](/community/damage/)', f"{creators(damage_sources)}為 {n_damage} 名主力的隊伍算出的總傷害、DPS 與靈子差距"],
        ['[家園配置](/community/housing/)', f"{creators(home_sources)}排的家園設施建設先後與各工作推薦的奇波"],
        ['[角色養成](/community/builds/)', f"{creators(build_sources)}為主力角色選的套裝、武器、培養順序與定弦"],
    ])
    rows = [[s['creator'], s['platform'], f"[{s['title']}]({s['url']})", s['published'], s['version']] for s in srcs]
    head = front('社群攻略', f"《藍色星原：旅謠》玩家發表的強度榜、配隊、傷害計算、家園配置與角色養成：{len({s['creator'] for s in srcs})} 位 Bilibili 創作者的公測 1.0 攻略。",
                 applies(srcs),
                 '每項評價都是具名創作者的看法，各有自己的梯度與評估條件，不是遊戲資料。',
                 srcs, ['攻略', 'Azur Promilia guides'])
    body = ['## 主題', '', topics, '## 來源', '', table(['創作者', '平台', '影片', '發布日期', '遊戲版本'], rows)]
    return head + '\n' + '\n'.join(body)


if __name__ == '__main__':
    main()
