// The footer's visitor map, drawn once at build time from src/data/visitors.json
// (filled by scripts/fetch-visitors.mjs). One dot per country, sized by visits; no
// cities, no IP addresses. The footer loads this file only when someone opens the map,
// and inserts it inline so its colours follow the site's light/dark theme.
import type { APIRoute } from 'astro';
import { geoArea, geoCentroid, geoNaturalEarth1, geoPath } from 'd3-geo';
import { feature } from 'topojson-client';
import isoCountries from 'i18n-iso-countries';
import land110 from 'world-atlas/land-110m.json';
import countries50 from 'world-atlas/countries-50m.json';
import visitors from '../data/visitors.json';

const W = 640;
const H = 330;

const esc = (s: string) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

// A country's dot sits on its largest piece of land, so France lands in France
// rather than in the Atlantic between Paris and French Guiana.
function anchor(f: any) {
	if (f.geometry?.type !== 'MultiPolygon') return geoCentroid(f);
	let best: any = null;
	let bestArea = -1;
	for (const coordinates of f.geometry.coordinates) {
		const part = { type: 'Polygon', coordinates } as any;
		const a = geoArea(part);
		if (a > bestArea) [best, bestArea] = [part, a];
	}
	return geoCentroid(best);
}

export const GET: APIRoute = () => {
	const land = feature(land110 as any, (land110 as any).objects.land) as any;
	const shapes = (feature(countries50 as any, (countries50 as any).objects.countries) as any).features;
	const byNumeric = new Map<string, any>(shapes.map((f: any) => [String(f.id).padStart(3, '0'), f]));

	const projection = geoNaturalEarth1().fitExtent([[6, 6], [W - 6, H - 6]], { type: 'Sphere' } as any);
	const path = geoPath(projection).digits(1);

	const rows = (visitors.countries as { code: string; name: string; count: number }[]) ?? [];
	const max = Math.max(1, ...rows.map((c) => c.count));

	const dots = [...rows]
		.sort((a, b) => b.count - a.count)
		.map((c) => {
			const f = byNumeric.get(String(isoCountries.alpha2ToNumeric(c.code) ?? ''));
			const xy = f && projection(anchor(f) as [number, number]);
			if (!xy) return '';
			const r = 2.5 + 9 * Math.sqrt(c.count / max);
			const label = `${c.name}: ${c.count.toLocaleString('en-US')} ${c.count === 1 ? 'visit' : 'visits'}`;
			return `<circle class="vm-dot" cx="${xy[0].toFixed(1)}" cy="${xy[1].toFixed(1)}" r="${r.toFixed(1)}"><title>${esc(label)}</title></circle>`;
		})
		.join('');

	const svg =
		`<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" role="img" aria-label="Visits by country">` +
		`<path class="vm-land" d="${path(land)}"/>` +
		`<g>${dots}</g>` +
		`</svg>`;

	return new Response(svg, { headers: { 'Content-Type': 'image/svg+xml' } });
};
