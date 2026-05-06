# Var's Personal Website — Design & Build Prompt for Claude Code

> **Stack: HTML, CSS, JavaScript (vanilla)**
> Read this entire file before touching anything. This is the source of truth for the design system, page structure, and homestead component.

---

## Project Structure

Scaffold the project with the following file structure:

```
/
├── index.html          # Home page (landing/intro)
├── about.html          # About page (homestead map)
├── styles.css          # Global design system — single source of truth
├── main.js             # Global JS (nav, shared interactions)
├── homestead.js        # Homestead map + modal logic (about page only)
└── DESIGN_PROMPT.md    # This file
```

Keep it flat and simple. No build tools, no bundlers — just vanilla HTML, CSS, and JS.

---

## Aesthetic Direction

The core concept is: **"a cozy ski lodge with an old arcade cabinet in the corner."**

- Warm, earthy tones are the **foundation** — deep walnut browns, aged parchment, charcoal with warm undertones, ember orange, pine green, muted gold
- 8-bit / pixel / retro elements are **accents only** — used for interactive components, hover states, dividers, and the homestead map
- Snow patches, wood textures, lantern glows, and night-sky atmosphere are part of the vibe
- Seasonal default: **winter/dusk** feel throughout
- Rule: **warm = default, pixel = punctuation**

---

## Design System (`styles.css`)

Place all of the following at the top of `styles.css` as CSS custom properties.
Comment each section clearly — this file should be easy to hand off and edit.

### Color Tokens

```css
/* =============================================
   COLOR TOKENS — edit here to retheme the site
   ============================================= */

:root {
  /* Backgrounds */
  --color-bg-primary: #1a120a;
  --color-bg-ground: #1c2e10;
  --color-bg-surface: #2d1f0f;

  /* Paths & Wood */
  --color-path: #3d2510;
  --color-wood-dark: #3d2510;
  --color-wood-mid: #5c3820;
  --color-wood-light: #8b5e38;

  /* Warm Accents */
  --color-warm-amber: #e8a030;
  --color-warm-orange: #c86020;
  --color-warm-yellow: #f0c060;
  --color-lantern: #f8d080;

  /* Nature */
  --color-snow: #c8d8c0;
  --color-grass: #1e2e12;

  /* Text */
  --color-text-primary: #d4c4a0;
  --color-text-muted: #8b7a60;
  --color-text-accent: #f0c060;

  /* Borders */
  --color-border: #3a2810;
  --color-border-warm: #5c4530;
}
```

### Typography

```css
/* =============================================
   TYPOGRAPHY
   Import these from Google Fonts in each HTML file:
   - Calistoga (display/headlines)
   - Press Start 2P (pixel UI labels — use sparingly)
   - Lora (body text)
   ============================================= */

:root {
  --font-display: 'Calistoga', serif;         /* Headlines, titles, lodge signage */
  --font-pixel: 'Press Start 2P', monospace;  /* Buttons, labels, pixel accents ONLY */
  --font-body: 'Lora', serif;                 /* All reading/body text */
}
```

Add this `<link>` inside the `<head>` of every HTML file:

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Calistoga&family=Press+Start+2P&family=Lora:ital,wght@0,400;0,600;1,400&display=swap" rel="stylesheet">
```

### Global Style Rules

```css
/* =============================================
   GLOBAL BASE STYLES
   ============================================= */
```

- `body`: background `var(--color-bg-primary)`, color `var(--color-text-primary)`, font `var(--font-body)`
- Subtle grain/noise overlay on `body::after` at ~4% opacity — bridges analog and retro-digital feel
- Buttons: chunky, beveled look. On `:hover` — `translateY(2px)` + shadow shrink to feel "pressed"
- Cards/panels: styled like wooden plaques — warm border, slight box-shadow in amber tones
- Links: `var(--color-warm-amber)` default, `var(--color-warm-yellow)` on hover
- Section dividers: use a pixel-art mountain/treeline silhouette `<div class="divider">` instead of plain `<hr>`
- No hardcoded color values in component styles — always reference a CSS variable

---

## Page 1 — Home (`index.html`)

This is the first thing visitors see. It should feel like **arriving at the lodge for the first time** — warm, atmospheric, personal.

### Google Font link
Include the font `<link>` in `<head>`.

### Navigation Bar
- Links: **Home** | **About / Homestead** — add more links here as the site grows
- Style: warm wood-toned bar, `var(--font-pixel)` for nav labels, small font size (~8px)
- Active page indicator: a small amber underline or glow
- Keep the nav easy to extend — new pages should just need a new `<a>` tag

### Hero Section
Include the following elements — use placeholder text where noted:

```
Headline:       People call me Var.
Subheadline:    [TODO: 1–2 sentence personal intro — who you are, what you do]
Location:       📍 Logan, UT        ← easy to update, put in a <span id="location">
CTA button:     Enter the Homestead →   (links to about.html)
```

- Hero should feel atmospheric — dark background, warm glow around the headline
- Headline uses `var(--font-display)`, large (~52–64px)
- CTA button uses `var(--font-pixel)`, small pixel-style, with the "pressed" hover effect
- Keep the hero section clearly commented so content is easy to swap out

### Below the Hero (optional placeholder sections)
Scaffold 2–3 empty sections below the hero with commented placeholders:

```html
<!-- TODO: Section 2 — e.g. featured project, quick links, or a teaser -->
<!-- TODO: Section 3 — e.g. currently working on / recent activity -->
```

Do not fill these in yet — they will be designed later.

---

## Page 2 — About / Homestead (`about.html`)

This is the centerpiece of the site. A **top-down pixel-art homestead** that visitors explore by clicking buildings. Each building opens a modal with content.

### Google Font link
Include the font `<link>` in `<head>`.

### Top Bar
Styled like the nav but specific to the homestead:
- Left: site title `"Var's Homestead"` in `var(--font-display)`, warm yellow
- Center: moon + 3 twinkling stars (CSS animation)
- Right: `[ résumé ↗ ]` — small pixel-font link, escape hatch for time-pressed visitors

```html
<!-- TODO: replace # with actual resume URL or PDF path -->
<a href="#" class="resume-link">[ résumé ↗ ]</a>
```

### Map Canvas
- Full-width dark grass background (`var(--color-bg-ground)`) with subtle grid overlay
- Scattered snow patches (CSS `border-radius: 50%` ellipses, low opacity)
- Two main SVG dirt paths: horizontal + vertical crossing at center, with diagonal offshoots to corner buildings
- Flickering lantern posts along paths (CSS `@keyframes flicker` animation)
- Pixel pine trees at map edges (CSS div triangles — no images)

### Buildings

Render all 6 buildings as clickable CSS div structures. No image assets.
Each building should have a unique color palette to distinguish it visually.

| Key | Display Name | Emoji | Color Palette | Content Theme |
|---|---|---|---|---|
| `varber` | Varber Shop | ✂️ | Purple tones `#4a2e50` | Style, personality, aesthetic |
| `varcheologist` | Varcheologist | 🦴 | Tan/earthy `#3a2c14` | Past, history, formative experiences as "artifacts" |
| `varden` | The Varden | 🌿 | Deep green `#1a3818` | Aspirations, things being grown into, seeds being planted |
| `varchitect` | Varchitect | 🏗️ | Warm brown `#382818` | Projects being built, designs in progress |
| `univarsity` | The Univarsity | 🎓 | Deep indigo `#2a2040` | Education, skills, academics |
| `dealership` | Var Dealership | 🚗 | Forest green `#2a3a28` | Hobbies, passions, things I geek out on |

**Building layout — position on the map:**

```
[Varber Shop]         [The Univarsity]        [Vardiologist]
        \                    |                    /
         ------- [horizontal path] --------
                             |
[Var Dealership] ---[vertical path]--- [Varchitect]
                             |
         ------- [horizontal path] --------
        /                    |                    \
[Varcheologist]         [Post Office]          [The Varden]
```

> Note: The layout above is a guide. Adjust x/y positions so buildings are evenly spaced and paths connect naturally.

**Building hover behavior:**
```css
.building:hover {
  transform: scale(1.08) translateY(-3px);
  z-index: 20;
}
.building:hover .b-label {
  color: var(--color-warm-yellow);
}
```

**Building click:** calls `openModal(key)` in `homestead.js`

### Modal System (in `homestead.js`)

Each modal contains:
- Title (emoji + name)
- Subtitle (one-line description of what lives here)
- Body copy (placeholder for now — clearly marked TODO)
- Tags (small pill labels)
- Close button (`[ X ]`) in pixel font

**Modal behavior:**
- Overlay fades in on open (`opacity` transition, `pointer-events: none` → `all`)
- Modal box slides up on open (`translateY(8px)` → `translateY(0)`)
- Click outside the box or `[ X ]` closes it
- Warm amber border + glow on modal box

**Placeholder content for each location** (mark all body copy with `/* TODO: replace with real content */`):

```javascript
const locations = {
  varber: {
    title: '✂️ Varber Shop',
    subtitle: 'style, personality & aesthetic',
    body: `/* TODO: Write a short description of your style, aesthetic philosophy, and personal vibe. */`,
    tags: ['personality', 'style', 'aesthetic']
  },
  varcheologist: {
    title: '🦴 Varcheologist',
    subtitle: 'artifacts from the past',
    body: `/* TODO: Describe your background, formative experiences, and the moments that shaped you. */`,
    tags: ['history', 'background', 'artifacts']
  },
  varden: {
    title: '🌿 The Varden',
    subtitle: 'seeds being planted',
    body: `/* TODO: Share the things you want to grow into — aspirations, new interests, future goals. */`,
    tags: ['aspirations', 'growth', 'future']
  },
  varchitect: {
    title: '🏗️ Varchitect',
    subtitle: 'things being built & designed',
    body: `/* TODO: List or describe your active projects, builds, and things in progress. */`,
    tags: ['projects', 'building', 'design']
  },
  univarsity: {
    title: '🎓 The Univarsity',
    subtitle: 'education, skills & knowledge',
    body: `/* TODO: Describe your academic background, skills, and what you've studied or taught yourself. */`,
    tags: ['education', 'skills', 'academics']
  },
  dealership: {
    title: '🚗 Var Dealership',
    subtitle: 'hobbies, passions & obsessions',
    body: `/* TODO: Talk about the things you geek out on outside of work and school. */`,
    tags: ['hobbies', 'passions', 'interests']
  }
};
```

---

## General Code Rules

- **All design values live in `styles.css`** as CSS custom properties — never hardcode hex values or font names in HTML or JS
- **Comment everything** that a future editor would need to find and change
- **Mark all placeholder content** with `/* TODO: replace with real content */` or `<!-- TODO -->` comments
- **Don't over-engineer** — no frameworks, no bundlers, no build steps. Just clean vanilla code
- **Mobile is a future task** — make sure nothing catastrophically breaks at small screen widths, but don't optimize for it yet
- **Homestead buildings are CSS div structures only** — no external image assets, so they render anywhere without dependencies
- The whole project should be easy to pick back up and extend at any time

---

## What NOT to Do

- Do not use Inter, Roboto, Arial, or system fonts anywhere
- Do not use purple gradients on white — this aesthetic is warm and dark
- Do not add frameworks or dependencies not listed here
- Do not fill in the placeholder `<!-- TODO -->` sections — leave them for the owner to write
- Do not make the homestead a full character walkaround yet — click-to-explore modals only for now

---

*Last updated via design session. Aesthetic direction and page list will evolve — check this file for the latest before making changes.*
