# CSP221A Final Project — student guide

A single-page static website: the student guide for the CSP221A final development
project (sprints, DevOps track, free hosting, rubrics, curated YouTube videos,
deliverables checklist, FAQ). It is styled like a macOS desktop, with app windows,
a menu bar clock, and folder icons.

- Plain HTML, CSS, and a little vanilla JS. No framework, no build step, no dependencies.
- Fonts load from Google Fonts (Geist, Geist Mono) with system fallbacks.
- Light mode only — the page looks the same for every visitor regardless of their
  system theme setting.
- Scroll reveals, drifting hero windows, hover states, count-up numbers, and a
  progress bar. All motion is switched off for visitors who set
  `prefers-reduced-motion: reduce`.
- The deliverables checklist saves ticks in the visitor's own browser (localStorage).

## Run locally

Open `index.html` in a browser, or serve the folder:

    npx serve .

## Deploy (free)

This folder is the site. It lives inside the CSP221A class repository, so a host
has to be pointed at `site/` rather than the repository root.

**Vercel, from GitHub (recommended).** In vercel.com choose *Add New > Project*,
import `stalzkie/CSP221A`, then set **Root Directory** to `site`. Framework preset
"Other", no build command, output directory `.`. Every push to `main` redeploys
automatically.

**Vercel, from the terminal.**

    cd site
    npm i -g vercel
    vercel            # preview deploy
    vercel --prod     # publish to production

**Alternatives.** Netlify (drag-and-drop this folder, or connect the repo with a
base directory of `site`) and GitHub Pages (*Settings > Pages*, deploy from `main`
— note Pages only serves `/` or `/docs`, so this folder would need renaming).

## Editing notes

- Colors are CSS custom properties on `:root` at the top of the `<style>` block.
- Sprint content lives in the four `<div role="tabpanel" id="p-s1">` to `p-s4` blocks.
- A video card is one `<a class="vid">` element; copy one and change the `href`,
  the filename in `<em>`, the channel in `.ch`, the format in `.kind`, and the
  title and description in `.vtxt`.
- The animation layer is the last block of the stylesheet and the `// animation
  layer` block in the script. Elements opt in with `class="reveal"` (one element)
  or `class="reveal-group"` (stagger the direct children).
- The folder-built "csp221a" in the footer is generated from the 5x7 letter map
  `G` in the script. A new `word` needs a matching letter in `G`.
- The free-hosting table was checked in October 2026. Confirm each host's current
  free tier before the term starts.
- No secrets or API keys belong in this repository. The site needs none.
