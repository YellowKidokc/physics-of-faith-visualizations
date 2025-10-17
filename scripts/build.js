import { promises as fs } from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import sharp from 'sharp';
import { marked } from 'marked';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT_DIR = path.resolve(__dirname, '..');
const IMAGES_DIR = path.join(ROOT_DIR, 'images');
const DIST_DIR = path.join(ROOT_DIR, 'dist');
const ASSETS_DIR = path.join(DIST_DIR, 'assets');

const IMAGE_EXTENSIONS = new Set(['.png', '.jpg', '.jpeg', '.gif', '.webp', '.tiff', '.bmp', '.svg']);
const TEXT_EXTENSIONS = ['.md', '.txt'];
const WATERMARK_TEXT = 'faiththruphysics.com';

async function ensureDir(dirPath) {
  await fs.mkdir(dirPath, { recursive: true });
}

async function removeDir(target) {
  await fs.rm(target, { recursive: true, force: true });
}

function isImageFile(fileName) {
  const ext = path.extname(fileName).toLowerCase();
  return IMAGE_EXTENSIONS.has(ext);
}

function prettifyTitle(fileName) {
  const nameWithoutExt = path.basename(fileName, path.extname(fileName));
  return nameWithoutExt
    .replace(/[_-]+/g, ' ')
    .replace(/\s+/g, ' ')
    .trim()
    .replace(/(^|\s)(\w)/g, (_, space, letter) => `${space}${letter.toUpperCase()}`);
}

async function readDescription(filePath) {
  const baseName = path.basename(filePath, path.extname(filePath));
  const dirName = path.dirname(filePath);

  for (const ext of TEXT_EXTENSIONS) {
    const candidate = path.join(dirName, `${baseName}${ext}`);
    try {
      const stats = await fs.stat(candidate);
      if (stats.isFile()) {
        const content = await fs.readFile(candidate, 'utf8');
        return marked.parse(content);
      }
    } catch (error) {
      // File does not exist; continue checking other extensions.
    }
  }
  return '';
}

function generateOverlaySvg(width, height) {
  const fontSize = Math.min(Math.max(Math.round(Math.min(width, height) * 0.02), 14), 42);
  const padding = Math.round(fontSize * 0.9);
  const textLengthFactor = WATERMARK_TEXT.length * fontSize * 0.6;
  let overlayWidth = Math.round(textLengthFactor + padding * 2);
  overlayWidth = Math.max(overlayWidth, fontSize * 8);
  overlayWidth = Math.min(overlayWidth, width);
  overlayWidth = Math.min(overlayWidth, 1400);
  overlayWidth = Math.max(overlayWidth, Math.min(width, fontSize * 6));

  let overlayHeight = Math.max(Math.round(fontSize * 3), fontSize * 2 + padding);
  overlayHeight = Math.min(overlayHeight, height);
  overlayHeight = Math.max(overlayHeight, Math.min(height, fontSize * 2.5));

  return Buffer.from(`<?xml version="1.0" encoding="UTF-8"?>
  <svg width="${overlayWidth}" height="${overlayHeight}" viewBox="0 0 ${overlayWidth} ${overlayHeight}" xmlns="http://www.w3.org/2000/svg">
    <style>
      text { font-family: 'Orbitron', 'Segoe UI', sans-serif; font-size: ${fontSize}px; fill: rgba(255,255,255,0.82); }
    </style>
    <rect x="0" y="${overlayHeight - fontSize - padding}" width="${overlayWidth}" height="${fontSize + padding}" rx="${Math.round(padding / 1.5)}" fill="rgba(0,0,0,0.45)" />
    <text x="${overlayWidth - padding}" y="${overlayHeight - Math.round(padding * 0.6)}" text-anchor="end">${WATERMARK_TEXT}</text>
  </svg>`);
}

function injectSvgWatermark(content) {
  if (!content.includes('</svg>')) {
    return content;
  }

  if (content.includes(WATERMARK_TEXT)) {
    return content;
  }

  const watermark = `\n  <g id="watermark" opacity="0.75">\n    <text x="98%" y="96%" text-anchor="end" font-family="'Orbitron', 'Segoe UI', sans-serif" font-size="16" fill="rgba(255,255,255,0.75)" paint-order="stroke" stroke="rgba(0,0,0,0.55)" stroke-width="1">${WATERMARK_TEXT}</text>\n  </g>\n`;

  return content.replace(/\n?\s*<\/svg>\s*$/i, `${watermark}</svg>`);
}

async function watermarkImage(sourcePath, destinationPath) {
  const extension = path.extname(sourcePath).toLowerCase();

  await ensureDir(path.dirname(destinationPath));

  if (extension === '.svg') {
    const svgContent = await fs.readFile(sourcePath, 'utf8');
    const updated = injectSvgWatermark(svgContent);
    await fs.writeFile(destinationPath, updated, 'utf8');
    return;
  }

  const metadata = await sharp(sourcePath, { animated: true, limitInputPixels: 0 }).metadata();
  let width = metadata.width ?? 1200;
  let height = metadata.height ?? 800;
  const frames = metadata.pages ?? 1;
  const pixelCount = width * height * frames;
  const MAX_PIXEL_COUNT = 80_000_000;
  let resizeOptions = null;

  if (pixelCount > MAX_PIXEL_COUNT) {
    const scale = Math.sqrt(MAX_PIXEL_COUNT / pixelCount);
    width = Math.max(1, Math.round(width * scale));
    height = Math.max(1, Math.round(height * scale));
    resizeOptions = {
      width,
      height,
      fit: 'inside',
      withoutEnlargement: true
    };
  }

  const overlay = generateOverlaySvg(width, height);

  let pipeline = sharp(sourcePath, { animated: true, limitInputPixels: 0 });
  if (resizeOptions) {
    pipeline = pipeline.resize(resizeOptions);
  }

  await pipeline
    .composite([
      {
        input: overlay,
        gravity: 'southeast'
      }
    ])
    .toFile(destinationPath);
}

async function processImageFile(fullPath, relativePath) {
  const ext = path.extname(fullPath).toLowerCase();
  if (!IMAGE_EXTENSIONS.has(ext)) {
    return null;
  }

  const outputPath = path.join(ASSETS_DIR, relativePath);
  await watermarkImage(fullPath, outputPath);

  const descriptionHtml = await readDescription(fullPath);
  const title = prettifyTitle(path.basename(fullPath));
  const publicPath = path.posix.join('assets', relativePath.split(path.sep).join('/'));

  return {
    title,
    descriptionHtml,
    imagePath: publicPath
  };
}

function escapeHtml(value) {
  return value
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

async function gatherImagesFromDirectory(rootDir, relativeBase = '') {
  const items = [];
  const entries = await fs.readdir(rootDir, { withFileTypes: true });
  const sortedEntries = entries
    .filter(entry => !entry.name.startsWith('.'))
    .sort((a, b) => a.name.localeCompare(b.name, undefined, { numeric: true, sensitivity: 'base' }));

  for (const entry of sortedEntries) {
    const entryFullPath = path.join(rootDir, entry.name);
    const entryRelativePath = relativeBase ? path.join(relativeBase, entry.name) : entry.name;

    if (entry.isDirectory()) {
      const nested = await gatherImagesFromDirectory(entryFullPath, entryRelativePath);
      items.push(...nested);
    } else if (entry.isFile() && isImageFile(entry.name)) {
      const processed = await processImageFile(entryFullPath, entryRelativePath);
      if (processed) {
        items.push(processed);
      }
    }
  }

  return items.sort((a, b) => a.title.localeCompare(b.title, undefined, { numeric: true, sensitivity: 'base' }));
}

function renderImageCard(item) {
  const descriptionBlock = item.descriptionHtml
    ? `<div class="image-description">${item.descriptionHtml}</div>`
    : '';

  return `
    <article class="image-card">
      <figure>
        <img src="${item.imagePath}" alt="${escapeHtml(item.title)}" loading="lazy" />
        <figcaption>
          <h3>${escapeHtml(item.title)}</h3>
          <div class="image-actions">
            <a class="button" href="${item.imagePath}" download>Download</a>
            <button type="button" class="button share-button" data-share="${item.imagePath}">Share URL</button>
          </div>
          ${descriptionBlock}
        </figcaption>
      </figure>
    </article>
  `;
}

function renderSection(title, items, extraClass = '') {
  if (!items.length) return '';
  return `
    <section class="gallery-section ${extraClass}">
      <div class="section-heading">
        <h2>${title}</h2>
        <div class="section-accent"></div>
      </div>
      <div class="gallery-grid">
        ${items.map(renderImageCard).join('\n')}
      </div>
    </section>
  `;
}

function renderPage(highlightSections, generalItems) {
  const highlightHtml = highlightSections
    .map(section => renderSection(section.displayName, section.items, 'highlight'))
    .join('\n');

  const generalHtml = renderSection('Gallery', generalItems, 'general');

  return `<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Syzygy Gallery — Physics of Faith Visual Archive</title>
    <meta name="description" content="Syzygy Gallery unifies Logos Unified Field, Quantum Mechanics, Theophysics, and Consciousness Substrate visuals." />
    <meta name="keywords" content="Logos Unified Field, Quantum Mechanics, Theophysics, Consciousness Substrate" />
    <meta property="og:title" content="Syzygy Gallery — Physics of Faith Visual Archive" />
    <meta property="og:description" content="Explore the Logos Unified Field, Quantum Mechanics, Theophysics, and Consciousness Substrate visual collection." />
    <meta name="theme-color" content="#04060d" />
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600&family=Inter:wght@300;400;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="styles.css" />
  </head>
  <body>
    <header class="site-header">
      <div class="header-content">
        <h1>Ψ A — Syzygy Gallery</h1>
        <p class="tagline">A cohesive archive of Logos Unified Field, Quantum Mechanics, Theophysics, and Consciousness Substrate visualizations.</p>
      </div>
    </header>
    <main>
      ${highlightHtml}
      ${generalHtml}
    </main>
    <footer class="site-footer">
      <p>© ${new Date().getFullYear()} faiththruphysics.com · Syzygy Gallery V2.0</p>
    </footer>
    <script src="script.js" type="module"></script>
  </body>
</html>`;
}

function formatSectionName(name) {
  return name
    .replace(/[_-]+/g, ' ')
    .replace(/\s+/g, ' ')
    .trim()
    .replace(/(^|\s)(\w)/g, (_, space, letter) => `${space}${letter.toUpperCase()}`);
}

async function build() {
  await removeDir(DIST_DIR);
  await ensureDir(ASSETS_DIR);

  const highlightSections = [];
  const generalItems = [];

  const entries = await fs.readdir(IMAGES_DIR, { withFileTypes: true });
  const sortedEntries = entries
    .filter(entry => !entry.name.startsWith('.'))
    .sort((a, b) => a.name.localeCompare(b.name, undefined, { numeric: true, sensitivity: 'base' }));

  for (const entry of sortedEntries) {
    if (entry.name === 'node_modules') continue;

    const entryPath = path.join(IMAGES_DIR, entry.name);

    if (entry.isDirectory()) {
      const items = await gatherImagesFromDirectory(entryPath, entry.name);
      if (items.length) {
        highlightSections.push({
          name: entry.name,
          displayName: formatSectionName(entry.name),
          items
        });
      }
    } else if (entry.isFile() && isImageFile(entry.name)) {
      const processed = await processImageFile(entryPath, entry.name);
      if (processed) {
        generalItems.push(processed);
      }
    }
  }

  highlightSections
    .sort((a, b) => a.displayName.localeCompare(b.displayName, undefined, { numeric: true, sensitivity: 'base' }))
    .forEach(section => {
      section.items.sort((a, b) => a.title.localeCompare(b.title, undefined, { numeric: true, sensitivity: 'base' }));
    });

  generalItems.sort((a, b) => a.title.localeCompare(b.title, undefined, { numeric: true, sensitivity: 'base' }));

  const page = renderPage(highlightSections, generalItems);
  await fs.writeFile(path.join(DIST_DIR, 'index.html'), page, 'utf8');

  await fs.copyFile(path.join(ROOT_DIR, 'src', 'styles.css'), path.join(DIST_DIR, 'styles.css'));
  await fs.copyFile(path.join(ROOT_DIR, 'src', 'script.js'), path.join(DIST_DIR, 'script.js'));
}

build().catch(error => {
  console.error('Build failed:', error);
  process.exitCode = 1;
});
