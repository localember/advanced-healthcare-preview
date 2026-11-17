"""Advanced Healthcare preview: full build (round 5, 2026-11-17).

  python3 _build/build.py            # from the preview repo root, with localember/localember at $LE (default /workspace/le)

Step 1 runs Harbor's own emitter (tools/static-build/designs/harbor/emit.py) on
_build/advanced-healthcare.record.json into ./site, with four per-client adjustments
that Harbor has no record field for yet (Build should carry them as record options, not Harbor edits):
  a. payment: Harbor applies record.payment only when model == "self_pay". This practice is an
     insurance practice (BCBS and UHC in network), so the record's cost_p / cost_items / cost_note /
     faq_answer are applied to every catalog cost section and payment FAQ here too.
  b. conditions: Harbor ships the whole fleet condition set. myadvhc.com lists six, so catalog
     condition pages are limited to record.conditions_helped (back-pain, neck-pain, headaches,
     sciatica, disc-injury; wellness-care is a service page).
  c. citation blocks: emit.py drops a citation's "stat" field, so the evidence box read
     "studies have looked at..." with the number missing. The stat is put back in front of the text
     (joined by U+2063; post.py/round5.py turns it into a bold lead line).
  d. copy pack: "Same-week visits for new patients" is not a claim this practice has made. Swapped for
     the record's real offer (complimentary consultation).
Step 2 runs _build/post.py (preview banner, noindex, inactive forms, gold CTAs, links, hero video,
round 4 images, round 5 changes) into ./out.
"""
import importlib.util, json, os, pathlib, sys
HERE = pathlib.Path(__file__).resolve().parent
LE = pathlib.Path(os.environ.get('LE', '/workspace/le'))
REC = HERE / 'advanced-healthcare.record.json'
spec = importlib.util.spec_from_file_location('harbor_emit', LE / 'tools/static-build/designs/harbor/emit.py')
em = importlib.util.module_from_spec(spec); spec.loader.exec_module(em)
record = json.loads(REC.read_text())

# a. payment for an insurance practice
_pay = record.get('payment') or {}
em.payment = lambda c: _pay if all(_pay.get(k) for k in ('faq_answer', 'cost_p', 'cost_items', 'cost_note')) else None

# b + c. catalog page set and citation stats
_keep_cond = {x['slug'] for x in record.get('conditions_helped') or []}
_orig_entries = em.catalog_entries
def catalog_entries(c):
    out = []
    for entry, kind in _orig_entries(c):
        if kind == 'condition' and entry.get('slug') not in _keep_cond:
            continue
        for b in entry.get('blocks') or []:
            if b.get('type') == 'citation' and b.get('stat') and not (b.get('text') or '').startswith(b['stat']):
                b['text'] = f"{b['stat']}\u2063{b['text']}"
        out.append((_swap(entry), kind))
    return out
em.catalog_entries = catalog_entries

# d. copy pack and catalog claims
SWAPS = {
    'Same-week visits for new patients. We will take it from there.': 'Start with a complimentary consultation. We will take it from there.',
    'Same-week visits for new patients. Come as you are, we will take it from there.': 'Start with a complimentary consultation. Come as you are, we will take it from there.',
    'Ask us directly. Same-week visits for new patients, and a straight answer either way.': 'Ask us directly. Start with a complimentary consultation, and a straight answer either way.',
    '⏱ Same-week new-patient visits': '✅ Complimentary consultation for new patients',
}
def _swap(obj):
    s = json.dumps(obj, ensure_ascii=False)
    for a, b in SWAPS.items():
        s = s.replace(json.dumps(a, ensure_ascii=False)[1:-1], json.dumps(b, ensure_ascii=False)[1:-1])
    return json.loads(s)
_orig_pack = em.load_pack
def load_pack():
    return _swap(_orig_pack())
em.load_pack = load_pack

if __name__ == '__main__':
    sys.argv = ['emit.py', '--record', str(REC), '--out', 'site/index.html']
    em.main()
    sys.path.insert(0, str(HERE))
    os.environ.setdefault('AHC_REPO', str(HERE.parent))
    import runpy; runpy.run_path(str(HERE / 'post.py'), run_name='__main__')
