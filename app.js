
let DATA = [];
let COLLECTIONS = [];
let filtered = [];
const byId = (id)=>document.getElementById(id);

async function loadJSON(path){
  const res = await fetch(path, {cache:'no-store'});
  return res.ok ? res.json() : [];
}

async function loadAll(){
  [DATA, COLLECTIONS] = await Promise.all([
    loadJSON('gallery.json'),
    loadJSON('collections.json')
  ]);
  filtered = [...DATA];
  hydrateTagFilter();
  renderFeatured();
  renderGrid();
  handleHashOpen();
}

function renderFeatured(){
  const wrap = byId('featured');
  const row = byId('featuredRow');
  const count = byId('featuredCount');
  if(!COLLECTIONS.length){ wrap.classList.add('hidden'); return; }
  wrap.classList.remove('hidden');
  count.textContent = `${COLLECTIONS.length} highlighted set${COLLECTIONS.length>1?'s':''}`;
  row.innerHTML = '';
  COLLECTIONS.forEach(col => {
    const card = document.createElement('article');
    card.className='featured-card';
    const img = document.createElement('img');
    img.className='featured-cover';
    img.src = col.cover || 'images/sample1.jpg';
    img.alt = col.title || col.slug;
    card.appendChild(img);
    const pad = document.createElement('div'); pad.className='featured-pad';
    const h3 = document.createElement('h3'); h3.textContent = col.title || col.slug;
    pad.appendChild(h3);
    const p = document.createElement('p'); p.textContent = col.summary || '';
    p.style.opacity=.85; p.style.margin='0.25rem 0 0.5rem';
    pad.appendChild(p);
    const badges = document.createElement('div'); badges.className='badges';
    const b1 = document.createElement('span'); b1.className='badge gold'; b1.textContent='FEATURED';
    badges.appendChild(b1);
    if(col.pages){ const b = document.createElement('span'); b.className='badge'; b.textContent = `${col.pages} pages`; badges.appendChild(b); }
    if(col.images){ const b = document.createElement('span'); b.className='badge'; b.textContent = `${col.images} images`; badges.appendChild(b); }
    if(col.tags){ col.tags.slice(0,3).forEach(t=>{ const b=document.createElement('span'); b.className='badge'; b.textContent=t; badges.appendChild(b); }); }
    pad.appendChild(badges);
    const actions = document.createElement('div'); actions.className='actions';
    const open = document.createElement('a'); open.className='btn'; open.textContent='Open Set'; open.href = col.href || `collections/${col.slug}/index.html`; open.target='_self';
    const view = document.createElement('a'); view.className='btn secondary'; view.textContent='Cover Image'; view.href = col.cover || '#'; view.target='_blank';
    actions.appendChild(open); actions.appendChild(view);
    pad.appendChild(actions);
    card.appendChild(pad);
    row.appendChild(card);
  });
}

function createImageCard(item){
  const card = document.createElement('article');
  card.className='card';
  const img = document.createElement('img');
  img.className='thumb'; img.loading='lazy'; img.src=item.thumb || item.src; img.alt=item.title || item.file || '';
  img.onerror=()=>{ img.src=item.src; };
  card.appendChild(img);
  card.onclick=()=>openModal(item);
  return card;
}

function renderGrid(){
  const grid = byId('grid');
  grid.innerHTML='';

  // Only show non-featured images in main grid
  const regularImages = filtered.filter(item => item.featured !== true);
  
  // Add section header for regular images
  if (regularImages.length > 0 && DATA.some(item => item.featured === true)) {
    const header = document.createElement('h2');
    header.textContent = '📁 Gallery Collection';
    header.style.marginBottom = '1.5rem';
    header.style.fontSize = '1.5rem';
    grid.appendChild(header);
  }
  
  regularImages.forEach(item => {
    const card = createImageCard(item);
    grid.appendChild(card);
  });
}

function slug(s){ return (s||'').toLowerCase().replace(/[^a-z0-9]+/g,'-').replace(/^-+|-+$/g,''); }

let shareStatusTimer = null;

function setShareStatus(message, isError=false){
  const status = byId('modalShareStatus');
  if(!status) return;
  status.textContent = message;
  status.classList.toggle('error', !!isError);
  if(shareStatusTimer){ clearTimeout(shareStatusTimer); }
  if(message){
    shareStatusTimer = setTimeout(()=>{
      status.textContent='';
      status.classList.remove('error');
    }, 4000);
  }
}

function openModal(item){
  history.replaceState(null,'','#'+(item.id || slug(item.file)));
  const m = byId('modal');
  byId('modalImg').src = item.src;
  byId('modalTitle').textContent = item.title || item.file;
  byId('modalCaption').textContent = item.caption || '';
  byId('modalFile').textContent = item.file || '';
  byId('modalCreated').textContent = item.created || '';
  const tagBox = byId('modalTags'); tagBox.innerHTML='';
  (item.tags||[]).forEach(t=>{ const span=document.createElement('span'); span.className='tag'; span.textContent=t; tagBox.appendChild(span);});
  const sib = byId('modalSiblings'); sib.innerHTML='';
  DATA.slice(0,10).forEach(s=>{ const a=document.createElement('a'); a.href='#'+(s.id||slug(s.file)); a.textContent=(s.title||s.file).slice(0,24); a.onclick=(e)=>{e.preventDefault(); openModal(s);} ; sib.appendChild(a); });

  const shareLink = `${location.origin}${location.pathname}#${item.id || slug(item.file)}`;
  const shareInput = byId('modalShareLink');
  if(shareInput){
    shareInput.value = shareLink;
    shareInput.onclick = ()=>shareInput.select();
  }
  const shareBtn = byId('modalShare');
  if(shareBtn){
    shareBtn.onclick = async ()=>{
      try{
        if(navigator.share){
          await navigator.share({title:item.title||item.file,url:shareLink});
          setShareStatus('Share dialog opened.');
        }else if(navigator.clipboard && navigator.clipboard.writeText){
          await navigator.clipboard.writeText(shareLink);
          setShareStatus('Link copied to clipboard.');
        }else{
          if(shareInput){
            shareInput.focus();
            shareInput.select();
            document.execCommand('copy');
            setShareStatus('Link copied to clipboard.');
          }
        }
      }catch(err){
        console.error('Share failed', err);
        setShareStatus('Unable to share this image.', true);
      }
    };
  }
  const downloadBtn = byId('modalDownload');
  if(downloadBtn){
    downloadBtn.href = item.src;
    downloadBtn.download = item.file || `${slug(item.title||'image')}.png`;
  }
  const fullBtn = byId('modalOpenFull');
  if(fullBtn){
    fullBtn.href = item.src;
  }

  setShareStatus('');
  m.classList.remove('hidden'); m.setAttribute('aria-hidden','false');
}
function closeModal(){ const m=byId('modal'); m.classList.add('hidden'); m.setAttribute('aria-hidden','true'); }
function handleHashOpen(){ const h=location.hash.replace('#',''); if(!h)return; const it=DATA.find(x=>(x.id||slug(x.file))===h); if(it){ openModal(it); } }
function hydrateTagFilter(){ const sel=byId('tagFilter'); const tags=new Set(); DATA.forEach(x=>(x.tags||[]).forEach(t=>tags.add(t))); sel.innerHTML='<option value=\"\">All Tags</option>'+Array.from(tags).sort().map(t=>`<option value=\"${t}\">${t}</option>`).join(''); }
function applyFilters(){ const q=byId('searchInput').value.trim().toLowerCase(); const tag=byId('tagFilter').value; filtered=DATA.filter(x=>{ const hay=[x.title,x.caption,(x.tags||[]).join(' '),x.file].join(' ').toLowerCase(); const qOk=!q||hay.includes(q); const tOk=!tag||(x.tags||[]).includes(tag); return qOk&&tOk;}); renderGrid(); }
function filterByTag(t){ byId('tagFilter').value=t; applyFilters(); }

window.addEventListener('DOMContentLoaded', () => {
  byId('closeModal').onclick = closeModal;
  byId('modalBackdrop').onclick = closeModal;
  byId('searchInput').oninput = applyFilters;
  byId('tagFilter').onchange = applyFilters;
  loadAll();
});
