"""Deterministic Topic 6-2-3 publication; no academic approval inferred."""
from pathlib import Path
from urllib.parse import urlsplit, unquote
import hashlib, json, re, subprocess, sys
import fitz, mistune
from bs4 import BeautifulSoup

root=Path('Paper 6/Unit 2 - Mobilisational Phase (1971–1990)/Topic 3')
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
assert original=='3b0d9d5908c2e26e838d1cf9240b8b783151825cfedc437fb0dd99c5ddd88bc3'
md=(src/'complete-notes.md').read_text()
word=lambda s:len(s.strip().split())
concepts=[]
for match in re.finditer(r'^## (\d+)\. ([^\n]+)\n',md,re.M):
    next_h=re.search(r'^## ',md[match.end():],re.M)
    end=match.end()+next_h.start() if next_h else len(md)
    concepts.append((int(match.group(1)),match.group(2),md[match.end():end]))
assert len(concepts)==34 and [n for n,_,_ in concepts]==list(range(1,35))
counts=[word(body) for _,_,body in concepts]
assert sum(x<300 for x in counts)<=30,counts
qsrc=(src/'original-practice.md').read_text()
questions=re.findall(r'\*\*MCQ (\d+)\.\*\*(.*?)\*\*Answer: ([A-D])\.\*\*',qsrc,re.S)
assert len(questions)==30,len(questions)
keys=[]
for i,(number,question,key) in enumerate(questions,1):
    assert int(number)==i
    assert all(re.search(r'\('+letter+r'\)',question) for letter in 'ABCD'),(i,question)
    keys.append(key)
assert len(keys)==30
answers=(src/'answer-blueprints.md').read_text()
assert re.findall(r'(?m)^### Mains Answer (\d+) —',answers)==['1','2','3','4','5','6']
body_counts=[]
ms=list(re.finditer(r'^### Mains Answer (\d+) —',answers,re.M))
for i,m in enumerate(ms):
    next_heading=answers.find('\n## ',m.end())
    end=min(ms[i+1].start() if i+1<len(ms) else len(answers),next_heading if next_heading!=-1 else len(answers))
    body=re.sub(r'\*\*([^*]+)\*\*',r'\1',answers[m.end():end])
    body_counts.append(word(body))
assert len(body_counts)==6 and all(200<=n<=250 for n in body_counts),body_counts
assert len(list((root/'diagrams').glob('*.png')))==3
pdf=src/'integrated-student-edition-cycle71.pdf'
subprocess.run([sys.executable,'scripts/render_topic_6_2_3_integrated.py','--input',str(src/'complete-notes.md'),'--output',str(pdf)],check=True)
doc=fitz.open(pdf)
blank=[i+1 for i,p in enumerate(doc) if len(p.get_text().strip())<60]
images=sum(len(p.get_images()) for p in doc)
boundary=[]
for i,p in enumerate(doc):
    for b in p.get_text('blocks'):
        x0,y0,x1,y1=b[:4]
        if x0<-1 or y0<-1 or x1>p.rect.width+1 or y1>p.rect.height+1:boundary.append(i+1)
assert 20<=len(doc)<=75 and not blank and images>=3 and not boundary,(len(doc),blank,images,boundary)
html=mistune.create_markdown(plugins=['table','strikethrough'])(md)
soup=BeautifulSoup(html,'html.parser')
for img in soup.find_all('img'):
    u=img.get('src','')
    if u.startswith('../diagrams/') or u.startswith('diagrams/'):
        img['src']='diagrams/'+u.rsplit('/',1)[-1]
seen={}
for h in soup.find_all(['h1','h2','h3']):
    slug=re.sub('[^a-z0-9]+','-',h.get_text(' ',strip=True).lower()).strip('-') or 'section'
    n=seen.get(slug,0);seen[slug]=n+1
    if n:slug+=f'-{n}'
    h['id']=slug
head='''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>TGPSC 6-2-3</title><style>body{font-family:system-ui,sans-serif;max-width:980px;margin:auto;padding:2rem;line-height:1.65;color:#172b3b}h1,h2,h3{color:#173e65}table{border-collapse:collapse;width:100%}th,td{border:1px solid #cdd9e3;padding:.55rem;text-align:left}th{background:#eaf2f7}img{max-width:100%;height:auto}a{color:#145c98}.banner{padding:1rem;background:#fff2d4;border:1px solid #b99045}</style></head><body><nav><a href="../../../index.html">Study portal</a></nav><p class="banner"><strong>STUDENT DRAFT — NOT ACADEMICALLY APPROVED.</strong> __SHALLOW__/34 concepts below 300 words. 1983 election tables and independent review pending.</p><p><a href="source/integrated-student-edition-cycle71.pdf">Integrated PDF</a> · <a href="source/complete-notes.md">Editable master</a> · <a href="complete-notes.pdf">Preserved original PDF</a></p>'''
head=head.replace('__SHALLOW__',str(sum(x<300 for x in counts)))
(root/'index.html').write_text(head+str(soup)+'</body></html>')
page=BeautifulSoup((root/'index.html').read_text(),'html.parser')
ids={x.get('id') for x in page.find_all(id=True)}
files_checked=fragments_checked=spa_routes=0;bad_files=[];bad_fragments=[]
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
qa={'date':'2026-10-29','topic_id':'6-2-3','cycle':71,'original_pdf_sha256':original,'original_preserved':True,
    'integrated_pdf_sha256':sha(pdf),'integrated_pdf_pages':len(doc),'pdf_images':images,'blank_pages':blank,
    'out_of_page_text_blocks':boundary,'concept_count':len(concepts),'concept_word_counts':counts,
    'concepts_below_300':sum(n<300 for n in counts),'mcq_count':30,'distractor_count':90,
    'answer_distribution':{o:keys.count(o) for o in 'ABCD'},'mains_body_only_counts':body_counts,
    'local_file_links_checked':files_checked,'broken_file_links':bad_files,'dom_fragment_links_checked':fragments_checked,
    'broken_fragment_links':bad_fragments,'spa_routes_excluded':spa_routes,
    'full_mcq_distractor_external_verification':False,'full_mains_claim_review_complete':False,
    'full_page_per_concept_met':False,'direct_browser_accessibility_certified':False,'independent_academic_approvals':0,
    'R8':'IN_PROGRESS_PENDING_ACTUAL_DOWNLOADED_ARTIFACT_AND_ACADEMIC_QA'}
(root/'QA-REPORT.md').write_text('# Cycle71 deterministic render QA\n\n'+json.dumps(qa,indent=2)+'\n')
(root/'README.md').write_text('# Paper VI / Unit II / Topic 3 — Regional parties and Telangana identity\n\n'
    'Original PDF SHA256 '+original+' preserved.\n\n'
    '[Offline HTML](index.html) · [Integrated PDF](source/integrated-student-edition-cycle71.pdf) · '
    '[Editable master](source/complete-notes.md) · [Original PDF](complete-notes.pdf).\n\n'
    '4 source-bounded depth expansions; 30 remain shallow; source access bounded; academic approval ZERO.\n')
manifest=json.loads((root/'manifest.json').read_text())
manifest.update({'academically_approved':False,'academic_status':'not_approved','source_word_count':word(md),
    'mcq_count':30,'mains_count':6,'integrated_pdf_status':'CI_rendered_pending_academic_audit',
    'integrated_pdf_pages':len(doc),'integrated_pdf_sha256':sha(pdf),'independent_academic_approvals':0})
manifest['metrics']={'concept_count':34,'concepts_below_300':sum(n<300 for n in counts),'answer_distribution':qa['answer_distribution'],
    'full_page_density_certified':False,'independent_review_complete':False}
manifest['files_sha256']={f.relative_to(root).as_posix():sha(f) for f in sorted(root.rglob('*'),key=lambda p:p.as_posix()) if f.is_file() and f.name!='manifest.json'}
(root/'manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n')
Path('project-control/academic-readiness/6-2-3-cycle71-ci-render-qa-2026-10-29.json').write_text(json.dumps(qa,indent=2)+'\n')
print(json.dumps({k:v for k,v in qa.items() if k!='concept_word_counts'},indent=2))