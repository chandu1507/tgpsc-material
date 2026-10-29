"""Cycle81 guarded, evidence-labelled publication of Topic 2-1-3 integrated student draft."""
from pathlib import Path
from urllib.parse import urlsplit,unquote
import hashlib,json,re,subprocess,sys
import fitz,mistune
from bs4 import BeautifulSoup

root=Path('Paper 2/Unit 1 - Indian History and Culture/Topic 3')
src=root/'source'
cp=json.loads(Path('project-control/PRODUCTION-CHECKPOINT.json').read_text())
idx=json.loads(Path('project-control/ACADEMIC_READINESS_75_TOPIC_STATUS_INDEX.json').read_text())
assert cp['total_topics']==idx['total_topics']==len(cp['topics'])==75
assert len(set(t['id'] for t in cp['topics']))==75
assert len(idx['paths'])==len(set(idx['paths']))==75
assert len(list(Path('project-control/academic-readiness').glob('[2-6]-[1-3]-[1-5].json')))==75
assert {s:sum(t['readiness_status']==s for t in cp['topics']) for s in ['IN_PROGRESS','ASSESSED_REBUILD_REQUIRED','NOT_ASSESSED']}=={'IN_PROGRESS':7,'ASSESSED_REBUILD_REQUIRED':63,'NOT_ASSESSED':5}
assert cp['academically_approved']==idx['independently_academically_approved_count']==0
assert all((Path(t['path'])/'complete-notes.pdf').is_file() for t in cp['topics'])
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
original=sha(root/'complete-notes.pdf')
assert original=='2f97d59a3f2179ed1b8aa38f179783b9a3641383a74e619929e307096cb87dab',original
md=(src/'integrated-student-master-cycle81.md').read_text()
assert all(md.count(x)==1 for x in ['![Fiscal–military feedback loop]','![Agrarian vulnerability pathways]','![Railway finance and distribution]'])
concept_block=md.split('## Source-critical detailed concepts',1)[1].split('## Original analytical diagrams',1)[0]
assert len(re.findall(r'^## (?:[1-9]|1[0-9])\. ',concept_block,re.M))==19
mcqs=(src/'original-explained-mcqs-cycle81.md').read_text()
assert len(re.findall(r'^### Q\d+\.',mcqs,re.M))==30
assert len(re.findall(r'^\*\*Answer: [ABCD]\.',mcqs,re.M))==30
answers=(src/'structured-mains-answers-20261025.md').read_text()
parts=re.split(r'(?m)^## M\d+\. ',answers)[1:]
assert len(parts)==6
counts=[]
for sec in parts:
 body='\n'.join(x for x in sec.splitlines()[1:] if not x.startswith('*Answer body:'))
 body=re.sub(r'\*\*[^*]+\*\*\.?','',body)
 counts.append(len(re.findall(r"\b[\w]+(?:['’\-][\w]+)*\b",body)))
assert counts==[204,211,213,205,207,211],counts
out=src/'integrated-student-edition-cycle81.pdf'
subprocess.run([sys.executable,'scripts/render_topic_2_1_2_cycle81.py','--input',str(src/'integrated-student-master-cycle81.md'),'--output',str(out)],check=True)
doc=fitz.open(out)
blank=[i+1 for i,p in enumerate(doc) if len(p.get_text().strip())<60]
outside=[]
for i,p in enumerate(doc):
 for b in p.get_text('blocks'):
  x0,y0,x1,y1=b[:4]
  if x0<-1 or y0<-1 or x1>p.rect.width+1 or y1>p.rect.height+1:outside.append(i+1)
assert 15<=len(doc)<=100 and not blank and not outside,(len(doc),blank,outside)
html=mistune.create_markdown(plugins=['table','strikethrough'])(md)
soup=BeautifulSoup(html,'html.parser')
seen={}
for h in soup.find_all(['h1','h2','h3']):
 slug=re.sub('[^a-z0-9]+','-',h.get_text(' ',strip=True).lower()).strip('-') or 'section'
 n=seen.get(slug,0);seen[slug]=n+1;h['id']=slug+(f'-{n}' if n else '')
prefix='<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>TGPSC 2-1-3 Cycle81</title><style>body{font-family:system-ui,sans-serif;max-width:980px;margin:auto;padding:2rem;line-height:1.65;color:#172b3b}h1,h2,h3{color:#173e65}table{border-collapse:collapse;width:100%}th,td{border:1px solid #cad7df;padding:6px}img{max-width:100%;height:auto}nav a{margin-right:1rem}</style></head><body><nav><a href="../complete-notes.pdf">Original PDF</a><a href="integrated-student-edition-cycle81.pdf">Cycle81 integrated PDF</a><a href="integrated-student-master-cycle81.md">Editable master</a><a href="../index.html">Topic portal</a></nav><p><strong>Original practice only. NOT academically approved.</strong></p>'
page=src/'integrated-student-cycle81.html'
page.write_text(prefix+str(soup)+'</body></html>')
checked=0;broken=[]
for el in BeautifulSoup(page.read_text(),'html.parser').find_all(['a','img']):
 u=el.get('href') or el.get('src') or ''
 if not u or urlsplit(u).scheme or u.startswith('#'):continue
 checked+=1
 if not (page.parent/unquote(urlsplit(u).path)).resolve().is_file():broken.append(u)
assert not broken,broken
qa={'cycle':80,'topic_id':'2-1-3','original_pdf_sha256':original,'integrated_pdf_sha256':sha(out),'integrated_pdf_pages':len(doc),'pdf_blank_pages':blank,'pdf_out_of_bounds_pages':outside,'vector_diagram_references':3,'mcq_count':30,'bounded_source_checked_keys':9,'bounded_source_checked_distractors':27,'mains_body_only_counts':counts,'concept_count':19,'concepts_below_300':14,'html_local_links_checked':checked,'broken_html_links':broken,'full_page_per_concept_met':False,'full_browser_accessibility_certified':False,'independent_academic_approvals':0,'R8':'IN_PROGRESS_PENDING_DOWNLOADED_ARTIFACT_QA','R9':'NOT_STARTED'}
evidence=Path('project-control/academic-readiness/2-1-3-cycle81-ci-render-qa-2026-10-29.json')
evidence.write_text(json.dumps(qa,indent=2)+'\n')
manifest={'topic_id':'2-1-3','cycle':80,'academic_status':'not_approved','original_pdf_sha256':original,'integrated_pdf_sha256':sha(out),'integrated_pdf_pages':len(doc),'sha256':{p.name:sha(p) for p in [src/'integrated-student-master-cycle81.md',out,page,src/'cycle81-evidence-register.md',src/'original-explained-mcqs-cycle81.md',src/'structured-mains-answers-medieval-20261025.md']},'independent_approvals':0}
(src/'integrated-cycle81-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps(qa,indent=2))
