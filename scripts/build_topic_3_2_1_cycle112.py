#!/usr/bin/env python3
"""Deterministically integrate Cycle112 source-critical additions into one editable master."""
from pathlib import Path
import argparse, hashlib, re, json
p=argparse.ArgumentParser()
p.add_argument('--baseline',type=Path,required=True)
p.add_argument('--addendum',type=Path,required=True)
p.add_argument('--output',type=Path,required=True)
p.add_argument('--qa',type=Path,required=True)
a=p.parse_args()
baseline=a.baseline.read_bytes()
assert hashlib.sha256(baseline).hexdigest()=='dda89da835b98257dcf70f54351cdfbacb92594ffac17fa87bf5397ccc33968a', 'Baseline changed: reconcile, do not blindly overwrite'
text=baseline.decode('utf-8')
extra=a.addendum.read_text()
assert all(extra.count(m)==1 for m in ['@@CONCEPT@@','@@MCQS@@','@@SOURCES@@'])
concept=extra.split('@@CONCEPT@@',1)[1].split('@@MCQS@@',1)[0].strip()
mcqs=extra.split('@@MCQS@@',1)[1].split('@@SOURCES@@',1)[0].strip()
sources=extra.split('@@SOURCES@@',1)[1].strip()
assert text.count('## 5. Visual learning:')==1
assert text.count('## 7. Original mains practice')==1
assert text.count('**Internal accuracy gates performed:**')==1
assert '**Q26.**' not in text and '### Concept H.' not in text
text=text.replace('## 5. Visual learning:',concept+'\n\n## 5. Visual learning:',1)
text=text.replace('## 7. Original mains practice',mcqs+'\n\n## 7. Original mains practice',1)
text=text.replace('**Internal accuracy gates performed:**',sources+'\n\n**Internal accuracy gates performed:**',1)
text=text.replace('**Status:** Expanded research draft', '**Status:** Cycle112 coherent integrated research draft')
text=text.replace('Prepared 23 October 2026.', 'Updated 30 October 2026; original 23 October draft preserved separately.')
assert len(re.findall(r'^### Concept [A-H][.]',text,re.M))==8
assert len(re.findall(r'^[*][*]Q[0-9]+[.][*][*]',text,re.M))==30
assert len(re.findall(r'^[*][*]Q[0-9]+[.][*][*]',text,re.M))==30
assert len(re.findall(r'^[*][*]Answer: [ABCD][.]',text,re.M))==30
assert text.count('constitutional-amendment-thresholds.svg')==1
a.output.parent.mkdir(parents=True,exist_ok=True)
a.output.write_text(text)
qa={'source_baseline_sha256':hashlib.sha256(baseline).hexdigest(),'master_sha256':hashlib.sha256(a.output.read_bytes()).hexdigest(),'concepts':8,'original_practice_mcqs':30,'mains':6,'source_conflict':'News On AIR 298+230 vs 489; original division record NOT retrieved','academic_approval':False}
a.qa.parent.mkdir(parents=True,exist_ok=True)
a.qa.write_text(json.dumps(qa,indent=2)+'\n')
print(json.dumps(qa,indent=2))
