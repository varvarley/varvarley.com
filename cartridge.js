// cartridge.js — DS cartridge project cards
// To add a project: push a new object to PROJECTS below.
// color cycles through data-project="1","2","3" then repeats.

const PROJECTS = [
  {
    title:       'Project One',
    code:        'NTR-PROJ1-USA',
    description: 'Short, punchy description of what this project does and what problem it solves.',
    tags:        ['Python', 'LangChain', 'AWS'],
    links: [
      { label: 'Code →',  href: '#' },
      { label: 'Demo →',  href: '#' },
    ],
  },
  {
    title:       'Project Two',
    code:        'NTR-PROJ2-USA',
    description: 'Short, punchy description of what this project does and what problem it solves.',
    tags:        ['SQL', 'Tableau', 'OpenAI API'],
    links: [
      { label: 'Code →',    href: '#' },
      { label: 'Write-up →', href: '#' },
    ],
  },
  {
    title:       'Project Three',
    code:        'NTR-PROJ3-USA',
    description: 'Short, punchy description of what this project does and what problem it solves.',
    tags:        ['Power BI', 'Python'],
    links: [
      { label: 'Code →', href: '#' },
    ],
  },
];

// Builds the full HTML string for one cartridge + description block
function buildCartridge(project, index) {
  const colorSlot = (index % 3) + 1; // cycles 1 → 2 → 3 → 1 → ...

  const tagsHTML = project.tags
    .map(t => `<li>${t}</li>`)
    .join('');

  const linksHTML = project.links
    .map(l => `<a href="${l.href}" target="_blank" rel="noopener">${l.label}</a>`)
    .join('');

  return `
    <div class="ds-cart-wrap">
      <div class="ds-cart" data-project="${colorSlot}">
        <div class="ds-cart-body">
          <div class="ds-cart-header">
            <span class="ds-cart-header-brand">NINTENDO DS</span>
          </div>
          <div class="ds-cart-art">
            <h3 class="ds-cart-title">${project.title}</h3>
          </div>
          <div class="ds-cart-footer">
            <div class="ds-cart-rating"><span class="ds-rating-letters">RP</span></div>
            <div class="ds-cart-seal"></div>
            <span class="ds-cart-footer-code">${project.code}</span>
          </div>
        </div>
        <div class="ds-cart-connector"></div>
      </div>
      <div class="ds-cart-desc">
        <p>${project.description}</p>
        <ul class="tags">${tagsHTML}</ul>
        <div class="project-links">${linksHTML}</div>
      </div>
    </div>`;
}

// Renders all cartridges into .project-grid
function renderCartridges() {
  const grid = document.querySelector('.project-grid');
  if (!grid) return;
  grid.innerHTML = PROJECTS.map(buildCartridge).join('');
}

document.addEventListener('DOMContentLoaded', renderCartridges);
