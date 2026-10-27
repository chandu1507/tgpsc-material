from pathlib import Path
import re, html, json, hashlib, zipfile, os
from datetime import datetime
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import mistune

ROOT=Path(__file__).resolve().parent.parent; SRC=ROOT/'source'
COMPONENTS=[('syllabus-and-summary.md','Syllabus map & summary'),('detailed-notes.md','Detailed textbook notes'),('visual-learning.md','Visuals and tables'),('quick-revision.md','Standalone quick revision'),('original-mcqs.md','25 original MCQs'),('mains-model-answers.md','6 mains model answers'),('sources-and-audit.md','Sources and internal audit')]
TITLE='Governance and Good Governance: E-Governance, Union Institutions, Commissions and Parliamentary Committees'
INTRO=f'''# {TITLE}\n\n**TGPSC Group I | Paper III | Unit III | Topic 1 | Expanded draft | 27 October 2026**\n\n**ACADEMIC STATUS: NOT APPROVED.** Original practice MCQs and mains answers only; no verified official PYQ claim.\n\n**Reader's guide:** Read the syllabus map first, then the 13 detailed chapters. Use the diagrams, revision sheets, 25 explained MCQs and six structured mains answers for consolidation. Official and primary-source links appear in the evidence register.\n'''
full=INTRO+'\n\n'+('\n\n'.join((SRC/f).read_text(encoding='utf-8') for f,_ in COMPONENTS))+'\n'
(SRC/'complete-notes.md').write_text(full,encoding='utf-8')

# ReportLab typography
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'; BOLD='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
pdfmetrics.registerFont(TTFont('DejaVu',FONT));pdfmetrics.registerFont(TTFont('DejaVu-Bold',BOLD));pdfmetrics.registerFontFamily('DejaVu',normal='DejaVu',bold='DejaVu-Bold',italic='DejaVu',boldItalic='DejaVu-Bold')
styles={
 'title':ParagraphStyle('title',fontName='DejaVu-Bold',fontSize=17,leading=24,textColor=colors.HexColor('#133655'),spaceAfter=14),
 'h1':ParagraphStyle('h1',fontName='DejaVu-Bold',fontSize=14.3,leading=20,textColor=colors.HexColor('#174f72'),spaceBefore=16,spaceAfter=9,keepWithNext=True),
 'h2':ParagraphStyle('h2',fontName='DejaVu-Bold',fontSize=11.3,leading=16,textColor=colors.HexColor('#1a536e'),spaceBefore=13,spaceAfter=7,keepWithNext=True),
 'h3':ParagraphStyle('h3',fontName='DejaVu-Bold',fontSize=9.8,leading=14,textColor=colors.HexColor('#3a5669'),spaceBefore=9,spaceAfter=5,keepWithNext=True),
 'p':ParagraphStyle('p',fontName='DejaVu',fontSize=9.2,leading=14.1,textColor=colors.HexColor('#263748'),spaceAfter=8),
 'small':ParagraphStyle('small',fontName='DejaVu',fontSize=8.2,leading=11.6,textColor=colors.HexColor('#263748'),spaceAfter=5),
 'quote':ParagraphStyle('quote',fontName='DejaVu',fontSize=9.1,leading=14,leftIndent=12,textColor=colors.HexColor('#476178'),spaceAfter=9),
 'cell':ParagraphStyle('cell',fontName='DejaVu',fontSize=7.7,leading=11,textColor=colors.HexColor('#243d4c')),
 'cellh':ParagraphStyle('cellh',fontName='DejaVu-Bold',fontSize=7.7,leading=11,textColor=colors.white),
}

def fmt(t):
 t=html.escape(t,quote=False)
 # inline markdown formatting
 t=re.sub(r'\*\*(.+?)\*\*',r'<b>\1</b>',t)
 t=re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)',r'<i>\1</i>',t)
 t=re.sub(r'`([^`]+)`',r'<font color="#154e70">\1</font>',t)
 t=re.sub(r'\[([^\]]+)\]\((https?://[^)]+)\)',r'<link href="\2" color="#155d8d">\1</link>',t)
 return t

def mkpara(t,style='p'):
 return Paragraph(fmt(t),styles[style])

def render_lines(markdown,section_idx=0):
 out=[]; lines=markdown.splitlines(); i=0
 while i<len(lines):
  s=lines[i].strip()
  if not s: i+=1;continue
  if s.startswith('![') and '](' in s:
   m=re.match(r'!\[(.*?)\]\((.*?)\)',s)
   if m:
    image_path=(SRC/m.group(2)).resolve()
    if image_path.exists():
     from PIL import Image as PILImage
     with PILImage.open(image_path) as _im: iw,ih=_im.size
     im=Image(str(image_path),width=498,height=498*ih/iw)
     out.append(Spacer(1,8));out.append(im);out.append(Spacer(1,12))
   i+=1;continue
  if s.startswith('|'):
   tbl=[]
   while i<len(lines) and lines[i].strip().startswith('|'):
    cells=[v.strip() for v in lines[i].strip().strip('|').split('|')]
    if not all(re.fullmatch(r':?-{2,}:?',v) for v in cells):tbl.append(cells)
    i+=1
   if len(tbl)>=2:
    n=max(len(r) for r in tbl); tbl=[r+['']*(n-len(r)) for r in tbl]
    widths={2:[175,320],3:[100,155,240],4:[82,135,136,142],5:[72,103,105,105,110]}.get(n,[495/n]*n)
    data=[]
    for rownum,row in enumerate(tbl):
     data.append([mkpara(v,'cellh' if rownum==0 else 'cell') for v in row])
    table=Table(data,colWidths=widths,repeatRows=1,hAlign='LEFT')
    table.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#28536e')),('VALIGN',(0,0),(-1,-1),'TOP'),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#f0f5f8')]),('LINEBELOW',(0,0),(-1,0),.5,colors.HexColor('#8aa2b2')),('GRID',(0,1),(-1,-1),.22,colors.HexColor('#c9d8e2')),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6)]))
    out.append(Spacer(1,7));out.append(table);out.append(Spacer(1,11))
   continue
  if s.startswith('#'):
   level=len(s)-len(s.lstrip('#')); title=s[level:].strip()
   if level==1: st='h1' if section_idx else 'title'
   elif level==2:st='h2'
   else:st='h3'
   out.append(mkpara(title,st));i+=1;continue
  if s.startswith('> '):
   out.append(mkpara(s[2:],'quote'));i+=1;continue
  # compact source links before generic bullets to avoid long URL overflow
  if s.startswith('- [S') and 'http' in s:
   m=re.match(r'- \[(S\d+)\] (https?://\S+)',s)
   if m:
    out.append(Paragraph(f'<link href="{html.escape(m.group(2),quote=True)}" color="#155d8d">{m.group(1)}: Open primary source</link>',styles['small']))
    i+=1;continue
  if s.startswith('- ') or re.match(r'^\d+\. ',s):
   out.append(mkpara('• '+re.sub(r'^(?:- |\d+\. )','',s),'small'));i+=1;continue
  para=[s];i+=1
  while i<len(lines) and lines[i].strip() and not re.match(r'^(?:#|\||>|- |\d+\. |!\[)',lines[i].strip()):
   para.append(lines[i].strip());i+=1
  out.append(mkpara(' '.join(para)))
 return out

pdf_path=SRC/'integrated-student-edition-2026-10-27.pdf'
doc=SimpleDocTemplate(str(pdf_path),pagesize=A4,leftMargin=49,rightMargin=48,topMargin=52,bottomMargin=51,title=TITLE,author='TGPSC Study Project | Expanded Draft',pageCompression=1)
story=render_lines(INTRO)
for idx,(f,label) in enumerate(COMPONENTS,1):
 story.append(PageBreak());story+=render_lines((SRC/f).read_text(),idx)

def decorate(c,doc):
 c.saveState();w,h=A4
 c.setStrokeColor(colors.HexColor('#d3dfe8'));c.line(49,44,w-48,44)
 c.setFont('DejaVu',7.1);c.setFillColor(colors.HexColor('#637789'))
 c.drawString(49,31,'TGPSC Group I  |  Paper III · Unit III · Topic 1  |  Expanded draft — not approved')
 c.drawRightString(w-48,31,f'{doc.page}')
 c.restoreState()
doc.build(story,onFirstPage=decorate,onLaterPages=decorate)

# Offline HTML chapter: no CDN, no remote scripts.
md=mistune.create_markdown(escape=False,plugins=['table','strikethrough'])
parts={f:md((SRC/f).read_text(encoding='utf-8')).replace('src="../visuals/','src="visuals/') for f,_ in COMPONENTS}
# interactive MCQ questions from Markdown
mcq_src=(SRC/'original-mcqs.md').read_text()
blocks=re.split(r'(?m)^### Q(\d+)\. ',mcq_src)[1:]
quiz=[]
for j in range(0,len(blocks),2):
 n=int(blocks[j]); body=blocks[j+1]
 q=body.split('\n',1)[0].strip()
 opts=re.findall(r'(?m)^([A-D])\. (.+?)  $',body)
 a=re.search(r'\*\*Answer: ([A-D])\.\*\* (.+)',body)
 if len(opts)!=4 or not a:raise ValueError(f'quiz parse {n} {opts} {a}')
 quiz.append({'n':n,'q':q,'options':opts,'correct':a.group(1),'explanation':a.group(2)})
quiz_json=json.dumps(quiz,ensure_ascii=False).replace('</','<\\/')
nav=[('syllabus-and-summary.md','Syllabus'),('detailed-notes.md','Textbook notes'),('visual-learning.md','Diagrams'),('quick-revision.md','Quick revision'),('original-mcqs.md','Practice MCQs'),('mains-model-answers.md','Mains answers'),('sources-and-audit.md','Sources & audit')]
nav_html=''.join(f'<button type="button" data-tab="t{i}" class="tab">{html.escape(label)}</button>' for i,(_,label) in enumerate(nav))
panes=''.join(f'<section id="t{i}" class="pane" role="tabpanel">{parts[f] if f!="original-mcqs.md" else "<h1>25 original practice MCQs</h1><p>Answer each question to reveal an explanation. Questions are not official PYQs.</p><div id=\"quiz\"></div>"}</section>' for i,(f,_) in enumerate(nav))
page=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>TGPSC P3 U3 T1 | Good Governance</title><style>
:root{{--ink:#18344b;--navy:#12334c;--teal:#1a6573;--orange:#de7b32;--bg:#f0f5f8}}*{{box-sizing:border-box}}body{{margin:0;font:15px/1.7 system-ui,-apple-system,Segoe UI,sans-serif;color:var(--ink);background:var(--bg)}}header{{background:linear-gradient(115deg,#102d49,#1b6071);color:white;padding:24px max(20px,5vw)}}header h1{{font-size:clamp(21px,3vw,32px);max-width:1050px;line-height:1.28}}header p{{max-width:980px;margin:6px 0}}header a{{color:#ffe5c8}}.badge{{display:inline-block;border:1px solid #f0caa6;background:#fff3e4;color:#8b4917;border-radius:20px;padding:4px 11px;font-size:12px;font-weight:700}}.layout{{max-width:1340px;margin:auto;display:grid;grid-template-columns:220px minmax(0,1fr);gap:22px;padding:24px}}nav{{position:sticky;top:12px;align-self:start;background:white;border-radius:12px;padding:14px;box-shadow:0 3px 15px #15324c12}}.tab{{display:block;width:100%;text-align:left;border:0;background:transparent;padding:12px 13px;border-radius:7px;color:#24465c;cursor:pointer;font-weight:600}}.tab.active{{background:#e5f2f3;border-left:4px solid var(--teal)}}main{{background:white;padding:26px 36px;border-radius:13px;box-shadow:0 3px 20px #17354e12;min-width:0}}.pane{{display:none}}.pane.active{{display:block}}h1{{line-height:1.3}}main h1{{font-size:25px;color:#163c5b;border-bottom:2px solid #e4edf2;padding-bottom:12px}}main h2{{font-size:21px;color:#205a71;margin-top:34px}}main h3{{font-size:17px;color:#3a5c6d;margin-top:24px}}p{{margin:10px 0 15px}}table{{width:100%;border-collapse:collapse;display:block;overflow-x:auto;margin:16px 0}}td,th{{border:1px solid #d7e3eb;padding:10px;vertical-align:top;min-width:90px}}th{{background:#234e68;color:white}}tr:nth-child(even){{background:#f6f9fb}}img{{max-width:100%;height:auto;border-radius:8px}}blockquote{{margin:15px 0;padding:12px 18px;border-left:4px solid var(--orange);background:#fff6eb}}.quizitem{{border:1px solid #d6e4ec;border-radius:10px;padding:18px;margin:16px 0;background:#fcfefe}}.quizitem label{{display:block;padding:7px 10px;border-radius:6px;cursor:pointer}}.quizitem label:hover{{background:#eff6f8}}.check{{background:#1b6573;color:white;border:0;padding:8px 16px;border-radius:6px;cursor:pointer;margin-top:8px}}.result{{display:none;margin-top:12px;padding:10px;border-radius:7px;background:#e9f4ee}}.result.wrong{{background:#fff0e9}}#search{{width:100%;padding:9px 10px;border:1px solid #b7cad7;border-radius:7px;margin:10px 0}}.tools{{display:flex;flex-wrap:wrap;gap:12px;margin:10px 0}}.tools a{{color:#d8f2ff}}.notice{{border-left:4px solid #dd893e;padding:12px;background:#fff7ee;margin:15px 0}}.jump{{background:#f1f6f8;padding:14px;border-radius:9px;margin:12px 0}}.jump a{{display:inline-block;margin:4px 8px 4px 0;color:#1a6078}}@media(max-width:800px){{.layout{{grid-template-columns:1fr;padding:10px}}nav{{position:static;display:flex;overflow-x:auto;gap:5px}}.tab{{min-width:135px;text-align:center}}main{{padding:18px}}}}@media print{{header,nav,.tools{{display:none}}.layout{{display:block}}main{{box-shadow:none}}.pane{{display:block!important}}}}
</style></head><body><header><div class="badge">EXPANDED DRAFT · NOT ACADEMICALLY APPROVED</div><h1>{html.escape(TITLE)}</h1><p>Paper III → Unit III → Topic 1 · TGPSC Group I · 13 detailed chapters · 25 original MCQs · 6 structured mains answers</p><div class="tools"><a href="source/integrated-student-edition-2026-10-27.pdf">Printable PDF</a><a href="source/complete-notes.md">Editable Markdown</a><a href="../../../index.html">75-topic portal</a></div></header><div class="layout"><nav aria-label="Study sections">{nav_html}</nav><main><label for="search">Search within current section</label><input id="search" type="search" placeholder="Type a term, e.g. Article 280, MeeSeva, PAC"><div id="searchStatus" aria-live="polite"></div><div id="jump" class="jump"></div><div class="notice">All MCQs and mains questions are original practice. The syllabus groups several statutory commissions under 'constitutional bodies'; the notes correct that classification.</div>{panes}</main></div><script>const quizData={quiz_json};const quiz=document.getElementById('quiz');quiz.innerHTML=quizData.map(x=>`<article class="quizitem"><strong>Q${{x.n}}. ${{x.q}}</strong>${{x.options.map(([letter,option])=>`<label><input type="radio" name="q${{x.n}}" value="${{letter}}"> ${{letter}}. ${{option}}</label>`).join('')}}<button class="check" onclick="checkAnswer(${{x.n}})">Check answer</button><div class="result" id="r${{x.n}}"></div></article>`).join('');function checkAnswer(n){{const x=quizData.find(q=>q.n===n),sel=document.querySelector(`input[name=q${{n}}]:checked`),el=document.getElementById(`r${{n}}`);el.style.display='block';el.className='result '+(sel&&sel.value===x.correct?'':'wrong');el.textContent=(sel?(sel.value===x.correct?'Correct. ':'Incorrect. '):'Select an option. ')+`Answer: ${{x.correct}}. ${{x.explanation}}`;}}const tabs=[...document.querySelectorAll('.tab')];function openTab(id){{tabs.forEach(b=>b.classList.toggle('active',b.dataset.tab===id));document.querySelectorAll('.pane').forEach(p=>p.classList.toggle('active',p.id===id));document.getElementById('search').value='';document.getElementById('searchStatus').textContent='';buildJump();window.scrollTo(0,0);}}tabs.forEach(b=>b.addEventListener('click',()=>openTab(b.dataset.tab)));function buildJump(){{const pane=document.querySelector('.pane.active'),heads=[...pane.querySelectorAll('h2')];document.getElementById('jump').innerHTML=heads.length?'<strong>Jump to:</strong> '+heads.map((h,i)=>{{h.id='sec-'+pane.id+'-'+i;return `<a href="#${{h.id}}">${{h.textContent}}</a>`}}).join(''):'';}}document.getElementById('search').addEventListener('input',e=>{{let term=e.target.value.trim().toLowerCase();let pane=document.querySelector('.pane.active');let matches=term?[...pane.querySelectorAll('p,h2,h3,td,li,strong')].filter(el=>el.textContent.toLowerCase().includes(term)).length:0;document.getElementById('searchStatus').textContent=term?`${{matches}} matching text blocks in this section`:' ';}});openTab('t0');</script></body></html>'''
(ROOT/'index.html').write_text(page,encoding='utf-8')

manifest={
 'topic_id':'P3-U3-T1','title':TITLE,'status':'expanded draft, NOT academically approved',
 'syllabus_primary_source':'TGPSC Notification 02/2024, Annexure-II, Paper III, Unit III, item 1',
 'total_planned_topics':75,'existing_topics':75,'remaining_without_first_draft':0,
 'academic_approvals':0,'original_mcqs':len(quiz),'verified_official_pyqs':0,
 'mains_model_answers':len(re.findall(r'(?m)^## M\d+\.',(SRC/'mains-model-answers.md').read_text())),
 'detailed_chapters':len(re.findall(r'(?m)^## \d+\. ',(SRC/'detailed-notes.md').read_text())),
 'manuscript_word_count':len(full.split()),'pdf_bytes':pdf_path.stat().st_size,
 'components':[f for f,_ in COMPONENTS],
 'source_register_count':20,'diagrams':2,
 'files':{},
 'note':'Existing topic 3-3-1 only; preserved legacy complete-notes.pdf unchanged; integrated PDF generated from seven editable components; no independent academic approval.'
}
for p in sorted(ROOT.rglob('*')):
 if p.is_file() and p.name!='manifest.json':
  manifest['files'][str(p.relative_to(ROOT))]={'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
(ROOT/'manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n')
(ROOT/'README.md').write_text(f'''# TGPSC Group I — Paper III / Unit III / Topic 1\n\n{TITLE}\n\nOpen `index.html` for the interactive offline chapter, `source/integrated-student-edition-2026-10-27.pdf` for print, or `source/complete-notes.md` for editing. Component Markdown files, diagrams (SVG and PNG), and source/audit register are included.\n\n**One expanded draft, NOT academically approved.** No official PYQ is claimed. The original 19-topic master is not available for merging.\n''')
print('PDF:',pdf_path, 'bytes',pdf_path.stat().st_size)
print('HTML bytes:',(ROOT/'index.html').stat().st_size)
print('Manuscript words:',len(full.split()),'MCQs:',len(quiz),'mains:',manifest['mains_model_answers'],'chapters:',manifest['detailed_chapters'])
