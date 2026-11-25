# Rules for agents maintaining this site

This site is an unofficial wiki for the game Azur Promilia (藍色星原：旅謠 / 蓝色星原：旅谣; developed by 積咪網路, published by 蠻啾網路 Manjuu). Its first readers are AI agents; humans come second. The rules in `../AGENTS.md` apply; this file holds what is specific to this site.

Published 2026-11-22 at `https://yuanaruru.com/azur-promilia-wiki/` (repository `workingyuanyuan/azur-promilia-wiki`, listed in the user site), after the owner's confirmation. State on 2026-11-22: the look, the motion (with the starfield) and the character cutouts are approved. Written: 23 character pages (every released character; 洛卿 waits for its version), 207 Kibo pages, the lookups (家園工作, 騎乘, one page per element), systems. 靈子: one generated page, `systems/lingzi` (75, from BWIKI category `灵子`; skill text from `records/gametext.json`, intro in `records/text/lingzi.json`). Not yet: the servers page (which service has Chinese is a launch fact; write it from the launch notices). The game's public launch (公測) is 2026-11-26 in mainland China, Taiwan / Hong Kong / Macau, Japan and Korea. There is no English service; an English open beta is announced for summer 2027.

## Decisions by the owner (2026-11-22)

- Timing: write the pages now from the test builds (星至測試, 恆序測試 and earlier) and correct them against the launch build after 2026-11-26. The advisors had all three proposed waiting for launch data; the owner chose to write now. `appliesTo` of every page names the build its facts come from, so that the pass after launch can find every page still resting on a test build.
- Languages: Traditional Chinese at the root, Simplified Chinese (`/zh-cn/`) written by script from it, with a name table for the names where the mainland service differs from the Taiwan service. Page addresses are ASCII slugs (official romanization where there is one, else pinyin or an internal id), so that `/ja/`, `/ko/` or `/en/` can be added later without changing URLs. Not English at the root: the game has almost no official English names.
- 奇波 (Kibo): lookup tables across entries (work, riding and traversal, element, where caught) and one page per 奇波, all generated from records.
- Official art: used, as on `endfield-wiki` and `nte-wiki`, credited in the `art` field. No fan-content guideline of Manjuu or the Taiwan publisher was found on 2026-11-22. Yostar's guideline for the Japanese service (`azurpromilia.jp/terms/guidelines`) forbids works that copy official illustrations directly with little originality; the owner confirmed the use of official art the same day with that guideline in view. Character art: the 12 character illustrations of the Taiwan official site's character section (`webstatic.jimi-global.com/.../home/assets/background-*.png`, 16:9 on an opaque light ground), cut out with `pipeline/cut_art.py` (anime-seg matte, whole figure, a soft fade where the figure runs off the canvas, never a straight cut through the figure) and saved as `public/art/characters/<slug>.webp` (at most 720 × 880, transparent, shown with no frame). The site has no official transparent image of them, so the cutout is ours: on the page it links to the original PNG, which `records/art.json` names, and the page notes credit the official site and the original (owner, 2026-11-22). The page of a character with both a file and an `art.json` entry shows it. The other 11 characters with a page (2026-11-25) show the game's own card art (スプラッシュアート) as the Japanese fan wiki wikiru hosts it, as given, scene included, only resized to at most 880 px. Art is not cut out as a rule (owner decision, 2026-11-25): an image that comes on its own transparent ground and shows no trace of a cutout made by a wiki is taken as the game's asset and shown as it is. Checked the same day: the ten cards are painted vignettes with soft alpha, floating debris and particles, and no matting halo; 星臨者 is a figure pair on a transparent ground (palette PNG). The picture links to the wikiru page of the character; the page notes credit that page and the file (`records/art.json`, `source: "wikiru"`). wikiru has the same kind of card for the 12 characters with official art; those keep the official cutout. The same site shows Kibo art with English file names (`airay`, `gusthawk`, ...); not used yet, because the names they map to are shown only on click.

## Defaults taken without a separate question (2026-11-22; the owner may change them)

- Service: the Taiwan / Hong Kong / Macau service (official site `azurpromilia.com/zh-tw/`, served from `azurpromilia.jimi-global.com`), one clock UTC+8 without a label beside each time. What differs on the mainland service is stated on one page (servers and platforms), not on every page. All three advisors proposed this.
- How pages are produced: records from which a script writes the Markdown for characters, 奇波, lookup tables and the names page; hand-written Markdown for systems and the version page.
- How the home page reaches every page: index pages per section, each listing every page of its section within its first 5,000 extracted characters (the `endfield-wiki` pattern).
- Look: taken from the Taiwan official site (colours, type, layout; not its wordmark, images or fonts).
- Who lets a change go live: the owner confirms every time.
- How the site follows its sources: `pnpm upstream`, also run every day by `.github/workflows/upstream.yml`, which keeps one issue (2026-11-25; it was on demand only until then, and the command had not been written). `upstream/README.md` says what it watches and what to do with each line.
- Address: `https://yuanaruru.com/azur-promilia-wiki/`.

## Advisors (2026-11-22)

Fable, Astra and Neon were asked about the plan (`~/.local/state/delegation-log/docs-sites/20261122-ap-plan*`). Adopted from all three: Traditional Chinese root; Taiwan service with one page for mainland differences; compete on answers across entries (which 奇波 for which work or terrain and back, where caught; which characters come without pulls; banner rules with the qualifier beside them), not on depth per entry; BWIKI is CC BY-NC-SA 3.0 and holds test-build data under the same URLs, so take facts only, restate them, commit no wikitext, and record the build each fact was read from (for the game text, superseded on 2026-11-25: see Content rules); the Taiwan official site's `robots.txt` disallows ClaudeBot and carries `Content-Signal: search=yes, ai-train=no, use=reference`, so fetch only a bounded list of named pages and commit no copy; a second-family reader checks spending and account claims.

## Commands

```
uv run --with opencc-python-reimplemented --with pypinyin python3 -I pipeline/build_records.py   # cache/bwiki -> records/characters.json, records/kibo.json
uv run --with opencc-python-reimplemented python3 -I pipeline/build_pages.py                     # records -> generated root pages
uv run --with opencc-python-reimplemented python3 -I scripts/to-zh-cn.py                         # root pages -> src/content/docs/zh-cn/
uv run -q --with opencc-python-reimplemented --with pypinyin python3 -I pipeline/check_text.py char <slug>   # the site's own text of one character (also: char-src, the character's source)
uv run -q --with opencc-python-reimplemented --with pypinyin python3 -I pipeline/gametext.py   # cache/bwiki -> records/gametext.json (the game's skill and trait text)
node scripts/prose-review.mjs run      # after pnpm build: a reader of another model reads every unit of prose not yet in reviews/prose-ledger.json
node scripts/prose-review.mjs status   # units of prose the ledger lacks
pnpm verify      # prose check, build, acceptance checks
pnpm upstream    # compare the official notices and BWIKI pages with what the pages were written from; changes no page (upstream/README.md)
pnpm preview     # serve dist/ with charset=utf-8 (scripts/preview.mjs)
python3 -I pipeline/fetch_bwiki.py 角色 奇波 鞍具 灵子   # refill cache/bwiki/ (resumable; exit 3 = blocked, run again later)
```

## Content rules

- Never edit `src/content/docs/zh-cn/` or a generated page by hand. Generated: `characters/` (except hand-written ones listed in `pipeline/build_pages.py`), `kibo/`. Hand-written: `index.md`, `systems/` except `systems/lingzi.md` and `systems/elements.md`, which are generated.
- Game text (owner decision, 2026-11-25): the skill and trait text of characters, Kibo and 靈子 is the game's own expression. The pages show it as BWIKI gives it, converted from Simplified to Traditional characters by OpenCC `s2tw` and nothing else: markup removed, line breaks joined with a space, and the names that the Taiwan official site spells otherwise replaced by that spelling. Character skills use the template filled with level-1 values where the template is complete, else the written text (the passive in slot 5 of every character). `pipeline/gametext.py` writes `records/gametext.json`; `scripts/to-zh-cn.py` turns it back into BWIKI's Simplified text (the round trip was exact on 811 Kibo texts and every character text line checked). Where the Taiwan service publishes its own text (launch build, official pages), that text replaces the conversion. Until 2026-11-25 the pages carried this text restated in our own words, which the root rules forbid; it was removed.
- Text the site writes itself: `records/text/characters/<slug>.json` (description, scope, caveat, lead, the note above the skill table, the kind of each skill) and `records/text/lingzi.json`. `pipeline/check_text.py char <slug>` checks it: fields present, description length, a lead that does not follow the character's introduction, the prose patterns.
- To check against the launch build: weapons in the record that do not match the kit (芃芃 弓, 夏兒 雙刀); 芃芃's element (BWIKI 火、地; wikiru 火 only); values that differ between test builds (wikiru's 卡塔露 counter shield lasts 10 s, BWIKI's 24 s).
- A skill slot that the game data leaves empty (no name, no text) is left off the page. A record value 未知 is left off the page.
- Riding: a Kibo can be ridden when a saddle (`鞍具`) names it (`为骑行<Kibo>准备的鞍具`); `records/kibo.json` field `saddles`. Which ones fly is not in the data; the pages do not say.
- Kibo are linked from the home page in two steps through one page per element (`kibo/elements/<fire|water|…>`): one index of 207 links does not fit in 5,000 characters of Markdown.
- The story copies of a Kibo carry （特殊） only in the BWIKI page title; the records add it to the name.
- A character page exists only when its text file exists; a Kibo page only when every skill and trait of it has text. Index and lookup pages list every character and Kibo, linked where a page exists.
- Characters that the game data dates after 1.0 with no date (`1.x`, `2027年xx月`) stay out of the pages (next-version content). 洛卿 is one (2026-11-22).
- Names: `records/names_tw.json` holds the Taiwan official names and romanizations (12 characters, from the official site's character section). Other Traditional names are the mainland name converted (`name_tw_source: "converted"`); replace them from the launch build. Slugs: official romanization, else the game's English name from BWIKI (`英文名`), else pinyin.
- Element of a character can be two (`地、火`).
- Element advantage (`systems/elements.md`) is generated from `records/elements.json`: which element deals 125% or 75% to which, and the sums for an enemy with two elements. BWIKI's 元素 page and wikiru's 属性相性表 were compared cell by cell on 2026-11-25 and agree.
- Japanese-service names of the characters: `records/names_ja.json` (24, from wikiru), matched to the records by the Japanese voice actor that BWIKI gives; ペイペイ and ポンポン share one, so they are matched by element, and メイプル, 星臨者 and 洛卿 by name. Shown in the facts table as 日服名稱 and as an alias. wikiru has no Japanese Kibo names (its list holds 12 Kibo under their Chinese names), and its アニマ names have no key that ties them to a 靈子; neither is used.
- `pipeline/check_prose.py` runs first in `pnpm verify`.

## Skin rules

- `src/styles/promilia.css`: night-blue ground, pale lavender text, star gold `#f0d58c` (dark) / `#c9962a` (light) as the mark colour only, periwinkle links, soft corners and pill buttons, Noto Serif TC / SC (Fontsource, SIL OFL, weight 700) for titles, headings, the site name and the sidebar groups.
- Motion (owner decision, 2026-11-22; motion that keeps going, as the root rules ask of a game wiki), taken from the official site's own motion measured that day (rise of 0.4rem with fade, ease cubic-bezier(0.333, 0, 0.3, 1), staggered delays, a light sweep, 0.2–0.33 s pointer responses). Once: the header's section links drop in, the star before the site name twinkles, a star-gold glint runs along the foot of the header, the title and first blocks rise in, each section heading, table and the page notes rise in when first scrolled into view with its star twinkling, and pages cross-fade while header and sidebar stay still. Keeps going: a starfield of two blurred layers on `body::before` / `::after` drifts up (one tile in 240 s and 300 s) and the near stars brighten and dim over 7 s; a mask keeps it out of the text column only, so it shows behind both sidebars (the stars behind the table of contents kept by owner decision, 2026-11-25; behind the left sidebar since that sidebar took the page's ground the same day) and in the bands outside the centred frame, and it shows only from 72rem, where the column is centred (narrower, the column fills the space). Character art does not move; all motion inside `prefers-reduced-motion: no-preference` (the stars then stand still). Code: the starfield and motion sections of `promilia.css` and the script in `src/components/SiteTitle.astro`. Full-page screenshots need a scroll through the page first, or the sections below the first screen stay hidden.
- Favicon (`public/favicon.svg`, 2026-11-22): a gold four-pointed star and two small pale-blue stars on the night blue of the skin, drawn for this site; the first one was copied from `endfield-wiki` by mistake.
- The four-point star (U+2726) before the site name and each h2 is drawn with CSS; `scripts/check-dist.mjs` check 5 fails when it reaches page text.

## Where things are

| Path | What |
| --- | --- |
| `pipeline/fetch_bwiki.py` | BWIKI API fetch into `cache/bwiki/` (not committed) |
| `pipeline/build_records.py`, `records/` | Records: facts per character and Kibo, Taiwan names |
| `pipeline/build_pages.py`, `records/text/` | Generated pages and the text the site writes itself |
| `pipeline/check_text.py` | Check of the site's own text for one character; reads the game data (also for `gametext.py`) |
| `pipeline/cut_art.py`, `cache/art-tw/` | Character cutouts from the Taiwan official site's illustrations (cache not committed) |
| `pipeline/baha_text.py`, `cache/baha/` | Text of saved Bahamut forum posts (not committed) |
| `pipeline/upstream.py`, `upstream/` | `pnpm upstream`: what the pages were written from against the sources (`upstream/README.md`) |
| `scripts/to-zh-cn.py` | Simplified Chinese pages; names that differ come from the records |
| `src/lib/kibo-nav.mjs` | Kibo part of the sidebar |
| `scripts/prose-review.mjs`, `scripts/prose-rubric.md`, `scripts/prose-site.mjs`, `reviews/prose-ledger.json` | Prose ledger: the shared reader and rubric (copied unchanged between sites), this site's settings (it skips the game text), the units read |
| `pipeline/gametext.py`, `records/gametext.json` | The game's skill and trait text, converted to Traditional characters |
| `records/names_ja.json`, `records/elements.json`, `records/art.json` | Japanese names, element advantage, where each character picture comes from |
| `cache/wikiru/` | wikiru pages and card art (not committed) |

## Sources (read 2026-11-22; wikiru 2026-11-25)

| Source | Allows | Used for |
| --- | --- | --- |
| Taiwan official site `azurpromilia.com/zh-tw/` (served from `azurpromilia.jimi-global.com`) | `robots.txt`: ClaudeBot and GPTBot disallowed; `Content-Signal: search=yes, ai-train=no, use=reference`. Named pages only, read in a browser; no copy kept | Taiwan names and romanizations (character section of the home page), launch notices. Notices are an API that needs signed headers; the site has three notices |
| BWIKI `wiki.biligame.com/ap/` | CC BY-NC-SA 3.0; `robots.txt` allows the API. Its firewall answers HTTP 567 and blocks the address for minutes after a few requests (urllib at once; curl after about 5) | Character and Kibo data (templates 角色图鉴, 奇波图鉴); the skill and trait text, shown as given (converted to Traditional characters); element advantage (page 元素) |
| Bahamut 哈啦板 `forum.gamer.com.tw` board 79865 | No licence; read with curl and a browser user agent | Taiwan wording, player questions, relays of official Facebook posts (images transcribed by Neon) |
| Gamersky, TapTap, OSLink articles | No licence | Gacha rules of the 旅跡測試 (2026-09-17) |
| Final Weapon, Games Press | No licence | Launch platforms, English open beta (summer 2027, US server), publishers per region |
| wikiru `azurpromilia.wikiru.jp` (Japanese fan wiki) | No licence or reuse terms found; its guideline covers editing and comments. `robots.txt` allows every crawler. Fetched with curl, 3 s apart; the attachment info pages answer 403 | Japanese character names, card art of 11 characters, the element table as a second source. Its damage-formula page is its own reading of mainland CBT3 material, marked by it as untested; not used |

## Agent test

2026-11-22, site only (12 questions, one Claude Sonnet reader, one run, local): 11 pass, 1 partial, 0 fail with 20 fetches; `tests/agent-eval/results/2026-11-22/scores.md`. The baseline on BWIKI and Bahamut was not run (BWIKI's firewall blocked the address; Bahamut refuses non-browser fetchers); run both after launch.

## Questions people ask (2026-11-22)

From Bahamut 哈啦板 titles and the guides read; Traditional Chinese, with the Simplified wording where it differs.

| Question | Page |
| --- | --- |
| 藍色星原什麼時候公測？幾點開服？ | home |
| 藍原抽卡保底幾抽？限定池會不會歪？／蓝原保底多少抽 歪不歪 | systems/gacha |
| 保底會繼承到下一期嗎？ | systems/gacha |
| 新手池幾抽必出五星？要幾張票？ | systems/gacha |
| 常駐池 50 抽自選是什麼？ | systems/gacha |
| 有沒有免費的五星角色？ | systems/gacha |
| 電腦／手機跑得動嗎？配置需求？ | home |
| 手機和電腦資料互通嗎？ | home |
| 限定角色有哪些？ | characters（類型欄） |
| 哪隻奇波會澆水／耕作／照料？／蓝色星原 奇波 浇水 | kibo/work |
| 奇波怎麼進化？幾級進化？ | kibo/<slug> |
| 哪些奇波可以騎、可以飛？ | kibo/riding（能飛的不在資料裡） |
| 火屬性的奇波有哪些？ | kibo/elements/fire |
| 莉莉是什麼屬性？技能怎麼用？ | characters/<slug> |
| 台服、日服、陸服差在哪？哪一服有中文？ | to write (servers page) |
| 有沒有英文版／國際服？ | home |
| 有 PC 版、PS5 版嗎？ | home |
| 靈子是什麼？ | systems/lingzi |
