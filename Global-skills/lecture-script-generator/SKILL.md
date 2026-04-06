---
name: lecture-script-generator
description: Generate a verbatim lecture teaching script (讲课稿) from A Level courseware PDFs. Use this skill whenever the user uploads a PDF of lecture slides/courseware and asks to generate a teaching script, lecture notes, 讲课稿, 讲稿, 教案, 课件讲稿, or anything about turning slides into something a teacher can read aloud while teaching. Also trigger when the user says "帮我写讲课稿", "把这个课件变成讲稿", "生成讲课稿", "做一份讲课用的稿子", "write a lecture script from these slides", or any request involving converting courseware/slides into a spoken teaching script. Works with A Level, IB, AP, GCSE, or any subject courseware PDFs. Make sure to use this skill whenever the user mentions 讲课稿, 讲稿, 教案, lecture script, teaching script, or wants to turn courseware into something they can teach from.
---

# Lecture Script Generator (讲课稿生成器)

## Skill Overview

This skill handles the complete workflow of extracting content from A Level courseware PDFs and producing a **verbatim lecture teaching script (逐字稿)** that a teacher can read aloud while delivering a lesson. It covers three phases: **extraction → script generation → proofreading**.

The output includes natural spoken explanations, teaching rhythm cues (interaction prompts, board-writing markers, pause points), and bilingual technical terms — all structured by the original slide/chapter order.

## Phase 1: PDF Content Extraction & Structuring

Start by extracting the courseware content. The `pdf` skill handles text extraction and OCR for scanned documents — use it as your primary tool.

**What to capture for each section/slide:**

- Slide number or section title
- All key concepts, definitions, formulas, and examples listed on the slide
- Diagrams, graphs, tables — describe them in text so the script can reference them naturally
- Any worked examples, practice problems, or case studies embedded in the slides
- The logical flow: how one slide connects to the next

**Structuring the content:**

Group slides into **teaching units (教学单元)** — typically 3-5 slides that cover one coherent subtopic. Each teaching unit will become one section of the lecture script.

**Why this matters:** The script needs to know not just what's on each slide, but how the material flows from one idea to the next. Missing a transition or misreading a diagram will result in an awkward teaching script.

**Assign each teaching unit a sequential number (1, 2, 3...) for ordered assembly later.**

## Phase 2: Verbatim Script Generation

Generate a **逐字稿 (verbatim script)** for every teaching unit. The core principle: write exactly what the teacher would *say* out loud — natural, conversational, pedagogically sound — not a textbook summary.

### ⚠️ CRITICAL: Parallel Execution with Ordered Assembly

**The Problem:** When spawning multiple subagents in parallel, they complete at different times. If each writes directly to the output file, the final document will have units in random order.

**The Solution:** Subagents return content, main process assembles in order.

### Step 1: Spawn Parallel Subagents (Return Content, NOT Write File)

Spawn one subagent per teaching unit. **Instruct subagents to RETURN their script content, NOT write to file.**

```typescript
task(
  category="deep",
  load_skills=["lecture-script-generator"],
  run_in_background=true,
  description="Generate script for Unit N",
  prompt=`TASK: Generate a verbatim lecture teaching script (逐字稿) for Teaching Unit [N] from the A Level courseware.

EXPECTED OUTCOME: Return the complete markdown-formatted script block for this teaching unit as your final message. DO NOT write to any file — just return the content.

⚠️ CRITICAL: You MUST return the script content in your response. Do NOT use the write tool. The main process will collect all unit scripts and assemble them in order.

MUST DO:
- Write in natural spoken Chinese — the teacher should be able to read this aloud directly. Use conversational phrasing like "大家看这里", "我们接下来看", "注意这个细节".
- Preserve English technical terms alongside Chinese: 导数 (Derivative), 链式法则 (Chain Rule), 定义域 (Domain). This helps students studying in English-medium programs.
- Include teaching rhythm cues using bracketed markers:
  - 【板书】— write this on the board
  - 【提问】— ask students a question
  - 【互动】— class discussion or student activity
  - 【停顿】— pause for students to absorb
  - 【强调】— emphasize this point (raise voice, repeat, or slow down)
  - 【举例】— give an example (expand beyond the slide)
  - 【翻片】— advance to the next slide
  - 【回顾】— briefly recap previous material
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

After all subagents complete (you'll receive notifications), collect results **in unit order**:

```typescript
// Collect in order, NOT by completion time
const unit1Result = await background_output({ task_id: "task_abc123" });
const unit2Result = await background_output({ task_id: "task_def456" });
const unit3Result = await background_output({ task_id: "task_ghi789" });
```

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
> 讲稿类型: 逐字稿（含教学节奏提示）

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

### Single-Unit Courseware

If there's only one teaching unit, generate directly in the main session — no delegation needed. Write the complete file in one operation.

### Language & Tone Guidelines

The script should sound like an experienced teacher speaking to their class:

- **Opening**: Start each unit with a natural transition from the previous material, or a hook to grab attention
- **Explanation**: Break down complex ideas into digestible steps. Use "我们" instead of "你" to create a collaborative feel
- **Checking understanding**: Build in natural checkpoints — "到这里大家有没有问题？", "这个结论很重要，我再重复一遍"
- **Closing**: End each unit with a brief summary and a bridge to the next topic

### Script Structure by Content Type

**Concept / Definition:**

```markdown
【翻片】

好，我们来看一个新的概念——[概念名称] ([English Term])。

【板书】[概念名称] ([English Term])

简单来说，[用通俗语言解释]。大家注意，这里的关键词是【强调】[关键词]。

【停顿】

我们来看它的精确定义：[给出定义]。

【提问】谁能用自己的话复述一下这个定义？

好，我来解释一下这个定义里的几个要点：
1. [要点一]
2. [要点二]
3. [要点三]
```

**Formula / Equation:**

```markdown
【翻片】

接下来这个公式非常重要——[公式名称] ([Formula Name])：

【板书】$$[formula]$$

【强调】这个公式大家必须要记牢，考试经常考。

我们来拆解一下：
- [变量/符号1] 代表 [含义]
- [变量/符号2] 代表 [含义]

【举例】举个例子，[给出具体数值代入的例子]。

【停顿】大家自己动手算一遍。
```

**Worked Example:**

```markdown
【翻片】

我们来看一道例题。

【读题】[读出题目内容]

【停顿】给大家30秒想一想思路。

好，我们一步步来解：

**第一步：** [说明这一步做什么，为什么这样做]
[详细计算/推导过程]

**第二步：** [继续...]

【强调】注意这里有一个容易出错的地方——[指出常见错误]。

**Final Answer:** [给出答案]

【回顾】总结一下，这道题的关键在于 [核心思路]。
```

**Diagram / Graph:**

```markdown
【翻片】

大家看这张图。

【板书】[图的标题或关键词]

【引导】先看横轴，它表示的是 [横轴含义]。纵轴表示的是 [纵轴含义]。

【强调】注意这个 [关键点/转折点/交点]——它告诉我们 [物理/数学/化学意义]。

【提问】谁能告诉我，从这个图上你能读出什么信息？

好，我来总结一下这张图要告诉我们的核心结论：[总结]。
```

## Phase 3: Automated Proofreading

After assembling the complete lecture script, run a proofreading pass via a delegated agent. This catches missing slides, awkward transitions, incorrect technical terms, and formatting issues before delivery.

Delegate the proofreading task as follows:

```
task(
  category="unspecified-high",
  load_skills=[],
  run_in_background=false,
  prompt="Act as an experienced A Level teacher and proofread the following lecture teaching script (讲课稿). Check each teaching unit:

1. **Content completeness:** Does every slide from the original courseware have corresponding script content? No slide or subtopic should be missing.
2. **Technical accuracy:** Are all technical terms correct? Are formulas and equations accurate? Are English technical terms properly paired with Chinese explanations?
3. **Teaching flow:** Are transitions between slides natural? Does the script read like natural spoken language, not a textbook? Are teaching rhythm cues (【板书】,【提问】,【停顿】etc.) placed at appropriate points?
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

- Filename convention: `[CourseName]_[Topic]_讲课稿.md` (e.g., `A-Level_Mathematics_Calculus_讲课稿.md`)
- Use the `write` tool to create the file
- In the chat, only confirm: "✅ 已生成讲课稿：`[filename].md`，共 [N] 个教学单元，含完整逐字稿与校对报告。"
- If the file is very large, still write it to disk — never split output across chat messages

## Workflow Summary

```
Phase 1: Extract & Structure
    ↓
    Group slides into numbered teaching units (1, 2, 3...)
    ↓
Phase 2: Generate Scripts (Parallel)
    ↓
    Spawn subagents for each unit (return content, NOT write)
    ↓
    Collect results: background_output(task_id_1), background_output(task_id_2), ...
    ↓
    Assemble in order: Unit 1 → Unit 2 → Unit 3 → ...
    ↓
    Write complete file (main process only)
    ↓
Phase 3: Proofread
    ↓
    Apply corrections to file
    ↓
    Done!
```

## Quality Checklist

Before delivering the final answer, confirm each item:

- [ ] **Every slide** from the courseware has corresponding script content — none skipped
- [ ] The script reads like **natural spoken language**, not academic prose
- [ ] Technical terms use the **bilingual format** (Chinese with English in parentheses)
- [ ] **Teaching rhythm cues** (【板书】,【提问】,【停顿】etc.) are placed at pedagogically appropriate points
- [ ] Transitions between slides/units are **smooth and logical**
- [ ] The **proofreading agent** has run and its corrections have been applied
- [ ] The output follows the **template structure** above
- [ ] The complete script is written to a **`.md` file** — NOT output to the chat window
- [ ] **Unit scripts are in correct order** — subagents returned content, main process assembled in order