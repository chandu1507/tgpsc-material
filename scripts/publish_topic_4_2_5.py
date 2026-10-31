from pathlib import Path
import hashlib, json, re, subprocess, sys
from urllib.parse import urlsplit, unquote
from bs4 import BeautifulSoup
import mistune, fitz

root=Path('Paper 4/Unit 2 - Telangana Economy/Topic 5')
src=root/'source'
cp=json.loads(Path('project-control/PRODUCTION-CHECKPOINT.json').read_text())
ix=json.loads(Path('project-control/ACADEMIC_READINESS_75_TOPIC_STATUS_INDEX.json').read_text())
assert cp['total_topics']==ix['total_topics']==len(cp['topics'])==75
assert len({t['id'] for t in cp['topics']})==75
assert len(list(Path('project-control/academic-readiness').glob('[2-6]-[1-3]-[1-5].json')))==75
from collections import Counter
counts=Counter(t['readiness_status'] for t in cp['topics'])
assert counts['IN_PROGRESS']==len(ix['pilot_in_progress'])
assert counts['ASSESSED_REBUILD_REQUIRED']==len(ix['assessed_rebuild_required'])
assert counts['NOT_ASSESSED']==ix['not_assessed_count']
assert sum(counts.values())==75 and len(ix['paths'])==len(set(ix['paths']))==75
assert cp['academically_approved']==ix['independently_academically_approved_count']==0
orig=hashlib.sha256((root/'complete-notes.pdf').read_bytes()).hexdigest()
assert orig=='cf32e25f46c9081db658e3fdd1b8fa52497dedcedad039d238d054a3416433a6',orig
parts=['syllabus-and-summary.md','quick-revision.md','detailed-notes.md','visual-learning.md','original-mcqs.md','answer-blueprints.md','mains-model-answers.md','verified-pyqs.md','sources-and-audit.md']
md='\n\n---\n\n'.join((src/n).read_text().strip() for n in parts)+'\n'
# The single editable integrated master is a deterministic join of the nine sources.
if (src/'complete-notes.md').read_text()!=md:
 (src/'complete-notes.md').write_text(md)
concepts=re.split(r'(?m)^## \d+\. ',(src/'detailed-notes.md').read_text())[1:]
assert len(concepts)==17
word_counts=[len(re.findall(r"\b[\w]+(?:[-'][\w]+)*\b",x)) for x in concepts]
assert min(word_counts)>=300,word_counts
q=(src/'original-mcqs.md').read_text()
assert len(re.findall(r'(?m)^### MCQ \d+\.',q))==30
keys=re.findall(r'\*\*Correct answer: ([ABCD])\.',q)
assert len(keys)==30
for n in range(1,31):
 block=re.search(rf'(?ms)^### MCQ {n}\. .*?(?=^### MCQ {n+1}\. |\Z)',q)
 assert block is not None,n
 assert all(re.search(rf'(?m)^{a}\. ',block.group()) for a in 'ABCD'),n
m=(src/'mains-model-answers.md').read_text()
answers=re.split(r'(?m)^## Q\d+\..*$',m)[1:]
counts=[len(re.findall(r"\b[\w]+(?:[-'][\w]+)*\b",re.sub(r'\*\*[^*]+\*\*','',x))) for x in answers]
assert len(counts)==6 and min(counts)>=200,counts
pdf=src/'integrated-student-edition-2026-10-27.pdf'
subprocess.run([sys.executable,'scripts/render_topic_4_2_5_integrated.py','--input',str(src/'complete-notes.md'),'--output',str(pdf)],check=True)
doc=fitz.open(pdf)
assert 20<=len(doc)<=65
assert all(len(p.get_text().strip())>60 for p in doc)
assert sum(len(p.get_images()) for p in doc)>=3
assert 'Worked laboratory' in '\n'.join(p.get_text() for p in doc)
viol=[]
for i,p in enumerate(doc):
 for b in p.get_text('dict')['blocks']:
  if b['type']==0:
   x0,y0,x1,y1=b['bbox']
   if x0<8 or y0<0 or x1>p.rect.width-8 or y1>p.rect.height-2:viol.append(i+1)
assert not viol,viol
# Keep student-facing integrated PDF and editable-source links present before hashing HTML.
html_path=root/'index.html'
html_text=html_path.read_text()
if 'id="cycle43-downloads"' not in html_text:
 anchor='<p class="status">Expanded draft — independent academic audit pending. All questions are original practice.</p>'
 links='<p class="small" id="cycle43-downloads"><strong>Cycle43 synchronized edition:</strong> <a href="source/integrated-student-edition-2026-10-27.pdf">Read the integrated PDF (29 pages)</a> · <a href="source/complete-notes.md">Editable Markdown master</a> · <a href="complete-notes.pdf">Preserved original PDF</a>. <em>Academic R1–R8 incomplete; no independent approval.</em></p>'
 assert anchor in html_text
 html_path.write_text(html_text.replace(anchor,anchor+links))
soup=BeautifulSoup((root/'index.html').read_text(),'html.parser')
main=soup.find('main');assert main
aside=soup.find('nav',id='chapter-toc')
if aside is None:
 aside=soup.new_tag('nav',id='chapter-toc');aside['style']='padding:12px 16px;background:#edf5fc;border-radius:8px;margin:18px 0;max-height:260px;overflow:auto'
 main.insert_before(aside)
rendered=BeautifulSoup(mistune.create_markdown(plugins=['table','strikethrough'])(md),'html.parser')
for im in rendered.find_all('img'):
 u=im.get('src','')
 if u.startswith('../visuals/'):im['src']='visuals/'+u.split('/')[-1]
seen={};toc=[]
for h in rendered.find_all(['h1','h2','h3']):
 slug=re.sub('[^a-z0-9]+','-',h.get_text(' ',strip=True).lower()).strip('-') or 'section'
 k=seen.get(slug,0);seen[slug]=k+1
 if k:slug+=f'-{k}'
 h['id']=slug
 if h.name in ('h1','h2'):toc.append((h.name,slug,h.get_text(' ',strip=True)))
main.clear()
for item in list(rendered.contents):main.append(item)
aside.clear();heading=soup.new_tag('h2');heading.string='Chapter contents';aside.append(heading)
for tag,slug,label in toc:
 a=soup.new_tag('a',href='#'+slug);a['class']='toc1' if tag=='h1' else 'toc2';a.string=label;aside.append(a)
(root/'index.html').write_text(str(soup))
ids={x.get('id') for x in soup.find_all(id=True)}
broken_files=[];broken_fragments=[];links=0;spa=0
for tag in soup.find_all(['a','img','script','link']):
 u=tag.get('href') or tag.get('src')
 if not u:continue
 if '#/paper/' in u:spa+=1;continue
 p=urlsplit(u)
 if p.scheme or u.startswith('//'):continue
 if p.path:
  links+=1
  if not (root/unquote(p.path)).resolve().exists():broken_files.append(u)
 if p.fragment and unquote(p.fragment) not in ids:broken_fragments.append(u)
assert not broken_files and not broken_fragments,(broken_files[:5],broken_fragments[:5])
manifest=json.loads((root/'manifest.json').read_text())
manifest['production_status']='cycle131_integrated_ci_pdf_partial_mcq_audit_pending'
manifest['academic_approved']=False
manifest['detailed_sections']=17
manifest['mcqs_original']=30
manifest['mains_original']=6
manifest['pdf_pages']=25
manifest['integrated_pdf_pages']=len(doc)
manifest['integrated_pdf_sha256']=hashlib.sha256(pdf.read_bytes()).hexdigest()
manifest['mains_answer_word_counts']=counts
for p in [root/'index.html',pdf,*[src/n for n in parts],src/'complete-notes.md']:
 key=str(p.relative_to(root));manifest['files'][key]={'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size}
(root/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
qa={'cycle':131,'topic':'4-2-5','date':'2026-10-31','original_pdf_sha256':orig,'original_pdf_preserved':True,'integrated_pdf_pages':len(doc),'integrated_pdf_sha256':manifest['integrated_pdf_sha256'],'integrated_pdf_images':sum(len(p.get_images()) for p in doc),'blank_pages':0,'text_boundary_violations':viol,'concepts':17,'min_concept_words':min(word_counts),'original_practice_mcqs':30,'mcq_distribution':{a:keys.count(a) for a in 'ABCD'},'mains_body_counts':counts,'local_file_links_checked':links,'broken_file_links':broken_files,'broken_fragments':broken_fragments,'spa_routes_excluded':spa,'R8':'IN_PROGRESS_NOT_PASS','independent_academic_approvals':0,'browser_accessibility_certified':False,'actual_post_edit_packaging_artifact_verified':False}
(root/'QA-REPORT.md').write_text('# Cycle131 GitHub CI render QA\n\n'+json.dumps(qa,indent=2)+'\n')
(root/'README.md').write_text(f'# Topic 4-2-5 — Industry and Service Sectors (Cycle43)\n\nOriginal 25-page complete-notes.pdf preserved SHA256 {orig}. One synchronized source/complete-notes.md, offline index.html and {len(doc)}-page source/integrated-student-edition-2026-10-27.pdf produced by guarded CI. 17 concepts, 30 original practice MCQs (5 revised), six 200+ body-word mains, three inherited diagrams. No verified official PYQs. R1–R8 incomplete, independent approvals ZERO.\n')
print(json.dumps(qa,indent=2))
