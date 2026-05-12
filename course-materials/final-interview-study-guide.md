# Final Interview Study Guide

**Course:** ISBA 4715 — Developing Business Applications Using SQL
**Assessment:** Analytics Engineer Interview (25% of course grade, 100 points)
**Format:** In-person, Hilton 114 (instructor's office), 20-minute Calendly slot
**Window:** Mon May 11, Tue May 12, or Wed May 13 — [book your slot at calendly.com/greg-lontok/sql-final-interview](https://calendly.com/greg-lontok/sql-final-interview)
**Recording:** Pre-interview practice run due 11:59pm the day before your Calendly slot, worth 10 pts of the 100-pt interview (see section 07).
**Resume:** `docs/resume.pdf` due May 11. Graded in the project rubric as deliverable #15 (5 pts), not in the interview score. See `project/README.md`.

---

## 01 Premise

You come into Hilton 114, go to the whiteboard, and defend your portfolio project against the role you've been targeting all semester. This is not a quiz. It is a conversation about work you actually built, judged against the job description in 03. The interviewer wants to know what you built, why you made the choices you made, and what the data tells the business.

**What an analytics engineer is.** Analytics engineering is the role that owns the transformation layer between raw ingested data and the analyst-ready models that dashboards and queries depend on. In practice, analytics engineers also do analysis on top of those models, turning the numbers into business decisions. That's why your portfolio includes both a dbt mart and a Streamlit dashboard with insights. The signature stack is SQL + dbt plus a cloud warehouse like Snowflake, exactly what you built in MP01 through MP04. Your portfolio project is an analytics engineering portfolio whether your JD calls the role "analytics engineer," "data engineer," or "data analyst": what matters is that you own the transformation layer end-to-end and can defend the insights it produces.

## 02 Rubric

The project is the assessment; "Tell me about yourself" is a quick on-ramp that gets you into the room. A pre-interview recording (section 07) counts toward the same 100.

| Section | Points | What's assessed |
|---|---|---|
| Pre-interview recording | 10 | Submitted on time, both questions present in the right length range, whiteboard visible. Pass/fail (see section 07). |
| "Tell me about yourself" (live) | 10 | Tailored to the portfolio JD: education, initiative, relevant experience, human connection, segue into project. Concise (≤1 minute), confident, structured. |
| Project (live) | 80 | Pipeline accuracy and completeness, technical defensibility, knowledge base is defensible when asked, insights are specific and actionable, story arc is clean (beginning → middle → end), challenge/improvement/lesson all addressed. |
| **Total** | **100** | |

| Grade | Criteria |
|---|---|
| **A** | Exceptional — clear mastery of problem-solving, business insight, technical depth, and communication. Ready to lead without hand-holding. *"I'm impressed. Let's hire this candidate."* |
| **B** | Strong — meets all core requirements and shows growth potential. Only minor gaps. *"Good enough but I'd want them in for another interview."* |
| **C** | Adequate — satisfies basic criteria but skills are uneven. Would require mentoring. *"I have reservations, but they might be coachable."* |
| **D / F** | Underperforming — fell significantly short of expectations. Substantial improvement needed before being considered for the role. *"Hard pass."* |

### Hints

The instructor leading you through your own repo is dialogue, not a hint. A hint is when the instructor supplies the answer to a defensibility question.

- **One free hint** across the entire project section (not per sub-segment)
- Each additional hint after the first: **−3 pts within the project's 80**
- **AI ownership:** if you cannot distinguish what you wrote from what AI scaffolded, the relevant component scores at most 50% of its weight

## 03 Your Job Description

There is one job description in the room: the posting at `docs/job-posting.pdf` in your portfolio repo, the role you've been targeting all semester. "Tell me about yourself" tailors who you are to that role. The project section tailors what you built to that role. If you've pivoted to a different role since picking your portfolio JD, swap the file and re-run the Practice Prompts in 05 against the new posting before May 11.

## 04 Structure and Questions

| Phase | Time | What happens |
|---|---|---|
| **"Tell me about yourself"** (10 pts) | 0:00–1:00 | "Tell me about yourself." 60 seconds tailored to your portfolio JD. |
| **Project** (80 pts) | 1:00–15:00 | "Tell me about your project." Go to the whiteboard. Draw and narrate the pipeline. Tell the full story. Be ready when the instructor asks about the knowledge base. |
| **Debrief + feedback** | 15:00–20:00 | Instructor walks through how you did. Closing feedback. |

### "Tell me about yourself"

60 seconds, anchored to `docs/job-posting.pdf`. Hit five targets:

- **Education** — degree, major, relevant coursework
- **Extracurricular or side project showing initiative** — signals you build things on your own
- **Relevant work or internship** — experience that maps to the JD's expectations
- **One personal tidbit** — a human detail that makes you memorable
- **Segue into the project** — one-sentence bridge into your portfolio project

**Stack words and phrases:** the technical terms in your JD. These include tool names (e.g., dbt, Snowflake, GitHub Actions), patterns (star schema, ETL, data modeling), and skills (SQL, Python, BI dashboards). Hiring managers scan answers for these because they're how the JD signals "we work with this." Landing two or three stack words in your "Tell me about yourself" tells the interviewer: I read the posting, and the work I built maps to your stack.

### Project

14 minutes, 80 points. You lead. The instructor asks questions and takes notes while you explain. Keep narrating and answer probes as they come up; don't pause and wait. Common patterns: "why X over Y?" (defend a technical decision), scale hypothetical ("what breaks at 100× volume?"), prioritization ("what slipped first when time got tight?").

Cover eight elements in order:

1. **Elevator pitch** — one sentence: who you're helping, what problem, how you're solving it
2. **Connection to your portfolio JD** — why this project, why this role, what skills overlap
3. **Pipeline whiteboard walk** — draw and narrate both pipelines: API → Snowflake → dbt staging → mart, plus scrape → `knowledge/raw/` → wiki. Label tools, schema, and table names.
4. **Technical deep dive** — four sub-segments:
   - **Data ingestion and automation:** API + Firecrawl scrape, GitHub Actions schedule + manual trigger, secrets handling
   - **Modeling and warehouse setup:** Snowflake raw → dbt staging → mart, star schema, one dbt test
   - **Knowledge base (verbal):** Don't demo live — narrate it. What's in `knowledge/raw/` (the scraped sources) versus `knowledge/wiki/` (the agent-built summary). One example of a question whose answer routes through the wiki and cites a specific raw file. The instructor will ask about the KB during the project narration; be ready to walk through the layers without opening a terminal.
   - **Streamlit dashboard sketch (optional):** Sketch panes on the whiteboard — descriptive, diagnostic, interactive. No live demo expected.
5. **Insights** — 1–2 specific insights and the business decisions they inform
6. **One significant challenge** and how you overcame it
7. **One future improvement** and why it matters
8. **One lesson learned** that transfers to future projects

### Debrief + feedback

The last 5 minutes is feedback time. The instructor walks through how you did and gives closing feedback.

## 05 Practice Prompts (rehearse with Claude Code)

**Practice with humans first; AI is the fallback.** The best rehearsal partners are the ones who have to listen to you: a classmate, a friend, a roommate, a parent, a sibling. Claude Code is what you reach for when you don't have a human handy, not because it's better. The parent test is your quality bar: can a non-technical person who cares about you follow your project walkthrough end-to-end? If they get lost, you've over-jargoned, and the interviewer will too. Aim to clear the parent test before May 11.

These prompts turn Claude Code into a rehearsal partner against your actual repo and your portfolio JD when no human is available. Paste them into a Claude Code session opened in your portfolio repo. The `@` references load files into context. They only work if the file exists at the path shown.

**Tip:** use speech-to-text for these rehearsals. Typing turns practice into a writing exercise, but the interviewer in Hilton 114 will be listening, not reading. Try [Wispr Flow (student pricing)](https://wisprflow.ai/students) or your OS's built-in dictation to dictate your responses. The closer rehearsal is to actually speaking, the better the feedback.

Note: the prompts below reference `@docs/job-posting.pdf`. If your JD is saved as a different format (`.md`, `.txt`), update the path before pasting.

---

### 05.a — "Tell me about yourself" content draft

Use this when: you're staring at a blank scratch file and need help generating content for each of the five "Tell me about yourself" components. This produces an initial draft you can refine with 05.b.

```text
Load @docs/job-posting.pdf and @docs/resume.pdf.

I'm drafting a 60-second "Tell me about yourself" for the role in the JD. Ask me one
focused question for each of the five components below, one at a time, waiting for my
answer before moving to the next:

1. Education — what's the most relevant thing about your degree, major, or coursework
   for this specific role?
2. Initiative — what extracurricular activity or side project shows you build things
   on your own, without being told to?
3. Relevant work — what internship, job, or volunteer experience maps to the JD's
   responsibilities?
4. Personal tidbit — what's one human detail about you (a hobby, where you grew up,
   something you're learning) that would make a hiring manager remember you?
5. Segue — what's a one-sentence bridge from your background into your portfolio
   project?

Tailor each question to the JD. If I say "I'm stuck," "I don't know," or "I don't
have one," give me three concrete example angles drawn from what's in my resume and
the JD (or, if neither helps, common student backgrounds like CS major, business
analytics minor, club leadership, retail/hospitality work, family small business)
before re-asking the question.

After I've answered all five, stitch my answers into a 60-second "Tell me about
yourself" draft. The output is an initial draft I'll refine with 05.b — don't polish
yet, just get the content on paper.

Start with the education question.
```

---

### 05.b — "Tell me about yourself" rehearsal

Use this when: you have a draft of your 60-second intro (from 05.a or your own scratch) and want to score it against the five "Tell me about yourself" targets and tighten it before practicing out loud.

```text
Load @docs/job-posting.pdf and @docs/resume.pdf. You are a hiring manager interviewing me for the role in the JD.

Start the interview now: ask me "Tell me about yourself."

After I type my response, score me on three things:
1. Did it hit all five targets — education, extracurricular/initiative, relevant work or
   internship, one personal tidbit (human connection), and a segue into my project?
2. Is it 60 seconds or under when spoken aloud at a natural pace?
3. Does it use at least two stack words or phrases that appear in the JD?

Give me one specific sentence to cut or rewrite, then ask me to try again.
```

---

### 05.c — Whiteboard pipeline rehearsal

Use this when: you want to practice narrating your pipeline end-to-end and getting three role-tied follow-ups at the end, before you're standing at the whiteboard in Hilton 114.

```text
Load @README.md, @knowledge/wiki/, and @docs/job-posting.pdf.

You are a technical interviewer. I'm going to narrate my pipeline as if I'm at
the whiteboard.

After I finish the full walkthrough, give me three questions you'd expect a real
interviewer to ask for this specific role, based on what's in the JD and what
gaps you noticed in my narration.

Start by saying "Tell me about your project."
```

---

### 05.d — Component drill on any pipeline layer

Use this when: you want to pressure-test your understanding of one specific piece of the repo before the interview.

```text
Find the files in this repo related to <COMPONENT>.
(Replace <COMPONENT> with the piece you want to drill — for example:
"GitHub Actions schedule," "dbt staging model," "Firecrawl scrape script,"
"Snowflake raw table schema," or "knowledge base wiki structure.")

Ask me five questions a senior analytics engineer would ask about that component:
1. What does it do?
2. Why did I choose this approach over an obvious alternative?
3. What's a realistic failure mode?
4. What would I change with more time?
5. What does the output flow into downstream?

After each answer, point to the specific file or section where my answer can
be verified — or flag if my answer doesn't match what's actually in the repo.
```

---

### 05.e — Full mock interview (the take-home rehearsal)

Use this when: you want to run the complete 20-minute interview structure before your Calendly slot. Run this at least once between May 5 and May 10.

```text
Load @docs/job-posting.pdf, @README.md, @knowledge/wiki/, and @CLAUDE.md.

You are a hiring manager conducting a 20-minute analytics engineer interview.
Run the full structure in sequence:

1. Open with "Tell me about yourself." After I answer, score my "Tell me about yourself" on the
   five targets (education, initiative, relevant work, personal tidbit, segue)
   and tell me one thing to improve before moving on.

2. Transition to "Tell me about your project." Anchor your follow-up questions
   to the responsibilities and skills listed in the JD. Probe my pipeline with
   at least three follow-up questions during the 14-minute project section.
   One of those probes must ask about my knowledge base — what's in
   knowledge/raw/ versus knowledge/wiki/, and how I'd cite a raw source if you
   asked me a question that routed through the wiki. I won't run a live demo;
   judge me on how clearly I narrate the layers.

3. Close with three follow-up questions — one on prioritization logic, one on
   an alternative approach I considered and rejected, one on what breaks first
   at 100× data volume.

4. After I answer all three, score me using the A/B/C/D/F descriptor rubric:
   A = ready to hire, B = strong with minor gaps, C = adequate but uneven,
   D/F = substantial gaps. Give one sentence of justification for each phase
   ("Tell me about yourself", pipeline walkthrough, follow-ups).

Start now with "Tell me about yourself".
```

---

### 05.f — Knowledge base readiness check

Use this when: you want to verify your wiki is coherent enough to defend verbally before the interview, ideally by May 4 so any issues surface while help is still available. You won't run a live demo in the interview, but the instructor will ask about the KB — and you can only answer accurately if the wiki actually works.

```text
Load @knowledge/wiki/ and @knowledge/raw/.

Run a five-step diagnostic on my knowledge base:

1. List every file in knowledge/wiki/ and every file in knowledge/raw/.
2. Identify three facts that appear in knowledge/raw/ source files but are not
   yet reflected in any knowledge/wiki/ page.
3. Pick one of those facts and query the wiki for it as if you were the
   interviewer asking a live question. Report exactly what the wiki returns
   and whether the answer cites a knowledge/raw/ source.
4. If the wiki can't answer the question, identify what's missing — is it a
   gap in the wiki page, a missing schema entry in CLAUDE.md, or a raw source
   that was never ingested?
5. Output a 5-line troubleshooting checklist I can run on the morning of my
   interview to confirm the KB is ready.
```

Note: if this prompt fails on May 4, that's why class Part 07 exists. Bring it to the live-fire session.

---

### 05.g — Resume polish

Use this when: you want targeted edits before committing `docs/resume.pdf` by May 11.

```text
Load @docs/job-posting.pdf and @docs/resume.pdf.

Review my resume against the JD and give me:
1. Three specific edits — quote the exact phrase in my current resume and the
   replacement wording. Focus on bullets that undersell a relevant skill or
   use vague language where the JD is specific.
2. One bullet to add, with proposed wording, that surfaces work my resume
   currently understates relative to the JD's requirements.
3. Three stack words or phrases from the JD that should appear at least once
   in my resume but currently don't.
```

## 06 Cheat sheet (recommended)

In L09 Session 02, you used `CLAUDE.md` as a contract: a single file in your repo that told the agent exactly what the knowledge base schema looked like and held it accountable to that shape. The same pattern applies here. If you want a cheat sheet, create `docs/interview-prep-notes.md` in your portfolio repo: a bulleted list where each line is one pipeline component you're prepared to defend in your interview. The contract is with yourself: "if it's not on this list, I'm not claiming I built it."

This isn't a checklist for the instructor. It's a pre-commitment to yourself. The AI policy in `project/README.md` is direct: "If you can't explain it, you don't get credit for it." The cheat sheet is how you make that concrete before the interview, not in the middle of one.

Save the file as `docs/interview-prep-notes.md`. Use this format:

```markdown
# What I'm prepared to defend in the final interview

- API extraction: `pipelines/extract_orders.py` — pulls daily orders from the e-commerce API into `data/raw/orders/`
- Snowflake raw → dbt staging: `models/staging/stg_orders.sql` — cleans column types, adds row hash
- Mart: `models/marts/fct_daily_revenue.sql` — fact table joined to `dim_date` and `dim_product`
- GitHub Actions schedule: `.github/workflows/daily-extract.yml` — runs daily at 06:00 UTC, writes to Snowflake
- Knowledge base wiki: `knowledge/wiki/competitive-landscape.md` — 4 wiki pages built from `knowledge/raw/` scrapes
- Streamlit dashboard: `app/dashboard.py` — descriptive view (revenue trend) + diagnostic view (segment drilldown)
```

Note: this example is intentionally generic. Your actual list will look different. Use your real file paths and one-sentence descriptions. Refine it as you practice between May 5 and your slot. Not required, not graded.

## 07 Pre-interview recording (10 pts)

A recorded practice run of both interview questions, submitted before your Calendly slot. Recording is the prep. Hearing yourself back is the closest thing to hearing what the interviewer hears, and it surfaces timing slips and filler words you can't catch any other way.

**What to record:**

- "Tell me about yourself" — about 60 seconds
- "Tell me about your project" — about 8–14 minutes, walking through your pipeline at a whiteboard

**Format:**

- Zoom cloud recording (LMU institutional account)
- You don't have to show your face, but the whiteboard must be visible
- A piece of paper counts as a whiteboard. A real whiteboard is recommended. The library study rooms have them.

**Delivery:** record from memory, not from notes. An honest attempt is the point — perfection isn't expected. Stumbles, pauses, and forgotten details are all fine; they tell you what to refine before the live interview.

**Due:** 11:59pm the day before your Calendly slot. Submit the Zoom share link in the Brightspace assignment.

**Grading:** Pass/fail. 10 pts if all three criteria below are met by the deadline; 0 pts if not.

- Recording exists at the submitted link and plays
- Both questions present, roughly within length bands ("Tell me about yourself" 45–90 sec; "Tell me about your project" ≥6 min walking through your pipeline)
- Whiteboard visible

The recording is reviewed only by the instructor.

## 08 Study Material

**Course materials:**
- `lessons/06-local-pipeline/` through `lessons/10-streamlit-dashboard/` — every tutorial
- Lesson slides — every L06–L10 slide deck where present
- `project/README.md` — the rubric you're being graded against
- `lessons/05-data-storytelling/README.md` — DC ACT framework, takeaway titles

**Your own work:**
- Your portfolio repo `README.md` and `CLAUDE.md`
- Your `knowledge/wiki/` files
- Your dbt models (`models/staging/`, `models/marts/`)
- Your Streamlit dashboard (the deployed URL — for your own reference; you'll sketch it on the whiteboard, not demo live)

**External:**
- O'Reilly Learning (LMU library has a free subscription) — search "data engineering interview"
- [Karpathy's LLM wiki gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) — the inspiration for your `knowledge/wiki/` pattern

## 09 Study Tips

- **Practice on humans, not just classmates.** Form a study group of 2–3 people, then keep going: a roommate, a parent, a friend in a different major. The best test is whether a non-technical person who cares about you can follow your project walkthrough (the parent test). If they get lost, the interviewer will too. AI rehearsal is the fallback when no human is available, not the headline.
- **Practice your elevator pitch out loud, not in your head.** Record yourself once.
- **Whiteboard from memory.** Close the laptop. Draw the pipeline. Compare to the L10 diagram afterward. Repeat until you can do it without consulting.
- **Rehearse without notes.** If you can't deliver "Tell me about yourself" without reading, you can't deliver it under pressure.
- **Draft short follow-up answers.** Use the 05.d component drill prompt across each layer; save the answers to scratch notes.
- **Focus on weak spots.** The cheat sheet (06) surfaces what you can't defend; spend study time there, not on the parts you already know.
- **Lead with the big picture.** Always open with the elevator pitch and the pipeline shape before diving into a specific file or query.
- **Strategize with Claude Code.** Use Practice Prompt 05.e (full mock) at least once before May 11. The score the prompt gives you is information.

## 10 Interview Tips

- **Take your time.** Silence while you think reads as confidence, not weakness.
- **Talk about what you know first.** If asked something open-ended, lead with the part you can defend cleanly. The interviewer will follow your lead.
- **Structure your response.** STAR (Situation → Task → Action → Result) works well for behavioral follow-ups. For technical follow-ups, lead with the answer, then the reasoning.
- **Keep answers concise.** A 30-second answer beats a 90-second one nine times out of ten. If the interviewer wants more, they'll ask.
- **Ask one clarifying question if a follow-up is ambiguous.** Better than answering a question that wasn't asked. The interviewer would rather repeat than score a misread answer.

## 11 Last Tips

- **Sleep.** Don't pull an all-nighter the day before your interview.
- **Breathe.** A slow exhale before "Tell me about yourself" resets your voice.
- **Carpe diem.** You built a real pipeline this semester. This is your moment to talk about it.

