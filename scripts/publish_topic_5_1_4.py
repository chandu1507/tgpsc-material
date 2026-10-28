from pathlib import Path
import hashlib, json, re, subprocess, sys
from urllib.parse import urlsplit, unquote
import fitz, mistune
from bs4 import BeautifulSoup

root=Path('Paper 5/Unit 1 - Role and Impact of Science and Technology/Topic 4')
src=root/'source'
cp=json.loads(Path('project-control/PRODUCTION-CHECKPOINT.json').read_text())
ix=json.loads(Path('project-control/ACADEMIC_READINESS_75_TOPIC_STATUS_INDEX.json').read_text())
assert cp['total_topics']==ix['total_topics']==len(cp['topics'])==75
assert len({t['id'] for t in cp['topics']})==75
assert len(ix['paths'])==len(set(ix['paths']))==75
assert len(list(Path('project-control/academic-readiness').glob('[2-6]-[1-3]-[1-5].json')))==75
counts={s:sum(t['readiness_status']==s for t in cp['topics']) for s in ['IN_PROGRESS','ASSESSED_REBUILD_REQUIRED','NOT_ASSESSED']}
assert counts=={'IN_PROGRESS':7,'ASSESSED_REBUILD_REQUIRED':34,'NOT_ASSESSED':34},counts
assert len(ix['assessed_rebuild_required'])==34 and ix['not_assessed_count']==34
assert set(ix['assessed_rebuild_required'])=={t['id'] for t in cp['topics'] if t['readiness_status']=='ASSESSED_REBUILD_REQUIRED'}
assert cp['academically_approved']==ix['independently_academically_approved_count']==0
assert all((Path(t['path'])/'complete-notes.pdf').is_file() for t in cp['topics'])
original=hashlib.sha256((root/'complete-notes.pdf').read_bytes()).hexdigest()
assert original=='767cc8cad529ab3599032a8f17ff91c84be2271f958e2ea4069a3deda78c9524',original

md=(src/'complete-notes.md').read_text()
mains=(src/'mains-model-answers.md').read_text().strip()
sources=(src/'sources-and-audit.md').read_text().strip()
assert mains in md and sources in md
assert 'Cycle 52 bounded direct-source correspondence' in md
concepts=re.findall(r'(?ms)^### Section (\d+)\. ([^\n]+)\n(.*?)(?=^### Section \d+\.|^## |\Z)',md)
assert len(concepts)==16,len(concepts)
word=lambda s:len(re.findall(r"\b[\w’-]+\b",s))
concept_words=[word(body) for _,_,body in concepts]
assert min(concept_words)>=300,concept_words
mcq_blocks=re.findall(r'(?ms)^### MCQ (\d+)\. (.*?)(?=^### MCQ \d+\.|^## |\Z)',md)
assert len(mcq_blocks)==30
answers=[]
for n,block in mcq_blocks:
    assert int(n)==len(answers)+1
    for opt in 'ABCD':assert re.search(r'(?m)^'+opt+r'\. ',block),(n,opt)
    ans=re.search(r'\*\*Correct answer: ([ABCD])\.',block)
    assert ans,n
    answers.append(ans.group(1))
assert {k:answers.count(k) for k in 'ABCD'}=={'A':9,'B':18,'C':2,'D':1}
mains_text=md.split('## Six original mains practice questions and complete model answers',1)[1].split('## Dated primary-source register and academic audit',1)[0]
models=re.findall(r'(?ms)^### Model (\d+)\. ([^\n]+)\n(.*?)(?=^### Model \d+\.|^## |\Z)',mains_text)
assert len(models)==6
body_counts=[]
for n,q,body in models:
    body=re.sub(r'\*\*Model-answer body-only word count:\*\*.*','',body)
    body=re.sub(r'\*\*[^*]+\.\*\*','',body)
    body_counts.append(word(body))
assert body_counts==[218,202,212,204,223,208],body_counts
assert len(list((root/'diagrams').glob('*.png')))==3

pdf=src/'integrated-student-edition-cycle52.pdf'
subprocess.run([sys.executable,'scripts/render_topic_5_1_4_integrated.py','--input',str(src/'complete-notes.md'),'--output',str(pdf)],check=True)
doc=fitz.open(pdf)
blank=[i+1 for i,p in enumerate(doc) if len(p.get_text().strip())<60]
images=sum(len(p.get_images()) for p in doc)
boundary=[]
for i,p in enumerate(doc):
    for block in p.get_text('blocks'):
        x0,y0,x1,y1=block[:4]
        if x0<-1 or y0<-1 or x1>p.rect.width+1 or y1>p.rect.height+1:boundary.append(i+1)
assert 20<=len(doc)<=45 and not blank and images>=3 and not boundary,(len(doc),blank,images,boundary)

body=mistune.create_markdown(plugins=['table','strikethrough'])(md)
rendered=BeautifulSoup(body,'html.parser')
for im in rendered.find_all('img'):
    u=im.get('src','')
    if u.startswith('../diagrams/'):im['src']='diagrams/'+u.split('/')[-1]
seen={}
for h in rendered.find_all(['h1','h2','h3']):
    slug=re.sub('[^a-z0-9]+','-',h.get_text(' ',strip=True).lower()).strip('-') or 'section'
    n=seen.get(slug,0);seen[slug]=n+1
    if n:slug+=f'-{n}'
    h['id']=slug
head='''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>TGPSC 5-1-4</title><style>body{font-family:system-ui,sans-serif;max-width:980px;margin:auto;padding:2rem;line-height:1.65;color:#172b3b}h1,h2,h3{color:#173e65}table{border-collapse:collapse;width:100%}th,td{border:1px solid #cdd9e3;padding:.55rem;text-align:left}th{background:#eaf2f7}img{max-width:100%;height:auto}a{color:#145c98}.banner{padding:1rem;background:#fff2d4;border:1px solid #b99045}</style></head><body><nav><a href="../../../index.html">Study portal</a></nav><p class="banner"><strong>STUDENT DRAFT — NOT ACADEMICALLY APPROVED.</strong> Complete independent source, MCQ, diagram and browser-accessibility checks pending.</p><p><a href="source/integrated-student-edition-cycle52.pdf">Integrated PDF</a> · <a href="source/complete-notes.md">Editable master</a> · <a href="complete-notes.pdf">Preserved original PDF</a></p>'''
(root/'index.html').write_text(head+str(rendered)+'</body></html>')
soup=BeautifulSoup((root/'index.html').read_text(),'html.parser')
ids={x.get('id') for x in soup.find_all(id=True)}
bad_files=[];bad_fragments=[];file_links=0;fragment_links=0;spa_routes=0
for tag in soup.find_all(['a','img','script','link']):
    u=tag.get('href') or tag.get('src')
    if not u:continue
    if '#/paper/' in u:spa_routes+=1;continue
    p=urlsplit(u)
    if p.scheme or u.startswith('//'):continue
    if p.path:
        file_links+=1
        if not (root/unquote(p.path)).resolve().exists():bad_files.append(u)
    if p.fragment:
        fragment_links+=1
        if unquote(p.fragment) not in ids:bad_fragments.append(u)
assert not bad_files and not bad_fragments,(bad_files,bad_fragments)
pdf_sha=hashlib.sha256(pdf.read_bytes()).hexdigest()
qa={'date':'2026-10-28','topic':'5-1-4','cycle':52,'original_pdf_sha256':original,'original_preserved':True,
'integrated_pdf_sha256':pdf_sha,'integrated_pdf_pages':len(doc),'pdf_images':images,'blank_pages':blank,
'text_boundary_violations':boundary,'concept_count':len(concepts),'min_concept_words':min(concept_words),
'original_mcqs':30,'correct_answers':{k:answers.count(k) for k in 'ABCD'},'distractors':90,
'mains_body_only_counts':body_counts,'html_file_links_checked':file_links,'broken_files':bad_files,
'html_fragment_links_checked':fragment_links,'broken_fragments':bad_fragments,
'spa_routes_excluded':spa_routes,'source_checks':'nine bounded primary-source correct-key correspondences plus one arithmetic; not a complete item audit',
'independent_academic_approvals':0,'R8':'IN_PROGRESS_NOT_PASS',
'actual_downloaded_post_edit_artifact_qa':False,'browser_accessibility_certified':False}
(root/'QA-REPORT.md').write_text('# Cycle52 CI render QA\n\n'+json.dumps(qa,indent=2)+'\n')
(root/'README.md').write_text('# Paper V / Unit I / Topic 4 — Applications of Space Technology\n\nOriginal 23-page PDF preserved (SHA256 '+original+').\nCycle52 editable master, offline HTML and integrated PDF synchronized through CI.\n16 concepts >=300 words, 30 original practice MCQs, six structured 200–250 body-word mains, three original diagrams.\nNine bounded correct-key correspondences only; no full independent MCQ, mains, diagram, syllabus or browser audit.\nZero academic approvals. No official PYQs authenticated.\n')
manifest=json.loads((root/'manifest.json').read_text())
manifest['academic_status']='not_approved'
manifest['official_syllabus_reauthenticated_cycle52']=False
manifest['syllabus_source_limitation']='Commission PDF direct retrieval returned HTTP 403; R1 IN_PROGRESS'
manifest['integrated_pdf_status']='CI_rendered_independent_academic_audit_pending'
manifest['integrated_pdf_pages']=len(doc)
manifest['integrated_pdf_sha256']=pdf_sha
manifest['metrics']['mains_answer_word_counts']=body_counts
manifest['metrics']['mains_count_method']='body-only, excluding question, subheading labels and count line'
manifest['metrics']['concepts_below_300']=0
files=manifest.get('files',{})
for f in root.rglob('*'):
    if f.is_file() and f.name!='manifest.json':
        files[f.relative_to(root).as_posix()]=hashlib.sha256(f.read_bytes()).hexdigest()
manifest['files']=files
(root/'manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n')
Path('project-control/academic-readiness/5-1-4-cycle52-ci-render-qa-2026-10-28.json').write_text(json.dumps(qa,indent=2)+'\n')
print(json.dumps(qa,indent=2))
