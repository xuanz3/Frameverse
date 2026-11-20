"""Build FRAMEVERSE / Zenless edition. No third-party runtime dependencies."""
from pathlib import Path
from html import escape as h
import json,re
R=Path(__file__).parent
D=json.loads((R/'data/archive.json').read_text(encoding='utf-8'))
PAGES=['Home','Agents','Districts','Bangboo','CG Archive','UI Language','Wallpapers','Journal','About']
URLS=['index.html','agents.html','scenes.html','bangboo.html','cg.html','ui.html','wallpapers.html','journal.html','about.html']
NAV=list(zip(PAGES,URLS))

def im(url,alt='',cls='',loading='lazy'):
    return f'<img src="{h(url)}" alt="{h(alt)}" class="{cls}" loading="{loading}" decoding="async">'

def topbar(current):
    nav=''.join(f'<a href="{u}" class="{ "active" if current==u else ""}">{h(t)}</a>' for t,u in NAV)
    return f'''<header class="topbar" id="top"><a class="brand" href="index.html" aria-label="FRAMEVERSE home"><span class="brand-icon">F<span>↗</span></span><span class="brand-text">FRAME<span>VERSE</span><small>VISUAL CULTURE ARCHIVE</small></span></a><nav class="desktop-nav" aria-label="Main navigation">{nav}</nav><div class="header-tools"><button type="button" class="icon-button search-open" aria-label="Open search"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7"><circle cx="10.8" cy="10.8" r="6.5"/><path d="m16 16 5 5"/></svg></button><span class="header-index">FV / 026</span><button type="button" class="mobile-toggle icon-button" aria-label="Open menu" aria-expanded="false"><span></span><span></span></button></div></header><nav class="mobile-nav" aria-label="Mobile navigation">{nav}</nav>'''

def footer():
    return '''<footer class="footer"><div class="footer-top"><span class="eyebrow">END OF TRANSMISSION / 终端联络</span><h2>THE ARCHIVE<br><i>NEVER SLEEPS.</i></h2><a href="agents.html" class="footer-explore">KEEP EXPLORING <span>↗</span></a></div><div class="footer-bottom"><a href="index.html" class="footer-wordmark">FRAMEVERSE<span>✳</span></a><div class="footer-links"><a href="about.html">ABOUT</a><a href="ui.html">UI LAB</a><a href="wallpapers.html">WALLPAPERS</a><a href="mailto:hello@frameverse.example" title="Placeholder address, not active" hidden>CONTACT</a></div><p>Independent fan-made visual archive · Zenless Zone Zero and related imagery belong to their respective rights holders. Not affiliated with HoYoverse.</p><span>© FRAMEVERSE · 2026</span></div></footer>'''

def search():
    return '''<div class="search-overlay" id="search-overlay" role="dialog" aria-modal="true" aria-label="Search archive" aria-hidden="true"><button class="search-close" type="button" aria-label="Close search">✕</button><div class="search-panel"><span class="eyebrow">FIND A SIGNAL / 全局搜索</span><div class="search-input-line"><span>⌕</span><input type="search" id="global-search" placeholder="Search the archive..." aria-label="Search all archive entries" autocomplete="off"></div><p class="search-help">SEARCH AGENTS, LOCATIONS, CG, BANGBOO & ARTWORK / ESC TO CLOSE</p><div id="search-results" class="search-results"></div></div></div><div class="lightbox" id="lightbox" role="dialog" aria-label="Artwork viewer" aria-modal="true" aria-hidden="true"><button type="button" class="lightbox-close" aria-label="Close artwork">✕</button><button type="button" class="lightbox-prev" aria-label="Previous artwork">←</button><div class="lightbox-content"><img id="lightbox-image" alt=""><div class="lightbox-info"><div><span class="eyebrow" id="lightbox-label">VISUAL ARCHIVE</span><h2 id="lightbox-title">ARTWORK</h2></div><a id="lightbox-download" download hidden>DOWNLOAD ORIGINAL ↧</a></div></div><button type="button" class="lightbox-next" aria-label="Next artwork">→</button></div>'''

def shell(page,title,description,content):
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#0b0d0f"><meta name="description" content="{h(description)}"><title>{h(title)} | FRAMEVERSE</title><link rel="icon" type="image/svg+xml" href="assets/icon.svg"><link rel="preload" href="assets/site.css" as="style"><link rel="stylesheet" href="assets/site.css"><script defer src="assets/site.js"></script></head><body data-page="{h(page)}">{topbar(page)}<main id="main">{content}</main>{footer()}{search()}</body></html>'''

def write(f,page,title,desc,content):
    (R/f).write_text(shell(page,title,desc,content),encoding='utf-8')

def sectionhead(no,tag,title,sub='',link=None):
    right=f'<a href="{link[1]}" class="section-more">{h(link[0])} <span>↗</span></a>' if link else ''
    return f'''<div class="section-header reveal"><div class="section-meta"><span class="section-number">{no} / {tag}</span><span class="section-rule"></span>{right}</div><div class="section-heading"><h2>{title}</h2><p>{sub}</p></div></div>'''

def intro(no,label,title,description,art=None):
    image=f'<div class="page-intro-art">{im(art,label,loading="eager")}</div>' if art else ''
    return f'''<section class="page-intro {"has-art" if art else ""}">{image}<div class="page-intro-content"><div class="eyebrow"><span class="status-dot"></span>{no} / {label}</div><h1>{title}</h1><p>{h(description)}</p><div class="intro-bottom"><span>FRAMEVERSE CULTURE NETWORK / 2026</span><span>SCROLL TO EXPLORE ↓</span></div></div></section>'''

# HOME
hero_data=[
    ('THE CITY','NEVER STANDS STILL.','NEW ERIDU / A VISUAL TRANSMISSION','A new way to explore the characters, streets and extraordinary visual language of Zenless Zone Zero.'),
    ('WELCOME TO','THE OTHER SIDE.','FRAMEVERSE / VISUAL LOG 002','Discover the art, worlds and people hiding inside the noise.'),
    ('COLOUR IN','EVERY FRAME.','FRAMEVERSE / VISUAL LOG 003','A living archive for the moments that deserve a closer look.'),
    ('BEYOND THE','ORDINARY.','FRAMEVERSE / VISUAL LOG 004','Follow the signal into a city built from stories.')]
slides=''.join(f'''<div class="hero-slide {'is-active' if i==0 else ''}" data-index="{i}" aria-hidden="{'false' if i==0 else 'true'}"><div class="hero-art" style="background-image:url('{D['wallpapers'][i]['image']}')"></div><div class="hero-shadow"></div><div class="hero-copy"><div class="eyebrow"><span class="status-dot"></span>{h(x[2])}</div><{"h1" if i==0 else "h2"}>{h(x[0])}<br><em>{h(x[1])}</em></{"h1" if i==0 else "h2"}><p>{h(x[3])}</p><a href="agents.html" class="solid-cta">EXPLORE THE ARCHIVE <span>↗</span></a></div></div>''' for i,x in enumerate(hero_data))
thumbs=''.join(f'<button type="button" data-slide="{i}" class="hero-thumb {'active' if i==0 else ''}" aria-label="View featured artwork {i+1}"><span>{i+1:02d}</span>{im(D['wallpapers'][i]['image'],'',loading='eager')}</button>' for i in range(4))
hero=f'''<section class="hero" aria-label="Featured visual stories"><div class="hero-slides">{slides}</div><div class="hero-bottom"><span class="hero-side">FRAMEVERSE — VISUAL ARCHIVE / Z.Z.Z.</span><div class="hero-controls"><button type="button" class="hero-arrow" data-dir="prev" aria-label="Previous featured artwork">←</button><span id="hero-counter">01 <i>/</i> 04</span><button type="button" class="hero-arrow" data-dir="next" aria-label="Next featured artwork">→</button></div><div class="hero-thumbnails">{thumbs}</div></div><div class="hero-progress"><span></span></div></section>'''

# Overview cards
feature_cards=[('01','CHARACTER ARCHIVE','The personalities behind the city.','agents.html',D['agents'][10]['image'],'agent'),('02','URBAN DOCUMENTS','Get lost in New Eridu.','scenes.html',D['scenes'][8]['image'],'scene'),('03','VISUAL EPISODES','The moments between stories.','cg.html',D['cg'][3]['image'],'cg'),('04','BANGBOO DATABASE','Small silhouettes, big personality.','bangboo.html',D['bangboo'][4]['image'],'boo')]
overview_cards=''.join(f'''<a class="overview-card {'overview-'+k}" href="{u}"><div class="overview-card-image">{im(pic,title)}<span class="overview-arrow">↗</span></div><div class="overview-card-footer"><span>{no} / {title}</span><p>{sub}</p></div></a>''' for no,title,sub,u,pic,k in feature_cards)
overview=f'''<section class="content-wrap home-overview">{sectionhead('01','THE DIRECTORY','A CITY.<br><i>IN FRAGMENTS.</i>','Not a wiki. Not a catalogue. A visual archive built to be explored.')}<div class="overview-grid">{overview_cards}</div></section>'''

# featured agents slider stage
agents=D['agents']
a0=agents[0]
agent_tabs=''.join(f'<button type="button" data-agent-feature="{i}" class="agent-tab {'active' if i==0 else ''}" data-src="{p['image']}" data-name="{h(p['name'])}" data-code="{p['id']}" aria-pressed="{'true' if i==0 else 'false'}"><span>{i+1:02d}</span><strong>{h(p['name'])}</strong><span>↗</span></button>' for i,p in enumerate(agents[:5]))
agentstage=f'''<section class="agent-stage-section"><div class="content-wrap"><div class="agent-stage-top"><span class="eyebrow">02 / CHARACTER DOSSIERS</span><span>FEATURED VISUAL ENTRIES / 05</span></div><div class="agent-showcase"><div class="agent-showcase-art"><div class="stage-halo"></div>{im(a0['image'],a0['name'],'agent-feature-image')}<span class="stage-caption">FIG. 001 / CHARACTER CARD</span></div><div class="agent-showcase-info"><span class="eyebrow">THE PEOPLE OF NEW ERIDU</span><h2>MEET THE<br><i>LINEUP.</i></h2><p>Stories begin with people. Browse visual dossiers assembled from the character cards in our archive.</p><div class="stage-current"><small>NOW VIEWING</small><h3 id="agent-feature-title">{h(a0['name'])}</h3></div><div class="agent-tabs">{agent_tabs}</div><a href="agents.html" class="inline-cta">ALL CHARACTER FILES <span>↗</span></a></div></div></div></section>'''

# city feature
s=D['scenes']
scene_panels=''.join(f'<a href="scenes.html" class="city-panel city-panel-{i+1}">{im(p['image'],'New Eridu street scene')}<span class="city-panel-overlay"><small>LOCATION FILE / {i+1:02d}</small><strong>{h(p['tag'])}</strong></span></a>' for i,p in enumerate([s[2],s[11],s[16]]))
city=f'''<section class="content-wrap city-section">{sectionhead('03','THE DISTRICTS','EVERY STREET<br><i>HAS A STORY.</i>','Twenty-four curated city photographs, from sunlit corners to neon evenings.',('EXPLORE ALL DISTRICTS','scenes.html'))}<div class="city-grid">{scene_panels}</div></section>'''

# CG highlighted
c=D['cg']
cg_feat=''.join(f'''<button class="cg-feature-card" type="button" data-lightbox="{p['image']}" data-title="{h(p['title'])}" data-label="CG ARCHIVE / {i+1:02d}">{im(p['image'],p['title'])}<span><small>VISUAL EPISODE / {i+1:02d}</small><strong>{h(p['title'])}</strong> <b>↗</b></span></button>''' for i,p in enumerate([c[3],c[7],c[2]]))
cgsec=f'''<section class="cg-feature-section"><div class="content-wrap">{sectionhead('04','STORY MOMENTS','PAUSE THE<br><i>STORY.</i>','Some frames are worth keeping.',('VIEW THE COMPLETE CG ARCHIVE','cg.html'))}<div class="cg-feature-grid">{cg_feat}</div></div></section>'''

b=D['bangboo']
boo_cards=''.join(f'''<button type="button" class="home-bang-card" data-lightbox="{p['image']}" data-title="{h(p['name'])}" data-label="BANGBOO / RANK {p['rank']}"><span class="rank-chip">{p['rank']}</span>{im(p['image'],p['name'])}<strong>{h(p['name'])}</strong></button>''' for p in b[:6])
boosec=f'''<section class="content-wrap bang-teaser">{sectionhead('05','BANGBOO SYSTEM','SMALL.<br><i>ICONIC.</i>','A little chaos goes a long way.',('OPEN THE BANGBOO ARCHIVE','bangboo.html'))}<div class="home-bang-grid">{boo_cards}</div></section>'''

ui=D['ui']
uisection=f'''<section class="home-ui-section"><div class="content-wrap ui-home-flex"><div class="ui-home-content"><span class="eyebrow">06 / VISUAL LANGUAGE LAB</span><h2>DESIGN IS<br><i>PART OF THE<br>STORY.</i></h2><p>The posters, cards, interface details and illustrated ephemera that make the world instantly recognisable.</p><a href="ui.html" class="solid-cta dark">ENTER UI LAB ↗</a></div><div class="ui-home-art"><div class="ui-art-one">{im(ui[0]['image'],'Visual illustration from ZZZ') }</div><div class="ui-art-two">{im(ui[6]['image'],'ZZZ promotional art') }</div><span class="ui-home-sticker">VISUAL<br>DNA ✳</span></div></div></section>'''

home=hero+overview+agentstage+city+cgsec+boosec+uisection
write('index.html','index.html','A visual archive of New Eridu','An independent Zenless Zone Zero visual culture archive of agents, city scenes, CG and graphic design.',home)

# Agents
agent_intro=intro('01','AGENT DOSSIERS','THE FACES <i>OF THE CITY.</i>','A collection of character-card visuals and experimental portraits, curated from the supplied visual archive.',D['wallpapers'][2]['image'])
agent_cards=''.join(f'''<a class="agent-card reveal" href="agent-{p['id']}.html" data-search="{h(p['name'].lower())}"><div class="agent-card-art">{im(p['image'],p['name'])}<span class="agent-card-number">{i+1:02d} / 12</span></div><div class="agent-card-info"><div><small>AGENT VISUAL FILE</small><strong>{h(p['name'])}</strong></div><span>↗</span></div></a>''' for i,p in enumerate(agents))
agentpage=agent_intro+f'''<section class="content-wrap archive-section"><div class="archive-toolbar"><div><span class="eyebrow">CHARACTER ARCHIVE / 人物档案</span><h2>SELECT AN ENTRY</h2></div><div class="toolbar-search"><span>⌕</span><input id="agent-filter" placeholder="Filter character cards..." aria-label="Filter character cards"></div></div><div class="agent-grid" id="agent-grid">{agent_cards}</div><p class="empty-state" id="agent-empty" hidden>No matching character files.</p></section>'''
write('agents.html','agents.html','Agents / Character Dossiers','Explore the visual character dossiers and poster designs of New Eridu.',agentpage)

for i,p in enumerate(agents):
    prev=agents[(i-1)%len(agents)];nxt=agents[(i+1)%len(agents)]
    detail=intro(f'{i+1:02d}','AGENT FILE',h(p['name']).replace(' / ','<br>') ,'An archived character visual. Artwork may contain text and character details in the original card.')+f'''<section class="content-wrap detail-section"><div class="detail-art-frame">{im(p['image'],p['name'],'detail-agent-image')}<span>ORIGINAL CARD ART / ENTRY {i+1:02d}</span></div><div class="detail-sidebar"><span class="eyebrow">ARCHIVE REFERENCE / {i+1:03d}</span><h2>{h(p['name'])}</h2><p>This page presents the supplied original character-card layout in full. Explore the typography, composition and art direction without replacing the original visual information.</p><div class="detail-metadata"><div><small>ARCHIVE CATEGORY</small><strong>CHARACTER VISUAL</strong></div><div><small>ITEM ID</small><strong>{h(p['id']).upper()}</strong></div><div><small>SOURCE</small><strong>USER-SUPPLIED CARD ART</strong></div></div><button type="button" class="outline-cta" data-lightbox="{p['image']}" data-title="{h(p['name'])}" data-label="CHARACTER CARD / {i+1:02d}">VIEW FULL ARTWORK ↗</button><div class="detail-pagination"><a href="agent-{prev['id']}.html">← PREVIOUS</a><a href="agents.html">ALL AGENTS</a><a href="agent-{nxt['id']}.html">NEXT →</a></div></div></section>'''
    write(f'agent-{p["id"]}.html', f'agent-{p["id"]}.html', p['name']+' / Character file', 'Visual archive character card from Zenless Zone Zero.',detail)

# Scene archives
scene_intro=intro('02','CITY DOCUMENTS','NEW ERIDU,<br><i>AFTER HOURS.</i>','A visual field guide to the city: storefronts, alleys, architecture, afternoon light and the in-between.',D['scenes'][3]['image'])
scene_categories=['ALL','DAYLIGHT','AFTERNOON','AFTER DARK','GOLDEN HOUR','INTERIOR','DETAIL STUDY','STREET OBJECTS']
scene_filter=''.join(f'<button type="button" class="filter-pill {"selected" if i==0 else ""}" data-filter="{h(cat)}" data-target="scenes" aria-pressed="{str(i==0).lower()}">{cat}</button>' for i,cat in enumerate(scene_categories))
scene_grid=''.join(f'''<button class="scene-card reveal" type="button" data-category="{h(p['tag'])}" data-title="{h(p['title'])}" data-lightbox="{p['image']}" data-label="{h(p['tag'])} · SCREENSHOT CREDIT IN ORIGINAL" ><div class="scene-img">{im(p['image'],p['title'])}</div><div class="scene-label"><span>{p['id'].upper()}</span><strong>{h(p['tag'])}</strong><span>↗</span></div></button>''' for p in D['scenes'])
scene_page=scene_intro+f'''<section class="content-wrap archive-section"><div class="archive-toolbar"><div><span class="eyebrow">VISUAL FIELD NOTES / 场景影像</span><h2>THE CITY, INDEXED.</h2></div><span class="total-count">24 VISUAL RECORDS</span></div><div class="filter-list">{scene_filter}</div><div class="scene-grid" id="scene-grid">{scene_grid}</div><p class="empty-state" id="scenes-empty" hidden>No scenes in this category.</p><p class="content-note">Original screenshot credits and in-image labels are preserved. Source material was supplied for this archive.</p></section>'''
write('scenes.html','scenes.html','Districts / New Eridu','A collection of scenes, streets and architecture from New Eridu.',scene_page)

# Bangboo
bang_intro=intro('03','BANGBOO ARCHIVE','SMALL IN SIZE.<br><i>BIG ON CHARACTER.</i>','A gallery of instantly recognisable Bangboo designs. Browse the original illustrations by archive rank.',D['wallpapers'][1]['image'])
bang_filters=''.join(f'<button type="button" class="filter-pill {"selected" if i==0 else ""}" data-filter="{r}" data-target="bangboos" aria-pressed="{str(i==0).lower()}">{label}</button>' for i,(r,label) in enumerate([('ALL','ALL UNITS'),('S','S SERIES'),('A','A SERIES')]))
bang_grid=''.join(f'''<button type="button" class="bang-card reveal" data-category="{p['rank']}" data-lightbox="{p['image']}" data-title="{h(p['name'])}" data-label="RANK {p['rank']} · BANGBOO FILE {i+1:03d}"><div class="bang-card-top"><span>BOO / {i+1:03d}</span><strong class="rank-chip">{p['rank']}</strong></div>{im(p['image'],p['name'],'bang-image')}<div class="bang-card-footer"><div><small>{p['rank']} SERIES · {p['id'].upper()}</small><strong>{h(p['name'])}</strong></div><span>↗</span></div></button>''' for i,p in enumerate(b))
bang_page=bang_intro+f'''<section class="content-wrap archive-section"><div class="archive-toolbar"><div><span class="eyebrow">UNIT DATABASE / 邦布图鉴</span><h2>MEET THE BANGBOO</h2></div><span class="total-count">{len(b)} INDEXED UNITS</span></div><div class="filter-list">{bang_filters}</div><div class="bang-grid" id="bangboo-grid">{bang_grid}</div><p class="empty-state" id="bangboos-empty" hidden>No units in this series.</p></section>'''
write('bangboo.html','bangboo.html','Bangboo / Visual index','An indexed gallery of Bangboo character artwork and illustrations.',bang_page)

# CG
cg_intro=intro('04','VISUAL EPISODES','THE MOMENTS<br><i>BETWEEN FRAMES.</i>','A cinematic archive of key narrative moments, brought together in one uninterrupted viewing space.',D['cg'][2]['image'])
cg_grid=''.join(f'''<button type="button" class="cg-archive-row reveal" data-lightbox="{p['image']}" data-title="{h(p['title'])}" data-label="{h(p['episode'])}"><div class="cg-archive-art">{im(p['image'],p['title'])}<span>VIEW IN FULL ↗</span></div><div class="cg-archive-meta"><span>CG / {i+1:02d}</span><strong>{h(p['title'])}</strong><small>{h(p['episode'])}</small></div></button>''' for i,p in enumerate(c))
cg_page=cg_intro+f'''<section class="content-wrap archive-section"><div class="archive-toolbar"><div><span class="eyebrow">FULL-WIDTH GALLERY / 剧情画廊</span><h2>STORY FRAMES</h2></div><span class="total-count">{len(c)} CINEMATIC FRAMES</span></div><div class="cg-archive-grid" id="cg-grid">{cg_grid}</div></section>'''
write('cg.html','cg.html','CG Archive / Visual Episodes','Explore the cinematic CG illustrations and narrative artwork.',cg_page)

# UI
ui_intro=intro('05','GRAPHIC CULTURE','THE VISUAL<br><i>LANGUAGE.</i>','A closer look at the posters, interface elements and visual ephemera that define the city.',D['ui'][13]['image'])
ui_filters=''.join(f'<button type="button" class="filter-pill {"selected" if i==0 else ""}" data-filter="{cat}" data-target="ui" aria-pressed="{str(i==0).lower()}">{label}</button>' for i,(cat,label) in enumerate([('ALL','ALL MATERIAL'),('ILLUSTRATION','ILLUSTRATION'),('EDITORIAL','POSTERS & PRINT'),('INTERFACE','INTERFACE OBJECTS')]))
ui_grid=''.join(f'''<button type="button" class="ui-tile reveal" data-category="{p['category']}" data-lightbox="{p['image']}" data-title="{h(p['title'])}" data-label="{h(p['category'])}">{im(p['image'],p['title'])}<span><strong>{h(p['title'])}</strong><small>VIEW ↗</small></span></button>''' for i,p in enumerate(ui))
ui_page=ui_intro+f'''<section class="content-wrap ui-intro-content"><div class="ui-manifesto"><span class="eyebrow">DESIGN LANGUAGE STUDIES / 图形系统</span><h2>THE INTERFACE<br>IS <i>THE UNIVERSE.</i></h2></div><p>From poster art to miniature interface objects, every visual fragment builds a sense of place. Here, form, texture and typography become part of the storytelling.</p></section><section class="content-wrap archive-section"><div class="archive-toolbar"><div><span class="eyebrow">THE MATERIAL LIBRARY</span><h2>VISUAL INDEX</h2></div><span class="total-count">{len(ui)} SELECTED PIECES</span></div><div class="filter-list">{ui_filters}</div><div class="ui-grid" id="ui-grid">{ui_grid}</div></section>'''
write('ui.html','ui.html','UI Language / Graphic archive','Graphic culture and visual identity from the world of Zenless Zone Zero.',ui_page)

# wallpapers
wall_intro=intro('06','WALLPAPER COLLECTION','ART FOR<br><i>EVERY SCREEN.</i>','Six selected panoramic illustrations, presented in a clean gallery for browsing and personal download.',D['wallpapers'][4]['image'])
wall_grid=''.join(f'''<div class="wallpaper-card reveal"><button type="button" class="wallpaper-art" data-lightbox="{p['image']}" data-title="{h(p['title'])}" data-label="WALLPAPER / {i+1:02d}" data-download="{p['image']}">{im(p['image'],p['title'])}<span class="wall-zoom">FULLSCREEN ↗</span></button><div class="wallpaper-bottom"><div><span>WALL / {i+1:02d} · {h(p['tag'])}</span><strong>{h(p['title'])}</strong></div><a href="{p['image']}" download="FRAMEVERSE-{p['id']}.webp" aria-label="Download {h(p['title'])}">DOWNLOAD ↓</a></div></div>''' for i,p in enumerate(D['wallpapers']))
wall_page=wall_intro+f'''<section class="content-wrap archive-section"><div class="archive-toolbar"><div><span class="eyebrow">DESKTOP WALLPAPERS / 高清壁纸</span><h2>CHOOSE A FREQUENCY</h2></div><span class="total-count">06 PANORAMIC VISUALS</span></div><div class="wallpaper-grid">{wall_grid}</div><p class="content-note">Downloaded files are optimized WebP versions for personal viewing. The source images are copyrighted works of their respective rights holders; no commercial license is conveyed.</p></section>'''
write('wallpapers.html','wallpapers.html','Wallpapers / New Eridu','Browse and download the selected panoramic wallpapers for personal viewing.',wall_page)

# journal (editorial, not fabricated news)
notes=[('FIELD NOTE 001','A CITY BUILT IN LAYERS','The recognizable rhythm of New Eridu lives in the smallest things: a storefront, a sign, a quiet corner of daylight.','scenes.html',D['scenes'][0]['image']),('FIELD NOTE 002','COLOUR AS A SIGNAL','In the visual language of Zenless Zone Zero, typography, colour and compositional noise keep every surface in motion.','ui.html',D['ui'][6]['image']),('FIELD NOTE 003','THE FRAME AS A MEMORY','The CG archive slows down the world for a moment, giving every scene room to breathe.','cg.html',D['cg'][5]['image']),('FIELD NOTE 004','THE ART OF THE SILHOUETTE','The visual character files capture personality in graphic form, from expressive poses to sharp typographic systems.','agents.html',D['agents'][5]['image'])]
j_intro=intro('07','EDITORIAL NOTES','NOTES FROM<br><i>THE CITY.</i>','Short visual essays and archive entry points, written as a guide to noticing the details.',D['wallpapers'][3]['image'])
j_cards=''.join(f'''<a class="journal-card reveal" href="{u}"><div class="journal-photo">{im(p,t)}</div><div class="journal-text"><span class="eyebrow">{id}</span><h2>{t}</h2><p>{d}</p><span class="inline-cta">READ THE VISUAL NOTE ↗</span></div></a>''' for id,t,d,u,p in notes)
j_page=j_intro+f'''<section class="content-wrap archive-section"><div class="archive-toolbar"><div><span class="eyebrow">A CULTURE OF LOOKING</span><h2>FOUR WAYS IN</h2></div><span class="total-count">EDITORIAL INDEX / 004</span></div><div class="journal-grid">{j_cards}</div></section>'''
write('journal.html','journal.html','Journal / Notes from the city','Editorial visual notes on the designs, characters and places of New Eridu.',j_page)

# About
about_intro=intro('08','ABOUT THE ARCHIVE','KEEP THE<br><i>SIGNAL ALIVE.</i>','FRAMEVERSE is an independent visual culture archive dedicated to exploring the design universe of Zenless Zone Zero.',D['wallpapers'][5]['image'])
about=about_intro+'''<section class="content-wrap about-statement"><div><span class="eyebrow">WHAT FRAMEVERSE IS</span><h2>A DIFFERENT WAY<br>TO <i>EXPLORE.</i></h2></div><div><p>FRAMEVERSE collects visual fragments from New Eridu: character artwork, city photography, cinematic images, Bangboo designs and interface culture. The archive is designed as a place to look closer—not as an official game database.</p><p>We are an independent, unofficial fan-made visual project. Zenless Zone Zero, its characters, images, names and associated marks belong to their respective rights holders. All original source imagery is reproduced only as supplied for the archive, with no claim of ownership or official affiliation.</p><a href="journal.html" class="inline-cta">EXPLORE THE EDITORIAL ↗</a></div></section><section class="content-wrap about-values"><div><span>01 / SEE</span><h3>VISUAL FIRST</h3><p>Big imagery, carefully chosen framing and less noise.</p></div><div><span>02 / EXPLORE</span><h3>BUILT TO DISCOVER</h3><p>Accessible filtering and archive navigation across each visual system.</p></div><div><span>03 / RESPECT</span><h3>CREDIT THE SOURCE</h3><p>Preserve creator information embedded in assets and acknowledge original owners.</p></div></section>'''
write('about.html','about.html','About FRAMEVERSE','Independent fan-made culture archive for Zenless Zone Zero.',about)

# Search index with category route hint, each entry linked to existing pages
index=[]
for a in D['agents']:index.append({'title':a['name'],'type':'AGENT','url':'agent-'+a['id']+'.html','image':a['image']})
for s in D['scenes']:index.append({'title':s['title']+' — '+s['tag'],'type':'DISTRICT','url':'scenes.html','image':s['image']})
for b in D['bangboo']:index.append({'title':b['name'],'type':'BANGBOO','url':'bangboo.html','image':b['image']})
for cg in D['cg']:index.append({'title':cg['title'],'type':'CG','url':'cg.html','image':cg['image']})
for u in D['ui']:index.append({'title':u['title'],'type':'UI','url':'ui.html','image':u['image']})
for w in D['wallpapers']:index.append({'title':w['title'],'type':'WALLPAPER','url':'wallpapers.html','image':w['image']})
(R/'data'/'search.json').write_text(json.dumps(index,ensure_ascii=False),encoding='utf-8')
# Remove obsolete routes, which belong to previous figures + convention model
for pat in ['figure-*.html','article-*.html']:
    for p in R.glob(pat):p.unlink()
for obsolete in ['collections.html','worlds.html','events.html','craft.html','resources.html','contact.html','privacy.html']:
    (R/obsolete).unlink(missing_ok=True)
(R/'robots.txt').write_text('User-agent: *\nAllow: /\n',encoding='utf-8')
print('Generated',len(list(R.glob('*.html'))),'pages.')
