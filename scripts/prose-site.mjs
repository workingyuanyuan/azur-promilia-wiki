// Site settings for scripts/prose-review.mjs (the prose ledger).
//
// - derived: locales a script writes from another (Simplified Chinese from Traditional,
//   scripts/to-zh-cn.py); their prose is the root locale's, converted, and is read there.
// - skip(path, lang): text the page shows as its source gives it. This site restates every
//   description in its own words (records/text/) and shows no source text, so nothing is skipped.

export default {
	derived: ['zh-cn'],
	skip() {
		return [];
	},
};
