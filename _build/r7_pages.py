from string import Template
from pathlib import Path
from r7_lib import LBP_PARAS, NPE_PARAS, WELL_PARAS
from r7_helpers import (
    pfx, crumbs_html, audio_html, insurance_block, cta_html, faq_html, related_html,
)

TMPL = Path(__file__).parent / "tmpl"

def _fill(name, mapping):
    return Template((TMPL / name).read_text()).safe_substitute(mapping)

LBP_FAQS = [
    ("What happens on the first visit for low back pain?",
     "On your first visit, Dr. Irwin takes a full detailed history: when it started, where it is, and whether it just happened or has been going on for years. From there he does a full ortho-neuro check with complete motion palpation, looking for tight muscles, inflammation, and whether it is a disc injury that needs more testing or something he is comfortable working with day one. The examination normally takes an hour. That is a deeper look than the 10 or 15 minute visits he sees at a lot of clinics in Fort Collins. <a href=\"../new-patients/\">See what a first visit includes</a>."),
    ("Do you take x-rays for back pain?",
     "The clinic has full diagnostic digital x-ray. Dr. Irwin uses it especially for areas of extreme pain and for referrals down into the leg, looking for degenerative change or arthritic conditions that may be leading toward the cause of the back pain."),
    ("How long does low back pain care take?",
     "It depends on your goal. He has said it could be as simple as three or four visits, if that is what you want. If you truly want to get the problem resolved and work on strengthening, it could take upwards of two, three, or four months to truly rehabilitate it back to where it needs to be. Most times care starts with a little bit of frequency. <a href=\"../types-of-care/\">Read about the types of care</a>."),
    ("What kinds of treatment do you use for low back pain?",
     "Alongside the exam and chiropractic care, the clinic uses dry needling, spinal decompression for disc-related injuries or osteoarthritic change (arthritis in the lower part of the back), shockwave therapy, massage therapy, and full passive and active stretching and flexibility programs, worked all the way through full strength and rehabilitation of a dysfunctional low back."),
    ("When should I come in for low back pain?",
     "The best thing you can do, in Dr. Irwin's words, is catch it right when it starts. So many people say it is just going to go away. He encourages you, at the start of lower back pain, to get in right away. That gives the body less of an opportunity to develop compensatory patterns and muscle guarding, things that make treatment take longer and make it harder to recover."),
]

NPE_FAQS = [
    ("How is your new patient exam different?",
     "Dr. Irwin calls the new patient exam the pillar of treatment in the clinic. It is quite a bit more lengthy than most clinics, and also way more in depth. A lot of clinics, in his words, will have a one-page intake form, put you on a table, talk a little about symptoms, adjust you, and send you on your way. That is not how it works here."),
    ("What happens during the exam?",
     "It starts with a complete health history, to get to when the problem potentially started, not just when it started this time, and to iron out the quality of pain, where it is, and if it radiates, plus any surgeries or symptoms you have had over the course of your life. Then there is a full evaluation in the exam room, starting with range of motion and palpation of the body and spine, then motion palpation and muscle testing, and, if needed, full-scale orthopedic and neurological evaluations, to pinpoint the area the problem is coming from before he lays a finger to adjust."),
    ("Do you take x-rays on the first visit?",
     "If the exam shows they are relevant, he will recommend a set or a full set of digital x-rays, so he can truly see what he is pushing into before adjusting. He uses the example of a mechanic: it is one thing to lay hands on the hood and guess, and another to open the hood and evaluate it. X-rays are usually taken, especially when pain is one of the primary drivers of the visit. Films can also show things like anterolisthesis or spondylolisthesis."),
    ("Do you adjust on the first day?",
     "Sometimes yes. After the evaluation, the doctor may choose to adjust on the first day. If it is a complex case, he may spend time going through the films and the exam before adjusting, and set up an appointment for you to come back, review the results, go through the x-rays, and then establish the type of care you want to go through. That return visit is the report of findings."),
    ("What is a report of findings?",
     "When you come back after a more complex first exam, Dr. Irwin reviews the results of the examination, goes through the x-rays that were taken, and then establishes the type of care you want to go through. You choose the path: visit-to-visit care, relief care, or corrective care. <a href=\"../types-of-care/\">Read about the types of care</a>."),
    ("Do I need a referral, and do you take insurance?",
     "No referral is needed to book a first visit. We are in network with BCBS and UHC, and we go over the costs with you before anything begins. Call (970) 472-8333 with questions about your plan. You can also start with a complimentary consultation."),
]

TOC_FAQS = [
    ("Do I have to choose a type of care up front?",
     "No. After the exam, and after the report of findings when one is needed, you establish the type of care you want to go through. In Dr. Irwin's words, at the end of the day it is the patient's choice."),
    ("What is visit-to-visit care?",
     "It is the most cost-effective form of treatment, for people whose sole goal is to get the pain out of the area. He definitely works with people like that. He also describes this as short-term acute pain management."),
    ("What is relief care, and how long does it last?",
     "Relief care is typically anywhere from two to six weeks. A lot of times it includes modalities such as massage therapy, decompression, dry needling, or SoftWave therapy, to try to get symptoms out as fast as possible. The whole goal is increasing range of motion and decreasing muscle guarding, muscle spasm, or muscle pain, to the point where you feel better."),
    ("What is corrective care?",
     "Most patients want more than just symptoms gone. They don't want the symptoms to come back, and they want to be stronger and healthier. Corrective care involves rehabilitating the area with strength-based exercises: endurance-based strength training first, then dynamic strength training, such as picking up weights, moving, bending, and twisting with it. The idea is that the next time you reach down to pick up a laundry basket or a box off the garage floor, your body has the strength to do it without throwing you back into that acute state or that state of pain."),
    ("What happens after relief or corrective care?",
     "A number of patients then choose to move on to wellness care, which is meant to maintain the results of that initial set of care. <a href=\"../wellness-care/\">Read about wellness care</a>."),
    ("Do you take insurance?",
     "No referral is needed to book a first visit. We are in network with BCBS and UHC, and we go over the costs with you before anything begins. Call (970) 472-8333 with questions about your plan."),
]

WELL_FAQS = [
    ("What is wellness care?",
     "It is for patients who, after they have done relief care and/or a full corrective form of care, choose to move on to what Dr. Irwin considers wellness care. It is designed to maintain the results they received through that initial set of care. Its goal is to help maintain good motion and function in an area."),
    ("How often would I come in?",
     "Wellness care is anywhere from every other week adjusting through once a month adjusting in the clinic. So every other week, every three weeks, or one time a month in the office."),
    ("Do I still do the exercises?",
     "Yes. Patients are encouraged to continue with the stretching and flexibility they have been taught, as well as their strength-based rehabilitation, so they can maintain good moving forward."),
    ("Can wellness care include massage or decompression?",
     "A lot of times people will elect to do massages on one of the massage clubs in the clinic, and some patients even elect to do spinal decompression therapy or dry needling once a month just to maintain good healthy function of the muscles."),
    ("Can I stop whenever I want?",
     "Yes. The type of care you do is your choice. Tell us if you want to pause or stop, and we will make a note of where you got to so picking it back up later is easy."),
    ("Do you take insurance for wellness care?",
     "We are in network with BCBS and UHC for care we bill to insurance, and we go over the costs with you before anything begins. Call (970) 472-8333 with questions about your plan. Coverage for ongoing wellness visits varies by plan, so we will be clear about the numbers up front."),
]

def back_pain_main(depth=1):
    pre = pfx(depth)
    return _fill("back-pain.main.html", {
        "pre": pre,
        "crumbs": crumbs_html([("Home", ""), ("Conditions", "conditions/"), ("Back pain", "back-pain/")], depth),
        "audio": audio_html("Low back pain, recorded November 9, 2026 (4 minutes).", f"{pre}assets/audio/low-back-pain.mp3", LBP_PARAS, "November 9, 2026", "4 minutes 3 seconds"),
        "insurance": insurance_block(),
        "cta": cta_html("You do not have to work around it.", "Start with a complimentary consultation. Come as you are, we will take it from there.", depth),
        "faq": faq_html("Back pain questions we hear most", LBP_FAQS, "lbp"),
        "related": related_html("You might also look at", [
            ("New patient exam", "What the first visit and report of findings actually include.", "new-patients/"),
            ("Sciatica &amp; leg pain", "When low back pain refers down the leg.", "sciatica/"),
            ("Types of care", "Visit-to-visit, relief, corrective, and wellness care, in his words.", "types-of-care/"),
        ], depth),
    })

def new_patients_main(depth=1):
    pre = pfx(depth)
    audio_title = "New patient exam, report of findings, and types of care, recorded November 10, 2026 (6 minutes). This memo also feeds the <a href=\"../types-of-care/\">types of care</a> page."
    return _fill("new-patients.main.html", {
        "pre": pre,
        "crumbs": crumbs_html([("Home", ""), ("Services", "services/"), ("New patients", "new-patients/")], depth),
        "audio": audio_html(audio_title, f"{pre}assets/audio/new-patient-exam.mp3", NPE_PARAS, "November 10, 2026", "6 minutes 6 seconds"),
        "insurance": insurance_block(),
        "cta": cta_html("Ready for a real first exam?", "Start with a complimentary consultation, then we will take the time the first visit deserves.", depth),
        "faq": faq_html("New patient questions we hear most", NPE_FAQS, "npe"),
        "related": related_html("You might also look at", [
            ("Types of care", "Visit-to-visit, relief, corrective, and wellness care, in his words.", "types-of-care/"),
            ("Back pain", "How the first exam works when lower back pain is the reason you come in.", "back-pain/"),
            ("New Patient Special", "Book a first visit or a complimentary consultation.", "special/"),
        ], depth),
    })

def types_of_care_main(depth=1):
    pre = pfx(depth)
    audio_title = "New patient exam, report of findings, and types of care, recorded November 10, 2026 (6 minutes). The same memo also feeds the <a href=\"../new-patients/\">new patient exam</a> page."
    return _fill("types-of-care.main.html", {
        "pre": pre,
        "crumbs": crumbs_html([("Home", ""), ("Services", "services/"), ("Types of care", "types-of-care/")], depth),
        "audio": audio_html(audio_title, f"{pre}assets/audio/new-patient-exam.mp3", NPE_PARAS, "November 10, 2026", "6 minutes 6 seconds"),
        "insurance": insurance_block(),
        "cta": cta_html("Choose the care that fits your goals.", "Start with a complimentary consultation and a thorough first exam.", depth),
        "faq": faq_html("Questions about types of care", TOC_FAQS, "toc"),
        "related": related_html("You might also look at", [
            ("New patient exam", "The exam and report of findings that come before you choose a type of care.", "new-patients/"),
            ("Wellness care", "How some patients maintain results after relief or corrective care.", "wellness-care/"),
            ("Physical rehabilitation", "Strength and movement work that often goes with corrective care.", "physical-rehabilitation/"),
        ], depth),
    })

def wellness_main(depth=1):
    pre = pfx(depth)
    return _fill("wellness-care.main.html", {
        "pre": pre,
        "crumbs": crumbs_html([("Home", ""), ("Services", "services/"), ("Wellness care", "wellness-care/")], depth),
        "audio": audio_html("Wellness care, recorded November 10, 2026 (about 1 and a half minutes).", f"{pre}assets/audio/wellness-care.mp3", WELL_PARAS, "November 10, 2026", "1 minute 34 seconds"),
        "insurance": insurance_block(),
        "cta": cta_html("Stay well, on your terms.", "If you want to maintain the results of your initial care, we will set a pace that fits.", depth, "Book a visit"),
        "faq": faq_html("Wellness care questions we hear most", WELL_FAQS, "well"),
        "related": related_html("You might also look at", [
            ("Types of care", "How wellness care sits after visit-to-visit, relief, or corrective care.", "types-of-care/"),
            ("Back pain", "The complaint that most often starts people down this path.", "back-pain/"),
            ("Massage therapy", "Some wellness patients elect massage through the clinic's massage clubs.", "massage-therapy/"),
        ], depth),
    })
