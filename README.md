# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

<!-- What topic or category of knowledge does your system cover?
     Why is this knowledge valuable, and why is it hard to find through official channels?
     Example: "Student reviews of CS professors at [university] — useful because official
     course descriptions don't reflect teaching style, exam difficulty, or workload." -->
     It covers a beginners guide to rock climbing. This includes tips for training, how to 
     prevent injury, explains the grading system, etc. It is useful because this info is
     scattered all over the place and I as an intermediate climber who just went through 
     this beginner phase looked through these sources. 

---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 | REI    | How to Start Climbing | https://www.rei.com/learn/expert-advice/getting-started-rock-climbing.html |
| 2 | REI    | How to start Bouldering | https://www.rei.com/learn/expert-advice/bouldering.html |
| 3 | Ascend | Climbing Etiquette | https://www.ascendclimbing.com/your-visit/rules-etiquette?utm_source=chatgpt.com |
| 4 | SportRock | Climbing Grades | https://www.sportrock.com/post/understanding-climbing-grades |
| 5 | Climbing Magazine | Climbing Shoes | https://www.climbing.com/gear/best-beginner-climbing-shoes/ |
| 6 | BreakingInMyShoes | Training Guide | https://breakinginmyshoes.wordpress.com/2013/05/06/climbing-training-for-beginners/ |
| 7 | 5.Life | Fear of Heights when Climbing | https://5.life/blog/2024/07/26/3-tips-to-overcome-your-fear-of-heights/ |
| 8 | RockClimbingRealms | Beginner to V4 Guide | https://rockclimbingrealms.com/tips-on-rock-climbing/#:~:text=The%20V3%2DV4%20jump%20is,level%20should%20come%20from%20climbing. |
| 9 | Butora | When to Hangboard Train | https://butorausa.com/blogs/beta-blog/when-to-hangboard?srsltid=AfmBOoqaYCVU6cLB9bOt8zpHO5GSnzAhkjEPo11FDwtt6wkILMHxVkEE |
| 10 | Climbing Magazine| Typical Climbing Mistakes | https://www.climbing.com/skills/7-beginner-climber-mistakes/ |

---

## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->
     I will use semantic, section-based chunking because most of my sources are educational articles organized by headings and subtopics. Each chunk will contain one heading and the paragraphs under that heading, so information about gear, safety, grades, training, and injury prevention stays together.

**Chunk size:**
My target chunk size will be about 500–800 words per chunk. This is large enough to keep a full explanation together, but small enough that the retrieval system can return focused results instead of an entire article. If a section is longer than 800 words, I will split it by paragraph into smaller chunks.


**Overlap:**
I will use an overlap of about 75–100 words between chunks when a section has to be split. This helps prevent important context from being lost between two chunks. For shorter sections that fit naturally into one chunk, I will not need overlap.

**Why these choices fit your documents:**

**Final chunk count:**

---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:**

**Production tradeoff reflection:**

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**

**How source attribution is surfaced in the response:**

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |
| 4 | | | | | |
| 5 | | | | | |

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:**

**What the system returned:**

**Root cause (tied to a specific pipeline stage):**

**What you would change to fix it:**

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:**

**One way your implementation diverged from the spec, and why:**

---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**

- *What I gave the AI:*
- *What it produced:*
- *What I changed or overrode:*

**Instance 2**

- *What I gave the AI:*
- *What it produced:*
- *What I changed or overrode:*
