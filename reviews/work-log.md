# Work log

Who wrote and checked what, and the state of the work on each date. Rules are in `AGENTS.md`; results of the agent tests are in `tests/agent-eval/results/`.

## State

Published 2026-11-22 at `https://yuanaruru.com/azur-promilia-wiki/` (repository `workingyuanyuan/azur-promilia-wiki`, listed in the user site), after the owner's confirmation. State on 2026-11-22: the look, the motion (with the starfield) and the character cutouts are approved. Written: 23 character pages (every released character; 洛卿 waits for its version), 207 Kibo pages, the lookups (家園工作, 騎乘, one page per element), systems. 靈子: one generated page, `systems/lingzi` (75, from BWIKI category `灵子`; skill text from `records/gametext.json`, intro in `records/text/lingzi.json`). The servers page `systems/servers` (2026-11-26): operators, the text language of each service (the language each service's App Store listing declares), voice languages (settings screenshots posted on PTT for the Taiwan and Japanese services, Nexon's announcement for Korean voice), account rules (official notices and the Japanese terms of use) and the mainland phone rebinding (one customer-service reply posted on NGA, named in the sentence). Mainland and Korean voice options beyond that are left out until a source shows them. The game's public launch (公測) is 2026-11-26 in mainland China, Taiwan / Hong Kong / Macau, Japan and Korea. There is no English service; an English open beta is announced for summer 2027.

## Advisors (2026-11-22)

Fable, Astra and Neon were asked about the plan (`~/.local/state/delegation-log/docs-sites/20261122-ap-plan*`). Adopted from all three: Traditional Chinese root; Taiwan service with one page for mainland differences; compete on answers across entries (which 奇波 for which work or terrain and back, where caught; which characters come without pulls; banner rules with the qualifier beside them), not on depth per entry; BWIKI is CC BY-NC-SA 3.0 and holds test-build data under the same URLs, so take facts only, restate them, commit no wikitext, and record the build each fact was read from (for the game text, superseded on 2026-11-25: see `AGENTS.md`, Decisions); the Taiwan official site's `robots.txt` disallows ClaudeBot and carries `Content-Signal: search=yes, ai-train=no, use=reference`, so fetch only a bounded list of named pages and commit no copy; a second-family reader checks spending and account claims.

- Timing: write the pages now from the test builds (星至測試, 恆序測試 and earlier) and correct them against the launch build after 2026-11-26. The advisors had all three proposed waiting for launch data; the owner chose to write now. `appliesTo` of every page names the build its facts come from, so that the pass after launch can find every page still resting on a test build.

## Agent test

2026-11-22, site only (12 questions, one Claude Sonnet reader, one run, local): 11 pass, 1 partial, 0 fail with 20 fetches; `tests/agent-eval/results/2026-11-22/scores.md`. The baseline on BWIKI and Bahamut was not run (BWIKI's firewall blocked the address; Bahamut refuses non-browser fetchers); run both after launch.
