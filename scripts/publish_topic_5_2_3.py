from pathlib import Path
from urllib.parse import urlsplit, unquote
import hashlib, json, re, subprocess, sys
import fitz, mistune
from bs4 import BeautifulSoup

root = Path("Paper 5/Unit 2 - Modern Applications of Science/Topic 3")
src = root / "source"
cp = json.loads(Path("project-control/PRODUCTION-CHECKPOINT.json").read_text())
ix = json.loads(Path("project-control/ACADEMIC_READINESS_75_TOPIC_STATUS_INDEX.json").read_text())
assert cp["total_topics"] == ix["total_topics"] == len(cp["topics"]) == 75
assert len({t["id"] for t in cp["topics"]}) == 75
assert len(ix["paths"]) == len(set(ix["paths"])) == 75
assert len(list(Path("project-control/academic-readiness").glob("[2-6]-[1-3]-[1-5].json"))) == 75
counts = {s: sum(t["readiness_status"] == s for t in cp["topics"]) for s in ("IN_PROGRESS","ASSESSED_REBUILD_REQUIRED","NOT_ASSESSED")}
assert counts == {"IN_PROGRESS":7,"ASSESSED_REBUILD_REQUIRED":38,"NOT_ASSESSED":30}, counts
assert set(ix["assessed_rebuild_required"]) == {t["id"] for t in cp["topics"] if t["readiness_status"] == "ASSESSED_REBUILD_REQUIRED"}
assert len(ix["assessed_rebuild_required"]) == 38 and ix["not_assessed_count"] == 30
assert cp["academically_approved"] == ix["independently_academically_approved_count"] == 0
assert all((Path(t["path"])/"complete-notes.pdf").is_file() for t in cp["topics"])
original = hashlib.sha256((root/"complete-notes.pdf").read_bytes()).hexdigest()
assert original == "5a1a65fe107fc58d73a063913d645bbc1137fb88b89798b1c87b3bee5c798592", original

md = (src/"complete-notes.md").read_text()
for f in ("original-mcqs.md","mains-model-answers.md","sources-and-audit.md"):
    assert (src/f).read_text().strip() in md, f
assert "Illustrative traceability audit" in md
word = lambda s: len(re.findall(r"\b[\w’-]+\b", s))
core = (src/"core.md").read_text()
concepts = re.findall(r"(?ms)^## (\d+)\. ([^\n]+)\n(.*?)(?=^## \d+\.|\Z)",core)
assert len(concepts) == 18, len(concepts)
concept_words = [word(b) for _,_,b in concepts]
assert min(concept_words) >= 300, concept_words
mcq_blocks = re.findall(r"(?ms)^### MCQ (\d+)\. (.*?)(?=^### MCQ \d+\.|^## |\Z)",md)
assert len(mcq_blocks) == 30, len(mcq_blocks)
answers = []
for n,b in mcq_blocks:
    assert int(n) == len(answers)+1, n
    assert all(re.search(r"(?m)^"+o+r"\. ",b) for o in "ABCD"), n
    a = re.search(r"\*\*Answer:\s*([ABCD])\.",b)
    assert a, n
    answers.append(a.group(1))
distribution = {a:answers.count(a) for a in "ABCD"}
assert distribution == {"A":4,"B":17,"C":8,"D":1}, distribution
mains = (src/"mains-model-answers.md").read_text()
models = re.findall(r"(?ms)^### Mains model (\d+)\. ([^\n]+)\n(.*?)(?=^### Mains model \d+\.|^## |\Z)",mains)
assert len(models) == 6, len(models)
body_counts = [word(re.sub(r"\*\*[^*]+\.\*\*","",b)) for _,_,b in models]
assert len(body_counts) == 6 and all(200 <= n <= 250 for n in body_counts), body_counts
assert len(list((root/"diagrams").glob("*.png"))) == 3

pdf = src/"integrated-student-edition-cycle56.pdf"
subprocess.run([sys.executable,"scripts/render_topic_5_2_3_integrated.py","--input",str(src/"complete-notes.md"),"--output",str(pdf)],check=True)
doc = fitz.open(pdf)
blank = [i+1 for i,p in enumerate(doc) if len(p.get_text().strip()) < 60]
images = sum(len(p.get_images()) for p in doc)
boundary = []
for i,p in enumerate(doc):
    for b in p.get_text("blocks"):
        x0,y0,x1,y1 = b[:4]
        if x0 < -1 or y0 < -1 or x1 > p.rect.width+1 or y1 > p.rect.height+1: boundary.append(i+1)
assert 20 <= len(doc) <= 45 and not blank and images >= 3 and not boundary, (len(doc),blank,images,boundary)

body = mistune.create_markdown(plugins=["table","strikethrough"])(md)
rendered = BeautifulSoup(body,"html.parser")
for im in rendered.find_all("img"):
    u=im.get("src","")
    if u.startswith("../diagrams/"): im["src"]="diagrams/"+u.split("/")[-1]
seen={}
for h in rendered.find_all(["h1","h2","h3"]):
    slug=re.sub("[^a-z0-9]+","-",h.get_text(" ",strip=True).lower()).strip("-") or "section"
    n=seen.get(slug,0);seen[slug]=n+1
    if n:slug+=f"-{n}"
    h["id"]=slug
head='''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>TGPSC 5-2-3</title><style>body{font-family:system-ui,sans-serif;max-width:980px;margin:auto;padding:2rem;line-height:1.65;color:#172b3b}h1,h2,h3{color:#173e65}table{border-collapse:collapse;width:100%}th,td{border:1px solid #cdd9e3;padding:.55rem;text-align:left}th{background:#eaf2f7}img{max-width:100%;height:auto}a{color:#145c98}.banner{padding:1rem;background:#fff2d4;border:1px solid #b99045}</style></head><body><nav><a href="../../../index.html">Study portal</a></nav><p class="banner"><strong>STUDENT DRAFT — NOT ACADEMICALLY APPROVED.</strong> Complete independent source, MCQ, diagram and browser-accessibility checks pending.</p><p><a href="source/integrated-student-edition-cycle56.pdf">Integrated PDF</a> · <a href="source/complete-notes.md">Editable master</a> · <a href="complete-notes.pdf">Preserved original PDF</a></p>'''
(root/"index.html").write_text(head+str(rendered)+"</body></html>")
soup=BeautifulSoup((root/"index.html").read_text(),"html.parser")
ids={x.get("id") for x in soup.find_all(id=True)}
bad_files=[];bad_fragments=[];file_links=0;fragment_links=0;spa_routes=0
for tag in soup.find_all(["a","img","script","link"]):
    u=tag.get("href") or tag.get("src")
    if not u:continue
    if "#/" in u:spa_routes+=1;continue
    p=urlsplit(u)
    if p.scheme or u.startswith("//"):continue
    if p.path:
        file_links+=1
        if not (root/unquote(p.path)).resolve().exists():bad_files.append(u)
    if p.fragment:
        fragment_links+=1
        if unquote(p.fragment) not in ids:bad_fragments.append(u)
assert not bad_files and not bad_fragments, (bad_files,bad_fragments)

pdf_sha=hashlib.sha256(pdf.read_bytes()).hexdigest()
qa={"date":"2026-10-28","topic":"5-2-3","cycle":55,"original_pdf_sha256":original,"original_preserved":True,
    "integrated_pdf_sha256":pdf_sha,"integrated_pdf_pages":len(doc),"pdf_images":images,"blank_pages":blank,
    "text_boundary_violations":boundary,"concept_count":len(concepts),"min_concept_words":min(concept_words),
    "original_mcqs":30,"correct_answers":distribution,"distractors":90,"mains_body_only_counts":body_counts,"mains_count_method":"regex word tokens after removing bold subheading labels; hyphenated tokens may differ from Cycle53 whitespace method",
    "html_file_links_checked":file_links,"broken_files":bad_files,"html_fragment_links_checked":fragment_links,
    "broken_fragments":bad_fragments,"spa_routes_excluded":spa_routes,
    "source_checks":"five bounded correct-key proposition checks (Q13, Q15, Q16, Q21, Q25); remaining 25 keys and all distractors unverified",
    "independent_academic_approvals":0,"R8":"BLOCKED_NOT_PASS",
    "actual_downloaded_post_edit_artifact_qa":False,"browser_accessibility_certified":False}
(root/"QA-REPORT.md").write_text("# Cycle56 CI render QA\n\n"+json.dumps(qa,indent=2)+"\n")
(root/"README.md").write_text("# Paper V / Unit II / Topic 3 — Food Biotechnology, Food Safety, Organic Farming, Mechanisation and Safe Drinking Water\n\nOriginal 24-page PDF preserved (SHA256 "+original+").\nCycle56 editable master, offline HTML and integrated PDF synchronized through deterministic CI.\n18 concepts >=300 words, 30 original practice MCQs, six structured 200–250 body-word mains, three inherited diagrams.\nFive bounded correct-key correspondences only; no full independent MCQ, mains, diagram, syllabus or browser audit.\nZero academic approvals. No official PYQs authenticated.\n")
manifest=json.loads((root/"manifest.json").read_text())
manifest["academic_status"]="not_approved"
manifest["official_syllabus_authenticated"]=False
manifest["syllabus_source_limitation"]="Inherited direct 2024 syllabus assertion not reauthenticated this cycle; R1 IN_PROGRESS"
manifest["integrated_pdf_status"]="CI_rendered_independent_academic_audit_pending"
manifest["integrated_pdf_pages"]=len(doc)
manifest["integrated_pdf_sha256"]=pdf_sha
manifest.setdefault("metrics",{})["mains_answer_word_counts"]=body_counts
manifest["metrics"]["mains_count_method"]="body-only, excluding question and subheading labels"
manifest["metrics"]["concepts_below_300"]=0
manifest["metrics"]["source_register"]=23
manifest["metrics"]["correct_answer_distribution"]=distribution
files={}
for f in root.rglob("*"):
    if f.is_file() and f.name!="manifest.json":
        files[f.relative_to(root).as_posix()]=hashlib.sha256(f.read_bytes()).hexdigest()
manifest["files"]=files
(root/"manifest.json").write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+"\n")
Path("project-control/academic-readiness/5-2-3-cycle56-ci-render-qa-2026-10-28.json").write_text(json.dumps(qa,indent=2)+"\n")
print(json.dumps(qa,indent=2))
