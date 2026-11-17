"""Round 5 check over the built preview (default ./out): internal links and assets resolve, every page
has noindex + the preview banner, no em dashes in visible text, no live forms, no banned terms."""
import pathlib, re, sys, html
OUT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else 'out')
bad = []; pages = sorted(OUT.rglob('index.html'))
for p in pages:
    s = p.read_text(); rel = p.relative_to(OUT)
    if 'name="robots" content="noindex' not in s: bad.append(f'{rel}: no noindex')
    if 'le-preview-banner' not in s: bad.append(f'{rel}: no banner')
    if '\u2014' in s: bad.append(f'{rel}: em dash')
    for t in ('UMR', 'Dry Needling', 'dry needling', 'Same-week', 'TBD', '{{', 'type="submit"'):
        if t in s: bad.append(f'{rel}: contains {t!r}')
    for m in re.finditer(r'<form[^>]*>', s):
        if 'data-preview="inactive"' not in m.group(0): bad.append(f'{rel}: live form')
    for u in re.findall(r'(?:href|src)="([^"]+)"', s) + re.findall(r'url\(([^)]+)\)', s):
        u = html.unescape(u).strip('\'"')
        if re.match(r'(https?:|mailto:|tel:|#|data:|//)', u): continue
        u = u.split('#')[0].split('?')[0]
        if not u: continue
        if u.startswith('/'): bad.append(f'{rel}: root-absolute link {u}'); continue
        t = (p.parent / u).resolve()
        if t.is_dir(): t = t / 'index.html'
        if not t.exists(): bad.append(f'{rel}: broken {u}')
    n = len(re.findall(r"<a[^>]*le-preview-off", s))
    if n: print(f'{rel}: {n} inactive (not-yet-built) link(s)')
print(f'{len(pages)} pages checked'); print('\n'.join(sorted(set(bad))) or 'no problems')
