# Maintaining kristiehu.github.io

The site is Astro + MDX. GitHub Actions builds and deploys it on every push to `main`.
Facts live in data files; pages only display them. Most updates are one small edit.

## Where things live

| What | File |
|---|---|
| Bio facts, education, experience, publications, awards, training | `src/data/profile.ts` |
| Leadership & service, teaching, coursework | `src/data/teaching.ts` |
| Posts (projects and papers) | `src/content/blog/<slug>.mdx` |
| Lab directions: titles, intros, covers | `src/data/directions.ts`, covers in `src/assets/covers/` |
| Post images | `src/content/blog/img/<slug>-<n>.png` |
| CV | `public/CV-2026.pdf` |
| Template for a new post | `templates/post-template.mdx` |

Anything in `public/` can be downloaded by anyone, even if no page links to it.

Colours: the site has a light and a dark theme (button in the header). It opens in the light theme; a visitor's own choice is remembered. Write colours with the tokens at the end of `src/styles/global.css` (for example `rgba(var(--ink), 0.7)` instead of `rgba(0, 0, 0, 0.7)`), so both themes work. There is one accent colour, `var(--blue)` (#4e7ab2), the same in both themes: use it for links, highlights and anything that marks "current" or "hover". The three direction colours in `src/data/directions.ts` are only for the small tag dots.

Type: one font family on every page. Source Serif 4 for reading text and all headings (upright, semibold), Source Sans 3 for small labels, tags and dates (the header and footer use the text face), Source Code Pro for code, and Source Han Serif (思源宋体) for Chinese, which is the same design family. Italic is only for quotes and the pronunciation. The fonts come from npm (`@fontsource-variable/...`, loaded in `BaseHead.astro`); the tokens are `--font-text`, `--font-display`, `--font-ui` and `--font-mono` at the end of `global.css`. Use the shared classes instead of styling headings page by page:

- `.kicker`: the small uppercase label above a title. Wrap a word in `<span class="accent">` to make it blue.
- `.page-title`: page titles, the name and the homepage headline. `<em>` turns a word blue.
- `.lede`: the intro paragraph.
- `.section-title`: section headings such as EDUCATION and PROJECTS.
- `.chip`: filter and back-link buttons.

## Add a post

1. Run `npm run new-post -- <slug> <direction>`, for example `npm run new-post -- drone-lidar-survey lidar`. It creates `src/content/blog/<slug>.mdx` from the template as a draft, with today's date. The slug is a short kebab-case name and becomes the URL `/blog/<slug>/`.
2. Save images as `src/content/blog/img/<slug>-1.png` and so on: lowercase, hyphens, no spaces or colons, about 2000 px wide at most. The cover (`heroImage`) appears on the Work cards and, on the post page, under the title at most 760 × 460 px (never enlarged); give it at least 1520 px of width so it stays sharp on high-density screens.
3. Check `direction:` (`lidar`, `earth-observation` or `data-systems`) and set `short:` to a 3–6 word label. The post then shows that main tag on the Lab page and appears on `/blog/<direction>/`. Leave `direction` out and it goes under "Earlier projects".
4. Keep `draft: true` and run `npm run dev`. Drafts appear locally with a DRAFT badge and are never built for the live site.
5. When it's ready, fill in `description`, check the numbers, and set `draft: false`.
6. If the post belongs to a paper, add `post: '<slug>'` to that paper in `src/data/profile.ts`. The About page then links to it automatically.

## Directions, the Lab and the homepage gallery

Every project has one main tag, its direction: `lidar`, `earth-observation` or `data-systems` (`direction:` in the frontmatter). Other `tags` are free-form, and a post can have several.

- **Homepage:** below the hero, a gallery of the three directions: cover, title, one line with a real fact (`line` in `directions.ts`), and the project count. No numbering, no label above the title. Clicking the portrait scrolls down to it.
- **Lab (`/blog/`):** every project as a card showing its main tag, with tag chips at the top to filter. Posts without a direction are listed under "Earlier projects" at the bottom.
- **A direction (`/blog/lidar/`, `/blog/earth-observation/`, `/blog/data-systems/`):** its intro, all its projects and its papers.

Nothing is listed by hand. Posts join a direction through `direction:` in their frontmatter, and papers through `direction` on their entry in `PUBLICATIONS` (`src/data/profile.ts`). Titles, intros, covers and tag colours live in `src/data/directions.ts`.

To add a fourth direction, add its id to `src/data/direction-ids.ts`, an entry to `src/data/directions.ts`, and a 1200 × 900 cover to `src/assets/covers/`. The Earth observation and Data systems covers are drawn by `scripts/render-covers.py` (Python + Pillow); a new one should reuse its palette and scale, on a flat background in the page colour (no glow behind the scene). Each cover also needs a light-theme version (`<name>-light.jpg`), made with `python scripts/render-covers.py light`.

## The portrait

The portrait on Home and About is a 3D point cloud made from the drawing in `src/assets/me_0.png`. `python scripts/render-portrait.py` turns it into `src/assets/portrait/` (the points, the default view, and a still for browsers without JavaScript); `src/components/PointPortrait.astro` draws the points in the current theme, sweeps them in once, turns them a few degrees toward the mouse wherever it is on the page (like a glance; not on touch screens), and animates the lighter's flame (it pauses when the portrait is off screen, and stays still for visitors who turn on reduced motion). The scan lines fade out just inside a smoothed outline, so the edge stays clean in both themes. To change the picture, replace `me_0.png`, rerun the script with `preview`, and check `preview-light.png` / `preview-dark.png` before publishing. How far she turns: `TILT` in the script (rerun it; the frame leaves room for the turn). How quickly: `FOLLOW_MS` in the component. Size: `<PointPortrait width={140} />` on Home, `{120}` on About.

## When something happens, update this

| Event | Update |
|---|---|
| Paper accepted or published | `PUBLICATIONS` in `profile.ts` (with `direction`), the CV PDF, and the related post's `venue`/`links` |
| Talk, poster or award | `profile.ts` (`AWARDS` or a publication entry) |
| New role, committee or volunteer position | `LEADERSHIP` in `teaching.ts` |
| New TA term or course | `TEACHING` in `teaching.ts` (add `terms`) |
| Course taken | `COURSEWORK` in `teaching.ts` (the section appears once it has entries) |
| Shipped something shareable at work | New post from the template, anonymised, `draft: true` until reviewed |
| Job title or degree change | `profile.ts`, then the CV, README and LinkedIn on the same day |

## Try a change before publishing

Nothing goes live until you `git push`, so you can try anything locally first.

```
cd ~/Desktop/kristiehu.github.io
git status              # start clean: "nothing to commit, working tree clean"
# …make the change, or let Claude make it…
npm install             # only needed after a pull or when package.json changed
npm run dev             # open http://localhost:4321 (drafts show too); Ctrl+C to stop
```

- **Keep it:** `git add -A && git commit -m "content: …" && git push`. GitHub Actions publishes it in a couple of minutes.
- **Drop it:** `git stash -u`. The folder goes back to the last commit. `git stash pop` brings the change back; `git stash drop` deletes it for good.

To see exactly what will go live (no drafts): `npm run build && npm run preview`.

## Monthly release (first Sunday, about an hour)

1. `git pull`
2. Pick one content item and one fix.
3. `npm run dev` and look at the pages you changed.
4. `npm run build` (it fails on a bad frontmatter field, which is the point).
5. Go through the checklist below.
6. `git add -A && git commit -m "content: …" && git push`

## Before you push

- [ ] `git pull` done first
- [ ] `npm run build` passes
- [ ] No personal data in new files: home address, phone, ID or certificate numbers
- [ ] Work material anonymised: client names, street addresses, internal IDs and network maps
- [ ] Commit message starts with `content:`, `fix:`, `style:` or `chore:`

## Known cleanup (from the October 2026 review)

- `public/RPAS-TC.pdf` shows a home address: delete it (and purge it from git history if the repo is public).
- 27 images have `:` in their names (e.g. `p4_2:18_b.png`), which breaks checkout on Windows. Rename them and update the references in the older posts.
- Four early posts (2019–2021, under "Earlier projects") still have an empty or placeholder `description`. Fill them in when you touch them.
- `src/components/Header.astro` has a stray `}` in its style block (the CSS warning during build).
- Leftovers: `src/components.zip`, `src/layouts.zip`, and the branch `claude/blissful-raman-14e958`.
