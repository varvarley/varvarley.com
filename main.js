// main.js — global interactions for varvarley.com

// ── Typewriter effect ──────────────────────────────────────────
// Types out the text of the .eyebrow element one character at a time.
// Adds .typed class when done to stop the cursor blinking.
const eyebrow = document.querySelector('.eyebrow');
if (eyebrow) {
  const fullText = eyebrow.textContent.trim();
  eyebrow.textContent = '';
  let i = 0;
  const type = () => {
    if (i < fullText.length) {
      eyebrow.textContent += fullText[i++];
      setTimeout(type, 90);
    } else {
      eyebrow.classList.add('typed'); // stop cursor once done
    }
  };
  setTimeout(type, 600); // short delay before typing starts
}

// ── Mobile nav toggle ──────────────────────────────────────────
const toggle   = document.querySelector('.nav-toggle');
const navLinks = document.querySelector('.nav-links');
if (toggle && navLinks) {
  toggle.addEventListener('click', () => {
    const open = navLinks.classList.toggle('is-open');
    toggle.setAttribute('aria-expanded', String(open));
  });
  // Close menu when a link is clicked
  navLinks.querySelectorAll('a').forEach(a =>
    a.addEventListener('click', () => navLinks.classList.remove('is-open'))
  );
}

// ── Auto-update copyright year ─────────────────────────────────
const yearEl = document.getElementById('year');
if (yearEl) yearEl.textContent = new Date().getFullYear();

// ── Nav transparency on scroll ─────────────────────────────────
// Adds .scrolled to site-header once the user scrolls past the
// hero, making the nav background solid instead of transparent.
const header = document.getElementById('site-header');
if (header) {
  const onScroll = () => {
    header.classList.toggle('scrolled', window.scrollY > 80);
  };
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll(); // run once on load in case page is already scrolled
}

// ── Dark / Light mode toggle ───────────────────────────────────
// Dark mode is the default (set on <html data-theme="dark">).
// Light mode tokens are a future TODO — the toggle button is
// wired up and saves the preference, but light styles aren't
// defined yet. When ready, add [data-theme="light"] { ... }
// to styles.css and remove the "coming soon" guard below.
const themeToggle = document.getElementById('theme-toggle');
const LIGHT_MODE_READY = true;

if (themeToggle) {
  // Load saved preference
  const saved = localStorage.getItem('theme');
  if (saved) document.documentElement.setAttribute('data-theme', saved);
  syncToggleLabel();

  themeToggle.addEventListener('click', () => {
    if (!LIGHT_MODE_READY) {
      // Light mode not yet implemented — show a friendly message
      themeToggle.textContent = '[ coming soon ]';
      setTimeout(() => syncToggleLabel(), 1800);
      return;
    }
    const current = document.documentElement.getAttribute('data-theme');
    const next    = current === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', next);
    localStorage.setItem('theme', next);
    syncToggleLabel();
  });
}

// Updates the toggle button icon to match the current theme
function syncToggleLabel() {
  if (!themeToggle) return;
  const theme = document.documentElement.getAttribute('data-theme');
  themeToggle.textContent = theme === 'dark' ? '🌙' : '☀️';
}
