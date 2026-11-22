# 藍色星原：旅謠 Wiki

Live site: https://yuanaruru.com/azur-promilia-wiki/ (简体中文 https://yuanaruru.com/azur-promilia-wiki/zh-cn/)

An unofficial reference for the game Azur Promilia (藍色星原：旅謠 / 蓝色星原：旅谣), Taiwan / Hong Kong / Macau service. It is written first for AI agents that read with a fetch tool, and for people second: every page has a Markdown twin, the answer and its qualifier come first, and each fact is tied to a dated source.

This site is not run by 積咪網路, 蠻啾網路 or any publisher of the game.

## What is in it

| Section | Pages |
| --- | --- |
| Characters | One page per released character (23): profile, skills with values at skill levels 1 and 12 |
| Kibo | One page per Kibo (207): element, stage, home work, riding, traits, skills, evolution; lookups by home work, riding and element |
| Systems | Observation (gacha) pools and pity; 靈子 (75 equipment cards) |

Languages: Traditional Chinese at the root, Simplified Chinese under `/zh-cn/` (written by script from the Traditional Chinese pages).

The game's public launch is 2026-11-26. Until the pages are checked against the launch build, game data comes from the test builds; each page names the build in its scope.

## Sources

Game data from BWIKI (`wiki.biligame.com/ap/`, CC BY-NC-SA 3.0): facts only, restated in our own words; no wikitext is kept in this repository. Taiwan names and character art from the Taiwan official site; the character pictures are cutouts made by this site and link to the official originals. Gacha rules from the official card-pool notices as relayed on the Bahamut forum.

## For agents

- `/llms.txt` and `/zh-cn/llms.txt`: what readers get wrong, bundles, page list
- `/index.json`: every page with its scope, caveat and dates
- `<page>.md`: the Markdown twin of any page

## Build

```
pnpm install
pnpm verify
```

Rules for maintaining the site are in `AGENTS.md`.
