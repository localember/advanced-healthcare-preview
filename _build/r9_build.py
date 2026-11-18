#!/usr/bin/env python3
"""Round 9: memos are internal source only. Rewrite memo-topic pages as
polished web copy for Google and AI search. Do not publish audio or transcripts."""
from __future__ import annotations
import json, re, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from r7_lib import ROOT, PREVIEW
from r7_helpers import (
    write_page, webpage_node, breadcrumb_node, faq_node, faq_html,
    related_html, insurance_block, cta_html, crumbs_html,
)

EM = "\u2014"

def words(text: str) -> int:
    return len(re.findall(r"[A-Za-z0-9']+", re.sub(r"<[^>]+>", " ", text)))

def direct(text: str, label: str) -> str:
    n = words(text)
    if n < 40 or n > 60:
        raise SystemExit(f"DIRECT {label}: {n} words (need 40-60)\n{text}")
    if EM in text or "\u2013" in text:
        raise SystemExit(f"dash in {label}")
    return text

def section(h2: str, answer: str, body: str) -> str:
    ans = direct(answer, h2)
    return f"    <h2>{h2}</h2>\n    <p class=\"le-direct\">{ans}</p>\n{body}"

def no_bad(s: str, label: str) -> None:
    if EM in s:
        raise SystemExit(f"em dash in {label}")
    if "Hear Dr. Irwin" in s or "le-audio" in s or "Read the transcript" in s:
        raise SystemExit(f"audio/transcript leftover in {label}")
    if "Same-week" in s or "{{" in s:
        raise SystemExit(f"banned term in {label}")

def hero(crumbs, kicker, h1, sub, img, alt, pills, actions_href="../special/", actions="Book an appointment"):
    pill_html = "\n".join(f'      <p class="har-sspill">{p}</p>' for p in pills)
    return f'''<section class="har-sshero" data-sd="svc.hero">
  <div class="har-sshero__inner">
    <div class="har-sshero__row">
    <div class="har-sshero__copy">
      {crumbs_html(crumbs, 1)}
      <p class="har-svcintro__kicker">{kicker}</p>
      <h1 class="har-sshero__h">{h1}</h1>
      <p class="har-sshero__sub">{sub}</p>
      <div class="har-sshero__actions">
        <a class="har-btn har-btn--solid" href="{actions_href}">{actions}</a>
      </div>
    </div>
    <div class="har-sshero__media">
      <div class="har-sshero__frame">
        <img class="har-sshero__img" src="{img}" alt="{alt}">
      </div>
    </div>
    </div>
    <div class="har-sshero__pills">
{pill_html}
    </div>
  </div>
</section>'''

def page_main(hero_html, short_label, short, sections, faqs, faq_heading, related, cta_h, cta_body, extra_before_faq=""):
    body = "\n".join(sections)
    return f'''<main>
{hero_html}
<section class="har-ssprose" data-sd="cat.prose">
  <div class="har-ssprose__inner">
    <div class="har-sscallout">
      <p class="har-svcintro__kicker">{short_label}</p>
      <p class="har-sscallout__p">{short}</p>
    </div>
{body}
{extra_before_faq}
    {insurance_block()}
  </div>
</section>
{faq_html(faq_heading, faqs, "r9")}
{related_html("You might also look at", related, 1)}
{cta_html(cta_h, cta_body, 1)}
</main>'''

# ---------------------------------------------------------------------------
# New patients
# ---------------------------------------------------------------------------
NP_SHORT = direct(
    "Your first visit at Advanced Healthcare in Fort Collins is a thorough new patient exam, not a one-page form and a quick adjustment. We take a complete health history and evaluate how you move before any adjustment. If x-rays are needed, we take them here in the clinic. Some people are adjusted the same day.",
    "np short",
)
NP_SECTIONS = [
    section(
        "What happens at your first chiropractic visit in Fort Collins?",
        NP_SHORT,
        """    <p>The exam is the foundation of care at Advanced Healthcare. It is more lengthy, and more in depth, than the brief visits many clinics offer. A typical short visit might use a one-page intake, talk through symptoms, and move straight to an adjustment. We take a deeper look first, so we can pinpoint where the problem is coming from.</p>
    <p>If the case is more complex, Dr. Irwin may have you return for a <a href="../types-of-care/">report of findings and a conversation about types of care</a> before treatment begins. Either way, the goal of the first visit is to understand the cause, not just to get you in and out quickly.</p>""",
    ),
    section(
        "What does the new patient exam include?",
        "We start with a complete health history: when the problem started, not just this episode, the quality of the pain, whether it radiates, any surgeries, and symptoms over the course of your life. Then we evaluate range of motion and palpation, and, when needed, muscle testing and orthopedic and neurological tests, before any adjustment.",
        """    <p>The evaluation looks at how areas of the body relate. Neck symptoms can come from the shoulder. Mid-back issues can too. Low back pain can be tied to pelvic unleveling, hip bursitis, or a muscular issue such as the piriformis, even when someone comes in saying they have sciatica. Degenerative disc disease in the lower back can also be part of the picture.</p>
    <p>The point of this work is to pinpoint the area the problem is coming from before Dr. Irwin begins an adjustment. That is what makes the first visit at this Fort Collins chiropractic office different from a quick, symptoms-only stop.</p>""",
    ),
    section(
        "Do you take x-rays on the first visit?",
        "If the exam shows we need to see more before we start adjusting, we recommend digital x-rays, taken here in the clinic. That is especially common when pain is a primary reason for the visit. Films can also reveal findings such as anterolisthesis or spondylolisthesis. Seeing what we are working with helps us treat the cause.",
        """    <p>We do not treat imaging as a formality, and we do not skip it when the exam shows it matters. If films are recommended, they are taken in the clinic, so you do not have to go somewhere else to get a basic set of digital radiographs.</p>""",
    ),
    section(
        "Do you adjust on the first day?",
        "Sometimes, yes. After the evaluation, Dr. Irwin may adjust you on the first day when that is appropriate. If the case is more complex, he may go through the exam and any films first, then have you return to review the findings before care begins. That choice is based on what the exam shows, not on a set routine.",
        """    <p>When a return visit is needed, that visit is the report of findings. It is time set aside to review the examination, go through any x-rays, and then establish the type of care you want to go through.</p>""",
    ),
    section(
        "What is a report of findings?",
        "A report of findings is a return visit used when the case is more complex. We review the exam, go through any x-rays that were taken, and then establish the type of care you want to go through. It is a conversation about what we found and what your options are, not a plan decided for you.",
        """    <p>From there, you choose how to proceed, from <a href="../types-of-care/">visit-to-visit, relief, or corrective care</a> to <a href="../wellness-care/">wellness care</a> later on, if you want it. Our goal is to get you as far along as you want to go, and as healthy as you want to be.</p>""",
    ),
]
NP_FAQS = [
    ("How is your new patient exam different?",
     "It is more lengthy, and more in depth, than a one-page form and a quick adjustment. The exam is the foundation of care here. We take a complete health history and a full evaluation before any adjustment, so we can find the cause."),
    ("What happens during the exam?",
     "A complete health history, then a full evaluation in the exam room: range of motion and palpation, and, when needed, muscle testing and orthopedic and neurological testing. The goal is to pinpoint where the problem is coming from."),
    ("Do you take x-rays on the first visit?",
     "When the exam shows they are relevant, yes. Digital x-rays are taken in the clinic, especially when pain is a primary reason for the visit, and they can also show findings such as anterolisthesis or spondylolisthesis."),
    ("Do you adjust on the first day?",
     "Sometimes. If the case is straightforward, Dr. Irwin may adjust you the same day. If it is more complex, he may have you return for a report of findings before treatment starts."),
    ("What is a report of findings?",
     "A return visit to review the exam and any x-rays, then establish the type of care you want to go through. It is used when the case is more complex."),
    ("Do I need a referral, and do you take insurance?",
     "No referral is needed to book a first visit. We are in network with BCBS and UHC, and we go over the costs with you before anything begins. Call (970) 472-8333 with questions about your plan."),
]
NP_RELATED = [
    ("Types of care", "Visit-to-visit, relief, corrective, and wellness care, so the plan is your choice.", "types-of-care/"),
    ("Low back pain care", "How we evaluate and treat lower back pain in Fort Collins.", "back-pain/"),
    ("Wellness care", "Ongoing care after relief or corrective work, on a schedule you choose.", "wellness-care/"),
    ("Meet Dr. Irwin", "Dr. Nathan Irwin, a Palmer graduate who has cared for Fort Collins patients since 2005.", "who-we-are/"),
]

# ---------------------------------------------------------------------------
# Back pain
# ---------------------------------------------------------------------------
BP_SHORT = direct(
    "Most back pain has a reason, and finding it beats guessing at it. At Advanced Healthcare in Fort Collins, Dr. Irwin takes a full-scale look at what is causing your low back pain. The first visit is a detailed history and a full exam that normally takes an hour, not a quick adjustment off a short form.",
    "bp short",
)
BP_SECTIONS = [
    section(
        "What causes low back pain?",
        "Most low back pain is mechanical: it comes from how the joints, discs, muscles, and nerves of the spine are moving and loading, rather than from a serious disease. In Fort Collins, that often starts with everyday strain, from yard work and raking leaves in the fall to scooping snow in winter. It may have started yesterday, or years ago.",
        """    <p>Everyday strain, a stretch of poor posture, a weak or guarded core, or a single awkward lift can leave the low back stiff, irritated, and slow to settle on its own. The usual contributors we see in Fort Collins families include:</p>
    <ul class="har-ssprose__list">
      <li>Prolonged sitting and desk work that shortens the hips and loads the low back.</li>
      <li>Lifting and twisting under load, from moving day to a toddler on one hip.</li>
      <li>Weak or deconditioned core muscles that leave the spine doing work they should share.</li>
      <li>Repetitive strain from a job, a sport, or a hobby done the same way for years.</li>
      <li>Old injuries that changed how you move and quietly overload one area.</li>
    </ul>
    <p>Less often, back pain points to something that needs a medical work-up first. Part of a good first visit is ruling that out, and referring you on if that is the right call.</p>""",
    ),
    section(
        "What happens at the first visit for back pain in Fort Collins?",
        "The first visit is an exam that normally takes an hour, not a 10 or 15 minute stop. We take a detailed history and an ortho-neuro check with motion palpation, looking for tight muscles, inflammation, or a disc injury that needs more testing. In-clinic digital x-rays are used when pain is extreme or refers down the leg.",
        """    <p>The history looks at when the pain started, where it is, and whether it is new or has been going on for years. From there, the exam helps us decide if we are comfortable starting care the first day, or if more testing is needed.</p>
    <p>When we use digital x-ray, we are looking for degenerative change or arthritic conditions that may be contributing to the pain, especially with extreme pain or symptoms down the leg. For a fuller picture of the first visit, see our <a href="../new-patients/">new patient exam in Fort Collins</a>.</p>""",
    ),
    section(
        "How does a Fort Collins chiropractor treat low back pain?",
        "Care starts with finding the cause, then matching treatment to your goals. Alongside chiropractic care, we may use dry needling, spinal decompression for disc-related injuries or osteoarthritic change, shockwave therapy, massage therapy, and stretching that leads into full strength and rehabilitation. Home stretching and strength work are part of getting the result to hold.",
        """    <p>Chiropractic care works on the mechanics of the problem. Specific adjustments restore movement to joints that have gotten stiff and guarded, which helps take pressure off irritated tissue and calm the pain. We start with a little frequency in treatment, then build from there.</p>
    <p>Depending on what the exam shows, care may also include <a href="../dry-needling/">dry needling</a>, <a href="../decompression/">spinal decompression</a> for disc-related injuries or arthritis in the lower back, <a href="../shockwave/">shockwave therapy</a>, <a href="../massage-therapy/">massage therapy</a>, and <a href="../physical-rehabilitation/">passive and active stretching through strength and rehabilitation</a>. The mix is chosen for your back, not as a fixed package.</p>""",
    ),
    section(
        "How long does low back pain care take?",
        "It depends on your goals. For some people, care can be as simple as three or four visits. If you want to get the problem resolved and work on strengthening, it can take two, three, or four months to truly rehabilitate a low back. After the exam, you choose the type of care that fits what you want to accomplish.",
        """    <p>Some people want short-term, visit-to-visit care just to get the pain out of the area. Others choose relief care, typically two to six weeks, or a corrective style of care that rebuilds endurance and then dynamic strength, so everyday lifting is less likely to set the pain off again. You can read about those options on our <a href="../types-of-care/">types of care</a> page.</p>""",
    ),
    section(
        "When should I come in for low back pain?",
        "The best time to come in is at the start of low back pain, rather than waiting to see if it will go away on its own. Coming in early gives the body less chance to develop compensatory patterns and muscle guarding, which can make treatment take longer and make it harder to recover.",
        """    <p>Low back pain can be crippling, and it can keep you from the activities you love, whether it started yesterday or a long time ago. If the pain is severe or comes with numbness, weakness, or fever, call your medical doctor first. For common mechanical back pain, keep gently moving rather than staying flat in bed, and avoid the one heavy lift or twist that set it off, until you can be seen.</p>""",
    ),
]
BP_FAQS = [
    ("What happens on the first visit for low back pain?",
     "A detailed history and a full exam that normally takes an hour, including an ortho-neuro check with motion palpation. We are looking for tight muscles, inflammation, or a disc injury that needs more testing, so we can treat the cause."),
    ("Do you take x-rays for back pain?",
     "We have full diagnostic digital x-ray in the clinic. We use it especially for areas of extreme pain or referrals down the leg, looking for degenerative change or arthritic conditions that may be contributing to the pain."),
    ("How long does low back pain care take?",
     "It can be three or four visits if that is your goal. If you want to resolve the problem and work on strengthening, it can take two, three, or four months to truly rehabilitate the low back. The plan follows your goals."),
    ("What kinds of treatment do you use for low back pain?",
     "Alongside the exam and chiropractic care, we may use dry needling, spinal decompression for disc-related injuries or osteoarthritic change, shockwave therapy, massage therapy, and stretching through full strength and rehabilitation."),
    ("When should I come in for low back pain?",
     "At the start of the pain, rather than waiting for it to go away. Coming in early gives compensatory patterns and muscle guarding less chance to set in, which can shorten care and make recovery easier."),
    ("Is chiropractic care safe for back pain?",
     "For most people with common, mechanical low back pain, gentle chiropractic care has a strong safety record. The first visit includes a careful history and exam so care is matched to your body. If something suggests you should be seen medically first, we will tell you."),
    ("Do you take insurance?",
     "No referral is needed to book a first visit. We are in network with BCBS and UHC, and we go over the costs with you before anything begins. Call (970) 472-8333 with questions about your plan."),
]
BP_RELATED = [
    ("New patient exam", "What the first visit and report of findings include at our Fort Collins office.", "new-patients/"),
    ("Sciatica and leg pain", "When low back pain refers down the leg.", "sciatica/"),
    ("Disc injury care", "When an irritated disc is part of the picture.", "disc-injury/"),
    ("Types of care", "Visit-to-visit, relief, corrective, and wellness care, in terms you can choose from.", "types-of-care/"),
]
BP_CITATION = """    <div class="har-ssbox">
      <p><strong class="le-stat">Around 80%</strong> of adults deal with low back pain at some point in their lives, which is why it is one of the most common reasons people seek care in the first place. You are far from alone in this, and it is one of the most workable things we see.</p>
      <p class="har-ssbox__src">Source: U.S. National Center for Complementary and Integrative Health (NCCIH), Low-Back Pain and Complementary Health Approaches. <a href="https://www.nccih.nih.gov/health/low-back-pain-and-complementary-health-approaches-what-you-need-to-know" target="_blank" rel="noopener">nccih.nih.gov</a></p>
    </div>"""

# ---------------------------------------------------------------------------
# Types of care
# ---------------------------------------------------------------------------
TOC_SHORT = direct(
    "After the exam, you choose the type of care. Visit-to-visit care is short-term, to get pain out of the area. Relief care is typically two to six weeks, to restore motion and calm muscle guarding. Corrective care rebuilds strength so the problem is less likely to return. Wellness care comes later if you want it.",
    "toc short",
)
TOC_SECTIONS = [
    section(
        "What types of chiropractic care does Advanced Healthcare offer?",
        TOC_SHORT,
        """    <p>These are not competing packages, and you are not locked into one of them. They are ways of matching care to your goals after a <a href="../new-patients/">thorough first exam</a>, and, when the case is more complex, after a report of findings. At the end of the day, the choice is yours.</p>""",
    ),
    section(
        "What is visit-to-visit care?",
        "Visit-to-visit care is the most cost-effective form of treatment we offer, and it is for people whose sole goal is to get the pain out of the area. It is short-term, acute pain management. We work with people who want that, and we do not push a longer plan on anyone who has chosen this approach.",
        """    <p>If you only want to be seen as needed while symptoms are active, say so. We will work with that goal, then you can decide later whether you want to go further.</p>""",
    ),
    section(
        "What is relief care, and how long does it last?",
        "Relief care typically lasts two to six weeks. The goal is to increase range of motion and decrease muscle guarding, muscle spasm, or muscle pain, to the point where you feel better. We often pair visits with other care in the office, such as massage, decompression, dry needling, or SoftWave, to help get symptoms out as quickly as possible.",
        """    <p>Relief care is more involved than visit-to-visit symptom relief, but it is still focused on getting you comfortable and moving again. If you later want to work on strength so the pain is less likely to return, that is the next conversation, not an automatic next step.</p>
    <p>Learn more about <a href="../massage-therapy/">massage therapy</a>, <a href="../decompression/">spinal decompression</a>, <a href="../dry-needling/">dry needling</a>, and <a href="../softwave/">SoftWave therapy</a>, which may be part of a relief plan when they fit what the exam shows.</p>""",
    ),
    section(
        "What is corrective care?",
        "Corrective care is for people who want more than just symptoms gone. They do not want the pain to come back, and they want the area stronger and healthier. We start with endurance-based strength training, then dynamic strength such as lifting, bending, and twisting, so everyday tasks are less likely to set the pain off again.",
        """    <p>That everyday test might be as simple as picking up a laundry basket and setting it on the washer, or lifting a box off the garage floor and putting it on a shelf. The aim is for your body to have the strength to do that work without throwing you back into an acute or painful state.</p>
    <p>Corrective work is paired with the hands-on care you already know from the clinic, and with the <a href="../physical-rehabilitation/">stretching and rehabilitation</a> you continue at home.</p>""",
    ),
    section(
        "What is wellness care, and when does it start?",
        "Wellness care is a later choice, not the starting point. After a relief set of care, a full corrective form of care, or both, some patients choose to keep coming in to maintain the results they have already received. Visits are every other week, every three weeks, or once a month, with a focus on good motion and function.",
        """    <p>You can read the full picture, including what people often continue at home and what they sometimes add in the office, on our <a href="../wellness-care/">wellness care</a> page.</p>""",
    ),
    section(
        "Who decides the type of care?",
        "You do. After the exam, and after a report of findings when the case is more complex, we establish the type of care you want to go through. Our goal is to get you as far along as you want to go, and back to as healthy as you want to be. The plan follows your goals, not a script.",
        """    <p>If you want to start with visit-to-visit care and change later, you can. If you want to go straight into a relief or corrective plan, you can. We will be clear about what we found and what each option involves, then you decide.</p>""",
    ),
]
TOC_FAQS = [
    ("Do I have to choose a type of care up front?",
     "No. The type of care is your choice after the exam, and after a report of findings when the case is more complex. You can also change direction later as your goals change."),
    ("What is visit-to-visit care?",
     "Short-term care whose sole goal is to get the pain out of the area. It is the most cost-effective form of treatment we offer, and we work with people who want that approach."),
    ("What is relief care, and how long does it last?",
     "Relief care is typically two to six weeks. The goal is to increase range of motion and decrease muscle guarding, spasm, or pain. It may include massage, decompression, dry needling, or SoftWave."),
    ("What is corrective care?",
     "A strength-based, rehabilitative style of care for people who want more than symptoms gone. We usually start with endurance-based strength training, then dynamic strength work, so everyday lifting is less likely to bring the pain back."),
    ("What happens after relief or corrective care?",
     "Some patients choose wellness care to maintain the results they have already received, at every other week, every three weeks, or once a month. That is a later choice, not a requirement."),
    ("Do you take insurance?",
     "No referral is needed to book a first visit. We are in network with BCBS and UHC, and we go over the costs with you before anything begins. Call (970) 472-8333 with questions about your plan."),
]
TOC_RELATED = [
    ("New patient exam", "What the first visit and report of findings include, before you choose a type of care.", "new-patients/"),
    ("Wellness care", "How we maintain results after relief or corrective care.", "wellness-care/"),
    ("Low back pain care", "An example of how those types of care are used for a common problem.", "back-pain/"),
    ("Chiropractic care", "The adjustments and movement work at the center of each plan.", "chiropractic/"),
]

# ---------------------------------------------------------------------------
# Wellness
# ---------------------------------------------------------------------------
WELL_NOTE = """    <p>Coverage for ongoing wellness visits can differ by plan. We are in network with BCBS and UHC, and we go over the costs with you before anything begins so you can decide what is worth it to you.</p>"""
WELL_SHORT = direct(
    "Wellness care in Fort Collins is for patients who, after relief or corrective care, want to maintain the results they have already received. Visits are every other week, every three weeks, or once a month. The goal is good motion and function, along with the stretching and strength work you have already been taught.",
    "well short",
)
WELL_SECTIONS = [
    section(
        "What is wellness chiropractic care?",
        "Wellness care is ongoing chiropractic care after you have already done a relief set of care, a full corrective form of care, or both. It is designed to maintain the results you received in that first stage of care, and to help maintain good motion and function in an area, rather than to start treatment for a new problem.",
        """    <p>It is a later choice, not the starting point. If you are new to the office, we begin with a <a href="../new-patients/">thorough first exam</a> and then the <a href="../types-of-care/">type of care</a> that fits your current goals.</p>""",
    ),
    section(
        "How often do wellness visits happen?",
        "Wellness visits at Advanced Healthcare range from every other week all the way to once a month. In the office, that means every other week, every three weeks, or one time a month, set to what helps you maintain the motion and function you have already gained, not to a single standard schedule.",
        """    <p>The rhythm can change as your body and your life change. The decision to continue, pause, or stop stays with you.</p>""",
    ),
    section(
        "What do you do between visits, and what can be added?",
        "Patients are encouraged to continue the stretching and flexibility they have been taught, as well as their strength-based rehabilitation, so they can keep moving well. Some people also elect massage through the clinic's massage clubs, and some elect spinal decompression or dry needling once a month to help maintain healthy muscle function.",
        """    <p>Those additions are optional, and they are chosen with you, not added as a requirement of wellness care. You can read more about <a href="../massage-therapy/">massage therapy</a>, <a href="../decompression/">spinal decompression</a>, and <a href="../dry-needling/">dry needling</a> if you want to understand where they fit.</p>""",
    ),
]
WELL_FAQS = [
    ("What is wellness care?",
     "Ongoing care after relief and/or a full corrective form of care, designed to maintain the results you have already received and to help maintain good motion and function."),
    ("How often would I come in?",
     "Every other week, every three weeks, or once a month, depending on what helps you maintain your results."),
    ("Do I still do the exercises?",
     "Yes. We encourage you to continue the stretching, flexibility, and strength-based rehabilitation you have been taught, so you can maintain good movement going forward."),
    ("Can wellness care include massage, decompression, or dry needling?",
     "Yes. Some patients elect massage through the clinic's massage clubs, and some elect spinal decompression or dry needling once a month to help maintain healthy muscle function."),
    ("Can I stop whenever I want?",
     "Yes. Wellness care is your choice. Tell us if you want to pause or stop, and we will note where you left off if you decide to pick it back up later."),
    ("Do you take insurance for wellness care?",
     "Coverage for ongoing wellness visits can differ by plan. We are in network with BCBS and UHC, and we go over the costs with you before anything begins. Call (970) 472-8333 with questions about your plan."),
]
WELL_RELATED = [
    ("Types of care", "Where wellness sits after visit-to-visit, relief, and corrective care.", "types-of-care/"),
    ("New patient exam", "The first visit that comes before any wellness plan.", "new-patients/"),
    ("Massage therapy", "Massage clubs some wellness patients use in the clinic.", "massage-therapy/"),
    ("Spinal decompression", "An option some patients elect once a month to help maintain muscle function.", "decompression/"),
]

# ---------------------------------------------------------------------------
# Dry needling (polish memo insight; this is not its own memo topic)
# ---------------------------------------------------------------------------
DN_SHORT = direct(
    "Dr. Irwin offers dry needling at Advanced Healthcare in Fort Collins. We use it among the treatments for low back pain, as one of the options in relief care, typically two to six weeks, alongside massage, decompression, and SoftWave, and as a once-a-month choice some wellness patients make to help maintain healthy muscle function.",
    "dn short",
)
DN_SECTIONS = [
    section(
        "Do you offer dry needling in Fort Collins?",
        "Yes. Dry needling is one of the treatments Dr. Irwin uses at Advanced Healthcare in Fort Collins. It is offered in the same office as chiropractic care, and it is used when it fits the problem in front of us, not as a stand-alone routine for every patient.",
        """    <p>If you are wondering whether it belongs in your plan, that is worked out at the <a href="../new-patients/">first exam</a>, and, when the case is more complex, at the report of findings.</p>""",
    ),
    section(
        "When is dry needling used?",
        DN_SHORT,
        """    <p>For <a href="../back-pain/">low back pain</a>, dry needling sits among the modalities we may use alongside spinal decompression, shockwave therapy, massage therapy, and stretching through strength and rehabilitation.</p>
    <p>In <a href="../types-of-care/">relief care</a>, typically two to six weeks, we may include dry needling with massage, decompression, or SoftWave when the goal is to get symptoms out as quickly as possible and to increase range of motion while decreasing muscle guarding, spasm, or pain.</p>
    <p>In <a href="../wellness-care/">wellness care</a>, after relief or corrective work, some patients elect dry needling once a month, sometimes with spinal decompression, to help maintain good healthy function of the muscles.</p>""",
    ),
    section(
        "How do I know if dry needling is part of my plan?",
        "That decision comes after the exam, and after a report of findings when the case is more complex. The type of care, and which treatments are used, is your choice. We will be clear about why dry needling may or may not fit, then you decide whether to include it.",
        """    <p>Dry needling is one tool, not a requirement of care at this office. If it is not a good fit, we will say so and point you to the options that are.</p>""",
    ),
]
DN_FAQS = [
    ("Do you offer dry needling?",
     "Yes. Dr. Irwin does dry needling at Advanced Healthcare in Fort Collins, alongside the other treatments used in the clinic."),
    ("When is dry needling used?",
     "Among the treatments for low back pain; as an option in relief care, typically two to six weeks, alongside massage, decompression, and SoftWave; and as a once-a-month choice some wellness patients make to help maintain healthy muscle function."),
    ("How do I know if dry needling is right for me?",
     "That is worked out at the first exam, and, when the case is complex, at the report of findings, before you choose a type of care."),
    ("Do you take insurance?",
     "No referral is needed to book a first visit. We are in network with BCBS and UHC, and we go over the costs with you before anything begins. Call (970) 472-8333 with questions about your plan."),
]
DN_RELATED = [
    ("Low back pain care", "Where dry needling may be used among other low back treatments.", "back-pain/"),
    ("Types of care", "How relief care and other plans are chosen after the exam.", "types-of-care/"),
    ("Wellness care", "Where some patients elect dry needling once a month.", "wellness-care/"),
    ("New patient exam", "The first visit that decides whether this belongs in your plan.", "new-patients/"),
]

def write_topic(src_rel, dest_rel, title, desc, nav, body_class, crumbs, kicker, h1, sub, img, alt, pills, short, sections, faqs, faq_h, related, cta_h, cta_body, extra_nodes, extra_before_faq=""):
    hero_html = hero(crumbs, kicker, h1, sub, img, alt, pills)
    # short answer already validated when it's a direct(); if not, validate
    if words(short) < 40 or words(short) > 70:
        # top short can be the same 40-60; allow slight wrap up to 70 for the callout only if needed
        direct(short, f"{dest_rel} short")
    main = page_main(hero_html, "The short answer", short, sections, faqs, faq_h, related, cta_h, cta_body, extra_before_faq)
    no_bad(main, dest_rel)
    src = ROOT / src_rel
    dest = ROOT / dest_rel
    nodes = extra_nodes
    write_page(src, dest, title, desc, 1, body_class, nav, main, nodes)
    return dest

def body_class_of(rel):
    s = (ROOT / rel).read_text()
    m = re.search(r'<body class="([^"]*)">', s)
    return m.group(1) if m else "service-single"

def run():
    # ---- new patients ----
    write_topic(
        "new-patients/index.html", "new-patients/index.html",
        "First Chiropractic Visit in Fort Collins, CO",
        "What to expect at your first chiropractic visit in Fort Collins. The new patient exam at Advanced Healthcare usually includes a full history, a thorough exam, and in-clinic digital x-rays when they are needed.",
        "new-patients/", body_class_of("new-patients/index.html"),
        [("Home", ""), ("New patient exam", "new-patients/")],
        "Your first visit",
        "Your first visit with a Fort Collins chiropractor",
        "A thorough new patient exam at Advanced Healthcare, so we can find the cause before we start care.",
        "../assets/images/Chiropractic-Fort-Collins-CO-Information-Center.webp",
        "The front desk and information center at Advanced Healthcare in Fort Collins",
        ["Complimentary consultation", "History, exam, and digital x-ray when needed", "2531 S Shields St, Fort Collins"],
        NP_SHORT, NP_SECTIONS, NP_FAQS, "New patient questions we hear most", NP_RELATED,
        "Ready for a thorough first exam?",
        "Book a complimentary consultation, or call (970) 472-8333. We will take it from there.",
        [
            webpage_node("First Chiropractic Visit in Fort Collins, CO", "new-patients/",
                         "What to expect at your first chiropractic visit in Fort Collins. The new patient exam at Advanced Healthcare usually includes a full history, a thorough exam, and in-clinic digital x-rays when they are needed."),
            breadcrumb_node([("Home", ""), ("New patient exam", "new-patients/")]),
            {"@type": "MedicalProcedure", "name": "New patient chiropractic exam",
             "url": f"{PREVIEW}/new-patients/",
             "procedureType": "Chiropractic care",
             "howPerformed": "In-office exam at Advanced Healthcare in Fort Collins, CO.",
             "provider": {"@id": "https://myadvhc.com/#business"}},
            faq_node(NP_FAQS),
        ],
    )

    # ---- back pain ----
    write_topic(
        "back-pain/index.html", "back-pain/index.html",
        "Back Pain Chiropractor in Fort Collins, CO",
        "Low back pain care in Fort Collins with Dr. Nathan Irwin at Advanced Healthcare. The first exam normally takes an hour. Care may be a few visits or two to four months of rehabilitation, depending on your goals.",
        "conditions/", body_class_of("back-pain/index.html"),
        [("Home", ""), ("Conditions", "conditions/"), ("Back pain", "back-pain/")],
        "Conditions we help with",
        "Back pain care in Fort Collins",
        "Most back pain has a reason, and finding it beats guessing at it. At Advanced Healthcare, the first visit is a full exam, so we can treat the cause.",
        "../assets/images/back-pain.webp",
        "Low back pain at a desk, the posture it most often builds in",
        ["Complimentary consultation", "The first exam normally takes an hour", "Serving Fort Collins"],
        BP_SHORT, BP_SECTIONS, BP_FAQS, "Back pain questions we hear most", BP_RELATED,
        "You do not have to work around it.",
        "Book a complimentary consultation, or call (970) 472-8333.",
        [
            webpage_node("Back Pain Chiropractor in Fort Collins, CO", "back-pain/",
                         "Low back pain care in Fort Collins with Dr. Nathan Irwin at Advanced Healthcare. The first exam normally takes an hour. Care may be a few visits or two to four months of rehabilitation, depending on your goals."),
            breadcrumb_node([("Home", ""), ("Conditions", "conditions/"), ("Back pain", "back-pain/")]),
            faq_node(BP_FAQS),
            {"@type": "MedicalCondition", "name": "Low back pain",
             "alternateName": ["Lower back pain", "Back pain"],
             "associatedAnatomy": {"@type": "AnatomicalStructure", "name": "Lumbar spine"}},
        ],
        extra_before_faq=BP_CITATION,
    )

    # ---- types of care ----
    write_topic(
        "types-of-care/index.html", "types-of-care/index.html",
        "Types of Chiropractic Care in Fort Collins, CO",
        "Visit-to-visit, relief, corrective, and wellness chiropractic care at Advanced Healthcare in Fort Collins. After the exam, you choose the plan that fits your goals.",
        "services/", body_class_of("types-of-care/index.html"),
        [("Home", ""), ("Services", "services/"), ("Types of care", "types-of-care/")],
        "What we do",
        "Types of chiropractic care in Fort Collins",
        "After the exam, you choose the type of care: visit-to-visit, relief, corrective, or, later, wellness. The plan follows your goals.",
        "../assets/images/chiropractic.webp",
        "Chiropractic care at Advanced Healthcare in Fort Collins",
        ["Complimentary consultation", "The type of care is your choice", "In network with BCBS and UHC"],
        TOC_SHORT, TOC_SECTIONS, TOC_FAQS, "Questions about types of care", TOC_RELATED,
        "Choose the care that fits your goals.",
        "Start with a complimentary consultation, or call (970) 472-8333.",
        [
            webpage_node("Types of Chiropractic Care in Fort Collins, CO", "types-of-care/",
                         "Visit-to-visit, relief, corrective, and wellness chiropractic care at Advanced Healthcare in Fort Collins. After the exam, you choose the plan that fits your goals."),
            breadcrumb_node([("Home", ""), ("Services", "services/"), ("Types of care", "types-of-care/")]),
            {"@type": "MedicalProcedure", "name": "Chiropractic types of care",
             "url": f"{PREVIEW}/types-of-care/",
             "procedureType": "Chiropractic care",
             "howPerformed": "In-office care at Advanced Healthcare in Fort Collins, CO.",
             "provider": {"@id": "https://myadvhc.com/#business"}},
            faq_node(TOC_FAQS),
        ],
    )

    # ---- wellness ----
    write_topic(
        "wellness-care/index.html", "wellness-care/index.html",
        "Wellness Chiropractic Care in Fort Collins, CO",
        "Wellness chiropractic care in Fort Collins after relief or corrective care. Visits are every other week, every three weeks, or once a month, to maintain motion and function.",
        "services/", body_class_of("wellness-care/index.html"),
        [("Home", ""), ("Services", "services/"), ("Wellness care", "wellness-care/")],
        "What we do",
        "Wellness care in Fort Collins",
        "Ongoing chiropractic care to maintain the results you have already received, on a schedule that fits you.",
        "../assets/images/wellness.webp",
        "An active person moving comfortably in daily life in Fort Collins",
        ["Complimentary consultation", "Every other week, every three weeks, or once a month", "In network with BCBS and UHC"],
        WELL_SHORT, WELL_SECTIONS, WELL_FAQS, "Wellness care questions we hear most", WELL_RELATED,
        "Stay well, on your terms.",
        "Book a complimentary consultation, or call (970) 472-8333.",
        [
            webpage_node("Wellness Chiropractic Care in Fort Collins, CO", "wellness-care/",
                         "Wellness chiropractic care in Fort Collins after relief or corrective care. Visits are every other week, every three weeks, or once a month, to maintain motion and function."),
            breadcrumb_node([("Home", ""), ("Services", "services/"), ("Wellness care", "wellness-care/")]),
            {"@type": "MedicalProcedure", "name": "Wellness chiropractic care",
             "url": f"{PREVIEW}/wellness-care/",
             "procedureType": "Chiropractic care",
             "howPerformed": "In-office care at Advanced Healthcare in Fort Collins, CO.",
             "provider": {"@id": "https://myadvhc.com/#business"}},
            faq_node(WELL_FAQS),
        ],
        extra_before_faq=WELL_NOTE,
    )

    # ---- dry needling polish ----
    write_topic(
        "dry-needling/index.html", "dry-needling/index.html",
        "Dry Needling in Fort Collins, CO",
        "Dry needling at Advanced Healthcare in Fort Collins, used for low back pain, in relief care, and as a once-a-month wellness option some patients choose.",
        "services/", body_class_of("dry-needling/index.html"),
        [("Home", ""), ("Services", "services/"), ("Dry Needling", "dry-needling/")],
        "What we do",
        "Dry needling in Fort Collins, CO",
        "One of the treatments Dr. Irwin uses at Advanced Healthcare, including for low back pain, relief care, and as a once-a-month wellness option some patients choose.",
        "../assets/images/Chiropractic-Fort-Collins-CO-Chiropractic-Adjustment-Room.webp",
        "A treatment room at Advanced Healthcare in Fort Collins",
        ["Complimentary consultation", "In network with BCBS and UHC"],
        DN_SHORT, DN_SECTIONS, DN_FAQS, "Dry needling questions we hear most", DN_RELATED,
        "Ready to talk about whether this fits your care?",
        "Book a complimentary consultation, or call (970) 472-8333.",
        [
            webpage_node("Dry Needling in Fort Collins, CO", "dry-needling/",
                         "Dry needling at Advanced Healthcare in Fort Collins, used for low back pain, in relief care, and as a once-a-month wellness option some patients choose."),
            breadcrumb_node([("Home", ""), ("Services", "services/"), ("Dry Needling", "dry-needling/")]),
            {"@type": "MedicalProcedure", "name": "Dry Needling",
             "url": f"{PREVIEW}/dry-needling/",
             "procedureType": "Chiropractic care",
             "howPerformed": "In-office care at Advanced Healthcare in Fort Collins, CO.",
             "provider": {"@id": "https://myadvhc.com/#business"}},
            faq_node(DN_FAQS),
        ],
    )

    print("topic pages written")

if __name__ == "__main__":
    run()
