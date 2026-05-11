// main.js — global interactions for varvarley.com

// ── Hero name typewriter + suffix cycler ──────────────────────────────────────
// Types "Josh" then "Varley" one character at a time, then endlessly cycles
// through suffixes: each is typed in, held, then backspaced out before the next.
const heroLine1  = document.querySelector('.hero-line1');
const heroLine2  = document.querySelector('.hero-line2');
const heroSuffix = document.querySelector('.hero-suffix');

if (heroLine1 && heroLine2 && heroSuffix) {
  const CHAR_SPEED = 140; // ms per character

  function typeLine(el, text, onDone) {
    let i = 0;
    el.classList.add('typing');
    const tick = () => {
      if (i < text.length) {
        el.textContent += text[i++];
        setTimeout(tick, CHAR_SPEED);
      } else {
        el.classList.remove('typing');
        if (onDone) onDone();
      }
    };
    tick();
  }

  setTimeout(() => {
    typeLine(heroLine1, 'Josh', () => {
      typeLine(heroLine2, 'Varley');
    });
  }, 600);
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

// ── About terminal — reveals code lines one by one when section scrolls into view ──
const aboutTerminal = document.getElementById('about-terminal');
if (aboutTerminal) {
  const lines    = aboutTerminal.querySelectorAll('.t-line');
  const outputEl = document.getElementById('terminal-output');
  let   fired    = false;

  function runTerminal() {
    if (fired) return;
    fired = true;
    let delay = 150;
    lines.forEach(line => {
      setTimeout(() => line.classList.add('visible'), delay);
      delay += 320;
    });
    if (outputEl) setTimeout(() => outputEl.classList.add('visible'), delay + 600);
  }

  const obs = new IntersectionObserver(entries => {
    if (entries[0].isIntersecting) { runTerminal(); obs.disconnect(); }
  }, { threshold: 0.4 });
  obs.observe(aboutTerminal);
}

// Updates the toggle aria-label to match the current theme (icon swap is handled by CSS)
function syncToggleLabel() {
  if (!themeToggle) return;
  const theme = document.documentElement.getAttribute('data-theme');
  themeToggle.setAttribute('aria-label', theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode');
}
