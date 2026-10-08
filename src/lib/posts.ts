import { getCollection } from 'astro:content';

/**
 * All posts that should exist on the site, newest first.
 * Drafts (frontmatter `draft: true`) are included in `npm run dev` only,
 * so you can preview them locally; they are never built for the live site.
 */
export async function getPosts() {
	const posts = await getCollection('blog', ({ data }) => import.meta.env.DEV || !data.draft);
	return posts.sort((a, b) => b.data.pubDate.valueOf() - a.data.pubDate.valueOf());
}
