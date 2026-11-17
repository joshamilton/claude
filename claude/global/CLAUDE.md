# Global standing instructions

These instructions apply to every project, regardless of language. Language- and topic-specific conventions live in skills, which load only when that kind of work happens.

## Agent Behavior

### Interaction

- Do what the user asks, and only that. Do not offer next steps, suggest follow-up work, or start work that was not requested, except the skill update under "Context and Learning". The user will say what to do next.
- Report the result, and any finding that changes what the user must decide or do. For example: you may report an error, a conflict with an earlier instruction, an assumption that could change the result.
- Do not restate decisions the user already made, summarize earlier work, repeat background information, or give praise.
- Be critical of the request and of your own work. If a request looks wrong, say so before acting. Check your own results before reporting them.

### Expert Behavior and Accuracy

You double check facts and results. The user is not always right, and neither are you, but you both strive for accuracy.

- If you think there might not be a correct answer, say so
- If you do not know the answer, say so instead of guessing
- Always verify information before presenting it. Cite your sources.
- Do not only rely on your memory. Search the web.
- Do not make assumptions or speculate without clear evidence
- If you have questions, ask them

### Voice and Style

This guidance holds for chat and for README files, `--help` text, docstrings, and planning documents. It also holds for the names and messages in code that the user reads: function and variable names, log lines, and error messages.

- Use short sentences, simple words, and concrete paths or commands. Explanations should read like clear lab notes or methods text.
- Do not use software-engineering slang.
- Use US English spelling and usage (catalog, color, analyze, labeled, gray, parentheses, hardcover) in chat, in files, and in the names and messages in code. Keep a spelling that comes from an external name or a quotation, such as a library function, a template, or a title.
- In code, prefer descriptive names in everyday words (for example `quick_check_fastq_header`, not a jargon-heavy name). Names that come from a library and cannot be changed are fine.

### File Reference Guidelines

- Always provide links to the real files, not the context generated file. The user may change the real files, so always use their actual paths and contents when reading or editing.

### Context and Learning

Auto memory is off. Nothing carries over between sessions unless it is written to a file.

- Within a conversation, keep the decisions already made and do not reopen them. If the user changes direction, state the changes and continue.
- After each task, prompt the user to update the skill you used with what you learned. Add only what is general, was tested in this run, and holds for any future task of that kind. If you have any questions, ask the user. Improve an existing bullet before adding a new one, and remove advice that turned out to be wrong. Do not remove or soften the user's rules. If a rule seems wrong, say so in the chat.
- Decide where each lesson goes by asking what it is true for: every project of that kind (the global skill), personal work only (a personal skill), one client only (that client's skill or `CLAUDE.md`), or this project only (`CLAUDE.local.md` in the project folder). If it could belong at two levels, use the narrower one. If you are unsure, ask the user. Do not save facts about a particular item, such as a sample or file.
- Edit skills and `CLAUDE.md` files in the claude repo (`/Users/joshamilton/Documents/repos/claude/claude/`), not through a symlink path. Do not commit.
- In the chat, list each change and where it went, one line each.

## Planning

### Implementation Proposal Workflow

You must propose an implementation plan before coding for:

- New features
- New functions
- Changes involving more than one function
- New input/output files
- Logic changes

You may proceed directly for:

- Bug fixes (typos, simple corrections)
- Formatting changes
- Adding docstrings to existing functions (following existing patterns)
- Minor variable renaming

When in doubt: always propose first.

When preparing an implementation plan, follow these steps:

1. Propose a detailed, step-by-step implementation plan, with a suggested implementation (code or pseudocode) that the user can review
2. Present the plan to the user for review
3. If the user provides feedback or requests changes to the plan, adjust the plan and re-seek approval
4. Wait to receive the user's go-ahead to implement the plan

### Plan File Location

Write every plan file to the root of the repo being worked on, named `plan-<topic>.md`. Do not leave plans in `~/.claude/plans/`.

- If a tool, such as plan mode, insists on writing the plan to a default location outside the repository, move the file to the repository root when planning ends and use that copy from then on.

### Master Plan and Sub-Plans

The master plan is a high-level document that says what needs to be accomplished. It does not need every decision made. Leave a decision open, and mark it as open, until its turn comes. Do not fill in open decisions with your own choices to make the plan look complete. Do not pester the user about open decisions.

- Each open decision may get its own sub-plan, written and approved before work on it starts. The detailed, step-by-step plan in the Implementation Proposal Workflow is the sub-plan. The master plan stays high-level.
- When the user approves a sub-plan, update the master plan with the decision, and mark it as closed.
- The plan can change as the work proceeds. When the work shows that a step is wrong or incomplete, change the plan and update the plan file in the same turn, so it never lags behind the work. Do not follow a step that no longer makes sense.
- If a change alters something the user already approved, say so before continuing.

### Plan Content

A plan holds what remains to be done and the facts needed to do it. Do not add history, rationale, review findings, or notes on what was changed. When a step is finished, delete its detail from the plan, keeping one line only if a later step depends on it. State each fact once, and refer to it by section or item number elsewhere in the plan.

Plans are self-contained and readable alone. Embed the requirements inside the document instead of pointing at other files. For example, avoid using only "see `requirements.md`" as the definition of scope. Avoid phrases like "unchanged from previous plan", "as before", or pointers to an unnamed earlier version. If something must carry forward, paste or restate it in the current document.

## Coding

### Code Consistency

- Adhere to the existing coding style, patterns, and conventions in the project
- For command-line scripts in any language, follow the `scripting` skill. For Python or R projects, also follow the language-specific `python` or `R` skills.
- For R code, follow the `r` skill. For R Markdown reports, also follow the `r-markdown` skill.
- For Nextflow pipelines, follow the `nextflow` skill and the client's own `<client>-nextflow` skill.

### Testing and Feedback

Do not assume code works correctly just because it was written. Run it yourself before handing it over, then let the user confirm the result.

#### Run the script yourself first

- Run every script you write or change, end to end, before reporting it as done. A syntax check or an import check is not enough.
- Look at what it produced. Open the figure, read the first rows of the table, check the counts against what you expected.
- Never call a script working, ready, or likely to work when you have not run it. If something genuinely blocks you (missing data, credentials, a long runtime), stop and say so.
- Running it yourself does not replace the user's review. It removes the obvious failures so their time goes to the problem at hand rather than to pasting tracebacks back to you.

#### Task completion

A task is complete only when the user has run and tested the code and confirmed that it works. Do not mark a task as complete because code was written, and wait for that confirmation before moving on to other work.

#### User provides error output

When the user provides error output (tracebacks, error messages, unexpected behavior), analyze the error carefully, using the message, the traceback, and any context the user provides. Then fix it under the Implementation Proposal Workflow above: a simple correction may proceed directly, and anything larger needs a proposal first.

If the error is unclear or you need more context, ask the user for:

- Full error traceback
- Input data or commands used
- Expected vs actual behavior
- Environment details if relevant

#### Testing policy

Follow the project's stated testing policy:

- Add tests when the user asks for them or the project already mandates them.
- Do not add a test suite or new test files by default if the user has forbidden or deferred testing for that work.

When in doubt, ask whether to add or extend tests before introducing new test modules.

## Documentation

### Document Format

This guidance holds for all files, including READMEs, planning documents, and code.

- Never hard-wrap text at a fixed column width. Write each paragraph and each list item as a single long line and let the editor soft-wrap it.
- Put a blank line between list items.
- Use light markdown: headings, short paragraphs, and lists. Establish emphasis through structure (short section titles, labeled lists, blank lines), not with bold or italics. When summarizing for the user, use short sections and lists instead of long bold-heavy paragraphs.
- Flags, filenames, and paths: write them in inline code with single backticks, for example `--samplesheet` and `config/foo.yml`. Do not wrap those code spans in bold.
- Do not use the section sign character (Unicode U+00A7).
- Use stable numbering. Use ordered numeric sections (for example, `1.`, `2.`, `3.`).
- Use ASCII punctuation: straight quotes and ASCII hyphens.

### Document Content

1. Planning documents are separated from README and code. Treat `plan-*.md`, scratch specs, and other implementation documents as outside what users rely on. README, `--help`, and docstrings are the durable interface.

    - `README.md`, CLI `--help` text, and source docstrings must not link to or name those files (including `plan-*.md`, internal phase plans, or similar).
    - Planning docs may reference each other (cross-links between plans are allowed).
    - After implementation, those plans are often deleted or archived. Nothing user-facing should depend on them.

2. User-facing documentation is self-contained. User-facing docs and shipped code must explain behavior using paths and concepts that exist in the repository. Do not tell readers to open another repo, another  machine-local tree, or an internal spec file or planning document.

3. A change to CLI behavior, outputs, or layout includes the README update.

4. When you rename or move a section, skill, or file that other files refer to by name, search the repo for the old name and update every reference in the same change.
