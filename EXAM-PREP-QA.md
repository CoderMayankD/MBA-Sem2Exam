# Exam Prep — Your Questions, Answered One by One

_Subjects: Managerial Accounting (MBACCZG502 / "FMA") and Managing People & Organization (MBACCZG511). Format: open-book (EC3)._

_Grounded in: your generated lecture notes (`*/Notes/`), the course's own question banks and case files (`*/shared/`), the classmates' consolidated "All Sub Index for Open Book Exam", the MPO sample mid-sem paper, and the stored exam-rules note. Where a claim comes from a specific source it is flagged inline. **This file is study material only — see Q1, it cannot go into the exam room.**_

---

## Q1 — What can I take into the exam, and where do I get it?

**Format:** BITS open-book exam (EC3). "Open book" here does **not** mean "look everything up" — see Q4. It means a specific, limited set of *printed / published* material is allowed.

### ✅ Permitted in the exam hall
| Item | Notes |
|---|---|
| **Faculty-approved watermarked Consolidated PDF** | Must be in a *properly bound* format (spiral/perfect bound), not loose sheets. This is the one document you build your whole open-book strategy around. |
| **Publisher copies of prescribed textbooks / reference books** | Only the actual published books named in the course handout. Photocopies / printouts of books are *not* the same thing. |
| **Scientific calculator** | Non-programmable, non-statistical only. |

### ❌ NOT permitted
- Soft copies of any reference material (laptop/phone/tablet).
- Solved questions, model solutions, previous-semester Q&A-format material.
- Loose sheets of reference material.
- Handwritten notes, "unauthorized" lecture notes, solution manuals.
- **AI-assisted / LLM-generated notes, tools, solved questions, model solutions.**
- Programmable or statistical calculators (the rules slide names the *Casio FX-991MS* as an example of what's disallowed — **confirm your own calculator model against the official instructions**, since interpretations of "programmable" vary).

### ⚠️ What this means for the material in *this* repo
Everything auto-generated here is **pre-exam revision only** and is explicitly barred from the hall:
- `*/Notes/*.md` and their PDFs (LLM-generated lecture notes)
- `*/Practice-Questions.md` / `.pdf` (LLM-generated + compiled solved questions)
- `Classmates/All Sub Index for Open Book Exam BITS-EC3.pdf` (a consolidated *index*, but it is an AI/independently-produced study aid, not the faculty-approved watermarked PDF — treat it as navigation practice, don't carry it in)

### ✅ The Managerial Accounting file you CAN take: `Managerial Accounting/ENCRYPTED FMA NSP S4.pdf`
This one **is** the permitted document. Verified from its metadata:
- Title **"BITS WILP Study Material"**, Author **"BITS Pilani – WILP Division"**, Creator **"BITS WILP Watermarking Tool v3.0"**, generated 17-Aug-2026.
- Every page carries the **"BITS WILP | Generated: 17-Aug-2026" watermark** + an "S1-2026-27 Work Integrated Learning Programmes" diagonal watermark — this is the faculty-approved watermarked consolidated PDF.
- 241 pages, 4:3 slides — it is the consolidation of all the FMA/Managerial Accounting decks (IFRS, 12 Red Flags, Ratio Analysis, Cash Flow, Costing, CVP, Standard Costing) into one file. The classmates' "All Sub Index" maps to this exact file page-for-page.
- Permissions: **printing allowed** (copy/edit disabled — that's fine, you're printing it). It opens without a password.
- **Action:** print it → **spiral/perfect bind** it (loose sheets are not allowed) → tab it using **Appendix A** below → carry that. Confirm with the course instructor that this Aug-2026 version is the one approved for *your* EC3 sitting.

### Where the permitted consolidated PDF comes from (general)
- It is the **official BITS WILP study material** for each course, from the **eLearn / Taxila (impartus) course portal**, or the version the course instructor circulates and states is approved for EC3.
- **MPO:** the two-part deck in `Managing People and Organization/shared/General/` — `...Lectures 1-9.pdf` (**D1**) and `...Lectures 10-16.pdf` (**D2**). Confirm it is the watermarked/approved copy, then print, bind, tab it the same way.

**Action:** get the approved PDF for each subject → print → **bind** → add tab index. Do this a week before, not the night before.

---

## Q2 — Managerial Accounting: the formulas & topics you must not miss

You said "Portal formulas … markup over the time" — that is the **P/V ratio / CVP family**, and yes, it is the single highest-yield block in the paper. Your notes are blunt about the exam shape:

> "Approximately 70–80% of the exam is expected to be **numerical**." — `Notes/16` Exam Pointers
> The exam tests **analysis as a manager**, not statement *preparation* — "Journal, Ledger, and Trial Balance … are not the focus of the exam." — `Notes/05`
> "The 'open book' format emphasizes **application and logic** … rather than simple formula substitution." — `Notes/15`

### Tier 1 — near-certain, master cold

**A. CVP / Break-even / P–V ratio (Lectures 12 & 14, index §8 pp.202–236)**

| Quantity | Formula |
|---|---|
| Contribution (total) | Sales − Variable Cost  →  also = Fixed Cost + Profit |
| Contribution per unit | SP/unit − VC/unit |
| **P/V ratio (contribution margin %)** | Contribution ÷ Sales × 100  =  (C per unit ÷ SP) × 100 |
| Identity to check every time | **VC% + P/V% = 100%** |
| Break-even (units) | Fixed Cost ÷ Contribution per unit |
| Break-even (₹ sales) | Fixed Cost ÷ P/V ratio |
| Margin of Safety (₹) | Actual Sales − Break-even Sales  (also = Profit ÷ P/V ratio) |
| Margin of Safety (units) | Profit ÷ Contribution per unit |
| **Profit** | Margin of Safety × P/V ratio |
| Sales (₹) for a target profit | (Fixed Cost + Target Profit) ÷ P/V ratio |
| Sales (units) for a target profit | (Fixed Cost + Target Profit) ÷ Contribution per unit |
| Fixed Cost (from BE sales) | Break-even Sales × P/V ratio |
| Pre-tax profit from post-tax | After-tax Profit ÷ (1 − tax rate) |
| Operating leverage | Contribution ÷ Profit |
| Indifference point (two cost structures) | set (C₁·Q − FC₁) = (C₂·Q − FC₂), solve Q |
| Multi-product BEP | Fixed Cost ÷ weighted-average contribution per *bundle* (use the sales mix ratio) |

**B. Standard Costing — the 6 variances (Lecture 15, index §9 pp.237–241)**
Put the **standard term first** so "favourable" comes out positive.

- Material Cost Variance: MCV = (SQ × SP) − (AQ × AP)
- Material Price Variance: MPV = AQ × (SP − AP)
- Material Usage Variance: MUV = SP × (SQ − AQ)
- Check: **MPV + MUV = MCV**
- Labour Cost Variance: LCV = (ST × SR) − (AT × AR)
- Labour Rate Variance: LRV = AT × (SR − AR)
- Labour Efficiency Variance: LEV = SR × (ST − AT)
- Check: **LRV + LEV = LCV**
- **SQ / ST are the standard quantity / time allowed for the ACTUAL output achieved** (e.g. std 5 kg/unit, actual output 200 units → SQ = 1,000 kg), *not* budgeted output. This is the #1 trap.
- If only totals are given, derive the rate first: SR = total std cost ÷ total std time.
- Focus is **material + labour**; overhead variances are "less critical" (`Notes/15`).

**C. Relevant-costing decisions (Lectures 11 & 13, index §8 "Make-or-Buy & Special Order")**
These are *logic* questions with light arithmetic. Rules to apply:
- **Sunk cost** (already incurred / won't change) → **ignore it**.
- **Opportunity cost** (contribution lost from the next-best use of a scarce resource) → **add it in**.
- **Fixed cost** → irrelevant *unless the decision itself changes it*.
- **Make or Buy:** compare *variable* make-cost vs outside price; add opportunity contribution of freed capacity; watch for a safety-critical / brand-range reason to keep making even at higher cost.
- **Special order:** accept if (i) spare capacity exists, (ii) price ≥ incremental cost of the extra units, (iii) no adverse knock-on to regular customers. If capacity is full, subtract the displaced regular contribution.
- **Drop a product:** compare contribution **lost** vs fixed cost **actually saved**. A line-item "loss" is not a reason to drop if the line still covers common fixed costs.
- **Limited resource / product mix:** rank by **contribution per unit of the scarce resource** (machine hour, kg, labour hour) — *not* profit per unit.
- **Process further:** earlier processing cost is sunk; compare only *extra* revenue vs *extra* cost.

**D. Cash Flow Statement — Indirect method, CFO (Lecture 16, index §4 pp.94–103)**
Start from PAT (or EBT/EBIT — identify which, it changes the interest treatment):
- **+ Depreciation / amortisation** (non-cash).
- **+ non-operating expenses** (loss on sale of asset; finance cost if you started below it).
- **− non-operating incomes** (profit on sale of asset; interest/dividend income).
- Working capital: asset ↑ → cash "locked" → **subtract**; liability ↑ → cash "freed" → **add** (and vice-versa).
- Classify by *what the item is*: asset-related → Investing; owner/lender funds → Financing; day-to-day → Operating. Receiving dividend = Investing; paying dividend = Financing.

### Tier 2 — very likely, know the formula + interpretation

**Ratio analysis (Lectures 9 & 10, index §3 pp.33–65).** Memorise these; look up the rest in the PDF:
- Current = CA ÷ CL; Quick = (CA − Inventory − Prepaid) ÷ CL; Absolute liquid = (Cash + Bank + ST investments) ÷ CL
- Gross Profit % = GP ÷ Net Sales × 100  (COGS = Opening stock + Purchases + Direct exp − Closing stock)
- Operating Profit % = EBIT ÷ Sales × 100; Net Profit % = PAT ÷ Net Sales × 100
- EPS = (PAT − Preference dividend) ÷ no. of equity shares; Diluted EPS adds convertibles to the denominator (**always ≤ Basic**)
- ROE = (PAT − Pref div) ÷ Equity shareholders' funds × 100
- ROCE = EBIT ÷ Capital Employed × 100  (Capital Employed = Debt + Equity)
- Debt–Equity = Long-term Debt ÷ Equity; Debt–Capital = Debt ÷ (Debt + Equity)
- Interest Coverage = EBIT ÷ Interest
- Debtors T/O = Net Credit Sales ÷ Avg Debtors; DSO = 365 ÷ Debtors T/O (some books use 360)
- Creditors T/O = Net Credit Purchases ÷ Avg Payables; DPO = 365 ÷ Creditors T/O
- Inventory T/O = COGS ÷ Avg Inventory; DIO = 365 ÷ Inventory T/O
- **Cash Conversion Cycle = DIO + DSO − DPO**
- P/E = Market price per share ÷ EPS
- DuPont: ROE = Net Profit Margin × Asset Turnover × Equity Multiplier

**Inventory valuation — FIFO / LIFO / WAC (index §6 pp.151–154).** In *rising* prices: FIFO → lower COGS, higher profit, higher tax; LIFO → higher COGS, lower profit, lower tax (LIFO is **banned under IFRS/IAS 2**, allowed under US GAAP). Know the *direction of the effect*, not just the definition.

### Tier 3 — supporting / conceptual (mostly lookup-able)
- Accounting principles / conventions (13 of them), accounting equation, asset vs liability vs income vs expense classification, prepaid vs outstanding adjustments — Lectures 1–8. Needed to *set up* a numerical, rarely asked standalone.
- IFRS/IAS specifics: revenue 5-step model (IFRS 15), fair-value hierarchy L1/L2/L3 (IFRS 13), IAS 2 inventory, IAS 16 PP&E, R&D treatment (research expensed, development capitalised) — index §1 pp.2–20.
- 12 red flags of financial-statement manipulation — index §2 pp.21–32 (`12 red flags.pptx`).
- Budgeting: cash budget, master budget, Zero-Base Budgeting — index §7 pp.155–160.
- Cost classification: direct/indirect, fixed/variable/semi-variable, relevant/irrelevant, prime cost — index §5 pp.120–150.

### The MA traps worth memorising (from your notes' "Tricky Logic & Traps")
- Variable cost **per unit is constant**; only *total* variable cost moves with volume.
- A "reduction in sales" hits profit by **ΔSales × contribution margin** (or × P/V%), **not** by the full selling price — fixed costs don't move.
- High current ratio ≠ liquid if it's all inventory/receivables. Negative working capital isn't automatically bad.
- Diluted EPS is **always ≤** Basic EPS.
- Use **Net Sales** as the denominator consistently across GP%, OP%, NP%.
- ROI/ROCE: profit is a *period* figure, investment is a *point-in-time* figure → use **average investment** = (Opening + Closing) ÷ 2.
- Debt–Equity uses **long-term** debt only (it measures solvency, not liquidity).
- Cash flow: when an asset is **sold**, the *whole cash proceeds* go in Investing; the profit/loss on sale is only used to *reverse it out* of Operating.
- "On credit / conversion / exchange / hire purchase" wording → usually a **non-cash** transaction.
- Special-order trap: compare offer price to **incremental cost**, never to full cost.

---

## Q3 — Which lectures (and which parts) are important and linked together for problem-solving?

### Managerial Accounting — the chains that produce exam questions

```
FOUNDATION            L1–L4  principles, accounting equation, classify A/L/I/E
   │                  L7–L8  build Statement of P&L + Balance Sheet, adjustments (prepaid/outstanding)
   │                  L5     "exam = analysis, not preparation" — journal/ledger/TB de-prioritised
   ▼
ANALYSIS OF STATEMENTS
   ├── Ratios              L9  (liquidity, solvency, turnover) + L10 (profitability, DuPont, evaluation)   → index §3
   └── Cash Flow (indirect) L16  (+ CFO/CFI/CFF, red flags)                                                → index §4
   ▼
COST & DECISION-MAKING (the heavily numerical spine)
   L11  cost classification; sunk cost; opportunity cost; fixed asset vs fixed cost; FIFO/LIFO/WAC
     │        (this logic is the PREREQUISITE for every L13 decision problem)
     ▼
   L12  CVP: contribution, P/V ratio, BEP, margin of safety
     │        (P/V ratio + MoS logic feeds directly into L14)
     ▼
   L13  applied decisions: make-or-buy, special order, drop-a-product, limited resource, process further
     │
     ▼
   L14  CVP continued: MoS ↔ profit, indifference point, multi-product bundles, target profit,
          + relevant-cost mini-cases (subsidy, inflation adjustment, step-fixed costs, multi-supplier)
   ▼
STANDARD COSTING
   L15  material + labour variances (MPV/MUV/MCV, LRV/LEV/LCV); "SQ/ST on actual output" rule
```

**The tightest linkages (a question in one needs the other):**
- **L11 → L13:** you cannot answer a make-or-buy / special-order / drop-product question without L11's sunk-cost & opportunity-cost logic. Study them as one block.
- **L12 → L14:** P/V ratio (L12) is the engine for MoS ↔ profit ↔ target-sales (L14). One integrated CVP question can pull from both.
- **L9/L10 ↔ L15/L16:** consistency of denominators (Net Sales, average balance-sheet figures, long-term debt) recurs everywhere. Learn the "rules of the denominator" once.
- **L7/L8 → everything:** COGS build-up, prepaid/outstanding adjustments, and the P&L→Balance-Sheet flow are the setup step for most numericals.
- **L1–L4** are worth the least direct marks — skim, don't camp there.

**If time is short, in order:** L12 + L14 (CVP) → L11 + L13 (decisions) → L15 (variances) → L16 (cash flow) → L9 + L10 (ratios) → L7 + L8 (statements) → L1–L4 (concepts).

### MPO — the topic clusters that produce exam questions

The paper is **subjective**: 5-mark theory questions + mini-case application (see the sample mid-sem in `shared/Sample paper - MidSem.docx`). 16 lecture-topics (D1 = topics 1–9, D2 = topics 10–16). Clusters, ranked by how reliably they show up:

| Rank | Cluster | Topics / models | Where (index) |
|---|---|---|---|
| 1 | **Motivation** | Maslow, Herzberg (hygiene vs motivators), Equity theory, Expectancy theory, Goal-setting; JCM; financial vs non-financial incentives | D1 p.137–186 |
| 2 | **Perception & Decision-Making** | Attribution theory (distinctiveness / consensus / consistency), fundamental attribution error, self-serving bias; judgment shortcuts (halo, stereotyping); decision biases (overconfidence, anchoring, confirmation, availability, escalation of commitment, hindsight); 3 ethical criteria | D1 p.98–111 |
| 3 | **Personality & Values** | Big Five (OCEAN), MBTI, Dark Triad, terminal vs instrumental values, Hofstede's dimensions | D1 p.73–97 |
| 4 | **Emotions & Moods** | Emotional labour → **surface vs deep acting → emotional dissonance**, Affective Events Theory, Emotional Intelligence | D1 p.112–136 |
| 5 | **Diversity** | Surface- vs deep-level diversity, biographical characteristics, diversity-management strategies, inclusion | D1 p.54–72 |
| 6 | **Leadership** | Trait → behavioural → contingency (Fiedler), Path-Goal, charismatic, **transformational vs transactional**, full-range model | D2 p.35–53 |
| 7 | **Groups & Teams** | Groups vs teams, **Tuckman: forming/storming/norming/performing/adjourning**, roles/norms/status, social loafing, cohesiveness, group decision techniques (brainstorming, nominal group, Delphi), groupthink | D1 p.187–206 / D2 p.1–33 |
| 8 | **Org Culture & Change** | Strong vs weak culture, socialisation model, **Lewin: unfreeze / change / refreeze**, resistance to change & how to reduce it, action research / OD | D2 p.79–113 |
| 9 | **HRM process** | Job analysis, recruitment process, selection methods & interview problems, **compensation** (philosophy, equity/expectancy applied to pay), **performance appraisal** (rating errors: halo, leniency, central tendency; methods incl. BARS; 360°/720°) | D2 p.114–207 |
| 10 | **Communication** | Functions, direction & networks (chain/wheel/all-channel), the grapevine, barriers (filtering, overload, selective perception) | D2 p.19–33 |
| 11 | **Intro / OB basics / HRM context** | Management functions, Mintzberg's 10 roles, Luthans (successful vs effective managers), Harvard model of HRM | D1 p.1–53 |
| 12 | **Org Structure** | 6 elements, departmentalisation, span of control, centralisation/formalisation, common designs, "structure follows strategy" | D2 p.54–78 |

**Cases you should pre-read and have a position on:**
- `MBA ZG511 Harvard Case study.pptx`
- `MBA ZG511 IIMA Case study.pptx` / `Vasudhas Dismay - IIM A Case study.pdf` — Vasudha Kumar, BV team lead, key colleague resigns 4 days before her maternity leave; "What should she do? What are the options?" (motivation, delegation, succession, retention).
- Plus the mini-case at the end of most lectures (Jack Nelson's Problem, Costs of Being Nice, Crying at Work, Carrot to the Stick, Calamities of Consensus, Tongue-Tied in Teams, Pay Equity Dilemma at TechNova).

**Linkage note:** MPO topics are *combined* in case questions — a single case can need motivation + diversity + leadership + communication at once. The skill is picking the 2–3 frameworks that actually fit the scenario and naming them explicitly.

---

## Q4 — Open-book strategy for a busy person: memorise vs. reference, per subject

### The core principle
Open book punishes people who plan to "look it up." A 3-hour paper that is 70–80% numerical (MA) or 6–7 essay/case answers (MPO) gives you **~15–25 minutes per question**. If you burn 5 of those flipping pages, you fail on time, not knowledge. So:

> **Memorise the *triggers and the logic*. Reference the *detail and the wording*.**

You can lean on the PDF *much* more for MPO (it's theory you can find and paraphrase) than for MA (you cannot look up 15 formulas mid-calculation). Rough split:
- **MA:** ~70% from memory, ~30% from the PDF.
- **MPO:** ~40% from memory (framework skeletons), ~60% from the PDF (explanations, examples, case-answer scaffolding).

### Build your consolidated PDF into a weapon (do this first, ~2 hrs)
1. Print + **bind** the approved PDF for each subject (loose sheets are disallowed anyway). For MA that's `Managerial Accounting/ENCRYPTED FMA NSP S4.pdf`.
2. **Tab the page edges** using **Appendix A** (MA — 9 tabs) and the Q3 table (MPO). Your own handwritten notes/index are not allowed, so use blank sticky flags with just a topic word, or a printed-from-Appendix-A tab strip — check with your instructor whether a typed one-line contents strip is acceptable; the safe version is single-word edge flags.
3. Colour-code the tabs by cluster: MA — yellow = ratios (tabs 3–4), pink = cash flow (5), orange = cost/decisions (6–7), blue = CVP (8), green = variances (9). MPO — one colour per cluster.
4. Target: **any topic findable in under 20 seconds.**

### Managerial Accounting — the memorise list (write these until automatic)
- **CVP block** (all of Tier 1A in Q2) — ~12 formulas. Non-negotiable.
- **6 variance formulas** + the two checks + "SQ/ST on actual output."
- **Decision rules** (sunk/opportunity/fixed; make-or-buy; special order; drop product; limited resource; process further) — as *rules*, not text.
- **CFO indirect adjustments** (+depreciation, ± non-operating, working-capital lock/free signs).
- **~12 ratio formulas** from Tier 2 (the liquidity/profitability/leverage/turnover core + P/E + CCC).
- The **traps list** at the end of Q2.

**Reference from the PDF (don't memorise):** full ratio definitions & the odd ones, IFRS/IAS clause details, FIFO/LIFO/WAC worked mechanics, 12 red flags, budgeting types, cost-classification taxonomy, any format/layout of the P&L.

**Technique in the hall:** for every numerical — (1) write the formula from memory first, (2) label every number with what it *is* (SQ? AQ? opening or closing?), (3) do the "sense check" before arithmetic (actual price < standard → favourable; VC% + PV% = 100), (4) state the interpretation in one line ("MPV is adverse and larger than the favourable MUV, so management should control purchase price"). The interpretation line is where open-book marks are won.

### MPO — the memorise list (skeletons only, ~1 line each)
- **Maslow** 5 levels · **Herzberg** hygiene vs motivators · **Equity** (input/outcome ratio vs referent) · **Expectancy** (Effort→Performance→Reward→Valence) · **Goal-setting** (specific + difficult + accepted + feedback)
- **Big Five** = OCEAN · **MBTI** = 4 dichotomies (E/I, S/N, T/F, J/P) · **Dark Triad** = Machiavellianism, narcissism, psychopathy
- **Attribution theory** = distinctiveness / consensus / consistency; + fundamental attribution error, self-serving bias
- **Decision biases** = overconfidence, anchoring, confirmation, availability, escalation of commitment, hindsight, representativeness
- **Emotional labour** = surface acting vs deep acting → emotional dissonance → burnout
- **Tuckman** = forming / storming / norming / performing / adjourning
- **Lewin** = unfreeze / change / refreeze; **resistance** reduced by: communication, participation, support, negotiation
- **JCM** = skill variety, task identity, task significance, autonomy, feedback
- **Leadership** = trait → behavioural → contingency (Fiedler: LPC + situational favourableness) → Path-Goal → transformational vs transactional
- **EVLN** = exit / voice / loyalty / neglect (responses to dissatisfaction)
- **Hofstede** = power distance, individualism/collectivism, masculinity/femininity, uncertainty avoidance, long-term orientation, indulgence
- **Appraisal errors** = halo, leniency/strictness, central tendency, recency, similarity; **methods** incl. graphic rating scale, checklist, BARS, 360°/720°, MBO
- **Mintzberg** = interpersonal / informational / decisional roles; **Luthans** = successful (networking) vs effective (communication + HRM) managers

**Reference from the PDF (D1/D2 + page):** the *explanation* of each model, the textbook example, the case-specific facts, anything you can't recall in full. You mostly need the *name* memorised so you know *what to look up* and can write while flipping.

**Technique in the hall (from your notes' MPO exam pointers):**
- Structure every answer: **Identify** (name the concept/issue in subject terms) → **Apply** (map the framework to the case facts) → **Recommend / Outcome**.
- Name the concept explicitly: *"This is **surface acting**, because she displays required emotions that don't match felt emotions, creating emotional dissonance…"*
- Use **subject terminology**, be **objective**, **don't storytell** — markers dock "narrative padding."
- For "what are your views" questions, the cap is often **4/5** — give a balanced view, don't over-invest.
- For case questions, pick the **right** framework for the context (e.g. psychological appraisal for a promotion candidate, not a standard appraisal) and **justify the choice** — justification scores more than selection.

### Time budget (busy-person plan)

**Managerial Accounting (do ~60% of your MA time here):**
1. CVP / P–V ratio — drill 10–15 past problems until formula recall is reflexive (L12, L14).
2. Relevant-cost decisions — do one of each type (make-or-buy, special order, drop, limited resource) (L11, L13).
3. Variances — do 5 material + 5 labour + 2 integrated (L15; use `Standard_Costing_Variance_Questions_with_Solutions.docx`).
4. Cash flow indirect — 3 full CFO problems (L16).
5. Ratios — 1 pass through `Financial_Ratio_Analysis_20_Practice_Questions...docx`, then the "advanced/interpretation" set (L9, L10).
6. Skim statements/adjustments + principles (L7, L8, then L1–L4).

**MPO (theory can be crammed later than MA):**
1. Motivation cluster — be able to write all 5 theories cold.
2. Perception / attribution / biases.
3. Personality + emotions.
4. Diversity + the 2 big cases (Harvard, Vasudha) — write a practice answer for each.
5. Leadership + culture/change.
6. HRM (recruitment, compensation, appraisal) + communication.
7. One skim of structure + intro/OB basics.

**Final 48 hours:** MA formula sheet recall test (blank paper, write all of Tier 1) + one timed MA mixed set; MPO framework-skeleton recall test + one timed case answer. Tab and index both PDFs. Confirm calculator model is allowed.

---

## Appendix A — Managerial Accounting open-book PDF: fast page index

**File:** `Managerial Accounting/ENCRYPTED FMA NSP S4.pdf` — 241 pages, "BITS WILP Study Material", watermarked, printing allowed. This is the file you print, bind and carry (see Q1).

**How to use this:** the PDF is ~8 separate lecture decks stapled together, so it has *no single contents page and repeats "Thank You" / title slides between sections*. Put a physical tab on the **first page of each block below**. Page numbers are the **PDF page number** (not the slide number printed on each slide — those restart every deck). Ranges were reconstructed by scanning the file; treat ±2 pages as normal and confirm the exact split when you tab it.

| Tab | Pages | Section | What's actually on those pages |
|---|---|---|---|
| **1. IFRS / IAS** | **1–20** | Accounting standards | IFRS S1/S2 (sustainability, climate), IFRS 5, 7, 8; **IFRS 13 fair-value hierarchy** L1/L2/L3 (p8–10); **IFRS 15 revenue 5-step model** (p11–14); **IAS 16** PP&E (p15–16); **IAS 2 inventories** + IAS 2 vs US GAAP (p17–19); **R&D: IFRS vs US GAAP** (p20) |
| **2. 12 Red Flags** | **21–32** | Financial-statement manipulation | Red flags 2–12: profit without performance, receivables > sales growth, inventory build-up, earnings–cash-flow gap, complex financing/SPEs, big write-offs, Q4 adjustments, auditor concerns, related-party, off-balance-sheet (p22–32) |
| **3. Ratio Analysis (A)** | **33–66** | Fundamental / ratio analysis (Uma Nagarajan deck) | Fundamental analysis = economic + industry + company/ratio (p35); **liquidity — current / quick / absolute liquid** (p37–42); profitability, solvency/leverage, turnover/activity ratios through p65 |
| **4. Ratio Analysis (B) + Valuation** | **67–93** | Ratios continued (Ankita Nagpal deck) | **Gross Profit ratio** and margin ratios (p75); **EV/Sales, P/E, valuation ratios** (p85); DuPont / industry-benchmarking angle |
| **5. Cash Flow Statement** | **94–119** | Cash flow (indirect & direct) | Theory: operating / investing / financing, direct vs indirect (p95–103); **"classify the transaction" drill** — operating/investing/financing/non-cash/cash-management (p110); **indirect-method worked problems** e.g. Gopal Dairy (p115+) |
| **6. Cost Concepts + Costing + Inventory + Budgeting** | **120–160** | Cost & management accounting | FA vs Cost/Mgmt Acctg vs Financial Mgmt (p122); **relevant / sunk / opportunity cost** (p125, 145–150); **categories of cost — prime cost, overheads** (p130); marginal cost (p139); **semi-fixed / semi-variable cost** graph (p140); **inventory valuation FIFO / LIFO / WAC** (p151–154); **budgeting — cash budget, master budget, ZBB** (p155–160) |
| **7. Decision-Making / Relevant Costing** | **161–200** | Short-run decisions | **relevant costs** (airline-meals example p170); **make-or-buy / vertical integration** (p180); **resource-utilisation decisions** — contribution per unit of limited resource (p190); **theory of constraints / bottleneck** (p196); special-order framing |
| **8. CVP / Marginal Costing** | **201–236** | Cost-Volume-Profit (Uma Nagarajan deck) | **CVP identity: Sales = Profit + FC + VC → Contribution = S − VC = FC + P** (p205); **break-even** (p210–213); **margin of safety** (p214–215); **make or buy** (p219–222); **special order** (p223); **"CVP ANALYSIS" fully worked problems** — BEP, P/V ratio, MoS, Fastride Cycle make-or-buy, foreign-vs-local special order (p225–236) |
| **9. Standard Costing & Variances** | **237–241** | Variance analysis | Definition of standard cost (p238); **MCV = SQ·SP − AQ·AP** (p239); **MPV = AQ(SP−AP), MUV = SP(SQ−AQ), check MPV+MUV=MCV** (p240); **LCV = ST·SR − AT·AR, LRV = AT(SR−AR), LEV = SR(ST−AT), check LRV+LEV=LCV** (p241). *Formulas only — no worked examples in the deck; practise from the variance question bank beforehand.* |

**Notes / gotchas when tabbing:**
- Some content slides are **images with instructor handwriting** (red pen) over them — the working shown in that ink is often the exam-relevant bit (e.g. the P/V ratio = C/S = 60/100 = 60% derivation on the Margin of Safety slide ~p215). Don't skip annotated slides.
- **Standard costing is only 5 pages** and has no solved examples — that topic is where you most need the formulas *memorised* (Q2 Tier 1B), the PDF barely helps mid-exam.
- The deck has **little on journal/ledger/trial-balance** and that's fine — `Notes/05` says statement *preparation* is not the exam focus.
- Cross-check: the `Classmates/All Sub Index...pdf` (Financial & Management Accounting pages) is a topic→page index to **this same file** if you want a second, finer-grained map while revising — but it can't go into the hall.

### What a past EC3 paper looked like (from `Managerial Accounting/shared/2025-2026_SEM_1_...MANAGERIAL_ACCOUNTING_EC3_...INSTR.docx`)
Open book, **2½ hours, 40% weightage, 3 questions**:
1. **[20 marks] Industry identification** — match 10 companies' financial data / ratios / DuPont pattern to their industry (cement, oil & gas, banking, IT, pharma, two-wheeler auto, hospitality, retail food, telecom, heavy engineering). *This is the ratio-analysis + industry-benchmarking block — Tabs 3–4 above, and the "industry → typical ratio profile" logic from `Notes/09`.*
2. **[10 marks] CVP** — given two years of sales & profit, find fixed cost, BEP (₹ and units), and sales for a target profit. *Tab 8; Q2 Tier 1A.*
3. **[10 marks] Theory** — concept, tools & techniques of managerial accounting and how it improves business performance. *Tab 6 intro; `Notes/11`.*

Don't assume your paper is identical, but the shape — one big ratio/industry question + one CVP question + one short theory question — is a strong signal for where to put your prep hours.

---

_Sources: `memory/exam_rules_open_book.md`; `Managerial Accounting/Notes/01–16`; `Managerial Accounting/Practice-Questions.md`; `Managerial Accounting/shared/` question banks; `Managing People and Organization/Notes/24` and others; `Managing People and Organization/Practice-Questions.md`; `Managing People and Organization/shared/Sample paper - MidSem.docx`; `Classmates/All Sub Index for Open Book Exam BITS-EC3.pdf` (Financial & Management Accounting and MPO sections); `Managerial Accounting/ENCRYPTED FMA NSP S4.pdf` (metadata + page-by-page scan, for Appendix A); `Managerial Accounting/shared/2025-2026_SEM_1_...MANAGERIAL_ACCOUNTING_EC3_...INSTR.docx` (past EC3 paper)._
