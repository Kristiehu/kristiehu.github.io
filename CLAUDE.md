# Notes for Claude

Read `MAINTAINING.md` first. Key rules for this repo:

- Facts belong in `src/data/profile.ts` and `src/data/teaching.ts`. Don't hard-code bio facts in pages.
- New posts start from `templates/post-template.mdx` with `draft: true`. Only set `draft: false` when Kristie says so.
- Every post gets `direction:` (ids in `src/data/direction-ids.ts`; leave out for "Earlier projects") and a `short:` label. Papers in `profile.ts` get `direction` too.
- Never state a number in a post that you haven't checked against her paper, data or CV.
- Image names: kebab-case, no spaces or colons.
- Colours: use the theme tokens at the end of `src/styles/global.css`, never raw black/white, and check both themes (`data-theme` on `<html>`). One accent colour: `var(--blue)`, identical in both themes; don't add a second one.
- Type: one family. Source Serif 4 (text and headings, upright), Source Sans 3 (UI and labels), Source Code Pro (code); use the font tokens and shared classes in `global.css` (`.kicker`, `.page-title`, `.lede`, `.section-title`, `.chip`). Don't add other fonts, italic titles, or wide letter-spacing. New posts: `npm run new-post -- <slug> <direction>`.
- The portrait is generated: edit `scripts/render-portrait.py` and rerun it, don't hand-edit `src/assets/portrait/`. Its per-theme numbers (`THEMES`) exist in both the script and `PointPortrait.astro`; change both.
- Never put files with personal data in `public/` (everything there is publicly downloadable).
- Run `npm run build` before finishing.
- In the Cowork device shell, prefix git with `GIT_OPTIONAL_LOCKS=0` (the mount can't delete lock files, so a plain `git status` leaves `.git/index.lock` behind). Kristie runs `git pull`/`git push` herself.
