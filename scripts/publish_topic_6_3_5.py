"""Cycle78 guarded Topic 6-3-5 PDF/HTML publication; never academic approval."""
from pathlib import Path
from urllib.parse import urlsplit,unquote
import hashlib,json,re,subprocess,sys
import fitz,mistune
from bs4 import BeautifulSoup
root=Path('Paper 6/Unit 3 - State Formation (1991–2014)/Topic 5')
src=root/'source'
checkpoint=json.loads(Path('project-control/PRODUCTION-CHECKPOINT.json').read_text())
index=json.loads(Path('project-control/ACADEMIC_READINESS_75_TOPIC_STATUS_INDEX.json').read_text())
assert len(checkpoint['topics'])==checkpoint['total_topics']==index['total_topics']==75
assert len(set(x['id'] for x in checkpoint['topics']))==75
assert len(index['paths'])==len(set(index['paths']))==75
assert len(list(Path('project-control/academic-readiness').glob('[2-6]-[1-3]-[1-5].json')))==75
for status,n in [('IN_PROGRESS',7),('ASSESSED_REBUILD_REQUIRED',60),('NOT_ASSESSED',8)]:
 assert sum(t['readiness_status']==status for t in checkpoint['topics'])==n,status
assert checkpoint['academically_approved']==index['independently_academically_approved_count']==0
assert all((Path(t['path'])/'complete-notes.pdf').is_file() for t in checkpoint['topics'])
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
original=sha(root/'complete-notes.pdf')
assert original=='6d044094ceff7305ad9f9cd67fb59d6695d43b53aa5f4911cd4e5b29e5c14f90',original
md=(src/'complete-notes.md').read_text()
practice=(src/'original-practice.md').read_text().strip()
answers=(src/'complete-model-answers.md').read_text().strip()
refs=(src/'references.md').read_text().strip()
detailed=(src/'detailed-notes.md').read_text().strip()
assert all(s in md for s in (practice,answers,refs,detailed))
heads=list(re.finditer(r'^### (\d+)\. (.+)$',detailed,re.M))
concepts=[]
for i,m in enumerate(heads):
 end=heads[i+1].start() if i+1<len(heads) else len(detailed)
 body=detailed[m.end():end]
 concepts.append({'section':int(m.group(1)),'words':len(re.findall(r"\b[\w]+(?:['’\-][\w]+)*\b",body))})
assert len(concepts)==38 and [x['section'] for x in concepts]==list(range(1,39))
assert sum(x['words']<300 for x in concepts)==30,concepts
assert all(concepts[n-1]['words']>=300 for n in [11,12,18,19,20,21,23,24])
keys=re.findall(r'^\*\*Answer: ([A-D])\.',practice,re.M)
assert len(keys)==30 and len(re.findall(r'^### MCQ \d+\.',practice,re.M))==30
assert {k:keys.count(k) for k in 'ABCD'}=={'A':7,'B':10,'C':11,'D':2}
sections=re.split(r'(?m)^### Mains Answer \d+\. ',answers)[1:]
assert len(sections)==6
counts=[]
for sec in sections:
 body='\n'.join(sec.splitlines()[1:])
 body=re.sub(r'\*\*[^*]+\*\*\.?','',body)
 counts.append(len(re.findall(r"\b[\w]+(?:['’\-][\w]+)*\b",body)))
assert counts==[228,219,212,200,214,216],counts
pdf=src/'integrated-student-edition-cycle78.pdf'
subprocess.run([sys.executable,'scripts/render_topic_6_3_5_integrated.py','--input',str(src/'complete-notes.md'),'--output',str(pdf)],check=True)
doc=fitz.open(pdf)
blank=[i+1 for i,p in enumerate(doc) if len(p.get_text().strip())<60]
outside=[]
for i,p in enumerate(doc):
 for b in p.get_text('blocks'):
  x0,y0,x1,y1=b[:4]
  if x0<-1 or y0<-1 or x1>p.rect.width+1 or y1>p.rect.height+1:outside.append(i+1)
embedded=sum(len(p.get_images()) for p in doc)
assert 15<=len(doc)<=100 and not blank and not outside and embedded>=3,(len(doc),blank,outside,embedded)
html=mistune.create_markdown(plugins=['table','strikethrough'])(md)
soup=BeautifulSoup(html,'html.parser')
for img in soup.find_all('img'):
 u=img.get('src','')
 if u.startswith('source/diagrams/') or u.startswith('../diagrams/') or u.startswith('diagrams/'):
  img['src']='source/diagrams/'+u.rsplit('/',1)[-1]
seen={}
for h in soup.find_all(['h1','h2','h3']):
 slug=re.sub('[^a-z0-9]+','-',h.get_text(' ',strip=True).lower()).strip('-') or 'section'
 n=seen.get(slug,0);seen[slug]=n+1
 h['id']=slug+(f'-{n}' if n else '')
header='<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>TGPSC 6-3-5</title><style>body{font-family:system-ui,sans-serif;max-width:980px;margin:auto;padding:2rem;line-height:1.65;color:#172b3b}h1,h2,h3{color:#173e65}table{border-collapse:collapse;width:100%}th,td{border:1px solid #cad7df;padding:6px}img{max-width:100%;height:auto}nav a{margin-right:1rem}</style></head><body><nav><a href="complete-notes.pdf">Original PDF</a><a href="source/integrated-student-edition-cycle78.pdf">Integrated PDF</a><a href="source/complete-notes.md">Editable master</a><a href="../../../index.html">Study portal</a></nav><p><strong>Original practice only. NOT academically approved.</strong></p>'
(root/'index.html').write_text(header+str(soup)+'</body></html>')
checked=0;bad=[]
for el in BeautifulSoup((root/'index.html').read_text(),'html.parser').find_all(['a','img']):
 u=el.get('href') or el.get('src') or ''
 if not u or urlsplit(u).scheme or u.startswith('#'):continue
 checked+=1
 path=unquote(urlsplit(u).path)
 if not (root/path).resolve().is_file():bad.append(path)
assert not bad,bad
qa={'cycle':78,'topic_id':'6-3-5','original_pdf_sha256':original,'integrated_pdf_sha256':sha(pdf),'integrated_pdf_pages':len(doc),'concept_count':38,'concept_word_counts':concepts,'concepts_below_300':30,'mcq_count':30,'key_distribution':{k:keys.count(k) for k in 'ABCD'},'mains_body_only_counts':counts,'embedded_images':embedded,'blank_pages':blank,'out_of_bounds_pages':outside,'local_links_checked':checked,'broken_links':bad,'all_75_original_pdf_files_present':True,'full_page_per_concept_met':False,'bounded_source_checked_mcq_keys':10,'bounded_source_checked_distractors':30,'mains_claim_level_review_complete':False,'browser_accessibility_certified':False,'R8':'IN_PROGRESS_PENDING_DOWNLOADED_ARTIFACT_QA','independent_academic_approvals':0}
(root/'QA-REPORT.md').write_text('# Cycle78 Topic 6-3-5 deterministic publication QA\n\n'+json.dumps(qa,indent=2)+'\n')
(root/'README.md').write_text('# Parliamentary Process, Reorganisation Act and First Telangana Government\n\nOriginal PDF preserved. Cycle78 eight source-critical expansions, 30 original practice MCQs, six mains answers, three existing diagrams and synchronized integrated PDF. **30/38 concepts still below 300 words; NOT academically approved.** Ten MCQ keys and 30 distractors bounded checked; all mains claim sets need independent review.\n\n[Original PDF](complete-notes.pdf) | [Integrated PDF](source/integrated-student-edition-cycle78.pdf) | [Editable master](source/complete-notes.md)\n')
manifest={'topic_id':'6-3-5','academic_status':'not_approved','cycle78_partial_rebuild':True,'concept_count':38,'concepts_below_300':30,'integrated_pdf_pages':len(doc),'integrated_pdf_sha256':sha(pdf),'original_pdf_sha256':original,'independent_academic_approvals':0,'full_page_per_concept_met':False}
manifest['sha256']={str(p.relative_to(root)):sha(p) for p in sorted(root.rglob('*')) if p.is_file() and p.name!='manifest.json'}
(root/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
evidence=Path('project-control/academic-readiness/6-3-5-cycle78-ci-render-qa-2026-10-29.json')
evidence.write_text(json.dumps(qa,indent=2)+'\n')
print(json.dumps({k:v for k,v in qa.items() if k!='concept_word_counts'},indent=2))
