from pathlib import Path
import argparse
import re, html, json, hashlib
from markdown_it import MarkdownIt
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether, PageBreak, Flowable
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from svglib.svglib import svg2rlg

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
 'p':ParagraphStyle('p',fontName='Noto',fontSize=8.6,leading=13.7,spaceAfter=5.5,allowWidows=0,allowOrphans=0),
 'li':ParagraphStyle('li',fontName='Noto',fontSize=8.5,leading=13.5,leftIndent=14,firstLineIndent=-8,spaceAfter=3),
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
        elif t.type=='link_open':
            u=t.attrGet('href') or ''
            if u.startswith('http'):parts.append('<link href="'+html.escape(u,quote=True)+'" color="#176AA3">')
            else:parts.append('')
        elif t.type=='link_close':parts.append('</link>')
        elif t.type in ('softbreak','hardbreak'):parts.append('<br/>')
        elif t.type=='html_inline':parts.append(html.escape(t.content))
        elif t.type=='image':parts.append(html.escape(t.content))
    return ''.join(parts)

story=[]
rendered_diagrams=[]
tokens=MarkdownIt('commonmark').enable('table').parse(src.read_text())
i=0; current_table=None; row=None; cell=None; list_depth=0
while i<len(tokens):
 t=tokens[i]
 if t.type=='heading_open':
    tag=t.tag; inl=tokens[i+1]; val=inline_html(inl)
    key={'h1':'title','h2':'h2','h3':'h3'}.get(tag,'h3')
    if tag=='h2' and 'Part C —' in inl.content:story.append(PageBreak())
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
      table=Table(current_table,colWidths=widths,repeatRows=1,hAlign='LEFT')
      table.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),navy),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#F3F7FA')]),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),('LINEBELOW',(0,0),(-1,-1),.25,colors.HexColor('#CCD9E3'))]))
      story.append(table);story.append(Spacer(1,8))
    current_table=None;i+=1;continue
 if t.type in ('bullet_list_open','ordered_list_open'):list_depth+=1;i+=1;continue
 if t.type in ('bullet_list_close','ordered_list_close'):list_depth=max(0,list_depth-1);i+=1;continue
 if t.type in ('list_item_open','list_item_close'):i+=1;continue
 if t.type=='paragraph_open':
    inl=tokens[i+1]; val=inline_html(inl)
    story.append(Paragraph(('•  '+val) if list_depth else val,styles['li' if list_depth else 'p']))
    match=re.search(r'diagrams/([0-9]{2}_[a-z_]+\\.svg)',inl.content)
    if match:
        diagram_path=src.parent/'diagrams'/match.group(1)
        if not diagram_path.exists():raise FileNotFoundError(diagram_path)
        illustration=svg2rlg(str(diagram_path))
        if illustration is None:raise RuntimeError('SVG conversion failed: '+str(diagram_path))
        scale=min(1,(A4[0]-84)/illustration.width)
        illustration.scale(scale,scale)
        illustration.width*=scale;illustration.height*=scale
        story.extend([Spacer(1,4),illustration,Spacer(1,9)])
        rendered_diagrams.append(match.group(1))
    i+=3;continue
 if t.type=='fence':story.append(Paragraph(html.escape(t.content).replace('\n','<br/>'),styles['note']));i+=1;continue
 i+=1

def footer(canvas,doc):
    canvas.saveState();w,h=A4
    canvas.setStrokeColor(colors.HexColor('#C7D5DF'));canvas.line(42,38,w-42,38)
    canvas.setFont('Noto',7.1);canvas.setFillColor(navy)
    canvas.drawString(42,26,'TGPSC Group I • Paper III • Indian Society • Topic 5 | NOT APPROVED')
    canvas.drawRightString(w-42,26,f'Page {doc.page}')
    canvas.restoreState()

assert rendered_diagrams==['01_entitlement_chain.svg','02_policy_matrix.svg','03_district_convergence.svg'],rendered_diagrams
doc=SimpleDocTemplate(str(out),pagesize=A4,rightMargin=42,leftMargin=42,topMargin=45,bottomMargin=52,invariant=1,title="TGPSC Paper III Unit I Topic 5 - Social Policies Integrated Edition",author="TGPSC Academic Readiness Production")
doc.build(story,onFirstPage=footer,onLaterPages=footer)
import fitz
pdf=fitz.open(str(out))
qa={'file':str(out),'pages':len(pdf),'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'pdf_text_words':sum(len(p.get_text().split()) for p in pdf),'page_text_lengths':[len(p.get_text()) for p in pdf], 'embedded_vector_diagrams':rendered_diagrams, 'total_pdf_vector_drawing_paths':sum(len(p.get_drawings()) for p in pdf), 'pages_with_no_text':[i+1 for i,p in enumerate(pdf) if len(p.get_text().strip())<60]}
if args.qa:
    args.qa.parent.mkdir(parents=True,exist_ok=True)
    args.qa.write_text(json.dumps(qa,indent=2))
print(json.dumps({k:v for k,v in qa.items() if k!='page_text_lengths'},indent=2))