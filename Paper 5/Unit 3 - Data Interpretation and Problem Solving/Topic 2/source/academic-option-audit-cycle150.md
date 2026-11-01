# Cycle 150 — source-correlated four-option academic review, Topic 5-3-2

**Date:** 1 November 2026. **Scope:** 10 existing original practice MCQs (17,22,23,24,25,26,27,28,29,30), 10 proposed keys and all 30 distractors. This is an **author-side bounded review**, not independent expert approval, not a claim of official TGPSC PYQs, and not full R5 completion. The previous Cycle 60 internal arithmetic review of 30 questions is not double-counted as independent source verification. All original questions and their keys remain in place.

## Source register — pages directly consulted for methodological correspondences

- **[C150-S1]** OpenStax, Principles of Data Science, section 3.4, Probability Theory. https://openstax.org/books/principles-data-science/pages/3-4-probability-theory. **Checked 1 November 2026.** Conditional probability and Bayes' rule; textbook method, not verification of invented numbers.
- **[C150-S2]** OpenStax, Contemporary Mathematics, section 2.7, Logical Arguments. https://openstax.org/books/contemporary-mathematics/pages/2-7-logical-arguments. **Checked 1 November 2026.** Modus tollens and conditional implication.
- **[C150-S3]** R Project, graphics::hist documentation (University of Minnesota mirror). https://rweb.stat.umn.edu/R/library/graphics/html/hist.html. **Checked 1 November 2026.** Non-equal class widths require area to encode relative frequency; density scale can be normalized.
- **[C150-S4]** UK Office for National Statistics, Sample design and estimation (27 Jan 2016). https://www.ons.gov.uk/methodology/methodologytopicsandstatisticalconcepts/sampledesignandestimation. **Checked 1 November 2026.** Sampling frames, weights and geographic representativeness.
- **[C150-S5]** Penn State STAT 100, Lesson 6.2, Simpson's paradox. https://online.stat.psu.edu/stat100/Lesson06. **Checked 1 November 2026.** Aggregation reversal and lurking variables; not a causal claim.
- **[C150-S6]** Stanford Encyclopedia of Philosophy, Simpson's Paradox (revised 6 June 2026). https://plato.stanford.edu/entries/paradox-simpson/. **Checked 1 November 2026.** Formal interpretation of reversal and causal-inference limitations.

## Question-by-question independent arithmetic and four-option reasoning

### MCQ 17 — existing answer C [C150-S1]

**Direct recomputation / inference:** Qualifiers: 40 rural + 60 urban = 100; P(rural | qualifies)=40/100=40%.

- **A:** 20%: 40/200 uses only urban applicants as denominator; not all qualifiers.
- **B:** 30%: equals 60/200 urban qualification rate, a different event.
- **C:** 40%: correct; numerator rural qualifiers 40 and conditioning group all qualifiers 100.
- **D:** 50%: does not follow from any appropriate conditioning denominator.

**Editorial quality flag:** Clear numerical key; the question should emphasize that the 40 and 60 are counts of qualifying applicants, not rates.

### MCQ 22 — existing answer D [C150-S2]

**Direct recomputation / inference:** All A are B; some B are C. The B∩C witnesses may be outside A or inside A, so A∩C is not entailed and its negation is not entailed.

- **A:** All A are C: counterexample has an A outside C.
- **B:** Some A are C: counterexample has all C-members in B outside A.
- **C:** No A are C: counterexample permits some A also in C.
- **D:** No definite A–C overlap: correct as a statement of non-entailment, NOT a claim that A∩C is empty.

**Editorial quality flag:** Wording is meta-logical and unusually terse. Prefer 'No definite conclusion about A–C overlap can be drawn' in a controlled future revision; do not claim formal syllogism PYQ provenance.

### MCQ 23 — existing answer B [C150-S2]

**Direct recomputation / inference:** P→Q and not-Q entail not-P by modus tollens; a true P would force Q and contradict not-Q.

- **A:** P is true: incompatible with P→Q and not-Q.
- **B:** P is false: correct deductive conclusion.
- **C:** Q is true: explicitly contradicts premise not-Q.
- **D:** Nothing: wrong because modus tollens yields a definite conclusion.

**Editorial quality flag:** All distractors straightforward; D is weak because the inference rule is explicit.

### MCQ 24 — existing answer C [C150-S2]

**Direct recomputation / inference:** Equation I x+y=10 has infinitely many pairs; II x−y=2 likewise; together 2x=12 so x=6, y=4.

- **A:** I only: not sufficient; x=0,y=10 and x=5,y=5 both satisfy I.
- **B:** II only: not sufficient; x=2,y=0 and x=3,y=1 both satisfy II.
- **C:** Both together only: correct unique solution x=6.
- **D:** Neither together: false because simultaneous independent equations determine x.

**Editorial quality flag:** Arithmetic internally recomputed. The referenced logic source is conceptual; algebraic result is a direct calculation.

### MCQ 25 — existing answer C [C150-S1]

**Direct recomputation / inference:** Out of 10,000: 100 have condition, 9,900 do not. True positives=0.90×100=90; false positives=0.05×9900=495. PPV=90/(90+495)=0.153846≈15.4%.

- **A:** 1%: base prevalence, not posterior probability after a positive result.
- **B:** 5%: false-positive rate among those without the condition, not PPV.
- **C:** 15.4%: correct positive predictive value from the stated cohort.
- **D:** 90%: sensitivity among affected people, not probability of condition given a positive result.

**Editorial quality flag:** Method is valid for the stated hypothetical prevalence/sensitivity/FPR. It is NOT a real-world diagnostic-performance estimate.

### MCQ 26 — existing answer B [C150-S1]

**Direct recomputation / inference:** Percentage-point change = 60−50=10 points. Relative percentage increase=(60−50)/50×100=20%.

- **A:** 10%: confuses 10 percentage points with 10% relative increase.
- **B:** 20%: correct relative increase from the initial 50% baseline.
- **C:** 50%: original rate, not its relative change.
- **D:** 60%: new rate, not its relative change.

**Editorial quality flag:** Key clear; distractors C and D are weak baseline/end-value cues.

### MCQ 27 — existing answer C [C150-S3]

**Direct recomputation / inference:** For a frequency-area histogram with unequal class widths, rectangle area equals class frequency: height=frequency/width. For a unit-area density histogram height=relative frequency/width; both are density rather than raw frequency.

- **A:** Raw frequency always: wrong with unequal widths because area would scale by width twice.
- **B:** Class midpoint: locates bin horizontally; not a height.
- **C:** Frequency density: correct in the frequency-area convention; normalized density differs by a constant 1/n.
- **D:** Cumulative frequency: belongs to cumulative displays, not the ordinary bin height.

**Editorial quality flag:** QUALIFICATION REQUIRED: question should explicitly say 'bar area proportional to class frequency' or 'frequency histogram'; density can be normalized. Keep C as best current option, but do not mark as independently approved.

### MCQ 28 — existing answer B [C150-S1]

**Direct recomputation / inference:** Starting at 100: after +25% gives 125; after −20% of 125 gives 100. Factor 1.25×0.80=1.

- **A:** −5%: incorrectly adds signed percentages without compounding.
- **B:** 0%: correct, final equals initial.
- **C:** 5%: incorrectly subtracts 20 from 25.
- **D:** 10%: no matching multiplicative calculation.

**Editorial quality flag:** Answer clear; A/C distractors are nearly the same misconception and could be diversified.

### MCQ 29 — existing answer B [C150-S4]

**Direct recomputation / inference:** Sampling households from one village does not automatically cover the district population. Inference requires a suitable frame/design, possible weights, coverage and nonresponse assessment.

- **A:** Always true: unjustified geographic extrapolation.
- **B:** Not necessarily true: correct; design and coverage must be evaluated.
- **C:** True if n>30: arbitrary sample-size threshold cannot fix geographic coverage bias.
- **D:** True if all ages included: age diversity within one village cannot establish district-wide representativeness.

**Editorial quality flag:** A/C/D are conspicuously weak distractors; strengthen examination discrimination in a future controlled revision.

### MCQ 30 — existing answer B [C150-S5,C150-S6]

**Direct recomputation / inference:** Low risk A=81/90=90%, B=10/10=100%. High risk A=5/10=50%, B=54/90=60%. Overall A=86/100=86%, B=64/100=64%. Thus B exceeds A within each stratum, but A exceeds B pooled; this is a strict Simpson reversal.

- **A:** A higher in both groups: contradicted by 90<100 and 50<60.
- **B:** B higher in both, A higher pooled: correct after all four fractions and both totals are checked.
- **C:** Same pooled rate: false, 86%≠64%.
- **D:** B higher pooled: false, 64%<86%.

**Editorial quality flag:** Correct mathematical illustration, not evidence of superior causal hospital performance. B is much longer than the distractors and may cue the key; revise options only after full revalidation.

## Boundaries and next gates

- This review covers exactly 10 of 30 original questions and 30 of 90 distractors at the source-correlated four-option level. The other 20 keys and 60 distractors still require equivalent review, notwithstanding Cycle 60 internal arithmetic checks.
- All six mains model answers require claim-level evidence review; their prior body-only length counts are not proof of factual correctness.
- The three inherited diagrams require scientific/logic accuracy assessment and complete browser/print accessibility checks. This audit does not certify them.
- R1 direct Commission PDF reauthentication remains incomplete; R2–R8 are not collectively PASS, R9 NOT_STARTED and independent approvals ZERO.
- Source pages support the **methods**; the example numbers are invented pedagogical data, not observed Telangana statistics.
