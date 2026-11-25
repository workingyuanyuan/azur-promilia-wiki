// Site settings for scripts/prose-review.mjs (the prose ledger).
//
// - derived: locales a script writes from another (Simplified Chinese from Traditional,
//   scripts/to-zh-cn.py); their prose is the root locale's, converted, and is read there.
// - skip(path, lang): text the page shows as the game gives it (records/gametext.json, written by
//   pipeline/gametext.py): the skill and trait text of characters, Kibo and 靈子, and the names of
//   those skills. It is the game's text, not the site's prose. Each line is looked up on its own,
//   because a table cell joins the lines with a space.

import { readFileSync } from 'node:fs';

const json = (rel) => JSON.parse(readFileSync(new URL(`../${rel}`, import.meta.url), 'utf8'));
const lines = (texts) => texts.flatMap((t) => (t || '').split('\n')).map((s) => s.trim()).filter(Boolean);

export default {
	derived: ['zh-cn'],
	skip(path) {
		const bare = path.replace(/^zh-cn\//, '');
		const g = json('records/gametext.json');
		const ch = /^characters\/([a-z0-9-]+)\/$/.exec(bare);
		if (ch && g.characters[ch[1]]) return lines(Object.values(g.characters[ch[1]]).flatMap((s) => [s.name, s.text]));
		if (/^kibo\/[a-z0-9-]+\/$/.test(bare) && !/^kibo\/(work|riding|elements)\/$/.test(bare)) {
			const kibo = json('records/kibo.json').find((k) => `kibo/${k.slug}/` === bare);
			if (!kibo) return [];
			const names = [kibo.fixed_skill, kibo.combo_skill, ...kibo.skills, ...kibo.passives.map((p) => p.name_tw)].filter(Boolean);
			return lines(names.flatMap((n) => [n, g.kibo[`${n}@${kibo.skill_fp?.[n]}`] || g.kibo[n]]));
		}
		if (bare === 'systems/lingzi/') return lines(Object.values(g.lingzi).flatMap((l) => [l.skill, l.one, l.full]));
		return [];
	},
};
