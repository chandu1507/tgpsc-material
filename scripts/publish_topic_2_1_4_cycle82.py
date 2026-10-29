"""Cycle82 guarded publisher: source-checked but NOT academically approved."""
from pathlib import Path
from urllib.parse import urlsplit, unquote
import hashlib, json, re, subprocess, sys
import fitz, mistune
from bs4 import BeautifulSoup

root=Path('Paper 2/Unit 1 - Indian History and Culture/Topic 4')
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
assert statuses=={'IN_PROGRESS':7,'ASSESSED_REBUILD_REQUIRED':64,'NOT_ASSESSED':4},statuses
assert index['not_assessed_count']==4
assert all((Path(t['path'])/'complete-notes.pdf').is_file() for t in topics)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
original=sha(root/'complete-notes.pdf')
assert original=='23b21afafae86150ceaa698bdbea3a6de53f354e0653804596d0d28d93813862',original
inventory='\n'.join(t['id']+':'+sha(Path(t['path'])/'complete-notes.pdf') for t in sorted(topics,key=lambda x:x['id']))
inventory_digest=hashlib.sha256(inventory.encode()).hexdigest()
master=src/'integrated-student-master-cycle82.md'
md=master.read_text()
assert 'NOT academically approved' in md
assert len(re.findall(r'^## (?:[1-9]|1[0-9])\. ',md,re.M))==19
assert len(re.findall(r'^### MCQ \d+\.',md,re.M))==30
assert len(re.findall(r'^\*\*Correct answer: [ABCD]\.',md,re.M))==30
assert len(re.findall(r'^## Question \d+\.',md,re.M))==6
for image in ['01-resistance-mechanisms.svg','02-nationalism-inclusion.svg','03-reform-strategies.svg']:
 assert md.count(']('+image+')')==1 and (src/image).is_file(),image
concept=md.split('# Detailed textbook-style concepts',1)[1].split('# Original analytical diagrams',1)[0]
parts=re.split(r'(?=^## (?:[1-9]|1[0-9])\. )',concept,flags=re.M)
word_counts=[len(x.split()) for x in parts if re.match(r'^## \d+\. ',x)]
assert len(word_counts)==19
shallow=sum(x<300 for x in word_counts)
assert shallow==13,(shallow,word_counts)
answers=(src/'structured-mains-answers-ii.md').read_text()
sections=re.split(r'(?m)^## Question [1-6]\. ',answers)[1:]
assert len(sections)==6
counts=[]
for section in sections:
 body='\n'.join(section.splitlines()[1:])
 body=re.sub(r'\*\*[^*]+\*\*\.?','',body)
 counts.append(len(re.findall(r"\b[\w]+(?:['’\-][\w]+)*\b",body)))
assert all(200<=x<=250 for x in counts),counts

pdf=src/'integrated-student-edition-cycle82.pdf'
subprocess.run([sys.executable,'scripts/render_topic_2_1_4_cycle82.py','--input',str(master),'--output',str(pdf)],check=True)
doc=fitz.open(pdf)
blank=[i+1 for i,p in enumerate(doc) if len(p.get_text().strip())<60]
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
prefix='<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>TGPSC Topic 2-1-4 Cycle82</title><style>body{font-family:system-ui,sans-serif;max-width:980px;margin:auto;padding:2rem;line-height:1.65;color:#172b3b}h1,h2,h3{color:#173e65}table{border-collapse:collapse;width:100%}th,td{border:1px solid #cad7df;padding:6px}img{max-width:100%;height:auto}nav a{margin-right:1rem}</style></head><body><nav><a href="../complete-notes.pdf">Original PDF</a><a href="integrated-student-edition-cycle82.pdf">Cycle82 PDF</a><a href="integrated-student-master-cycle82.md">Editable master</a><a href="../index.html">Topic portal</a></nav><p><strong>Original practice only. NOT academically approved.</strong></p>'
page=src/'integrated-student-cycle82.html'
page.write_text(prefix+str(soup)+'</body></html>')
checked=0;broken=[]
for el in BeautifulSoup(page.read_text(),'html.parser').find_all(['a','img']):
 u=el.get('href') or el.get('src') or ''
 if not u or urlsplit(u).scheme or u.startswith('#'):continue
 checked+=1
 if not (page.parent/unquote(urlsplit(u).path)).resolve().is_file():broken.append(u)
assert not broken,broken
qa={'cycle':82,'topic_id':'2-1-4','status':'ASSESSED_REBUILD_REQUIRED','original_pdf_sha256':original,'all_75_original_pdf_inventory_digest':inventory_digest,'original_topic_pdf_count':75,'readiness_json_count':75,'integrated_pdf_sha256':sha(pdf),'integrated_pdf_pages':len(doc),'pdf_blank_pages':blank,'pdf_out_of_bounds_pages':outside,'concept_count':19,'concepts_below_300':shallow,'concept_body_word_counts':word_counts,'mcq_count':30,'bounded_source_checked_keys':8,'bounded_source_checked_distractors':24,'mains_body_only_counts':counts,'html_local_links_checked':checked,'broken_html_links':broken,'diagrams_included_not_certified':3,'R1':'IN_PROGRESS_OFFICIAL_2024_PDF_403','R8':'IN_PROGRESS_PENDING_DOWNLOADED_ARTIFACT_AND_BROWSER_QA','R9':'NOT_STARTED','full_page_per_concept_met':False,'live_browser_accessibility_certified':False,'independent_academic_approvals':0}
evidence=pc/'academic-readiness/2-1-4-cycle82-ci-render-qa-2026-10-29.json'
evidence.write_text(json.dumps(qa,indent=2,ensure_ascii=False)+'\n')
manifest={'topic_id':'2-1-4','cycle':82,'academic_status':'not_approved','original_pdf_sha256':original,'integrated_pdf_sha256':sha(pdf),'integrated_pdf_pages':len(doc),'sha256':{p.name:sha(p) for p in [master,pdf,page,src/'source-evidence-audit-ii.md',src/'original-explained-mcqs-ii.md',src/'structured-mains-answers-ii.md']}}
(src/'integrated-cycle82-manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({'pages':len(doc),'pdf_sha256':sha(pdf),'counts':counts,'concepts_below_300':shallow,'html_local_links_checked':checked,'original_pdf_count':75,'approval':0},indent=2))
