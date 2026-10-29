"""Cycle77 guarded 6-3-4 integrated publication. Does NOT establish academic approval."""
from pathlib import Path
from urllib.parse import urlsplit,unquote
import hashlib,json,re,subprocess,sys
import fitz,mistune
from bs4 import BeautifulSoup

root=Path('Paper 6/Unit 3 - State Formation (1991–2014)/Topic 4')
src=root/'source'
checkpoint=json.loads(Path('project-control/PRODUCTION-CHECKPOINT.json').read_text())
index=json.loads(Path('project-control/ACADEMIC_READINESS_75_TOPIC_STATUS_INDEX.json').read_text())
assert len(checkpoint['topics'])==checkpoint['total_topics']==index['total_topics']==75
assert len(set(x['id'] for x in checkpoint['topics']))==75
assert len(index['paths'])==len(set(index['paths']))==75
assert len(list(Path('project-control/academic-readiness').glob('[2-6]-[1-3]-[1-5].json')))==75
assert sum(t['readiness_status']=='IN_PROGRESS' for t in checkpoint['topics'])==7
assert sum(t['readiness_status']=='ASSESSED_REBUILD_REQUIRED' for t in checkpoint['topics'])==59
assert sum(t['readiness_status']=='NOT_ASSESSED' for t in checkpoint['topics'])==9
assert checkpoint['academically_approved']==index['independently_academically_approved_count']==0
assert all((Path(t['path'])/'complete-notes.pdf').is_file() for t in checkpoint['topics'])
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
original=sha(root/'complete-notes.pdf')
assert original=='13b1609daccd0949df1c7fade614d1ef7d0e453f076aa92b189faf3a055c17d0'
md=(src/'complete-notes.md').read_text()
practice=(src/'original-practice.md').read_text().strip()
answers=(src/'complete-model-answers.md').read_text().strip()
refs=(src/'references.md').read_text().strip()
assert practice in md and answers in md and refs in md

heads=list(re.finditer(r'^### (\d+)\. (.+)$',md,re.M))
concepts=[]
for i,m in enumerate(heads):
 end=heads[i+1].start() if i+1<len(heads) else md.find('## ',m.end())
 end=end if end>=0 else len(md)
 body=md[m.end():end]
 concepts.append({'section':int(m.group(1)),'words':len(re.findall(r"\b[\w’'-]+\b",body))})
assert len(concepts)==40 and [x['section'] for x in concepts]==list(range(1,41))
assert sum(x['words']<300 for x in concepts)==32
assert all(concepts[n-1]['words']>=300 for n in [26,27,28,31,32,36,37,40])
keys=re.findall(r'^\*\*Answer: ([A-D])\.',practice,re.M)
assert len(keys)==30 and len(re.findall(r'^\*\*Q\d+\.',practice,re.M))==30
assert {k:keys.count(k) for k in 'ABCD'}=={'A':8,'B':7,'C':7,'D':8}
# Six answers counted excluding question headings and subsection labels.
secs=re.split(r'(?m)^## Question \d+:',answers)[1:]
assert len(secs)==6
counts=[]
for sec in secs:
 body='\n'.join(sec.splitlines()[2:]);body=re.sub(r'\*\*[^*]+\*\*\.?','',body)
 counts.append(len(re.findall(r"\b[\w]+(?:['’\-][\w]+)*\b",body)))
assert counts==[211,211,210,210,211,210],counts

pdf=src/'integrated-student-edition-cycle77.pdf'
subprocess.run([sys.executable,'scripts/render_topic_6_3_4_integrated.py','--input',str(src/'complete-notes.md'),'--output',str(pdf)],check=True)
doc=fitz.open(pdf)
blank=[i+1 for i,p in enumerate(doc) if len(p.get_text().strip())<60]
outside=[]
for i,p in enumerate(doc):
 for b in p.get_text('blocks'):
  x0,y0,x1,y1=b[:4]
  if x0 < -1 or y0 < -1 or x1 > p.rect.width+1 or y1 > p.rect.height+1:outside.append(i+1)
embedded=sum(len(p.get_images()) for p in doc)
assert 15<=len(doc)<=100 and not blank and not outside and embedded>=3,(len(doc),blank,outside,embedded)

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
 h['id']=slug+(f'-{n}' if n else '')
header='<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>TGPSC 6-3-4</title><style>body{font-family:system-ui,sans-serif;max-width:980px;margin:auto;padding:2rem;line-height:1.65;color:#172b3b}h1,h2,h3{color:#173e65}table{border-collapse:collapse;width:100%}th,td{border:1px solid #cad7df;padding:6px}img{max-width:100%;height:auto}nav a{margin-right:1rem}</style></head><body><nav><a href="complete-notes.pdf">Original PDF</a><a href="source/integrated-student-edition-cycle77.pdf">Integrated PDF</a><a href="source/complete-notes.md">Editable master</a><a href="../../../index.html">Study portal</a></nav><p><strong>Original practice only. NOT academically approved.</strong></p>'
(root/'index.html').write_text(header+str(soup)+'</body></html>')
checked=0;bad=[]
for el in BeautifulSoup((root/'index.html').read_text(),'html.parser').find_all(['a','img']):
 u=el.get('href') or el.get('src') or ''
 if not u or urlsplit(u).scheme or u.startswith('#'):continue
 checked+=1
 path=unquote(urlsplit(u).path)
 if not (root/path).resolve().is_file():bad.append(path)
assert not bad,bad
qa={'cycle':77,'topic_id':'6-3-4','original_pdf_sha256':original,'integrated_pdf_sha256':sha(pdf),'integrated_pdf_pages':len(doc),'concept_count':40,'concept_word_counts':concepts,'concepts_below_300':32,'mcq_count':30,'key_distribution':{k:keys.count(k) for k in 'ABCD'},'mains_body_only_counts':counts,'embedded_images':embedded,'blank_pages':blank,'out_of_bounds_pages':outside,'local_links_checked':checked,'broken_links':bad,'all_75_original_pdf_files_present':True,'full_page_per_concept_met':False,'source_checked_mcq_keys':6,'source_checked_distractors':18,'mains_claim_level_review_complete':False,'browser_accessibility_certified':False,'R8':'IN_PROGRESS_PENDING_DOWNLOADED_ARTIFACT_QA','independent_academic_approvals':0}
(root/'QA-REPORT.md').write_text('# Cycle77 Topic 6-3-4 deterministic publication QA\n\n'+json.dumps(qa,indent=2)+'\n')
(root/'README.md').write_text('# Cultural Revivalism, Social Participation and Major Protest Events\n\nOriginal PDF preserved. Cycle77 source-labelled expansions in eight sections, corrected six structured mains answers, 30 original explained practice MCQs, three existing diagrams and a synchronized integrated PDF. **32/40 concepts remain below 300 words; this is NOT academically approved.** Six MCQ keys and 18 distractors were bounded source-checked. Remaining questions and mains claim sets require independent review.\n\n[Original PDF](complete-notes.pdf) | [Integrated PDF](source/integrated-student-edition-cycle77.pdf) | [Editable master](source/complete-notes.md)\n')
manifest=json.loads((root/'manifest.json').read_text())
manifest.update({'academic_status':'not_approved','cycle77_partial_rebuild':True,'concept_count':40,'concepts_below_300':32,'integrated_pdf_pages':len(doc),'integrated_pdf_sha256':sha(pdf),'independent_academic_approvals':0,'full_page_per_concept_met':False})
manifest['sha256']={str(p.relative_to(root)):sha(p) for p in sorted(root.rglob('*')) if p.is_file() and p.name!='manifest.json'}
(root/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
evidence=Path('project-control/academic-readiness/6-3-4-cycle77-ci-render-qa-2026-10-29.json')
evidence.write_text(json.dumps(qa,indent=2)+'\n')
print(json.dumps({k:v for k,v in qa.items() if k!='concept_word_counts'},indent=2))
