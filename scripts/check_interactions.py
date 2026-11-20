"""Targeted browser interactions without network navigation (sandbox browser policy)."""
from playwright.sync_api import sync_playwright
from pathlib import Path
R=Path(__file__).resolve().parents[1]
issues=[]
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
 for mode,w,h in [('desktop',1440,900),('mobile',390,844)]:
  page=browser.new_page(viewport={'width':w,'height':h},reduced_motion='reduce')
  errors=[]
  page.on('pageerror',lambda e:errors.append(str(e)))
  def intercept(route):
   file=R/route.request.url.split('frameverse.test/')[-1].split('?')[0]
   if file.is_file():
    ctype={'css':'text/css','js':'application/javascript','json':'application/json','webp':'image/webp','svg':'image/svg+xml'}.get(file.suffix.lstrip('.'),'text/html')
    route.fulfill(status=200,body=file.read_bytes(),content_type=ctype,headers={'Access-Control-Allow-Origin':'*'})
   else:route.fulfill(status=404,body='Not found')
  page.route('https://frameverse.test/**',intercept)
  def load(name):
   page.set_content((R/name).read_text().replace('<head>','<head><base href="https://frameverse.test/">',1),wait_until='load',timeout=12000)
  load('index.html')
  if mode=="desktop": page.locator('[data-slide="2"]').click(force=True)
  else:
   page.locator('[data-dir="next"]').click()
   page.locator('[data-dir="next"]').click()
  v=page.locator('.hero-slide.is-active').get_attribute('data-index')
  if v!='2':issues.append(f'{mode}: hero slider did not change ({v})')
  page.locator('[data-agent-feature="2"]').click(force=True)
  page.wait_for_timeout(240)
  if 'PULCHRA' not in page.locator('#agent-feature-title').inner_text():issues.append(f'{mode}: agent switcher failed')
  page.locator('.search-open').click(force=True)
  page.locator('#global-search').fill('VIVIAN')
  page.wait_for_timeout(350)
  n=page.locator('.search-result').count()
  print(mode,'global search hits:',n)
  if n==0:issues.append(f'{mode}: search no results')
  page.keyboard.press('Escape')
  load('agents.html')
  page.locator('#agent-filter').fill('TRIGGER')
  n=page.locator('#agent-grid .agent-card:visible').count()
  print(mode,'agent search hits:',n)
  if n!=1:issues.append(f'{mode}: agent filter returned {n}')
  load('scenes.html')
  page.locator('[data-target="scenes"][data-filter="AFTER DARK"]').click(force=True)
  n=page.locator('#scene-grid .scene-card:visible').count()
  print(mode,'scene filter hits:',n)
  if not 0<n<24:issues.append(f'{mode}: scene filter returned {n}')
  load('bangboo.html')
  page.locator('[data-target="bangboos"][data-filter="S"]').click(force=True)
  n=page.locator('#bangboo-grid .bang-card:visible').count()
  print(mode,'S rank bangboo count:',n)
  if not 0<n<22:issues.append(f'{mode}: bangboo filter returned {n}')
  load('wallpapers.html')
  page.locator('.wallpaper-art').first.click(force=True)
  if not page.locator('#lightbox').evaluate('(x)=>x.classList.contains("open")'):issues.append(f'{mode}: lightbox does not open')
  page.keyboard.press('ArrowRight');page.keyboard.press('Escape')
  if page.locator('#lightbox').evaluate('(x)=>x.classList.contains("open")'):issues.append(f'{mode}: lightbox did not close')
  load('agent-agent-01.html')
  overflow=page.evaluate('document.documentElement.scrollWidth - window.innerWidth')
  if overflow>1:issues.append(f'{mode}: agent detail horizontal overflow: {overflow}')
  if mode=='mobile':
   load('index.html');page.locator('.mobile-toggle').click()
   if page.locator('.mobile-nav').get_attribute('class').find('open')==-1:issues.append('mobile nav did not open')
   page.locator('.mobile-toggle').click()
  if errors:issues.append(f'{mode}: JS exceptions {errors[:3]}')
  page.close()
 browser.close()
print('ISSUES:',issues)
if issues:raise SystemExit(1)
