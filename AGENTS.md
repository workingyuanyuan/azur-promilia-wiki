# Rules for agents maintaining this site

An unofficial wiki for the game Azur Promilia (藍色星原：旅謠 / 蓝色星原：旅谣; developed by 積咪網路, published by 蠻啾網路 Manjuu), at `https://yuanaruru.com/azur-promilia-wiki/` from the public repository `workingyuanyuan/azur-promilia-wiki`. The rules in `../AGENTS.md` apply; this file holds what is specific to this site.

Read before the work: `SOURCES.md` before fetching a source or writing from one (what each allows, how to read it, what each page rests on and how it was checked, what to check against the launch build); `pipeline/README.md` before running a pipeline script (fetch, records, pages, in order); `upstream/README.md` when `pnpm upstream` reports a difference or a version lands; `../COMMUNITY.md` before working on the community section and when a version lands. Who wrote and checked what goes in `reviews/work-log.md`; the question list (`questions.md`, `questions.json`) and test results in `tests/agent-eval/`.

## Decisions

By the owner unless marked `agent`; the owner may change an agent's default.

- Timing (2026-11-22): the pages were written from the test builds and are corrected against the launch build (2026-11-26). `appliesTo` of every page names the build its facts come from, so that every page still resting on a test build can be found.
- Languages (2026-11-22): Traditional Chinese at the root, Simplified Chinese (`/zh-cn/`) written by script from it, with a name table where the mainland service differs from the Taiwan service. Page addresses are ASCII slugs (official romanization, else the game's English name from BWIKI, else pinyin), so that `/ja/`, `/ko/` or `/en/` can be added without changing URLs. The game has almost no official English names.
- Service (agent, 2026-11-22): the Taiwan / Hong Kong / Macau service, one clock UTC+8 without a label beside each time. What differs on the mainland service is stated on one page (`systems/servers`), not on every page.
- 奇波 (Kibo): lookup tables across entries (work, riding and traversal, element, where caught) and one page per 奇波, all generated from records.
- How pages are produced (agent): records from which a script writes the Markdown for characters, 奇波, lookup tables, the generated system pages and the community section; hand-written Markdown for the other system pages and the home page.
- The home page links index pages per section, each listing every page of its section within its first 5,000 extracted characters (agent); Kibo are reached in two steps through one page per element (`kibo/elements/<fire|water|…>`), because 207 links do not fit in 5,000 characters.
- Official art is used (2026-11-22), with Yostar's guideline for the Japanese service in view, which forbids works that copy official illustrations directly with little originality. The 12 characters of the Taiwan official site show its illustration, cut out by `pipeline/cut_art.py` and linked to the original PNG. The others show the game's card art as wikiru hosts it, as given, only resized, linked to the wikiru page (2026-11-25). `records/art.json` names each source.
- Game text (2026-11-25): the skill and trait text of characters, Kibo and 靈子, and the set and affix effects of gear, are the game's own expression. Pages show it as BWIKI gives it, converted to Traditional characters by OpenCC `s2tw` and nothing else, with the names the Taiwan official site spells otherwise replaced by that spelling. Where the Taiwan service publishes its own text, that text replaces the conversion.
- Player research from the game's NGA board (`fid=510587`) may serve as a source for fact pages (2026-11-26), and guide videos on Bilibili for the community section and, under the rule for a lone secondary source, for facts (2026-11-27). No transcript or frame is kept in the repository.
- Agent's defaults (2026-11-22): no BWIKI wikitext is committed, the game text of the records apart; a reader of a second model family checks claims about spending and accounts.
- Next-version content stays out: characters that the game data dates after 1.0 with no date (`1.x`, `2027年xx月`) have no page.
- Player-made tools (language patches, mods, launchers) are not a subject of the site (2026-11-28).
- Look (agent; approved 2026-11-22): taken from the Taiwan official site: night-blue ground, pale lavender text, star gold as the mark colour only, periwinkle links, soft corners and pill buttons, serif titles. Favicon: a gold four-pointed star and two small pale-blue stars on night blue.
- Motion (2026-11-22), from the official site's own motion. Once: entrances of the header links, title, first blocks and each section when first scrolled into view (its star twinkling), a twinkle of the star before the site name, a star-gold glint along the foot of the header, page cross-fades while header and sidebar stay still. Keeps going: a starfield of two blurred layers that drifts and twinkles; a mask keeps it out of the text column only, so it shows behind both sidebars and the table of contents (2026-11-25) and outside the centred frame, from 72rem. Character art does not move.
- Home page key visual: the poster of the Taiwan official site's home page (`poster-*.jpg`, no lettering).
- Agent's defaults: the owner confirms every change before it goes live; `pnpm upstream` runs every day in a workflow that keeps one issue (2026-11-25).

## Commands

```
pnpm verify      # prose check, build, acceptance checks
pnpm upstream    # compare the official notices and BWIKI pages with what the pages were written from (upstream/README.md)
pnpm preview     # serve dist/ with charset=utf-8
node scripts/prose-review.mjs run      # after pnpm build: read the prose not yet in the ledger (`status` instead of `run`: count it)
pnpm scout search 蓝色星原 强度榜 --since 2026-11-26   # newest guide videos on Bilibili; * = already a source
pnpm scout read BV1KH1HzqECe   # a guide's description, tags, pinned comment and pictures, the creator's replies (to $TMPDIR/scout; BILIBILI_COOKIES = cookie file for all comments)
uv run -q --with opencc-python-reimplemented --with pypinyin python3 -I pipeline/check_text.py char <slug>   # the site's own text of one character (char-src: its source)
```

Fetching, building the records and writing the pages: the commands and their order are in `pipeline/README.md`.

## Content rules

- Never edit by hand: `src/content/docs/zh-cn/`, `characters/` (except the hand-written ones listed in `pipeline/build_pages.py`), `kibo/`, `community/`, and `systems/lingzi`, `systems/elements`, `systems/housing`, `systems/gear`. Hand-written: `index.md` and the other pages of `systems/`.
- Game text is written by `pipeline/gametext.py` into `records/gametext.json` (how: `pipeline/README.md`); flavour text of gear is left out.
- Text the site writes itself: `records/text/characters/<slug>.json` (description, scope, caveat, lead, the note above the skill table, the kind of each skill) and `records/text/lingzi.json`, checked by `pipeline/check_text.py char <slug>`: fields present, description length, a lead that does not follow the character's introduction, the prose patterns.
- A character page exists only when its text file exists; a Kibo page only when every skill and trait of it has text. Index and lookup pages list every character and Kibo, linked where a page exists.
- Left off the page: a skill slot that the game data leaves empty, a record value 未知, and which Kibo fly (not in the data). A Kibo can be ridden when a saddle (`鞍具`) names it.
- Names: `records/names_tw.json` holds the Taiwan official names and romanizations; other Traditional names are the mainland name converted (`name_tw_source: "converted"`) and are replaced from the launch build. `records/names_tw_lingzi.json` holds the 靈子 names that differ from the conversion. Japanese-service names (`records/names_ja.json`) show in the facts table as 日服名稱 and as an alias. The story copies of a Kibo carry （特殊） in the name. A character can have two elements (`地、火`).
- While a page's game text is still the test build's, launch-build values follow it in a section of their own, below the table they qualify, and name their source in the intro sentence when it stands alone: 公測改動 on character pages (`records/launch_changes.json`), 公測的套裝效果 on `systems/gear` (`records/gear_launch.json`). Remove an entry once that text comes from the launch build.
- The Kibo pages' row 星彩（異色） shows BWIKI's field `异色`; whether it records 星彩, 閃光 or 異色 is not settled: settle it before relabeling (`SOURCES.md`).
- Community section (`../COMMUNITY.md`): `pipeline/build_community.py` writes `community/` and its pages (`tier-list`, `teams`, `damage`, `housing`, `builds`) from `records/community/sources.json` (one record per guide: creator, title, date, version, conditions, the creator's own tiers) and `claims.json` (one record per tier row, team row, damage figure, 靈子 comparison or gear choice, with the second of the video or the id of the creator's comment that carries it).
- In the community records every name resolves against the site's records: facilities against `records/housing.json`, gear by name and slot against `records/gear.json`. A team row may carry `member_kibo` (main first). The videos of one creator count as one source. Each tier keeps its source's scale; table rows follow the character list.
- Every rating and team links its video at the second it is shown (`?t=`) or the creator's comment (`#reply<id>`); `checkCommunity` in `scripts/check-page-text.mjs` fails a table row (or its header), list item or paragraph of the section without a link to its source. Fact pages, the character pages included, never link the section.
- `pipeline/check_prose.py` runs first in `pnpm verify`.

## Skin rules

- The skin is `src/styles/promilia.css`; fonts: Noto Serif TC / SC (Fontsource, SIL OFL, weight 700) for titles, headings, the site name and the sidebar groups.
- The four-point star (U+2726) before the site name and each h2 is drawn with CSS; check 5 of `scripts/check-dist.mjs` fails when it reaches page text.
- Full-page screenshots need a scroll through the page first, or the sections below the first screen stay hidden. With reduced motion the stars stand still.

## Where things are

| Path | What |
| --- | --- |
| `pipeline/`, `records/` | Fetch, records and page scripts; each script's header says what it reads and writes |
| `records/text/` | The text the site writes itself |
| `records/community/` | Sources and claims of the community section |
| `src/lib/kibo-nav.mjs` | Kibo part of the sidebar |
| `scripts/prose-site.mjs` | Prose ledger settings: it skips the game text |
