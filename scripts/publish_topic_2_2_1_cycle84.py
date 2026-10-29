"""Cycle84 deterministic, guarded Topic 2-2-1 publication. Not an academic approval."""
from pathlib import Path
from urllib.parse import urlsplit, unquote
import re, json, hashlib, subprocess, sys
import fitz, mistune
from bs4 import BeautifulSoup

root=Path('Paper 2/Unit 2 - Telangana History and Cultural Heritage/Topic 1')
src=root/'source';pc=Path('project-control')
checkpoint=json.loads((pc/'PRODUCTION-CHECKPOINT.json').read_text())
index=json.loads((pc/'ACADEMIC_READINESS_75_TOPIC_STATUS_INDEX.json').read_text())
topics=checkpoint['topics']
assert len(topics)==len({x['id'] for x in topics})==checkpoint['total_topics']==index['total_topics']==75
assert len(index['paths'])==len(set(index['paths']))==75
assert len(list((pc/'academic-readiness').glob('[2-6]-[1-3]-[1-5].json')))==75
assert checkpoint['academically_approved']==index['independently_academically_approved_count']==0
status={k:sum(t['readiness_status']==k for t in topics) for k in ('IN_PROGRESS','ASSESSED_REBUILD_REQUIRED','NOT_ASSESSED')}
assert status=={'IN_PROGRESS':7,'ASSESSED_REBUILD_REQUIRED':66,'NOT_ASSESSED':2},status
assert index['not_assessed_count']==2 and '2-2-1' in index['assessed_rebuild_required']
assert all((Path(t['path'])/'complete-notes.pdf').is_file() for t in topics)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
original=sha(root/'complete-notes.pdf')
assert original=='08855c26b7d2910bd990674a3ced68d1011d8de0e56e6bfdf19d4582597208c2',original
master=src/'integrated-student-master-cycle84.md';md=master.read_text()
assert 'NOT academically approved' in md and 'NOT official TGPSC previous-year questions' in md
concept=md.split('# Detailed textbook-style concepts (16 substantive sections)',1)[1].split('## Evidence-to-inference comparison',1)[0]
parts=re.split(r'(?=^## \d+\.\s)',concept,flags=re.M)
counts=[len(re.findall(r"\b[\w]+(?:['’\-][\w]+)*\b",p)) for p in parts if re.match(r'^## \d+\.\s',p)]
assert len(counts)==16 and all(n>=300 for n in counts),counts
practice=md.split('## Original practice MCQs',1)[1].split('## Six complete original mains',1)[0]
answers=re.findall(r'\*\*Answer: ([ABCD])\.',practice)
assert len(answers)==30 and {k:answers.count(k) for k in 'ABCD'}=={'A':8,'B':8,'C':7,'D':7}
assert len(re.findall(r'^### MCQ \d+\.',practice,re.M))==30
mains=md.split('## Six complete original mains model answers',1)[1].split('## Answer blueprints',1)[0]
parts=re.split(r'(?=^### Mains [1-6]\.)',mains,flags=re.M)
body_counts=[]
for p in parts:
 if not p.startswith('### Mains '):continue
 p='\n'.join(p.splitlines()[1:])
 body_counts.append(len(re.findall(r"\b[\w]+(?:['’\-][\w]+)*\b",p)))
assert len(body_counts)==6 and all(200<=n<=250 for n in body_counts),body_counts
for image in ['diagram-evidence-ladder.svg','diagram-ancient-telangana-sites.svg','diagram-vishnukundin-patronage.svg']:
 assert md.count(']('+image+')')==1 and (src/image).is_file(),image
pdf=src/'integrated-student-edition-cycle84.pdf'
subprocess.run([sys.executable,'scripts/render_topic_2_2_1_cycle84.py','--input',str(master),'--output',str(pdf)],check=True)
doc=fitz.open(pdf)
blank=[i+1 for i,p in enumerate(doc) if len(p.get_text().strip())<50]
outside=[]
for i,p in enumerate(doc):
 for b in p.get_text('blocks'):
  if b[0]<-1 or b[1]<-1 or b[2]>p.rect.width+1 or b[3]>p.rect.height+1:outside.append(i+1)
assert 20<=len(doc)<=70 and not blank and not outside,(len(doc),blank,outside)
# All 16 numbered concepts must begin on distinct PDF pages.
heading_pages={}
for i,p in enumerate(doc):
 for m in re.finditer(r'(?m)^(\d{1,2})\. (?:Evidence hierarchy|Megalithic societies|Kotilingala|Peddabankur|Dhulikatta|Satavahana politics|Satavahana economy|Phanigiri|Ikshvakus|Vishnukundin charters|Ipur charter|Jainism|Language and literature|Art and architecture|Heritage administration|Synthesis)',p.get_text()):
  heading_pages[int(m.group(1))]=i+1
assert len(heading_pages)==16 and len(set(heading_pages.values()))==16,heading_pages
html=mistune.create_markdown(plugins=['table','strikethrough'])(md)
soup=BeautifulSoup(html,'html.parser');seen={}
for h in soup.find_all(['h1','h2','h3']):
 slug=re.sub('[^a-z0-9]+','-',h.get_text(' ',strip=True).lower()).strip('-') or 'section'
 n=seen.get(slug,0);seen[slug]=n+1;h['id']=slug+(f'-{n}' if n else '')
head='<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>TGPSC Topic 2-2-1 Cycle84</title><style>body{font-family:system-ui,sans-serif;max-width:980px;margin:auto;padding:2rem;line-height:1.7;color:#172b3b}h1,h2,h3{color:#173e65}table{border-collapse:collapse;width:100%}th,td{border:1px solid #cad7df;padding:6px}img{max-width:100%;height:auto}nav a{margin-right:1rem}</style></head><body><nav><a href="../complete-notes.pdf">Original PDF</a><a href="integrated-student-edition-cycle84.pdf">Cycle84 PDF</a><a href="integrated-student-master-cycle84.md">Editable master</a><a href="../index.html">Topic portal</a></nav><p><strong>Original practice only. NOT academically approved.</strong></p>'
page=src/'integrated-student-cycle84.html';page.write_text(head+str(soup)+'</body></html>')
checked=0;broken=[]
for el in BeautifulSoup(page.read_text(),'html.parser').find_all(['a','img']):
 u=el.get('href') or el.get('src') or ''
 if not u or urlsplit(u).scheme or u.startswith('#'):continue
 checked+=1
 if not (page.parent/unquote(urlsplit(u).path)).resolve().is_file():broken.append(u)
assert not broken,broken
inventory='\n'.join(t['id']+':'+sha(Path(t['path'])/'complete-notes.pdf') for t in sorted(topics,key=lambda x:x['id']))
qa={'cycle':84,'topic_id':'2-2-1','academic_status':'ASSESSED_REBUILD_REQUIRED','original_pdf_sha256':original,'original_pdf_inventory_count':75,'original_pdf_inventory_digest':hashlib.sha256(inventory.encode()).hexdigest(),'readiness_json_count':75,'integrated_pdf_pages':len(doc),'integrated_pdf_sha256':sha(pdf),'pdf_blank_pages':blank,'pdf_outside_pages':outside,'concept_count':16,'concept_body_word_counts':counts,'concepts_under_300':0,'concept_start_pages':heading_pages,'mcq_count':30,'mcq_key_distribution':{k:answers.count(k) for k in 'ABCD'},'mains_body_only_counts':body_counts,'local_html_links_checked':checked,'broken_local_html_links':broken,'source_checked_mcq_keys':0,'source_checked_mcq_distractors':0,'R1':'PASS','R8':'IN_PROGRESS_PENDING_ACTUAL_DOWNLOADED_ARTIFACT_AND_LIVE_BROWSER','R9':'NOT_STARTED','independent_approvals':0}
evidence=pc/'academic-readiness/2-2-1-cycle84-ci-render-qa-2026-10-29.json';evidence.write_text(json.dumps(qa,indent=2,ensure_ascii=False)+'\n')
manifest={'topic_id':'2-2-1','cycle':84,'academic_status':'not_approved','original_pdf_sha256':original,'pdf_sha256':sha(pdf),'pdf_pages':len(doc),'sha256':{p.name:sha(p) for p in [master,pdf,page]}}
(src/'integrated-cycle84-manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({'pdf_pages':len(doc),'pdf_sha256':sha(pdf),'concept_count':16,'concepts_under_300':0,'mcq_count':30,'mains_counts':body_counts,'local_links':checked,'approval':0},indent=2))