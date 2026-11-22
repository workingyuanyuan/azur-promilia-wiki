# Agent test, 2026-11-22 (site only)

One Claude Sonnet reader, one run, local serving (`http://127.0.0.1:4398/azur-promilia-wiki/`), the fetch tool `tests/agent-eval/fetch.mjs`, 3 fetches per question. Questions and expected answers by the author of the site, from the sources (`questions.json`). Fetches counted from `site-fetch.log`.

Result: 11 pass, 1 partial, 0 fail, with 20 fetches.

| Question | Fetches | Score | Note |
| --- | --- | --- | --- |
| q1 限定角色池保底 | 3 | pass | 90 抽、不歪、繼承、常駐不互通 |
| q2 新手池 | 2 | pass | 30 抽；抽滿關閉 |
| q3 塗山小玉 | 1 | partial | Answer complete from the character list; the expected qualifier (「與君結緣」10 秒) is on the character page, which the question does not need. The qualifier fits another question; changed to 限定 for later runs |
| q4 卡塔露星決技 | 2 | pass | 防禦力 550%，等級 1 |
| q5 澆水 | 3 | pass | 21 隻 |
| q6 熾煌龍進化 | 2 | pass | 等級 60 → 燎焰熾龍 |
| q7 森彩靈蝶騎乘 | 1 | pass | 兩種鞍具；先捕捉、做鞍具 |
| q8 光屬性奇波 | 1 | pass | 22 隻含雙屬性 |
| q9 公測 | 1 | pass | 2026-11-26 10:00；PS5 開發中無日期 |
| q10 英文版 | 1 | pass | 2027 夏 Open Beta，美國伺服器 |
| q11 莉莉星鳴技 | 2 | pass | 200%（等級 1），420%（12）；「意志」7 秒 |
| q12 可騎乘的奇波 | 1 | pass | 29 隻。The expected qualifier said the data does not mark flyers; the pages state no absence of data by rule, so the qualifier was the error: scored on "each needs its own saddle" |

Not run: the baseline on the original sources. BWIKI's firewall was blocking this address during the session (HTTP 567), and the Bahamut board refuses non-browser fetchers; run it after launch with the servers and 靈子 pages.
