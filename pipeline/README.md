# The pipeline: fetch, records, pages

Read this before running a script in this folder. `../AGENTS.md` holds the rules and the commands every change needs; `../SOURCES.md` the sources; each script's header says what it reads and writes. Run in this order:

```
python3 -I pipeline/fetch_bwiki.py 角色 奇波 鞍具 灵子 装备   # refill cache/bwiki/ (resumable; exit 3 = blocked, run again later)
uv run --with opencc-python-reimplemented --with pypinyin python3 -I pipeline/build_records.py   # cache/bwiki -> records/characters.json, records/kibo.json
uv run -q --with opencc-python-reimplemented --with pypinyin python3 -I pipeline/gametext.py     # cache/bwiki -> records/gametext.json
uv run -q --with opencc-python-reimplemented python3 -I pipeline/build_gear.py                   # cache/bwiki/装备.json -> records/gear.json
uv run --with opencc-python-reimplemented python3 -I pipeline/build_pages.py                     # records -> generated root pages, community section included
uv run --with opencc-python-reimplemented python3 -I scripts/to-zh-cn.py                         # root pages -> src/content/docs/zh-cn/
```

| Path | What |
| --- | --- |
| `records/housing.json`, `records/elements.json`, `records/kibo_en.json` | The home (facilities, the work each takes, outputs from BWIKI item pages of the third test, the launch mines from 666bj, pasture products), element advantage, English Kibo names |
| `cache/` | Copies of sources, not committed: `bwiki/`, `art-tw/`, `baha/`, `wikiru/` |

## Game text

- Game text is written by `pipeline/gametext.py` into `records/gametext.json`: markup removed, line breaks joined with a space; character skills use the template filled with level-1 values where the template is complete, else the written text. `scripts/to-zh-cn.py` turns it back into BWIKI's Simplified text. Flavour text of gear is left out.
