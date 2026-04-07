---
name: lecture-script-generator
description: Generate a verbatim lecture teaching script (讲课稿) from A Level courseware PDFs. Use this skill whenever the user uploads a PDF of lecture slides/courseware and asks to generate a teaching script, lecture notes, 讲课稿, 讲稿, 教案, 课件讲稿, or anything about turning slides into something a teacher can read aloud while teaching. Also trigger when the user says "帮我写讲课稿", "把这个课件变成讲稿", "生成讲课稿", "做一份讲课用的稿子", "write a lecture script from these slides", or any request involving converting courseware/slides into a spoken teaching script. Works with A Level, IB, AP, GCSE, or any subject courseware PDFs. Make sure to use this skill whenever the user mentions 讲课稿, 讲稿, 教案, lecture script, teaching script, or wants to turn courseware into something they can teach from.
---

# Lecture Script Generator

## Skill Overview

This skill handles the complete workflow of extracting content from A Level courseware PDFs and producing a **verbatim lecture teaching script (逐字稿)** that a teacher can read aloud while delivering a lesson. It covers three phases: **extraction → script generation → proofreading**.

The output includes natural spoken explanations and bilingual technical terms — all structured by the original slide/chapter order.

## Phase 1: PDF Content Extraction & Structuring

Start by extracting the courseware content. The `pdf` skill handles text extraction and OCR for scanned documents — use it as your primary tool.

**What to capture for each section/slide:**

- Slide number or section title
- All key concepts, definitions, formulas, and examples listed on the slide
- Diagrams, graphs, tables — describe them in text so the script can reference them naturally
- Any worked examples, practice problems, or case studies embedded in the slides
- The logical flow: how one slide connects to the next

**Extract metadata for filename:**
- **Course name / subject** (e.g., Mathematics, Physics, Chemistry)
- **Topic** (e.g., Calculus, Mechanics, Organic Chemistry)
- **Exam level** (A Level / IB / AP / GCSE)

These will be used for the output filename: `[CourseName]_[Topic]_讲课稿.md`.

**Structuring the content:**

Group slides into **teaching units** that cover one coherent subtopic. Each teaching unit will become one section of the lecture script.

**Why this matters:** The script needs to know not just what's on each slide, but how the material flows from one idea to the next. Missing a transition or misreading a diagram will result in an awkward teaching script.

**Assign each teaching unit a sequential number (1, 2, 3...) for ordered assembly later.**

**Single-unit vs multi-unit decision:**
- **≤ 5 slides total** → Treat as a single teaching unit. Generate directly in the main session — no delegation needed.
- **> 5 slides** → Group into multiple teaching units and proceed with parallel delegation (Phase 2).

## Phase 2: Verbatim Script Generation

Generate a **逐字稿 (verbatim script)** for every teaching unit. The core principle: write exactly what the teacher would *say* out loud — natural, conversational, pedagogically sound — not a textbook summary.

### ⚠️ CRITICAL: Parallel Execution with Ordered Assembly

**The Problem:** When spawning multiple subagents in parallel, they complete at different times. If each writes directly to the output file, the final document will have units in random order.

**The Solution:** Subagents return content, main process assembles in order.

### Step 1: Spawn Parallel Subagents (Return Content, NOT Write File)

Spawn one subagent per teaching unit. **Instruct subagents to RETURN their script content, NOT write to file.**

⚠️ **CRITICAL: Do NOT load `lecture-script-generator` skill for subagents.** The subagent would read this same skill file and attempt to re-delegate, causing infinite recursion. Instead, inject the generation rules directly in the prompt below.

```typescript
task(
  category="deep",
  load_skills=[],
  run_in_background=true,
  description="Generate script for Unit N",
  prompt=`TASK: Generate a verbatim lecture teaching script (逐字稿) for Teaching Unit [N] from the A Level courseware.

EXPECTED OUTCOME: Return the complete markdown-formatted script block for this teaching unit as your final message. DO NOT write to any file — just return the content.

⚠️ CRITICAL: You are a delegated executor. Do NOT re-delegate this task. Do NOT use the write tool. Return the script content directly in your response.

MUST DO:
- Write in natural spoken Chinese — the teacher should be able to read this aloud directly. Use conversational phrasing like "我们接下来看", "注意这个细节".
- Preserve English technical terms alongside Chinese: 导数 (Derivative), 链式法则 (Chain Rule), 定义域 (Domain). This helps students studying in English-medium programs.
- Use LaTeX for math: $E = mc^2$ or $$\int_0^1 x^2 dx$$.
- Make transitions smooth between slides — don't just jump from topic to topic. Use phrases like "讲完了X，我们自然要问……", "有了这个基础，接下来……"
- If the slides contain a worked example, walk through it step by step as if explaining to students in real time.
- If the slides contain a diagram or graph, describe what students should look at: "大家看这张图，注意横轴是……纵轴是……曲线在这一点……"
- Format your output exactly like this:

## 教学单元[N]: [Unit Title]

**对应幻灯片:** Slide [X] – Slide [Y]

### 讲课逐字稿

[Your script content here]

---

MUST NOT DO:
- Do NOT use the write tool — return content only.
- Do NOT re-delegate this task to other agents.
- Do NOT skip any slide or subtopic within this teaching unit.
- Do NOT write in formal academic prose — this is spoken language, not a textbook.
- Do NOT add content that contradicts the courseware. You can expand with examples and explanations, but never introduce incorrect or off-syllabus material.

CONTEXT: [Paste the extracted slide content for this teaching unit here]`
)
```

**Track each task_id with its unit number:**
```
Unit 1 → task_id: "task_abc123"
Unit 2 → task_id: "task_def456"
Unit 3 → task_id: "task_ghi789"
...
```

### Step 2: Collect Results and Assemble in Order

After launching all subagents in the background, **end your response and wait for the system `<system-reminder>` notification** for each task completion. Do NOT poll `background_output` on running tasks.

Once all tasks are complete, collect results **in unit order** (NOT by completion time):

```typescript
// Collect in order, NOT by completion time
background_output(task_id="task_abc123")  // Unit 1
background_output(task_id="task_def456")  // Unit 2
background_output(task_id="task_ghi789")  // Unit 3
```

**Error handling for subagent results:**
- If a subagent returns empty or truncated content → **retry** with the same `session_id` and prompt: `"Your previous output was incomplete. Please regenerate the complete script for this unit."`
- If a subagent fails or errors → **retry** with `session_id` and prompt: `"The previous task failed. Please regenerate the script for this unit."`
- If retry also fails → generate that unit's content in the main session using the slide content from Phase 1.
- Always verify each unit result contains the expected `## 教学单元[N]:` header before proceeding to assembly.

### Step 3: Write Final Document (Main Process Only)

Only the main process writes the final file, combining:

1. **Header** (title, metadata)
2. **Unit scripts** (in numerical order 1, 2, 3...)
3. **课堂总结** (lesson summary)
4. **校对报告** (after Phase 3 proofreading)

```markdown
# [Course Name / Subject] — [Topic] 讲课稿

> 科目: [Mathematics / Physics / Chemistry / etc.]
> 教学单元数: [N]
> 适用级别: [A Level / IB / AP / GCSE / etc.]
> 讲稿类型: 逐字稿

---

[Unit 1 script from subagent]

[Unit 2 script from subagent]

[Unit 3 script from subagent]

---

## 课堂总结

[Brief summary of the entire lesson]

---

## 校对报告 (Proofreading Report)

[Results from Phase 3]
```

**Output path decision:**
- **User specified an output path** → Write directly to that path (using the `write` tool). If the path is a directory rather than a filename, use the default filename within that directory.
- **User did not specify** → Use the default naming rule: `[CourseName]_[Topic]_讲课稿.md`, write to the current working directory.
- **Metadata missing fallback** → `讲课稿_YYYY-MM-DD.md`

### Language & Tone Guidelines

The script should sound like an experienced teacher speaking to their class:

- **Opening**: Start each unit with a natural transition from the previous material, or a hook to grab attention
- **Explanation**: Break down complex ideas into digestible steps. Use "我们" instead of "你" to create a collaborative feel
- **Checking understanding**: Build in natural checkpoints — "到这里大家有没有问题？", "这个结论很重要，我再重复一遍"
- **Closing**: End each unit with a brief summary and a bridge to the next topic

### Script Structure by Content Type

**Concept / Definition:**

```markdown
好，我们来看一个新的概念——[概念名称] ([English Term])。

[概念名称] ([English Term])

简单来说，[用通俗语言解释]。大家注意，这里的关键词是 [关键词]。

我们来看它的精确定义：[给出定义]。

谁能用自己的话复述一下这个定义？

好，我来解释一下这个定义里的几个要点：
1. [要点一]
2. [要点二]
3. [要点三]
```

**Formula / Equation:**

```markdown
接下来这个公式非常重要——[公式名称] ([Formula Name])：

$$[formula]$$

这个公式大家必须要记牢，考试经常考。

我们来拆解一下：
- [变量/符号1] 代表 [含义]
- [变量/符号2] 代表 [含义]

举个例子，[给出具体数值代入的例子]。

大家自己动手算一遍。
```

**Worked Example:**

```markdown
我们来看一道例题。

[读出题目内容]

给大家30秒想一想思路。

好，我们一步步来解：

**第一步：** [说明这一步做什么，为什么这样做]
[详细计算/推导过程]

**第二步：** [继续...]

注意这里有一个容易出错的地方——[指出常见错误]。

**Final Answer:** [给出答案]

总结一下，这道题的关键在于 [核心思路]。
```

**Diagram / Graph:**

```markdown
大家看这张图。

[图的标题或关键词]

先看横轴，它表示的是 [横轴含义]。纵轴表示的是 [纵轴含义]。

注意这个 [关键点/转折点/交点]——它告诉我们 [物理/数学/化学意义]。

谁能告诉我，从这个图上你能读出什么信息？

好，我来总结一下这张图要告诉我们的核心结论：[总结]。
```

## Phase 3: Automated Proofreading

After assembling the complete lecture script, run a proofreading pass via a delegated agent. This catches missing slides, awkward transitions, incorrect technical terms, and formatting issues before delivery.

Delegate the proofreading task as follows (use `deep` category for thorough analytical checking):

```
task(
  category="deep",
  load_skills=[],
  run_in_background=false,
  prompt="Act as an experienced A Level teacher and proofread the following lecture teaching script (讲课稿). Check each teaching unit:

1. **Content completeness:** Does every slide from the original courseware have corresponding script content? No slide or subtopic should be missing.
2. **Technical accuracy:** Are all technical terms correct? Are formulas and equations accurate? Are English technical terms properly paired with Chinese explanations?
3. **Teaching flow:** Are transitions between slides natural? Does the script read like natural spoken language, not a textbook?
4. **Pedagogical quality:** Does the script explain concepts clearly? Are there enough checkpoints for student understanding? Are common pitfalls highlighted?
5. **Format compliance:** Does every unit follow the script template structure? Are all LaTeX formulas properly closed?

For each teaching unit, list any issues found along with the corrected content. If a unit has no issues, mark it as '✅ No issues'.

Here is the script to proofread:
[Paste the full lecture script document here]"
)
```

After receiving the proofreading results, apply all corrections to the final output file. Include a brief summary of what was fixed (or confirm that no issues were found) in the "校对报告 (Proofreading Report)" section at the end of the file.

## Output Format — File Only, Never Chat

**CRITICAL: Write the complete lecture script to a `.md` file. Do NOT output the script content to the chat window.**

**Output path resolution (in priority order):**
1. **User specified a full file path** (e.g., `./lectures/calculus_讲课稿.md`) → Write directly to that path.
2. **User specified a directory** (e.g., `./lectures/`) → Write into that directory with the default filename.
3. **User did not specify** → Use the default naming rule `[CourseName]_[Topic]_讲课稿.md`, write to the current working directory.
4. **Metadata missing fallback** → `讲课稿_YYYY-MM-DD.md`

- Use the `write` tool to create the file
- In the chat, only confirm: "✅ Generated lecture script: `[filepath]`, [N] teaching units, complete verbatim script with proofreading report."
- If the file is very large, still write it to disk — never split output across chat messages

## Workflow Summary

```
Phase 1: Extract & Structure
    ↓
    Extract metadata (course name, topic, level) for filename
    ↓
    ≤ 5 slides? → Single unit → Generate directly in main session → skip to Phase 3
    ↓
    > 5 slides? → Group into numbered teaching units (1, 2, 3...)
    ↓
Phase 2: Generate Scripts (Parallel)
    ↓
    Spawn subagents for each unit (load_skills=[], return content, NOT write)
    ↓
    End response → wait for system <system-reminder> notifications
    ↓
    Collect results in order: background_output(task_id_1), background_output(task_id_2), ...
    ↓
    Verify each unit result → retry with session_id if incomplete/failed
    ↓
    Assemble in order: Unit 1 → Unit 2 → Unit 3 → ...
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

- [ ] **Metadata extracted**: course name, topic, and level captured for filename
- [ ] **Every slide** from the courseware has corresponding script content — none skipped
- [ ] The script reads like **natural spoken language**, not academic prose
- [ ] Technical terms use the **bilingual format** (Chinese with English in parentheses)
- [ ] Transitions between slides/units are **smooth and logical**
- [ ] **Subagent results verified**: each unit has complete content, retries applied if needed
- [ ] The **proofreading agent** (category=deep) has run and its corrections have been applied
- [ ] The output follows the **template structure** above
- [ ] The complete script is written to a **`.md` file** — NOT output to the chat window
- [ ] **Unit scripts are in correct order** — subagents returned content, main process assembled in order
