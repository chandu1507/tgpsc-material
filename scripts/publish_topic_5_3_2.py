"""Cycle60 deterministic Topic 5-3-2 publication. Not an academic approval."""
from pathlib import Path
from urllib.parse import urlsplit,unquote
import hashlib,json,re,subprocess,sys
import fitz,mistune
from bs4 import BeautifulSoup

root=Path('Paper 5/Unit 3 - Data Interpretation and Problem Solving/Topic 2')
src=root/'source'
cp=json.loads(Path('project-control/PRODUCTION-CHECKPOINT.json').read_text())
ix=json.loads(Path('project-control/ACADEMIC_READINESS_75_TOPIC_STATUS_INDEX.json').read_text())
assert cp['total_topics']==ix['total_topics']==len(cp['topics'])==75
assert len({t['id'] for t in cp['topics']})==75
assert len(ix['paths'])==len(set(ix['paths']))==75
assert len(list(Path('project-control/academic-readiness').glob('[2-6]-[1-3]-[1-5].json')))==75
assert {t['id'] for t in cp['topics'] if t['readiness_status']=='ASSESSED_REBUILD_REQUIRED'}==set(ix['assessed_rebuild_required'])
assert ix['not_assessed_count']==sum(t['readiness_status']=='NOT_ASSESSED' for t in cp['topics'])
assert cp['academically_approved']==ix['independently_academically_approved_count']==0
assert all((Path(t['path'])/'complete-notes.pdf').is_file() for t in cp['topics'])
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
original=sha(root/'complete-notes.pdf')
assert original=='3de54ec5e1cca90b6d5ddce1ed290ab8f6ec90042b56e3aaff382bd139eb71d5'
md=(src/'complete-notes.md').read_text()
for name in ('core.md','original-mcqs.md','mains-model-answers.md'):
    assert (src/name).read_text().strip() in md,name
assert 'Hospital B treats 10 low-risk patients with 10 recoveries (100%)' in md
assert 'strictly higher observed recovery rate in both risk strata' in md
assert '### MCQ 30. In a hypothetical hospital comparison' in md
word=lambda s:len(re.findall(r'\b[\w’-]+\b',s))
concepts=re.findall(r'(?ms)^## (\d+)\. ([^\n]+)\n(.*?)(?=^## \d+\.|\Z)',(src/'core.md').read_text())
assert len(concepts)==18
assert min(word(body) for _,_,body in concepts)>=300
mcqs=(src/'original-mcqs.md').read_text()
items=re.findall(r'(?ms)^### MCQ (\d+)\. (.*?)(?=^### MCQ \d+\.|\Z)',mcqs)
assert len(items)==30
keys=[]
for n,body in items:
    assert int(n)==len(keys)+1
    assert all('**'+o+'.**' in body for o in 'ABCD')
    m=re.search(r'\*\*Answer:\*\*\s*([ABCD])',body);assert m,n
    keys.append(m.group(1))
assert {o:keys.count(o) for o in 'ABCD'}=={'A':2,'B':15,'C':12,'D':1}
mains=(src/'mains-model-answers.md').read_text()
models=re.findall(r'(?ms)^### Model answer (\d+):[^\n]*\n(.*?)(?=^### Model answer \d+:|\Z)',mains)
assert len(models)==6
bodycounts=[]
for n,body in models:
    body=re.sub(r'(?m)^#{1,6}\s+[^\n]*\n','',body)
    body=re.sub(r'(?mi)^\s*\*\*[^\n]*word count[^\n]*','',body)
    bodycounts.append(word(body))
assert all(200<=n<=250 for n in bodycounts),bodycounts
assert len(list((root/'diagrams').glob('*.png')))==3
pdf=src/'integrated-student-edition-cycle60.pdf'
subprocess.run([sys.executable,'scripts/render_topic_5_3_2_integrated.py','--input',str(src/'complete-notes.md'),'--output',str(pdf)],check=True)
doc=fitz.open(pdf)
blank=[i+1 for i,p in enumerate(doc) if len(p.get_text().strip())<60]
images=sum(len(p.get_images()) for p in doc)
boundary=[]
for i,p in enumerate(doc):
    for block in p.get_text('blocks'):
        x0,y0,x1,y1=block[:4]
        if x0<-1 or y0<-1 or x1>p.rect.width+1 or y1>p.rect.height+1:boundary.append(i+1)
assert 18<=len(doc)<=45 and not blank and images>=3 and not boundary
html=mistune.create_markdown(plugins=['table','strikethrough'])(md)
soup=BeautifulSoup(html,'html.parser')
for img in soup.find_all('img'):
    u=img.get('src','')
    if u.startswith('../diagrams/'):img['src']='diagrams/'+u.rsplit('/',1)[-1]
seen={}
for h in soup.find_all(['h1','h2','h3']):
    slug=re.sub('[^a-z0-9]+','-',h.get_text(' ',strip=True).lower()).strip('-') or 'section'
    n=seen.get(slug,0);seen[slug]=n+1
    if n:slug+=f'-{n}'
    h['id']=slug
head='''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>TGPSC 5-3-2</title><style>body{font-family:system-ui,sans-serif;max-width:980px;margin:auto;padding:2rem;line-height:1.65;color:#172b3b}h1,h2,h3{color:#173e65}table{border-collapse:collapse;width:100%}th,td{border:1px solid #cdd9e3;padding:.55rem;text-align:left}th{background:#eaf2f7}img{max-width:100%;height:auto}a{color:#145c98}.banner{padding:1rem;background:#fff2d4;border:1px solid #b99045}</style></head><body><nav><a href="../../../index.html">Study portal</a></nav><p class="banner"><strong>STUDENT DRAFT — NOT ACADEMICALLY APPROVED.</strong> Complete syllabus, mains claims, diagrams and browser accessibility checks pending.</p><p><a href="source/integrated-student-edition-cycle60.pdf">Integrated PDF</a> · <a href="source/complete-notes.md">Editable master</a> · <a href="complete-notes.pdf">Preserved original PDF</a></p>'''
(root/'index.html').write_text(head+str(soup)+'</body></html>')
page=BeautifulSoup((root/'index.html').read_text(),'html.parser')
ids={x.get('id') for x in page.find_all(id=True)}
files_checked=fragments_checked=0;bad_files=[];bad_fragments=[];spa_routes=0
for tag in page.find_all(['a','img','script','link']):
    u=tag.get('href') or tag.get('src')
    if not u:continue
    if '#/' in u:spa_routes+=1;continue
    parsed=urlsplit(u)
    if parsed.scheme or u.startswith('//'):continue
    if parsed.path:
        files_checked+=1
        if not (root/unquote(parsed.path)).resolve().exists():bad_files.append(u)
    if parsed.fragment:
        fragments_checked+=1
        if unquote(parsed.fragment) not in ids:bad_fragments.append(u)
assert not bad_files and not bad_fragments,(bad_files,bad_fragments)
qa={'date':'2026-10-28','topic_id':'5-3-2','cycle':60,'original_pdf_sha256':original,'original_preserved':True,
    'integrated_pdf_sha256':sha(pdf),'integrated_pdf_pages':len(doc),'pdf_images':images,'blank_pages':blank,
    'out_of_page_text_blocks':boundary,'concept_count':len(concepts),'concepts_below_300':0,
    'mcq_count':30,'distractor_count':90,'answer_distribution':{o:keys.count(o) for o in 'ABCD'},
    'mains_body_only_counts':bodycounts,'local_file_links_checked':files_checked,'broken_file_links':bad_files,
    'dom_fragment_links_checked':fragments_checked,'broken_fragment_links':bad_fragments,'spa_routes_excluded':spa_routes,
    'all_30_keys_and_90_distractors_internal_audit':'see project-control/academic-readiness/5-3-2-cycle60-direct-math-and-options-audit-2026-10-28.json',
    'full_mains_claim_review_complete':False,'direct_browser_accessibility_certified':False,
    'independent_academic_approvals':0,'R8':'IN_PROGRESS_NOT_PASS','actual_downloaded_artifact_verified':False}
(root/'QA-REPORT.md').write_text('# Cycle60 deterministic render QA\n\n'+json.dumps(qa,indent=2)+'\n')
(root/'README.md').write_text('# Paper V / Unit III / Topic 2 — Tabular Data, Probability and Reasoning\n\n'
    'Original 22-page PDF preserved (SHA256 '+original+').\n'
    'Cycle60 editable master, offline HTML and integrated PDF synchronized through CI. '
    '18 concepts (all at least 300 words), 30 original explained practice MCQs, six 200–250 body-word mains, three original diagrams. '
    'Strict Simpson reversal example and applied MCQ30 corrected. '
    'All keys and distractors internally recomputed; no named independent expert approval. '
    'Original 2024 commission syllabus not reauthenticated this cycle. R1–R8 not fully passed.\n')
manifest=json.loads((root/'manifest.json').read_text())
manifest.update({'academic_status':'not_approved','manuscript_words':word(md),'original_mcqs':30,
    'mains_word_counts':bodycounts,'integrated_pdf_status':'CI_rendered_pending_academic_audit',
    'integrated_pdf_pages':len(doc),'integrated_pdf_sha256':sha(pdf),
    'official_syllabus_authenticated_this_cycle':False,'independent_academic_approvals':0})
manifest['metrics']={'concept_count':18,'concepts_below_300':0,'answer_distribution':{o:keys.count(o) for o in 'ABCD'},
    'mains_body_only_counts':bodycounts,'simpson_example_strict_reversal':True,'independent_review_complete':False}
manifest['files']={f.relative_to(root).as_posix():sha(f) for f in root.rglob('*') if f.is_file() and f.name!='manifest.json'}
(root/'manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n')
Path('project-control/academic-readiness/5-3-2-cycle60-ci-render-qa-2026-10-28.json').write_text(json.dumps(qa,indent=2)+'\n')
print(json.dumps(qa,indent=2))
