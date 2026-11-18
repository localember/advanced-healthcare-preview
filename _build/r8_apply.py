#!/usr/bin/env python3
"""Round 8: restore dry needling (verbatim memo clauses), add the service page
and catalog draft, and patch related copy, schema, services hub, and checks."""
from __future__ import annotations
import json, re, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from r7_lib import ROOT, PREVIEW, LBP_PARAS, NPE_PARAS, WELL_PARAS
from r7_helpers import (
    write_page, webpage_node, breadcrumb_node, faq_node, faq_html,
    related_html, insurance_block, cta_html, crumbs_html,
)

# --- 1. Restore verbatim clauses in r7_lib.py ---------------------------------
lib = (ROOT / "_build" / "r7_lib.py").read_text()
repls = [
    (
        "work with that low back pain. We do spinal decompression for disc-related injuries",
        "work with that low back pain. We do dry needling. We do spinal decompression for disc-related injuries",
    ),
    (
        "like massage therapy or decompression or SoftWave therapy",
        "like massage therapy or decompression or dry needling or SoftWave therapy",
    ),
    (
        "elect to do spinal decompression therapy once a month just to maintain good healthy function of the muscles.",
        "elect to do spinal decompression therapy or dry needling once a month just to maintain good healthy function of the muscles.",
    ),
]
for a, b in repls:
    if a not in lib:
        # already restored, or unexpected wording
        if b not in lib:
            raise SystemExit(f"r7_lib.py missing expected clause:\n{a}")
    else:
        lib = lib.replace(a, b)
(ROOT / "_build" / "r7_lib.py").write_text(lib)
print("updated _build/r7_lib.py")

# --- 2. r7_pages FAQ / body strings ------------------------------------------
pages = (ROOT / "_build" / "r7_pages.py").read_text()
page_repls = [
    (
        "modalities such as massage therapy, decompression, or SoftWave therapy",
        "modalities such as massage therapy, decompression, dry needling, or SoftWave therapy",
    ),
    (
        "elect to do spinal decompression therapy once a month just to maintain good healthy function of the muscles.",
        "elect to do spinal decompression therapy or dry needling once a month just to maintain good healthy function of the muscles.",
    ),
    (
        "Alongside the exam and chiropractic care, the clinic uses spinal decompression for disc-related injuries or osteoarthritic change (arthritis in the lower part of the back), shockwave therapy, massage therapy,",
        "Alongside the exam and chiropractic care, the clinic uses dry needling, spinal decompression for disc-related injuries or osteoarthritic change (arthritis in the lower part of the back), shockwave therapy, massage therapy,",
    ),
]
for a, b in page_repls:
    if a in pages:
        pages = pages.replace(a, b)
    elif b not in pages:
        print("WARN r7_pages.py missing:", a[:80])
(ROOT / "_build" / "r7_pages.py").write_text(pages)
print("updated _build/r7_pages.py")

# --- 3. Sitewide HTML / llms / check patches ---------------------------------
DN_CARD = """    <article class="har-offering har-offering--lift">
      <h3 class="har-offering__title">Dry Needling</h3>
      <p class="har-offering__body">One of the treatments Dr. Irwin uses for low back pain, in relief care, and as a once-a-month option some wellness patients choose.</p>
      <a class="har-btn har-btn--outline" href="../dry-needling/">Learn more</a>
    </article>
"""

html_repls = [
    (
        "work with that low back pain. We do spinal decompression for disc-related injuries",
        "work with that low back pain. We do dry needling. We do spinal decompression for disc-related injuries",
    ),
    (
        "like massage therapy or decompression or SoftWave therapy",
        "like massage therapy or decompression or dry needling or SoftWave therapy",
    ),
    (
        "modalities such as massage therapy, decompression, or SoftWave therapy",
        "modalities such as massage therapy, decompression, dry needling, or SoftWave therapy",
    ),
    (
        'decompression</a>, or <a href="../softwave/">SoftWave therapy</a>',
        'decompression</a>, <a href="../dry-needling/">dry needling</a>, or <a href="../softwave/">SoftWave therapy</a>',
    ),
    (
        "elect to do spinal decompression therapy once a month just to maintain good healthy function of the muscles.",
        "elect to do spinal decompression therapy or dry needling once a month just to maintain good healthy function of the muscles.",
    ),
    (
        'spinal decompression therapy</a> once a month just to maintain good healthy function of the muscles.',
        'spinal decompression therapy</a> or <a href="../dry-needling/">dry needling</a> once a month just to maintain good healthy function of the muscles.',
    ),
    (
        "Alongside the exam and chiropractic care, the clinic uses spinal decompression for disc-related injuries or osteoarthritic change (arthritis in the lower part of the back), shockwave therapy, massage therapy,",
        "Alongside the exam and chiropractic care, the clinic uses dry needling, spinal decompression for disc-related injuries or osteoarthritic change (arthritis in the lower part of the back), shockwave therapy, massage therapy,",
    ),
    (
        "sometimes with massage, decompression, or SoftWave",
        "sometimes with massage, decompression, dry needling, or SoftWave",
    ),
]

touched = []
for path in sorted(ROOT.rglob("index.html")):
    if "/_build/" in str(path):
        continue
    s = path.read_text()
    orig = s
    for a, b in html_repls:
        s = s.replace(a, b)
    # Add a related card on memo-fed pages that mention the restored clauses,
    # if the page already has a related grid and does not already link the service.
    rel = str(path.relative_to(ROOT))
    memo_rel = {
        "back-pain/index.html",
        "types-of-care/index.html",
        "wellness-care/index.html",
        "new-patients/index.html",
        "massage-therapy/index.html",
        "decompression/index.html",
        "softwave/index.html",
    }
    if rel in memo_rel and 'href="../dry-needling/"' not in s and "har-ssrelated__grid" in s:
        s = s.replace(
            '</div>\n  </div>\n</section>\n\n\n<section class="har-visit"',
            DN_CARD + '</div>\n  </div>\n</section>\n\n\n<section class="har-visit"',
            1,
        )
    if s != orig:
        path.write_text(s)
        touched.append(str(path.relative_to(ROOT)))
print("patched html:", ", ".join(touched) or "(none)")

# Services hub card (after Massage Therapy)
svc = ROOT / "services" / "index.html"
shtml = svc.read_text()
if 'href="../dry-needling/"' not in shtml:
    needle = """    <article class="har-offering">
      <h3 class="har-offering__title">Massage Therapy</h3>
      <p class="har-offering__body">Therapeutic massage from licensed therapists, easing tight muscles so the work holds.</p>
      <a class="har-btn har-btn--outline" href="../massage-therapy/">Learn more</a>
    </article>
"""
    card = """    <article class="har-offering">
      <h3 class="har-offering__title">Dry Needling</h3>
      <p class="har-offering__body">One of the treatments Dr. Irwin uses for low back pain, in relief care, and as a once-a-month option some wellness patients choose.</p>
      <a class="har-btn har-btn--outline" href="../dry-needling/">Learn more</a>
    </article>
"""
    if needle not in shtml:
        raise SystemExit("services hub massage card not found")
    shtml = shtml.replace(needle, needle + card, 1)
    svc.write_text(shtml)
    print("added Dry Needling card to services hub")
else:
    print("services hub already links dry needling")

# llms.txt and source
for name in ("llms.txt", "_build/llms.txt.src"):
    p = ROOT / name
    if not p.exists():
        continue
    t = p.read_text()
    t = t.replace(
        "sometimes with massage, decompression, or SoftWave",
        "sometimes with massage, decompression, dry needling, or SoftWave",
    )
    if "dry-needling" not in t:
        t = t.replace(
            "- [Massage therapy](https://myadvhc.com/massage-therapy/)\n",
            "- [Massage therapy](https://myadvhc.com/massage-therapy/)\n- [Dry needling](https://myadvhc.com/dry-needling/)\n",
        )
    # wellness sentence in llms if present
    t = t.replace(
        "some elect spinal decompression once a month",
        "some elect spinal decompression or dry needling once a month",
    )
    p.write_text(t)
    print("updated", name)

# check.py: dry needling is no longer a banned term
chk = ROOT / "_build" / "check.py"
ct = chk.read_text()
ct2 = ct.replace("('UMR', 'Dry Needling', 'dry needling', 'Same-week', 'TBD', '{{', 'type=\"submit\"')",
                 "('UMR', 'Same-week', 'TBD', '{{', 'type=\"submit\"')")
if ct2 == ct:
    print("WARN check.py ban list not updated as expected")
else:
    chk.write_text(ct2)
    print("updated _build/check.py ban list")

# --- 4. Catalog draft --------------------------------------------------------
draft = {
    "id": "dry-needling",
    "name": "Dry Needling",
    "slug": "dry-needling",
    "status": "catalog draft",
    "note": "New catalog file. No dry-needling.json existed in localember/localember tools/bd-generator/catalog/services. Add this to the catalog repo later; do not push it from this preview. Body is limited to Dr. Irwin's November 2026 voice memos plus the standard clinic insurance block. Do not invent mechanism, session length, needle type, sensations, or safety claims.",
    "h1": "Dry Needling in {{city}}, {{state}}",
    "nav_label": "Dry Needling",
    "short_name": "Dry Needling",
    "hero": {
        "kicker": "What we do",
        "sub": "Dry needling is one of the treatments Dr. Irwin uses in the office, including for low back pain, as part of relief care, and as an option some wellness patients choose once a month.",
        "image": "Catalog/Services/placeholder-clinic-treatment.webp",
        "alt": "A treatment room at Advanced Healthcare in {{city}}"
    },
    "meta": [
        "Complimentary consultation for new patients",
        "In network with BCBS and UHC"
    ],
    "blocks": [
        {
            "type": "answer",
            "label": "The short answer",
            "text": "Dr. Irwin offers dry needling at Advanced Healthcare in Fort Collins. He includes it among the treatments used for low back pain, as one of the modalities in relief care (alongside massage, decompression, and SoftWave) when the goal is to get symptoms out as quickly as possible, and as an option some wellness patients elect once a month to help maintain healthy muscle function."
        },
        {
            "type": "lede",
            "text": "This page stays inside what Dr. Irwin said in his November 2026 voice memos. If you want to know whether dry needling belongs in your plan, that is worked out at the first exam."
        },
        {
            "type": "h2",
            "text": "When Dr. Irwin uses dry needling"
        },
        {
            "type": "p",
            "text": "In his low back pain memo, he lists dry needling among the modalities used in the office, alongside spinal decompression for disc-related injuries or osteoarthritic change, shockwave therapy, massage therapy, and stretching through full strength and rehabilitation."
        },
        {
            "type": "p",
            "text": "In his types of care memo, relief care is typically two to six weeks. A lot of times that type of care includes different modalities, like massage therapy, decompression, dry needling, or SoftWave therapy, to try to get symptoms out as fast as possible. The goal of relief care is increasing range of motion and decreasing muscle guarding, spasm, or pain, to the point where the patient feels better."
        },
        {
            "type": "p",
            "text": "In his wellness care memo, some patients, after relief and/or a full corrective form of care, elect spinal decompression therapy or dry needling once a month just to maintain good healthy function of the muscles."
        },
        {
            "type": "h2",
            "text": "How do I know if it is part of my plan?"
        },
        {
            "type": "p",
            "text": "The type of care, and which modalities are used, is the patient's choice after the exam. If the case is more complex, that conversation happens at a return visit to review the exam and any x-rays, then establish the type of care the patient wants to go through."
        }
    ],
    "faqs": [
        {
            "q": "Do you offer dry needling?",
            "a": "Yes. Dr. Irwin does dry needling in the clinic. He names it in his memos on low back pain, relief care, and wellness care."
        },
        {
            "q": "When is dry needling used?",
            "a": "He lists it among the modalities for low back pain; as one of the options in relief care, typically two to six weeks, alongside massage, decompression, and SoftWave; and as something some wellness patients elect once a month to help maintain healthy muscle function."
        },
        {
            "q": "How do I know if dry needling is right for me?",
            "a": "That is worked out at the first exam, and, when the case is complex, at the report of findings, before you choose a type of care."
        },
        {
            "q": "Do you take insurance?",
            "a": "No referral is needed to book a first visit. We are in network with BCBS and UHC, and we go over the costs with you before anything begins."
        }
    ],
    "related": [
        {"title": "Low back pain", "slug": "back-pain"},
        {"title": "Types of care", "slug": "types-of-care"},
        {"title": "Wellness care", "slug": "wellness-care"},
        {"title": "New patient exam", "slug": "new-patients"}
    ]
}
draft_path = ROOT / "_build" / "catalog-drafts" / "dry-needling.json"
draft_path.write_text(json.dumps(draft, indent=2) + "\n")
print("wrote", draft_path.relative_to(ROOT))

# --- 5. Service page ---------------------------------------------------------
faqs = [
    (
        "Do you offer dry needling?",
        "Yes. Dr. Irwin does dry needling in the clinic. He names it in his memos on low back pain, relief care, and wellness care.",
    ),
    (
        "When is dry needling used?",
        "He lists it among the modalities for low back pain; as one of the options in relief care, typically two to six weeks, alongside massage, decompression, and SoftWave; and as something some wellness patients elect once a month to help maintain healthy muscle function.",
    ),
    (
        "How do I know if dry needling is right for me?",
        'That is worked out at the <a href="../new-patients/">first exam</a>, and, when the case is complex, at the report of findings, before you choose a <a href="../types-of-care/">type of care</a>.',
    ),
    (
        "Do you take insurance?",
        "No referral is needed to book a first visit. We are in network with BCBS and UHC, and we go over the costs with you before anything begins. Call our office at (970) 472-8333 with any questions about your plan.",
    ),
]
# Schema FAQ answers must be plain text (no tags)
faq_schema = [
    (q, re.sub(r"<[^>]+>", "", a)) for q, a in faqs
]
related = [
    ("Low back pain", "When dry needling is one of the modalities used for lower back pain.", "back-pain/"),
    ("Types of care", "Visit-to-visit, relief, and corrective care, in his words, including where dry needling can fit in relief care.", "types-of-care/"),
    ("Wellness care", "Some wellness patients elect dry needling once a month to help maintain healthy muscle function.", "wellness-care/"),
    ("New patient exam", "What the first visit and report of findings actually include.", "new-patients/"),
]

crumbs = [("Home", ""), ("Services", "services/"), ("Dry Needling", "dry-needling/")]
main = f'''<main>
<section class="har-sshero" data-sd="svc.hero">
  <div class="har-sshero__inner">
    <div class="har-sshero__row">
    <div class="har-sshero__copy">
      {crumbs_html(crumbs, 1)}
      <p class="har-svcintro__kicker">What we do</p>
      <h1 class="har-sshero__h" data-sd="svc.h1">Dry Needling in Fort Collins, CO</h1>
      <p class="har-sshero__sub">Dry needling is one of the treatments Dr. Irwin uses at Advanced Healthcare in Fort Collins, including for low back pain, as part of relief care, and as an option some wellness patients choose once a month.</p>
      <div class="har-sshero__actions">
        <a class="har-btn har-btn--solid" href="../special/">Book an appointment</a>
      </div>
    </div>
    <div class="har-sshero__media">
      <div class="har-sshero__frame">
        <img class="har-sshero__img" data-sd="svc.photo" src="../assets/images/Chiropractic-Fort-Collins-CO-Chiropractic-Adjustment-Room.webp" alt="A treatment room at Advanced Healthcare in Fort Collins">
      </div>
    </div>
    </div>
    <div class="har-sshero__pills">
      <p class="har-sspill" data-sd="svc.pill">Complimentary consultation for new patients</p>
      <p class="har-sspill">In network with BCBS and UHC</p>
    </div>
  </div>
</section>
<section class="har-ssprose" data-sd="cat.prose">
  <div class="har-ssprose__inner">
    <div class="har-sscallout">
      <p class="har-svcintro__kicker">The short answer</p>
      <p class="har-sscallout__p">Dr. Irwin offers dry needling at Advanced Healthcare in Fort Collins. He includes it among the treatments used for low back pain, as one of the modalities in relief care (alongside massage, decompression, and SoftWave) when the goal is to get symptoms out as quickly as possible, and as an option some wellness patients elect once a month to help maintain healthy muscle function.</p>
    </div>
    <p class="har-ssprose__lead">This page stays inside what Dr. Irwin said in his November 2026 voice memos. If you want to know whether dry needling belongs in your plan, that is worked out at the first exam.</p>
    <h2>When Dr. Irwin uses dry needling</h2>
    <p>In his low back pain memo, he lists dry needling among the modalities used in the office, alongside <a href="../decompression/">spinal decompression</a> for disc-related injuries or osteoarthritic change, <a href="../shockwave/">shockwave therapy</a>, <a href="../massage-therapy/">massage therapy</a>, and stretching through full strength and rehabilitation.</p>
    <p>In his types of care memo, relief care is typically two to six weeks. A lot of times that type of care includes different modalities, like massage therapy, decompression, dry needling, or <a href="../softwave/">SoftWave therapy</a>, to try to get symptoms out as fast as possible. The goal of relief care is increasing range of motion and decreasing muscle guarding, spasm, or pain, to the point where the patient feels better. See <a href="../types-of-care/">types of care</a>.</p>
    <p>In his wellness care memo, some patients, after relief and/or a full corrective form of care, elect spinal decompression therapy or dry needling once a month just to maintain good healthy function of the muscles. See <a href="../wellness-care/">wellness care</a>.</p>
    <h2>How do I know if it is part of my plan?</h2>
    <p>The type of care, and which modalities are used, is the patient's choice after the exam. If the case is more complex, that conversation happens at a return visit to review the exam and any x-rays, then establish the type of care the patient wants to go through. Start with the <a href="../new-patients/">new patient exam</a>.</p>
    {insurance_block()}
  </div>
</section>
{faq_html("Dry Needling Questions We Hear Most", faqs, "dn")}
{related_html("You might also look at", related, 1)}
{cta_html("Ready to talk about whether this fits your care?", "Book a complimentary consultation, or call (970) 472-8333.", 1)}
</main>'''

# Avoid em dashes and check
if "\u2014" in main or "\u2013" in main:
    raise SystemExit("em dash or en dash slipped into dry needling main")

extra = [
    webpage_node(
        "Dry Needling in Fort Collins, CO",
        "dry-needling/",
        "Dry needling at Advanced Healthcare in Fort Collins, offered by Dr. Nathan Irwin for low back pain, relief care, and as a once-a-month wellness option some patients choose.",
    ),
    breadcrumb_node([
        ("Home", ""),
        ("Services", "services/"),
        ("Dry Needling", "dry-needling/"),
    ]),
    {
        "@type": "MedicalProcedure",
        "name": "Dry Needling",
        "url": f"{PREVIEW}/dry-needling/",
        "procedureType": "Chiropractic care",
        "howPerformed": "In-office care at Advanced Healthcare in Fort Collins, CO.",
        "provider": {"@id": "https://myadvhc.com/#business"},
    },
    faq_node(faq_schema),
]

src = ROOT / "massage-therapy" / "index.html"
dest = ROOT / "dry-needling" / "index.html"
# Body class: match other service pages
body_class = "har-body har-body--svc"
# Try to copy massage body class if present
import re as _re
ms = src.read_text()
bm = _re.search(r'<body class="([^"]*)">', ms)
if bm:
    body_class = bm.group(1)

write_page(
    src,
    dest,
    "Dry Needling in Fort Collins, CO",
    "Dry needling at Advanced Healthcare in Fort Collins, offered by Dr. Nathan Irwin for low back pain, relief care, and as a once-a-month wellness option some patients choose.",
    1,
    body_class,
    "services/",
    main,
    extra,
)

# Final sanity: no em dashes in new/changed pages, transcripts restored
dn = dest.read_text()
assert "noindex" in dn and "le-preview-banner" in dn
assert "\u2014" not in dn
assert 'type="submit"' not in dn
assert "Dry Needling" in dn
assert "MedicalProcedure" in dn
assert "We do dry needling. We do spinal decompression" in (ROOT / "back-pain" / "index.html").read_text()
assert "or dry needling or SoftWave" in (ROOT / "types-of-care" / "index.html").read_text()
assert "decompression therapy or dry needling once a month" in (ROOT / "wellness-care" / "index.html").read_text()
print("dry needling page and restorations OK")
