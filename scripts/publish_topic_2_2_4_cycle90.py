"""Cycle90: deterministic publisher for existing Topic 2-2-4; never an academic approval."""
from pathlib import Path
import hashlib, json, re, subprocess, sys
from urllib.parse import urlsplit,unquote
import fitz,mistune
from bs4 import BeautifulSoup
ROOT=Path('Paper 2/Unit 2 - Telangana History and Cultural Heritage/Topic 4')
SRC=ROOT/'source'; PC=Path('project-control')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
ck=json.loads((PC/'PRODUCTION-CHECKPOINT.json').read_text())
idx=json.loads((PC/'ACADEMIC_READINESS_75_TOPIC_STATUS_INDEX.json').read_text())
ts=ck['topics']
assert len(ts)==len({t['id'] for t in ts})==75
assert len(list((PC/'academic-readiness').glob('[2-6]-[1-3]-[1-5].json')))==75
assert idx['total_topics']==ck['total_topics']==75
assert ck['academically_approved']==idx['independently_academically_approved_count']==0
assert {k:sum(t['readiness_status']==k for t in ts) for k in ('IN_PROGRESS','ASSESSED_REBUILD_REQUIRED','NOT_ASSESSED')}=={'IN_PROGRESS':7,'ASSESSED_REBUILD_REQUIRED':68,'NOT_ASSESSED':0}
assert all((Path(t['path'])/'complete-notes.pdf').is_file() for t in ts)
assert sha(ROOT/'complete-notes.pdf')=='8ebfd5a08024a3dd729d326d5b1f53201fafc0de6bd86a3e194b583cd9a90ba1'
master=SRC/'integrated-student-edition-pilot-2026-10-26.md'; md=master.read_text(encoding='utf-8')
assert 'NOT independently academically approved' in md and 'NOT official PYQs' in md
practice=md.split('## 20. Thirty original',1)[1].split('## 21. Sources',1)[0]
questions=[q for q in re.split(r'(?=^### MCQ \d+\.)',practice,flags=re.M) if q.startswith('### MCQ')]
assert len(questions)==30,len(questions)
for n,q in enumerate(questions,1):
 assert q.startswith('### MCQ '+str(n)+'.'),n
 opts=re.findall(r'^([ABCD])\. (.+)$',q,re.M)
 assert [a for a,b in opts]==list('ABCD') and len(set(b for a,b in opts))==4,(n,opts)
 assert len(re.findall(r'\*\*Answer: [ABCD]\.',q))==1,n
for n,key in {6:'A',7:'B',8:'D',12:'B',13:'A',28:'A'}.items():
 q=questions[n-1]
 assert ('**Answer: '+key+'.**') in q and '**Source' in q,(n,q[-300:])
mains=md.split('## 19. Six original',1)[1].split('## 20. Thirty original',1)[0]
assert len(re.findall(r'^## Question \d+\.',mains,re.M))==6
for name in ['diagram-a-public-sphere.svg','diagram-b-reform-axes.svg','diagram-c-timeline.svg']:
 assert (SRC/name).is_file() and md.count(']('+name+')')==1,name
pdf=SRC/'integrated-student-edition-pilot-2026-10-26.pdf'
subprocess.run([sys.executable,'scripts/render_topic_2_2_4_cycle90.py','--input',str(master),'--output',str(pdf)],check=True)
doc=fitz.open(pdf)
blank=[i+1 for i,p in enumerate(doc) if len(p.get_text().strip())<35]
outside=[]
for i,p in enumerate(doc):
 for b in p.get_text('blocks'):
  if b[0]<-1 or b[1]<-1 or b[2]>p.rect.width+1 or b[3]>p.rect.height+1:outside.append(i+1)
assert len(doc)>=20 and not blank and not outside,(len(doc),blank,outside)
for n in [6,7,8,12,13,28]:
 assert ('MCQ '+str(n)+'.') in '\n'.join(p.get_text() for p in doc)
html=mistune.create_markdown(plugins=['table','strikethrough'])(md)
soup=BeautifulSoup(html,'html.parser');seen={}
for h in soup.find_all(['h1','h2','h3']):
 slug=re.sub('[^a-z0-9]+','-',h.get_text(' ',strip=True).lower()).strip('-') or 'section'
 k=seen.get(slug,0);seen[slug]=k+1;h['id']=slug+(f'-{k}' if k else '')
prefix='<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>TGPSC Topic 2-2-4 Cycle90</title><style>body{font-family:system-ui,sans-serif;max-width:960px;margin:auto;padding:2rem;line-height:1.65;color:#172b3b}h1,h2,h3{color:#173e65}img{max-width:100%;height:auto}table{border-collapse:collapse}td,th{border:1px solid #b8c9d9;padding:.35rem}</style></head><body><nav><a href="../complete-notes.pdf">Original PDF</a> · <a href="integrated-student-edition-pilot-2026-10-26.pdf">Cycle90 PDF</a> · <a href="integrated-student-edition-pilot-2026-10-26.md">Editable master</a> · <a href="../index.html">Topic portal</a></nav><p><strong>Original practice only. NOT academically approved.</strong></p>'
page=SRC/'integrated-student-cycle90.html';page.write_text(prefix+str(soup)+'</body></html>',encoding='utf-8')
checked=0;broken=[]
for el in BeautifulSoup(page.read_text(),'html.parser').find_all(['a','img']):
 u=el.get('href') or el.get('src') or ''
 if not u or urlsplit(u).scheme or u.startswith('#'):continue
 checked+=1
 if not (page.parent/unquote(urlsplit(u).path)).resolve().is_file():broken.append(u)
assert not broken,broken
qa={'cycle':90,'topic_id':'2-2-4','original_pdf_sha256':sha(ROOT/'complete-notes.pdf'),'original_pdf_topics_preserved':75,'readiness_json_count':75,'integrated_pdf_pages':len(doc),'integrated_pdf_sha256':sha(pdf),'blank_pdf_pages':blank,'out_of_bounds_pdf_pages':outside,'mcq_count':30,'revised_source_correlated_mcqs':[6,7,8,12,13,28],'bounded_option_checks':24,'independent_mcq_audit_complete':False,'mains_count':6,'mains_claim_audit_complete':False,'html_local_links_checked':checked,'broken_html_local_links':broken,'R4':'BLOCKED','R5':'IN_PROGRESS','R8':'IN_PROGRESS_PENDING_ACTUAL_DOWNLOADED_ARTIFACT','R9':'NOT_STARTED','academic_approvals':0}
(PC/'academic-readiness/2-2-4-cycle90-ci-render-qa-2026-10-29.json').write_text(json.dumps(qa,indent=2)+'\n')
(SRC/'integrated-cycle90-manifest.json').write_text(json.dumps({'topic_id':'2-2-4','cycle':90,'status':'NOT_APPROVED','original_pdf_sha256':qa['original_pdf_sha256'],'files':{p.name:sha(p) for p in [master,pdf,page]},'pdf_pages':len(doc)},indent=2)+'\n')
print(json.dumps(qa,indent=2))
