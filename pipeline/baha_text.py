"""Print the text of the first post (and replies with -a) of a saved Bahamut forum page.

Usage: python3 -I pipeline/baha_text.py cache/baha/p532.html [-a]
"""
import html
import re
import sys

t = open(sys.argv[1], encoding='utf-8', errors='ignore').read()
title = re.search(r'<title>(.*?)</title>', t, re.S)
print('==', html.unescape(title.group(1).strip()) if title else '?')
posts = re.findall(r'<div class="c-article__content">(.*?)</div>\s*</article>', t, re.S)
for body in posts[: None if '-a' in sys.argv else 1]:
    body = re.sub(r'<br\s*/?>|</div>|</p>', '\n', body)
    body = re.sub(r'<img[^>]*data-src="([^"]+)"[^>]*>', r'[img \1]', body)
    body = re.sub(r'<[^>]+>', '', body)
    print(re.sub(r'\n\s*\n+', '\n', html.unescape(body)).strip())
    print('--')
