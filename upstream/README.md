# Following the sources of this site

The pages are written from the BWIKI pages of each character, Kibo, 靈子 and saddle (test-build data until the pass after launch), the notices of the Taiwan official site, and a few news articles and Bahamut posts. `pnpm upstream` compares the sources with what the pages were written from.

```
pnpm upstream            # report. Exit 0: no difference. 1: differences. 2: the check could not be made
pnpm upstream --write    # also record the notices and BWIKI category members seen and the fingerprints of the cited notices in upstream/manifest.json
```

It changes no page and needs no token or package: Python's standard library and `curl`. It reads the Traditional Chinese pages and the records only: `zh-cn` is written from them.

## What is watched, and where the record is

| Watched | Compared with | Kept in |
| --- | --- | --- |
| The notice list of the Taiwan official site: every page of the announcement API that `azurpromilia.jimi-global.com/home/news` calls (`api-grp-rgn1.jimi-global.com/announce/web/announcement/pagelatestlist`, signed as the site's script signs it: `sign` = MD5 of the milliseconds in `timestamp` followed by the sorted query). The reading must give as many notices as the list states | The notices known: those the pages cite (links to `azurpromilia.jimi-global.com/home/news/detail/<id>`) and those read at the last `--write`, with title and date | The pages and `manifest.json` (`notices`) |
| The text of every cited notice (`getdetail?id=<id>`, then the HTML it names, tags removed) | A SHA-256 from the last `--write` | `manifest.json` (`cited`) |
| The newest revision of each BWIKI page a record was built from: characters, Kibo, 靈子 and saddles | `source.revid` in `records/characters.json`, `kibo.json` (and in each of its `saddles`) and `lingzi.json`; the character and Kibo pages cite the same revision (`oldid=`) | The records and the pages |
| The newest revision of any other BWIKI page that a page cites by `oldid=` (元素, for `systems/elements`) | The `oldid` the pages cite | The pages |
| The members of the BWIKI categories 角色, 奇波, 灵子 and 鞍具 | The records' titles and the members read at the last `--write` | The records and `manifest.json` (`entries`) |

The first manifest (2026-11-25) holds what the pages were built from on 2026-11-22: the category members fetched into `cache/bwiki/`, and the one notice the pages cite, checked against the home page. 14 saddle pages were listed in Category 鞍具 then and never fetched; they were fetched and the riding page rebuilt with them on 2026-11-25 (43 rideable Kibo). After that `--write`, the five notices no page used yet (two banners, three to classify) were taken out of `notices` again, so that they stay reported until a page rests on them. The two banners went into `systems/gacha` the same day; on 2026-11-26 the rewards notice went into `systems/gacha`, the FAQ into the home page (platforms, requirements), and 公平營運 (account rules) became a note. The five rate notices of launch day (始源, 恆常, 恆序, 弦定, 羈點) are cited by `systems/gacha`; the launch notice (正式開啟) is a note. The manifest must exist: without it the check stops, because a new one would take the present sources as what the pages were written from.

Not watched: wikiru (`azurpromilia.wikiru.jp`: Japanese names in `records/names_ja.json`, card art in `records/art.json`, element advantage; a PukiWiki with no revision ids to cite; read it by hand when the Japanese service adds a character), the Taiwan official site's character section (its names are in `records/names_tw.json`; read it by hand when a notice announces a character), Bahamut 哈啦板 (it refuses fetchers without a browser), and the news articles (Gamersky, TapTap, Final Weapon, Games Press, Wikipedia): they report one event and are not corrected. The Taiwan official site's `robots.txt` disallows ClaudeBot and GPTBot by name and carries `Content-Signal: search=yes, ai-train=no, use=reference`; the check reads only the notice API and the notices the pages cite, keeps fingerprints, not text, and sends a browser user agent as the site's own script does. BWIKI's firewall answers HTTP 567 to every request that asks for gzip, and to about one request in four at random (tested 2026-11-25, 8 s apart): the check uses `curl` without `--compressed`, one request every 8 seconds, about 12 requests in all, and tries a refused request again after 20, 60 and 180 seconds.

## The report

One line for each difference, then the notes, then a count. A line reads `kind: id: detail`, where the id is a notice id, `<category>/<BWIKI title>` (with the page's slug where it has one), or `page/<BWIKI title>` (with the pages that cite it) for a BWIKI page that no record names.

| Line | Meaning | What to do |
| --- | --- | --- |
| `new banner notice` | A notice whose title has 觀測 (卡池, 祈願): a new banner | Add it to `systems/gacha` and to the characters it offers (類型), in both languages through the script |
| `new update notice` | A version, update or maintenance notice | Read it; update what it changes. A new version: see "After launch" below |
| `new notice to classify` | A notice that matches no known kind (FAQ, fairness, rewards) | Read it. If a page should rest on it, update or write the page; if it is a new kind of banner or update title, add the word to `KINDS` in `pipeline/upstream.py`; if notices of its kind are never needed, add a word to `NOTE_TITLE` |
| `cited notice changed` | A cited notice has another title or date in the list, or another text than at the last `--write` | Read it and update the pages it names |
| `cited notice gone` / `cited notice left the list` | The API answered a cited notice with an error code twice (the line gives the code), or it is no longer listed | Find where it went; update the pages that cite it |
| `not in the manifest` | A cited notice has no fingerprint yet | Check that the pages it names agree with it, then `--write` |
| `bwiki page changed` | A BWIKI page has a newer revision than the one its record (or, for `page/…`, the page) was built from; the line links the diff | Read the diff. For `page/…`: update the hand-written page and its `oldid`. Otherwise, a change to a fact the page shows: `fetch_bwiki.py` again (delete the page's entry from `cache/bwiki/<category>.json` first, as the fetch keeps cached pages), then `build_records.py`, `build_pages.py` and `to-zh-cn.py`. Edits that change no fact (layout, typos): rebuild anyway, so the record cites the newest revision |
| `bwiki page gone` / `bwiki entry left the category` | The page a record was built from is gone or renamed, or left its category | Find the new title (BWIKI moves pages on renames); update the record's source |
| `new bwiki entry` | A member of a category that no record knows: a new character, Kibo, 靈子 or saddle | Delete `cache/bwiki/<category>.titles.json` (the fetch keeps the member list it read first), fetch, and build its record and page; a character dated after the current version stays out (as 洛卿 did) and `--write` records it as known |
| `note: new notice` | An activity, pre-download, preview or other notice no page rests on | Nothing is due; `--write` records it as known |
| `note: notice changed` | A known notice that no page cites has a new title or date | Nothing is due |
| `note: bwiki entry gone` | A known category member without a page here left the category | Nothing is due |
| `note: not read: BWIKI` | The run skipped BWIKI (`UPSTREAM_SKIP_BWIKI`); exit 0 then says nothing about BWIKI | Run `pnpm upstream` on a computer |

`check not made` with exit 2 is not a report: fix the cause it names and run again. "HTTP 567" is BWIKI's firewall: wait a few minutes. "the notice list changed while it was read" or "gave N distinct notices … not the M it states" means a notice was added or removed between two pages, or the form of the list changed; "API error" or "has no members" means BWIKI answered without the data asked for. "cites … at revision A, the record at B" means a page was not rebuilt after its record changed: rebuild the pages.

## After launch (2026-11-26)

Every page was written from test builds. After launch, BWIKI moves to launch data and nearly every page will be reported changed. Take them by category: the characters first, then the saddles and riding, then the Kibo, then 靈子. For each, refetch, rebuild the records and pages, read the diff of the generated pages, and set `appliesTo` to the launch build where the facts now rest on it. Names from the launch build replace the converted Traditional names (`name_tw_source: "converted"`).

## After updating

1. Set `lastVerified` of each page that was read again.
2. `pnpm upstream --write`, then `pnpm upstream` until no line is left, then `pnpm verify`.
3. The owner confirms the content before the push.

`--write` records every notice read as known, every cited notice as it is now, and every category member as now. Run it after the pages agree with them, not before: a banner notice or a new saddle recorded as seen is no longer reported. It cannot hide a changed character, Kibo, 靈子 or saddle page: those revisions are read from the records.

`lastVerified` moves only for a page that was read against its sources again. A run without a difference moves nothing.
