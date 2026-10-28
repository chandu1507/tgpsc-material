"""Cycle62 deterministic Topic 5-3-4 student publication. Academic approval is NOT implied."""
from pathlib import Path
from urllib.parse import urlsplit,unquote
import hashlib,json,re,subprocess,sys
import fitz,mistune
from bs4 import BeautifulSoup

root=Path('Paper 5/Unit 3 - Data Interpretation and Problem Solving/Topic 4')
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
assert original=='564061e2c2e121aa0184c7bb465da5889bef10c7b45773aecc8ba70194bf2fc8'
md=(src/'complete-notes.md').read_text()
practice=(src/'original-practice.md').read_text()
mains=(src/'complete-model-answers.md').read_text()
source=(src/'source-audit.md').read_text()
assert 'When is their first reunion after departure?' in md and 'When is their first reunion after departure?' in practice
assert 'worker-hours?' in md and 'worker-hours?' in practice
assert 'previously mismatched URL' in md and 'previously mismatched URL' in source
assert 'Graph interpretation under missing observations' in md
assert 'if an inspection rejects 18 of 180 claimed units' in md and 'if an inspection rejects 18 of 180 claimed units' in mains
word=lambda s:len(re.findall(r'\b[\w’-]+\b',s))
concepts=re.findall(r'(?ms)^## (\d{1,2})\. ([^\n]+)\n(.*?)(?=^## \d{1,2}\.|\Z)',md)
concepts=[x for x in concepts if 1<=int(x[0])<=18]
assert len(concepts)==18 and [int(x[0]) for x in concepts]==list(range(1,19))
concept_counts=[word(body) for _,_,body in concepts]
assert min(concept_counts[1:])>=300,concept_counts
items=re.findall(r'(?ms)^\*\*MCQ (\d{2})\. (.*?)\*\*\n\n(.*?)(?=^\*\*MCQ \d{2}\.|\Z)',practice)
assert len(items)==30
keys=[]
for n,q,body in items:
 assert int(n)==len(keys)+1
 assert len(re.findall(r'(?m)^[ABCD]\. ',body))==4
 m=re.search(r'\*\*Answer:\s*([ABCD])\.',body);assert m,n
 keys.append(m.group(1))
assert {k:keys.count(k) for k in 'ABCD'}=={'A':2,'B':14,'C':13,'D':1},keys
models=re.findall(r'(?ms)^### M([1-6])\. [^\n]+\n(.*?)(?=^### M[1-6]\. |\Z)',mains)
assert len(models)==6
bodycounts=[word(re.sub(r'\*\*[^*]+\*\*','',body)) for n,body in models]
assert all(200<=n<=250 for n in bodycounts),bodycounts
assert len(list((root/'diagrams').glob('*.png')))==3
pdf=src/'integrated-student-edition-cycle62.pdf'
subprocess.run([sys.executable,'scripts/render_topic_5_3_3_integrated.py','--input',str(src/'complete-notes.md'),'--output',str(pdf)],check=True)
doc=fitz.open(pdf)
blank=[i+1 for i,p in enumerate(doc) if len(p.get_text().strip())<60]
images=sum(len(p.get_images()) for p in doc)
boundary=[]
for i,p in enumerate(doc):
    for block in p.get_text('blocks'):
        x0,y0,x1,y1=block[:4]
        if x0<-1 or y0<-1 or x1>p.rect.width+1 or y1>p.rect.height+1:boundary.append(i+1)
assert 18<=len(doc)<=50 and not blank and images>=3 and not boundary,(len(doc),blank,images,boundary)
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
head='''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>TGPSC 5-3-4</title><style>body{font-family:system-ui,sans-serif;max-width:980px;margin:auto;padding:2rem;line-height:1.65;color:#172b3b}h1,h2,h3{color:#173e65}table{border-collapse:collapse;width:100%}th,td{border:1px solid #cdd9e3;padding:.55rem;text-align:left}th{background:#eaf2f7}img{max-width:100%;height:auto}a{color:#145c98}.banner{padding:1rem;background:#fff2d4;border:1px solid #b99045}</style></head><body><nav><a href="../../../index.html">Study portal</a></nav><p class="banner"><strong>STUDENT DRAFT — NOT ACADEMICALLY APPROVED.</strong> Full claim-level verification, official syllabus reauthentication and direct browser accessibility checks pending.</p><p><a href="source/integrated-student-edition-cycle62.pdf">Integrated PDF</a> · <a href="source/complete-notes.md">Editable master</a> · <a href="complete-notes.pdf">Preserved original PDF</a></p>'''
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
qa={'date':'2026-10-28','topic_id':'5-3-4','cycle':62,'original_pdf_sha256':original,'original_preserved':True,
    'integrated_pdf_sha256':sha(pdf),'integrated_pdf_pages':len(doc),'pdf_images':images,'blank_pages':blank,
    'out_of_page_text_blocks':boundary,'concept_count':len(concepts),'concept_word_counts':concept_counts,'section_1_is_syllabus_map':True,'sections_2_to_18_below_300':0,
    'mcq_count':30,'distractor_count':90,'answer_distribution':{o:keys.count(o) for o in 'ABCD'},
    'mains_body_only_counts':bodycounts,'local_file_links_checked':files_checked,'broken_file_links':bad_files,
    'dom_fragment_links_checked':fragments_checked,'broken_fragment_links':bad_fragments,'spa_routes_excluded':spa_routes,
    'mcq09_and_mcq20_ambiguities_corrected':True,'all_30_keys_and_90_distractors_internally_checked':True,
    'full_mains_claim_review_complete':False,'full_page_per_concept_met':False,'direct_browser_accessibility_certified':False,
    'independent_academic_approvals':0,'R8':'IN_PROGRESS_NOT_PASS','actual_downloaded_artifact_verified':False}
(root/'QA-REPORT.md').write_text('# Cycle62 deterministic render QA\n\n'+json.dumps(qa,indent=2)+'\n')
(root/'README.md').write_text('# Paper V / Unit III / Topic 4 — Time, Work, Speed, Interest and Reasoning\n\n'
    'Original 20-page PDF preserved (SHA256 '+original+').\n'
    'Cycle62 editable master, offline HTML and integrated PDF synchronized through CI. '
    'MCQ09 worker-hours and MCQ20 t=0 ambiguities clarified; misleading 2025 MoSPI link corrected; '
    'new graph sampling and speed-time worked examples; M1 body count repaired. '
    '30 original practice MCQs, six 200–250 body-word mains, three original diagrams. '
    'Internal key checks are not named independent academic review. Full-page concept density, mains claims, diagrams, syllabus and browser QA pending.\n')
manifest=json.loads((root/'manifest.json').read_text())
manifest.update({'academically_approved':False,'academic_status':'not_approved','source_word_count':word(md),
    'mcq_count':30,'mains_count':6,'integrated_pdf_status':'CI_rendered_pending_academic_audit',
    'integrated_pdf_pages':len(doc),'integrated_pdf_sha256':sha(pdf),
    'official_syllabus_authenticated_this_cycle':False,'independent_academic_approvals':0})
manifest['metrics']={'concept_count':18,'section_1_is_syllabus_map':True,'sections_2_to_18_below_300':0,'answer_distribution':{o:keys.count(o) for o in 'ABCD'},
    'mains_body_only_counts':bodycounts,'mcq09_and_mcq20_ambiguities_corrected':True,'independent_review_complete':False}
manifest['files_sha256']={f.relative_to(root).as_posix():sha(f) for f in root.rglob('*') if f.is_file() and f.name!='manifest.json'}
(root/'manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n')
Path('project-control/academic-readiness/5-3-4-cycle62-ci-render-qa-2026-10-28.json').write_text(json.dumps(qa,indent=2)+'\n')
print(json.dumps({k:v for k,v in qa.items() if k!='concept_word_counts'},indent=2))
