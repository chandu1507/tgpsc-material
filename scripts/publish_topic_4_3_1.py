from pathlib import Path
import hashlib, json, re, subprocess, sys
from urllib.parse import urlsplit, unquote
import cairosvg, fitz, mistune
from bs4 import BeautifulSoup

root = Path('Paper 4/Unit 3 - Development and Environmental Problems/Topic 1')
src = root/'source'
cp = json.loads(Path('project-control/PRODUCTION-CHECKPOINT.json').read_text())
ix = json.loads(Path('project-control/ACADEMIC_READINESS_75_TOPIC_STATUS_INDEX.json').read_text())
assert cp['total_topics'] == ix['total_topics'] == len(cp['topics']) == 75
assert len({t['id'] for t in cp['topics']}) == 75
assert len(ix['paths']) == len(set(ix['paths'])) == 75
assert len(list(Path('project-control/academic-readiness').glob('[2-6]-[1-3]-[1-5].json'))) == 75
counts = {s:sum(t['readiness_status']==s for t in cp['topics']) for s in ['IN_PROGRESS','ASSESSED_REBUILD_REQUIRED','NOT_ASSESSED']}
assert counts == {'IN_PROGRESS':7,'ASSESSED_REBUILD_REQUIRED':26,'NOT_ASSESSED':42}, counts
assert cp['academically_approved'] == ix['independently_academically_approved_count'] == 0
assert all((Path(t['path'])/'complete-notes.pdf').is_file() for t in cp['topics'])
original = hashlib.sha256((root/'complete-notes.pdf').read_bytes()).hexdigest()
assert original == 'd603a819b43cba8f322a3e5afe81c98e48f4bae439c79ab05fd8c08295be6260', original

parts = ['syllabus-and-summary.md','quick-revision.md','detailed-notes.md','visual-learning.md','original-mcqs.md','answer-blueprints.md','mains-model-answers.md','verified-pyqs.md','sources-and-audit.md']
md = '\n\n---\n\n'.join((src/n).read_text().strip() for n in parts)+'\n'
assert (src/'complete-notes.md').read_text() == md, 'Canonical master out of sync with components'
concepts = re.split(r'(?m)^## \d+\. ', (src/'detailed-notes.md').read_text())[1:]
concept_words = [len(re.findall(r"\b[\w]+(?:[-'][\w]+)*\b", c)) for c in concepts]
assert len(concepts) == 17 and min(concept_words) >= 300, concept_words
mcq = (src/'original-mcqs.md').read_text()
assert len(re.findall(r'(?m)^\*\*Q\d+\.',mcq)) == 30
assert len(re.findall(r'(?m)^\*\*Answer: [ABCD]\.\*\*',mcq)) == 30
blocks = re.split(r'(?m)(?=^\\*\\*Q\\d+\\.\\*\\*)', mcq)
blocks = [b for b in blocks if re.match(r'^\\*\\*Q\\d+\\.\\*\\*', b)]
assert len(blocks) == 30, len(blocks)
for n, block in enumerate(blocks, 1):
    assert block.startswith(f'**Q{n}.**'), n
    assert all(re.search(rf'(?m)^{a}\\. ', block) for a in 'ABCD'), n
    assert re.search(r'\\*\\*Answer: [ABCD]\\.\\*\\*', block), n
mains = (src/'mains-model-answers.md').read_text()
answer_bodies = re.split(r'(?m)^## Model Answer \d+\..*$', mains)[1:]
assert len(answer_bodies)==6
body_counts = []
for body in answer_bodies:
    body = re.sub(r'\*\*[^*]+\*\*','',body)
    body = '\n'.join(x for x in body.splitlines() if not x.startswith('#'))
    body_counts.append(len(re.findall(r"\b[\w]+(?:[-'][\w]+)*\b",body)))
assert min(body_counts) >= 200, body_counts
assert '## 17. Worked laboratory:' in md
assert 'not official' in md.lower() and 'not independently' in md.lower()

svg = root/'visuals/cumulative-load-laboratory.svg'
png = root/'visuals/cumulative-load-laboratory.png'
assert svg.exists()
cairosvg.svg2png(url=str(svg),write_to=str(png),output_width=920,output_height=320)
pdf = src/'integrated-student-edition-cycle45.pdf'
subprocess.run([sys.executable,'scripts/render_topic_4_3_1_integrated.py','--input',str(src/'complete-notes.md'),'--output',str(pdf)],check=True)
doc = fitz.open(pdf)
blank = [i+1 for i,p in enumerate(doc) if len(p.get_text().strip()) < 60]
images = sum(len(p.get_images()) for p in doc)
assert 20 <= len(doc) <= 65 and not blank and images >= 4,(len(doc),blank,images)
text = '\n'.join(p.get_text() for p in doc)
assert '300 kg/day' in text and '180 kg/day' in text
boundary = []
for i,p in enumerate(doc):
    for block in p.get_text('dict')['blocks']:
        if block['type'] == 0:
            x0,y0,x1,y1=block['bbox']
            if x0<8 or y0<0 or x1>p.rect.width-8 or y1>p.rect.height-2:boundary.append(i+1)
assert not boundary,boundary

old = BeautifulSoup((root/'index.html').read_text(),'html.parser')
body = old.body
assert body is not None
nav = body.find('nav',recursive=False)
if nav is not None:nav.extract()
body.clear()
if nav is not None:body.append(nav)
downloads = old.new_tag('p')
downloads['id']='cycle45-integrated-downloads'
for label,href in [('Cycle45 integrated PDF', 'source/integrated-student-edition-cycle45.pdf'),('Editable Markdown master','source/complete-notes.md'),('Preserved original PDF','complete-notes.pdf')]:
    a=old.new_tag('a',href=href);a.string=label
    downloads.append(a);downloads.append(' · ')
body.append(downloads)
rendered=BeautifulSoup(mistune.create_markdown(plugins=['table','strikethrough'])(md),'html.parser')
for im in rendered.find_all('img'):
    u=im.get('src','')
    if u.startswith('../visuals/'): im['src']='visuals/'+u.split('/')[-1]
seen={}
for h in rendered.find_all(['h1','h2','h3']):
    slug=re.sub('[^a-z0-9]+','-',h.get_text(' ',strip=True).lower()).strip('-') or 'section'
    k=seen.get(slug,0);seen[slug]=k+1
    if k:slug+=f'-{k}'
    h['id']=slug
for node in list(rendered.contents):body.append(node)
(root/'index.html').write_text(str(old))
soup=BeautifulSoup((root/'index.html').read_text(),'html.parser')
ids={x.get('id') for x in soup.find_all(id=True)}
broken_files=[];broken_fragments=[];file_links=0;fragment_links=0;spa_routes=0
for tag in soup.find_all(['a','img','script','link']):
    u=tag.get('href') or tag.get('src')
    if not u:continue
    if '#/paper/' in u:spa_routes+=1;continue
    p=urlsplit(u)
    if p.scheme or u.startswith('//'):continue
    if p.path:
        file_links+=1
        if not (root/unquote(p.path)).resolve().exists():broken_files.append(u)
    if p.fragment:
        fragment_links+=1
        if unquote(p.fragment) not in ids:broken_fragments.append(u)
assert not broken_files and not broken_fragments,(broken_files,broken_fragments)

pdf_sha=hashlib.sha256(pdf.read_bytes()).hexdigest()
readme = f"""# Paper IV / Unit III / Topic 1 — Environment vs Development

Original 27-page complete-notes.pdf preserved (SHA256 {original}).
Cycle45 source/complete-notes.md, offline index.html and source/integrated-student-edition-cycle45.pdf synchronized through GitHub Actions.
17 explanatory concepts >=300 words, 30 original practice MCQs (Q14/Q23/Q29 revised), six 200+ body-word mains answers, three inherited diagrams and one original quantitative load diagram.
The load example is hypothetical, not a Telangana government pollution statistic.
No official PYQs authenticated. R1–R8 incomplete; no independent academic approval.
"""
(root/'README.md').write_text(readme)
qa = {'date':'2026-10-28','topic':'4-3-1','cycle':45,'original_pdf_sha256':original,'original_preserved':True,
      'integrated_pdf_sha256':pdf_sha,'integrated_pdf_pages':len(doc),'pdf_images':images,
      'blank_pages':blank,'text_boundary_violations':boundary,'concept_count':len(concepts),
      'min_concept_words':min(concept_words),'original_mcqs':30,'mains_body_counts':body_counts,
      'html_file_links_checked':file_links,'broken_files':broken_files,
      'html_fragment_links_checked':fragment_links,'broken_fragments':broken_fragments,
      'spa_routes_excluded':spa_routes,'source_checks':'bounded author-side only',
      'independent_academic_approvals':0,'R8':'IN_PROGRESS_NOT_PASS',
      'actual_downloaded_post_edit_artifact_qa':False,'browser_accessibility_certified':False}
(root/'QA-REPORT.md').write_text('# Cycle45 GitHub CI render QA\n\n'+json.dumps(qa,indent=2)+'\n')
manifest=json.loads((root/'manifest.json').read_text())
manifest['detailed_sections']=17
manifest['diagram_count']=4
manifest['original_mcqs']=30
manifest['integrated_pdf_pages']=len(doc)
manifest['integrated_pdf_sha256']=pdf_sha
manifest['integrated_pdf_status']='CI_rendered_independent_academic_audit_pending'
manifest['academic_approval']='not_approved'
files=manifest.get('files',{})
for f in root.rglob('*'):
    if f.is_file() and f.name != 'manifest.json':
        rel=f.relative_to(root).as_posix()
        files[rel]={'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'bytes':f.stat().st_size}
manifest['files']=files
(root/'manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n')
Path('project-control/academic-readiness/4-3-1-cycle45-ci-render-qa-2026-10-28.json').write_text(json.dumps(qa,indent=2)+'\n')
print(json.dumps(qa,indent=2))
