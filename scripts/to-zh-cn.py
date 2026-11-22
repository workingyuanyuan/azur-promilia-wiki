# Writes the Simplified Chinese pages (src/content/docs/zh-cn/) from the Traditional
# Chinese pages at the root (src/content/docs/, without zh-cn/). Run it after every change
# to a root page:
#
#   uv run --with opencc-python-reimplemented python3 -I scripts/to-zh-cn.py
#
# Steps: replace names that the two services write differently (taken from records/), then
# Taiwan wording with mainland wording (VOC), convert the characters (OpenCC tw2s), swap the
# title with its Simplified alias, and point links at /zh-cn/. Source URLs are kept.
# OpenCC's phrase mode (tw2sp) is not used: it rewrites game terms.

import glob
import json
import os
import re
import sys

from opencc import OpenCC

cc = OpenCC('tw2s')
root = sys.argv[1] if len(sys.argv) > 1 else 'src/content/docs'
records = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'records')

# Names: the mainland name of every character and Kibo whose Traditional name does not
# convert to it (the Taiwan service chose another name, or another character form).
NAMES = []
for f in ('characters.json', 'kibo.json'):
    path = os.path.join(records, f)
    if os.path.exists(path):
        for r in json.load(open(path, encoding='utf-8')):
            if cc.convert(r['name_tw']) != r['name_cn']:
                NAMES.append((r['name_tw'], r['name_cn']))
NAMES.sort(key=lambda p: -len(p[0]))

# Taiwan wording -> mainland wording. Applied after the names, before the character
# conversion. Add a pair when a root page brings in a Taiwan term.
VOC = [
    ('伺服器', '服务器'), ('透過', '通过'), ('帳號', '账号'), ('登入', '登录'), ('資訊', '信息'),
    ('網路', '网络'), ('台港澳', '港澳台'), ('預約', '预约'), ('軟體', '软件'), ('品質', '质量'),
]

NAMES_FIX = []


def conv(s):
    for a, b in NAMES + VOC:
        s = s.replace(a, b)
    return cc.convert(s)


def page(src, rel):
    text = open(src, encoding='utf-8').read()
    m = re.match(r'---\n(.*?)\n---\n(.*)', text, re.S)
    lines, body = m.group(1).split('\n'), m.group(2)

    unquote = lambda v: json.loads(v) if v.startswith('"') else v
    title = unquote(next(l for l in lines if l.startswith('title:'))[6:].strip())
    start = next((k for k, l in enumerate(lines) if l.startswith('aliases:')), None)
    aliases, end = [], None
    if start is not None:
        end = start + 1
        while end < len(lines) and lines[end].startswith('  - '):
            aliases.append(unquote(lines[end][4:]))
            end += 1
    # The Simplified name is an alias of the zh-tw page: it becomes the title, and the
    # Traditional title takes its place among the aliases.
    simplified = conv(title)
    if simplified != title:
        if simplified not in aliases:
            sys.exit(f'{rel}: add the alias "{simplified}" to the root page')
        aliases = [title if a == simplified else a for a in aliases]
        title = simplified

    out = []
    for k, l in enumerate(lines):
        if l.startswith('title:'):
            out.append('title: ' + json.dumps(title, ensure_ascii=False))
        elif start is not None and start < k < end:
            out.append('  - ' + json.dumps(aliases[k - start - 1], ensure_ascii=False))
        elif l.lstrip().startswith('url:'):
            out.append(l)
        else:
            out.append(conv(l))
    front = '\n'.join(out)

    if '```' in body:
        sys.exit(f'{rel}: code blocks are not handled; keep them unconverted before using them')
    body = conv(body)
    # Internal links are root-relative (/characters/lily/); the Simplified page links its own language.
    # Images under /art/ are shared by both languages and keep their path.
    body = re.sub(r'\]\((/(?!/|art/))', r'](/zh-cn\1', body)

    dst = os.path.join(root, 'zh-cn', rel)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    open(dst, 'w', encoding='utf-8').write('---\n' + front + '\n---\n' + body)


files = sorted(f for f in glob.glob(root + '/**/*.md', recursive=True) if not os.path.relpath(f, root).startswith('zh-cn' + os.sep))
for f in glob.glob(os.path.join(root, 'zh-cn', '**', '*.md'), recursive=True):
    os.remove(f)
for f in files:
    page(f, os.path.relpath(f, root))
print(len(files), 'pages written to', os.path.join(root, 'zh-cn'), '| names that differ:', len(NAMES))
