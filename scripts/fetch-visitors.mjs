#!/usr/bin/env node
// Pull visits per country from GoatCounter into src/data/visitors.json, for the footer map.
//
//   GOATCOUNTER_TOKEN=... node scripts/fetch-visitors.mjs
//
// Runs in GitHub Actions before each build (the token is the GOATCOUNTER_TOKEN secret).
// It never fails the build: with no token, or if GoatCounter can't be reached, it keeps
// whatever src/data/visitors.json already holds. Only country totals are stored; GoatCounter
// does not give out IP addresses and nothing here asks for them.
import { existsSync, readFileSync, writeFileSync } from 'node:fs';
import { createRequire } from 'node:module';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import countries from 'i18n-iso-countries';

countries.registerLocale(createRequire(import.meta.url)('i18n-iso-countries/langs/en.json'));

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const out = join(root, 'src/data/visitors.json');
const code = readFileSync(join(root, 'src/consts.ts'), 'utf8').match(/GOATCOUNTER_CODE\s*=\s*"([^"]*)"/)?.[1];
const token = process.env.GOATCOUNTER_TOKEN;

function keep(reason) {
	console.warn(`fetch-visitors: ${reason}; keeping the existing src/data/visitors.json`);
	if (!existsSync(out)) writeFileSync(out, JSON.stringify({ updated: null, countries: [] }, null, '\t') + '\n');
	process.exit(0);
}

if (!code) keep('no GOATCOUNTER_CODE in src/consts.ts');
if (!token) keep('no GOATCOUNTER_TOKEN');

const base = `https://${code}.goatcounter.com/api/v0/stats/locations`;
const start = '2025-01-01T00:00:00Z';
const rows = [];

try {
	for (let offset = 0, page = 0; page < 20; page++) {
		const res = await fetch(`${base}?start=${start}&limit=100&offset=${offset}`, {
			headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' },
		});
		if (!res.ok) keep(`GoatCounter answered ${res.status}`);
		const body = await res.json();
		const stats = Array.isArray(body.stats) ? body.stats : [];
		rows.push(...stats);
		if (!body.more || stats.length === 0) break;
		offset += stats.length;
	}
} catch (err) {
	keep(`request failed (${err.message})`);
}

// GoatCounter names locations by ISO 3166-1 alpha-2 code; fall back to the English name.
const byCode = new Map();
for (const r of rows) {
	const id = String(r.id ?? '').toUpperCase();
	const alpha2 = /^[A-Z]{2}$/.test(id) ? id : countries.getAlpha2Code(String(r.name ?? ''), 'en');
	const count = Number(String(r.count ?? 0).replace(/[^0-9]/g, '')) || 0;
	if (!alpha2 || !count) continue;
	const prev = byCode.get(alpha2);
	byCode.set(alpha2, {
		code: alpha2,
		name: countries.getName(alpha2, 'en') || r.name || alpha2,
		count: (prev?.count ?? 0) + count,
	});
}

const data = {
	updated: new Date().toISOString(),
	countries: [...byCode.values()].sort((a, b) => b.count - a.count),
};
writeFileSync(out, JSON.stringify(data, null, '\t') + '\n');
console.log(`fetch-visitors: ${data.countries.length} countries written to src/data/visitors.json`);
