---
name: exam-solver
description: Extract questions from exam PDFs (A Level, IB, AP, etc.) and produce detailed Chinese solutions with step-by-step reasoning, automatic proofreading, and question-answer paired markdown output. Use this skill whenever the user uploads a PDF exam paper, pastes exam questions, or asks to solve/answer exam questions — even if they don't explicitly mention "exam" or "PDF". Trigger on phrases like "帮我做这套试卷", "写一下这个PDF的答案", "解这些题", "做答案", "solve this paper", "answer these questions", or any request involving exam papers, test papers, past papers, or practice papers from A Level, IB, AP, GCSE, or similar international exam boards. Also trigger when the user uploads any document that looks like an exam and asks for answers, solutions, or explanations.
---

# Exam Paper Solver

## Skill Overview

This skill handles the complete workflow of extracting questions from exam PDFs and producing detailed, step-by-step **Chinese-language solutions**. It covers three phases: **extraction → solving → proofreading**.

## Phase 1: PDF Content Extraction & Structuring

**FIRST ACTION — before anything else:** Use TodoWrite to create the following tasks. You MUST mark each one complete as you finish it. Do not claim the work is done until every todo is checked off.

```
TodoWrite([
  { id: "meta",      content: "Extract metadata: exam name, subject, level for filename",                    status: "in_progress" },
  { id: "extract",   content: "Extract ALL questions — verify none are skipped",                             status: "pending" },
  { id: "solve",     content: "Every question has a complete solution",                                      status: "pending" },
  { id: "approach",  content: "Every solution has an approach section (解题思路)",                           status: "pending" },
  { id: "kpoints",   content: "Every solution lists knowledge points (涉及知识点) with full explanations",  status: "pending" },
  { id: "formulas",  content: "Every solution lists formulas (涉及公式) in proper LaTeX",                   status: "pending" },
  { id: "reasoning", content: "Every solution shows full reasoning, not just the answer",                    status: "pending" },
  { id: "bilingual", content: "Technical terms use bilingual format (Chinese + English in parentheses)",     status: "pending" },
  { id: "units",     content: "Physics/Chemistry answers include correct units",                             status: "pending" },
  { id: "verify",    content: "All subagent results verified; retries applied where needed",                 status: "pending" },
  { id: "proofread", content: "Proofreading agent (category=deep) has run and corrections applied",         status: "pending" },
  { id: "order",     content: "Question solutions are assembled in correct numerical order",                 status: "pending" },
  { id: "filepath",  content: "Output path resolved correctly; file written to disk (NOT chat)",             status: "pending" },
])
```

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

⚠️ **CRITICAL: Do NOT load `exam-solver` skill for subagents** — it would trigger infinite recursion. Load `exam-solver-worker` instead, which contains only the solving rules.

```typescript
// Replace [N] with the actual question number (e.g., 1, 2, 3...)
task(
  category="deep",
  load_skills=["exam-solver-worker"],
  run_in_background=true,
  description="Solve Question [N]",
  prompt=`按照 exam-solver-worker skill 的规范，解答第 [N] 题。

⚠️ CRITICAL: 你是委托执行者。不要再次委派任务。不要使用 write 工具。直接在回复中返回解答内容。

CONTEXT:
[Paste the extracted question text for Question [N] here]`
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

After launching all background tasks, you MUST **immediately stop generating output**. Write nothing further — no summaries, no "I've launched X tasks", no closing remarks. Your response ends the moment the last `task(run_in_background=true)` call is made.

**You will be notified automatically** via `<system-reminder>` when each task completes. Only after receiving notifications for ALL tasks should you proceed to collect results. Do NOT call `background_output` on a task that has not yet sent a completion notification — it will block or return empty results.

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

```markdown
# [考试名称 / 科目] 完整解答

> 考试委员会：[A Level / IB / AP / GCSE / 等]
> 科目：[数学 / 物理 / 化学 / 等]
> 解答语言：中文（专业术语保留英文）

---

[Question 1 solution from subagent]

[Question 2 solution from subagent]

[Question 3 solution from subagent]
```

**Output path decision:**
- **User specified a full file path** → Write directly to that path (using the `write` tool).
- **User specified a directory** → Write into that directory using the default filename.
- **User did not specify** → Use the default naming rule: `[ExamName]_[Subject]_Solutions.md`, write to the current working directory.
- **Metadata missing fallback** → `Solutions_YYYY-MM-DD.md`

**Writing rules:**
- Use the `write` tool to create the file
- In the chat, only confirm: "✅ 已生成解答：`[filepath]`，共 [N] 题，包含完整解题步骤和校对报告。"
- If the file is very large, still write it to disk — never split output across chat messages

> Solving format rules (language, structure, per-type templates, step requirements) are defined in `exam-solver-worker`. Subagents load that skill directly.

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
4. **Knowledge points (涉及知识点):** Are the relevant knowledge points listed for each question? Are they accurate and complete? **Each knowledge point must be explained in detail — definition, principle, applicable conditions, and key takeaways. A bare name like "牛顿第二定律" with no explanation is NOT acceptable.**
5. **Formulas (涉及公式):** Are all formulas used in the solution listed with proper LaTeX notation? Are they correctly stated?
6. **Language quality:** Is the **entire solution written in Chinese** (except technical terms and formulas which may remain in English)? Are any sections accidentally written in English prose? Are technical terms accurately translated into Chinese? Is the prose natural and fluent?
7. **Format compliance:** Does every question follow the required structure (approach → knowledge points → formulas → solution → final answer)? Are all LaTeX formulas properly closed?

For each question, list any issues found along with the corrected content. If a question has no issues, mark it as '✅ No issues'.

Here are the solutions to proofread:
[Paste the full solution document here]"
)
```

After receiving the proofreading results:
1. Apply all corrections directly to the relevant question sections in the file (use the `edit` tool).
2. **Append** the proofreading report to the end of the file using the `edit` tool — add the following block after the last question:

```markdown

---

## 校对报告

[逐题列出发现的问题及修正内容。无问题的题目标注"✅ 无问题"。]
```

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
    Spawn subagents for each question (load_skills=["exam-solver-worker"], return content, NOT write)
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
