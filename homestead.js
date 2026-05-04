// Homestead map — modal logic
// Each location maps to a building on the map canvas.
// Replace the body strings with your own content — look for TODO comments.

const locations = {
  varber: {
    title: '✂️ Varber Shop',
    subtitle: 'style, personality & aesthetic',
    // TODO: Write a short description of your style, aesthetic philosophy, and personal vibe.
    body: 'This is where my aesthetic lives. Come back soon — the barber is still setting up shop.',
    tags: ['personality', 'style', 'aesthetic']
  },
  varcheologist: {
    title: '🦴 Varcheologist',
    subtitle: 'artifacts from the past',
    // TODO: Describe your background, formative experiences, and the moments that shaped you.
    body: 'Dusting off the artifacts. Check back soon for a tour through the excavation site.',
    tags: ['history', 'background', 'artifacts']
  },
  varden: {
    title: '🌿 The Varden',
    subtitle: 'seeds being planted',
    // TODO: Share the things you want to grow into — aspirations, new interests, future goals.
    body: 'The garden is being planted. Come back when the season turns.',
    tags: ['aspirations', 'growth', 'future']
  },
  varchitect: {
    title: '🏗️ Varchitect',
    subtitle: 'things being built & designed',
    // TODO: List or describe your active projects, builds, and things in progress.
    body: 'Blueprints on the table, scaffolding going up. Project details coming soon.',
    tags: ['projects', 'building', 'design']
  },
  univarsity: {
    title: '🎓 The Univarsity',
    subtitle: 'education, skills & knowledge',
    // TODO: Describe your academic background, skills, and what you've studied or taught yourself.
    body: 'Information Systems & Data Analytics at Utah State University. Graduating May 2026. More detail on the way.',
    tags: ['education', 'skills', 'academics']
  },
  dealership: {
    title: '🚗 Var Dealership',
    subtitle: 'hobbies, passions & obsessions',
    // TODO: Talk about the things you geek out on outside of work and school.
    body: 'The lot is being stocked. Check back soon to browse the collection.',
    tags: ['hobbies', 'passions', 'interests']
  }
};

function openModal(key) {
  const loc = locations[key];
  if (!loc) return;

  document.getElementById('modal-title').textContent    = loc.title;
  document.getElementById('modal-subtitle').textContent = loc.subtitle;
  document.getElementById('modal-body').textContent     = loc.body;

  const tagsEl = document.getElementById('modal-tags');
  tagsEl.innerHTML = loc.tags.map(t => `<li>${t}</li>`).join('');

  document.getElementById('modal-overlay').classList.add('is-open');
  document.getElementById('modal-overlay').querySelector('.modal-close').focus();
}

function closeModal() {
  document.getElementById('modal-overlay').classList.remove('is-open');
}

// Click outside the box to close
document.getElementById('modal-overlay').addEventListener('click', (e) => {
  if (e.target === e.currentTarget) closeModal();
});

// Keyboard: Escape to close, Enter/Space to open focused building
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') closeModal();
});

document.querySelectorAll('.building').forEach(b => {
  b.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      b.click();
    }
  });
});
