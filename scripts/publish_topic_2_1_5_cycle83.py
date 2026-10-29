"""Cycle83 guarded Topic 2-1-5 publisher. Publication integrity is not academic approval."""
from pathlib import Path
from urllib.parse import urlsplit, unquote
import hashlib, json, re, subprocess, sys
import fitz, mistune
from bs4 import BeautifulSoup

root=Path('Paper 2/Unit 1 - Indian History and Culture/Topic 5')
src=root/'source'
pc=Path('project-control')
checkpoint=json.loads((pc/'PRODUCTION-CHECKPOINT.json').read_text())
index=json.loads((pc/'ACADEMIC_READINESS_75_TOPIC_STATUS_INDEX.json').read_text())
topics=checkpoint['topics']
assert len(topics)==len({x['id'] for x in topics})==checkpoint['total_topics']==index['total_topics']==75
assert len(index['paths'])==len(set(index['paths']))==75
assert len(list((pc/'academic-readiness').glob('[2-6]-[1-3]-[1-5].json')))==75
assert checkpoint['academically_approved']==index['independently_academically_approved_count']==0
statuses={s:sum(t['readiness_status']==s for t in topics) for s in ('IN_PROGRESS','ASSESSED_REBUILD_REQUIRED','NOT_ASSESSED')}
assert statuses=={'IN_PROGRESS':7,'ASSESSED_REBUILD_REQUIRED':65,'NOT_ASSESSED':3},statuses
assert index['not_assessed_count']==3
assert all((Path(t['path'])/'complete-notes.pdf').is_file() for t in topics)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
original=sha(root/'complete-notes.pdf')
assert original=='b35f6eedbad2bb3b7235bf3ac1d27e0a7ae731b03a4cd33e1f83dde7468d23a3',original
inventory='\n'.join(t['id']+':'+sha(Path(t['path'])/'complete-notes.pdf') for t in sorted(topics,key=lambda x:x['id']))
inventory_digest=hashlib.sha256(inventory.encode()).hexdigest()

master=src/'integrated-student-master-cycle83.md'
md=master.read_text()
assert 'NOT academically approved' in md
concept=md.split('# Detailed textbook-style concepts',1)[1].split('# Original analytical diagrams',1)[0]
parts=re.split(r'(?=^## \d+[A-Z]?\.\s)',concept,flags=re.M)
word_counts=[len(re.findall(r"\b[\w]+(?:['’\-][\w]+)*\b",x)) for x in parts if re.match(r'^## \d+[A-Z]?\.\s',x)]
assert len(word_counts)==23,word_counts
shallow=sum(x<300 for x in word_counts)
assert shallow==18,(shallow,word_counts)
assert len(re.findall(r'^### Q\d+\.',md,re.M))==30
assert len(re.findall(r'^\*\*Answer: [ABCD]\.\*\*',md,re.M))==30
assert len(re.findall(r'^## Question \d+:',md,re.M))==6
for image in ['cabinet-mission-architecture-cycle83.svg','diagrams/agrarian-comparison.svg','diagrams/constitutional-choices.svg','diagrams/three-phase-and-social-movements.svg']:
 assert md.count(']('+image+')')==1 and (src/image).is_file(),image

answers=(src/'six-structured-mains-answers-cycle83.md').read_text().split('## Cycle83 source-audit limitations',1)[0]
sections=re.split(r'(?m)^## Question [1-6]:',answers)[1:]
assert len(sections)==6
counts=[]
for section in sections:
 body='\n'.join(x for x in section.splitlines()[1:] if not x.startswith('**Answer blueprint:**'))
 body=re.sub(r'\*\*[^*]+\*\*\.?','',body)
 counts.append(len(re.findall(r"\b[\w]+(?:['’\-][\w]+)*\b",body)))
assert all(200<=x<=250 for x in counts),counts

pdf=src/'integrated-student-edition-cycle83.pdf'
subprocess.run([sys.executable,'scripts/render_topic_2_1_5_cycle83.py','--input',str(master),'--output',str(pdf)],check=True)
doc=fitz.open(pdf)
blank=[i+1 for i,p in enumerate(doc) if len(p.get_text().strip())<50]
outside=[]
for i,p in enumerate(doc):
 for b in p.get_text('blocks'):
  x0,y0,x1,y1=b[:4]
  if x0<-1 or y0<-1 or x1>p.rect.width+1 or y1>p.rect.height+1:outside.append(i+1)
assert 15<=len(doc)<=120 and not blank and not outside,(len(doc),blank,outside)

html=mistune.create_markdown(plugins=['table','strikethrough'])(md)
soup=BeautifulSoup(html,'html.parser')
seen={}
for h in soup.find_all(['h1','h2','h3']):
 slug=re.sub('[^a-z0-9]+','-',h.get_text(' ',strip=True).lower()).strip('-') or 'section'
 n=seen.get(slug,0);seen[slug]=n+1;h['id']=slug+(f'-{n}' if n else '')
prefix='<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>TGPSC Topic 2-1-5 Cycle83</title><style>body{font-family:system-ui,sans-serif;max-width:980px;margin:auto;padding:2rem;line-height:1.65;color:#172b3b}h1,h2,h3{color:#173e65}table{border-collapse:collapse;width:100%}th,td{border:1px solid #cad7df;padding:6px}img{max-width:100%;height:auto}nav a{margin-right:1rem}</style></head><body><nav><a href="../complete-notes.pdf">Original PDF</a><a href="integrated-student-edition-cycle83.pdf">Cycle83 PDF</a><a href="integrated-student-master-cycle83.md">Editable master</a><a href="../index.html">Topic portal</a></nav><p><strong>Original practice only. NOT academically approved.</strong></p>'
page=src/'integrated-student-cycle83.html'
page.write_text(prefix+str(soup)+'</body></html>')
checked=0;broken=[]
for el in BeautifulSoup(page.read_text(),'html.parser').find_all(['a','img']):
 u=el.get('href') or el.get('src') or ''
 if not u or urlsplit(u).scheme or u.startswith('#'):continue
 checked+=1
 if not (page.parent/unquote(urlsplit(u).path)).resolve().is_file():broken.append(u)
assert not broken,broken
qa={'cycle':83,'topic_id':'2-1-5','status':'ASSESSED_REBUILD_REQUIRED','original_pdf_sha256':original,'all_75_original_pdf_inventory_digest':inventory_digest,'original_topic_pdf_count':75,'readiness_json_count':75,'integrated_pdf_sha256':sha(pdf),'integrated_pdf_pages':len(doc),'pdf_blank_pages':blank,'pdf_out_of_bounds_pages':outside,'concept_count':23,'concepts_below_300':shallow,'concept_body_word_counts':word_counts,'mcq_count':30,'bounded_source_checked_keys':6,'bounded_source_checked_distractors':18,'mains_body_only_counts':counts,'html_local_links_checked':checked,'broken_html_links':broken,'diagrams_included_not_certified':4,'R1':'IN_PROGRESS_OFFICIAL_2024_PDF_INACCESSIBLE','R8':'IN_PROGRESS_PENDING_DOWNLOADED_ARTIFACT_AND_BROWSER_QA','R9':'NOT_STARTED','full_page_per_concept_met':False,'live_browser_accessibility_certified':False,'independent_academic_approvals':0}
evidence=pc/'academic-readiness/2-1-5-cycle83-ci-render-qa-2026-10-29.json'
evidence.write_text(json.dumps(qa,indent=2,ensure_ascii=False)+'\n')
manifest={'topic_id':'2-1-5','cycle':83,'academic_status':'not_approved','original_pdf_sha256':original,'integrated_pdf_sha256':sha(pdf),'integrated_pdf_pages':len(doc),'sha256':{p.name:sha(p) for p in [master,pdf,page,src/'source-register-cycle83.md',src/'original-explained-mcqs-cycle83.md',src/'six-structured-mains-answers-cycle83.md',src/'cabinet-mission-architecture-cycle83.svg']}}
(src/'integrated-cycle83-manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({'pages':len(doc),'pdf_sha256':sha(pdf),'mains_counts':counts,'concepts_below_300':shallow,'html_local_links_checked':checked,'original_pdf_count':75,'approval':0},indent=2))
