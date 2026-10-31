from pathlib import Path
import hashlib, json, re, html
from bs4 import BeautifulSoup
import mistune, fitz

root = Path('Paper 5/Unit 1 - Role and Impact of Science and Technology/Topic 3')
src = root / 'source'
master = src / 'integrated-editable-master-cycle139.md'
audit = src / 'cycle139-four-concept-ten-mcq-primary-source-audit.md'
original = root / 'complete-notes.pdf'
outpdf = src / 'integrated-student-edition-cycle139.pdf'
outhtml = root / 'integrated-student-edition-cycle139.html'
manifest = root / 'integrated-cycle139-manifest.json'
qa_path = Path('project-control/academic-readiness/5-1-3-cycle139-ci-render-qa-2026-10-31.json')
cp = json.loads(Path('project-control/PRODUCTION-CHECKPOINT.json').read_text())
ix = json.loads(Path('project-control/ACADEMIC_READINESS_75_TOPIC_STATUS_INDEX.json').read_text())
assert cp['total_topics'] == ix['total_topics'] == len(cp['topics']) == 75
assert len({t['id'] for t in cp['topics']}) == 75
assert len(ix['paths']) == len(set(ix['paths'])) == 75
assert len(list(Path('project-control/academic-readiness').glob('[2-6]-[1-3]-[1-5].json'))) == 75
assert sum(t['readiness_status'] == 'IN_PROGRESS' for t in cp['topics']) == len(ix['pilot_in_progress']) == 7
assert sum(t['readiness_status'] == 'ASSESSED_REBUILD_REQUIRED' for t in cp['topics']) == len(ix['assessed_rebuild_required']) == 68
assert cp['academically_approved'] == ix['independently_academically_approved_count'] == 0
assert all((Path(t['path']) / 'complete-notes.pdf').is_file() for t in cp['topics'])
for t in cp['topics']:
    record = json.loads(Path(t['readiness_gate_file']).read_text())
    assert record['status'] == t['readiness_status'], t['id']
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(original) == 'bc41a053ecb189e99840f74351e65a4d414c4ba4f88f6258cb1e6de39df3b902'
body = master.read_text(encoding='utf-8')
aud = audit.read_text(encoding='utf-8')
assert aud in body, 'Integrated master missing verbatim audit'
assert len(re.findall(r'(?m)^### MCQ \d+\.', body)) == 30
assert len(re.findall(r'(?m)^\*\*Correct answer: [ABCD]\.\*\*', body)) == 30
assert len(re.findall(r'(?m)^## [1-9][0-9]?\. ', body)) == 16
assert len(re.findall(r'(?m)^- \*\*Q\d+ ', aud)) == 10
assert 'not independent examination-key certification' in aud
assert outpdf.is_file()
pdf = fitz.open(outpdf)
pages = len(pdf)
assert pages >= 20
assert not [i+1 for i,p in enumerate(pdf) if len(p.get_text().strip()) < 60]
images = sum(len(p.get_images()) for p in pdf)
assert images >= 3, images
for idx in [0, pages-1]:
    page_text = pdf[idx].get_text()
    assert 'Topic 5-1-3' in page_text and 'Paper V' in page_text
    assert 'Global Environmental Issues' not in page_text
pdf.close()
markup = mistune.create_markdown(plugins=['table'])(body)
soup = BeautifulSoup(markup, 'html.parser')
used = set()
headings = []
for h in soup.select('h1,h2,h3'):
    base = re.sub(r'[^a-z0-9]+', '-', h.get_text(' ', strip=True).lower()).strip('-') or 'section'
    slug = base
    n = 2
    while slug in used:
        slug = f'{base}-{n}'
        n += 1
    used.add(slug)
    h['id'] = slug
    if h.name in ('h2','h3'):
        headings.append((h.get_text(' ', strip=True), slug))
for img in soup.find_all('img'):
    url = img.get('src','')
    assert url.startswith('diagrams/') and (root / url).is_file(), url
toc = '\n'.join(f'<li><a href="#{html.escape(slug)}">{html.escape(title)}</a></li>' for title,slug in headings)
doc = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Topic 5-1-3 — Integrated student edition (Cycle139)</title><style>body{{font:16px/1.65 system-ui,sans-serif;max-width:1000px;margin:auto;padding:2rem;color:#172b40}}nav{{background:#eff6fb;padding:1rem;border-radius:10px}}a{{color:#115e91}}img{{max-width:100%;height:auto}}h2{{margin-top:2.5rem;border-bottom:1px solid #d8e2ec}}li{{margin-bottom:.35rem}}main{{overflow-wrap:anywhere}}@media print{{nav{{display:none}}body{{max-width:none}}}}</style></head><body><header><p><a href="index.html">Original topic page</a> · <a href="source/integrated-student-edition-cycle139.pdf">Integrated PDF</a> · <a href="source/integrated-editable-master-cycle139.md">Editable master</a> · <a href="source/cycle139-four-concept-ten-mcq-primary-source-audit.md">Option audit</a></p></header><nav aria-label="Table of contents"><h2>Contents</h2><ol>{toc}</ol></nav><main>{str(soup)}</main></body></html>'''
outhtml.write_text(doc, encoding='utf-8')
check = BeautifulSoup(doc, 'html.parser')
ids = {x.get('id') for x in check.select('[id]')}
fragment_links = [x.get('href') for x in check.select('a[href^="#"]')]
assert all(x[1:] in ids for x in fragment_links)
for x in check.select('a[href],img[src]'):
    href = x.get('href') or x.get('src')
    if href and not href.startswith(('https://','http://','mailto:','#')):
        assert (root / href.split('#')[0]).is_file(), href
files = [original, master, audit, outpdf, outhtml]
manifest.write_text(json.dumps({'topic':'5-1-3','cycle':139,'source':'source/integrated-editable-master-cycle139.md','pdf':'source/integrated-student-edition-cycle139.pdf','html':'integrated-student-edition-cycle139.html','original_pdf_unchanged':True,'files':{str(p.relative_to(root)):sha(p) for p in files}},indent=2)+'\n')
qa_path.parent.mkdir(parents=True, exist_ok=True)
qa_path.write_text(json.dumps({'cycle':139,'topic':'5-1-3','status':'CI_RENDERED_NOT_INDEPENDENTLY_APPROVED','topic_count':75,'original_pdf_sha256':sha(original),'pdf_pages':pages,'pdf_sha256':sha(outpdf),'html_sha256':sha(outhtml),'master_sha256':sha(master),'audited_mcqs':[10,11,16,17,20,22,23,24,26,29],'author_side_options':40,'html_toc_fragments':len(fragment_links),'broken_html_fragments':0,'approval_count':0,'requires_downloaded_artifact_qa':True},indent=2)+'\n')
print(json.dumps({'pages':pages,'sha256':sha(outpdf),'html_fragments':len(fragment_links),'manifest':str(manifest)}))
