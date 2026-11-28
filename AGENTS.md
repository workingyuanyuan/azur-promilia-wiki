# Rules for agents maintaining this site

This site is an unofficial wiki for the game Azur Promilia (藍色星原：旅謠 / 蓝色星原：旅谣; developed by 積咪網路, published by 蠻啾網路 Manjuu). Its first readers are AI agents; humans come second. The rules in `../AGENTS.md` apply; this file holds what is specific to this site.

Published 2026-11-22 at `https://yuanaruru.com/azur-promilia-wiki/` (repository `workingyuanyuan/azur-promilia-wiki`, listed in the user site), after the owner's confirmation. State on 2026-11-22: the look, the motion (with the starfield) and the character cutouts are approved. Written: 23 character pages (every released character; 洛卿 waits for its version), 207 Kibo pages, the lookups (家園工作, 騎乘, one page per element), systems. 靈子: one generated page, `systems/lingzi` (75, from BWIKI category `灵子`; skill text from `records/gametext.json`, intro in `records/text/lingzi.json`). The servers page `systems/servers` (2026-11-26): operators, the text language of each service (the language each service's App Store listing declares), voice languages (settings screenshots posted on PTT for the Taiwan and Japanese services, Nexon's announcement for Korean voice), account rules (official notices and the Japanese terms of use) and the mainland phone rebinding (one customer-service reply posted on NGA, named in the sentence). Mainland and Korean voice options beyond that are left out until a source shows them. The game's public launch (公測) is 2026-11-26 in mainland China, Taiwan / Hong Kong / Macau, Japan and Korea. There is no English service; an English open beta is announced for summer 2027.

## Decisions by the owner (2026-11-22)

- Timing: write the pages now from the test builds (星至測試, 恆序測試 and earlier) and correct them against the launch build after 2026-11-26. The advisors had all three proposed waiting for launch data; the owner chose to write now. `appliesTo` of every page names the build its facts come from, so that the pass after launch can find every page still resting on a test build.
- Languages: Traditional Chinese at the root, Simplified Chinese (`/zh-cn/`) written by script from it, with a name table for the names where the mainland service differs from the Taiwan service. Page addresses are ASCII slugs (official romanization where there is one, else pinyin or an internal id), so that `/ja/`, `/ko/` or `/en/` can be added later without changing URLs. Not English at the root: the game has almost no official English names.
- 奇波 (Kibo): lookup tables across entries (work, riding and traversal, element, where caught) and one page per 奇波, all generated from records.
- Official art: used, as on `endfield-wiki` and `nte-wiki`, credited in the `art` field. No fan-content guideline of Manjuu or the Taiwan publisher was found on 2026-11-22. Yostar's guideline for the Japanese service (`azurpromilia.jp/terms/guidelines`) forbids works that copy official illustrations directly with little originality; the owner confirmed the use of official art the same day with that guideline in view. Character art: the 12 character illustrations of the Taiwan official site's character section (`webstatic.jimi-global.com/.../home/assets/background-*.png`, 16:9 on an opaque light ground), cut out with `pipeline/cut_art.py` (anime-seg matte, whole figure, a soft fade where the figure runs off the canvas, never a straight cut through the figure) and saved as `public/art/characters/<slug>.webp` (at most 720 × 880, transparent, shown with no frame). The site has no official transparent image of them, so the cutout is ours: on the page it links to the original PNG, which `records/art.json` names, and the page notes credit the official site and the original (owner, 2026-11-22). The page of a character with both a file and an `art.json` entry shows it. The other 11 characters with a page (2026-11-25) show the game's own card art (スプラッシュアート) as the Japanese fan wiki wikiru hosts it, as given, scene included, only resized to at most 880 px. Art is not cut out as a rule (owner decision, 2026-11-25): an image that comes on its own transparent ground and shows no trace of a cutout made by a wiki is taken as the game's asset and shown as it is. Checked the same day: the ten cards are painted vignettes with soft alpha, floating debris and particles, and no matting halo; 星臨者 is a figure pair on a transparent ground (palette PNG). The picture links to the wikiru page of the character; the page notes credit that page and the file (`records/art.json`, `source: "wikiru"`). wikiru has the same kind of card for the 12 characters with official art; those keep the official cutout. The same site shows Kibo art with English file names (`airay`, `gusthawk`, ...); not used yet, because the names they map to are shown only on click.
- Player research from the NGA board of the game (`bbs.nga.cn`, `fid=510587`, mainland players) may serve as a source (2026-11-26), as on `nte-wiki` and `endfield-wiki`. `systems/combat` (damage formula, marks and 超限, 架勢, co-op scaling) rests on the guide 「蓝原伤害乘区初探(旅迹测试)」 (`tid=47612632`, 666bj, 2026-09-23) alone: its first section names the source once, and `appliesTo` names the 旅跡測試 build. Its tables of mark effects, 超限 effects and Kibo aptitudes are images in the post, read on 2026-11-26. Terms follow the game text on the character pages (星鳴技, 架勢槽, 超限, 印記); terms the game text lacks (反制技, 霸體, 部位傷害倍率) are the guide's, converted by `s2tw`. Check against the launch build when a player retests it.
- Guide videos on Bilibili may serve as a source (2026-11-27), for the community section 社群攻略 (`/community/`, root rules: Community section) and, under the rule for a lone secondary source, for facts. Four launch-day videos were read that day (`BV1A4ymzKEmY`, `BV11R17ztEXK`, `BV1oPyBzFEcf`, `BV1qwySzcEkk`), transcribed locally; no transcript or frame is kept in the repository. What they showed for the fact pages: the launch build changed many character kits (星臨者's 星鳴技 cooldown 12 → 24 s, 諾諾's team attack bonus 8% → 15%, 海悠悠's 星鳴技 gives one 火印記 at once and one on the next two-stage 重擊), while the BWIKI character pages were last revised 2026-11-21, before launch; the housing system (buildings, 增效 points, Kibo posting, 家園幣) and gear (five slots, 品階, 升星, sub-stat levels summed across gear) have no page yet.
- Home page key visual (2026-11-26, root rule): the poster of the Taiwan official site's home page (`webstatic.jimi-global.com/.../home/assets/poster-*.jpg`, 3840 × 2160, no lettering), resized to 1200 px as `public/art/key-visual.webp`.

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
pnpm scout search 蓝色星原 强度榜 --since 2026-11-26   # newest guide videos on Bilibili; * = already a source
pnpm scout read BV1KH1HzqECe   # a guide's description, tags, pinned comment and pictures, the creator's replies (to $TMPDIR/scout; BILIBILI_COOKIES = cookie file for all comments)
pnpm preview     # serve dist/ with charset=utf-8 (scripts/preview.mjs)
python3 -I pipeline/fetch_bwiki.py 角色 奇波 鞍具 灵子   # refill cache/bwiki/ (resumable; exit 3 = blocked, run again later)
```

## Content rules

- Never edit `src/content/docs/zh-cn/` or a generated page by hand. Generated: `characters/` (except hand-written ones listed in `pipeline/build_pages.py`), `kibo/`. Hand-written: `index.md`, `systems/` except `systems/lingzi.md`, `systems/elements.md` and `systems/housing.md`, which are generated.
- Game text (owner decision, 2026-11-25): the skill and trait text of characters, Kibo and 靈子 is the game's own expression. The pages show it as BWIKI gives it, converted from Simplified to Traditional characters by OpenCC `s2tw` and nothing else: markup removed, line breaks joined with a space, and the names that the Taiwan official site spells otherwise replaced by that spelling. Character skills use the template filled with level-1 values where the template is complete, else the written text (the passive in slot 5 of every character). `pipeline/gametext.py` writes `records/gametext.json`; `scripts/to-zh-cn.py` turns it back into BWIKI's Simplified text (the round trip was exact on 811 Kibo texts and every character text line checked). Where the Taiwan service publishes its own text (launch build, official pages), that text replaces the conversion. Until 2026-11-25 the pages carried this text restated in our own words, which the root rules forbid; it was removed.
- Text the site writes itself: `records/text/characters/<slug>.json` (description, scope, caveat, lead, the note above the skill table, the kind of each skill) and `records/text/lingzi.json`. `pipeline/check_text.py char <slug>` checks it: fields present, description length, a lead that does not follow the character's introduction, the prose patterns.
- To check against the launch build: weapons in the record that do not match the kit (芃芃 弓, 夏兒 雙刀); 芃芃's element (BWIKI 火、地; wikiru 火 only); values that differ between test builds (wikiru's 卡塔露 counter shield lasts 10 s, BWIKI's 24 s).
- Launch-build changes (2026-11-27): until launch-build game text replaces the test-build text, each character page has a section 公測改動, below the skill table it qualifies, written from `records/launch_changes.json`: the changes against the third test that the on-screen cards of one Bilibili video list (`BV1qwySzcEkk`, 丸子), restated as facts; the intro sentence names that source because it stands alone. Numbers before the arrow match the test-build text (multipliers are the skill-level-12 values; two passives give the value at 3 stacks). An independent reader compared the records with the cards; vague items without a direction were left out. `systems/combat` names the same video for the change in how 超限 damage is calculated. Remove a character's entry once its skill text comes from the launch build.
- A skill slot that the game data leaves empty (no name, no text) is left off the page. A record value 未知 is left off the page.
- Riding: a Kibo can be ridden when a saddle (`鞍具`) names it (`为骑行<Kibo>准备的鞍具`); `records/kibo.json` field `saddles`. Which ones fly is not in the data; the pages do not say.
- Kibo are linked from the home page in two steps through one page per element (`kibo/elements/<fire|water|…>`): one index of 207 links does not fit in 5,000 characters of Markdown.
- The story copies of a Kibo carry （特殊） only in the BWIKI page title; the records add it to the name.
- A character page exists only when its text file exists; a Kibo page only when every skill and trait of it has text. Index and lookup pages list every character and Kibo, linked where a page exists.
- Characters that the game data dates after 1.0 with no date (`1.x`, `2027年xx月`) stay out of the pages (next-version content). 洛卿 is one (2026-11-22).
- Names: `records/names_tw.json` holds the Taiwan official names and romanizations (12 characters, from the official site's character section). Other Traditional names are the mainland name converted (`name_tw_source: "converted"`); replace them from the launch build. The rate notices of 2026-11-26 (pool lists, images) give the Taiwan names of the 20 standard characters and of every SR and R 靈子: all match the records except the R 靈子 禁呪, which the Taiwan service spells 禁咒. `records/names_tw_lingzi.json` holds the 靈子 names that differ from the conversion (from the 恆序觀測 notice's pool list); `build_records.py` and `gametext.py` apply it to the 靈子 and to its skill, which bears the 靈子's name (2026-11-26). Slugs: official romanization, else the game's English name from BWIKI (`英文名`), else pinyin.
- Element of a character can be two (`地、火`).
- Element advantage (`systems/elements.md`) is generated from `records/elements.json`: which element deals 125% or 75% to which, and the sums for an enemy with two elements. BWIKI's 元素 page and wikiru's 属性相性表 were compared cell by cell on 2026-11-25 and agree.
- Japanese-service names of the characters: `records/names_ja.json` (24, from wikiru), matched to the records by the Japanese voice actor that BWIKI gives; ペイペイ and ポンポン share one, so they are matched by element, and メイプル, 星臨者 and 洛卿 by name. Shown in the facts table as 日服名稱 and as an alias. wikiru has no Japanese Kibo names (its list holds 12 Kibo under their Chinese names), and its アニマ names have no key that ties them to a 靈子; neither is used.
- `pipeline/check_prose.py` runs first in `pnpm verify`.

- Community section 社群攻略 (2026-11-27, root rules: Community section): `pipeline/build_community.py` (called from `build_pages.py`) writes `community/`, `community/tier-list`, `community/teams`, `community/damage` and `community/housing` (家園配置) from `records/community/`: `sources.json` (one record per video: creator, title, date, version, the conditions the creator states, the creator's own tiers) and `claims.json` (one record per tier row, team row, team damage figure or 靈子 comparison, with the second of the video it is shown at or the id of the creator's comment that carries it). Read from the charts on screen (tier lists of 叫我棉被, 春風滿馬, 丸子; team charts of 叫我棉被, team cards of 春風滿馬), checked by an independent reader (Gemini) against the frames: 96 of 96 matched, one option in small print was added. Each tier keeps its source's scale; table rows follow the character list. The pages say what two sources or more share (the same end of their scales; the same three-person team) and nothing the site judges itself. 瀧瀧瀧ii's damage figures (2026-11-27) are read from the picture of the creator's pinned comment and one reply of the creator under a viewer's question, checked by Gemini against the picture. 家園配置 (2026-11-27): 春風滿馬's build order of the home facilities and Kibo per work from the two pictures of the pinned comment of `BV1yky2zKEAu`, and 11 pieces of advice from the pictures and the narration (local speech recognition); Gemini checked them against the pictures and 45-second audio clips: it corrected which Kibo carry 及其进化体, the ≥ in the trait order and the crop 月麻 (heard as 亚麻), and misread one label (主产), which a zoomed crop settled. Facility names resolve against `records/housing.json`. Two videos read 2026-11-28: 叫我棉被's 塗山小玉 guide (`BV1VQ1WzRER9`: three team cards with each member's Kibo, and a 靈子 chart that puts each 靈子 at 滿階 and 1 階 against 花之舞 1 階 = 100%) and 打遊戲的老二's beginner guide (`BV1Wey6z7E8p`: two 塗山小玉 teams with Kibo and a free 忒拉拉 team); read from the frames and the burned-in subtitles, checked by Gemini against the frames. Its gear, 定弦 and skill advice is not recorded: gear names have no records yet. A team row may carry `member_kibo` (main first); in 兩份以上都列出的隊伍 the videos of one creator count as one source. Every rating and team links its video at the second it is shown (`?t=`) or the creator's comment (`#reply<id>`); `checkCommunity` in `scripts/check-page-text.mjs` fails a table row (or header), list item or paragraph of the section without such a link, and the rubric's `names-source` turns around under `community/`. Fact pages, the character pages included, never link the section.

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
| `records/launch_changes.json` | Launch-build changes per character, from one Bilibili video (section 公測改動) |
| `records/housing.json` | The home (家園): facilities, the work each takes, outputs (BWIKI item pages, third test), the launch mines (666bj), pasture products; written to `systems/housing` |
| `records/community/` | Community section: `sources.json` (one record per guide video) and `claims.json` (one per tier row, team row, damage figure or 靈子 comparison); written to pages by `pipeline/build_community.py` |
| `pipeline/scout_guides.py` | `pnpm scout`: Bilibili search and the comments of a guide, for finding sources; writes nothing to the repository |
| `records/names_tw_lingzi.json` | Taiwan names of 靈子 that differ from the converted mainland name |
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
| Japanese official site `azurpromilia.jp` (Yostar) | `robots.txt` allows every crawler | English names of Kibo (`records/kibo_en.json`). Read again 2026-11-26: its 5 characters bear the names wikiru gives; its pre-download notice gives the same requirements as the Taiwan FAQ (no iOS memory) and the launch at 11:00 JST, which is 10:00 UTC+8 |
| NGA 玩家社區 `bbs.nga.cn`, board `fid=510587` (read 2026-11-26) | No `robots.txt` (404); no licence. The first request answers 403 with a `ngaPassportUid` cookie and, in the page's script, a value `guestJs=<time>_<id>`; send both, with a `bbs.nga.cn` Referer, 3 s apart; a `guestJs` made up from the clock is refused. Pages are GBK. Images load from `img.nga.cn` (`img.nga.178.com` does not resolve here) | `systems/combat`; `systems/housing` (`tid=47985685`, 666bj, written with AI help as its author states: only its work-per-facility table, matched by a video, and its launch mines, named in the sentence); player questions |
| App Store listings of the four services (read 2026-11-26 through the iTunes lookup API) | Store metadata | Text language of each service (`languageCodesISO2A`), the seller of each app |
| PTT `www.ptt.cc` C_Chat | `robots.txt` disallows ClaudeBot and carries `Content-Signal: search=yes, ai-train=no, use=reference`. Two named posts read (M.1795514834.A.EA5, M.1795508022.A.982) with the `over18` cookie, and the settings screenshots they link; no copy kept | Voice languages of the Taiwan and Japanese services |
| Inven Global | No licence | Korean voice of the Korean service (Nexon's announcement, 2026-05-18) |
| Bilibili `www.bilibili.com` (read 2026-11-27) | `robots.txt` disallows no video page for any crawler and has no `Content-Signal`; no licence. Videos fetched with yt-dlp and the account cookies; HTTP 567 on one CDN mirror: take another format id. `pnpm scout` finds and reads guides (search; description, tags, pinned comment with its pictures, the creator's replies) | Guides of named players for the community section; leads for the fact pages |
| Not used (read 2026-11-26) | | The mainland official site `azurpromilia.manjuu.com` is a launch page (download, pre-launch events, 塗山小玉 and 源千代) with no notice list or game data. `ap-cbt3.csxylic.com` is a fan site of CBT3 client data (0.3.0; `robots.txt` disallows ClaudeBot, `Content-Signal: search=yes, ai-train=no, use=reference`); its 75 靈子 are BWIKI's 75, test data. `hyazurpromiliawiki.com` is a personal wiki whose lists hold placeholders |

## Agent test

2026-11-22, site only (12 questions, one Claude Sonnet reader, one run, local): 11 pass, 1 partial, 0 fail with 20 fetches; `tests/agent-eval/results/2026-11-22/scores.md`. The baseline on BWIKI and Bahamut was not run (BWIKI's firewall blocked the address; Bahamut refuses non-browser fetchers); run both after launch.

## Questions people ask (2026-11-22)

From Bahamut 哈啦板 titles, NGA titles (2026-11-26) and the guides read; Traditional Chinese, with the Simplified wording where it differs.

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
| 台服、日服、陸服差在哪？哪一服有中文？ | systems/servers |
| 有沒有英文版／國際服？ | home |
| 有 PC 版、PS5 版嗎？ | home |
| 靈子是什麼？ | systems/lingzi |
| 家園有哪些設施？哪隻奇波做什麼工作？／蓝原家园设施 产出 | systems/housing |
| 牧場放什麼奇波產什麼？哪隻奇波產奶、產蛋？ | systems/housing |
| 家園先蓋什麼？家園奇波推薦／家园设施优先级 | community/housing |
| 傷害怎麼算？暴擊、等級壓制、超限傷害怎麼算？／蓝原伤害公式 伤害乘区 | systems/combat |
| 架勢條多長？破韌值多少？星結合擊怎麼觸發？ | systems/combat |
| 日服能設中文嗎？／日服能设置中文么（NGA, 2026-11-26） | systems/servers |
| 台服有日配嗎？ | systems/servers |
| 帳號能不能換綁手機？／这游戏不能换绑吗（NGA, 2026-11-26） | systems/servers |
| 沒滿級抓的奇波跟滿級抓的有差嗎？（NGA, 2026-11-26） | not answered yet |
