import re, shutil, pathlib, os
SRC=pathlib.Path('site'); OUT=pathlib.Path('out')
if OUT.exists(): shutil.rmtree(OUT)
OUT.mkdir()
SHIP=['', 'special', 'privacy-policy','terms-service','hipaa-privacy-policy','healthcare-disclaimer','good-faith-estimate','accessibility','anti-discrimination',
 # round 5: inner pages (Harbor emitter archetypes + catalog pages this record publishes) and a blog index
 'who-we-are','services','conditions','patient-stories','contact-us','blog',
 'chiropractic','softwave','shockwave','decompression','neuropathy','massage-therapy','physical-rehabilitation','wellness-care',
 'back-pain','neck-pain','headaches','sciatica','disc-injury']
LE=os.environ.get('LE','/workspace/le')
DS=pathlib.Path(LE)/'design-system/harbor'
for f in ['harbor.css','harbor-fonts.css','harbor.js','rough-notation.js']: shutil.copy(DS/f, OUT/f)
shutil.copytree(DS/'assets/fonts', OUT/'assets/fonts')
img=OUT/'assets/images'; img.mkdir(parents=True)
FLOOR=pathlib.Path(LE)/'tools/bd-generator/clients/palmetto-static-src/assets/images'
MINE=pathlib.Path(os.environ.get('AHC_MINE','/workspace/irwin/mockup-2026-10-30/img'))
STOCK=pathlib.Path(LE)/'tools/bd-generator/assets/stock/Catalog'
import round5
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
GOLD_CSS='''<style id="le-cta-gold">
/* Advanced Healthcare: main CTAs in logo goldenrod #E0A424 with navy #022038 text (7.51:1). Hover #C8901A (5.89:1). Navy stays on headers, nav and secondary links. */
:root{--le-cta-gold:#E0A424;--le-cta-gold-hover:#C8901A;--le-cta-gold-text:#022038}
.har-btn--book,.har-btn--submit,.har-btn--solid,.har-icons a[data-sd="icons.ctabtn"]{background-color:var(--le-cta-gold)!important;color:var(--le-cta-gold-text)!important;border-color:var(--le-cta-gold)!important;font-weight:700}
.har-btn--book:hover,.har-btn--book:focus-visible,.har-btn--submit:hover,.har-btn--submit:focus-visible,.har-btn--solid:hover,.har-btn--solid:focus-visible,.har-icons a[data-sd="icons.ctabtn"]:hover,.har-icons a[data-sd="icons.ctabtn"]:focus-visible{background-color:var(--le-cta-gold-hover)!important;border-color:var(--le-cta-gold-hover)!important;color:var(--le-cta-gold-text)!important}
.har-btn--book.har-welcome__link{background-color:var(--har-cta)!important;border-color:var(--har-cta)!important;color:#fff!important;font-weight:500}
.har-btn--book.har-welcome__link:hover{background-color:var(--har-cta)!important;color:#fff!important}
.har-btn--submit[disabled]{opacity:.85;cursor:not-allowed}
</style>
'''
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
def blog_page():
    t=(SRC/'special'/'index.html').read_text()
    a=t.index('<main id="main">'); b=t.index('</main>')
    body=('<main id="main">\n<section class="har-pagehero" style="--har-pagehero-bg:url(assets/images/Chiropractic-Fort-Collins-CO-Information-Center.webp)">\n'
          '  <div class="har-pagehero__inner">\n    <h1 class="har-pagehero__title">Blog</h1>\n  </div>\n</section>\n'
          + blog_band().replace('<h2 class="har-blog__h" id="blog-h">From the Blog</h2>','<h2 class="har-blog__h" id="blog-h">Articles from Advanced Healthcare</h2>')
          + '<p class="har-blog__all" style="padding:0 20px 64px">The full articles live on the current site for now. They move here in the full build.</p>\n')
    t=t[:a]+body+t[b:]
    t=re.sub(r'<title>[^<]*</title>','<title>Blog - Advanced Healthcare, Chiropractor in Fort Collins, CO</title>',t,count=1)
    t=t.replace('href="/blog/"','href="/blog/" aria-current="page"',1)
    (SRC/'blog').mkdir(exist_ok=True); (SRC/'blog'/'index.html').write_text(t)
blog_page()
used=set()
for slug in SHIP:
    sp=SRC/slug/'index.html'; s=sp.read_text()
    depth=0 if slug=='' else 1
    pre='' if depth==0 else '../'
    if depth:
        s=s.replace('src="assets/', 'src="../assets/').replace('url(assets/','url(../assets/')
    if slug=='':
        import hero_video; s=hero_video.apply(s)
        import svc_images; s=svc_images.apply(s)
        s=round5.apply_home(s)
        i=s.find('<section class="har-facts')
        s=s[:i]+blog_band()+s[i:]
    s=round5.apply_all(s)
    s=round5.localize(slug, s)
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
    s=s.replace('</head>', BANNER_CSS+'\n'+GOLD_CSS+'</head>',1)
    s=re.sub(r'(<body[^>]*>)', r'\1'+BANNER, s, count=1)
    # inactive forms
    s=re.sub(r'<form([^>]*?) action="[^"]*"', r'<form\1 action="#" onsubmit="return false;" data-preview="inactive"', s)
    s=re.sub(r'<button class="har-btn har-btn--submit"([^>]*?) type="submit"([^>]*)>[^<]*</button>', r'<button class="har-btn har-btn--submit"\1 type="button" disabled aria-disabled="true"\2>Submit (inactive in preview)</button>', s)
    s=s.replace('\u2014',', ')
    d=OUT/slug; d.mkdir(parents=True,exist_ok=True); (d/'index.html').write_text(s)
    used|=set(re.findall(r'assets/images/([^"\')\s]+)', s))
for u in sorted(used):
    for base in (pathlib.Path(os.environ.get('AHC_REPO','.'))/'assets/images',MINE,FLOOR,STOCK/'Services',STOCK/'Conditions',pathlib.Path(os.environ.get('AHC_REPO','.'))/'assets/images'):
        if (base/u).exists(): shutil.copy(base/u, img/u); break
    else:
        for base in (STOCK/'Services',STOCK/'Conditions'):
            if (base/u.replace('-',' ')).exists(): shutil.copy(base/u.replace('-',' '), img/u); break
        else: print('MISSING image', u)
shutil.copy(MINE/'Advanced-Healthcare-Logo-250x84-1.webp', img/'favicon.webp')
if (pathlib.Path(os.environ.get('AHC_REPO','.'))/'assets/video').exists(): shutil.copytree(pathlib.Path(os.environ.get('AHC_REPO','.'))/'assets/video', OUT/'assets/video')
(OUT/'robots.txt').write_text('User-agent: *\nDisallow: /\n')
(OUT/'.nojekyll').write_text('')
(OUT/'README.md').write_text((pathlib.Path(__file__).parent/'README.template.md').read_text())
print('images', len(used))
