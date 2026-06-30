# CLAUDE.md — varvarley.com

Read this file before making any changes. These are standing rules for all work on this project.

---

## Current Version: 0.21.2

This project uses semantic versioning: `MAJOR.MINOR.PATCH`

| Change type                                         | Bump  | Example           |
|-----------------------------------------------------|-------|-------------------|
| Typos, small style tweaks, minor bug fixes          | PATCH | 0.11.0 → 0.11.1   |
| New section, new page, new feature, content updates | MINOR | 0.11.0 → 0.12.0   |
| Full redesign, major structural overhaul            | MAJOR | 0.11.0 → 1.0.0    |

**Rules:**
- Update the version number in the footer of **every** HTML file with every change.
- Keep a one-line version history comment at the top of `styles.css`.
- Always end commit messages with "Bumped version to X.X.X."

---

## Current State

- **Status:** Active — design polish + homestead evolution phase
- **Working:** All pages live at varvarley.com. Nav, hero, project cards (DS cartridges), homestead map (buildings exist, modals are stubs), work.html poem, contact page.
- **In progress:** Homestead building redesign (shapes/colors/layout — modals remain stubs for now). Design polish across all pages.
- **Known stubs:** `work.html` Technical / Creative / People sections, all homestead modals, `varchive.html` content.
- **Deferred:** Mobile optimization, filling content stubs, modal content.
- **Next priorities:** Homestead buildings visual redesign → general design polish → possible layout experiments (e.g. horizontal scroll on project cards).

---

## Stack

- **Language:** Vanilla HTML, CSS, JS — no frameworks, no bundlers, no build step
- **Deployment:** AWS S3 via `deploy.ps1` (PowerShell script). Flow: edit → open HTML in browser to review → deploy via Claude Code → check live at varvarley.com
- **No linting, no local server** — preview by opening `.html` files directly in browser
- **Package manager:** None

---

## File Map

| File               | Purpose                                                          |
|--------------------|------------------------------------------------------------------|
| `index.html`       | Home — hero, about, project cards, homestead CTA, contact       |
| `about.html`       | Homestead map — CSS buildings + modal stubs                      |
| `work.html`        | Work page — poem + three stub sections (Technical/Creative/People) |
| `varchive.html`    | Archive page — content thin, structure exists                    |
| `contact.html`     | Contact page                                                     |
| `styles.css`       | **Single source of truth** for all design tokens                 |
| `main.js`          | Global JS — nav toggle, year auto-fill, shared interactions      |
| `homestead.js`     | Homestead map + modal logic (about page only)                    |
| `deploy.ps1`       | S3 deployment script — run via Claude Code                       |
| `assets/`          | Resume PDF, favicon, any static assets                           |
| `portfolio-site/`  | **Ignore** — stale old draft, not the live site                  |
| `InspoPics/`       | Reference images for design direction                            |
| `DESIGN_PROMPT.md` | **Outdated** — do not use as reference. The live site at varvarley.com is the canonical design reference. |

---

## Design System

The live site at **varvarley.com is the canonical design reference.** DESIGN_PROMPT.md is outdated — ignore it.

### Aesthetic
- Warm earthy lodge/homestead feel
- Pixel/retro elements used sparingly — interactive accents only (buttons, labels, hover states)
- Light and dark mode both implemented and must stay in sync with every change

### Fonts (defined in `:root` — never reference outside of that block)
- `Calistoga` — hero/display text
- `Montserrat 700 all-caps` — section headings (h2) via `--font-heading`
- `Press Start 2P` — pixel labels/buttons (sparingly, small size only)
- `JetBrains Mono` — body text

### Tokens
- All color, font, spacing, radius, and shadow values live in `:root` in `styles.css`
- **Never hardcode hex values or font names** in HTML or JS
- When adding a new component: define tokens in `:root` first, then use them

### Current active pages/components to match
- Hero: typewriter on name, gradient fills full height, frosted header
- Project cards: DS cartridge style
- Homestead: CSS-only building structures (no image assets)

---

## Design Decision Rules

**Claude proposes, Josh approves. Always.**

- Before implementing any layout change, new component, or visual experiment: describe the approach and wait for explicit approval.
- This includes: layout restructuring, new interaction patterns, color adjustments, font changes, spacing overhauls.
- Small bug fixes and typo corrections can be applied directly.
- "Mostly the same layout" is not permission to change layout. Propose first.

### What's in scope for this phase
- Design polish: spacing, typography consistency, transitions, hover states
- Homestead building redesign (shapes, colors, map layout) — propose visuals before implementing
- Possible layout experiments (e.g. horizontal scroll on project cards) — propose before touching

### What's out of scope / deferred
- Mobile optimization
- Filling content stubs (work.html sections, homestead modals, varchive)
- New pages

---

## Code Style — CSS

- All design values in `:root`. No exceptions.
- Every section in `styles.css` must have a clearly labeled comment block.
- No magic numbers — if it's not in `:root`, put it there first.
- Both light and dark mode must be updated together when touching color or visual styles.

---

## Code Style — HTML & JS

- Every major HTML section gets a comment: `<!-- ============ HERO ============ -->`
- Every JS function gets a one-line comment explaining what it does.
- Placeholder/stub content marked with `<!-- TODO -->` or `/* TODO */`.
- Homestead buildings: CSS div structures only — no image assets.

---

## Git Commit Format

```
Short summary (what changed)

- Specific detail about one change
- Specific detail about another change
- Note anything that affects other files or future work
- Bumped version to X.X.X
```

---

## What NOT to Do

- Do NOT reference `DESIGN_PROMPT.md` — it's outdated
- Do NOT touch `portfolio-site/` — stale draft, ignore it
- Do NOT hardcode hex values or font names anywhere outside `:root`
- Do NOT implement layout or structural changes without proposing first
- Do NOT optimize for mobile in this phase — don't break it, but don't chase it
- Do NOT fill content stubs unless explicitly asked
- Do NOT run the deploy script without being asked to deploy
- Do NOT invent new design tokens — check `:root` first, add there if genuinely new
