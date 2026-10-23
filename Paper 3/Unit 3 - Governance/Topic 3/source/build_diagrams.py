from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
out=Path('/mnt/data/TGPSC_P3_U3_T3/visuals');out.mkdir(parents=True,exist_ok=True)
F='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf';B='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
font=lambda n,b=False: ImageFont.truetype(B if b else F,n)
navy='#15324b';orange='#d8792e';pale='#eaf3f7';text='#18334c';green='#3e8278'
img=Image.new('RGB',(1900,760),'white');d=ImageDraw.Draw(img)
d.rounded_rectangle((20,20,1880,740),30,outline='#cddfe8',width=4,fill='#f9fcfe')
d.text((65,65),'Development delivery: from deprivation to verifiable outcome',font=font(42,True),fill=navy)
steps=[('1. Deprivation','Who is excluded?'),('2. Right / scheme','Which legal basis?'),('3. Competent agency','Who may decide?'),('4. Fund & deliver','Who pays / acts?'),('5. Verify & remedy','Did it work?')]
for i,(a,b) in enumerate(steps):
 x=65+i*367;y=245
 d.rounded_rectangle((x,y,x+315,y+200),20,fill=pale,outline=green,width=4)
 d.text((x+17,y+40),a,font=font(23,True),fill=navy)
 d.text((x+17,y+103),b,font=font(22),fill=text)
 if i<4:
  d.polygon([(x+328,y+95),(x+347,y+95),(x+347,y+84),(x+360,y+100),(x+347,y+116),(x+347,y+105),(x+328,y+105)],fill=orange)
d.text((65,545),'Measure: coverage + quality + sustained outcome + correction of wrongful exclusion',font=font(28,True),fill=green)
d.text((65,605),'Community voice informs decisions; technical standards, law and budgets determine lawful implementation.',font=font(23),fill=text)
img.save(out/'development-accountability.png')
img=Image.new('RGB',(1900,860),'white');d=ImageDraw.Draw(img)
d.rounded_rectangle((20,20,1880,840),30,outline='#cddfe8',width=4,fill='#f9fcfe')
d.text((65,60),'Three rights pathways: distinct legal foundations, shared delivery challenge',font=font(40,True),fill=navy)
cols=[('HEALTH','Article 21 interpretation','NHM / public health /','eligible insurance packages','Care quality, referral, cost'),('FOOD SECURITY','NFSA, 2013','PHH: 5 kg/person/month','AAY: 35 kg/household/month','Receipt, nutrition, grievance'),('EDUCATION','Article 21A + RTE, 2009','Ages 6–14; school duties','Samagra Shiksha support','Attendance, safety, learning')]
for i,lines in enumerate(cols):
 x=75+i*610;y=230
 d.rounded_rectangle((x,y,x+550,y+425),28,fill=['#e9f3fa','#f8efe5','#e9f4ed'][i],outline=[navy,orange,green][i],width=5)
 d.text((x+30,y+35),lines[0],font=font(32,True),fill=navy)
 for j,s in enumerate(lines[1:]):d.text((x+30,y+112+j*67),s,font=font(22 if len(s)>28 else 25, j==0),fill=text)
d.text((85,715),'Common test: identify eligibility, the responsible officer, actual service quality and an effective appeal.',font=font(27,True),fill=green)
img.save(out/'rights-triangle.png')
print([p.name for p in out.iterdir()])
