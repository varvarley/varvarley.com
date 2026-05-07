# CLAUDE.md — varvarley.com project instructions

Read this file before making any changes. These are standing rules for all work on this project.

---

## Versioning

This project uses semantic versioning: `MAJOR.MINOR.PATCH`

| Change type                                         | Bump    | Example         |
|-----------------------------------------------------|---------|-----------------|
| Typos, small style tweaks, minor bug fixes          | PATCH   | 0.1.0 → 0.1.1   |
| New section, new page, new feature, content updates | MINOR   | 0.1.1 → 0.2.0   |
| Full redesign, major structural overhaul            | MAJOR   | 0.2.0 → 1.0.0   |

**Rules:**
- Update the version number in the footer of every HTML file (`index.html`, `about.html`, and any future pages) with every change.
- Keep a one-line version history comment at the top of `styles.css` so it's easy to see what changed at a glance.
- Current version: **0.1.0**

---

## Git Commit Messages

Commit messages should be slightly more descriptive than a one-liner. Follow this format:

```
Short summary (what changed)

- Specific detail about one change
- Specific detail about another change
- Note anything that affects other files or future work
```

Example:
```
Update hero section and nav links

- Changed headline copy to "People call me Var."
- Added location tag (📍 Logan, UT) below lede
- Swapped CTA from #projects to about.html (homestead)
- Bumped version to 0.1.1
```

Always include "Bumped version to X.X.X" as the last bullet when the version changes.

---

## Code Style — CSS

- **Never hardcode hex values or font names** in HTML or JS. All design values live in `styles.css` as CSS custom properties.
- All color tokens are defined in the `:root` block at the top of `styles.css` under `/* COLOR TOKENS */`. Edit there to retheme the whole site.
- All font families are defined in `:root` under `/* TYPOGRAPHY */`. Never reference a font name outside of that block.
- Spacing, radius, and shadow values are also in `:root` — use them, don't invent new magic numbers.
- When adding a new component, define any new tokens in `:root` first, then reference them in the component style.

---

## Code Style — Comments

- Every section in `styles.css` must have a clearly labeled comment block so any section can be found quickly.
- In HTML, every major section must have a comment marking what it is (e.g. `<!-- ============ HERO ============ -->`).
- In JS, every function must have a one-line comment explaining what it does.
- All placeholder content must be marked with a `<!-- TODO -->` or `/* TODO */` comment so it's easy to find later.
- When adding a new building to the homestead map, add a comment above it with its name and color palette for reference.

---

## Design Rules

See `DESIGN_PROMPT.md` for the full aesthetic direction. Short version:

- **Warm = default, pixel = punctuation.** Warm earthy tones everywhere; pixel/retro elements only for interactive accents (buttons, labels, hover states).
- Fonts: `Montserrat` (bold, all-caps) for section headings (h2), `Calistoga` for display/hero text, `Press Start 2P` for pixel labels/buttons (use sparingly, small size), `JetBrains Mono` for body text.
- No frameworks, no bundlers — vanilla HTML, CSS, and JS only.
- Mobile is a future task — don't break small screens, but don't optimize for them yet.
- Homestead buildings are CSS div structures only — no external image assets.

---

## File Map

| File             | Purpose                                              |
|------------------|------------------------------------------------------|
| `index.html`     | Home page                                            |
| `about.html`     | Homestead map page                                   |
| `styles.css`     | Global design system — single source of truth        |
| `main.js`        | Global JS (nav toggle, year, shared interactions)    |
| `homestead.js`   | Homestead map + modal logic (about page only)        |
| `DESIGN_PROMPT.md` | Full aesthetic brief — read before visual changes  |
| `CLAUDE.md`      | This file                                            |
