## Six complete structured mains model answers — original practice

### Model answer 1: Explain a disciplined method for interpreting a complex two-way administrative table.

### Introduction
A two-way table classifies observations simultaneously by two characteristics, such as district and programme status. Accurate interpretation begins by understanding what a cell represents rather than rushing to percentage calculations. In administration, a denominator error can change a policy recommendation.

### Method
First, identify the title, population, period, units, data source and exclusions. Check whether categories are mutually exclusive and whether row and column totals reconcile. Second, distinguish row percentages, column percentages and grand-total percentages. A cell of 40 rural qualifiers among 100 rural applicants yields a 40% rural qualification rate; the same 40 among 140 total qualifiers yields a 28.57% rural share of qualifiers. These are different questions.

### Analytical checks
Use pooled numerators and denominators for combined rates, not unweighted averages of subgroup percentages. Reconstruct missing cells only where totals give enough independent equations. Investigate overlaps, suppressed observations, revised district boundaries and missing periods. For a trend comparison, maintain consistent definitions and population coverage.

### Telangana application
A district handbook may show larger enrolment counts in a populous mandal but higher enrolment rates in a smaller mandal. Reporting both measures prevents a misleading “best-performing mandal” ranking. Data should be accompanied by provenance and any sampling uncertainty.

### Conclusion
A sound table answer states the exact metric, demonstrates arithmetic, checks totals and distinguishes description from causal explanation. This turns tabulation into defensible evidence rather than a mechanical calculation.

### Model answer 2: Discuss conditional probability and Bayes rule with an administrative screening example.

### Introduction
Conditional probability changes the relevant sample space after information becomes available. It is central to screening, complaint prioritisation and interpreting alerts. Confusing P(A|B) with P(B|A) is a serious analytical error.

### Core principles
For P(B)>0, P(A|B)=P(A∩B)/P(B). Bayes rule gives P(A|B)=P(B|A)P(A)/P(B). The denominator P(B) is obtained by summing the probabilities of all mutually exclusive routes to B. Independence is a special assumption, not a default.

### Worked illustration
Assume an illustrative condition affects 1% of 10,000 people. A screening test has 90% sensitivity and 95% specificity. Of 100 affected people, 90 test positive. Of 9,900 unaffected, 5%, or 495, test positive falsely. Thus 585 positive tests contain 90 true cases. The probability of the condition after a positive result is 90/585, approximately 15.38%, not 90%.

### Interpretation and limitations
The low base rate explains the large false-positive share. If prevalence changes, the posterior changes even with unchanged test performance. Expected counts may differ from observed counts; test independence and accuracy can vary by population. Screening results therefore require confirmation and context.

### Conclusion
Bayesian reasoning makes the prior probability explicit and prevents overconfident interpretation of alerts. Public officials should disclose assumptions, denominators and uncertainty rather than converting a sensitivity figure directly into an individual risk estimate.

### Model answer 3: Show how Venn diagrams and inclusion–exclusion improve measurement of programme reach.

### Introduction
When households receive more than one public service, adding programme enrolments can exaggerate the number of unique beneficiaries. Set theory provides a precise language for counting overlaps without treating every overlap as wrongdoing.

### Two-programme method
Let A denote crop-advisory recipients and B livestock-advisory recipients. The unique reach is |A∪B|=|A|+|B|−|A∩B|. In an illustrative population of 1,000 households, suppose |A|=520, |B|=410 and |A∩B|=170. Then unique reach is 760; 240 households received neither. The count of households receiving only crop advice is 350, and only livestock advice is 240.

### Extension and audit
For three programmes, subtract pairwise intersections and add the triple intersection once. Draw the central overlap first, then pairwise-only regions and single-service regions. Verify that disjoint regions sum to the population. If source lists use inconsistent household identifiers, matching errors can create false overlaps or omissions.

### Administrative interpretation
Overlap may reflect desirable integrated service delivery. The mathematical task is to report unique reach; an administrative audit separately asks whether duplicate payments, eligibility violations or poor targeting occurred. Person-level linking should follow applicable privacy and data-governance safeguards.

### Conclusion
Inclusion–exclusion prevents double counting and clarifies the distinction between total service interactions and unique households reached. Transparent definitions make programme statistics more credible and useful for resource allocation.

### Model answer 4: Explain why independence assumptions matter in probability-based public decisions.

### Introduction
Probability calculations are only as reliable as the assumptions describing how events arise. Independence means knowing one event does not change the probability of another. In many real administrative settings, shared conditions make outcomes dependent.

### Mathematical distinction
For independent A and B, P(A∩B)=P(A)P(B). Disjoint events instead have zero intersection and generally are not independent when both have positive probabilities. Drawing two women without replacement from four women and six men has probability (4/10)(3/9)=2/15. Replacing the first person changes the probability to (4/10)²=4/25.

### Practical implications
Repeated failures of electricity feeders during one storm are correlated through weather. Multiplying marginal failure probabilities as though events were independent can underestimate simultaneous outages. Similarly, household observations clustered in one village share conditions and should not be treated as independent district-wide samples without design adjustment.

### Telangana application
Rainfall and crop-loss probabilities vary by mandal, soil and irrigation access. A single statewide average cannot describe every local risk. The Telangana statistical directorate's mandal-level data can help identify heterogeneity, while survey methodology determines appropriate weights and uncertainty measures.

### Conclusion
Before applying a formula, identify the experiment, replacement rule, common causes and sampling design. Where dependence is plausible, use conditional probabilities, stratification or sensitivity analysis. An explicitly qualified estimate is better than a precise but unjustified probability.

### Model answer 5: Assess how logical reasoning and data sufficiency can improve governance decisions.

### Introduction
Logical reasoning separates what evidence establishes from what merely seems plausible. Data sufficiency asks whether available facts determine an answer uniquely. Both skills are essential for transparent administration and for solving aptitude questions accurately.

### Formal reasoning
A statement “if P then Q” supports P therefore Q and not Q therefore not P. It does not justify Q therefore P. If a road is flooded, it may be closed; observing closure alone does not prove flooding because repairs could also close it. Syllogisms similarly require care: all A being B and some B being C do not establish that any A are C.

### Sufficiency test
Suppose an audit asks for x, with statement I: x+y=12 and statement II: x−y=4. Neither independently determines x; together they yield x=8. If a question asks only whether x is positive, the inequality x>3 would be sufficient without a precise value. Each statement must first be evaluated alone.

### Governance application
A rise in school attendance after a transport intervention does not prove causation. Seasonal trends, scholarships and record changes are alternative explanations. Officials should identify the claim, premises, missing comparisons and possible confounders before presenting a conclusion as established fact.

### Conclusion
Logical validity and factual truth are separate tests. By requiring explicit premises, counterexamples and adequate data, public institutions can reduce unjustified inferences while still making practical decisions under uncertainty.

### Model answer 6: Develop a step-by-step strategy for Paper V Unit III reasoning and diagrammatic problems.

### Introduction
Data interpretation and reasoning questions reward accurate representation, denominator discipline and logical consistency. The objective is not merely speed; it is obtaining an answer that can be checked independently under examination pressure.

### Representation strategy
Read the question twice, marking the requested quantity and relevant units. Convert a complex table into row and column totals, a sequential draw into a probability tree, overlapping groups into a Venn diagram, and seating conditions into numbered positions. For a diagram, identify the scale, legend, direction and whether shapes represent counts or cumulative values.

### Calculation and verification
Write the governing relation before inserting numbers. For pooled rates, add successes and denominators separately. For conditional probabilities, define the condition as the denominator. For permutations, ask whether order matters; for combinations, ask whether it does not. For ranks without ties, use N=r+s−1. After solving, verify probabilities lie between zero and one and disjoint Venn regions sum to the stated total.

### Managing ambiguity
If a sequence admits multiple simple rules, state the assumed pattern. If an arrangement has several valid solutions, do not invent a unique answer. Distinguish a possible conclusion from a necessary one. In a policy scenario, separate descriptive association from causation and disclose data limitations.

### Conclusion
Practise mixed sets of original questions and classify errors as reading, modelling, arithmetic or inference failures. A systematic audit trail develops transferable reasoning skill, protects marks and produces clearer evidence-based administrative decisions.