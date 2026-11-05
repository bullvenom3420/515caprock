"""Build 515 Cap Rock's index.html from the 310 Meadowcrest page structure.
Same sections, layout, motion and scroll code; Cap Rock palette, type and content."""
import re, json
src = open('/home/claude/310meadowcrest/index.html').read()
s = src

def rep(a, b, count=1):
    global s
    n = s.count(a)
    assert n >= 1, ('MISSING', a[:80])
    if count == 1:
        assert n == 1, ('NOT UNIQUE', n, a[:80])
    s = s.replace(a, b)

def resub(pat, b, flags=re.S):
    global s
    s2, n = re.subn(pat, b, s, flags=flags)
    assert n >= 1, ('NO MATCH', pat[:80])
    s = s2

PHONE = '+18179094709'; PHONE_TXT = '(817) 909-4709'
URL = 'https://515caprock.com/'

# ---------------------------------------------------------------- head
desc = ("515 Cap Rock Drive, Richardson, Texas. A new French Country home in Collin County with "
        "4,719 square feet of living space: five bedrooms, five and a half baths, a study, a family "
        "room with a wood-burning fireplace, a scullery and covered outdoor living.")
resub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{desc}">')
resub(r'<title>[^<]*</title>', '<title>515 Cap Rock Drive, Richardson, TX 75080</title>')
resub(r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="{URL}">')
resub(r'<meta property="og:url" content="[^"]*">', f'<meta property="og:url" content="{URL}">')
resub(r'<meta property="og:title" content="[^"]*">', '<meta property="og:title" content="515 Cap Rock Drive, Richardson, TX 75080">')
resub(r'<meta property="og:description" content="[^"]*">', '<meta property="og:description" content="A new French Country home in Richardson with five bedrooms, five and a half baths and 4,719 square feet of living space.">')
resub(r'<meta property="og:image" content="[^"]*">', f'<meta property="og:image" content="{URL}assets/mobile/intro-mobile-poster.jpg">')
ld = {"@context": "https://schema.org", "@type": "SingleFamilyResidence", "name": "515 Cap Rock Drive",
      "url": URL, "description": "New French Country home in Richardson, Texas, in Collin County. Five bedrooms, "
      "five and a half baths, study, family room with a wood-burning fireplace, scullery, game room, loft and "
      "covered outdoor living. 4,719 square feet of living space.",
      "image": URL + "assets/mobile/intro-mobile-poster.jpg",
      "address": {"@type": "PostalAddress", "streetAddress": "515 Cap Rock Drive", "addressLocality": "Richardson",
                  "addressRegion": "TX", "postalCode": "75080", "addressCountry": "US"},
      "numberOfRooms": 5, "numberOfBedrooms": 5, "numberOfFullBathrooms": 5, "numberOfPartialBathrooms": 1,
      "floorSize": {"@type": "QuantitativeValue", "value": 4719, "unitCode": "FTK", "unitText": "sq ft"},
      "amenityFeature": [{"@type": "LocationFeatureSpecification", "name": n, "value": True} for n in
                         ["Primary suite on main floor", "Study", "Two-story foyer", "Wood-burning fireplace",
                          "Scullery", "Game room", "Loft", "Covered outdoor living", "Two-car garage"]]}
resub(r'<script type="application/ld\+json">.*?</script>', '<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False) + '</script>')
rep('family=Geist:wght@300..600&family=Instrument+Serif:ital@0;1&display=swap',
    'family=Geist:wght@300..600&family=Cormorant+Garamond:ital,wght@0,400;0,500;1,400&display=swap')

# ---------------------------------------------------------------- palette (Mix: rosé page, claret residence band)
NIGHT, NIGHT2, NINK, NMUTED = '#181214', '#2a1d21', '#f5efe8', '#b9a9a6'
for a, b in [('#13121b', NIGHT), ('#1d1b29', NIGHT2), ('#1c1a28', NIGHT2), ('#ecebf2', NINK), ('#9a97ab', NMUTED),
             ('rgba(236,235,242', 'rgba(245,239,232'), ('rgba(19,18,27', 'rgba(24,18,20'),
             ('#a19eb0', '#c4b2ae'), ('#7f7c8e', '#a8938f'), ('#f9f8f5', '#ecd9d3')]:
    s = s.replace(a, b)
rep(":root{--stone:#f5f3ef;--paper:#fbfaf8;--ink:#17161d;--ink-2:#4b4953;--muted:#8a8791;--rule:#dfdbd4;--bronze:#8b7b65;\n          --serif:'Instrument Serif',Georgia,'Times New Roman',serif;",
    ":root{--stone:#ecd9d3;--paper:#f8efeb;--ink:#2a1c1f;--ink-2:#4e3a3e;--muted:#6b4f54;--rule:#d4bcb5;--bronze:#8b4a45;\n          --serif:'Cormorant Garamond',Georgia,'Times New Roman',serif;")
rep('.masthead{background:linear-gradient(180deg,rgba(255,255,255,.96),rgba(255,255,255,0))}',
    '.masthead{background:linear-gradient(180deg,rgba(236,217,211,.96),rgba(236,217,211,0))}')
rep('background:rgba(251,250,248,.86);-webkit-backdrop-filter', 'background:rgba(248,239,235,.88);-webkit-backdrop-filter')
rep('background:rgba(255,255,255,.6)}', 'background:rgba(248,239,235,.6)}')
s = s.replace('.m-hero{display:block;background:#fff;', '.m-hero{display:block;background:var(--stone);')
rep('.footer{background:var(--night);color:#f5efe8;display:block', '.footer{background:#2a1c1f;color:#f5efe8;display:block')
rep('dialog.lb img{position:absolute;', 'dialog.lb img{position:absolute;')
# Cormorant sits smaller than Instrument Serif: nudge display sizes up a touch, add the residence band
rep('    /* call link */', '''    /* Cap Rock: drawings sit on the rosé page; the residence band is deep claret */
    .m-hero img{mix-blend-mode:multiply}
    .pl-sheet,.el-grid button{background:var(--paper)}
    #overview{background:#5c2b2c;color:#f5e9e4;--ink:#f5e9e4;--ink-2:#ead6d0;--muted:#e0c3bc;--rule:#7d4848;--bronze:#e8b9ae}
    #overview.block{padding-bottom:clamp(80px,9vw,128px)}
    .ov-lede,.h2,.stat b{font-weight:500}
    /* call link */''')

# ---------------------------------------------------------------- pets: baked into the frames now
resub(r'\s*<svg class="spin-image pets pets-desk show" id="petsDesk".*?</svg>', '')
resub(r'\s*<svg class="pets pets-mob".*?</svg>', '')
rep("    const petsDesk=document.getElementById('petsDesk');\n", '')
rep(" petsDesk.classList.toggle('show', i===0);", '')
dog = open('/home/claude/515caprock/tools/pets/dog.svg').read()
dog = dog[dog.index('<g class="pet-dog"'):dog.rindex('</svg>')]
cat = open('/home/claude/515caprock/tools/pets/cat.svg').read()
cat = cat[cat.index('<g class="pet-cat"'):cat.rindex('</svg>')]
tpl = ('<template id="petsTpl"><svg xmlns="http://www.w3.org/2000/svg">' + dog.strip() + '\n<!-- cat lying on the sill of the right-hand window -->\n'
       + cat.strip() + '</svg></template>\n')   # wrapped in <svg> so the browser parses the drawings as SVG
rep("window.MeadowcrestViewer(host, window.MEADOWCREST_MODEL, {petsMarkup:document.getElementById('petsDesk').innerHTML,",
    "window.CapRockViewer(host, window.CAPROCK_MODEL, {petsMarkup:document.getElementById('petsTpl').innerHTML,")
rep('<footer class="footer">', tpl + '<footer class="footer">')

# ---------------------------------------------------------------- masthead + intro
rep('<a href="#top" class="brand" aria-label="310 Meadowcrest home">310 <span>·</span> MEADOWCREST</a>',
    '<a href="#top" class="brand" aria-label="515 Cap Rock home">515 <span>·</span> CAP ROCK</a>')
rep('<img width="2300" height="1124" class="illustration" src="assets/front_elevation.jpg" alt="Original front architectural elevation for 310 Meadowcrest, November 20, 2025" loading="lazy">',
    '<img width="2300" height="1241" class="illustration" src="assets/front_elevation.jpg" alt="Front architectural elevation of 515 Cap Rock Drive, June 3, 2026" loading="lazy">')
rep('Original architectural elevation <span style="padding:0 14px">/</span> November 20, 2025',
    'Architectural elevation <span style="padding:0 14px">/</span> June 3, 2026')
rep('alt="Conceptual three-dimensional massing model of 310 Meadowcrest"', 'alt="Conceptual three-dimensional model of 515 Cap Rock Drive"')
s = s.replace('aria-label="The conceptual massing model turns one full rotation"', 'aria-label="The conceptual model of the house turns one full rotation"')
rep('<img src="assets/front_elevation-1200.webp" srcset="assets/front_elevation-1200.webp 1200w, assets/front_elevation.jpg 2300w" sizes="(max-width: 800px) 100vw, 1240px" width="1200" height="586" alt="Front elevation drawing of 310 Meadowcrest">',
    '<img src="assets/front_elevation-1200.webp" srcset="assets/front_elevation-1200.webp 1200w, assets/front_elevation.jpg 2300w" sizes="(max-width: 800px) 100vw, 1240px" width="1200" height="648" alt="Front elevation drawing of 515 Cap Rock Drive">')
rep('<div class="m-hero-cap"><span>Front elevation</span><span>November 2025</span></div>',
    '<div class="m-hero-cap"><span>Front elevation</span><span>June 2026</span></div>')

# ---------------------------------------------------------------- overview
resub(r'<p class="ov-lede">.*?</p>', '<p class="ov-lede">A French Country home of 4,719 square feet, now in progress.</p>')
resub(r'(<p class="ov-lede">[^<]*</p>\s*)<p class="ov-body">.*?</p>',
      r'\1<p class="ov-body">Five bedrooms and five and a half baths, with a two-story foyer under a 22′6″ ceiling. Brick and cast stone, three arched French doors and three roll-top dormers. The family room, kitchen and dining room open to a covered outdoor living area. The renderings and plans shown here are based on the June 3, 2026 drawings.</p>')
rep('<div><dt>Address</dt><dd>310 Meadowcrest Drive<br>Richardson, TX 75080</dd></div>', '<div><dt>Address</dt><dd>515 Cap Rock Drive<br>Richardson, TX 75080</dd></div>')
rep('<div><dt>Style</dt><dd>Tudor</dd></div>', '<div><dt>Style</dt><dd>French Country</dd></div>')
rep('<div><dt>Plans dated</dt><dd>November 20, 2025</dd></div>', '<div><dt>Plans dated</dt><dd>June 3, 2026</dd></div>')
resub(r'<div class="stats" role="list">.*?</div>\s*</div>\s*<ul class="features"', '''<div class="stats" role="list">
        <div class="stat" role="listitem"><b>4,719</b><span>Living sq ft</span></div>
        <div class="stat" role="listitem"><b>5,559</b><span>Total sq ft</span></div>
        <div class="stat" role="listitem"><b>5</b><span>Bedrooms</span></div>
        <div class="stat" role="listitem"><b>5.5</b><span>Baths</span></div>
        <div class="stat" role="listitem"><b>9,776</b><span>Sq ft lot</span></div>
        <div class="stat" role="listitem"><b>2</b><span>Car garage</span></div>
      </div>
      <ul class="features"''')
resub(r'<ul class="features" aria-label="Highlights">.*?</ul>',
      '<ul class="features" aria-label="Highlights"><li>Two-story foyer, 22′6″</li><li>Primary suite on the main floor</li><li>Study</li><li>Wood-burning fireplace</li><li>Scullery</li><li>Game room and loft</li><li>Covered outdoor living</li></ul>')

# ---------------------------------------------------------------- location (schools left out until confirmed)
rep('<p class="ov-body">On Meadowcrest Drive in the Canyon Creek neighborhood of Richardson, near Prairie Creek Park, in Dallas County. The home is zoned to Richardson ISD: Prairie Creek Elementary, Richardson North Junior High and J.J. Pearce High School.</p>',
    '<p class="ov-body">On Cap Rock Drive in Richardson, in Collin County.</p>')
resub(r'<div class="loc-cols">.*?</div>\s*</div>\s*(<div class="call">)', '''<div class="loc-cols">
          <dl class="facts">
            <div><dt>Street</dt><dd>Cap Rock Drive</dd></div>
            <div><dt>City</dt><dd>Richardson, TX 75080</dd></div>
            <div><dt>County</dt><dd>Collin</dd></div>
          </dl>
          <dl class="facts">
            <div><dt>School district</dt><dd>?</dd></div>
            <div><dt>Elementary</dt><dd>?</dd></div>
            <div><dt>Junior high</dt><dd>?</dd></div>
            <div><dt>High school</dt><dd>?</dd></div>
          </dl>
          <p class="note">School assignments can change. Confirm current zoning with the school district.</p>
        </div>
      </div>
      \\1''')

# ---------------------------------------------------------------- design direction: blank placeholders to fill later
PH = ('<figure class="%s ph-fig"><div class="ph" role="img" aria-label="%s inspiration image placeholder">'
      '<span>%s image</span></div><figcaption><span>%s</span><span>Inspiration</span></figcaption></figure>')
resub(r'<div class="dd-grid">.*?</div>\s*</div>\s*</section>',
      '<div class="dd-grid">\n        ' + PH % ('a', 'Exterior', 'Exterior', 'Exterior') + '\n        '
      + PH % ('b', 'Kitchen', 'Kitchen', 'Kitchen') + '\n      </div>\n    </div>\n  </section>')
rep('    /* call link */', '''    .dd-grid .ph-fig{background:var(--paper)}
    .ph-fig .ph{position:absolute;inset:clamp(10px,1.2vw,16px);border:1px dashed var(--rule);display:flex;align-items:center;justify-content:center}
    .ph-fig .ph span{font-size:11px;letter-spacing:.2em;text-transform:uppercase;color:var(--muted)}
    .ph-fig figcaption{color:var(--muted);background:none}
    .dd-grid .b.ph-fig{min-height:clamp(320px,34vw,520px)}
    /* call link */''')

# ---------------------------------------------------------------- order: claret residence band first, then the front elevation
m = re.search(r'\n<!-- HOME SCREEN[^\n]*-->\n<section class="m-hero".*?</section>\n', s, re.S)
assert m, 'm-hero'
hero = m.group(0)
s = s.replace(hero, '\n')
rep('  <!-- LOCATION AND SCHOOLS -->', '  <!-- FRONT ELEVATION -->' + hero.replace('\n<!-- HOME SCREEN', '\n<!-- (was the home screen)', 1).split('-->', 1)[1] + '\n  <!-- LOCATION AND SCHOOLS -->')
rep('    /* call link */', '''    .m-hero{padding:clamp(64px,7vw,104px) 0 0}
    @media(max-width:800px){.m-hero{padding:28px 0 0}#overview.block{padding-top:calc(88px + env(safe-area-inset-top,0px))}}
    /* call link */''')

# ---------------------------------------------------------------- plans
rep('<h2 class="h2" id="pl-title">Two floors, 4,450 conditioned square feet.</h2>', '<h2 class="h2" id="pl-title">Two floors, 4,719 conditioned square feet.</h2>')
rep('First floor <small>2,630 sf</small>', 'First floor <small>2,579 sf</small>')
rep('Second floor <small>1,820 sf</small>', 'Second floor <small>2,140 sf</small>')
s = s.replace('width="1425" height="1600" src="assets/first_plan.webp"', 'width="1580" height="1600" src="assets/first_plan.webp"')
s = s.replace('width="1425" height="1600" src="assets/second_plan.webp"', 'width="1580" height="1600" src="assets/second_plan.webp"')
resub(r'<ul class="rooms" aria-label="First floor rooms and ceiling heights">.*?</ul>', '''<ul class="rooms" aria-label="First floor rooms and ceiling heights">
            <li><span>Two-story foyer</span><span>22′6″ ceiling</span></li>
            <li><span>Study</span><span>10′</span></li>
            <li><span>Dining</span><span>10′</span></li>
            <li><span>Family room with wood-burning fireplace</span><span>11′</span></li>
            <li><span>Kitchen with 5′ × 11′ island</span><span>10′</span></li>
            <li><span>Scullery</span><span>10′</span></li>
            <li><span>Laundry</span><span>10′</span></li>
            <li><span>Powder room</span><span>10′</span></li>
            <li><span>Primary bedroom</span><span>Box ceiling to 11′</span></li>
            <li><span>Primary bath</span><span>10′</span></li>
            <li><span>Covered outdoor living</span><span>11′</span></li>
            <li><span>Two-car garage</span><span>566 sf</span></li>
          </ul>''')
resub(r'<ul class="rooms" aria-label="Second floor rooms and ceiling heights">.*?</ul>', '''<ul class="rooms" aria-label="Second floor rooms and ceiling heights">
            <li><span>Game room</span><span>10′</span></li>
            <li><span>Loft</span><span>10′</span></li>
            <li><span>Bedroom 2</span><span>9′</span></li>
            <li><span>Bedroom 3</span><span>10′</span></li>
            <li><span>Bedroom 4</span><span>9′</span></li>
            <li><span>Bedroom 5</span><span>9′</span></li>
            <li><span>Four full baths</span><span>8′–9′</span></li>
            <li><span>Attic storage</span><span></span></li>
          </ul>''')

# ---------------------------------------------------------------- elevations
s = s.replace('<img width="2300" height="1124" src="assets/front_elevation.jpg"', '<img width="2300" height="1241" src="assets/front_elevation.jpg"')
s = s.replace('<img width="2300" height="1097" src="assets/rear_elevation.jpg"', '<img width="2300" height="1117" src="assets/rear_elevation.jpg"')
resub(r'<p class="disclosure">.*?</p>', '<p class="disclosure">The rotating model is a conceptual study, not a surveyed or construction-ready model. It is built from the June 3, 2026 plans, elevations and roof plan, and shows only what those drawings show. Square footages are taken from the plans. Final construction, materials and finishes may differ.</p>')

# ---------------------------------------------------------------- 3D section + footer
s = s.replace('aria-label="Interactive 3D massing model"', 'aria-label="Interactive 3D model"')
s = s.replace('<span>Nov 2025</span>', '<span>June 2026</span>')
s = s.replace('3D massing model', '3D model').replace('massing model', 'model')
s = s.replace('A 120-frame conceptual massing model rotating 360 degrees', 'A 120-frame conceptual model of the house rotating 360 degrees')
resub(r'<div class="ft-top">.*?</div></div>\s*<div class="ft-bot">.*?</div>', '''<div class="ft-top"><div class="ft-word">515 Cap Rock</div><div class="ft-meta"><span>515 Cap Rock Drive, Richardson, TX 75080</span><span>Plans dated June 3, 2026</span></div></div>
    <div class="ft-bot"><span>© 2026 515 Cap Rock</span><span>Renderings are conceptual. Final construction may differ.</span></div>''')

# masthead turns claret over the residence band (desktop)
rep("const darkEls=[story,document.getElementById('mModel'),document.querySelector('.footer')];",
    "const darkEls=[story,document.getElementById('mModel'),document.querySelector('.footer')], claretEl=document.getElementById('overview');")
rep("mh.classList.toggle('on-dark', darkEls.some(el=>{const r=el.getBoundingClientRect(); return r.top<=70 && r.bottom>70;}));",
    "mh.classList.toggle('on-dark', darkEls.some(el=>{const r=el.getBoundingClientRect(); return r.top<=70 && r.bottom>70;}));\n      { const r=claretEl.getBoundingClientRect(); mh.classList.toggle('on-claret', r.top<=70 && r.bottom>70); }")
rep('    .masthead.on-dark .brand span{color:#b9a9a6}', '    .masthead.on-dark .brand span{color:#b9a9a6}\n    .masthead.on-claret{background:linear-gradient(180deg,rgba(92,43,44,.94),rgba(92,43,44,0));color:#f5e9e4}.masthead.on-claret .brand span{color:#e0c3bc}')

# ---------------------------------------------------------------- pets: live idle layer (desktop)
import os
meta = []
for i in range(120):
    fn = '/home/claude/515caprock/assets/pets-meta/%03d.json' % i
    meta.append(json.load(open(fn)) if os.path.exists(fn) else [None, None])
# clean (pet-free) window patches, one atlas per pet: the live copy sits on these, so
# no part of the baked-in pose can show through while it moves
from PIL import Image
ATLAS = {}
for k, name in ((0, 'dog'), (1, 'cat')):
    cells = [(i, m[k]) for i, m in enumerate(meta) if m[k] and 'patch' in m[k]
             and os.path.exists('/home/claude/515caprock/assets/pets-meta/%03d-%d.png' % (i, k))]
    if not cells:
        continue
    cw = max(d['patch'][2] for _, d in cells); ch = max(d['patch'][3] for _, d in cells)
    cols = 12; rows = (len(cells) + cols - 1) // cols
    atlas = Image.new('RGBA', (cols * cw, rows * ch), (0, 0, 0, 0))
    for n, (i, d) in enumerate(cells):
        im = Image.open('/home/claude/515caprock/assets/pets-meta/%03d-%d.png' % (i, k))
        cx, cy = (n % cols) * cw, (n // cols) * ch
        atlas.paste(im, (cx, cy)); d['cell'] = [cx, cy]
    os.makedirs('/home/claude/515caprock/assets/pets', exist_ok=True)
    atlas.save('/home/claude/515caprock/assets/pets/%s-patches.webp' % name, quality=92, method=6)
    ATLAS[name] = atlas.size

def inner(fn, cls):
    t = open(fn).read(); a = t.index('<g class="%s"' % cls); return t[a:t.rindex('</svg>')].strip()

DOG = inner('/home/claude/515caprock/tools/pets/dog.svg', 'pet-dog')
CAT = inner('/home/claude/515caprock/tools/pets/cat.svg', 'pet-cat')
def patch_svg(name):
    w, h = ATLAS.get(name, (1, 1))
    return ('<svg id="patch%s" viewBox="0 0 1 1" preserveAspectRatio="none"><image href="assets/pets/%s-patches.webp" width="%d" height="%d"/></svg>'
            % (name.title(), name, w, h))
live = ('<svg class="spin-image pet-live" id="petLive" viewBox="0 0 1600 1040" preserveAspectRatio="xMidYMid meet" aria-hidden="true">'
        '<defs><clipPath id="clipDog"><polygon id="clipDogP" points="0,0"/></clipPath><clipPath id="clipCat"><polygon id="clipCatP" points="0,0"/></clipPath></defs>'
        + patch_svg('dog') + patch_svg('cat') +
        '<g clip-path="url(#clipDog)"><svg id="liveDog" viewBox="0 0 100 132" preserveAspectRatio="none" overflow="visible">' + DOG + '</svg></g>'
        '<g clip-path="url(#clipCat)"><svg id="liveCat" viewBox="0 0 70 92" preserveAspectRatio="none" overflow="visible">' + CAT + '</svg></g></svg>')
rep('decoding="sync">\n', 'decoding="sync">\n      ' + live + '\n')
rep('</head>', '<script>window.CAPROCK_PETS=' + json.dumps(meta, separators=(',', ':')) + ';</script>\n</head>')
LIVE_CSS = """    /* pets: an animated twin over the baked-in pet, shown only while the rotation is at rest */
    .pet-live{pointer-events:none;visibility:hidden}.pet-live.on{visibility:visible}
    #liveDog,#liveCat{filter:brightness(.94)}
    #petLive .dog-tail{transform-box:view-box;transform-origin:73px 110px;animation:cr-wag .46s ease-in-out infinite alternate}
    #petLive .dog-head{transform-box:view-box;transform-origin:50px 62px;animation:cr-tilt 5.2s ease-in-out infinite}
    #petLive .dog-eyes{transform-box:view-box;transform-origin:50px 43px;animation:cr-blink 4.6s infinite}
    #petLive .cat-tail{transform-box:view-box;transform-origin:50px 84px;animation:cr-flick 3.4s ease-in-out infinite}
    #petLive .cat-head{transform-box:view-box;transform-origin:35px 45px;animation:cr-look 7s ease-in-out infinite}
    #petLive .cat-eyes{transform-box:view-box;transform-origin:35px 31px;animation:cr-blink 5.3s infinite 1.2s}
    @keyframes cr-wag{from{transform:rotate(-14deg)}to{transform:rotate(16deg)}}
    @keyframes cr-tilt{0%,58%,100%{transform:rotate(0)}66%,84%{transform:rotate(-8deg)}}
    @keyframes cr-blink{0%,93%,100%{transform:scaleY(1)}95.5%{transform:scaleY(.1)}}
    @keyframes cr-flick{0%,100%{transform:rotate(0)}35%{transform:rotate(-16deg)}50%{transform:rotate(-4deg)}65%{transform:rotate(-12deg)}}
    @keyframes cr-look{0%,40%,100%{transform:rotate(0)}48%,70%{transform:rotate(6deg)}}
    @media(prefers-reduced-motion:reduce){#petLive *{animation:none!important}}
    /* call link */"""
rep('    /* call link */', LIVE_CSS)
rep("      if(i!==shown){ show(i); shown=i; }", "      if(i!==shown){ show(i); shown=i; pets.hide(); }\n      pets.arm(i);")
rep("    function onScroll(){if(!pending){pending=true;requestAnimationFrame(render)}}",
    "    function onScroll(){pets.hide();if(!pending){pending=true;requestAnimationFrame(render)}}")
PETS_JS = """    function show(i){ img.src=frames[i]; }
    /* live pets: switched on ~0.25 s after the rotation stops, exactly over the baked-in pets */
    const pets=(function(){
      const L=document.getElementById('petLive'), M=window.CAPROCK_PETS||[];
      const parts=[['liveDog','clipDogP','patchDog'],['liveCat','clipCatP','patchCat']].map(ids=>ids.map(x=>document.getElementById(x)));
      const still=matchMedia('(prefers-reduced-motion: reduce)').matches; let t=0;
      function hide(){ clearTimeout(t); L.classList.remove('on'); }
      function arm(i){ clearTimeout(t); if(still) return;
        t=setTimeout(()=>{ const m=M[i]; if(!m || i!==shown || !(img.complete&&img.naturalWidth)) return; let any=false;
          parts.forEach(([svg,poly,pat],k)=>{ const d=m[k], ok=!!(d && d.facing>0.55 && d.px>300 && d.cell); svg.style.display=pat.style.display=ok?'':'none'; if(!ok) return; any=true;
            const [px,py,pw,ph]=d.patch; pat.setAttribute('x',px); pat.setAttribute('y',py); pat.setAttribute('width',pw); pat.setAttribute('height',ph);
            pat.setAttribute('viewBox',d.cell[0]+' '+d.cell[1]+' '+pw+' '+ph);
            svg.setAttribute('x',d.x); svg.setAttribute('y',d.y); svg.setAttribute('width',d.w); svg.setAttribute('height',d.h);
            poly.setAttribute('points',d.clip.map(q=>q.join(',')).join(' ')); });
          L.classList.toggle('on',any); },260); }
      return {hide,arm};
    })();"""
rep("    function show(i){ img.src=frames[i]; }", PETS_JS)
# ---------------------------------------------------------------- smooth intro: decode ahead, never stall on a frame
rep("""    const cache=[]; let started=false;
    function start(){ if(started) return; started=true;
      frames.forEach((src,i)=>{const im=new Image(); im.decoding='async'; im.src=src; cache[i]=im;}); }
    function show(i){ img.src=frames[i]; }""",
"""    /* Frames load in spin order, six at a time, and each one is decoded off the main thread before it
       is ever put on screen. If the frame the scroll asks for isn't ready yet, the nearest ready frame
       stands in, so the page never freezes waiting for a decode (the old stutter at the start and end). */
    const ready=new Uint8Array(N), cache=[]; let started=false, want=0;
    function start(){ if(started) return; started=true; ready[0]=1;
      let next=1, live=0;
      const pump=()=>{ while(live<6 && next<N){ const i=next++; live++;
          const im=new Image(); im.decoding='async'; im.src=frames[i]; cache[i]=im;
          const p=im.decode?im.decode():new Promise((ok,no)=>{im.onload=ok;im.onerror=no;});
          p.then(()=>{ ready[i]=1; live--; if(i===want) show(want); pump(); },()=>{ live--; pump(); }); } };
      pump(); }
    function nearest(i){ if(ready[i]) return i; for(let d=1;d<N/2;d++){ const a=(i-d+N)%N, b=(i+d)%N; if(ready[a]) return a; if(ready[b]) return b; } return 0; }
    function show(i){ want=i; const k=nearest(i); if(img.dataset.f!==String(k)){ img.src=frames[k]; img.dataset.f=String(k); } }""")
s = s.replace("if(!m || i!==shown || !(img.complete&&img.naturalWidth)) return;",
              "if(!m || i!==shown || img.dataset.f!==String(i) || !(img.complete&&img.naturalWidth)) return;")
rep('alt="Conceptual three-dimensional model of 515 Cap Rock Drive" decoding="sync">', 'alt="Conceptual three-dimensional model of 515 Cap Rock Drive" decoding="async" data-f="0">')
# 3D model hints: rotate, and tap a spot to zoom into it
rep('<p class="lede"><span class="hint-mouse">Drag sideways</span><span class="hint-touch">Swipe sideways</span> to walk around the house.</p>',
    '<p class="lede"><span class="hint-mouse">Drag sideways</span><span class="hint-touch">Swipe sideways</span> to walk around the house. <span class="hint-mouse">Click</span><span class="hint-touch">Tap</span> any spot to zoom in on it.</p>')
rep('<span><span class="hint-mouse">Drag to rotate</span><span class="hint-touch">Swipe to rotate</span></span>',
    '<span><span class="hint-mouse">Drag to rotate · click to zoom</span><span class="hint-touch">Swipe to rotate · tap or pinch to zoom</span></span>')
# slower spin: a longer scroll story
rep('    .story{height:270vh}', '    .story{height:420vh}')
# phone intro: slower (the video is longer now) and a quiet close button
rep('setTimeout(finish,8000);', 'setTimeout(finish,16000);')
# phone intro: start only once the whole clip is buffered (no mid-spin stalls); the poster is the exact first frame
rep("    v.play().catch(()=>setTimeout(finish,600));   // autoplay blocked: show the still front view briefly",
    """    let go=false; const play=()=>{ if(go||finished) return; go=true;
      const p=v.play(); if(p&&p.catch) p.catch(()=>setTimeout(finish,600));   // autoplay blocked: show the still front view briefly
    };
    if(v.readyState>=4) play(); else { v.addEventListener('canplaythrough',play,{once:true}); setTimeout(()=>{ if(v.readyState>=3) play(); },3500); }
    setTimeout(()=>{ if(!go) finish(); },6500);       // very slow connection: skip to the still front view""")
rep('<div class="m-chip">Conceptual rendering</div>', '<button type="button" class="m-skip" id="mSkip" aria-label="Skip intro"><svg viewBox="0 0 16 16" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"><path d="M4 4l8 8M12 4l-8 8"/></svg></button>\n  <div class="m-chip">Conceptual rendering</div>')
rep("    sec.addEventListener('click',()=>{ if(performance.now()-t0>1500){ finish(); exit(); } });",
    "    sec.addEventListener('click',()=>{ if(performance.now()-t0>1500){ finish(); exit(); } });\n    document.getElementById('mSkip').addEventListener('click',e=>{ e.stopPropagation(); finish(); exit(); });")
rep('    /* call link */', '''    .m-skip{display:none}
    @media(max-width:800px){
      .m-skip{display:grid;place-items:center;position:absolute;top:calc(14px + env(safe-area-inset-top,0px));right:max(14px,env(safe-area-inset-right,0px));width:40px;height:40px;padding:0;border:1px solid rgba(245,239,232,.16);border-radius:50%;background:transparent;color:var(--night-muted);cursor:pointer;transition:color .2s,border-color .2s;-webkit-tap-highlight-color:transparent;z-index:2}
      .m-skip svg{width:14px;height:14px}
      .m-skip:active,.m-skip:focus-visible{color:var(--night-ink);border-color:rgba(245,239,232,.4);outline:none}
    }
    /* call link */''')
rep("theme.content='#fbfaf8';", "theme.content='#ecd9d3';")
rep('<!-- cat lying on the sill of the right-hand window -->', '<!-- cat sitting on the sill of the Bed 5 window -->')

# ---------------------------------------------------------------- guardrail checks
low = s.lower()
for bad in ('meadowcrest', 'cross timbers', 'angie', 'stith', 'architects', 'alford', 'tudor', 'canyon creek', 'prairie', 'pearce', '2025', 'massing'):
    assert bad not in low, ('LEFTOVER', bad)
open('/home/claude/515caprock/index.html', 'w').write(s)
print('ok', len(s))
