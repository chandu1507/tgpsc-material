from pathlib import Path
import re,html,json,hashlib,zipfile,os,shutil,datetime
import mistune
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,Image,KeepTogether,PageBreak
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT,TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PIL import Image as PILImage
ROOT=Path('/mnt/data/TGPSC_P3_U3_T3');SRC=ROOT/'source'
TITLE='Programmes, Agencies and Institutions for Urban and Rural Development; Participatory Development; Poverty Alleviation; Women Empowerment; Rights to Health, Food Security and Education'
parts=['syllabus-and-summary.md','detailed-notes.md','visual-learning.md','quick-revision.md','original-mcqs.md','mains-model-answers.md','sources-and-audit.md']
header=f'''# {TITLE}\n\n**TGPSC Group I | Paper III | Unit III | Topic 3 | Expanded draft | 23 October 2026**\n\n**ACADEMIC STATUS: NOT APPROVED.** All 25 MCQs and six mains questions are original practice material. No verified official PYQ is claimed. This manuscript has undergone structural and internal source checks, not a full subject-expert audit.\n\n**Study route:** syllabus map → detailed concept chapters → diagrams and tables → standalone quick revision → explained MCQs → structured mains practice → evidence register.\n\n'''
md=header+'\n\n'.join((SRC/p).read_text(encoding='utf-8') for p in parts)
(SRC/'complete-notes.md').write_text(md,encoding='utf-8')
# offline HTML
htmlbody=mistune.create_markdown(plugins=['table','strikethrough'])(md)
# image URLs are relative to topic root in html
css='''body{margin:0;background:#edf3f8;color:#1c3146;font:16px/1.7 system-ui,-apple-system,sans-serif}header{background:#16334e;color:white;padding:25px max(5vw,18px)}header h1{font-size:27px;line-height:1.3;max-width:1000px}header p{max-width:900px}main{max-width:1000px;margin:20px auto;background:white;padding:32px 44px;border-radius:14px;box-shadow:0 3px 20px #d9e3eb}h1,h2,h3{color:#16334e;line-height:1.35}h1{border-bottom:3px solid #dc8840;padding-bottom:12px;margin-top:35px}h2{margin-top:32px;border-left:5px solid #d9792b;padding-left:13px}h3{margin-top:22px}p{margin:12px 0}blockquote{background:#edf4f8;padding:10px 18px;border-left:5px solid #468779;margin:16px 0}table{border-collapse:collapse;width:100%;font-size:14px;margin:18px 0}td,th{border:1px solid #cbd9e3;padding:8px 10px;text-align:left;vertical-align:top}th{background:#e8f1f7}tr:nth-child(even){background:#f7fafc}img{max-width:100%;height:auto;display:block;margin:20px auto}a{color:#a44f12;overflow-wrap:anywhere}.toc{columns:2;max-height:330px;overflow:auto;font-size:14px}.toc a{display:block;margin:4px 0;text-decoration:none}.badge{background:#ffebdc;color:#7c3c14;padding:5px 9px;border-radius:7px;font-weight:bold}nav{background:#f0f5f8;padding:15px;border-radius:8px}footer{text-align:center;color:#567;padding:20px}@media(max-width:700px){main{padding:20px 17px}.toc{columns:1}table{font-size:12px}}@media print{body{background:white}header{color:black;background:white}main{box-shadow:none;margin:0;padding:0}h2,h3{break-after:avoid}table{break-inside:auto}}'''
heads=re.findall(r'^## (.+)$',md,flags=re.M)
# insert heading ids in html, link TOC
from bs4 import BeautifulSoup
soup=BeautifulSoup(htmlbody,'html.parser');toc=[]
for i,h in enumerate(soup.find_all('h2')):
 id=f'section-{i+1}';h['id']=id;toc.append(f'<a href="#{id}">{html.escape(h.get_text())}</a>')
page=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(TITLE)} — TGPSC</title><style>{css}</style></head><body><header><h1>TGPSC Group I · Paper III · Unit III · Topic 3</h1><p>Urban and rural development · Participatory development · Poverty alleviation · Women empowerment · Health, food and education rights</p><p><span class="badge">Expanded draft — academically unapproved</span> &nbsp; 25 original MCQs · 6 mains models</p><p><a style="color:#ffd4aa" href="../../../index.html">← 75-topic offline study portal</a> &nbsp; <a style="color:#ffd4aa" href="complete-notes.pdf">Read PDF</a> &nbsp; <a style="color:#ffd4aa" href="source/complete-notes.md">Editable Markdown</a></p></header><main><nav><b>Chapter contents</b><div class="toc">{''.join(toc)}</div></nav>{str(soup)}</main><footer>Original study draft; no official PYQs claimed. Research cutoff: 23 October 2026.</footer></body></html>'''
(ROOT/'index.html').write_text(page,encoding='utf-8')
# reportlab PDF
pdfmetrics.registerFont(TTFont('DV','/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('DVB','/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'))
pdfmetrics.registerFontFamily('DV',normal='DV',bold='DVB',italic='DV',boldItalic='DVB')
ss=getSampleStyleSheet()
styles={
 'body':ParagraphStyle('body',fontName='DV',fontSize=9.4,leading=15.2,spaceAfter=9,textColor=colors.HexColor('#21374b')),
 'h1':ParagraphStyle('h1x',fontName='DVB',fontSize=17,leading=23,spaceBefore=21,spaceAfter=13,textColor=colors.HexColor('#173954'),keepWithNext=True),
 'h2':ParagraphStyle('h2x',fontName='DVB',fontSize=12.8,leading=19,spaceBefore=16,spaceAfter=9,textColor=colors.HexColor('#a45a20'),keepWithNext=True),
 'h3':ParagraphStyle('h3x',fontName='DVB',fontSize=10.3,leading=16,spaceBefore=12,spaceAfter=7,textColor=colors.HexColor('#255974'),keepWithNext=True),
 'small':ParagraphStyle('smallx',fontName='DV',fontSize=7.3,leading=11.5,spaceAfter=5,textColor=colors.HexColor('#21374b')),
 'caption':ParagraphStyle('captionx',fontName='DV',fontSize=8,leading=12,spaceAfter=11,textColor=colors.HexColor('#426073')),
 'bullet':ParagraphStyle('bulletx',fontName='DV',fontSize=9.1,leading=14,spaceAfter=5,leftIndent=17,firstLineIndent=-11,textColor=colors.HexColor('#21374b')),
}
def inline(nodes):
 out=[]
 for n in nodes:
  t=n.get('type');ch=n.get('children',[])
  if t=='text':out.append(html.escape(n.get('raw','')))
  elif t=='strong':out.append('<b>'+inline(ch)+'</b>')
  elif t=='emphasis':out.append('<i>'+inline(ch)+'</i>')
  elif t=='link':out.append('<link href="'+html.escape(n.get('attrs',{}).get('url',''),quote=True)+'" color="#1d6a8a">'+inline(ch)+'</link>')
  elif t=='codespan':out.append('<font color="#a45a20">'+html.escape(n.get('raw',''))+'</font>')
  elif t in ('softbreak','linebreak'):out.append('<br/>')
  elif t=='image':out.append(html.escape(n.get('attrs',{}).get('url','')))
  else:out.append(inline(ch) if ch else html.escape(n.get('raw','')))
 return ''.join(out)
parser=mistune.create_markdown(renderer='ast',plugins=['table','strikethrough'])
story=[]
for n in parser(md):
 t=n['type']
 if t in ('blank_line','thematic_break'):continue
 if t=='heading':
  level=n.get('attrs',{}).get('level',2);style=styles['h1'] if level==1 else styles['h2'] if level==2 else styles['h3'];story.append(Paragraph(inline(n.get('children',[])),style))
 elif t=='paragraph':
  ch=n.get('children',[])
  if len(ch)==1 and ch[0]['type']=='image':
   path=ROOT/ch[0].get('attrs',{}).get('url','');
   if path.exists():
    im=PILImage.open(path);w,h=im.size;maxw=500;scale=min(maxw/w,410/h);story.append(Image(str(path),width=w*scale,height=h*scale));story.append(Spacer(1,8))
  else:story.append(Paragraph(inline(ch),styles['body']))
 elif t=='block_quote':
  for q in n.get('children',[]):
   if q.get('type') in ('paragraph','block_text'):story.append(Paragraph(inline(q.get('children',[])),styles['body']))
 elif t=='list':
  for j,li in enumerate(n.get('children',[]),1):
   for sub in li.get('children',[]):
    if sub.get('type') in ('block_text','paragraph'):
     marker=str(j)+'. ' if n.get('attrs',{}).get('ordered') else '• '
     story.append(Paragraph(marker+inline(sub.get('children',[])),styles['bullet']))
 elif t=='table':
  rows=[]
  for block in n.get('children',[]):
   for r in ([block] if block['type']=='table_head' else block.get('children',[])):
    cells=r.get('children',[]);rows.append([inline(c.get('children',[])) for c in cells])
  if not rows:continue
  # source register long URLs: print concise clickable source rows, not unbreakable 100-char URLs
  if len(rows[0])==4 and rows[0][0]=='ID':
   for r in rows[1:]:
    url=r[3];lab=html.escape(r[0]+' — '+re.sub('<[^>]+>','',r[1]))
    content=f'<b>{lab}</b>. '+r[2]+f' <link href="{html.escape(url,quote=True)}" color="#1d6a8a">[official source]</link>'
    story.append(Paragraph(content,styles['small']))
   continue
  nc=len(rows[0]);available=500
  ratios={2:[0.38,0.62],3:[0.25,0.37,0.38],4:[0.20,0.29,0.25,0.26]}.get(nc,[1/nc]*nc)
  data=[[Paragraph(c,styles['small']) for c in row] for row in rows]
  table=Table(data,colWidths=[available*x for x in ratios],repeatRows=1,hAlign='LEFT')
  table.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#e3eef4')),('VALIGN',(0,0),(-1,-1),'TOP'),('GRID',(0,0),(-1,-1),0.4,colors.HexColor('#c3d6df')),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7)]))
  story.append(table);story.append(Spacer(1,10))
# use no page numbers to avoid misleading citations

def on_page(canvas,doc):
 canvas.saveState();canvas.setStrokeColor(colors.HexColor('#d2dfe8'));canvas.line(46,42,A4[0]-46,42)
 canvas.setFont('DV',7);canvas.setFillColor(colors.HexColor('#617588'))
 canvas.drawString(46,29,'TGPSC Group I · Paper III / Unit III / Topic 3 · Expanded draft — not academically approved')
 canvas.restoreState()
doc=SimpleDocTemplate(str(ROOT/'complete-notes.pdf'),pagesize=A4,rightMargin=46,leftMargin=46,topMargin=52,bottomMargin=57,title=TITLE,author='TGPSC Group I Study Library',pageCompression=1)
doc.build(story,onFirstPage=on_page,onLaterPages=on_page)
print('MANUSCRIPT WORDS',len(md.split()),'HTML',len(page),'PDF', (ROOT/'complete-notes.pdf').stat().st_size)
