import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';
import { DIRECTION_IDS } from './data/direction-ids';

// Blog / project posts live in src/content/blog/*.mdx.
// See MAINTAINING.md for how to add one (templates/post-template.mdx).
const blog = defineCollection({
	loader: glob({ base: './src/content/blog', pattern: '**/*.{md,mdx}' }),
	schema: ({ image }) =>
		z.object({
			title: z.string(),
			// One-line outcome. Shown on the card and used as the meta description.
			description: z.string(),
			pubDate: z.coerce.date(),
			updatedDate: z.coerce.date().optional(),
			heroImage: image().optional(),
			tags: z.array(z.string()).default([]),
			// draft: true → visible in `npm run dev` (with a DRAFT badge), never built for the live site.
			draft: z.boolean().default(false),
			// Which Lab direction the post belongs to (src/data/directions.ts). Leave out → "Earlier projects".
			direction: z.enum(DIRECTION_IDS).optional(),
			// 3–6 word label for the post's line on the Lab page. Falls back to the title.
			short: z.string().optional(),
			// e.g. "Mining 6(2), 2026" or "NeurIPS 2026 Workshop · REO-2"
			venue: z.string().optional(),
			links: z
				.object({
					paper: z.string().url().optional(),
					code: z.string().url().optional(),
					data: z.string().url().optional(),
				})
				.optional(),
		}),
});

export const collections = { blog };
