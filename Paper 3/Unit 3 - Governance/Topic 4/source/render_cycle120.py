"""Cycle120 guarded integrated renderer: preserve the original 35-page PDF and master."""
from pathlib import Path
import hashlib, json, re, runpy, shutil
from collections import Counter
import fitz

ROOT=Path(__file__).resolve().parent.parent
SRC=ROOT/'source'
ORIGINAL_SHA='0d4fb8463bbced10bc1f481020e9b2350f77ae646f1c0dcdd910781a33a98a63'
def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
legacy_pdf=ROOT/'complete-notes.pdf'
assert sha(legacy_pdf)==ORIGINAL_SHA, 'Original PDF changed: refuse overwrite'
original_pdf=legacy_pdf.read_bytes()
original_master=(SRC/'complete-notes.md').read_bytes()
original_html=(ROOT/'index.html').read_bytes()
mcqs=(SRC/'original-mcqs.md').read_text()+'\n'+(SRC/'cycle120-mcqs.md').read_text()
concepts=(SRC/'detailed-notes.md').read_text()+'\n'+(SRC/'cycle120-concept.md').read_text()
assert len(re.findall(r'(?m)^### Q\d+\.',mcqs))==30
assert len(re.findall(r'(?m)^\*\*Answer:\s*[ABCD]',mcqs))==30
assert len(re.findall(r'(?m)^## \d+\.',concepts))==15
assert len(re.findall(r'(?m)^### Mains Q\d+\.',(SRC/'mains-model-answers.md').read_text()))==6
pdf=SRC/'integrated-student-edition-cycle120.pdf'
try:
    runpy.run_path(str(SRC/'build_topic.py'),run_name='__main__')
    md=(SRC/'complete-notes.md').read_text()
    md=md.replace('Expanded draft | 31 October 2026','Cycle120 integrated draft | 31 October 2026')
    (SRC/'integrated-student-edition-cycle120.md').write_text(md)
    shutil.copy2(legacy_pdf,pdf)
    html=(ROOT/'index.html').read_text()
    html=html.replace('href="complete-notes.pdf"','href="source/integrated-student-edition-cycle120.pdf"')
    html=html.replace('href="source/complete-notes.md"','href="source/integrated-student-edition-cycle120.md"')
    html=html.replace('Expanded draft — academically unapproved','Cycle120 integrated draft — academically unapproved')
    # A <base href="../"> fixes image paths but silently redirects fragment-only
    # TOC links to the parent index instead of anchors in this document.
    # Keep the offline HTML self-contained: rewrite only file references,
    # leaving #section-N links relative to this same document.
    offline_html = html.replace('href="../../../index.html"', 'href="../../../../index.html"')
    offline_html = offline_html.replace('href="source/integrated-student-edition-cycle120.pdf"', 'href="integrated-student-edition-cycle120.pdf"')
    offline_html = offline_html.replace('href="source/integrated-student-edition-cycle120.md"', 'href="integrated-student-edition-cycle120.md"')
    offline_html = offline_html.replace('src="visuals/', 'src="../visuals/')
    assert '<base ' not in offline_html, 'Fragment navigation must remain document-relative'
    (SRC/'integrated-student-edition-cycle120.html').write_text(offline_html)
    (ROOT/'index.html').write_text(html)
finally:
    legacy_pdf.write_bytes(original_pdf)
    (SRC/'complete-notes.md').write_bytes(original_master)
    if not pdf.exists(): (ROOT/'index.html').write_bytes(original_html)
assert sha(legacy_pdf)==ORIGINAL_SHA
with fitz.open(pdf) as doc:
    pages=len(doc)
    assert 30<=pages<=55,pages
    txt='\n'.join(p.get_text() for p in doc)
    assert 'Q26.' in txt and 'Q30.' in txt and 'Unspent CSR Account' in txt
    assert all(len(p.get_text().strip())>45 for p in doc)
    for i,p in enumerate(doc):
        for block in p.get_text('dict')['blocks']:
            if block['type']==0:
                x0,y0,x1,y1=block['bbox']
                assert x0>=15 and y0>=0 and x1<=p.rect.width-12 and y1<=p.rect.height-7,(i+1,block['bbox'])
files=['index.html','source/cycle120-concept.md','source/cycle120-mcqs.md','source/cycle120-source-audit.md','source/integrated-student-edition-cycle120.md','source/integrated-student-edition-cycle120.pdf','source/integrated-student-edition-cycle120.html']
answers=re.findall(r'(?m)^\*\*Answer:\s*([ABCD])',mcqs)
manifest={'topic_id':'3-3-4','cycle':120,'academic_status':'ASSESSED_REBUILD_REQUIRED','academic_approved':False,'original_pdf_sha256':ORIGINAL_SHA,'original_pdf_preserved':True,'integrated_pdf_pages':pages,'concepts':15,'original_practice_mcqs':30,'answer_distribution':dict(Counter(answers)),'mains_answers':6,'official_pyqs_verified':0,'source_check_scope':'Five new MCQ keys and 15 distractors bounded author-side; 25 older MCQs and six mains not independently audited','files_sha256':{p:sha(ROOT/p) for p in files}}
(SRC/'integrated-cycle120-manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n')
print('CYCLE120',json.dumps({'pages':pages,'integrated_pdf_sha256':sha(pdf),'original_pdf_sha256':sha(legacy_pdf),'mcqs':30}))
