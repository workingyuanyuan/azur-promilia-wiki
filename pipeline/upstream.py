"""Compares the sources of this site with what its pages were written from. Changes no page.

upstream/README.md says what is watched, what each line of the report means and how to update
the pages.

  python3 -I pipeline/upstream.py           report. Exit 0: no difference. 1: differences.
                                            2: the check could not be made
  python3 -I pipeline/upstream.py --write   also record the notices and BWIKI category members
                                            seen and the fingerprints of the cited notices in
                                            upstream/manifest.json (exit 0 whatever it reports;
                                            2 without writing when the check could not be made)

Watched:
  1. The notice list of the Taiwan official site (the announcement API that the site's news page
     calls, every page of it). A new banner (觀測) or update notice is a difference, and so is a
     notice that matches no known kind; activities, pre-download and other previews are notes.
  2. The text of every cited notice: a SHA-256 in the manifest.
  3. The BWIKI pages that the records were built from (`source.revid` in records/characters.json,
     lingzi.json and kibo.json, the saddles of a Kibo included), and any other BWIKI page a page
     cites by `oldid=` (元素), against their newest revision.
  4. The members of the BWIKI categories 角色, 奇波, 灵子 and 鞍具: a member that no record or
     manifest entry knows is a difference.

UPSTREAM_SKIP_BWIKI=1 skips 3 and 4 and says so in a note.
"""

import hashlib
import html
import json
import os
import re
import subprocess
import sys
import time
import urllib.parse
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / 'src' / 'content' / 'docs'
MANIFEST = ROOT / 'upstream' / 'manifest.json'
WRITE = '--write' in sys.argv

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0 Safari/537.36'
TZ = timezone(timedelta(hours=8))

NOTICE_API = 'https://api-grp-rgn1.jimi-global.com/announce/web/announcement/'
NOTICE_PAGE = 'https://azurpromilia.jimi-global.com/home/news/detail/'
NOTICE_LINK = re.compile(r'https://azurpromilia\.jimi-global\.com/home/news/detail/(\d+)')
PAGE_SIZE = 10  # the API answers code 1 to a pageSize of 20

BWIKI_API = 'https://wiki.biligame.com/ap/api.php'
BWIKI_GAP = 8  # seconds between BWIKI requests: its firewall blocks the address after a few quick ones
# Seconds before each retry: its firewall refuses about one request in four at random (HTTP 567),
# and refuses longer runs after other quick requests from the same address.
BWIKI_RETRY = (20, 60, 180)
BWIKI_TRIES = len(BWIKI_RETRY) + 1
BWIKI_BATCH = 50
OLDID = re.compile(r'https://wiki\.biligame\.com/ap/index\.php\?title=([^&\s]+)&oldid=(\d+)')
# Category -> the record file whose entries carry `source: {title, revid}`. The 鞍具 pages give
# the `saddles` of records/kibo.json, each with its own source.
CATEGORIES = {'角色': 'characters', '奇波': 'kibo', '灵子': 'lingzi', '鞍具': None}

# Kinds of a new notice, by title. The first that matches wins.
KINDS = [
    ('new banner notice', re.compile(r'觀測|卡池|祈願')),
    ('new update notice', re.compile(r'版本|更新說明|更新公告|改版|維護公告|停機維護')),
]
# Titles of notices that no page rests on: previews, pre-download, events, store news.
NOTE_TITLE = re.compile(r'預下載|預約|預告|直播|網頁活動|抽獎|轉發|社群|商城|周邊|聯動預熱|公平營運')


class NotMade(Exception):
    """The comparison could not be made."""


def curl(url, headers=(), timeout=60):
    # No --compressed: BWIKI's firewall answers a request that asks for gzip with HTTP 567.
    args = ['curl', '-sS', '--fail', '-A', UA, '--max-time', str(timeout)]
    for h in headers:
        args += ['-H', h]
    try:
        out = subprocess.run(args + [url], capture_output=True, text=True, timeout=timeout + 10)
    except subprocess.TimeoutExpired:
        raise NotMade(f'{url.split("?")[0]}: no answer in {timeout} s')
    if out.returncode:
        raise NotMade(f'{url.split("?")[0]}: {out.stderr.strip() or f"curl exit {out.returncode}"}')
    return out.stdout


# ---- Taiwan official notices -------------------------------------------------------------------

def notice_api(path, params):
    """GET with the signature that the official site's script adds: md5(milliseconds + sorted query)."""
    query = '&'.join(f'{k}={params[k]}' for k in sorted(params))
    ts = str(int(time.time() * 1000))
    sign = hashlib.md5((ts + query).encode()).hexdigest()
    body = curl(f'{NOTICE_API}{path}?{query}', ['lang: zh-Hant', f'timestamp: {ts}', f'sign: {sign}',
                                                 'content-type: application/json',
                                                 'referer: https://azurpromilia.jimi-global.com/'])
    time.sleep(1)
    try:
        d = json.loads(body)
    except ValueError:
        raise NotMade(f'notice API {path}: not JSON')
    if not isinstance(d, dict):
        raise NotMade(f'notice API {path}: unexpected answer')
    return d


def notice_list():
    rows, page, total = [], 1, None
    while True:
        d = notice_api('pagelatestlist', {'page': page, 'pageSize': PAGE_SIZE})
        data = d.get('data')
        if d.get('code') != 0 or not isinstance(data, dict) or not isinstance(data.get('rows'), list):
            raise NotMade(f'notice list page {page}: {d.get("code")} {d.get("msg")}')
        if total is not None and data.get('total') != total:
            raise NotMade(f'the notice list changed while it was read ({total} then {data.get("total")} notices): run again')
        total = data.get('total')
        rows += data['rows']
        if len(rows) >= total:
            break
        if not data['rows']:
            raise NotMade(f'the notice list ended at {len(rows)} notices, not the {total} it states')
        page += 1
    ids = {r.get('id') for r in rows}
    if len(ids) != total or len(rows) != total or None in ids:
        raise NotMade(f'the notice list gave {len(ids)} distinct notices in {len(rows)} rows, not the {total} it states')
    if any(not r.get('title') or not r.get('startTime') for r in rows):
        raise NotMade('a notice in the list has no title or start time: the form of the list changed')
    return {r['id']: {'title': r['title'].strip(), 'date': day(r['startTime']), 'type': r['type']} for r in rows}


def notice_text(nid):
    """(title, SHA-256 of the text) of one notice, or (None, reason) when the API answers with an error code."""
    d = notice_api('getdetail', {'id': nid})
    if d.get('code') != 0 or not d.get('data'):
        return None, f'API code {d.get("code")}: {d.get("msg")}'
    if not d['data'].get('contentUrl') or not d['data'].get('title'):
        raise NotMade(f'notice {nid}: no contentUrl or title in the answer: the form of the API changed')
    page = curl(d['data']['contentUrl'])
    page = re.sub(r'<(script|style)\b[^>]*>.*?</\1>', ' ', page, flags=re.S | re.I)
    text = re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', page))).strip()
    if not text:
        raise NotMade(f'notice {nid}: empty text')
    return d['data']['title'].strip(), hashlib.sha256(text.encode()).hexdigest()


def notice_or_none(nid):
    """notice_text, asked twice before a notice counts as gone: (title, sha) or (None, reason)."""
    got = notice_text(nid)
    if got[0] is None:
        time.sleep(5)
        got = notice_text(nid)
    return got


def day(ms):
    return datetime.fromtimestamp(int(ms) / 1000, TZ).strftime('%Y-%m-%d')


def kind_of(n):
    if n['type'] != 'notice':
        return None
    for kind, pattern in KINDS:
        if pattern.search(n['title']):
            return kind
    if NOTE_TITLE.search(n['title']):
        return None
    return 'new notice to classify'


# ---- BWIKI -------------------------------------------------------------------------------------

_last_bwiki = 0.0


def bwiki(params):
    global _last_bwiki
    wait = _last_bwiki + BWIKI_GAP - time.time()
    if wait > 0:
        time.sleep(wait)
    url = BWIKI_API + '?' + urllib.parse.urlencode({**params, 'format': 'json'})
    for attempt in range(BWIKI_TRIES):
        try:
            body = curl(url, ['Accept: application/json', 'Accept-Language: zh-CN,zh;q=0.9'], timeout=90)
            break
        except NotMade as e:
            if attempt == BWIKI_TRIES - 1:
                raise NotMade(f'BWIKI: {e} (HTTP 567 is its firewall: run again in a few minutes)')
            time.sleep(BWIKI_RETRY[attempt])
        finally:
            _last_bwiki = time.time()
    try:
        d = json.loads(body)
    except ValueError:
        raise NotMade('BWIKI: the API answered with something that is not JSON')
    if not isinstance(d, dict) or 'error' in d:
        raise NotMade(f'BWIKI: API error {d.get("error") if isinstance(d, dict) else d!r:.200}')
    return d


def category(cat):
    """{title: revid} of every member of a category (namespace 0)."""
    out, cont = {}, {}
    while True:
        d = bwiki({'action': 'query', 'generator': 'categorymembers', 'gcmtitle': f'Category:{cat}',
                   'gcmnamespace': 0, 'gcmlimit': BWIKI_BATCH, 'prop': 'revisions', 'rvprop': 'ids', **cont})
        for p in d.get('query', {}).get('pages', {}).values():
            if p.get('revisions'):
                out[p['title']] = p['revisions'][0]['revid']
        if 'continue' not in d:
            if not out:
                raise NotMade(f'BWIKI: Category:{cat} has no members: the category or the API changed')
            return out
        cont = {k: v for k, v in d['continue'].items()}


def revisions(titles):
    """{title: revid or None} for titles outside the categories read."""
    out = {}
    titles = sorted(titles)
    for i in range(0, len(titles), BWIKI_BATCH):
        d = bwiki({'action': 'query', 'prop': 'revisions', 'rvprop': 'ids', 'titles': '|'.join(titles[i:i + BWIKI_BATCH])})
        norm = {n['to']: n['from'] for n in d.get('query', {}).get('normalized', [])}
        if 'query' not in d:
            raise NotMade('BWIKI: no query in the answer to a revision request')
        for p in d['query'].get('pages', {}).values():
            out[norm.get(p['title'], p['title'])] = p['revisions'][0]['revid'] if p.get('revisions') else None
    missing = set(titles) - set(out)
    if missing:
        raise NotMade(f'BWIKI: no answer for {", ".join(sorted(missing)[:5])}')
    return out


def diff_link(title, old, new):
    return f'https://wiki.biligame.com/ap/index.php?title={urllib.parse.quote(title)}&diff={new}&oldid={old}'


# ---- What the pages were written from ----------------------------------------------------------

def root_pages():
    """The Traditional Chinese pages; zh-cn is written from them."""
    return [p for p in DOCS.rglob('*.md') if 'zh-cn' not in p.relative_to(DOCS).parts]


def page_id(p):
    return p.relative_to(DOCS).with_suffix('').as_posix()


def records():
    """{category: {title: (revid, slug)}} from the records."""
    out = {cat: {} for cat in CATEGORIES}
    for cat, name in CATEGORIES.items():
        if name:
            for r in json.loads((ROOT / 'records' / f'{name}.json').read_text(encoding='utf-8')):
                out[cat][r['source']['title']] = (r['source']['revid'], r.get('slug'))
                for s in r.get('saddles') or []:
                    out['鞍具'][s['source']['title']] = (s['source']['revid'], f'riding of {r.get("slug")}')
    return out


def main():
    if not MANIFEST.exists():
        raise NotMade(f'{MANIFEST.relative_to(ROOT)} is missing: restore it from git; a new one would take the present sources as what the pages were written from')
    manifest = json.loads(MANIFEST.read_text(encoding='utf-8'))
    known = manifest.get('notices', {})
    fingerprints = manifest.get('cited', {})
    entries = manifest.get('entries', {})
    differences, notes, summary = [], [], []

    # What the pages cite.
    cited, oldids = {}, {}
    for p in root_pages():
        text = p.read_text(encoding='utf-8')
        for nid in NOTICE_LINK.findall(text):
            cited.setdefault(nid, set()).add(page_id(p))
        for title, oldid in OLDID.findall(text):
            oldids.setdefault(urllib.parse.unquote(title), set()).add((int(oldid), page_id(p)))
    recs = records()
    by_title = {t: v for cat in recs.values() for t, v in cat.items()}
    # A BWIKI page that no record names (a hand-written page's source, such as 元素) is watched
    # at the revision the pages cite: {title: {oldid: {page, ...}}}.
    page_only = {}
    for title, cites in oldids.items():
        for oldid, page in cites:
            if title not in by_title:
                page_only.setdefault(title, {}).setdefault(oldid, set()).add(page)
                continue
            if oldid != by_title[title][0]:
                raise NotMade(f'{page} cites {title} at revision {oldid}, the record at {by_title[title][0]}: rebuild the pages from the records')

    # 1. Notices.
    notices = notice_list()
    for nid, n in sorted(notices.items(), key=lambda x: (x[1]['date'], x[0])):
        line = f'{nid}: {n["title"]} ({n["date"]}, {n["type"]}) {NOTICE_PAGE}{nid}'
        if nid in cited:
            old = known.get(nid)
            if old and (old['title'], old['date']) != (n['title'], n['date']):
                differences.append(f'cited notice changed: {nid}: list now reads "{n["title"]}" ({n["date"]}), was "{old["title"]}" ({old["date"]}); pages: {", ".join(sorted(cited[nid]))}')
            continue
        if nid in known:
            if (known[nid]['title'], known[nid]['date']) != (n['title'], n['date']):
                notes.append(f'note: notice changed: {line}')
            continue
        kind = kind_of(n)
        (differences.append(f'{kind}: {line}') if kind else notes.append(f'note: new notice: {line}'))

    # 2. Cited notices.
    new_prints = {}
    for nid in sorted(cited):
        pages = ', '.join(sorted(cited[nid]))
        got = notice_or_none(nid)
        if got[0] is None:
            differences.append(f'cited notice gone: {nid}: {got[1]}; pages: {pages}')
            continue
        title, sha = got
        new_prints[nid] = sha
        if nid not in notices:
            differences.append(f'cited notice left the list: {nid}: {title}; pages: {pages}')
        if nid not in fingerprints:
            differences.append(f'not in the manifest: {nid}: {title}; pages: {pages}')
        elif fingerprints[nid] != sha:
            differences.append(f'cited notice changed: {nid}: {title}: its text differs from the last --write; pages: {pages}')
    summary.append(f'{len(notices)} notices in the list, {len(cited)} cited notices read')

    # 3 and 4. BWIKI.
    members = {}
    if os.environ.get('UPSTREAM_SKIP_BWIKI'):
        notes.append('note: not read: BWIKI (UPSTREAM_SKIP_BWIKI); run pnpm upstream on a computer')
    else:
        for cat in CATEGORIES:
            members[cat] = category(cat)
        written = recs
        outside = {t for cat in CATEGORIES for t in written[cat] if t not in members[cat]} | set(page_only)
        elsewhere = revisions(outside) if outside else {}
        changed = 0
        for cat in CATEGORIES:
            for title, (old, slug) in sorted(written[cat].items()):
                new = members[cat].get(title, elsewhere.get(title))
                where = f'{cat}/{title}' + (f' ({slug})' if slug else '')
                if new is None:
                    differences.append(f'bwiki page gone: {where}: no page under this title')
                elif new != old:
                    changed += 1
                    differences.append(f'bwiki page changed: {where}: r{old}..r{new} {diff_link(title, old, new)}')
                if new is not None and title not in members[cat]:
                    differences.append(f'bwiki entry left the category: {where}: still a page, no longer in Category:{cat}')
            seen = set(written[cat]) | set(entries.get(cat, []))
            for title in sorted(set(members[cat]) - seen):
                differences.append(f'new bwiki entry: {cat}/{title}: https://wiki.biligame.com/ap/{urllib.parse.quote(title)}')
            for title in sorted(set(entries.get(cat, [])) - set(written[cat]) - set(members[cat])):
                notes.append(f'note: bwiki entry gone: {cat}/{title} (known, no page here)')
        for title, by_oldid in sorted(page_only.items()):
            new = elsewhere.get(title)
            for old, pages in sorted(by_oldid.items()):
                where = f'page/{title} ({", ".join(sorted(pages))})'
                if new is None:
                    differences.append(f'bwiki page gone: {where}: no page under this title')
                elif new != old:
                    changed += 1
                    differences.append(f'bwiki page changed: {where}: r{old}..r{new} {diff_link(title, old, new)}')
        summary.append(', '.join(f'{len(members[c])} in {c}' for c in CATEGORIES) + f', {len(page_only)} cited by pages only; {changed} pages written from changed')

    for line in differences + notes:
        print(line)
    print(f'{"; ".join(summary)}; {len(differences)} differences, {len(notes)} notes.')

    if WRITE:
        manifest['notices'] = {**known, **notices}
        manifest['cited'] = {**{k: v for k, v in fingerprints.items() if k in cited}, **new_prints}
        manifest.pop('saddles', None)
        if members:
            manifest['entries'] = {cat: sorted(members[cat]) for cat in CATEGORIES}
        MANIFEST.parent.mkdir(exist_ok=True)
        MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=1, sort_keys=True) + '\n', encoding='utf-8')
        print(f'wrote {MANIFEST.relative_to(ROOT)}')
        return 0
    return 1 if differences else 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except NotMade as e:
        print(f'check not made: {e}')
        sys.exit(2)
