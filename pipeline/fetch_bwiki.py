"""Fetch the wikitext of named BWIKI categories into cache/bwiki/ (not committed).

BWIKI (wiki.biligame.com/ap/) is CC BY-NC-SA 3.0. Only facts are taken from it; its wording
and table layouts are not reused, and no copy of the wikitext is committed. The fetch is
bounded: the members of the categories named below, through the MediaWiki API with curl, 10 titles
per request, one request every 20 seconds; resumable when the firewall blocks.

Usage: python3 -I pipeline/fetch_bwiki.py [category ...]   (default: 角色 奇波 鞍具)
Writes cache/bwiki/<category>.json: {title: {revid, timestamp, wikitext}}.
"""

import json
import subprocess
import sys
import time
import urllib.parse
from pathlib import Path

API = 'https://wiki.biligame.com/ap/api.php'
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0 Safari/537.36'
OUT = Path(__file__).resolve().parent.parent / 'cache' / 'bwiki'


class Blocked(Exception):
    """The firewall refused the request (HTTP 567); the address is blocked for a while."""


def call(params):
    url = API + '?' + urllib.parse.urlencode({**params, 'format': 'json'})
    # curl, not urllib: the site's firewall answered urllib with HTTP 567 and then refused
    # every request from the address for a while (2026-11-22).
    out = subprocess.run(['curl', '-sS', '--fail', '-A', UA, '-H', 'Accept: application/json', '-H', 'Accept-Language: zh-CN,zh;q=0.9', url],
                         capture_output=True, text=True, timeout=90)
    if out.returncode:
        raise Blocked(out.stderr.strip())
    time.sleep(20)
    return json.loads(out.stdout)


def members(category):
    titles, cont = [], {}
    while True:
        d = call({'action': 'query', 'list': 'categorymembers', 'cmtitle': f'Category:{category}', 'cmlimit': 500, 'cmnamespace': 0, **cont})
        titles += [m['title'] for m in d['query']['categorymembers']]
        if 'continue' not in d:
            return titles
        cont = {'cmcontinue': d['continue']['cmcontinue']}


def pages(titles, out, save):
    """Adds the pages of `titles` missing from `out`, saving after each request."""
    todo = [t for t in titles if t not in out]
    for i in range(0, len(todo), 10):
        d = call({'action': 'query', 'prop': 'revisions', 'rvprop': 'ids|timestamp|content', 'rvslots': 'main', 'titles': '|'.join(todo[i:i + 10])})
        for p in d['query']['pages'].values():
            rev = p['revisions'][0]
            out[p['title']] = {'revid': rev['revid'], 'timestamp': rev['timestamp'], 'wikitext': rev['slots']['main']['*']}
        save()
    return out


def main():
    """Resumable: pages already in the cache are kept. Exit 3 when blocked; run again later."""
    cats = sys.argv[1:] or ['角色', '奇波', '鞍具']
    OUT.mkdir(parents=True, exist_ok=True)
    try:
        for cat in cats:
            file = OUT / f'{cat}.json'
            data = json.loads(file.read_text(encoding='utf-8')) if file.exists() else {}
            listing = OUT / f'{cat}.titles.json'
            titles = json.loads(listing.read_text(encoding='utf-8')) if listing.exists() else members(cat)
            listing.write_text(json.dumps(titles, ensure_ascii=False), encoding='utf-8')
            save = lambda: file.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding='utf-8')
            pages(titles, data, save)
            print(f'{cat}: {len(data)} of {len(titles)} pages')
    except Blocked as e:
        print(f'blocked: {e}')
        sys.exit(3)


if __name__ == '__main__':
    main()
