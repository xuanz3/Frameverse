/* FRAMEVERSE / progressive enhancement. No runtime dependencies. */
(() => {
  'use strict';
  const $ = (selector, root=document) => root.querySelector(selector);
  const $$ = (selector, root=document) => [...root.querySelectorAll(selector)];
  const header = $('.header');
  const progress = $('.scroll-progress');
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const safeText = (value) => String(value || '').toLocaleLowerCase().trim();
  const showToast = (message) => {
    const toast = $('.toast'); if (!toast) return;
    toast.textContent = message; toast.classList.add('show');
    window.clearTimeout(showToast.timeout);
    showToast.timeout = window.setTimeout(() => toast.classList.remove('show'), 3500);
  };

  const updateScroll = () => {
    if (header) header.classList.toggle('scrolled', window.scrollY > 25);
    const max = document.documentElement.scrollHeight - window.innerHeight;
    if (progress) progress.style.width = `${max > 0 ? 100 * window.scrollY / max : 0}%`;
  };
  window.addEventListener('scroll', updateScroll, {passive: true}); updateScroll();

  // Accessible mobile navigation.
  const mobileToggle = $('.mobile-toggle'), mobileNav = $('.nav-mobile');
  const closeMenu = () => {
    if (!mobileToggle || !mobileNav) return;
    mobileToggle.setAttribute('aria-expanded','false'); mobileToggle.setAttribute('aria-label','Open menu');
    header?.classList.remove('menu-open'); mobileNav.inert = true;
    if (!$('.search-overlay:not([hidden])')) document.body.classList.remove('no-scroll');
  };
  if (mobileToggle && mobileNav) {
    mobileNav.inert = true;
    mobileToggle.addEventListener('click', () => {
      const opening = mobileToggle.getAttribute('aria-expanded') !== 'true';
      if (!opening) return closeMenu();
      mobileToggle.setAttribute('aria-expanded','true'); mobileToggle.setAttribute('aria-label','Close menu');
      header.classList.add('menu-open'); mobileNav.inert = false;
      document.body.classList.add('no-scroll');
    });
    $$('a', mobileNav).forEach(a => a.addEventListener('click',closeMenu));
    window.addEventListener('resize', () => {if (window.innerWidth > 1050) closeMenu();});
  }

  // Site-wide search opens with Ctrl / Cmd + K.
  const overlay = $('.search-overlay'), searchInput = $('#global-search'), searchResults = $('.search-results');
  let searchIndex = [], previouslyFocused = null;
  const createResult = (item) => {
    const a = document.createElement('a'); a.className='search-result'; a.href=item.href;
    if (item.external) {a.target='_blank';a.rel='noopener noreferrer';}
    const strong=document.createElement('strong'), hint=document.createElement('span');
    strong.textContent=item.title; hint.textContent=`${item.type} / ${item.hint}`;
    a.append(strong,hint); return a;
  };
  const renderSearch = () => {
    if (!searchResults || !searchInput) return;
    const query=safeText(searchInput.value);
    const matches=searchIndex.filter(x => safeText([x.title,x.type,x.hint].join(' ')).includes(query)).slice(0,9);
    searchResults.replaceChildren();
    matches.forEach(item=>searchResults.append(createResult(item)));
    if (!matches.length) {const p=document.createElement('p');p.textContent='No results. Try a different search term.';p.className='source-note';searchResults.append(p);}
  };
  const openSearch = async () => {
    if (!overlay) return;
    closeMenu(); previouslyFocused=document.activeElement;
    overlay.hidden=false;document.body.classList.add('no-scroll');searchInput?.focus();
    if (!searchIndex.length) {
      try {const response=await fetch('assets/search-index.json');if (!response.ok) throw Error('Search unavailable');searchIndex=await response.json();}
      catch {showToast('Search index could not be loaded. Please retry.');}
    }
    if (!overlay.hidden) renderSearch();
  };
  const closeSearch = () => {
    if (!overlay) return;overlay.hidden=true;document.body.classList.remove('no-scroll');
    if (previouslyFocused instanceof HTMLElement) previouslyFocused.focus();
  };
  $$('.search-open').forEach(b=>b.addEventListener('click',openSearch));
  $('.search-close')?.addEventListener('click',closeSearch);
  overlay?.addEventListener('click',e=>{if(e.target===overlay)closeSearch();});
  searchInput?.addEventListener('input',renderSearch);
  document.addEventListener('keydown',e => {
    if ((e.metaKey||e.ctrlKey) && e.key.toLowerCase()==='k') {e.preventDefault();overlay?.hidden ? openSearch() : closeSearch();}
    if (e.key==='Escape') {if (overlay && !overlay.hidden) closeSearch();else closeMenu();}
    if(e.key==='Tab' && overlay && !overlay.hidden) {
      const focusable=$$('button, input, a[href]',overlay).filter(x=>!x.hasAttribute('disabled'));
      if(!focusable.length)return;
      const first=focusable[0], last=focusable[focusable.length-1];
      if(e.shiftKey&&document.activeElement===first){e.preventDefault();last.focus();}
      else if(!e.shiftKey&&document.activeElement===last){e.preventDefault();first.focus();}
    }
  });

  // Hero: slideshow remains user-operable when automatic motion is disabled.
  const slides=$$('.hero-slide'); let activeSlide=0, autoTimer;
  function goToSlide(index) {
    if (!slides.length) return;
    activeSlide=(index+slides.length)%slides.length;
    slides.forEach((s,i)=>{const active=i===activeSlide;s.classList.toggle('active',active);s.setAttribute('aria-hidden',String(!active));s.querySelectorAll('a').forEach(a=>a.tabIndex=active?0:-1);});
    $$('.hero-dot').forEach((b,i)=>{b.classList.toggle('active',i===activeSlide);b.setAttribute('aria-selected',String(i===activeSlide));});
  }
  const resetTimer=()=>{window.clearInterval(autoTimer);if(slides.length&&!reducedMotion)autoTimer=window.setInterval(()=>goToSlide(activeSlide+1),8500);};
  if(slides.length){goToSlide(0);resetTimer();
    $$('.hero-dot').forEach(b=>b.addEventListener('click',()=>{goToSlide(Number(b.dataset.goto));resetTimer();}));
    $('.hero-prev')?.addEventListener('click',()=>{goToSlide(activeSlide-1);resetTimer();});
    $('.hero-next')?.addEventListener('click',()=>{goToSlide(activeSlide+1);resetTimer();});
    $('.hero')?.addEventListener('mouseenter',()=>window.clearInterval(autoTimer));
    $('.hero')?.addEventListener('mouseleave',resetTimer);
    document.addEventListener('visibilitychange',()=>{if(document.hidden)window.clearInterval(autoTimer);else resetTimer();});
  }

  // Collections: text query, universe filters and deterministic sorting.
  const collectionGrid=$('#collection-results');
  if(collectionGrid){
    const cards=$$('.product-card',collectionGrid), queryInput=$('#collection-search'), sort=$('#collection-sort'), count=$('#collection-count');
    let universe='All';
    const params=new URLSearchParams(location.search);
    if (['Anime','Comics'].includes(params.get('world'))) universe=params.get('world');
    const render=()=>{
      const query=safeText(queryInput?.value);
      const visible=cards.filter(c => (universe==='All'||c.dataset.universe===universe) && safeText(c.textContent+' '+c.dataset.category).includes(query));
      const sorted=[...cards];
      if(sort?.value==='az')sorted.sort((a,b)=>a.dataset.name.localeCompare(b.dataset.name));
      if(sort?.value==='za')sorted.sort((a,b)=>b.dataset.name.localeCompare(a.dataset.name));
      sorted.forEach(c=>{c.hidden=!visible.includes(c);collectionGrid.appendChild(c);});
      if(count)count.textContent=`SHOWING ${String(visible.length).padStart(2,'0')} / ${String(cards.length).padStart(2,'0')}`;
      const empty=$('#collection-empty');if(empty)empty.hidden=visible.length>0;
      $$('.filter').forEach(b=>{const selected=b.dataset.filter===universe;b.classList.toggle('active',selected);b.setAttribute('aria-pressed',String(selected));});
    };
    $$('.filter').forEach(b=>b.addEventListener('click',()=>{universe=b.dataset.filter;render();}));
    queryInput?.addEventListener('input',render);sort?.addEventListener('change',render);render();
  }

  // Directory: region and keyword filtering.
  const eventsResult=$('#events-results');
  if(eventsResult){
    const cards=$$('.event-card',eventsResult), eventSearch=$('#event-search');let region='All';
    const render=()=>{
      const query=safeText(eventSearch?.value);let visible=0;
      cards.forEach(card=>{const show=(region==='All'||card.dataset.region===region)&&safeText(card.dataset.keywords).includes(query);card.hidden=!show;if(show)visible++;});
      $('#event-count').textContent=`${String(visible).padStart(2,'0')} EVENT${visible===1?'':'S'}`;
      $('#events-empty').hidden=visible>0;
      $$('.event-filter').forEach(b=>{const a=b.dataset.region===region;b.classList.toggle('active',a);b.setAttribute('aria-pressed',String(a));});
    };
    $$('.event-filter').forEach(b=>b.addEventListener('click',()=>{region=b.dataset.region;render();}));
    eventSearch?.addEventListener('input',render);render();
  }

  const journalGrid=$('.journal-grid');
  if(journalGrid){let cat='All';
    const cards=$$('.journal-grid-card',journalGrid);
    const render=()=>{let visible=0;cards.forEach(c=>{const on=cat==='All'||c.dataset.category===cat;c.hidden=!on;if(on)visible++;});$('#journal-empty').hidden=visible>0;$$('.journal-filter').forEach(b=>{const active=b.dataset.cat===cat;b.classList.toggle('active',active);b.setAttribute('aria-pressed',String(active));});};
    $$('.journal-filter').forEach(b=>b.addEventListener('click',()=>{cat=b.dataset.cat;render();}));render();
  }

  // Gallery thumbnails and accessible enlargement.
  const mainImage=$('.detail-main-image'), thumbs=$$('.thumb'), lightbox=$('.lightbox');
  if(mainImage){
    const bigImage=$('img',lightbox);
    thumbs.forEach(b=>b.addEventListener('click',()=>{
      if(!b.dataset.image)return;mainImage.src=b.dataset.image;mainImage.alt=b.dataset.alt||'';
      if(bigImage){bigImage.src=mainImage.src;bigImage.alt=mainImage.alt;}
      thumbs.forEach(t=>{const a=t===b;t.classList.toggle('active',a);t.setAttribute('aria-pressed',String(a));});
    }));
    const closeLightbox=()=>{if(!lightbox)return;lightbox.hidden=true;document.body.classList.remove('no-scroll');$('.zoom-image')?.focus();};
    $('.zoom-image')?.addEventListener('click',()=>{if(!lightbox)return;bigImage.src=mainImage.src;bigImage.alt=mainImage.alt;lightbox.hidden=false;document.body.classList.add('no-scroll');$('.lightbox-close')?.focus();});
    $('.lightbox-close')?.addEventListener('click',closeLightbox);
    lightbox?.addEventListener('click',e=>{if(e.target===lightbox)closeLightbox();});
    document.addEventListener('keydown',e=>{if(e.key==='Escape'&&lightbox&&!lightbox.hidden)closeLightbox();});
  }

  // Contact deliberately uses a mailto workflow, rather than claiming to send an email server-side.
  const form=$('#contact-form');
  if(form){
    const initialSubject=new URLSearchParams(location.search).get('subject');
    if(initialSubject){const options=$$('#contact-topic option');const option=options.find(o=>o.value==='Visual concept inquiry');if(option)option.selected=true;$('#contact-message').value=`Hello FRAMEVERSE team,\n\n${initialSubject}\n\n`;}
    form.addEventListener('submit',e=>{
      e.preventDefault();if(!form.reportValidity())return;
      const data=new FormData(form);
      const subject=`FRAMEVERSE — ${data.get('topic')}`;
      const body=`Name: ${data.get('name')}\nEmail: ${data.get('email')}\nTopic: ${data.get('topic')}\n\n${data.get('message')}`;
      const mailto=`mailto:portfolio4684@gmail.com?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
      window.location.href=mailto;showToast('Your email application should now open. Review and send the message there.');
    });
  }

  // Subtle reveal motion. All content stays visible without JavaScript.
  if('IntersectionObserver' in window && !reducedMotion){
    const revealItems=$$('.reveal');
    const observer=new IntersectionObserver(entries=>{entries.forEach(e=>{if(e.isIntersecting){e.target.classList.remove('pending');observer.unobserve(e.target);}});},{threshold:0.09,rootMargin:'0px 0px -20px 0px'});
    revealItems.forEach(item=>{const box=item.getBoundingClientRect();if(box.top>window.innerHeight-40){item.classList.add('pending');observer.observe(item);}});
  }
})();
