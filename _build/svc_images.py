"""Round 4: real SoftWave and Shockwave photos on the homepage expertise band.
Source: Build ticket AHC-2026-11-17a, Drive folder "Site Images" (originals stay in Drive).
  Softwave-Hero.webp (2560x1400, 2.6 MB)        -> assets/images/softwave-treatment.webp (1600x875): lead card photo
  softwave-unit-1.webp (1200x800, 30 KB)       -> assets/images/softwave-unit.webp (1046x714, white margin and baked shadow cropped off): SoftWave row
  Shockwave-Therapy-2.webp (528x607, 12.4 KB)  -> assets/images/shockwave-handpiece.webp (528x607, not upscaled): Shockwave row
Call apply(html) on the homepage HTML. Idempotent."""
CSS = '''<style id="le-svc-images">
.le-svc-thumb{display:block;width:100%;height:auto;max-width:340px;aspect-ratio:3/2;object-fit:cover;margin-top:14px;border-radius:10px;box-shadow:0 6px 16px rgba(0,0,0,.22)}
.le-svc-thumb--shock{max-width:340px;object-position:20% 30%}
.har-expertise__photo[src*="softwave-treatment"]{object-position:62% 50%}
.har-expertise__row>div{min-width:0}
</style>'''
OLD_PHOTO = '''src="assets/images/Chiropractic-Fort-Collins-CO-Chiropractic-Adjustment-Room.webp" alt="An adjustment room at Advanced Healthcare in Fort Collins">'''
NEW_PHOTO = '''src="assets/images/softwave-treatment.webp" alt="A provider treating a patient's foot with a SoftWave applicator" width="1600" height="875" loading="lazy">'''
SW_ROW = '''<h3 class="har-expertise__rowh">SoftWave</h3><p>Unfocused acoustic-wave sessions for minor muscle aches, alongside chiropractic care.</p>'''
SH_ROW = '''<h3 class="har-expertise__rowh">Shockwave Therapy</h3><p>Shockwave therapy for long-running tendon and heel problems that have stopped easing.</p>'''
SW_IMG = '<img class="le-svc-thumb" src="assets/images/softwave-unit.webp" alt="A SoftWave therapy unit with its touchscreen controls" width="1046" height="714" loading="lazy">'
SH_IMG = '<img class="le-svc-thumb le-svc-thumb--shock" src="assets/images/shockwave-handpiece.webp" alt="A shockwave therapy handpiece being applied to a patient\'s arm" width="528" height="607" loading="lazy">'
def apply(s):
    if 'le-svc-thumb' in s: return s
    for old in (OLD_PHOTO, SW_ROW, SH_ROW): assert old in s, old[:40]
    s = s.replace(OLD_PHOTO, NEW_PHOTO, 1)
    s = s.replace(SW_ROW, SW_ROW + SW_IMG, 1)
    s = s.replace(SH_ROW, SH_ROW + SH_IMG, 1)
    return s.replace('</head>', CSS + '\n</head>', 1)
