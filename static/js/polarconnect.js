/* =====================================================
   PolarConnect – Main JavaScript
   ===================================================== */

'use strict';

/* ---------- Navbar scroll effect ---------- */
(function () {
  const navbar = document.getElementById('pc-navbar');
  if (!navbar) return;
  window.addEventListener('scroll', () => {
    navbar.classList.toggle('scrolled', window.scrollY > 40);
  }, { passive: true });
})();

/* ---------- Back to top ---------- */
(function () {
  const btn = document.getElementById('backToTop');
  if (!btn) return;
  window.addEventListener('scroll', () => {
    btn.classList.toggle('visible', window.scrollY > 300);
  }, { passive: true });
  btn.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));
})();

/* ---------- Animated counters ---------- */
function animateCounter(el) {
  const target = parseInt(el.dataset.target, 10);
  const duration = 1800;
  const start = performance.now();
  function step(now) {
    const elapsed = now - start;
    const progress = Math.min(elapsed / duration, 1);
    const eased = 1 - Math.pow(1 - progress, 3);
    el.textContent = Math.round(eased * target).toLocaleString();
    if (progress < 1) requestAnimationFrame(step);
  }
  requestAnimationFrame(step);
}

(function () {
  const counters = document.querySelectorAll('[data-target]');
  if (!counters.length) return;
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting && !entry.target.dataset.animated) {
        entry.target.dataset.animated = '1';
        animateCounter(entry.target);
      }
    });
  }, { threshold: 0.5 });
  counters.forEach(c => observer.observe(c));
})();

/* ---------- Lightbox ---------- */
(function () {
  const lightbox = document.getElementById('pcLightbox');
  if (!lightbox) return;
  const lbImg   = lightbox.querySelector('#lbImage');
  const lbCap   = lightbox.querySelector('#lbCaption');
  const lbClose = lightbox.querySelector('.pc-lightbox-close');

  document.querySelectorAll('[data-lightbox]').forEach(item => {
    item.addEventListener('click', () => {
      lbImg.src     = item.dataset.src || item.querySelector('img')?.src || '';
      lbCap.textContent = item.dataset.caption || '';
      lightbox.classList.add('open');
      document.body.style.overflow = 'hidden';
    });
  });

  function closeLightbox() {
    lightbox.classList.remove('open');
    document.body.style.overflow = '';
  }

  lbClose?.addEventListener('click', closeLightbox);
  lightbox.addEventListener('click', e => { if (e.target === lightbox) closeLightbox(); });
  document.addEventListener('keydown', e => { if (e.key === 'Escape') closeLightbox(); });
})();

/* ---------- Toast / Alert auto-dismiss ---------- */
(function () {
  const alerts = document.querySelectorAll('.alert-auto-dismiss');
  alerts.forEach(a => {
    setTimeout(() => {
      a.style.transition = 'opacity 0.5s';
      a.style.opacity    = '0';
      setTimeout(() => a.remove(), 500);
    }, 4000);
  });
})();

/* ---------- Password toggle ---------- */
document.querySelectorAll('[data-toggle-password]').forEach(btn => {
  btn.addEventListener('click', () => {
    const target = document.getElementById(btn.dataset.togglePassword);
    if (!target) return;
    const isText = target.type === 'text';
    target.type = isText ? 'password' : 'text';
    btn.querySelector('i')?.classList.toggle('fa-eye', isText);
    btn.querySelector('i')?.classList.toggle('fa-eye-slash', !isText);
  });
});

/* ---------- Interactive Polar Map ---------- */
function initPolarMap() {
  const mapEl = document.getElementById('polar-map');
  if (!mapEl || typeof L === 'undefined') return;

  const map = L.map('polar-map', {
    center: [10, 0],
    zoom: 2,
    minZoom: 1,
    maxZoom: 12,
    zoomControl: true,
  });

  window._polarMap = map;

  /* ---- Tile layers: ESRI Street (default) + ESRI Gray ---- */
  const esriStreet = L.tileLayer(
    'https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}',
    { attribution: 'Tiles &copy; Esri &mdash; Esri, DeLorme, NAVTEQ', maxZoom: 19 }
  );
  const esriGray = L.tileLayer(
    'https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Light_Gray_Base/MapServer/tile/{z}/{y}/{x}',
    { attribution: 'Tiles &copy; Esri', maxZoom: 16 }
  );

  // Test ESRI Street first; fall back to Gray if unavailable
  (function tryESRI() {
    var img = new Image();
    img.onload  = function() { esriStreet.addTo(map); window._activeBaseTile = esriStreet; };
    img.onerror = function() { esriGray.addTo(map);   window._activeBaseTile = esriGray;   };
    img.src = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/2/1/2?_t=' + Date.now();
    // Hard fallback after 4s
    setTimeout(function() {
      if (!map.hasLayer(esriStreet) && !map.hasLayer(esriGray)) {
        esriGray.addTo(map);
        window._activeBaseTile = esriGray;
      }
    }, 4000);
  })();

  /* Expose switcher globally for buttons */
  window._pcSwitchTiles = function(type) {
    if (map.hasLayer(esriStreet)) map.removeLayer(esriStreet);
    if (map.hasLayer(esriGray))   map.removeLayer(esriGray);
    if (type === 'street') { esriStreet.addTo(map); window._activeBaseTile = esriStreet; }
    else                   { esriGray.addTo(map);   window._activeBaseTile = esriGray;   }
  };

  /* ---- Marker icon factory ---- */
  function makeIcon(color, size, shape) {
    size = size || 18;
    var html;
    if (shape === 'star') {
      html = `<div style="width:${size}px;height:${size}px;background:${color};
        clip-path:polygon(50% 0%,61% 35%,98% 35%,68% 57%,79% 91%,50% 70%,21% 91%,32% 57%,2% 35%,39% 35%);
        box-shadow:0 2px 8px rgba(0,0,0,0.5);cursor:pointer"></div>`;
    } else if (shape === 'diamond') {
      html = `<div style="width:${size}px;height:${size}px;background:${color};
        transform:rotate(45deg);border:2px solid white;
        box-shadow:0 2px 8px rgba(0,0,0,0.5);cursor:pointer"></div>`;
    } else {
      html = `<div style="width:${size}px;height:${size}px;border-radius:50%;
        background:${color};border:3px solid white;
        box-shadow:0 2px 12px rgba(0,0,0,0.55);cursor:pointer;
        transition:transform 0.15s"></div>`;
    }
    return L.divIcon({ className: '', html, iconSize: [size, size],
      iconAnchor: [size/2, size/2], popupAnchor: [0, -(size/2 + 4)] });
  }

  /* ---- Colour + shape scheme ----
     🔵 Cyan circle    = Indian stations
     🔷 Blue circle    = Other national stations
     🟡 Gold diamond   = Geographic landmarks / ice features
     🔴 Red circle     = Climate-critical hotspots
     🟢 Green circle   = Wildlife / ecosystem hotspots
     🟠 Orange circle  = Expedition / historic sites
  */

  const hotspots = [

    /* ===== INDIAN STATIONS ===== */
    { name:'Maitri Station (India)', lat:-70.77, lng:11.73, type:'station', color:'#28C7E8', size:22,
      region:'Antarctica', research:'Glaciology, atmospheric ozone, geomagnetism, meteorology, upper atmosphere physics.',
      desc:'India\'s second Antarctic station in the Schirmacher Oasis, Queen Maud Land. Operational year-round since 1989. Hosts up to 25 researchers in summer.',
      demo:true },
    { name:'Bharati Station (India)', lat:-69.41, lng:76.19, type:'station', color:'#28C7E8', size:22,
      region:'Antarctica', research:'Oceanography, atmospheric science, marine biology, environmental monitoring.',
      desc:'India\'s most modern Antarctic station in the Larsemann Hills. Established 2012. Solar-wind-diesel hybrid power. Capacity ~24 personnel.',
      demo:true },
    { name:'Himadri Station (India — Arctic)', lat:78.92, lng:11.93, type:'station', color:'#28C7E8', size:22,
      region:'Arctic', research:'Arctic aerosols, ozone, glacier mass balance, sea ice monitoring, marine biology.',
      desc:'India\'s Arctic research station at Ny-Ålesund, Svalbard, Norway. Operational since 2008. Shared international research hub with 10+ nations.',
      demo:true },
    { name:'Dakshin Gangotri (India — Historic)', lat:-70.09, lng:12.00, type:'historic', color:'#E67E22', size:16, shape:'diamond',
      region:'Antarctica', research:'Historic: meteorology, glaciology, upper atmosphere physics.',
      desc:'India\'s first Antarctic base, established 1983. Decommissioned 1990 after encroaching ice. Now used as a supply depot during expeditions.',
      demo:true },

    /* ===== OTHER NATIONAL STATIONS ===== */
    { name:'McMurdo Station (USA)', lat:-77.85, lng:166.67, type:'station', color:'#1769AA', size:20,
      region:'Antarctica', research:'Earth sciences, biology, glaciology, astrophysics, climate.',
      desc:'The largest Antarctic research station with capacity for 1,200 people in summer. Operated by the US Antarctic Program (USAP) on Ross Island.',
      demo:true },
    { name:'Amundsen–Scott South Pole Station (USA)', lat:-89.99, lng:0.00, type:'station', color:'#1769AA', size:18,
      region:'Antarctica', research:'Astronomy (IceCube neutrino detector), atmospheric science, glaciology.',
      desc:'Located at the geographic South Pole, 2,835 m elevation. Temperature averages −49°C. The IceCube Neutrino Observatory is buried 2.4 km below.',
      demo:false },
    { name:'Scott Base (New Zealand)', lat:-77.85, lng:166.76, type:'station', color:'#27AE60', size:16,
      region:'Antarctica', research:'Geology, glaciology, biology, atmospheric science.',
      desc:'New Zealand\'s year-round Antarctic station near McMurdo, Ross Island. Named after British explorer Robert Falcon Scott.',
      demo:true },
    { name:'Concordia Station (France / Italy)', lat:-75.10, lng:123.35, type:'station', color:'#E67E22', size:16,
      region:'Antarctica', research:'Ice core paleoclimatology, astronomy, atmospheric physics, human physiology.',
      desc:'Joint French–Italian station on Dome C, East Antarctic plateau at 3,233 m altitude. The deepest ice cores ever extracted (800,000-year record) were drilled nearby.',
      demo:true },
    { name:'Halley VI Station (UK)', lat:-75.52, lng:-25.50, type:'station', color:'#9B59B6', size:16,
      region:'Antarctica', research:'Atmospheric chemistry, ozone monitoring, meteorology, space weather.',
      desc:'British Antarctic Survey station on the Brunt Ice Shelf. The discovery of the ozone hole in 1985 was made here. The station is designed to be relocated on skis as the ice shelf moves.',
      demo:true },
    { name:'Princess Elisabeth Station (Belgium)', lat:-71.95, lng:23.35, type:'station', color:'#27AE60', size:16,
      region:'Antarctica', research:'Glaciology, meteorology, atmospheric science, biology.',
      desc:'The world\'s first zero-emission Antarctic research station, opened 2009. Entirely powered by wind and solar energy.',
      demo:true },
    { name:'Neumayer Station III (Germany)', lat:-70.68, lng:-8.27, type:'station', color:'#E74C3C', size:16,
      region:'Antarctica', research:'Meteorology, atmospheric chemistry, marine biology, geophysics.',
      desc:'Germany\'s year-round Antarctic station on the Ekström Ice Shelf, Queen Maud Land. The station is elevated on hydraulic legs to prevent being buried by snow.',
      demo:true },
    { name:'Vostok Station (Russia)', lat:-78.46, lng:106.84, type:'station', color:'#E74C3C', size:16,
      region:'Antarctica', research:'Ice core climatology, geomagnetism, meteorology, subglacial lake research.',
      desc:'Remote Russian station on the East Antarctic plateau at 3,488 m. Site of the world\'s lowest recorded temperature: −89.2°C (1983). Overlies the subglacial Lake Vostok.',
      demo:true },
    { name:'Rothera Station (UK)', lat:-67.57, lng:-68.13, type:'station', color:'#9B59B6', size:16,
      region:'Antarctica', research:'Marine biology, glaciology, atmospheric science, climate change.',
      desc:'British Antarctic Survey\'s main hub on Adelaide Island, Antarctic Peninsula. Has a runway and harbour, serving as a logistics hub for field operations across the Peninsula.',
      demo:true },
    { name:'Ny-Ålesund International Research Hub', lat:78.93, lng:11.86, type:'station', color:'#27AE60', size:18,
      region:'Arctic', research:'Atmospheric chemistry, glaciology, marine biology, climate monitoring.',
      desc:'The world\'s northernmost permanent settlement with research infrastructure. Hosts stations from India, Germany, France, UK, Norway, Japan, South Korea, China, Italy, Netherlands and others.',
      demo:false },

    /* ===== GEOGRAPHIC LANDMARKS ===== */
    { name:'Geographic South Pole', lat:-90.00, lng:0.00, type:'landmark', color:'#F39C12', size:18, shape:'star',
      region:'Antarctica',
      desc:'The southernmost point on Earth. Located on the Antarctic plateau at 2,835 m above sea level. The Amundsen–Scott station sits here.',
      demo:false },
    { name:'Geographic North Pole', lat:89.99, lng:0.00, type:'landmark', color:'#F39C12', size:18, shape:'star',
      region:'Arctic',
      desc:'The northernmost point on Earth, located in the middle of the Arctic Ocean beneath approximately 4 km of water. Covered by drifting sea ice. No permanent land beneath.',
      demo:false },
    { name:'Antarctic Peninsula', lat:-68.00, lng:-65.00, type:'hotspot', color:'#E74C3C', size:16,
      region:'Antarctica',
      desc:'The fastest-warming region on Earth — warmed nearly 3°C in 50 years. Major ice shelves (Larsen A, B) have collapsed. A key area for climate change impact research.',
      demo:false },
    { name:'Ross Ice Shelf', lat:-81.50, lng:-175.00, type:'landmark', color:'#9B59B6', size:16, shape:'diamond',
      region:'Antarctica',
      desc:'The largest ice shelf in Antarctica — roughly the size of France (487,000 km²). Up to 750 m thick. Buttresses glaciers behind it; its collapse would accelerate sea-level rise.',
      demo:false },
    { name:'Thwaites Glacier ("Doomsday Glacier")', lat:-75.50, lng:-107.00, type:'hotspot', color:'#E74C3C', size:18,
      region:'Antarctica',
      desc:'One of the fastest-retreating and most closely monitored glaciers on Earth. Its complete collapse could raise global sea levels by ~65 cm. Subject of major international research (ITGC).',
      demo:false },
    { name:'Pine Island Glacier', lat:-75.17, lng:-100.00, type:'hotspot', color:'#E74C3C', size:16,
      region:'Antarctica',
      desc:'One of the fastest-moving glaciers in Antarctica, losing ~45 billion tonnes of ice per year. Part of the West Antarctic Ice Sheet\'s most vulnerable sector.',
      demo:false },
    { name:'Larsen C Ice Shelf', lat:-67.50, lng:-61.50, type:'hotspot', color:'#9B59B6', size:16,
      region:'Antarctica',
      desc:'In 2017, Iceberg A-68 calved from Larsen C — one of the largest icebergs ever recorded (5,800 km²). The ice shelf continues to thin and is considered at risk of future collapse.',
      demo:false },
    { name:'Lake Vostok (Subglacial)', lat:-77.00, lng:105.00, type:'landmark', color:'#28C7E8', size:14, shape:'diamond',
      region:'Antarctica',
      desc:'The largest known subglacial lake in Antarctica, buried under ~4 km of ice. Approximately 250 km long and 50 km wide. May harbour microbial life isolated for millions of years.',
      demo:false },
    { name:'Prydz Bay', lat:-69.00, lng:74.00, type:'landmark', color:'#27AE60', size:14, shape:'diamond',
      region:'Antarctica',
      desc:'A large bay in East Antarctica adjacent to India\'s Bharati Station. Important for oceanographic research and home to significant krill and penguin populations.',
      demo:false },
    { name:'Schirmacher Oasis', lat:-70.77, lng:11.50, type:'landmark', color:'#28C7E8', size:14, shape:'diamond',
      region:'Antarctica',
      desc:'A 34 km long ice-free rocky oasis in Queen Maud Land where India\'s Maitri station is located. Contains freshwater lakes and is unusually biodiverse for Antarctica.',
      demo:false },

    /* ===== ARCTIC HOTSPOTS ===== */
    { name:'Svalbard Archipelago', lat:78.22, lng:15.65, type:'hotspot', color:'#F39C12', size:18,
      region:'Arctic',
      desc:'Norwegian Arctic archipelago and global hub for Arctic science. Warming at ~7°C since 1970 — the fastest-warming place on Earth. Home to 10+ national research stations including India\'s Himadri.',
      demo:false },
    { name:'Greenland Ice Sheet', lat:72.00, lng:-40.00, type:'hotspot', color:'#E74C3C', size:18,
      region:'Arctic',
      desc:'The world\'s second-largest ice body — 1.7 million km², up to 3.5 km thick. Currently losing ~280 billion tonnes of ice per year. If fully melted, would raise sea levels by ~7 m.',
      demo:false },
    { name:'Jakobshavn Glacier, Greenland', lat:69.17, lng:-49.95, type:'hotspot', color:'#E74C3C', size:14,
      region:'Arctic',
      desc:'The fastest-moving glacier on Earth — up to 46 m/day. Responsible for ~6–7% of Greenland\'s total ice loss. Its meltwater contributes significantly to global sea-level rise.',
      demo:false },
    { name:'Arctic Sea Ice Minimum Zone', lat:85.00, lng:-10.00, type:'hotspot', color:'#E74C3C', size:16,
      region:'Arctic',
      desc:'The region of the Arctic Ocean that remains ice-covered at the September minimum. Sea ice extent at this minimum has declined ~13% per decade since 1979 — one of the clearest climate change signals.',
      demo:false },
    { name:'Franz Josef Land (Russia)', lat:81.00, lng:55.00, type:'landmark', color:'#9B59B6', size:14, shape:'diamond',
      region:'Arctic',
      desc:'A remote Russian archipelago near the North Pole, heavily glaciated. An important habitat for polar bears, walruses and seabirds. Contains several Russian research outposts.',
      demo:false },
    { name:'Beaufort Sea', lat:73.00, lng:-136.00, type:'hotspot', color:'#27AE60', size:14,
      region:'Arctic',
      desc:'The Beaufort Sea off northern Alaska and Canada is one of the most dynamic sea ice regions. The Beaufort Gyre — a large clockwise ocean current — plays a key role in Arctic freshwater balance.',
      demo:false },
    { name:'Barents Sea', lat:74.00, lng:38.00, type:'hotspot', color:'#27AE60', size:14,
      region:'Arctic',
      desc:'One of the most productive Arctic seas, with rich fish stocks and important shipping lanes. The Barents Sea ice edge has retreated dramatically in recent decades and is a key area for Arctic warming research.',
      demo:false },
    { name:'Bering Strait', lat:65.70, lng:-168.90, type:'landmark', color:'#F39C12', size:14, shape:'diamond',
      region:'Arctic',
      desc:'The 82 km wide strait separating Russia and Alaska. The only connection between the Pacific and Arctic Oceans. A critical conduit for warm Pacific water entering the Arctic.',
      demo:false },

    /* ===== WILDLIFE HOTSPOTS ===== */
    { name:'South Georgia Island', lat:-54.25, lng:-36.57, type:'hotspot', color:'#27AE60', size:16,
      region:'Sub-Antarctic',
      desc:'One of the world\'s most important wildlife sites — 100 million+ seabirds, 2–3 million fur seals and 400,000 elephant seals. Breeding ground for albatrosses, penguins and king penguins.',
      demo:false },
    { name:'Cape Royds, Ross Island', lat:-77.55, lng:166.17, type:'hotspot', color:'#27AE60', size:14,
      region:'Antarctica',
      desc:'Site of the world\'s most southerly Adélie penguin colony (~4,000 pairs). Also contains Shackleton\'s hut from the 1907–09 Nimrod Expedition, preserved as a heritage site.',
      demo:false },
    { name:'Deception Island', lat:-62.97, lng:-60.65, type:'hotspot', color:'#E67E22', size:14,
      region:'Antarctic Peninsula',
      desc:'An active volcanic caldera in the South Shetland Islands. Hosts one of the world\'s largest chinstrap penguin colonies (~100,000 pairs) and several research stations from multiple nations.',
      demo:false },
    { name:'Weddell Sea', lat:-74.00, lng:-40.00, type:'landmark', color:'#28C7E8', size:14, shape:'diamond',
      region:'Antarctica',
      desc:'The Weddell Sea is considered the clearest sea in the world and is the formation site of Antarctic Bottom Water — the densest ocean water on Earth that drives global thermohaline circulation.',
      demo:false },
    { name:'Davis Station (Australia)', lat:-68.58, lng:77.97, type:'station', color:'#27AE60', size:16,
      region:'Antarctica',
      desc:'Australia\'s busiest Antarctic station in Prydz Bay, near India\'s Bharati Station. India and Australia collaborate on joint oceanographic research in this region.',
      demo:true },

    /* ===== EXPEDITION HISTORIC SITES ===== */
    { name:'Cape Evans (Shackleton / Scott Hub)', lat:-77.64, lng:166.41, type:'historic', color:'#E67E22', size:14, shape:'diamond',
      region:'Antarctica',
      desc:'Site of Scott\'s hut from the 1910–13 Terra Nova Expedition. The last base from which Scott\'s party departed for the South Pole (arriving 17 January 1912, 33 days after Amundsen).',
      demo:false },
    { name:'Elephant Island', lat:-61.10, lng:-54.88, type:'historic', color:'#E67E22', size:14, shape:'diamond',
      region:'Antarctic Peninsula',
      desc:'Where Shackleton\'s crew sheltered for 4.5 months after their ship Endurance was crushed by ice in 1916. Shackleton then made an 800-mile open-boat voyage to South Georgia to rescue them.',
      demo:false },
    { name:'Cape Adare (First Antarctic Landing)', lat:-71.30, lng:170.14, type:'historic', color:'#E67E22', size:14, shape:'diamond',
      region:'Antarctica',
      desc:'Site of the first confirmed landing on Antarctica (1895) and the first Antarctic winter-over (1899). Borchgrevink\'s Southern Cross Expedition overwintered here — the first humans to do so.',
      demo:false },
  ];

  /* Load extra hotspots injected from Django views */
  const djStations = window.PC_MAP_STATIONS || [];
  djStations.forEach(s => {
    if (s.name && s.lat && s.lng) hotspots.push(s);
  });

  /* ---- Render all markers ---- */
  hotspots.forEach(function(s) {
    var iconColor = s.color || '#28C7E8';
    var iconSize  = s.size  || 16;
    var iconShape = s.shape || 'circle';
    var marker = L.marker([s.lat, s.lng], {
      icon: makeIcon(iconColor, iconSize, iconShape)
    }).addTo(map);

    /* Type label */
    var typeLabel = {
      station:  'Research Station',
      landmark: 'Geographic Feature',
      hotspot:  'Climate / Science Hotspot',
      historic: 'Historic / Expedition Site',
    }[s.type] || 'Location';

    /* Demo tag */
    var demoNote = s.demo
      ? '<p style="font-size:0.68rem;color:#E98C7B;margin-top:6px;padding-top:6px;border-top:1px solid rgba(255,255,255,0.12)"><i class="fas fa-info-circle me-1"></i>Indicative / demonstration data</p>'
      : '';

    /* Research tag */
    var researchNote = s.research
      ? `<p style="font-size:0.75rem;color:rgba(255,255,255,0.65);margin:6px 0 0"><strong style="color:#28C7E8">Research:</strong> ${s.research}</p>`
      : '';

    /* Region badge */
    var regionBadge = s.region
      ? `<span style="background:rgba(40,199,232,0.15);color:#28C7E8;border:1px solid rgba(40,199,232,0.3);border-radius:4px;padding:1px 6px;font-size:0.63rem;font-weight:600;text-transform:uppercase;letter-spacing:0.5px">${s.region}</span>`
      : '';

    var typeColors = {
      station:  '#28C7E8',
      landmark: '#F39C12',
      hotspot:  '#E74C3C',
      historic: '#E67E22',
    };
    var accentColor = typeColors[s.type] || '#28C7E8';

    marker.bindPopup(`
      <div style="min-width:240px;max-width:300px">
        <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:6px">
          <span style="font-size:0.62rem;color:${accentColor};text-transform:uppercase;letter-spacing:1px;font-weight:700">${typeLabel}</span>
          ${regionBadge}
        </div>
        <h6 style="color:white;margin:0 0 7px;font-size:0.95rem;line-height:1.3;font-weight:700">${s.name}</h6>
        <p style="font-size:0.8rem;color:rgba(255,255,255,0.78);margin:0;line-height:1.55">${s.desc}</p>
        ${researchNote}
        ${demoNote}
      </div>
    `, { maxWidth: 310 });

    marker.on('mouseover', function() { this.openPopup(); });
  });

  /* ---- Layer control ---- */
  L.control.layers(
    { 'ESRI Street': esriStreet, 'ESRI Gray': esriGray },
    {},
    { position: 'topright', collapsed: false }
  ).addTo(map);
}

document.addEventListener('DOMContentLoaded', initPolarMap);

/* ---------- Quiz Engine ---------- */
(function () {
  const quizForm = document.getElementById('quizForm');
  if (!quizForm) return;

  const questions   = document.querySelectorAll('.pc-quiz-question');
  const progressFill = document.getElementById('quizProgressFill');
  const progressText = document.getElementById('quizProgressText');
  let current = 0;

  function showQuestion(idx) {
    questions.forEach((q, i) => q.classList.toggle('d-none', i !== idx));
    const pct = ((idx + 1) / questions.length) * 100;
    if (progressFill) progressFill.style.width = pct + '%';
    if (progressText) progressText.textContent = `Question ${idx + 1} of ${questions.length}`;
  }

  document.getElementById('quizNext')?.addEventListener('click', () => {
    const opts = questions[current].querySelectorAll('.pc-quiz-option');
    const selected = [...opts].find(o => o.classList.contains('selected'));
    if (!selected) { alert('Please select an answer.'); return; }
    if (current < questions.length - 1) {
      current++;
      showQuestion(current);
    } else {
      quizForm.submit();
    }
  });

  document.querySelectorAll('.pc-quiz-option').forEach(opt => {
    opt.addEventListener('click', () => {
      const siblings = opt.closest('.pc-quiz-question').querySelectorAll('.pc-quiz-option');
      siblings.forEach(s => s.classList.remove('selected'));
      opt.classList.add('selected');
      opt.querySelector('input[type=radio]').checked = true;
    });
  });

  if (questions.length) showQuestion(0);
})();

/* ---------- Global Search ---------- */
(function () {
  const form  = document.getElementById('globalSearchForm');
  const input = document.getElementById('globalSearchInput');
  if (!form || !input) return;
  form.addEventListener('submit', e => {
    if (!input.value.trim()) {
      e.preventDefault();
      input.focus();
    }
  });
})();

/* ---------- File upload preview ---------- */
document.querySelectorAll('input[type=file][data-preview]').forEach(input => {
  input.addEventListener('change', () => {
    const previewEl = document.getElementById(input.dataset.preview);
    if (!previewEl || !input.files[0]) return;
    const reader = new FileReader();
    reader.onload = e => {
      previewEl.src = e.target.result;
      previewEl.style.display = 'block';
    };
    reader.readAsDataURL(input.files[0]);
  });
});

/* ---------- Smooth anchor links ---------- */
document.querySelectorAll('a[href^="#"]').forEach(a => {
  a.addEventListener('click', e => {
    const target = document.querySelector(a.getAttribute('href'));
    if (target) {
      e.preventDefault();
      target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  });
});
