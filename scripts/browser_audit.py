"""Optional comprehensive browser smoke audit (requires Python Playwright + Chromium).
Uses a sandbox-safe resource interceptor; no server or external website is required.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright
from shutil import which
R=Path(__file__).resolve().parents[1]
PAGES=sorted([p.name for p in R.glob('*.html')])
issues=[];cases=0
with sync_playwright() as p:
 kwargs={'headless':True,'args':['--no-sandbox']}
 if which('chromium'):kwargs['executable_path']=which('chromium')
 browser=p.chromium.launch(**kwargs)
 for width in [320,390,768,1440]:
  page=browser.new_page(viewport={'width':width,'height':850},reduced_motion='reduce')
  errors=[]
  page.on('pageerror',lambda e:errors.append(str(e)))
  def fulfill(route):
   f=R/route.request.url.split('frameverse.test/')[-1].split('?')[0]
   if f.is_file():
    mt={'css':'text/css','js':'application/javascript','json':'application/json','webp':'image/webp','svg':'image/svg+xml'}.get(f.suffix.lstrip('.'),'text/html')
    route.fulfill(status=200,body=f.read_bytes(),content_type=mt,headers={'Access-Control-Allow-Origin':'*'})
   else:route.fulfill(status=404,body='missing')
  page.route('https://frameverse.test/**',fulfill)
  for doc in PAGES:
   html=(R/doc).read_text(encoding='utf-8').replace('<head>','<head><base href="https://frameverse.test/">',1)
   page.set_content(html,wait_until='load',timeout=12000)
   w=page.evaluate('document.documentElement.scrollWidth - window.innerWidth')
   h=page.locator('h1').count()
   if w>1:issues.append(f'{width}px {doc}: overflow {w}px')
   if h!=1:issues.append(f'{width}px {doc}: {h} h1 headings')
   cases+=1
  if errors:issues.append(f'{width}px: JavaScript exceptions: {errors[:3]}')
  page.close()
 browser.close()
print(f'Checked {cases} viewport × page combinations.')
if issues:
 for item in issues:print('ISSUE:',item)
 raise SystemExit(1)
print('PASS: no overflow, missing h1, or JavaScript exceptions.')
