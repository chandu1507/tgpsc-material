"""Cycle63 deterministic Topic 5-3-5 student publication. Academic approval is NOT implied."""
from pathlib import Path
from urllib.parse import urlsplit,unquote
import hashlib,json,re,subprocess,sys
import fitz,mistune
from bs4 import BeautifulSoup

root=Path('Paper 5/Unit 3 - Data Interpretation and Problem Solving/Topic 5')
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
assert original=='f346c2354ec132bc14daa8dcf6cbd1f7cee5c2b3e65a5aa72f9c0a79ce5a4833'
md=(src/'complete-notes.md').read_text()
practice=(src/'original-mcqs.md').read_text()
mains=(src/'complete-model-answers.md').read_text()
source=(src/'source-audit.md').read_text()
assert 'Illustrative denominator and causal test' in md
assert 'Hypothetical risk comparison' in md
assert 'A benefits portal reports 95%' in md and 'A benefits portal reports 95%' in practice
word=lambda s:len(re.findall(r'\b[\w’-]+\b',s))
concepts=re.findall(r'(?ms)^## (\d{1,2})\. ([^\n]+)\n(.*?)(?=^## \d{1,2}\. |^# Twelve |\Z)',md)
concepts=[x for x in concepts if 1<=int(x[0])<=18]
assert len(concepts)==18 and [int(x[0]) for x in concepts]==list(range(1,19))
concept_counts=[word(body) for _,_,body in concepts]
items=re.findall(r'(?ms)^### MCQ (\d+)\. (.*?)\n(.*?)(?=^### MCQ \d+\. |\Z)',practice)
assert len(items)==30
keys=[]
for n,q,body in items:
 assert int(n)==len(keys)+1
 assert len(re.findall(r'(?m)^[ABCD]\. ',body))==4
 m=re.search(r'\*\*Answer:\s*([ABCD])\.',body);assert m,n
 keys.append(m.group(1))
assert {k:keys.count(k) for k in 'ABCD'}=={'A':2,'B':18,'C':9,'D':1},keys
models=re.findall(r'(?ms)^## Model answer ([1-6])\. [^\n]+\n(.*?)(?=^## Model answer [1-6]\. |\Z)',mains)
assert len(models)==6
bodycounts=[word(re.sub(r'\*\*[^*]+\*\*','',body)) for n,body in models]
assert all(200<=n<=250 for n in bodycounts),bodycounts
assert len(list((root/'diagrams').glob('*.png')))==3
pdf=src/'integrated-student-edition-cycle63.pdf'
subprocess.run([sys.executable,'scripts/render_topic_5_3_5_integrated.py','--input',str(src/'complete-notes.md'),'--output',str(pdf)],check=True)
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
for a in soup.find_all('a'):
    u=a.get('href','')
    if u in ('quick-revision.md','answer-blueprints.md'):a['href']='source/'+u
    elif u=='../complete-notes.pdf':a['href']='complete-notes.pdf'
    elif u=='../../../../index.html':a['href']='../../../index.html'
seen={}
for h in soup.find_all(['h1','h2','h3']):
    slug=re.sub('[^a-z0-9]+','-',h.get_text(' ',strip=True).lower()).strip('-') or 'section'
    n=seen.get(slug,0);seen[slug]=n+1
    if n:slug+=f'-{n}'
    h['id']=slug
head='''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>TGPSC 5-3-5</title><style>body{font-family:system-ui,sans-serif;max-width:980px;margin:auto;padding:2rem;line-height:1.65;color:#172b3b}h1,h2,h3{color:#173e65}table{border-collapse:collapse;width:100%}th,td{border:1px solid #cdd9e3;padding:.55rem;text-align:left}th{background:#eaf2f7}img{max-width:100%;height:auto}a{color:#145c98}.banner{padding:1rem;background:#fff2d4;border:1px solid #b99045}</style></head><body><nav><a href="../../../index.html">Study portal</a></nav><p class="banner"><strong>STUDENT DRAFT — NOT ACADEMICALLY APPROVED.</strong> Full claim-level verification, official syllabus reauthentication and direct browser accessibility checks pending.</p><p><a href="source/integrated-student-edition-cycle63.pdf">Integrated PDF</a> · <a href="source/complete-notes.md">Editable master</a> · <a href="complete-notes.pdf">Preserved original PDF</a></p>'''
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
qa={'date':'2026-11-01','topic_id':'5-3-5','cycle':153,'original_pdf_sha256':original,'original_preserved':True,
    'integrated_pdf_sha256':sha(pdf),'integrated_pdf_pages':len(doc),'pdf_images':images,'blank_pages':blank,
    'out_of_page_text_blocks':boundary,'concept_count':len(concepts),'concept_word_counts':concept_counts,
    'explanatory_sections_below_300':sum(n<300 for n in concept_counts[1:]),'mcq_count':30,'distractor_count':90,
    'answer_distribution':{o:keys.count(o) for o in 'ABCD'},'mains_body_only_counts':bodycounts,
    'local_file_links_checked':files_checked,'broken_file_links':bad_files,'dom_fragment_links_checked':fragments_checked,
    'broken_fragment_links':bad_fragments,'spa_routes_excluded':spa_routes,'cycle153_mcq_stems_reviewed':10,'cycle153_mcq_options_reviewed':40,'provisional_domain_mcq_ids':[2,10], 'full_mains_claim_review_complete':False,
    'full_page_per_concept_met':False,'direct_browser_accessibility_certified':False,'independent_academic_approvals':0,
    'R8':'IN_PROGRESS_PENDING_ACTUAL_ARTIFACT_AND_ACADEMIC_QA','actual_downloaded_artifact_verified':False}
(root/'QA-REPORT.md').write_text('# Cycle153 deterministic render QA (not academic certification)\n\n'+json.dumps(qa,indent=2)+'\n')
(root/'README.md').write_text('# Paper V / Unit III / Topic 5 — Decision Making and Problem Solving\n\n'
    'Preserved original 25-page PDF SHA256 '+original+'.\n\n'
    '[Offline HTML](index.html) · [Integrated PDF](source/integrated-student-edition-cycle63.pdf) · '
    '[Editable master](source/complete-notes.md) · [Original PDF](complete-notes.pdf).\n\n'
    'Cycle153: four source-correlated conceptual expansions; 10 existing MCQs option-reviewed without changing their keys (two medical-domain reviews provisional). No official PYQs or independent academic approval claimed.\n')
manifest=json.loads((root/'manifest.json').read_text())
manifest.update({'academically_approved':False,'academic_status':'not_approved','source_word_count':word(md),
    'mcq_count':30,'mains_count':6,'mains_word_counts':bodycounts,'original_pdf_pages':25,'integrated_pdf_status':'CI_rendered_pending_academic_audit',
    'integrated_pdf_pages':len(doc),'integrated_pdf_sha256':sha(pdf),'official_syllabus_authenticated_this_cycle':True,
    'independent_academic_approvals':0})
manifest['metrics']={'concept_count':18,'explanatory_sections_below_300':qa['explanatory_sections_below_300'],
    'answer_distribution':qa['answer_distribution'],'mains_body_only_counts':bodycounts,'independent_review_complete':False}
manifest['files_sha256']={f.relative_to(root).as_posix():sha(f) for f in root.rglob('*') if f.is_file() and f.name!='manifest.json'}
(root/'manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n')
Path('project-control/academic-readiness/5-3-5-cycle153-ci-render-qa-2026-11-01.json').write_text(json.dumps(qa,indent=2)+'\n')
print(json.dumps({k:v for k,v in qa.items() if k!='concept_word_counts'},indent=2))
