#!/usr/bin/env python3
"""Import the validated Paper II checkpoint without overwriting the site portal."""
from pathlib import Path
from zipfile import ZipFile
from html import escape
import json, re, sys
try:
    import mistune
except ImportError:
    sys.exit("Install the 'mistune' package first.")
archive=Path("incoming/TGPSC_PAPER_II_15_TOPICS_REVISED_DRAFT.zip")
if not archive.exists():sys.exit(f"Missing upload: {archive}")
source_root="TGPSC-GROUP-1/"
topic_re=re.compile(r"^Paper 2/Unit [123] - [^/]+/Topic [1-5]$")
allowed={"syllabus-index","quick-revision","high-value-exam-facts","detailed-notes","visual-learning","verified-mcqs","verified-mains-pyqs","answer-blueprints","complete-model-answers","original-practice","current-affairs","references","quality-audit"}
sections=[("syllabus-index","Syllabus and index"),("quick-revision","Quick revision"),("high-value-exam-facts","Exam-critical facts"),("detailed-notes","Detailed notes"),("visual-learning","Comparisons and diagrams"),("verified-mcqs","Verified MCQs"),("verified-mains-pyqs","Verified mains PYQs"),("answer-blueprints","Mains answer blueprints"),("complete-model-answers","Complete model answers"),("original-practice","Original practice"),("current-affairs","Current affairs"),("references","References"),("quality-audit","Quality audit")]
files={}
with ZipFile(archive) as z:
    if z.testzip():sys.exit("ZIP integrity failed")
    if len(z.infolist())>2500 or sum(i.file_size for i in z.infolist())>70_000_000:
        sys.exit("Unexpected ZIP size or file count")
    for info in z.infolist():
        if info.is_dir() or not info.filename.startswith(source_root):continue
        rel=info.filename[len(source_root):]
        folder,_,name=rel.rpartition("/")
        if topic_re.fullmatch(folder) and name=="complete-notes.pdf":
            if info.file_size>20_000_000:sys.exit("Oversized topic PDF")
            data=z.read(info)
            if not data.startswith(b"%PDF-"):sys.exit("Invalid PDF")
            files[rel]=data
        elif folder.endswith("/source") and topic_re.fullmatch(folder[:-7]) and name.endswith(".md") and name[:-3] in allowed:
            if info.file_size>2_000_000:sys.exit("Oversized notes file")
            data=z.read(info);data.decode("utf-8");files[rel]=data
pdfs=[x for x in files if x.endswith("/complete-notes.pdf")]
if len(pdfs)!=15 or len({x.rpartition("/")[0] for x in pdfs})!=15:
    sys.exit("Expected 15 distinct Paper II PDFs; no changes made")
for pdf in pdfs:
    folder=pdf.rpartition("/")[0]
    md=files.get(folder+"/source/detailed-notes.md")
    if not md or len(md.decode("utf-8").split())<100:
        sys.exit("Missing substantive chapter: "+folder)
renderer=mistune.create_markdown(renderer="html",escape=True,plugins=["table","strikethrough"])
stylesheet="body{margin:0;background:#f5f7fb;color:#20314c;font:16px/1.75 system-ui,sans-serif}header{padding:30px max(18px,calc((100vw - 1080px)/2));background:#1c345f;color:#fff}header a{color:#fff}main{max-width:1080px;margin:auto;padding:15px}section{background:#fff;border:1px solid #dce4ee;border-radius:12px;margin:15px 0;padding:22px}nav{display:flex;gap:8px;flex-wrap:wrap;padding:12px 0}nav a{padding:7px;background:#e7ecfa;border-radius:6px}table{display:block;overflow:auto;border-collapse:collapse}td,th{border:1px solid #ccc;padding:7px}p,li{max-width:100ch}@media print{nav{display:none}header{background:#fff;color:#111}header a{color:#111}}"
topics=[]
for pdf in sorted(pdfs):
    folder=pdf.rpartition("/")[0]
    raw=files[folder+"/source/detailed-notes.md"].decode()
    match=re.search(r"^#\s+(.+)$",raw,re.MULTILINE)
    title=match.group(1).strip() if match else folder.split("/")[-1]
    parts=[];links=[]
    for slug,label in sections:
        key=folder+"/source/"+slug+".md"
        if key not in files:continue
        parts.append('<section id="'+slug+'"><h2>'+escape(label)+'</h2>'+renderer(files[key].decode())+'</section>')
        links.append('<a href="#'+slug+'">'+escape(label)+'</a>')
    page='<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+escape(title)+'</title><style>'+stylesheet+'</style></head><body><header><a href="../../../index.html#/paper/2">← Paper II portal</a><h1>'+escape(title)+'</h1><p>Expanded working draft; NOT academically approved.</p><a href="complete-notes.pdf">Download topic PDF</a></header><main><section><strong>Study-material notice:</strong> Original practice is not official PYQ. Historic claims, source coverage and all mains model answers need independent academic review.</section><nav>'+''.join(links)+'</nav>'+''.join(parts)+'</main></body></html>'
    target=Path(folder)/"index.html"
    target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(page,encoding="utf-8")
    topics.append({"path":folder,"sections":len(parts)})
for rel,data in files.items():
    target=Path(rel)
    target.parent.mkdir(parents=True,exist_ok=True)
    target.write_bytes(data)
Path("PAPER-II-IMPORT-REPORT.json").write_text(json.dumps({"topics":topics,"pdfs":len(pdfs),"markdown_files":len(files)-len(pdfs),"fully_approved":0},indent=2),encoding="utf-8")
print("Imported",len(topics),"topic pages,",len(pdfs),"PDFs and",len(files)-len(pdfs),"Markdown files.")
