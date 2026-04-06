---
name: exam-solver
description: Extract questions from exam PDFs (A Level, IB, AP, etc.) and produce detailed Chinese solutions with step-by-step reasoning, automatic proofreading, and question-answer paired markdown output. Use this skill whenever the user uploads a PDF exam paper, pastes exam questions, or asks to solve/answer exam questions — even if they don't explicitly mention "exam" or "PDF". Trigger on phrases like "帮我做这套试卷", "写一下这个PDF的答案", "解这些题", "做答案", "solve this paper", "answer these questions", or any request involving exam papers, test papers, past papers, or practice papers from A Level, IB, AP, GCSE, or similar international exam boards. Also trigger when the user uploads any document that looks like an exam and asks for answers, solutions, or explanations.
---

# Exam Paper Solver

## Skill Overview

This skill handles the complete workflow of extracting questions from exam PDFs and producing detailed, step-by-step **Chinese-language solutions**. It covers three phases: **extraction → solving → proofreading**.

## Phase 1: PDF Content Extraction

Start by extracting the exam content. The `pdf` skill handles text extraction and OCR for scanned documents — use it as your primary tool.

**What to capture for each question:**
- Full question text (or a key summary if extremely long)
- Question number and all sub-parts (a, b, c… / i, ii, iii…)
- Marks or points allocation if shown
- Diagrams, graphs, tables — describe them in text so the solution can reference them
- Any given data, constants, or formulas provided in the question

**Why this matters:** Missing a sub-question or misreading a diagram value will cascade into wrong answers. Verify completeness before moving to Phase 2.

## Phase 2: Question-by-Question Solutions

Solve **every question** on the paper. The core principle: show the reader *how* to think through the problem, not just what the answer is.

### Subagent Delegation (MANDATORY for multi-question papers)

**Do NOT solve all questions sequentially in the main session.** Instead, delegate one subagent per question:

1. **Spawn parallel subagents** — one per question — using `task()`:

```typescript
task(
  category="deep",
  load_skills=["exam-solver"],
  run_in_background=true,
  description="Solve Q1",
  prompt=`TASK: Solve Question 1 from the exam paper. Write a detailed Chinese solution with step-by-step reasoning.
EXPECTED OUTCOME: A markdown-formatted solution block for Question 1, following the template in the exam-solver skill.
REQUIRED TOOLS: write (to write the solution to the output file).
MUST DO:
- Show full working: state approach, show calculations, explain reasoning, box final answer.
- Use Chinese with English technical terms: 导数 (Derivative), 链式法则 (Chain Rule).
- Use LaTeX for math: $E = mc^2$ or $$\int_0^1 x^2 dx$$.
- Include units for Physics/Chemistry. Match 3 significant figures if unspecified.
- Write the solution to the output file at: ${outputFilePath}
MUST NOT DO:
- Do NOT skip any sub-question (a, b, c / i, ii, iii).
- Do NOT output to chat — write only to the file.
CONTEXT: [Paste the extracted question text for Q1 here]`
)
```

2. **Collect all subagent results** and verify every question is written to the file
3. **Run proofreading** (Phase 3) only after ALL subagent solutions are complete

**Single-question papers:** Solve directly in the main session — no delegation needed.

### Language Requirements

Write all solution content in **Chinese** with English technical terms preserved alongside using the format `中文术语 (English Term)`.

- Examples: 导数 (Derivative), 链式法则 (Chain Rule), 定义域 (Domain)
- Mathematical formulas use standard LaTeX: `$E = mc^2$` or `$$\int_0^1 x^2 \, dx$$`

This bilingual approach helps students studying in English-medium programs who think in Chinese — they can map concepts back to their exam vocabulary.

### Solution Depth

Each solution should read like a tutor walking a student through the problem:

1. **State the approach** before executing it
2. **Show the work** — calculations, algebraic manipulations, logical deductions
3. **Explain the reasoning** — cite the theorem, formula, or principle being applied
4. **Highlight the final answer** clearly so it is easy to locate

A student should be able to read the solution and understand not just *what* the answer is, but *how* to arrive at it independently next time.

### Strategies by Question Type

**Calculation / Derivation** (Math, Physics, Chemistry computations):

```markdown
**Step 1:** [Brief statement of what this step accomplishes]
[Detailed calculation or derivation]
*Note: This applies [formula/theorem name] because [reason/condition].*

**Step 2:** [Continue...]
...

**Final Answer:** $\boxed{answer}$
```

**Proof:**

```markdown
**Proof Strategy:** [One-sentence summary, e.g., "Use mathematical induction" or "Proof by contradiction"]

**Proof:**
- Given: [List known conditions]
- To prove: [State the conclusion to be proven]
- Proof: [Step-by-step derivation, each step labeled with its justification]

$\blacksquare$ Q.E.D.
```

**Multiple Choice:**

```markdown
**Analysis:**
- Option A: [Why it is correct or incorrect]
- Option B: [Why it is correct or incorrect]
- Option C: [Why it is correct or incorrect]
- Option D: [Why it is correct or incorrect]

**Final Answer:** $\boxed{\text{X}}$, because [core reason]
```

**Graph / Diagram:**

```markdown
**Diagram Analysis:** [Describe key data points, trends, intersections read from the visual]

**Solution:** [Derivation incorporating the diagram data]

**Final Answer:** $\boxed{answer}$
```

### Answering Guidelines

- **Match the exam level:** A Level solutions should be noticeably deeper than GCSE; IB HL deeper than SL. Judge the level from the paper title or question complexity.
- **Include units for Physics/Chemistry:** Numerical answers must carry correct units (e.g., $\text{m s}^{-2}$, $\text{mol dm}^{-3}$).
- **Significant figures:** Follow the question's stated precision; if unspecified, default to 3 significant figures.
- **Alternative methods:** If a question has a clearly different second approach, briefly note it after the main solution to broaden the student's perspective.

## Phase 3: Automated Proofreading

After completing all solutions, run a proofreading pass via a delegated agent. This catches calculation errors, missing steps, and formatting issues before delivery.

Delegate the proofreading task as follows:

```
task(
  category="unspecified-high",
  load_skills=[],
  run_in_background=false,
  prompt="Act as an exam marker and proofread the following exam solutions. Check each question:

1. **Answer correctness:** Re-calculate key steps and verify the final answer is correct. Pay special attention to sign errors, unit conversions, and significant figures.
2. **Step completeness:** Are there any skipped steps? Could a student reproduce the answer from these steps alone?
3. **Language quality:** Are technical terms accurately translated into Chinese? Is the prose natural and fluent?
4. **Format compliance:** Does every question follow the 'Question → Solution → Final Answer' structure? Are all LaTeX formulas properly closed?

For each question, list any issues found along with the corrected content. If a question has no issues, mark it as '✅ No issues'.

Here are the solutions to proofread:
[Paste the full solution document here]"
)
```

After receiving the proofreading results, apply all corrections to the final output file. Include a brief summary of what was fixed (or confirm that no issues were found) in the "Proofreading Report" section at the end of the file.

## Output Format — File Only, Never Chat

**CRITICAL: Write the complete solution to a `.md` file. Do NOT output the solution content to the chat window.**

- Filename convention: `[ExamName]_[Subject]_Solutions.md` (e.g., `A-Level_Math_Paper1_Solutions.md`)
- Use the `write` tool to create the file
- In the chat, only confirm: "✅ 已生成文件：`[filename].md`，共 [N] 题，包含完整解题过程与校对报告。"
- If the file is very large, still write it to disk — never split output across chat messages

Use the following Markdown structure inside the file:

```markdown
# [Exam Name / Subject] — Complete Solutions

> Exam Board: [A Level / IB / AP / GCSE / etc.]
> Subject: [Mathematics / Physics / Chemistry / etc.]
> Solution Language: Chinese (with English technical terms)

---

## Question 1 ([X] marks)

**Question:** [Original question text or key summary]

### Solution

[Detailed Chinese solution with step-by-step reasoning and formulas]

**Final Answer:** $\boxed{answer}$

---

## Question 2 ([X] marks)

... (repeat the above structure for every question on the paper)

---

## Proofreading Report

[Results from the proofreading agent: each question marked ✅ No issues or with listed corrections]
```

## Quality Checklist

Before delivering the final answer, confirm each item:

- [ ] **Every question** on the paper has a solution — none skipped
- [ ] Each solution shows the **full reasoning process**, not just the answer
- [ ] Technical terms use the **bilingual format** (Chinese with English in parentheses)
- [ ] Physics/Chemistry answers include **correct units**
- [ ] The **proofreading agent** has run and its corrections have been applied
- [ ] The output follows the **template structure** above
- [ ] The complete solution is written to a **`.md` file** — NOT output to the chat window
- [ ] For multi-question papers, **subagents were used** to solve questions in parallel
