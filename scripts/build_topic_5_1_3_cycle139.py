from pathlib import Path
import re,hashlib,json

root=Path('Paper 5/Unit 1 - Role and Impact of Science and Technology/Topic 3')
src=root/'source'
audit=src/'cycle139-four-concept-ten-mcq-primary-source-audit.md'
master=src/'integrated-editable-master-cycle139.md'
text=audit.read_text(encoding='utf-8')
core=(src/'core.md').read_text(encoding='utf-8')
for n in (10,11,12,16):
    block=re.search(r'(?ms)^### '+str(n)+r'\. .*?(?=^### (?:10|11|12|16)\. |^## Ten existing|\Z)',text)
    assert block, n
    addition=block.group().strip()
    target=re.search(r'(?ms)^## '+str(n)+r'\. .*?(?=^## \d+\.|\Z)',core)
    assert target,n
    core=core[:target.end()]+'\n### Cycle139 source-based expansion\n\n'+addition+'\n\n'+core[target.end():]
parts=[('Syllabus and examination map','syllabus-and-summary.md'),('Quick revision','quick-revision.md'),('Core concepts',None),('Worked applications','worked-applications.md'),('Visual learning','visual-learning.md'),('Original practice MCQs','original-mcqs.md'),('Mains model answers','mains-model-answers.md'),('Answer blueprints','answer-blueprints.md'),('Source register','sources-and-audit.md')]
sections=[]
for title,name in parts:
    if name is None:body=core
    else:
        f=src/name
        if not f.is_file():continue
        body=f.read_text(encoding='utf-8')
    sections.append('# '+title+'\n\n'+body)
out='# Space Programme in India: INSAT, IRS, EDUSAT, Chandrayaan-1 and Developmental Applications\n\n**TGPSC Group I | Paper V | Unit I | Topic 3 | Cycle139 integrated student edition | NOT academically approved | 31 October 2026**\n\n'+'\n\n---\n\n'.join(sections)+'\n\n---\n\n# Cycle139 primary-source and MCQ audit\n\n'+text
assert len(re.findall(r'(?m)^## \d+\. ',core))==16
assert len(re.findall(r'(?m)^### MCQ \d+\.',out))==30
assert len(re.findall(r'(?m)^### Model \d+\.',out))==6
assert '12 October 2026' in out and '23 October 2026' in out
master.write_text(out,encoding='utf-8')
print(json.dumps({'master':str(master),'sha256':hashlib.sha256(master.read_bytes()).hexdigest(),'bytes':len(master.read_bytes())}))
