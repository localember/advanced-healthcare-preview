"""Round 5 (John, 2026-11-17, via Local Ember Advisor). Applied by post.py.

apply_all(html, pre)   every page: real social icons (Facebook, X, YouTube) in the header VISIT US slot
                       and the footer, from record.brand.socials; 44px tap targets, visible on navy.
apply_home(html)       homepage only:
  4. New Patient Special card: goldenrod #E0A424, navy #022038 text, navy CLICK HERE with white text.
  5. Reviews band: room below the testimonial panel before the next band.
  6. Expertise band rewritten chiropractic-first ("Chiropractic Care in Fort Collins"), adjustment-room
     photo leading, SoftWave and Shockwave kept as secondary rows with their round 4 photos.
  7. Welcome band: YouTube video F9y4ARql1_g as a click-to-load youtube-nocookie embed (poster
     assets/images/irwin-video-poster.webp, from i.ytimg.com maxresdefault); Dr. Irwin's photo moves to
     the OUR SERVICES (conditions) band intro.
  (3. hero overlay lives in hero_video.py.)
LOCALIZE: light per-page wording for this practice on shared catalog pages (one chiropractor)."""
import json, pathlib, re, html as H
REC = json.loads((pathlib.Path(__file__).parent / 'advanced-healthcare.record.json').read_text())
SOC = REC['brand']['socials']

SVG = {
 'facebook': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M22 12.07C22 6.5 17.52 2 12 2S2 6.5 2 12.07c0 5.02 3.66 9.18 8.44 9.93v-7.03H7.9v-2.9h2.54V9.41c0-2.5 1.49-3.89 3.77-3.89 1.09 0 2.24.2 2.24.2v2.46h-1.26c-1.24 0-1.63.77-1.63 1.56v1.88h2.78l-.44 2.9h-2.34V22c4.78-.75 8.44-4.91 8.44-9.93z"/></svg>',
 'twitter': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>',
 'youtube': '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M23.5 6.2a3 3 0 0 0-2.1-2.1C19.5 3.6 12 3.6 12 3.6s-7.5 0-9.4.5A3 3 0 0 0 .5 6.2 31 31 0 0 0 0 12a31 31 0 0 0 .5 5.8 3 3 0 0 0 2.1 2.1c1.9.5 9.4.5 9.4.5s7.5 0 9.4-.5a3 3 0 0 0 2.1-2.1A31 31 0 0 0 24 12a31 31 0 0 0-.5-5.8zM9.6 15.6V8.4l6.3 3.6-6.3 3.6z"/></svg>',
}
LABEL = {'facebook': 'Facebook', 'twitter': 'X (Twitter)', 'youtube': 'YouTube'}

def _icons(cls):
    out = []
    for k in ('facebook', 'twitter', 'youtube'):
        u = SOC.get(k)
        if not u: continue
        c = f' class="{cls}"' if cls else ''
        out.append(f'<a{c} data-social="{k}" href="{H.escape(u)}" target="_blank" rel="noopener" aria-label="Advanced Healthcare on {LABEL[k]} (opens in a new tab)">{SVG[k]}</a>')
    return '\n          '.join(out)

SOC_CSS = '''<style id="le-social">
/* Round 5: social icons, 44px tap targets. Header: navy icons on the white top line. Footer: gold circles with navy icons on the navy colophon. */
.har-social{align-items:center;gap:2px;flex-wrap:nowrap}
.har-topline__right{flex-shrink:0}
.har-topline__right{align-items:center}
.har-social .har-social__icon{width:44px;height:44px;align-items:center;justify-content:center;margin:-10px 0}
.har-social .har-social__icon svg{width:20px;height:20px;fill:#022038}
.har-social .har-social__icon:hover svg,.har-social .har-social__icon:focus-visible svg{fill:#C8901A}
.har-colophon__social{margin-top:18px;gap:12px;flex-wrap:wrap}
.har-colophon__social a{width:44px;height:44px;padding:0;background:#E0A424}
.har-colophon__social a svg{width:20px;height:20px;fill:#022038}
.har-colophon__social a:hover,.har-colophon__social a:focus-visible{background:#fff}
.har-colophon__social a:hover svg,.har-colophon__social a:focus-visible svg{fill:#022038}
/* Harbor bug: its <1024px rule stacks .har-sshero__inner, but the two-column flex is .har-sshero__row, so service and condition heroes stayed side by side at 390px. */
@media (max-width:1023px){.har-sshero__row{flex-direction:column;align-items:stretch;gap:28px}}
.le-stat{display:block;font-family:var(--har-font-head);font-size:26px;line-height:1.25;color:#022038;margin:0 0 8px}
</style>'''

def apply_all(s):
    s = re.sub(r'(<div class="har-social" data-sd="header.social">)[\s\S]*?(</div>)',
               lambda m: m.group(1) + '\n          ' + _icons('har-social__icon') + '\n          ' + m.group(2), s, count=1)
    s = re.sub(r'(<div class="har-colophon__social">)[\s\S]*?(</div>)',
               lambda m: m.group(1) + '\n          ' + _icons('') + '\n        ' + m.group(2), s, count=1)
    s = re.sub(r'<p>([^<\u2063]*)\u2063', r'<p><strong class="le-stat">\1</strong>', s)
    if 'id="le-social"' not in s:
        s = s.replace('</head>', SOC_CSS + '\n</head>', 1)
    return s

HOME_CSS = '''<style id="le-round5">
/* 4. New Patient Special card in logo goldenrod, navy text, navy button */
.har-icons .har-card--cta{background:#E0A424}
.har-icons .har-card--cta .har-card__title{color:#022038}
.har-icons .har-card--cta .har-card__icon svg{fill:#022038}
.har-icons .har-card--cta a[data-sd="icons.ctabtn"]{background-color:#022038!important;border-color:#022038!important;color:#fff!important;font-weight:700}
.har-icons .har-card--cta a[data-sd="icons.ctabtn"]:hover,.har-icons .har-card--cta a[data-sd="icons.ctabtn"]:focus-visible{background-color:#fff!important;border-color:#022038!important;color:#022038!important}
.har-icons .har-card--cta a[data-sd="icons.ctabtn"]:focus-visible{outline:3px solid #022038;outline-offset:3px}
/* 5. room below the testimonial panel */
.har-reviews__inner{padding-top:56px;padding-bottom:96px}
.har-reviews__dots{margin-top:24px}
@media (max-width:767px){.har-reviews__inner{padding-top:40px;padding-bottom:64px}.har-reviews__panel{padding-left:20px;padding-right:20px}}
/* 6. chiropractic-first expertise band */
.har-expertise__lead{align-self:flex-start}
@media (min-width:1120px){.har-expertise__lead{position:sticky;top:64px}}
.har-expertise__h{text-transform:none}
.har-expertise__photo[src*="Adjustment-Room"]{width:100%;max-width:300px;height:auto;aspect-ratio:263/400;object-fit:cover}
@media (max-width:767px){.har-expertise__photo[src*="Adjustment-Room"]{max-width:260px;margin-inline:auto}}
.le-exp-intro{margin:20px 0 0;font-size:var(--har-base);line-height:var(--har-lh-body);color:var(--har-body)}
.har-expertise__row a{color:#022038;font-weight:700;text-decoration:underline;text-underline-offset:3px}
.har-expertise__row a:hover{color:#C8901A}
.le-exp-more{margin-top:24px;display:inline-block}
.le-exp-secondary{font-size:12px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:#5a6b7b;margin:0 0 4px}
/* 7. click-to-load YouTube */
.le-yt{position:relative;width:100%;aspect-ratio:16/9;border-radius:var(--har-r-img);overflow:hidden;background:#000;box-shadow:5px 20px 20px 0 #00000040}
.le-yt__btn{position:absolute;inset:0;width:100%;height:100%;padding:0;border:0;cursor:pointer;background:#000}
.le-yt__btn img{width:100%;height:100%;object-fit:cover;display:block}
.le-yt__play{position:absolute;left:50%;top:50%;width:76px;height:76px;margin:-38px 0 0 -38px;border-radius:50%;background:#E0A424;display:flex;align-items:center;justify-content:center;box-shadow:0 6px 18px rgba(0,0,0,.35);transition:transform .2s,background .2s}
.le-yt__play svg{width:30px;height:30px;fill:#022038;margin-left:5px}
.le-yt__btn:hover .le-yt__play,.le-yt__btn:focus-visible .le-yt__play{transform:scale(1.08);background:#C8901A}
.le-yt__btn:focus-visible{outline:3px solid #E0A424;outline-offset:3px}
.le-yt iframe{position:absolute;inset:0;width:100%;height:100%;border:0}
.le-yt__cap{margin:10px 0 0;font-size:14px;color:var(--har-body);text-align:center}
.har-welcome__media{justify-content:center}
.har-conditions__photo img[src*="Nate-Irwin"]{object-fit:cover;object-position:50% 28%;max-width:523px}
@media (max-width:767px){.le-yt__play{width:64px;height:64px;margin:-32px 0 0 -32px}}
</style>'''

YT_ID = 'F9y4ARql1_g'
YT_TITLE = 'Chiropractic Care at Advanced Healthcare in Fort Collins, CO with Dr. Nathan Irwin'
YT = f'''<div class="har-welcome__media">
        <div class="le-yt" data-yt="{YT_ID}">
          <button class="le-yt__btn" type="button" aria-label="Play video: {YT_TITLE}">
            <img src="assets/images/irwin-video-poster.webp" alt="" width="1280" height="720" loading="lazy">
            <span class="le-yt__play" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg></span>
          </button>
        </div>
        <p class="le-yt__cap">Watch: Chiropractic care at Advanced Healthcare with Dr. Nathan Irwin</p>
      </div>'''
YT_JS = f'''<script id="le-yt-js">
document.querySelectorAll('.le-yt').forEach(function(w){{var b=w.querySelector('.le-yt__btn');if(!b)return;
b.addEventListener('click',function(){{var f=document.createElement('iframe');
f.src='https://www.youtube-nocookie.com/embed/'+w.getAttribute('data-yt')+'?autoplay=1&rel=0';
f.title={json.dumps(YT_TITLE)};f.allow='accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share';
f.allowFullscreen=true;f.referrerPolicy='strict-origin-when-cross-origin';w.replaceChild(f,b);f.focus();}});}});
</script>'''

def row(n, h, body, extra=''):
    return f'''      <li class="har-expertise__row">
        <span class="har-expertise__num" aria-hidden="true">{n}</span>
        <div>{extra}<h3 class="har-expertise__rowh">{h}</h3><p>{body}</p></div>
      </li>'''

def expertise():
    rows = [
        row(1, 'Chiropractic Adjustments', 'Specific adjustments matched to what your spine needs, not a one-size-fits-all routine. Gentle adjustments restore proper alignment, ease pain and support your body&#x27;s natural healing, with simple movement guidance so the relief holds between visits. <a href="/chiropractic/">Chiropractic care in Fort Collins</a>'),
        row(2, 'Conditions We Treat', 'Care for <a href="/back-pain/">back pain</a>, <a href="/neck-pain/">neck pain</a>, <a href="/headaches/">headaches and migraines</a>, <a href="/sciatica/">sciatica</a> and <a href="/disc-injury/">disc injuries</a>, plus <a href="/wellness-care/">wellness care</a> for people who would rather keep moving well. We focus on the root cause of your discomfort, not just the symptoms.'),
        row(3, 'A Whole-Body, Family-Oriented Approach', 'Dr. Irwin founded his practice in 2005 with a whole-body approach and a family-oriented mindset. Every visit starts with listening, then a care plan built around you, pairing adjustments with stretches, strengthening, <a href="/massage-therapy/">massage</a> and <a href="/physical-rehabilitation/">rehab</a>. <a href="/who-we-are/">Meet Dr. Irwin</a>'),
        row(4, 'Spinal Decompression and Neuropathy Care', 'Gentle motorised traction for the low back, easing pressure on an irritated disc or nerve, and care for the mechanical and spinal side of neuropathy, alongside the medical care you already have. <a href="/decompression/">Spinal decompression</a> · <a href="/neuropathy/">Neuropathy care</a>'),
        row(5, 'SoftWave', 'Unfocused acoustic-wave sessions for minor muscle aches, alongside chiropractic care. <a href="/softwave/">About SoftWave</a><img class="le-svc-thumb" src="assets/images/softwave-unit.webp" alt="A SoftWave therapy unit with its touchscreen controls" width="1046" height="714" loading="lazy">', '<p class="le-exp-secondary">Also at Advanced Healthcare</p>'),
        row(6, 'Shockwave Therapy', 'Shockwave therapy for long-running tendon and heel problems that have stopped easing. <a href="/shockwave/">About Shockwave Therapy</a><img class="le-svc-thumb le-svc-thumb--shock" src="assets/images/shockwave-handpiece.webp" alt="A shockwave therapy handpiece being applied to a patient&#x27;s arm" width="528" height="607" loading="lazy">'),
    ]
    # thumbs sit after the paragraph, matching round 4
    rows = [r.replace('<img class="le-svc-thumb', '</p><img class="le-svc-thumb').replace('loading="lazy"></p>', 'loading="lazy">') for r in rows]
    return '''<section class="har-expertise" data-sd="expertise.band">
  <div class="har-expertise__inner" data-sd="expertise.inner">
    <div class="har-expertise__lead">
      <p class="har-eyebrow">OUR <span class="har-annotate"><span class="har-annotate__word">EXPERTISE</span></span></p>
      <h2 class="har-expertise__h" data-sd="expertise.h">Chiropractic Care in Fort Collins</h2>
      <p class="le-exp-intro">Advanced Healthcare is a chiropractic office on S Shields St in Fort Collins, led by Dr. Nathan Irwin, a graduate of Palmer College of Chiropractic who has cared for Fort Collins patients since 2005. Our approach involves thorough listening to understand your specific needs, followed by the development of a tailored care plan to achieve your wellness objectives.</p>
      <img class="har-expertise__photo" data-sd="expertise.photo" data-enter="left"
           src="assets/images/Chiropractic-Fort-Collins-CO-Chiropractic-Adjustment-Room.webp" alt="A chiropractic adjustment room at Advanced Healthcare in Fort Collins" width="263" height="400" loading="lazy">
      <a class="har-btn har-btn--book le-exp-more" href="/services/">Explore Our Services</a>
    </div>
    <ol class="har-expertise__rows" data-sd="expertise.body">
''' + '\n'.join(rows) + '''
    </ol>
  </div>
</section>'''

def apply_home(s):
    if 'id="le-round5"' in s: return s
    # 6
    a = s.index('<section class="har-expertise"'); b = s.index('</section>', a) + len('</section>')
    s = s[:a] + expertise() + s[b:]
    # 7
    old_media = re.search(r'<div class="har-welcome__media">\s*<img class="har-welcome__photo"[^>]*>\s*</div>', s)
    assert old_media, 'welcome media'
    s = s[:old_media.start()] + YT + s[old_media.end():]
    old_ph = '<img data-sd="conditions.photo" data-enter="left" src="assets/images/Chiropractic-Fort-Collins-CO-Information-Center.webp" alt="Fort Collins chiropractic office">'
    assert old_ph in s, 'conditions photo'
    s = s.replace(old_ph, '<img data-sd="conditions.photo" data-enter="left" src="assets/images/Chiropractor-Nate-Irwin.webp" alt="Dr. Nathan Irwin, chiropractor at Advanced Healthcare in Fort Collins" width="570" height="570" loading="lazy">', 1)
    s = s.replace('</head>', HOME_CSS + '\n</head>', 1)
    s = s.replace('</body>', YT_JS + '\n</body>', 1)
    return s

# Light localisation of shared catalog wording for a one-chiropractor office that offers massage.
LOCALIZE = {
    'massage-therapy': [
        ('the same office as the chiropractors', 'the same office as Dr. Irwin'),
        ('the same office as the chiropractor', 'the same office as Dr. Irwin'),
    ],
    'physical-rehabilitation': [
        ('Soft-tissue work, when this office offers it and it belongs in the plan, can settle a muscle that will not let the joint move.', 'Massage, which this office offers, can settle a muscle that will not let the joint move when it belongs in the plan.'),
    ],
}
def localize(slug, s):
    for a, b in LOCALIZE.get(slug, []):
        s = s.replace(a, b)
    return s

def _dedupe_stories(s):
    """Harbor's stories grid pads to 8 cards by repeating reviews; this practice has 5 real ones, shown once each."""
    seen = set()
    def keep(m):
        name = re.search(r'har-story__name">([^<]*)<', m.group(0))
        k = name.group(1) if name else m.group(0)
        if k in seen: return ''
        seen.add(k); return m.group(0)
    return re.sub(r'\s*<article class="har-story"[\s\S]*?</article>', keep, s)

_localize_text = localize
def localize(slug, s):
    s = _localize_text(slug, s)
    if slug == 'patient-stories':
        s = _dedupe_stories(s)
    return s
