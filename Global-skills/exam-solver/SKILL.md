---
name: exam-solver
description: Extract questions from exam PDFs (A Level, IB, AP, etc.) and produce detailed Chinese solutions with step-by-step reasoning, automatic proofreading, and question-answer paired markdown output. Use this skill whenever the user uploads a PDF exam paper, pastes exam questions, or asks to solve/answer exam questions — even if they don't explicitly mention "exam" or "PDF". Trigger on phrases like "帮我做这套试卷", "写一下这个PDF的答案", "解这些题", "做答案", "solve this paper", "answer these questions", or any request involving exam papers, test papers, past papers, or practice papers from A Level, IB, AP, GCSE, or similar international exam boards. Also trigger when the user uploads any document that looks like an exam and asks for answers, solutions, or explanations.
---

# Exam Paper Solver

## Skill Overview

This skill handles the complete workflow of extracting questions from exam PDFs and producing detailed, step-by-step **Chinese-language solutions**. It covers three phases: **extraction → solving → proofreading**.

## Phase 1: PDF Content Extraction & Structuring

Start by extracting the exam content. The `pdf` skill handles text extraction and OCR for scanned documents — use it as your primary tool.

**What to capture for each question:**
- Full question text (or a key summary if extremely long)
- Question number and all sub-parts (a, b, c… / i, ii, iii…)
- Marks or points allocation if shown
- Diagrams, graphs, tables — describe them in text so the solution can reference them
- Any given data, constants, or formulas provided in the question

**Extract metadata for filename:**
- **Exam name / paper** (e.g., A Level Mathematics Paper 1, IB Physics HL Paper 2)
- **Subject** (e.g., Mathematics, Physics, Chemistry)
- **Exam level** (A Level / IB / AP / GCSE)

These will be used for the output filename: `[ExamName]_[Subject]_Solutions.md`.

**Why this matters:** Missing a sub-question or misreading a diagram value will cascade into wrong answers. Verify completeness before moving to Phase 2.

**Single-question vs multi-question decision:**
- **≤ 2 questions total** → Solve directly in the main session — no delegation needed.
- **> 2 questions** → Proceed with parallel delegation (Phase 2).

## Phase 2: Question-by-Question Solutions

Solve **every question** on the paper. The core principle: show the reader *how* to think through the problem, not just what the answer is.

### ⚠️ CRITICAL: Parallel Execution with Ordered Assembly

**The Problem:** When spawning multiple subagents in parallel, they complete at different times. If each writes directly to the output file, the final document will have questions in random order.

**The Solution:** Subagents return content, main process assembles in order.

### Step 1: Spawn Parallel Subagents (Return Content, NOT Write File)

Spawn one subagent per question. **Instruct subagents to RETURN their solution content, NOT write to file.**

⚠️ **CRITICAL: Do NOT load `exam-solver` skill for subagents.** The subagent would read this same skill file and attempt to re-delegate, causing infinite recursion. Instead, inject the solving rules directly in the prompt below.

```typescript
// Replace [N] with the actual question number (e.g., 1, 2, 3...)
task(
  category="deep",
  load_skills=[],
  run_in_background=true,
  description="Solve Question [N]",
  prompt=`TASK: Solve Question [N] from the exam paper. Write a detailed Chinese solution with step-by-step reasoning.

EXPECTED OUTCOME: Return the complete markdown-formatted solution block for Question [N] as your final message. DO NOT write to any file — just return the content.

⚠️ CRITICAL: You are a delegated executor. Do NOT re-delegate this task. Do NOT use the write tool. Return the solution content directly in your response.

MUST DO:
- **Include a "解题思路" section** before the detailed solution: explain the overall approach, what the question is testing, and the key insight needed.
- **List "涉及知识点"**: enumerate the knowledge points, concepts, and theorems this question tests.
- **List "涉及公式"**: write out every formula used, with LaTeX notation, and briefly state when/why each is applied.
- Show full working: state approach, show calculations, explain reasoning, box final answer.
- Use Chinese with English technical terms: 导数 (Derivative), 链式法则 (Chain Rule).
- Use LaTeX for math: $E = mc^2$ or $$\int_0^1 x^2 \, dx$$.
- Include units for Physics/Chemistry. Match 3 significant figures if unspecified.
- Format your output exactly like this:

## Question [N] ([X] marks)

**Question:** [Original question text or key summary]

### 解题思路

[Overall approach: what this question is testing, the key insight, and the general strategy to solve it]

### 涉及知识点

- [Knowledge point 1]
- [Knowledge point 2]
- ...

### 涉及公式

- [Formula 1 in LaTeX]: [Brief explanation of when/why to use it]
- [Formula 2 in LaTeX]: [Brief explanation of when/why to use it]
- ...

### Solution

[Your detailed step-by-step solution]

**Final Answer:** $\boxed{answer}$

---

MUST NOT DO:
- Do NOT use the write tool — return content only.
- Do NOT re-delegate this task to other agents.
- Do NOT skip any sub-question (a, b, c / i, ii, iii).
- Do NOT output only the final answer — show full working.

CONTEXT: [Paste the extracted question text for Question [N] here]`
)
```

**Track each task_id with its question number:**
```
Q1 → task_id: "task_abc123"
Q2 → task_id: "task_def456"
Q3 → task_id: "task_ghi789"
...
```

### Step 2: Collect Results and Assemble in Order

After launching all subagents in the background, **end your response and wait for the system `<system-reminder>` notification** for each task completion. Do NOT poll `background_output` on running tasks.

Once all tasks are complete, collect results **in question order** (NOT by completion time):

```typescript
// Collect in order, NOT by completion time
background_output(task_id="task_abc123")  // Q1
background_output(task_id="task_def456")  // Q2
background_output(task_id="task_ghi789")  // Q3
```

**Error handling for subagent results:**
- If a subagent returns empty or truncated content → **retry** with the same `session_id` and prompt: `"Your previous output was incomplete. Please regenerate the complete solution for this question."`
- If a subagent fails or errors → **retry** with `session_id` and prompt: `"The previous task failed. Please regenerate the solution for this question."`
- If retry also fails → solve that question in the main session using the extracted question text from Phase 1.
- Always verify each question result contains the expected `## Question [N]` header before proceeding to assembly.

### Step 3: Write Final Document (Main Process Only)

Only the main process writes the final file, combining:

1. **Header** (title, metadata)
2. **Question solutions** (in numerical order 1, 2, 3...)
3. **Proofreading Report** (after Phase 3)

```markdown
# [Exam Name / Subject] — Complete Solutions

> Exam Board: [A Level / IB / AP / GCSE / etc.]
> Subject: [Mathematics / Physics / Chemistry / etc.]
> Solution Language: Chinese (with English technical terms)

---

[Question 1 solution from subagent]

[Question 2 solution from subagent]

[Question 3 solution from subagent]

---

## Proofreading Report

[Results from Phase 3]
```

**Output path decision:**
- **User specified a full file path** → Write directly to that path (using the `write` tool).
- **User specified a directory** → Write into that directory using the default filename.
- **User did not specify** → Use the default naming rule: `[ExamName]_[Subject]_Solutions.md`, write to the current working directory.
- **Metadata missing fallback** → `Solutions_YYYY-MM-DD.md`

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
### 解题思路

[Overall approach: what this question is testing, the key insight, and the general strategy]

### 涉及知识点

- [Knowledge point 1]
- [Knowledge point 2]

### 涉及公式

- $[formula_1]$: [When/why to use]
- $[formula_2]$: [When/why to use]

### Solution

**Step 1:** [Brief statement of what this step accomplishes]
[Detailed calculation or derivation]
*Note: This applies [formula/theorem name] because [reason/condition].*

**Step 2:** [Continue...]
...

**Final Answer:** $\boxed{answer}$
```

**Proof:**

```markdown
### 解题思路

[Proof approach: e.g., "Use mathematical induction" or "Proof by contradiction", and why this method is chosen]

### 涉及知识点

- [Knowledge point 1]
- [Knowledge point 2]

### 涉及公式

- $[formula_1]$: [When/why to use]

### Proof

- Given: [List known conditions]
- To prove: [State the conclusion to be proven]
- Proof: [Step-by-step derivation, each step labeled with its justification]

$\blacksquare$ Q.E.D.
```

**Multiple Choice:**

```markdown
### 解题思路

[What concept this question tests, and the elimination strategy]

### 涉及知识点

- [Knowledge point 1]

### 涉及公式

- $[formula]$: [If applicable]

### Analysis

- Option A: [Why it is correct or incorrect]
- Option B: [Why it is correct or incorrect]
- Option C: [Why it is correct or incorrect]
- Option D: [Why it is correct or incorrect]

**Final Answer:** $\boxed{\text{X}}$, because [core reason]
```

**Graph / Diagram:**

```markdown
### 解题思路

[What the diagram is showing, what data needs to be extracted, and the overall approach]

### 涉及知识点

- [Knowledge point 1]
- [Knowledge point 2]

### 涉及公式

- $[formula_1]$: [When/why to use]

### Diagram Analysis

[Describe key data points, trends, intersections read from the visual]

### Solution

[Derivation incorporating the diagram data]

**Final Answer:** $\boxed{answer}$
```

### Answering Guidelines

- **Match the exam level:** A Level solutions should be noticeably deeper than GCSE; IB HL deeper than SL. Judge the level from the paper title or question complexity.
- **Include units for Physics/Chemistry:** Numerical answers must carry correct units (e.g., $\text{m s}^{-2}$, $\text{mol dm}^{-3}$).
- **Significant figures:** Follow the question's stated precision; if unspecified, default to 3 significant figures.
- **Alternative methods:** If a question has a clearly different second approach, briefly note it after the main solution to broaden the student's perspective.

## Phase 3: Automated Proofreading

After completing all solutions, run a proofreading pass via a delegated agent. This catches calculation errors, missing steps, and formatting issues before delivery.

Delegate the proofreading task as follows (use `deep` category for thorough analytical checking):

```
task(
  category="deep",
  load_skills=[],
  run_in_background=false,
  prompt="Act as an exam marker and proofread the following exam solutions. Check each question:

1. **Answer correctness:** Re-calculate key steps and verify the final answer is correct. Pay special attention to sign errors, unit conversions, and significant figures.
2. **Step completeness:** Are there any skipped steps? Could a student reproduce the answer from these steps alone?
3. **Approach section (解题思路):** Does every question have a clear approach section explaining the strategy and key insight?
4. **Knowledge points (涉及知识点):** Are the relevant knowledge points listed for each question? Are they accurate and complete?
5. **Formulas (涉及公式):** Are all formulas used in the solution listed with proper LaTeX notation? Are they correctly stated?
6. **Language quality:** Are technical terms accurately translated into Chinese? Is the prose natural and fluent?
7. **Format compliance:** Does every question follow the required structure (approach → knowledge points → formulas → solution → final answer)? Are all LaTeX formulas properly closed?

For each question, list any issues found along with the corrected content. If a question has no issues, mark it as '✅ No issues'.

Here are the solutions to proofread:
[Paste the full solution document here]"
)
```

After receiving the proofreading results, apply all corrections to the final output file. Include a brief summary of what was fixed (or confirm that no issues were found) in the "Proofreading Report" section at the end of the file.

## Output Format — File Only, Never Chat

**CRITICAL: Write the complete solution to a `.md` file. Do NOT output the solution content to the chat window.**

**Output path resolution (in priority order):**
1. **User specified a full file path** (e.g., `./solutions/math_paper1_solutions.md`) → Write directly to that path.
2. **User specified a directory** (e.g., `./solutions/`) → Write into that directory with the default filename.
3. **User did not specify** → Use the default naming rule `[ExamName]_[Subject]_Solutions.md`, write to the current working directory.
4. **Metadata missing fallback** → `Solutions_YYYY-MM-DD.md`

- Use the `write` tool to create the file
- In the chat, only confirm: "✅ Generated solutions: `[filepath]`, [N] questions, complete step-by-step solutions with proofreading report."
- If the file is very large, still write it to disk — never split output across chat messages

## Workflow Summary

```
Phase 1: Extract & Structure
    ↓
    Extract metadata (exam name, subject, level) for filename
    ↓
    ≤ 2 questions? → Single session → Solve directly → skip to Phase 3
    ↓
    > 2 questions? → Number questions (1, 2, 3...)
    ↓
Phase 2: Solve Questions (Parallel)
    ↓
    Spawn subagents for each question (load_skills=[], return content, NOT write)
    ↓
    End response → wait for system <system-reminder> notifications
    ↓
    Collect results in order: background_output(task_id_1), background_output(task_id_2), ...
    ↓
    Verify each question result → retry with session_id if incomplete/failed
    ↓
    Assemble in order: Q1 → Q2 → Q3 → ...
    ↓
    Write complete file (main process only) — use user-specified path if provided, else default naming
    ↓
Phase 3: Proofread (category="deep", synchronous)
    ↓
    Apply corrections to file
    ↓
    Done!
```

## Quality Checklist

Before delivering the final answer, confirm each item:

- [ ] **Metadata extracted**: exam name, subject, and level captured for filename
- [ ] **Every question** on the paper has a solution — none skipped
- [ ] Each solution includes an **approach section** (解题思路) with strategy and key insight
- [ ] Each solution lists **knowledge points** (涉及知识点)
- [ ] Each solution lists **formulas used** (涉及公式) in proper LaTeX
- [ ] Each solution shows the **full reasoning process**, not just the answer
- [ ] Technical terms use the **bilingual format** (Chinese with English in parentheses)
- [ ] Physics/Chemistry answers include **correct units**
- [ ] **Subagent results verified**: each question has complete content, retries applied if needed
- [ ] The **proofreading agent** (category=deep) has run and its corrections have been applied
- [ ] The output follows the **template structure** above
- [ ] The complete solution is written to a **`.md` file** — NOT output to the chat window
- [ ] **Question solutions are in correct order** — subagents returned content, main process assembled in order
- [ ] **Output path correct** — user-specified path used if provided, else default naming applied
