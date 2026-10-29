"""Cycle85 deterministic Topic 2-2-2 student edition; NOT academic certification."""
from pathlib import Path
import json, re, hashlib, subprocess, sys
from urllib.parse import urlsplit, unquote
import fitz, mistune
from bs4 import BeautifulSoup

ROOT=Path('Paper 2/Unit 2 - Telangana History and Cultural Heritage/Topic 2')
SRC=ROOT/'source'
PC=Path('project-control')
SHA=lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
checkpoint=json.loads((PC/'PRODUCTION-CHECKPOINT.json').read_text())
index=json.loads((PC/'ACADEMIC_READINESS_75_TOPIC_STATUS_INDEX.json').read_text())
topics=checkpoint['topics']
assert len(topics)==len({t['id'] for t in topics})==75
assert index['total_topics']==checkpoint['total_topics']==75
assert checkpoint['academically_approved']==index['independently_academically_approved_count']==0
assert len(list((PC/'academic-readiness').glob('[2-6]-[1-3]-[1-5].json')))==75
assert len(index['paths'])==75
assert all((Path(t['path'])/'complete-notes.pdf').is_file() for t in topics)
counts={k:sum(t['readiness_status']==k for t in topics) for k in ['IN_PROGRESS','ASSESSED_REBUILD_REQUIRED','NOT_ASSESSED']}
assert counts=={'IN_PROGRESS':7,'ASSESSED_REBUILD_REQUIRED':67,'NOT_ASSESSED':1},counts
assert index['not_assessed_count']==1 and '2-2-2' in index['assessed_rebuild_required']
original=SHA(ROOT/'complete-notes.pdf')
assert original=='1c53597fbae9aaa794f6f3e2c5ca065e19eb38757941d8ce5d16462822b567b1'
master=SRC/'integrated-student-master-cycle85.md'
md=master.read_text(encoding='utf-8')
assert 'NOT academically approved' in md and 'NOT official TGPSC previous-year questions' in md
concept=md.split('# Detailed textbook-style concepts (22 substantive sections)',1)[1].split('## Evidence diagrams and interpretation',1)[0]
sections=[s for s in re.split(r'(?=^## \d+\. )',concept,flags=re.M) if re.match(r'^## \d+\. ',s)]
word=lambda s:len(re.findall(r"\b[\w]+(?:['’\-][\w]+)*\b",s))
depth=[word(s.split('\n',1)[1]) for s in sections]
assert len(depth)==22 and sum(n<300 for n in depth)==16,depth
practice=md.split('## Original practice MCQs (30, four options each)',1)[1].split('## Six complete original mains model answers',1)[0]
qs=[s for s in re.split(r'(?=^### Q\d+\. )',practice,flags=re.M) if s.startswith('### Q')]
assert len(qs)==30
keys=[]
for n,q in enumerate(qs,1):
 assert q.startswith('### Q'+str(n)+'. ')
 opts=re.findall(r'^([ABCD])\) (.+)$',q,re.M)
 assert len(opts)==4 and [x[0] for x in opts]==list('ABCD'),(n,opts)
 assert len({x[1] for x in opts})==4,n
 ans=re.findall(r'\*\*Answer: ([ABCD])\.',q)
 assert len(ans)==1,n
 keys.append(ans[0])
assert {x:keys.count(x) for x in 'ABCD'}=={'A':8,'B':8,'C':7,'D':7}
mains=md.split('## Six complete original mains model answers',1)[1].split('## Source register and limitations',1)[0]
assert len(re.findall(r'^### Mains [1-6]\. ',mains,re.M))==6
for name in ['diagram-tank-political-ecology.svg','diagram-evidence-confidence.svg','diagram-resistance-timelines.svg']:
 assert (SRC/name).is_file() and md.count(']('+name+')')==1
pdf=SRC/'integrated-student-edition-cycle85.pdf'
subprocess.run([sys.executable,'scripts/render_topic_2_2_2_cycle85.py','--input',str(master),'--output',str(pdf)],check=True)
doc=fitz.open(pdf)
blank=[i+1 for i,p in enumerate(doc) if len(p.get_text().strip())<35]
outside=[]
for i,p in enumerate(doc):
 for b in p.get_text('blocks'):
  if b[0]<-1 or b[1]<-1 or b[2]>p.rect.width+1 or b[3]>p.rect.height+1:outside.append(i+1)
assert 20<=len(doc)<=100 and not blank and not outside,(len(doc),blank,outside)
html=mistune.create_markdown(plugins=['table','strikethrough'])(md)
soup=BeautifulSoup(html,'html.parser');seen={}
for h in soup.find_all(['h1','h2','h3']):
 slug=re.sub('[^a-z0-9]+','-',h.get_text(' ',strip=True).lower()).strip('-') or 'section'
 n=seen.get(slug,0);seen[slug]=n+1;h['id']=slug+(f'-{n}' if n else '')
head='<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>TGPSC Topic 2-2-2 Cycle85</title><style>body{font-family:system-ui,sans-serif;max-width:960px;margin:auto;padding:2rem;line-height:1.65;color:#172b3b}h1,h2,h3{color:#173e65}img{max-width:100%;height:auto}table{border-collapse:collapse}td,th{border:1px solid #b8c9d9;padding:.35rem}</style></head><body><nav><a href="../complete-notes.pdf">Original PDF</a> · <a href="integrated-student-edition-cycle85.pdf">Cycle85 PDF</a> · <a href="integrated-student-master-cycle85.md">Editable master</a> · <a href="../index.html">Topic portal</a></nav><p><strong>Original practice only. NOT academically approved.</strong></p>'
page=SRC/'integrated-student-cycle85.html';page.write_text(head+str(soup)+'</body></html>',encoding='utf-8')
checked=0;broken=[]
for el in BeautifulSoup(page.read_text(),'html.parser').find_all(['a','img']):
 u=el.get('href') or el.get('src') or ''
 if not u or urlsplit(u).scheme or u.startswith('#'):continue
 checked+=1
 if not (page.parent/unquote(urlsplit(u).path)).resolve().is_file():broken.append(u)
assert not broken,broken
inventory='\n'.join(t['id']+':'+SHA(Path(t['path'])/'complete-notes.pdf') for t in sorted(topics,key=lambda x:x['id']))
qa={'cycle':85,'topic_id':'2-2-2','academic_status':'ASSESSED_REBUILD_REQUIRED','independent_approvals':0,'original_pdf_sha256':original,'original_pdf_inventory_count':75,'original_pdf_inventory_digest':hashlib.sha256(inventory.encode()).hexdigest(),'readiness_json_count':75,'integrated_pdf_pages':len(doc),'integrated_pdf_sha256':SHA(pdf),'blank_pdf_pages':blank,'out_of_bounds_pdf_pages':outside,'concept_count':22,'concept_body_word_counts':depth,'concepts_under_300':16,'mcq_count':30,'mcq_key_distribution':{k:keys.count(k) for k in 'ABCD'},'mcq_malformed_option_count':0,'bounded_author_source_correlated_keys':8,'bounded_author_source_correlated_distractors':24,'remaining_keys_needing_independent_audit':22,'remaining_distractors_needing_independent_audit':66,'mains_count':6,'mains_claim_level_verified':False,'html_local_links_checked':checked,'broken_html_local_links':broken,'R1':'IN_PROGRESS','R8':'IN_PROGRESS_PENDING_ACTUAL_DOWNLOADED_GITHUB_ARTIFACT_AND_BROWSER','R9':'NOT_STARTED'}
(PC/'academic-readiness/2-2-2-cycle85-ci-render-qa-2026-10-29.json').write_text(json.dumps(qa,indent=2,ensure_ascii=False)+'\n')
manifest={'topic_id':'2-2-2','cycle':85,'academic_status':'NOT_APPROVED','original_pdf_sha256':original,'pdf_sha256':SHA(pdf),'pdf_pages':len(doc),'files':{p.name:SHA(p) for p in [master,pdf,page]}}
(SRC/'integrated-cycle85-manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({'pdf_pages':len(doc),'pdf_sha256':SHA(pdf),'concepts_under300':16,'mcqs':30,'mains':6,'broken_local_links':broken,'approvals':0},indent=2))
