# Agent test

Checks whether an agent with only a fetch tool answers questions about the game better from this site than from the community wiki and the forum where the game's facts are kept.

## Files

| File | Role |
| --- | --- |
| `questions.json` | The questions with the expected answer, the qualifier that is easy to miss, and the page that holds them. Written by the author of the site from the game data, the official card-pool images and the launch notices |
| `fetch.mjs` | The fetch tool given to the agent. Modelled on the MCP reference Fetch server: main-article extraction, Markdown output, 5,000 characters per call, `start_index` to continue. Every call is logged to `runs/<run>.log` |
| `results/<date>/` | Answers and fetch logs of each recorded run |

## How to run

1. Build the site with a local address and serve it:

```
SITE_URL=http://127.0.0.1:4398/azur-promilia-wiki pnpm build
pnpm preview
```

2. Give a fresh agent the questions (without the expected answers), the fetch command below as its only source, a start URL, and a budget of 3 fetches per question.

```
node tests/agent-eval/fetch.mjs --run <run-name> --q <question-id> <url> [start_index]
```

Start URL for this site: `http://127.0.0.1:4398/azur-promilia-wiki/`. Start URLs for the baseline: `https://wiki.biligame.com/ap/` (BWIKI; its firewall may block a fetch) and `https://forum.gamer.com.tw/B.php?bsn=79865` (Bahamut board). The Taiwan official site is left out: its `robots.txt` disallows AI fetchers and its pages are drawn by script.

3. Score each answer against `questions.json`: pass needs the answer and the qualifier; partial is one of the two or an unverified inference; fail is a wrong or missing answer.

4. Run `pnpm verify` afterwards so that `dist/` carries the public address again.

## Search test

Checks whether an agent that starts from a question, with no URL, finds this site. It runs on the live site once its pages are indexed. It is a record, not a gate for publishing.

1. Give a fresh agent the questions from `questions.json` (without the expected answers, and without this site's name or address), a web search tool, and the fetch command above as its only way to read a page. No start URL.
2. Record the search tool, the queries the agent made and its answers. The fetch log holds the URLs it read.
3. Score each question: pass needs a page of this site among the pages read, and the answer with its qualifier. Record "not found" when no page of this site was read.
