// The Kibo part of the sidebar: the lookup tables in a fixed order, then one link per Kibo
// page in the order of records/kibo.json (by element, then name). Read by astro.config.mjs.
import { readFileSync, existsSync } from 'node:fs';
import { fileURLToPath } from 'node:url';

const records = fileURLToPath(new URL('../../records/kibo.json', import.meta.url));
const docs = new URL('../content/docs/kibo/', import.meta.url);

/** Slugs of the lookup tables under /kibo/, in sidebar order. */
export const KIBO_TABLES = ['work', 'riding', 'elements'];

/** `{ slug }` of every Kibo that has a page. */
export const KIBO = existsSync(records)
	? JSON.parse(readFileSync(records, 'utf8')).filter((k) => existsSync(fileURLToPath(new URL(`${k.slug}.md`, docs))))
	: [];
