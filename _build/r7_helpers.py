#!/usr/bin/env python3
from __future__ import annotations
import json, re
from pathlib import Path
from r7_lib import ROOT, PREVIEW, LIVE, BIZ_ID, MAPS, LOGO, FAQ_ICON

def pfx(depth: int) -> str:
    return "" if depth == 0 else "../" * depth

def business_node() -> dict:
    hours = []
    for day, spans in [
        ("Monday", [("08:00", "12:00"), ("14:00", "18:00")]),
        ("Tuesday", [("14:00", "18:00")]),
        ("Wednesday", [("08:00", "12:00"), ("14:00", "18:00")]),
        ("Thursday", [("08:00", "12:00"), ("14:00", "18:00")]),
    ]:
        for opens, closes in spans:
            hours.append({
                "@type": "OpeningHoursSpecification",
                "dayOfWeek": day,
                "opens": opens,
                "closes": closes,
            })
    person = {
        "@type": "Person",
        "name": "Dr. Nathan M. Irwin",
        "honorificPrefix": "Dr.",
        "honorificSuffix": "DC",
        "jobTitle": "Chiropractor",
    }
    return {
        "@type": "Chiropractor",
        "@id": BIZ_ID,
        "name": "Advanced Healthcare",
        "alternateName": "Advanced Healthcare Chiropractic",
        "url": LIVE,
        "telephone": "+1-970-472-8333",
        "image": LOGO,
        "logo": LOGO,
        "description": (
            "Chiropractor in Fort Collins, CO. Dr. Nathan Irwin has provided "
            "chiropractic care at Advanced Healthcare since 2005. Friday is by appointment. "
            "Saturday and Sunday are closed."
        ),
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "2531 S Shields St #2H",
            "addressLocality": "Fort Collins",
            "addressRegion": "CO",
            "postalCode": "80526",
            "addressCountry": "US",
        },
        "geo": {
            "@type": "GeoCoordinates",
            "latitude": 40.5547248,
            "longitude": -105.0980313,
        },
        "hasMap": MAPS,
        "areaServed": {"@type": "City", "name": "Fort Collins, CO"},
        "founder": person,
        "employee": person,
        "aggregateRating": {
            "@type": "AggregateRating",
            "ratingValue": "4.8",
            "reviewCount": "264",
            "bestRating": "5",
            "worstRating": "1",
        },
        "openingHoursSpecification": hours,
        "sameAs": [
            "https://www.facebook.com/AdvancedHealthcarePLLC/",
            "https://twitter.com/AdvHC",
            "https://www.youtube.com/channel/UCXiiUtTMeOtYIlWgTKLu37A/videos",
            MAPS,
        ],
        "medicalSpecialty": "Chiropractic",
        "currenciesAccepted": "USD",
        "paymentAccepted": "Blue Cross Blue Shield, UnitedHealthcare",
    }

def webpage_node(name, path, description):
    url = f"{PREVIEW}/{path}" if path else PREVIEW + "/"
    return {
        "@type": "WebPage",
        "@id": url + "#webpage",
        "url": url,
        "name": name,
        "description": description,
        "isPartOf": {"@type": "WebSite", "name": "Advanced Healthcare", "url": LIVE},
        "about": {"@id": BIZ_ID},
        "inLanguage": "en-US",
    }

def breadcrumb_node(items):
    els = []
    for i, (name, path) in enumerate(items, 1):
        url = f"{PREVIEW}/{path}" if path else PREVIEW + "/"
        els.append({"@type": "ListItem", "position": i, "name": name, "item": url})
    return {"@type": "BreadcrumbList", "itemListElement": els}

def faq_node(faqs):
    ents = []
    for q, a in faqs:
        text = re.sub(r"<[^>]+>", "", a).replace("&amp;", "&")
        ents.append({
            "@type": "Question",
            "name": q,
            "acceptedAnswer": {"@type": "Answer", "text": text},
        })
    return {"@type": "FAQPage", "mainEntity": ents}

def graph(*nodes):
    data = {"@context": "https://schema.org", "@graph": [business_node(), *nodes]}
    return json.dumps(data, indent=2, ensure_ascii=False)

def crumbs_html(items, depth):
    pre = pfx(depth)
    lis = []
    for i, (name, path) in enumerate(items):
        last = i == len(items) - 1
        href = pre if path == "" else f"{pre}{path}"
        if last:
            lis.append(f'<li><span aria-current="page">{name}</span></li>')
        else:
            lis.append(f'<li><a href="{href}">{name}</a></li>')
    return '<nav class="le-crumbs" aria-label="Breadcrumb"><ol>' + "".join(lis) + "</ol></nav>"

def faq_html(heading, items, prefix):
    parts = [
        '<section class="har-ssfaq" data-sd="cond.faq">',
        '  <div class="har-ssframe">',
        f"    <h2>{heading}</h2>",
        '    <div class="har-ssfaq__list">',
    ]
    for i, (q, a) in enumerate(items, 1):
        parts.append(
            f'    <div class="har-faq__item">\n'
            f'      <button class="har-faq__q" type="button" aria-expanded="false" aria-controls="{prefix}-faq-{i}" id="{prefix}-faq-{i}-btn">\n'
            f'        <span>{q}</span>{FAQ_ICON}\n'
            f'      </button>\n'
            f'      <div class="har-faq__a" id="{prefix}-faq-{i}" role="region" aria-labelledby="{prefix}-faq-{i}-btn"><div><p>{a}</p></div></div>\n'
            f'    </div>'
        )
    parts += ["    </div>", "  </div>", "</section>"]
    return "\n".join(parts)

def related_html(heading, cards, depth):
    pre = pfx(depth)
    arts = []
    for title, body, href in cards:
        arts.append(
            f'    <article class="har-offering har-offering--lift">\n'
            f'      <h3 class="har-offering__title">{title}</h3>\n'
            f'      <p class="har-offering__body">{body}</p>\n'
            f'      <a class="har-btn har-btn--outline" href="{pre}{href}">Learn more</a>\n'
            f'    </article>'
        )
    return (
        '<section class="har-ssrelated" data-sd="svc.related">\n'
        '  <div class="har-ssframe">\n'
        f'    <h2>{heading}</h2>\n'
        '    <div class="har-ssrelated__grid">\n'
        + "\n".join(arts)
        + "\n    </div>\n  </div>\n</section>\n"
    )

def audio_html(title, src, paras, memo_date, duration):
    ps = "\n      ".join(f"<p>{para}</p>" for para in paras)
    return (
        f'<div class="le-audio">\n'
        f'  <p class="le-audio__h">Hear Dr. Irwin explain</p>\n'
        f'  <p class="le-audio__sub">{title}</p>\n'
        f'  <audio controls preload="metadata">\n'
        f'    <source src="{src}" type="audio/mpeg">\n'
        f'    Your browser does not play audio. <a href="{src}">Download the recording</a>.\n'
        f'  </audio>\n'
        f'  <details>\n'
        f'    <summary>Read the transcript</summary>\n'
        f'    <div class="le-audio__transcript">\n'
        f'      {ps}\n'
        f'    </div>\n'
        f"    <p class=\"le-audio__note\">Lightly cleaned from Dr. Irwin's {memo_date} voice memo ({duration}). The wording is his.</p>\n"
        f'  </details>\n'
        f'</div>'
    )

INSURANCE = (
    "    <h2>What does care cost, and do you take insurance?</h2>\n"
    "    <p>No referral is needed to book a first visit. We are in network with BCBS and UHC, and we go over the costs with you before anything begins. Call our office at (970) 472-8333 with any questions about your plan.</p>\n"
    "    <div class=\"har-ssbox har-ssbox--cta\">\n"
    "      <ul class=\"har-ssprose__list har-ssprose__list--tight\">\n"
    "      <li>In network with BCBS and UHC.</li>\n"
    "      <li>No referral needed to book a first visit.</li>\n"
    "      <li>We go over the costs with you before anything begins.</li>\n"
    "    </ul>\n"
    "      <p class=\"har-ssbox__note\">We cannot promise a specific outcome; every body is different.</p>\n"
    "    </div>"
)

def insurance_block():
    return INSURANCE

def cta_html(h, body, depth, label="Book your first visit"):
    pre = pfx(depth)
    return (
        f'<section class="har-svccta" data-sd="cond.cta">\n'
        f'  <div class="har-svccta__inner">\n'
        f'    <h2 class="har-svccta__h">{h}</h2>\n'
        f'    <p class="har-svccta__body">{body}</p>\n'
        f'    <a class="har-btn har-btn--solid" href="{pre}special/">{label}</a>\n'
        f'  </div>\n'
        f'</section>'
    )

def split_template(path):
    html = path.read_text()
    i_head_end = html.index("</head>")
    i_body = html.index("<body")
    i_main = html.index('<main id="main">')
    i_visit = html.index('<section class="har-visit"')
    head = html[:i_head_end]
    header = html[i_body : i_main + len('<main id="main">')]
    footer = html[i_visit:]
    return head, header, footer

def finalize_head(head, title, description, depth, jsonld):
    head = re.sub(r"<title>.*?</title>", f"<title>{title}</title>", head, count=1)
    if 'name="description"' in head:
        head = re.sub(
            r'<meta name="description" content="[^"]*">',
            f'<meta name="description" content="{description}">',
            head,
            count=1,
        )
    else:
        head = re.sub(
            r"</title>",
            f'</title>\n<meta name="description" content="{description}">',
            head,
            count=1,
        )
    href = f"{pfx(depth)}le-seo.css"
    if "le-seo.css" not in head:
        head += f'\n<link rel="stylesheet" href="{href}">\n'
    head = re.sub(
        r"\n?<script type=\"application/ld\+json\" id=\"le-schema\">.*?</script>\n?",
        "\n",
        head,
        flags=re.S,
    )
    head += f'<script type="application/ld+json" id="le-schema">\n{jsonld}\n</script>\n'
    return head

def set_nav_active(header, href_suffix):
    header = re.sub(r' class="har-nav__item is-active"', ' class="har-nav__item"', header)
    pattern = rf'(<li class="har-nav__item")(><a class="har-nav__link" href="[^"]*{re.escape(href_suffix)}")'
    header, n = re.subn(pattern, r'<li class="har-nav__item is-active"\2', header, count=1)
    return header

def set_body_class(header, cls):
    return re.sub(r'<body class="[^"]*">', f'<body class="{cls}">', header, count=1)

def assemble(head, header, main, footer):
    return head + "</head>\n" + header + "\n" + main + "\n" + footer

def write_page(src, dest, title, description, depth, body_class, nav_href, main, extra_nodes):
    head, header, footer = split_template(src)
    jsonld = graph(*extra_nodes)
    json.loads(jsonld)
    head = finalize_head(head, title, description, depth, jsonld)
    header = set_body_class(header, body_class)
    header = set_nav_active(header, nav_href)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(assemble(head, header, main, footer))
    print(f"wrote {dest.relative_to(ROOT)}")

def extract_faqs(html):
    faqs = []
    for m in re.finditer(
        r'<button class="har-faq__q"[^>]*>\s*<span>(.*?)</span>.*?'
        r'<div class="har-faq__a"[^>]*>\s*<div><p>(.*?)</p></div>',
        html,
        re.S,
    ):
        q = re.sub(r"<[^>]+>", "", m.group(1))
        faqs.append((q, m.group(2)))
    return faqs
