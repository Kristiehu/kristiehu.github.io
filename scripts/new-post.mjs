#!/usr/bin/env node
// Start a new post from templates/post-template.mdx.
//
//   npm run new-post -- <slug> [direction]
//
//   slug       short kebab-case name; becomes the URL /blog/<slug>/   e.g. drone-lidar-survey
//   direction  lidar | earth-observation | data-systems  (leave out for "Earlier projects")
//
// The post starts as a draft: it shows in `npm run dev` with a DRAFT badge and is never published
// until you set `draft: false`.
import { existsSync, readFileSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const [slug, direction] = process.argv.slice(2);

const ids = [...readFileSync(join(root, 'src/data/direction-ids.ts'), 'utf8').matchAll(/'([a-z-]+)'/g)].map((m) => m[1]);

function fail(msg) {
	console.error(`\n  ${msg}\n\n  Usage: npm run new-post -- <slug> [${ids.join(' | ')}]\n`);
	process.exit(1);
}

if (!slug) fail('Give the post a slug, e.g. npm run new-post -- drone-lidar-survey lidar');
if (!/^[a-z0-9]+(-[a-z0-9]+)*$/.test(slug)) fail(`"${slug}" isn't a valid slug: use lowercase letters, numbers and hyphens.`);
if (direction && !ids.includes(direction)) fail(`"${direction}" isn't a direction. Use one of: ${ids.join(', ')}.`);

const target = join(root, 'src/content/blog', `${slug}.mdx`);
if (existsSync(target)) fail(`src/content/blog/${slug}.mdx already exists.`);

const today = new Date().toISOString().slice(0, 10);
let text = readFileSync(join(root, 'templates/post-template.mdx'), 'utf8')
	.replaceAll('SLUG', slug)
	.replace("pubDate: 'YYYY-MM-DD'", `pubDate: '${today}'`);
text = direction
	? text.replace(/^direction: \S+/m, `direction: ${direction}`)
	: text.replace(/^direction: /m, '# direction: ');

writeFileSync(target, text);
console.log(`
  Created src/content/blog/${slug}.mdx  (draft)

  Next:
  1. Fill in title, description, short and tags at the top of the file.
  2. Save images as src/content/blog/img/${slug}-1.png, ${slug}-2.png, …
  3. npm run dev  →  http://localhost:4321/blog/${slug}/
  4. When it's ready, set draft: false, then commit and push.
`);
