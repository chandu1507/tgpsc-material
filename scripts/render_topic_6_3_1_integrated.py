from pathlib import Path
import argparse
import re, html, json, hashlib
from markdown_it import MarkdownIt
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether, PageBreak, Flowable, Image
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.graphics.shapes import Drawing, Rect, String, Line
from PIL import Image as PILImage

parser=argparse.ArgumentParser(description='Render a full integrated student edition from Markdown')
parser.add_argument('--input',required=True,type=Path)
parser.add_argument('--output',required=True,type=Path)
parser.add_argument('--qa',type=Path,default=None)
args=parser.parse_args()
src=args.input
out=args.output
out.parent.mkdir(parents=True,exist_ok=True)
font='/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf'; bold='/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf'; italic='/usr/share/fonts/truetype/noto/NotoSans-Italic.ttf'
if not Path(font).exists():
    font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'; bold='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'; italic='/usr/share/fonts/truetype/dejavu/DejaVuSans-Oblique.ttf' 
for n,p in [('Noto',font),('NotoBold',bold),('NotoItalic',italic)]:pdfmetrics.registerFont(TTFont(n,p))
pdfmetrics.registerFontFamily('Noto',normal='Noto',bold='NotoBold',italic='NotoItalic',boldItalic='NotoBold')
navy=colors.HexColor('#132A44'); accent=colors.HexColor('#176AA3'); pale=colors.HexColor('#EAF2F7')
styles={
 'title':ParagraphStyle('title',fontName='NotoBold',fontSize=17,leading=23,textColor=navy,spaceAfter=16),
 'h2':ParagraphStyle('h2',fontName='NotoBold',fontSize=12,leading=17,textColor=navy,spaceBefore=15,spaceAfter=8,keepWithNext=True),
 'h3':ParagraphStyle('h3',fontName='NotoBold',fontSize=10.2,leading=15,textColor=accent,spaceBefore=11,spaceAfter=6,keepWithNext=True),
 'p':ParagraphStyle('p',fontName='Noto',fontSize=8.75,leading=14.5,spaceAfter=7,allowWidows=0,allowOrphans=0),
 'li':ParagraphStyle('li',fontName='Noto',fontSize=8.6,leading=14,leftIndent=14,firstLineIndent=-8,spaceAfter=4),
 'cell':ParagraphStyle('cell',fontName='Noto',fontSize=7.2,leading=10.5),
 'cellhead':ParagraphStyle('cellhead',fontName='NotoBold',fontSize=7.2,leading=10.5,textColor=colors.white),
 'note':ParagraphStyle('note',fontName='Noto',fontSize=7.3,leading=10.5,textColor=colors.HexColor('#43546C')),
}
def inline_html(tok):
    parts=[]
    for t in tok.children or []:
        if t.type=='text':parts.append(html.escape(t.content))
        elif t.type=='code_inline':parts.append('<font name="NotoBold">'+html.escape(t.content)+'</font>')
        elif t.type=='strong_open':parts.append('<b>')
        elif t.type=='strong_close':parts.append('</b>')
        elif t.type=='em_open':parts.append('<i>')
        elif t.type=='em_close':parts.append('</i>')
        elif t.type=='link_open':parts.append('')
        elif t.type=='link_close':parts.append('')
        elif t.type in ('softbreak','hardbreak'):parts.append('<br/>')
        elif t.type=='html_inline':parts.append(html.escape(t.content))
        elif t.type=='image':parts.append(html.escape(t.content))
    return ''.join(parts)


story=[]
tokens=MarkdownIt('commonmark').enable('table').parse(src.read_text())
i=0; current_table=None; row=None; cell=None; list_depth=0
while i<len(tokens):
 t=tokens[i]
 if t.type=='heading_open':
    tag=t.tag; inl=tokens[i+1]; val=inline_html(inl)
    key={'h1':'title','h2':'h2','h3':'h3'}.get(tag,'h3')
    if tag=='h1' and ('Original practice MCQs' in inl.content or 'Original mains practice' in inl.content):story.append(PageBreak())
    story.append(Paragraph(val,styles[key]));i+=3;continue
 if t.type=='table_open':current_table=[];i+=1;continue
 if t.type=='tr_open':row=[];i+=1;continue
 if t.type in ('th_open','td_open'):
    inl=tokens[i+1]; val=inline_html(inl);row.append(Paragraph(val,styles['cellhead'] if t.type=='th_open' else styles['cell']));i+=3;continue
 if t.type=='tr_close':current_table.append(row);i+=1;continue
 if t.type=='table_close':
    if current_table:
      widths=None
      n=len(current_table[0]); avail=A4[0]-84
      if n==2:widths=[avail*.56,avail*.44]
      elif n==3:widths=[avail*.32,avail*.33,avail*.35]
      elif n==4:widths=[avail*.25]*4
      elif n>4:widths=[avail/n]*n
      table=Table(current_table,colWidths=widths,repeatRows=1,hAlign='LEFT')
      table.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),navy),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#F3F7FA')]),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),('LINEBELOW',(0,0),(-1,-1),.25,colors.HexColor('#CCD9E3'))]))
      story.append(table);story.append(Spacer(1,8))
    current_table=None;i+=1;continue
 if t.type in ('bullet_list_open','ordered_list_open'):list_depth+=1;i+=1;continue
 if t.type in ('bullet_list_close','ordered_list_close'):list_depth=max(0,list_depth-1);i+=1;continue
 if t.type in ('list_item_open','list_item_close'):i+=1;continue
 if t.type=='paragraph_open':
    inl=tokens[i+1]; val=inline_html(inl)
    imgs=[c for c in (inl.children or []) if c.type=='image']
    if imgs:
      for tok in imgs:
        u=tok.attrGet('src') or ''
        f=(src.parent/u).resolve()
        if not f.is_file(): f=(src.parent.parent/u).resolve()
        if not f.is_file(): raise FileNotFoundError(f)
        w,h=PILImage.open(f).size; scale=min(470/w,220/h)
        story.append(Image(str(f),width=w*scale,height=h*scale));story.append(Spacer(1,7))
      i+=3;continue
    story.append(Paragraph(('•  '+val) if list_depth else val,styles['li' if list_depth else 'p']))
    i+=3;continue
 if t.type=='fence':story.append(Paragraph(html.escape(t.content).replace('\n','<br/>'),styles['note']));i+=1;continue
 i+=1

def footer(canvas,doc):
    canvas.saveState();w,h=A4
    canvas.setStrokeColor(colors.HexColor('#C7D5DF'));canvas.line(42,38,w-42,38)
    canvas.setFont('Noto',7.1);canvas.setFillColor(navy)
    canvas.drawString(42,26,'TGPSC Group I | Paper VI | Public awakening | Topic 6-3-1 | NOT approved')
    canvas.drawRightString(w-42,26,f'Page {doc.page}')
    canvas.restoreState()

doc=SimpleDocTemplate(str(out),pagesize=A4,rightMargin=42,leftMargin=42,topMargin=45,bottomMargin=52,invariant=1,title="TGPSC Paper VI Unit III Topic 1 - Integrated Student Edition",author="TGPSC Academic Readiness Production")
doc.build(story,onFirstPage=footer,onLaterPages=footer)
import fitz
pdf=fitz.open(str(out))
qa={'file':str(out),'pages':len(pdf),'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'pdf_text_words':sum(len(p.get_text().split()) for p in pdf),'page_text_lengths':[len(p.get_text()) for p in pdf], 'pages_with_no_text':[i+1 for i,p in enumerate(pdf) if len(p.get_text().strip())<60]}
if args.qa:
    args.qa.parent.mkdir(parents=True,exist_ok=True)
    args.qa.write_text(json.dumps(qa,indent=2))
print(json.dumps({k:v for k,v in qa.items() if k!='page_text_lengths'},indent=2))