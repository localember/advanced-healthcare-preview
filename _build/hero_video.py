"""Hero video for the Advanced Healthcare Harbor preview (round 3).
Silent b-roll loop cut from John's Drive mp4 (source 00:31.0 to 00:43.6, 12.6 s, 1280x720, h264, no audio, 1.8 MB).
Under 700px wide or with prefers-reduced-motion the video is never requested: poster only.
Call apply(html) on the homepage HTML. Idempotent."""
CSS = '''<style id="le-hero-video">
.har-hero__bg{display:none!important}
.le-hero-poster,.le-hero-video{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;z-index:-1}
.le-hero-poster{background:#022038 url(assets/images/hero-poster.jpg) center/cover no-repeat}
.le-hero-video{opacity:0;transition:opacity .6s ease}
.le-hero-video.is-playing{opacity:1}
/* Round 5: black gradient (was navy), lighter, left-weighted so the headline side stays readable */
.har-hero__slide{background-image:linear-gradient(90deg,rgba(0,0,0,.62) 0%,rgba(0,0,0,.46) 45%,rgba(0,0,0,.28) 100%)!important}
.har-hero__copy{text-shadow:0 1px 3px rgba(0,0,0,.45)}
@media (max-width:699px){.har-hero__actions .har-btn{max-width:100%;white-space:normal;text-align:center}.le-hero-video{display:none}.har-hero__slide{background-image:linear-gradient(rgba(0,0,0,.58),rgba(0,0,0,.58))!important}}
@media (prefers-reduced-motion:reduce){.le-hero-video{display:none}}
</style>'''
MARKUP = '''    <div class="le-hero-poster" aria-hidden="true"></div>
    <video class="le-hero-video" data-src="assets/video/hero-loop.mp4" poster="assets/images/hero-poster.jpg" muted loop playsinline preload="none" aria-hidden="true" tabindex="-1"></video>
'''
JS = '''<script id="le-hero-video-js">
(function(){var v=document.querySelector('.le-hero-video');if(!v)return;
var small=window.matchMedia('(max-width:699px)').matches,reduce=window.matchMedia('(prefers-reduced-motion:reduce)').matches;
if(small||reduce)return;
v.muted=true;v.src=v.getAttribute('data-src');
v.addEventListener('playing',function(){v.classList.add('is-playing')});
var p=v.play();if(p&&p.catch)p.catch(function(){});})();
</script>'''
def apply(s):
    if 'le-hero-video' in s: return s
    s = s.replace('</head>', CSS + '\n</head>', 1)
    marker = '  <div class="har-hero__stage"'
    assert marker in s
    s = s.replace(marker, MARKUP + marker, 1)
    s = s.replace('</body>', JS + '\n</body>', 1)
    return s
