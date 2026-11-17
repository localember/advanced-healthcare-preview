# Advanced Healthcare design preview

Design preview only, not the live site (myadvhc.com is untouched). Every page has noindex, robots.txt
disallows everything, a "Design preview, not live" banner, and inactive forms.

## What is here (round 5, 2026-11-17)

- Homepage on the Local Ember Harbor template.
- Inner pages from Harbor's own emitter: Who We Are, Services, Conditions, Patient Stories, Contact,
  Book An Appointment (special/), and a Blog index that links out to his three posts on myadvhc.com.
- Service pages from the Local Ember catalog (tools/bd-generator/catalog/services): chiropractic,
  softwave, shockwave, decompression, neuropathy, massage-therapy, physical-rehabilitation, wellness-care.
- Condition pages from the catalog (catalog/conditions): back-pain, neck-pain, headaches, sciatica,
  disc-injury. These match the six condition cards on myadvhc.com (wellness is the wellness-care page).
- Local Ember standard legal pages.

## Rebuild

```
git clone https://github.com/localember/localember /workspace/le    # or set LE=/path/to/localember
cd <work dir>
AHC_REPO=/path/to/advanced-healthcare-preview python3 /path/to/advanced-healthcare-preview/_build/build.py
python3 /path/to/advanced-healthcare-preview/_build/check.py out
```

`_build/build.py` runs Harbor's emitter on `_build/advanced-healthcare.record.json` into `site/`, then
`_build/post.py` writes the preview into `out/`. Copy `out/` over the repo root (keep `_build/`).

| File | What it does |
| --- | --- |
| `_build/advanced-healthcare.record.json` | Client record. Socials, services, `conditions_helped`, payment, catalog overrides. |
| `_build/build.py` | Emitter wrapper: insurance payment text from the record, six condition pages only, catalog citation stats restored, no "same-week visits" claim. |
| `_build/post.py` | Preview layer: banner, noindex, inactive forms, gold CTAs, relative links, blog band and blog page. |
| `_build/hero_video.py` | Hero loop video and its black overlay (round 5: black, lighter). |
| `_build/svc_images.py` | Round 4 SoftWave and Shockwave photos. |
| `_build/round5.py` | Round 5: social icons, New Patient Special colours, reviews spacing, chiropractic-first expertise band, YouTube click-to-load, Dr. Irwin photo in Our Services, light catalog localisation, story dedupe, Harbor service-hero mobile fix. |
| `_build/check.py` | Link, asset, noindex, banner, em dash and banned-term check. |

Social links live in one place: `brand.socials` in the record (Facebook, X as `twitter`, YouTube).
