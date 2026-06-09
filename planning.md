# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

<!-- What domain did you choose? Why is this knowledge valuable and hard to find through official channels? -->
It covers a beginners guide to rock climbing. This includes tips for training, how to 
     prevent injury, explains the grading system, etc. It is useful because this info is
     scattered all over the place and I as an intermediate climber who just went through 
     this beginner phase looked through these sources. 
---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

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
<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size:**
My target chunk size will be about 200 words per chunk. This is large enough to keep a full explanation together, but small enough that the retrieval system can return focused results instead of an entire article. 

**Overlap:**
I will use an overlap of 50 words between chunks when a section has to be split. This helps prevent important context from being lost between two chunks. For shorter sections that fit naturally into one chunk, I will not need overlap.

**Reasoning:**
Explained already.

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:**
all-MiniLM-L6-v2 via sentence-transformers

**Top-k:** 
I will retreive 3 chunks because most of the information should be similar so there is not a need for more than that.

**Production tradeoff reflection:**
I would consider a stronger embedding model than all-MiniLM-L6-v2. I would compare models based on accuracy, context length, and latency. Accuracy matters because climbing questions can use different wording than the sources, such as “fear of falling” versus “fear of heights.” Context length matters because some guide sections may be longer and need to stay together. Latency matters because users expect quick answers, especially in an interactive app. 
---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | What type of climbing shoes are good for beginners? | Something about the shoes not being aggressive, comfortable fit, not downturned shoes. |
| 2 | How can I prevent injury? | Make sure to warm up and take ample rest. |
| 3 | Can I start hangboarding if I started climbing this week? | No, you should try to climb until you hit a plateu first, then do it. |
| 4 | How should I fall down after a boulder? | You want to fall backwards, feet hitting the ground first then your back. |
| 5 | What does 5.12a mean. | That is the Yosemite Decimal system and the 5 means you need a rope whilst the 12 means it is quite difficult. The a implies its an easier 5.12. |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1. I feel that some questions may warrant different answers that could both be right, so the answer may be confusing

2. Since the topic is so broad there might be too much fluff in a chunk, or just too much variety in answers

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->
[Document Ingestion]
- Source URLs / saved text files
- requests + BeautifulSoup or manual text files
- Clean HTML, ads, navigation, footers
        |
        v
[Chunking]
- Semantic section-based chunking
- Target size: 300–600 words
- Overlap: 50–100 words when splitting long sections
        |
        v
[Embedding + Vector Store]
- Embedding model: sentence-transformers/all-MiniLM-L6-v2
- Vector store: ChromaDB
- Store chunk text + source metadata
        |
        v
[Retrieval]
- User question enters system
- Semantic similarity search in ChromaDB
- Retrieve top-k = 5 chunks
        |
        v
[Generation]
- LLM: Groq llama-3.3-70b-versatile
- Answer only using retrieved chunks
- Return answer with source citations
---

## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)
     - What you expect it to produce
     - How you'll verify the output matches your spec

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->

**Milestone 3 — Ingestion and chunking:**

**Milestone 4 — Embedding and retrieval:**

**Milestone 5 — Generation and interface:**
