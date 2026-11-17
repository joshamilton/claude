# Skill workflow

## Creating or revising a skill

1. Before writing a rule, decide where it belongs: every project of a kind (a global skill), one language or tool (its skill), one client (that client's skill or `CLAUDE.md`), or one project (`CLAUDE.local.md`). See "Where content belongs" in `references/structure.md`.

2. Search the existing skills for the rule first, and cite it instead of restating it.

3. When the skill has siblings, read a sibling first and match its headings and rule lists.

4. Propose the plan before writing: a new skill is a new set of files, so the Implementation Proposal Workflow in the global `CLAUDE.md` applies. Wait for the go-ahead.

5. Write `SKILL.md` and its description, then the reference files and the assets.

6. Edit the skills in the claude repo, not through a symlink path, and do not commit (see "Context and Learning" in the global `CLAUDE.md`).

## Where this repo differs from skill-creator

- Descriptions: `skill-creator` advises a description that is a little pushy. Keep the "Use when" format, and name the contexts that should load the skill, but do not stretch the description to cover unrelated work.

- Test cases: do not add `evals/` folders or run the benchmark loop unless the user asks (see "Testing policy" in the global `CLAUDE.md`). When the user asks, put the workspace outside the repo (for example `/tmp/<skill-name>-workspace`), not beside the skill.

- Words: write for scientists, not software engineers, as "Voice and Style" in the global `CLAUDE.md` says. Skip software slang and explain an idea in a short everyday phrase.

- Formatting: follow "Document Format" in the global `CLAUDE.md`: no bold or italics for emphasis, a blank line between list items, no hard wrapping, and ASCII punctuation.

## Checks before reporting a skill done

1. Run every template and code example in the skill, end to end, and look at what it produced. Run sibling templates in the same way, and check that they behave the same (exit codes, log line format).

2. Compare sibling files heading by heading, for example with `grep "^## "` on each file.

3. Check the front matter: `name` matches the folder.

4. Check the description against "Descriptions" in `references/structure.md`: it is in the third person, starts with "Use when", follows the order when, what, capabilities, names the key case first, has one trigger for each real case, gives the capabilities as one short clause, is under 1,024 characters (count them), and has no `<` or `>` characters. For a general skill, check that it mentions both personal and client work where both apply.

5. Check the folder: `SKILL.md` is under 500 lines, the files with a standard role have the standard names, and there is no `README.md`.

6. Search the repo for the old name after a rename or a move, and fix every reference in the same change, including the `README.md`, `plan-*.md`, and other skills.

7. Check that the code fences in each file are balanced.

8. Tell the user which files changed. Do not call the task complete until the user confirms it.
