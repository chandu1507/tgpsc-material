"""Cycle133 deterministic Topic 4-3-2 source -> integrated PDF/HTML publisher.
Preserves original complete-notes.pdf; never marks academic approval.
"""
from pathlib import Path
import re,json,hashlib,collections,subprocess,sys
from bs4 import BeautifulSoup
from urllib.parse import urlsplit,unquote
import mistune,fitz

root=Path('.')
topic=root/'Paper 4/Unit 3 - Development and Environmental Problems/Topic 2'
src=topic/'source'
cp=json.loads((root/'project-control/PRODUCTION-CHECKPOINT.json').read_text())
ix=json.loads((root/'project-control/ACADEMIC_READINESS_75_TOPIC_STATUS_INDEX.json').read_text())
assert cp['total_topics']==ix['total_topics']==len(cp['topics'])==75
assert len({t['id'] for t in cp['topics']})==75
assert len(ix['paths'])==len(set(ix['paths']))==75
assert len(list((root/'project-control/academic-readiness').glob('[2-6]-[1-3]-[1-5].json')))==75
assert cp['academically_approved']==ix['independently_academically_approved_count']==0
counts=dict(collections.Counter(t['readiness_status'] for t in cp['topics']))
assert counts=={'IN_PROGRESS':len(ix['pilot_in_progress']),'ASSESSED_REBUILD_REQUIRED':len(ix['assessed_rebuild_required'])}
for t in cp['topics']:
    assert (root/t['path']/'complete-notes.pdf').is_file(),t['id']
    assert (root/f'project-control/academic-readiness/{t["id"]}.json').is_file(),t['id']
original=hashlib.sha256((topic/'complete-notes.pdf').read_bytes()).hexdigest()
assert original=='14f637399f9d006c22218213e3672f20f491f1a06936c6eeb64b363290d800cd',original
master=(src/'complete-notes.md').read_text()
for part in ['core.md','original-mcqs.md','sources-and-audit.md']:
    assert (src/part).read_text().strip() in master, f'Unsynchronized master: {part}'
core=(src/'core.md').read_text()
sections=list(re.finditer(r'(?m)^## (\d+)\. ',core))
assert len(sections)==16
words={int(m.group(1)):len(core[m.end():sections[i+1].start() if i+1<len(sections) else len(core)].split()) for i,m in enumerate(sections)}
assert min(words.values())>=300,words
mcq=(src/'original-mcqs.md').read_text()
questions=re.findall(r'(?ms)^### MCQ (\d+)\. (.*?)(?=^### MCQ |\Z)',mcq)
assert len(questions)==30 and [int(n) for n,_ in questions]==list(range(1,31))
for n,block in questions:
    assert all(re.search(rf'(?m)^{a}\. ',block) for a in 'ABCD'),n
    assert re.search(r'\*\*Answer: [ABCD]\.\*\*',block),n
for n in [4,9,16,26]:
    assert 'Cycle133 option review' in questions[n-1][1],n
pdf=src/'integrated-student-edition-cycle133.pdf'
subprocess.run([sys.executable,'scripts/render_topic_4_3_2_integrated.py','--input',str(src/'complete-notes.md'),'--output',str(pdf)],check=True)
doc=fitz.open(pdf)
assert 20<=len(doc)<=60,len(doc)
blank=[];out=[]
for i,page in enumerate(doc):
    if len(page.get_text().strip())<40:blank.append(i+1)
    for b in page.get_text('dict')['blocks']:
        if b['type']==0:
            x0,y0,x1,y1=b['bbox']
            if x0<3 or y0<0 or x1>page.rect.width-3 or y1>page.rect.height-1:out.append(i+1)
assert not blank and not out,(blank,out)
assert 'Natural Resources • Topic 2' in doc[0].get_text()

soup=BeautifulSoup((topic/'index.html').read_text(),'html.parser')
nav=soup.body.find('div',class_='nav')
alert=soup.body.find('div',class_='alert')
assert nav is not None and alert is not None
for t in list(soup.body.contents):
    if t is not nav and t is not alert:t.extract()
nav.clear()
for label,u in [('← Study portal','../../../index.html'),('Integrated Cycle133 PDF','source/integrated-student-edition-cycle133.pdf'),('Preserved original PDF','complete-notes.pdf'),('Editable Markdown','source/complete-notes.md')]:
    a=soup.new_tag('a',href=u);a.string=label;nav.append(a);nav.append(' · ')
rendered=BeautifulSoup(mistune.create_markdown(plugins=['table','strikethrough'])(master),'html.parser')
for im in rendered.find_all('img'):
    u=im.get('src','')
    if u.startswith('../visuals/'):im['src']='visuals/'+u.split('/')[-1]
seen={}
for h in rendered.find_all(['h1','h2','h3']):
    slug=re.sub('[^a-z0-9]+','-',h.get_text(' ',strip=True).lower()).strip('-') or 'section'
    k=seen.get(slug,0);seen[slug]=k+1
    if k:slug+=f'-{k}'
    h['id']=slug
for t in list(rendered.contents):soup.body.append(t)
(topic/'index.html').write_text(str(soup),encoding='utf-8')
ids={x['id'] for x in soup.find_all(id=True)}
files=frags=spa=0;bad=[];bad_frag=[]
for t in soup.find_all(['a','img','script','link']):
    u=t.get('href') or t.get('src')
    if not u:continue
    if '#/paper/' in u:spa+=1;continue
    x=urlsplit(u)
    if x.scheme or u.startswith('//'):continue
    if x.path:
        files+=1
        if not (topic/unquote(x.path)).resolve().is_file():bad.append(u)
    if x.fragment:
        frags+=1
        if unquote(x.fragment) not in ids:bad_frag.append(u)
assert not bad and not bad_frag,(bad,bad_frag)
manifest=json.loads((topic/'manifest.json').read_text())
manifest.update({'status':'cycle133_author_side_depth_and_option_review_not_approved','integrated_pdf_pages':len(doc),'integrated_pdf_sha256':hashlib.sha256(pdf.read_bytes()).hexdigest(),'academic_approval':'not_approved','cycle133_source_checked_option_reviews':4,'cycle133_core_concepts_above_300_whitespace_words':16})
manifest['files']={}
for p in sorted(topic.rglob('*')):
    if p.is_file() and p.name not in ('manifest.json','QA-REPORT-CYCLE133.md'):
        manifest['files'][str(p.relative_to(topic))]={'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size}
(topic/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
qa=json.loads((root/'project-control/academic-readiness/4-3-2-cycle133-concept-depth-and-four-option-audit-2026-10-31.json').read_text())
qa.update({'pdf_render_pending':False,'pdf_render':'GitHub_Actions_reportlab_deterministic','pdf_pages':len(doc),'pdf_sha256':manifest['integrated_pdf_sha256'],'pdf_blank_pages':blank,'pdf_text_boundary_violations':out,'html_file_links_checked':files,'html_broken_file_links':bad,'html_fragment_links_checked':frags,'html_broken_fragments':bad_frag,'html_spa_routes_excluded':spa,'manifest_hashes_checked':len(manifest['files']),'post_edit_actions_artifact_downloaded':False,'browser_accessibility_certified':False})
(topic/'QA-REPORT-CYCLE133.md').write_text('# Topic 4-3-2 Cycle133 deterministic CI render QA\n\n'+json.dumps(qa,indent=2)+'\n')
print(json.dumps({'pages':len(doc),'pdf_sha256':manifest['integrated_pdf_sha256'],'concepts':len(sections),'min_words':min(words.values()),'original_mcqs':len(questions),'original_pdf_sha256':original,'broken_links':bad,'broken_fragments':bad_frag},indent=2))
