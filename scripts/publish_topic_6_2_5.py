"""Cycle73 guarded Topic 6-2-5 publication. Academic approval is NEVER inferred."""
from pathlib import Path
from urllib.parse import urlsplit, unquote
import hashlib, json, re, subprocess, sys
import fitz, mistune
from bs4 import BeautifulSoup

root=Path('Paper 6/Unit 2 - Mobilisational Phase (1971–1990)/Topic 5')
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
sha=lambda path:hashlib.sha256(path.read_bytes()).hexdigest()
original=sha(root/'complete-notes.pdf')
md=(src/'complete-notes.md').read_text()
word=lambda s:len(re.findall(r"[\w]+(?:[’'-][\w]+)*",s,re.U))
headings=list(re.finditer(r'^## (\d+)\. ([^\n]+)\n',md,re.M))
concepts=[]
for i,m in enumerate(headings):
    n=int(m.group(1))
    if 2<=n<=27:
        end=headings[i+1].start() if i+1<len(headings) else len(md)
        body=re.sub(r'!\[[^\]]*\]\([^)]+\)','',md[m.end():end])
        concepts.append({'section':n,'words':word(body)})
assert len(concepts)==26 and [x['section'] for x in concepts]==list(range(2,28))
assert sum(x['words']<300 for x in concepts)<=22,concepts
practice=(src/'original-practice.md').read_text().strip()
assert practice in md
mcqs=list(re.finditer(r'\*\*MCQ (\d+)\.\*\*(.*?)\*\*Answer: ([A-D])\.\*\*',practice,re.S))
assert len(mcqs)==30
keys=[]
for i,m in enumerate(mcqs,1):
    assert int(m.group(1))==i
    assert all(re.search(r'\('+c+r'\)',m.group(2)) for c in 'ABCD')
    keys.append(m.group(3))
ms=list(re.finditer(r'^### Mains (\d+) —[^\n]*$',md,re.M))
assert len(ms)==6
body_counts=[]
for i,m in enumerate(ms):
    end=ms[i+1].start() if i+1<len(ms) else md.index('\n## 34.',m.end())
    body=re.sub(r'^\*\*[^*\n]+\*\*\s*','',md[m.end():end],flags=re.M)
    body_counts.append(word(body))
assert all(200<=n<=250 for n in body_counts),body_counts
images=re.findall(r'!\[[^\]]*\]\(([^)]+)\)',md)
assert len(images)==3 and all((src/p).resolve().is_file() for p in images)
pdf=src/'integrated-student-edition-cycle73.pdf'
subprocess.run([sys.executable,'scripts/render_topic_6_2_5_integrated.py','--input',str(src/'complete-notes.md'),'--output',str(pdf)],check=True)
doc=fitz.open(pdf)
blank=[i+1 for i,p in enumerate(doc) if len(p.get_text().strip())<60]
out_of_bounds=[]
for i,p in enumerate(doc):
    for b in p.get_text('blocks'):
        x0,y0,x1,y1=b[:4]
        if x0<-1 or y0<-1 or x1>p.rect.width+1 or y1>p.rect.height+1:out_of_bounds.append(i+1)
image_count=sum(len(p.get_images()) for p in doc)
assert 18<=len(doc)<=80 and not blank and image_count>=3 and not out_of_bounds,(len(doc),blank,image_count,out_of_bounds)
html=mistune.create_markdown(plugins=['table','strikethrough'])(md)
soup=BeautifulSoup(html,'html.parser')
for img in soup.find_all('img'):
    u=img.get('src','')
    if u.startswith('../diagrams/') or u.startswith('diagrams/'):img['src']='diagrams/'+u.rsplit('/',1)[-1]
seen={}
for h in soup.find_all(['h1','h2','h3']):
    slug=re.sub('[^a-z0-9]+','-',h.get_text(' ',strip=True).lower()).strip('-') or 'section'
    n=seen.get(slug,0);seen[slug]=n+1
    if n:slug+=f'-{n}'
    h['id']=slug
head='<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>TGPSC 6-2-5</title><style>body{font-family:system-ui,sans-serif;max-width:980px;margin:auto;padding:2rem;line-height:1.65;color:#172b3b}h1,h2,h3{color:#173e65}table{border-collapse:collapse;width:100%}th,td{border:1px solid #cad7df;padding:6px}img{max-width:100%;height:auto}nav a{margin-right:1rem}</style></head><body><nav><a href="complete-notes.pdf">Original PDF</a><a href="source/integrated-student-edition-cycle73.pdf">Integrated PDF</a><a href="source/complete-notes.md">Editable master</a><a href="../../../../index.html">Study portal</a></nav><p><strong>Original practice only. NOT academically approved.</strong></p>'
(root/'index.html').write_text(head+str(soup)+'</body></html>')
soup2=BeautifulSoup((root/'index.html').read_text(),'html.parser')
checked=0;bad=[]
for el in soup2.find_all(['a','img']):
    u=el.get('href') or el.get('src') or ''
    if not u or urlsplit(u).scheme or u.startswith('#'):continue
    p=unquote(urlsplit(u).path)
    checked+=1
    if not (root/p).resolve().is_file():bad.append(p)
assert not bad,bad
qa={'cycle':73,'topic_id':'6-2-5','original_pdf_sha256':original,'integrated_pdf_sha256':sha(pdf),'integrated_pdf_pages':len(doc),
    'concept_count':26,'concept_word_counts':concepts,'concepts_below_300':sum(x['words']<300 for x in concepts),
    'mcq_count':30,'key_distribution':{c:keys.count(c) for c in 'ABCD'},
    'mains_body_only_counts':body_counts,'embedded_images':image_count,
    'blank_pages':blank,'out_of_bounds_pages':out_of_bounds,'local_links_checked':checked,'broken_links':bad,
    'all_75_original_pdf_files_present':True,'full_page_per_concept_met':False,
    'all_30_mcq_keys_independently_verified':False,'all_90_distractors_independently_verified':False,
    'mains_claim_level_review_complete':False,'direct_browser_accessibility_certified':False,
    'R8':'IN_PROGRESS_PENDING_DOWNLOADED_ARTIFACT_QA','independent_academic_approvals':0}
(root/'QA-REPORT.md').write_text('# Cycle73 Topic 6-2-5 deterministic publication QA\n\n'+json.dumps(qa,indent=2)+'\n')
(root/'README.md').write_text('# Paper VI / Unit II / Topic 5 — Quest for Telangana identity\n\n'
    'Original PDF SHA256 '+original+' preserved.\n\n'
    '[Offline HTML](index.html) · [Integrated PDF](source/integrated-student-edition-cycle73.pdf) · '
    '[Editable master](source/complete-notes.md) · [Original PDF](complete-notes.pdf).\n\n'
    'Four concept expansions, two mains corrections, three revised MCQs, three embedded diagrams. '
    '22 concepts still shallow; zero independent approvals.\n')
manifest=json.loads((root/'manifest.json').read_text())
manifest.update({'academically_approved':False,'academic_status':'not_approved',
    'source_word_count':word(md),'mcq_count':30,'mains_count':6,
    'integrated_pdf_status':'CI_rendered_pending_academic_audit','integrated_pdf_pages':len(doc),
    'integrated_pdf_sha256':sha(pdf),'independent_academic_approvals':0})
manifest['metrics']={'concept_count':26,'concepts_below_300':qa['concepts_below_300'],
    'answer_distribution':qa['key_distribution'],'full_page_density_certified':False,
    'independent_review_complete':False}
manifest['files_sha256']={f.relative_to(root).as_posix():sha(f) for f in sorted(root.rglob('*'),key=lambda p:p.as_posix()) if f.is_file() and f.name!='manifest.json'}
(root/'manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n')
Path('project-control/academic-readiness/6-2-5-cycle73-ci-render-qa-2026-10-29.json').write_text(json.dumps(qa,indent=2)+'\n')
print(json.dumps({k:v for k,v in qa.items() if k!='concept_word_counts'},indent=2))
