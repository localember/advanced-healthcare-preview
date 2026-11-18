#!/usr/bin/env python3
import json, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from r7_lib import ROOT, BIZ_ID, PREVIEW, LIVE
from r7_helpers import (
    write_page, graph, webpage_node, breadcrumb_node, faq_node,
    finalize_head, extract_faqs, crumbs_html,
)
from r7_pages import (
    back_pain_main, new_patients_main, types_of_care_main, wellness_main,
    LBP_FAQS, NPE_FAQS, TOC_FAQS, WELL_FAQS,
)

def write_four():
    src_cond = ROOT / "back-pain/index.html"
    src_svc = ROOT / "wellness-care/index.html"

    lbp_desc = (
        "Low back pain care in Fort Collins with Dr. Nathan Irwin. The first exam normally takes an hour. "
        "Care may be a few visits or two to four months of rehabilitation, depending on your goals."
    )
    write_page(src_cond, ROOT / "back-pain/index.html",
        "Back Pain Care in Fort Collins, CO", lbp_desc, 1, "condition-single", "conditions/",
        back_pain_main(),
        [
            webpage_node("Back Pain Care in Fort Collins, CO", "back-pain/", lbp_desc),
            breadcrumb_node([("Home", ""), ("Conditions", "conditions/"), ("Back pain", "back-pain/")]),
            faq_node(LBP_FAQS),
            {"@type": "MedicalCondition", "name": "Low back pain",
             "alternateName": ["Lower back pain", "Back pain"],
             "associatedAnatomy": {"@type": "AnatomicalStructure", "name": "Lumbar spine"}},
        ])

    npe_desc = (
        "What a first visit with Dr. Nathan Irwin in Fort Collins includes: a complete health history, "
        "a full exam, digital x-rays when needed, and a report of findings before you choose a type of care."
    )
    write_page(src_svc, ROOT / "new-patients/index.html",
        "New Patient Exam and First Visit in Fort Collins, CO", npe_desc, 1, "service-single", "services/",
        new_patients_main(),
        [
            webpage_node("New Patient Exam and First Visit in Fort Collins, CO", "new-patients/", npe_desc),
            breadcrumb_node([("Home", ""), ("Services", "services/"), ("New patients", "new-patients/")]),
            faq_node(NPE_FAQS),
            {"@type": "MedicalProcedure", "name": "New patient chiropractic examination",
             "procedureType": "Examination and report of findings",
             "howPerformed": "Complete health history, physical and orthopedic and neurological evaluation as needed, and digital x-rays when indicated, at Advanced Healthcare in Fort Collins, CO.",
             "provider": {"@id": BIZ_ID}},
        ])

    toc_desc = (
        "Types of chiropractic care at Advanced Healthcare in Fort Collins: visit-to-visit care, "
        "relief care of about two to six weeks, and corrective care with strength-based rehabilitation. You choose."
    )
    write_page(src_svc, ROOT / "types-of-care/index.html",
        "Types of Chiropractic Care in Fort Collins, CO", toc_desc, 1, "service-single", "services/",
        types_of_care_main(),
        [
            webpage_node("Types of Chiropractic Care in Fort Collins, CO", "types-of-care/", toc_desc),
            breadcrumb_node([("Home", ""), ("Services", "services/"), ("Types of care", "types-of-care/")]),
            faq_node(TOC_FAQS),
            {"@type": "MedicalProcedure", "name": "Chiropractic types of care",
             "procedureType": "Visit-to-visit, relief, and corrective chiropractic care",
             "howPerformed": "A plan chosen after the new patient exam and, when needed, a report of findings, at Advanced Healthcare in Fort Collins, CO.",
             "provider": {"@id": BIZ_ID}},
        ])

    well_desc = (
        "Wellness chiropractic care in Fort Collins with Dr. Nathan Irwin. After relief or corrective care, "
        "visits every other week, every three weeks, or once a month to maintain motion and function."
    )
    write_page(src_svc, ROOT / "wellness-care/index.html",
        "Wellness &amp; Maintenance Chiropractic Care in Fort Collins, CO", well_desc, 1, "service-single", "services/",
        wellness_main(),
        [
            webpage_node("Wellness and Maintenance Chiropractic Care in Fort Collins, CO", "wellness-care/", well_desc),
            breadcrumb_node([("Home", ""), ("Services", "services/"), ("Wellness care", "wellness-care/")]),
            faq_node(WELL_FAQS),
            {"@type": "MedicalProcedure", "name": "Wellness chiropractic care",
             "procedureType": "Maintenance chiropractic care",
             "howPerformed": "Scheduled visits every other week, every three weeks, or once a month after an initial set of care, at Advanced Healthcare in Fort Collins, CO.",
             "provider": {"@id": BIZ_ID}},
        ])


def patch_existing():
    path = ROOT / "index.html"
    html = path.read_text()
    html = html.replace(
        '<section class="har-faq" data-sd="faq.band"',
        '<section class="har-faq" id="faqs" data-sd="faq.band"',
        1,
    )
    html = html.replace(
        "<p>We start by listening. Expect a conversation about your history and goals, a hands-on exam, and a clear explanation of what we found and the options that fit, before anything else.</p>",
        "<p>The new patient exam is the pillar of treatment here, and it is more in depth than most clinics. Dr. Irwin takes a complete health history, then a full evaluation with range of motion, palpation, muscle testing, and, when needed, orthopedic and neurological testing, before he lays a finger to adjust. If the exam shows they are needed, digital x-rays are taken in the clinic. Sometimes he will adjust on the first day. If it is a more complex case, he may have you come back to go through the exam and films, then establish the type of care you want to do. <a href=\"new-patients/\">See what a first visit includes</a>.</p>",
        1,
    )
    html = html.replace(
        "<p>It depends on what is going on and how your body responds. After your first exam we will walk you through a plan and check in as you go, rather than committing you to a fixed number up front.</p>",
        "<p>It depends on your goals and what the exam finds. Some people want visit-to-visit care just to get the pain out of the area. Relief care is often two to six weeks, with the goal of increasing range of motion and decreasing muscle guarding and pain. Most patients want more than just symptoms gone, and choose a corrective style of care that includes strength-based rehabilitation. After that, some people move on to wellness care. <a href=\"types-of-care/\">Read about the types of care</a>. At the end of the day, it is your choice, and the goal is to get you as far along as you want to go.</p>",
        1,
    )
    old = (
        "Care for <a href=\"back-pain/\">back pain</a>, <a href=\"neck-pain/\">neck pain</a>, "
        "<a href=\"headaches/\">headaches and migraines</a>, <a href=\"sciatica/\">sciatica</a> and "
        "<a href=\"disc-injury/\">disc injuries</a>, plus <a href=\"wellness-care/\">wellness care</a> "
        "for people who would rather keep moving well. We focus on the root cause of your discomfort, not just the symptoms."
    )
    new = (
        "Care for <a href=\"back-pain/\">back pain</a>, <a href=\"neck-pain/\">neck pain</a>, "
        "<a href=\"headaches/\">headaches and migraines</a>, <a href=\"sciatica/\">sciatica</a> and "
        "<a href=\"disc-injury/\">disc injuries</a>, plus <a href=\"wellness-care/\">wellness care</a> "
        "for people who would rather keep moving well. Every plan starts with a "
        "<a href=\"new-patients/\">thorough first exam</a>, and you choose the "
        "<a href=\"types-of-care/\">type of care</a> that fits your goals. We focus on the cause of the problem, not just a quick adjustment."
    )
    if old in html:
        html = html.replace(old, new, 1)
        print("patched homepage conditions sentence")
    else:
        print("WARN: homepage conditions sentence not found")

    faqs = extract_faqs(html)
    desc = (
        "Chiropractor in Fort Collins, CO. Dr. Nathan Irwin at Advanced Healthcare. "
        "Thorough new patient exams, types of care you choose, and 4.8 stars from 264 Google reviews."
    )
    nodes = [
        webpage_node("Chiropractor in Fort Collins, CO - Advanced Healthcare", "", desc),
        breadcrumb_node([("Home", "")]),
    ]
    if faqs:
        nodes.append(faq_node(faqs))
    jsonld = graph(*nodes)
    json.loads(jsonld)
    head, rest = html.split("</head>", 1)
    head = finalize_head(head, "Chiropractor in Fort Collins, CO - Advanced Healthcare", desc, 0, jsonld)
    path.write_text(head + "</head>" + rest)
    print(f"patched index.html ({len(faqs)} homepage FAQs in schema)")

    sp = ROOT / "services/index.html"
    shtml = sp.read_text()
    card_npe = (
        "    <article class=\"har-offering\">\n"
        "      <h3 class=\"har-offering__title\">New Patient Exam</h3>\n"
        "      <p class=\"har-offering__body\">A lengthy, in-depth first exam, and a report of findings when the case is more complex, before you choose a type of care.</p>\n"
        "      <a class=\"har-btn har-btn--outline\" href=\"../new-patients/\">Learn more</a>\n"
        "    </article>\n"
    )
    card_toc = (
        "    <article class=\"har-offering\">\n"
        "      <h3 class=\"har-offering__title\">Types of Care</h3>\n"
        "      <p class=\"har-offering__body\">Visit-to-visit, relief, and corrective care, explained in Dr. Irwin's words, so the plan is your choice.</p>\n"
        "      <a class=\"har-btn har-btn--outline\" href=\"../types-of-care/\">Learn more</a>\n"
        "    </article>\n"
    )
    needle = "      <a class=\"har-btn har-btn--outline\" href=\"../chiropractic/\">Learn more</a>\n    </article>\n"
    if "new-patients/" not in shtml and needle in shtml:
        shtml = shtml.replace(needle, needle + card_npe + card_toc, 1)
        sp.write_text(shtml)
        print("patched services grid")
    else:
        print("services grid skip or already patched")

    cp = ROOT / "conditions/index.html"
    chtml = cp.read_text()
    chtml2 = chtml.replace(
        "Most back pain has a reason, and finding it beats guessing at it.",
        "It could have started yesterday or years ago. The first visit is a full exam, not a 10-minute adjustment.",
        1,
    )
    if chtml2 != chtml:
        cp.write_text(chtml2)
        print("patched conditions blurb")

    chp = ROOT / "chiropractic/index.html"
    ch = chp.read_text()
    old = (
        "<h2>What is a first visit like?</h2>\n"
        "    <p>It starts with a conversation and a careful check, not an adjustment. We take a history, perform a thorough examination, and determine whether chiropractic care fits your problem. If it does, we explain what we found in plain language. If it does not, we will say so and help you find the right next step.</p>\n"
        "    <p>Then you come back for a second visit. That is where we go through everything the examination and any imaging turned up, explain what it means in plain language, and give you our recommendations: what we believe is going on, what we would do about it, and roughly how long we would expect it to take. You leave that visit knowing the plan, not guessing at it.</p>"
    )
    new = (
        "<h2>What is a first visit like?</h2>\n"
        "    <p>The new patient exam is the pillar of treatment in the clinic, and it is more lengthy and more in depth than most clinics. It starts with a complete health history and a full evaluation: range of motion, palpation, muscle testing, and, if needed, orthopedic and neurological testing, to pinpoint the area before Dr. Irwin lays a finger to adjust. If the exam shows x-rays are relevant, digital films are taken in the clinic.</p>\n"
        "    <p>Sometimes he will choose to adjust on the first day. If it is a complex case, he may spend time going through the films and the exam, then have you come back to review the results, go through the x-rays, and establish the <a href=\"../types-of-care/\">type of care</a> you want to go through. <a href=\"../new-patients/\">Read about the first visit and the report of findings</a>.</p>"
    )
    if old in ch:
        chp.write_text(ch.replace(old, new, 1))
        print("patched chiropractic first-visit copy")
    else:
        print("WARN: chiropractic first-visit block not found")

    spp = ROOT / "special/index.html"
    sh = spp.read_text()
    if "new-patients/" not in sh:
        sh = sh.replace(
            '<p class="har-bookslot__body">Fill out the form below, including all required fields, and we will get back to you as soon as possible.</p>',
            '<p class="har-bookslot__body">Fill out the form below, including all required fields, and we will get back to you as soon as possible. Wondering what that first visit is like? <a href="../new-patients/">Read about the new patient exam and report of findings</a>.</p>',
            1,
        )
        spp.write_text(sh)
        print("patched special page")


def patch_sitewide_schema():
    skip = {
        "back-pain/index.html", "new-patients/index.html", "types-of-care/index.html",
        "wellness-care/index.html", "index.html",
    }
    meta = {
        "accessibility/index.html": ("Accessibility Statement - Advanced Healthcare", "Accessibility", "legal"),
        "anti-discrimination/index.html": ("Anti-Discrimination Disclaimer - Advanced Healthcare", "Anti-Discrimination", "legal"),
        "blog/index.html": ("Blog - Advanced Healthcare, Chiropractor in Fort Collins, CO", "Blog", "blog"),
        "chiropractic/index.html": ("Chiropractic Care in Fort Collins, CO", "Chiropractic Care", "service"),
        "conditions/index.html": ("Conditions We Help With in Fort Collins, CO", "Conditions", "hub"),
        "contact-us/index.html": ("Contact Advanced Healthcare - Fort Collins, CO", "Contact", "page"),
        "decompression/index.html": ("Non-Surgical Spinal Decompression in Fort Collins, CO", "Spinal Decompression", "service"),
        "disc-injury/index.html": ("Disc Injury Care in Fort Collins, CO", "Disc Injury", "condition"),
        "good-faith-estimate/index.html": ("Good Faith Estimate - Advanced Healthcare", "Good Faith Estimate", "legal"),
        "headaches/index.html": ("Headache & Migraine Care in Fort Collins, CO", "Headaches & Migraines", "condition"),
        "healthcare-disclaimer/index.html": ("Healthcare Disclaimer - Advanced Healthcare", "Healthcare Disclaimer", "legal"),
        "hipaa-privacy-policy/index.html": ("HIPAA Privacy Practices - Advanced Healthcare", "HIPAA Privacy Practices", "legal"),
        "massage-therapy/index.html": ("Massage Therapy in Fort Collins, CO", "Massage Therapy", "service"),
        "neck-pain/index.html": ("Neck Pain Care in Fort Collins, CO", "Neck Pain", "condition"),
        "neuropathy/index.html": ("Neuropathy Care in Fort Collins, CO", "Neuropathy", "service"),
        "patient-stories/index.html": ("Patient Stories - Advanced Healthcare", "Patient Stories", "page"),
        "physical-rehabilitation/index.html": ("Physical Rehabilitation in Fort Collins, CO", "Physical Rehabilitation", "service"),
        "privacy-policy/index.html": ("Privacy Policy - Advanced Healthcare", "Privacy Policy", "legal"),
        "sciatica/index.html": ("Sciatica Care in Fort Collins, CO", "Sciatica", "condition"),
        "services/index.html": ("Chiropractic Services in Fort Collins, CO", "Services", "hub"),
        "shockwave/index.html": ("Shockwave Therapy in Fort Collins, CO", "Shockwave Therapy", "service"),
        "softwave/index.html": ("SoftWave in Fort Collins, CO", "SoftWave", "service"),
        "special/index.html": ("New Patient Special - Advanced Healthcare", "Book an Appointment", "page"),
        "terms-service/index.html": ("Terms Of Service - Advanced Healthcare", "Terms of Service", "legal"),
        "who-we-are/index.html": ("Who We Are - Advanced Healthcare", "Who We Are", "page"),
    }
    for rel, (title, crumb_name, kind) in meta.items():
        if rel in skip:
            continue
        path = ROOT / rel
        if not path.exists():
            continue
        html = path.read_text()
        slug = rel.split("/")[0] + "/"
        desc_m = re.search(r'name="description" content="([^"]+)"', html)
        desc = desc_m.group(1) if desc_m else title
        if kind == "condition":
            crumbs = [("Home", ""), ("Conditions", "conditions/"), (crumb_name, slug)]
        elif kind == "service":
            crumbs = [("Home", ""), ("Services", "services/"), (crumb_name, slug)]
        else:
            crumbs = [("Home", ""), (crumb_name, slug)]
        nodes = [webpage_node(title, slug, desc), breadcrumb_node(crumbs)]
        if kind == "condition":
            nodes.append({"@type": "MedicalCondition", "name": crumb_name,
                          "associatedAnatomy": {"@type": "AnatomicalStructure", "name": "Spine"}})
        if kind == "service":
            nodes.append({"@type": "MedicalProcedure", "name": crumb_name,
                          "procedureType": "Chiropractic care",
                          "howPerformed": "In-office care at Advanced Healthcare in Fort Collins, CO.",
                          "provider": {"@id": BIZ_ID}})
        faqs = extract_faqs(html)
        if faqs:
            nodes.append(faq_node(faqs))
        jsonld = graph(*nodes)
        json.loads(jsonld)
        head, rest = html.split("</head>", 1)
        head = finalize_head(head, title, desc, 1, jsonld)
        html = head + "</head>" + rest
        if 'class="le-crumbs"' not in html:
            crumb = crumbs_html(crumbs, 1)
            inserted = False
            for pat, repl in [
                (r'(<div class="har-sshero__copy">\s*)', r"\1" + crumb + "\n      "),
                (r'(<div class="har-pagehero__inner">\s*)', r"\1" + crumb + "\n    "),
                (r'(<div class="har-svcintro__inner">\s*)', r"\1" + crumb + "\n    "),
            ]:
                html2, n = re.subn(pat, repl, html, count=1)
                if n:
                    html = html2
                    inserted = True
                    break
            if not inserted:
                html = html.replace('<main id="main">', '<main id="main">\n' + crumb + "\n", 1)
        path.write_text(html)
        print(f"schema+crumbs {rel} ({len(faqs)} faqs)")


def write_llms():
    text = Path(__file__).with_name("llms.txt.src")
    # written separately if present, else inline short
    src = ROOT / "llms.txt"
    src.write_text((Path(__file__).parent / "llms.txt.src").read_text() if (Path(__file__).parent / "llms.txt.src").exists() else "Advanced Healthcare\n")
    print("wrote llms.txt")


def main():
    write_four()
    patch_existing()
    patch_sitewide_schema()
    write_llms()
    print("done")

if __name__ == "__main__":
    main()
