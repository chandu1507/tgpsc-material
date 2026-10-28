"""Cycle74 guarded Topic 6-3-1 PDF/HTML publication. Never infer academic approval."""
from pathlib import Path
from urllib.parse import urlsplit, unquote
import hashlib, json, re, subprocess, sys
import fitz, mistune
from bs4 import BeautifulSoup

root=Path('Paper 6/Unit 3 - State Formation (1991–2014)/Topic 1')
src=root/'source'
cp=json.loads(Path('project-control/PRODUCTION-CHECKPOINT.json').read_text())
ix=json.loads(Path('project-control/ACADEMIC_READINESS_75_TOPIC_STATUS_INDEX.json').read_text())
assert cp['total_topics']==ix['total_topics']==len(cp['topics'])==75
assert len({t['id'] for t in cp['topics']})==75
assert len(ix['paths'])==len(set(ix['paths']))==75
assert len(list(Path('project-control/academic-readiness').glob('[2-6]-[1-3]-[1-5].json')))==75
assert sum(t['readiness_status']=='ASSESSED_REBUILD_REQUIRED' for t in cp['topics'])==56
assert ix['not_assessed_count']==12
assert cp['academically_approved']==ix['independently_academically_approved_count']==0
assert all((Path(t['path'])/'complete-notes.pdf').is_file() for t in cp['topics'])
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
original=sha(root/'complete-notes.pdf')
assert original=='a84ba74ea6ab0c48598d65b246694bce1b74f23faa53a114e4e239a02c17846e'
md=(src/'complete-notes.md').read_text()
practice=(src/'original-practice.md').read_text().strip()
references=(src/'references.md').read_text().strip()
assert practice in md and references in md
heads=list(re.finditer(r'^## (\d+)\. ([^\n]+)\n',md,re.M))
concepts=[]
for j,m in enumerate(heads):
    n=int(m.group(1))
    if 1<=n<=41:
        end=heads[j+1].start() if j+1<len(heads) else len(md)
        body=md[m.end():end].strip()
        concepts.append({'section':n,'words':len(body.split())})
assert len(concepts)==41 and [x['section'] for x in concepts]==list(range(1,42))
assert sum(x['words']<300 for x in concepts)==38,concepts
for n in [11,24,33]:assert concepts[n-1]['words']>=300
qblocks=list(re.finditer(r'^\*\*Q(\d+)\. (.*?)\*\*\n([\s\S]*?)(?=^\*\*Q\d+\.|\Z)',practice,re.M))
assert len(qblocks)==30
keys=[]
for j,m in enumerate(qblocks,1):
    assert int(m.group(1))==j
    block=m.group(3)
    assert all(re.search(r'^- '+c+r'\.',block,re.M) for c in 'ABCD')
    ans=re.search(r'^\*\*Answer: ([A-D])\.',block,re.M)
    assert ans
    keys.append(ans.group(1))
assert {k:keys.count(k) for k in 'ABCD'}=={'A':10,'B':18,'C':2,'D':0}
mains=(src/'complete-model-answers.md').read_text()
answers=re.split(r'^## Mains model answer \d+ — .*$',mains,flags=re.M)[1:]
counts=[len(a.split('**Answer length:**')[0].strip().split()) for a in answers]
assert counts==[201,209,213,203,207,203]
images=re.findall(r'!\[[^\]]*\]\(([^)]+)\)',md)
assert len(images)==3 and all((src/u).resolve().is_file() for u in images)
pdf=src/'integrated-student-edition-cycle74.pdf'
subprocess.run([sys.executable,'scripts/render_topic_6_3_1_integrated.py','--input',str(src/'complete-notes.md'),'--output',str(pdf)],check=True)
doc=fitz.open(pdf)
blank=[i+1 for i,p in enumerate(doc) if len(p.get_text().strip())<60]
outside=[]
for i,p in enumerate(doc):
    for b in p.get_text('blocks'):
        x0,y0,x1,y1=b[:4]
        if x0<-1 or y0<-1 or x1>p.rect.width+1 or y1>p.rect.height+1:outside.append(i+1)
image_count=sum(len(p.get_images()) for p in doc)
assert 20<=len(doc)<=90 and not blank and not outside and image_count>=3
html=mistune.create_markdown(plugins=['table','strikethrough'])(md)
soup=BeautifulSoup(html,'html.parser')
for img in soup.find_all('img'):
    u=img.get('src','')
    if u.startswith('../diagrams/') or u.startswith('diagrams/'):img['src']='diagrams/'+u.rsplit('/',1)[-1]
seen={}
for h in soup.find_all(['h1','h2','h3']):
    slug=re.sub('[^a-z0-9]+','-',h.get_text(' ',strip=True).lower()).strip('-') or 'section'
    n=seen.get(slug,0);seen[slug]=n+1
    h['id']=slug+(f'-{n}' if n else '')
header='<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>TGPSC 6-3-1</title><style>body{font-family:system-ui,sans-serif;max-width:980px;margin:auto;padding:2rem;line-height:1.65;color:#172b3b}h1,h2,h3{color:#173e65}table{border-collapse:collapse;width:100%}th,td{border:1px solid #cad7df;padding:6px}img{max-width:100%;height:auto}nav a{margin-right:1rem}</style></head><body><nav><a href="complete-notes.pdf">Original PDF</a><a href="source/integrated-student-edition-cycle74.pdf">Integrated PDF</a><a href="source/complete-notes.md">Editable master</a><a href="../../../index.html">Study portal</a></nav><p><strong>Original practice only. NOT academically approved.</strong></p>'
(root/'index.html').write_text(header+str(soup)+'</body></html>')
checked=0;bad=[]
for el in BeautifulSoup((root/'index.html').read_text(),'html.parser').find_all(['a','img']):
    u=el.get('href') or el.get('src') or ''
    if not u or urlsplit(u).scheme or u.startswith('#'):continue
    checked+=1
    path=unquote(urlsplit(u).path)
    if not (root/path).resolve().is_file():bad.append(path)
assert not bad,bad
qa={'cycle':74,'topic_id':'6-3-1','original_pdf_sha256':original,'integrated_pdf_sha256':sha(pdf),'integrated_pdf_pages':len(doc),'concept_count':41,'concept_word_counts':concepts,'concepts_below_300':38,'mcq_count':30,'key_distribution':{k:keys.count(k) for k in 'ABCD'},'mains_body_only_counts':counts,'embedded_images':image_count,'blank_pages':blank,'out_of_bounds_pages':outside,'local_links_checked':checked,'broken_links':bad,'all_75_original_pdf_files_present':True,'full_page_per_concept_met':False,'independent_keys_verified':0,'independent_distractors_verified':0,'mains_claim_level_review_complete':False,'browser_accessibility_certified':False,'R8':'IN_PROGRESS_PENDING_DOWNLOADED_ARTIFACT_QA','independent_academic_approvals':0}
(root/'QA-REPORT.md').write_text('# Cycle74 Topic 6-3-1 deterministic publication QA\n\n'+json.dumps(qa,indent=2)+'\n')
(root/'README.md').write_text('# Public Awakening, Civil Society and Telangana Identity (1988–2004)\n\nOriginal 24-page PDF preserved. Cycle74 source-critical editable master, 30 original explained practice MCQs, six structured mains answers, three original diagrams, and a deterministic integrated PDF. **38/41 concepts remain under 300 words; this is NOT academically approved.** Exact 1997 Suryapet dates conflict in secondary sources; no signed organiser minutes obtained.\n\n[Original PDF](complete-notes.pdf) | [Integrated PDF](source/integrated-student-edition-cycle74.pdf) | [Editable master](source/complete-notes.md)\n')
manifest=json.loads((root/'manifest.json').read_text())
manifest.update({'academic_status':'not_approved','cycle74_partial_rebuild':True,'concept_count':41,'concepts_below_300':38,'integrated_pdf_pages':len(doc),'integrated_pdf_sha256':sha(pdf),'independent_academic_approvals':0,'full_page_per_concept_met':False})
manifest['sha256']={str(p.relative_to(root)):sha(p) for p in sorted(root.rglob('*')) if p.is_file() and p.name!='manifest.json'}
(root/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
evidence=Path('project-control/academic-readiness/6-3-1-cycle74-ci-render-qa-2026-10-29.json')
evidence.write_text(json.dumps(qa,indent=2)+'\n')
print(json.dumps({k:v for k,v in qa.items() if k not in ('concept_word_counts',)},indent=2))
