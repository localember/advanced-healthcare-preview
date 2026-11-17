import re, shutil, pathlib, os
SRC=pathlib.Path('site'); OUT=pathlib.Path('out')
if OUT.exists(): shutil.rmtree(OUT)
OUT.mkdir()
SHIP=['', 'special', 'privacy-policy','terms-service','hipaa-privacy-policy','healthcare-disclaimer','good-faith-estimate','accessibility','anti-discrimination']
LE='/workspace/le'
DS=pathlib.Path(LE)/'design-system/harbor'
for f in ['harbor.css','harbor-fonts.css','harbor.js','rough-notation.js']: shutil.copy(DS/f, OUT/f)
shutil.copytree(DS/'assets/fonts', OUT/'assets/fonts')
img=OUT/'assets/images'; img.mkdir(parents=True)
FLOOR=pathlib.Path(LE)/'tools/bd-generator/clients/palmetto-static-src/assets/images'
MINE=pathlib.Path('/workspace/irwin/mockup-2026-10-30/img')
BANNER_CSS='''<style>
.le-preview-banner{position:sticky;top:0;z-index:9999;background:#f2a63b;color:#022038;font:600 14px/1.4 Poppins,sans-serif;text-align:center;padding:8px 12px}
:root{--har-ink:#022038;--har-comp-1:#022038}
.har-blog{padding:72px 20px;background:#fff}
.har-blog__inner{max-width:1200px;margin:0 auto}
.har-blog__h{font-family:var(--har-font-head);font-size:var(--har-h2);line-height:var(--har-lh-head);color:#022038;text-align:center;margin:0 0 8px}
.har-blog__sub{text-align:center;margin:0 auto 36px;max-width:640px}
.har-blog__grid{display:grid;grid-template-columns:repeat(3,1fr);gap:24px}
.har-blog__card{display:flex;flex-direction:column;background:#fff;box-shadow:var(--har-card-shadow);text-decoration:none;color:var(--har-body)}
.har-blog__card img{width:100%;aspect-ratio:3/1;object-fit:cover;display:block}
.har-blog__body{padding:18px 20px 22px}
.har-blog__title{font-weight:700;font-size:18px;line-height:1.35;color:#022038;margin:0 0 8px}
.har-blog__ex{margin:0 0 12px;font-size:15px;line-height:1.7}
.har-blog__more{font-weight:700;font-size:14px;color:var(--har-cta)}
.har-blog__all{text-align:center;margin-top:32px}
@media (max-width:900px){.har-blog__grid{grid-template-columns:1fr}}
.le-preview-off{cursor:not-allowed}
</style>'''
BANNER='<div class="le-preview-banner" role="note">Design preview, not live. Forms are inactive.</div>'
POSTS=[
 ('3 Tips from a Fort Collins CO Chiropractor','Are you tired of dealing with persistent back pain, neck stiffness, or shoulder discomfort?','https://www.myadvhc.com/3-tips-from-a-fort-collins-co-chiropractor/','3-Tips.webp'),
 ('Fort Collins CO Chiropractor Talks about Bulging Discs','Are you tired of being sidelined by back pain?','https://www.myadvhc.com/fort-collins-co-chiropractor-talks-about-bulging-discs/','Bulging-disc.webp'),
 ('Fort Collins CO Chiropractor Discusses Different Types of Headaches','Are headaches turning your days into a constant battle between you and pain?','https://www.myadvhc.com/fort-collins-co-chiropractor-discusses-different-types-of-headaches/','Different-Headache-types.webp'),
]
def blog_band():
    cards=''.join(f'''
      <a class="har-blog__card" href="{u}" target="_blank" rel="noopener">
        <img src="assets/images/{im}" alt="" loading="lazy">
        <div class="har-blog__body"><p class="har-blog__title">{t}</p><p class="har-blog__ex">{x}</p><span class="har-blog__more">Read on the current site</span></div>
      </a>''' for t,x,u,im in POSTS)
    return f'''<section class="har-blog" data-sd="blog.band" aria-labelledby="blog-h">
  <div class="har-blog__inner">
    <h2 class="har-blog__h" id="blog-h">From the Blog</h2>
    <p class="har-blog__sub">Tips and articles from Advanced Healthcare in Fort Collins.</p>
    <div class="har-blog__grid">{cards}
    </div>
  </div>
</section>
'''
used=set()
for slug in SHIP:
    sp=SRC/slug/'index.html'; s=sp.read_text()
    depth=0 if slug=='' else 1
    pre='' if depth==0 else '../'
    if depth:
        s=s.replace('src="assets/', 'src="../assets/').replace('url(assets/','url(../assets/')
    def fix(m):
        path=m.group(1)
        seg=path.strip('/').split('/')[0] if path.strip('/') else ''
        if seg in SHIP:
            return f'href="{pre}{seg+"/" if seg else ""}"' if (pre or seg) else 'href="./"'
        return 'href="#" class="le-preview-off" title="This page comes in the full build" aria-disabled="true"'
    s=re.sub(r'href="(/[^"]*)"', fix, s)
    # merge duplicate class attrs created on <a class=... href=# class=...>
    s=re.sub(r'(<a\b[^>]*?)class="([^"]*)"([^>]*?) href="#" class="le-preview-off"', r'\1class="\2 le-preview-off"\3 href="#"', s)
    if '<meta name="robots"' in s:
        s=re.sub(r'<meta name="robots"[^>]*>','<meta name="robots" content="noindex,nofollow">',s)
    else:
        s=s.replace('<head>','<head>\n<meta name="robots" content="noindex,nofollow">',1)
    s=s.replace('</head>', BANNER_CSS+'\n</head>',1)
    s=re.sub(r'(<body[^>]*>)', r'\1'+BANNER, s, count=1)
    # inactive forms
    s=re.sub(r'<form([^>]*?) action="[^"]*"', r'<form\1 action="#" onsubmit="return false;" data-preview="inactive"', s)
    s=s.replace('<button class="har-btn har-btn--submit" type="submit">Submit</button>','<button class="har-btn har-btn--submit" type="button" disabled aria-disabled="true">Submit (inactive in preview)</button>')
    if slug=='':
        i=s.find('<section class="har-facts')
        s=s[:i]+blog_band()+s[i:]
    s=s.replace('\u2014',', ')
    d=OUT/slug; d.mkdir(parents=True,exist_ok=True); (d/'index.html').write_text(s)
    used|=set(re.findall(r'assets/images/([^"\')\s]+)', s))
for u in sorted(used):
    for base in (MINE,FLOOR):
        if (base/u).exists(): shutil.copy(base/u, img/u); break
    else: print('MISSING image', u)
shutil.copy(MINE/'Advanced-Healthcare-Logo-250x84-1.webp', img/'favicon.webp')
(OUT/'robots.txt').write_text('User-agent: *\nDisallow: /\n')
(OUT/'.nojekyll').write_text('')
(OUT/'README.md').write_text('# Advanced Healthcare design preview\n\nDesign preview only, not the live site. Homepage on the Local Ember Harbor template, with Local Ember standard legal pages. noindex, robots Disallow, inactive forms.\n')
print('images', len(used))
