// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
import sitemap from '@astrojs/sitemap';
import starlightLinksValidator from 'starlight-links-validator';
import { sitemapOptions } from './src/lib/sitemap.mjs';
import { ORIGIN, BASE, TITLE, DESCRIPTION } from './src/lib/site.mjs';
import { satteri } from '@astrojs/markdown-satteri';
import { hastBase, hastFootnotes } from './src/lib/hast-base.mjs';
import { KIBO, KIBO_TABLES } from './src/lib/kibo-nav.mjs';

export default defineConfig({
	site: ORIGIN,
	base: BASE || undefined,
	trailingSlash: 'always',
	// Content links are written without the sub-path; this adds it in the HTML.
	markdown: { processor: satteri({ hastPlugins: [hastBase, hastFootnotes] }) },
	integrations: [
		// Added here so that it takes options; Starlight then leaves its own copy out.
		sitemap(sitemapOptions()),
		starlight({
			title: TITLE,
			description: DESCRIPTION,
			defaultLocale: 'root',
			locales: {
				root: { label: '繁體中文', lang: 'zh-TW' },
				'zh-cn': { label: '简体中文', lang: 'zh-CN' },
			},
			sidebar: [
				{
					label: '角色',
					translations: { 'zh-CN': '角色' },
					items: [{ autogenerate: { directory: 'characters' } }],
				},
				{
					label: '奇波',
					translations: { 'zh-CN': '奇波' },
					items: [
						{ slug: 'kibo' },
						...KIBO_TABLES.map((slug) => ({ slug: `kibo/${slug}` })),
						{
							label: '奇波一覽',
							translations: { 'zh-CN': '奇波一览' },
							collapsed: true,
							items: KIBO.map((k) => ({ slug: `kibo/${k.slug}` })),
						},
					],
				},
				{
					label: '系統',
					translations: { 'zh-CN': '系统' },
					items: [{ autogenerate: { directory: 'systems' } }],
				},
				{
					label: '社群攻略',
					translations: { 'zh-CN': '社群攻略' },
					items: [{ slug: 'community' }, { slug: 'community/tier-list' }, { slug: 'community/teams' }, { slug: 'community/damage' }, { slug: 'community/housing' }, { slug: 'community/builds' }],
				},
			],
			customCss: ['@fontsource/noto-serif-tc/700.css', '@fontsource/noto-serif-sc/700.css', './src/styles/promilia.css'],
			components: {
				// Three overrides: the site name with its links, the answer above the body with the page notes after it, and the theme buttons.
				SiteTitle: './src/components/SiteTitle.astro',
				MarkdownContent: './src/components/MarkdownContent.astro',
				ThemeSelect: './src/components/ThemeSelect.astro',
			},
			routeMiddleware: './src/routeData.ts',
			credits: false,
			pagination: false,
			expressiveCode: {
				themes: ['night-owl', 'github-light'],
				// `patch` gets diff colours but keeps the literal +/- in the page text.
				// The `diff` language is not used: Expressive Code draws its +/- with CSS,
				// so an agent reading the HTML would not see which lines were added or removed.
				shiki: { langAlias: { patch: 'diff' } },
				styleOverrides: { borderRadius: '0', borderWidth: '1px', frames: { shadowColor: 'transparent' } },
			},
			plugins: [
				starlightLinksValidator({
					exclude: ['/**/*.md', '/*.md', '/llms.txt', '/**/llms.txt', '/index.json', '/**/index.json', '/**/art/**'],
				}),
			],
		}),
	],
});
