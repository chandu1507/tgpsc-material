from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent/'visuals';ROOT.mkdir(exist_ok=True)
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
BOLD='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
def ft(sz,b=False):return ImageFont.truetype(BOLD if b else FONT,sz)
NAVY='#173954'; BLUE='#eaf3f7'; ORANGE='#bd6424'; DARK='#21374b'; GREEN='#2d796a'
def rounded(d,xy,fill,outline=None,r=20):d.rounded_rectangle(xy,radius=r,fill=fill,outline=outline,width=3)
def center(d,box,lines,color=DARK,sz=22):
 x0,y0,x1,y1=box;txt=lines.split('\n');h=len(txt)*sz*1.35; yy=(y0+y1-h)/2
 for line in txt:
  bb=d.textbbox((0,0),line,font=ft(sz,True));d.text(((x0+x1-(bb[2]-bb[0]))/2,yy),line,font=ft(sz,True),fill=color);yy+=sz*1.35
def arrow(d,xy1,xy2,color=ORANGE,width=5):
 import math
 d.line([xy1,xy2],fill=color,width=width)
 a=math.atan2(xy2[1]-xy1[1],xy2[0]-xy1[0]);L=15
 for s in [-1,1]:
  q=(xy2[0]-L*math.cos(a+s*0.6),xy2[1]-L*math.sin(a+s*0.6));d.line([xy2,q],fill=color,width=width)
# 1
im=Image.new('RGB',(1350,650),'white');d=ImageDraw.Draw(im)
d.text((45,20),'Development delivery: separate five accountabilities',font=ft(32,True),fill=NAVY)
boxes=[(35,110,250,250),(305,110,520,250),(575,110,790,250),(845,110,1060,250),(1115,110,1325,250)]
labels=['PUBLIC MANDATE\nRights and goals','FINANCE\nTax / grants','DELIVERY\nState / firm / NGO','VERIFICATION\nAudit / users','REMEDY\nAppeal / correction']
for i,(b,l) in enumerate(zip(boxes,labels)):
 rounded(d,b,BLUE if i%2==0 else '#f9eee5',NAVY);center(d,b,l,sz=18)
 if i<4:arrow(d,(b[2]+5,180),(boxes[i+1][0]-6,180))
rounded(d,(260,380,1090,540),'#e5f4ed',GREEN);center(d,(260,380,1090,540),'CITIZENS: access, feedback, RTI, inclusion and grievances',sz=23)
arrow(d,(675,375),(675,260),GREEN);d.text((320,565),'Contracting a service never contracts away public accountability.',font=ft(21),fill=DARK)
im.save(ROOT/'development-governance.png',optimize=True)
# 2
im=Image.new('RGB',(1400,710),'white');d=ImageDraw.Draw(im)
d.text((40,20),'PPP: a lifecycle with checkpoints, not free financing',font=ft(32,True),fill=NAVY)
labels=['PUBLIC NEED\n& alternatives','FEASIBILITY\n& social risk','OPEN BIDDING\n& concession','BUILD / OPERATE\n& independent test','HAND BACK\n& fiscal closure']
boxes=[(35+i*280,120,260+i*280,280) for i in range(5)]
for i,(b,l) in enumerate(zip(boxes,labels)):
 rounded(d,b,'#eaf3f7' if i%2==0 else '#fff1e5',NAVY);center(d,b,l,sz=18)
 if i<4:arrow(d,(b[2]+8,200),(boxes[i+1][0]-8,200))
risks=['Demand / affordability','Land / environment','Construction / delays','Quality / tariff / debt','Termination / asset condition']
for i,(b,t) in enumerate(zip(boxes,risks)):
 rounded(d,(b[0],355,b[2],435),'#e8f5ec',GREEN);center(d,(b[0],355,b[2],435),t,sz=15)
 d.line((b[0]+112,280,b[0]+112,355),fill=GREEN,width=3)
rounded(d,(165,520,1235,630),'#fff2e8',ORANGE);center(d,(165,520,1235,630),'Public test: lifecycle value + equitable access + enforceable remedies',sz=24)
im.save(ROOT/'ppp-lifecycle.png',optimize=True)
# 3
im=Image.new('RGB',(1400,620),'white');d=ImageDraw.Draw(im)
d.text((40,20),'SHG pathway: credit is an instrument, empowerment is an outcome',font=ft(30,True),fill=NAVY)
labels=['SAVINGS\n& trust','BANK LINKAGE\n& records','SKILLS\n& market access','NET EARNINGS\n& resilience','AUTONOMY\n& public voice']
boxes=[(40+i*275,130,245+i*275,290) for i in range(5)]
for i,(b,l) in enumerate(zip(boxes,labels)):
 rounded(d,b,'#e8f2f6' if i<3 else '#e4f4e8',NAVY if i<3 else GREEN);center(d,b,l,sz=18)
 if i<4:arrow(d,(b[2]+7,210),(boxes[i+1][0]-7,210))
rounded(d,(140,390,1260,520),'#fff0e5',ORANGE);center(d,(140,390,1260,520),'Check exclusion, debt stress, unpaid work, leadership and control of income',sz=22)
im.save(ROOT/'shg-pathway.png',optimize=True)
print('diagrams',[(p.name,p.stat().st_size) for p in ROOT.iterdir()])
