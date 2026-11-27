// Shared site facts and URL rules. Plain JS so astro.config.mjs, Astro code and
// the check script all use the same rules.

// The public address, including the sub-path of a GitHub Pages project site, without a
// trailing slash. SITE_URL overrides it for local agent tests (see tests/agent-eval/README.md).
export const SITE = (process.env.SITE_URL ?? 'https://yuanaruru.com/azur-promilia-wiki').replace(/\/+$/, '');
/** Scheme and host of SITE. */
export const ORIGIN = new URL(SITE).origin;
/** Sub-path the site is served under: `/azur-promilia-wiki`, or the empty string at a domain root. */
export const BASE = new URL(SITE).pathname.replace(/\/+$/, '');
export const TITLE = { 'zh-TW': '藍色星原 Wiki', 'zh-CN': '蓝色星原 Wiki' };
export const DESCRIPTION =
	'《藍色星原：旅謠》(Azur Promilia) 的非官方資料站：角色、奇波、系統與社群攻略。';

/** Root-relative address for an `href` or `src` in HTML: the site path behind BASE. */
export function withBase(path) {
	return BASE + path;
}

/**
 * Locales: `dir` is the content sub-folder and URL prefix ('' = root); `maxDescription` is the
 * length limit of the one-sentence answer, in characters. A language may lack pages for a
 * time: `records/pending.json` lists the root pages it does not have yet.
 */
export const LOCALES = [
	{ dir: '', lang: 'zh-TW', label: '繁體中文', maxDescription: 70 },
	{ dir: 'zh-cn', lang: 'zh-CN', label: '简体中文', maxDescription: 70 },
];

/** Starlight's route data gives the home page an empty id; the collection calls it `index`. */
export function pageId(id) {
	return id === '' ? 'index' : id;
}

/** Locale of a content entry id such as `characters/lily`, `zh-cn/characters/lily`, `index`, `zh-cn`. */
export function localeOf(id) {
	return (
		LOCALES.find((l) => l.dir && (id === l.dir || id.startsWith(l.dir + '/'))) ?? LOCALES[0]
	);
}

/** Entry id without its locale prefix. The home page is `index` in every locale. */
export function bareId(id) {
	const { dir } = localeOf(id);
	if (!dir) return id;
	return id === dir ? 'index' : id.slice(dir.length + 1);
}

/** Entry id of the same page in another locale. */
export function idInLocale(id, locale) {
	const bare = bareId(id);
	if (!locale.dir) return bare;
	return bare === 'index' ? locale.dir : `${locale.dir}/${bare}`;
}

/** Site path of the HTML page for an entry id. */
export function htmlPath(id) {
	return id === 'index' ? '/' : `/${id}/`;
}

/** Site path of the Markdown twin: drop the trailing slash, append `.md`; home is `/index.md`. */
export function mdPath(id) {
	return `/${id}.md`;
}

/** Markdown twin of an internal HTML path such as `/characters/lily/` or `/`. */
export function mdPathFromHtmlPath(path) {
	const trimmed = path.replace(/^\/+|\/+$/g, '');
	return mdPath(trimmed === '' ? 'index' : trimmed);
}

/** Site path of a language's page index: `/llms.txt`, `/zh-tw/llms.txt`. */
export function llmsPath(locale) {
	return `${locale.dir ? '/' + locale.dir : ''}/llms.txt`;
}

/**
 * The opening of each language's llms.txt: what a reader gets wrong without being told.
 * Site-specific. Keep it short: it shares the first 5,000 characters with the page list.
 */
export const LLMS_NOTES = {
	'zh-TW': {
		summary: DESCRIPTION,
		heading: '回答之前',
		notes: [
			'遊戲於 2026-11-26 在中國大陸、台港澳、日本、韓國同時公測，英文服尚未營運（英文 Open Beta 預定 2027 年夏季）。各頁的「適用範圍」寫明資料取自哪一個版本：公測前的測試版（星至測試、恆序測試等）或公測版；兩者的數值、卡池與角色可能不同。',
			'名稱與時間以台港澳服（azurpromilia.com/zh-tw/）為準，時間為 UTC+8。中國大陸服由蠻啾網路營運，帳號與伺服器分開；只在「伺服器與平台」一頁列出兩服的差異。',
			'同一個名稱有幾種寫法：台港澳服的繁體中文（艾妮絲）、中國大陸服的簡體中文（艾妮丝）、官方羅馬拼寫（Anais）。少數名稱不只是字體不同。頁面網址用官方羅馬拼寫的小寫，沒有官方拼寫時用拼音。',
			'奇波（Kibo）是可捕捉、可騎乘、可在家園工作的夥伴，與可抽取的角色是兩回事。',
			'本站並非官方網站。角色與奇波的數值讀自遊戲內文字（由 BWIKI 整理），名稱讀自官方網站與公告。技能與特性說明照 BWIKI 所載的測試版原文，由簡體字逐字轉為繁體字，不是台港澳服的正式文字。日服名稱與 11 名角色的立繪取自日文玩家 wiki（wikiru）。強度榜與配隊只在「社群攻略」一區（/community/），每項評價都標明創作者、影片與發布日期，是玩家的看法，不是遊戲資料；其他頁不引用它們。',
			'每一頁都有 Markdown 版本：去掉網址結尾的斜線，加上 `.md`。',
		],
		pages: '頁面',
		home: '首頁：各索引頁，索引頁列出所有頁面',
		full: '所有頁面合併成一個檔案',
		digest: '每一頁的答案、注意事項、日期與出處，不含內文',
		json: '所有語言的所有頁面與別名，JSON 格式',
		otherLanguage: '本索引的其他語言',
		more: '更多',
	},
	'zh-CN': {
		summary: '《蓝色星原：旅谣》(Azur Promilia) 的非官方资料站：角色、奇波、系统与社群攻略。',
		heading: '回答之前',
		notes: [
			'游戏于 2026-11-26 在中国大陆、台港澳、日本、韩国同时公测，英文服尚未运营（英文 Open Beta 预定 2027 年夏季）。各页的「适用范围」写明资料取自哪一个版本：公测前的测试版（星至测试、恒序测试等）或公测版；两者的数值、卡池与角色可能不同。',
			'名称与时间以台港澳服（azurpromilia.com/zh-tw/）为准，时间为 UTC+8。中国大陆服由蛮啾网络运营，账号与服务器分开；只在「服务器与平台」一页列出两服的差异。',
			'同一个名称有几种写法：台港澳服的繁体中文（艾妮絲）、中国大陆服的简体中文（艾妮丝）、官方罗马拼写（Anais）。少数名称不只是字体不同。页面网址用官方罗马拼写的小写，没有官方拼写时用拼音。',
			'奇波（Kibo）是可捕捉、可骑乘、可在家园工作的伙伴，与可抽取的角色是两回事。',
			'本站并非官方网站。角色与奇波的数值读自游戏内文字（由 BWIKI 整理），名称读自官方网站与公告。技能与特性说明照 BWIKI 所载的测试版原文。日服名称与 11 名角色的立绘取自日文玩家 wiki（wikiru）。强度榜与配队只在「社群攻略」一区（/zh-cn/community/），每项评价都标明创作者、视频与发布日期，是玩家的看法，不是游戏资料；其他页不引用它们。',
			'每一页都有 Markdown 版本：去掉网址结尾的斜线，加上 `.md`。',
		],
		pages: '页面',
		home: '首页：各索引页，索引页列出所有页面',
		full: '所有页面合并成一个文件',
		digest: '每一页的答案、注意事项、日期与出处，不含正文',
		json: '所有语言的所有页面与别名，JSON 格式',
		otherLanguage: '本索引的其他语言',
		more: '更多',
	},
};

/** UI labels for the facts shown on every page, in both outputs. */
export const LABELS = {
	'zh-TW': {
		appliesTo: '適用範圍',
		caveat: '注意事項',
		effectiveDate: '來源日期',
		lastVerified: '最後查證',
		aliases: '其他寫法',
		sources: '出處',
		art: '美術',
		artBy: '蠻啾網路，取自官方網站',
		markdown: 'Markdown',
		page: '頁面',
		otherLanguage: '其他語言',
		allPages: '所有頁面',
		home: '首頁',
		pageList: '所有頁面清單',
		unofficial: '非官方',
		sections: '分類',
	},
	'zh-CN': {
		appliesTo: '适用范围',
		caveat: '注意事项',
		effectiveDate: '来源日期',
		lastVerified: '最后查证',
		aliases: '其他写法',
		sources: '出处',
		art: '美术',
		artBy: '蛮啾网络，取自官方网站',
		markdown: 'Markdown',
		page: '页面',
		otherLanguage: '其他语言',
		allPages: '所有页面',
		home: '首页',
		pageList: '所有页面清单',
		unofficial: '非官方',
		sections: '分类',
	},
};

/** Format a Date (or date string) as YYYY-MM-DD. */
export function isoDate(d) {
	return new Date(d).toISOString().slice(0, 10);
}
