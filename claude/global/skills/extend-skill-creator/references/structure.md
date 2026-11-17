# Skill structure rules

## Where content belongs

1. A guideline lives in one skill only. If it is true for every project of a kind, it goes in the most general skill (the `global` folder). When two skills would repeat a guideline, move it to the one skill that both can cite.

2. A language skill holds only what is specific to that language. What Python and R share (project layout, naming, flags, logging, exit codes, plots, data files) lives in the general `scripting` skill, and the `python` and `r` skills cite it.

3. A client skill holds only facts that belong to that client alone: identity values, names, and checklists that only that client needs. Anything generic moves up to a global skill.

4. A skill may cite other skills, and a section of the global `CLAUDE.md` by name (for example "Voice and Style"). Cite instead of restating.

5. A skill that extends an Anthropic skill says so, for example "This skill extends the guidance in the Anthropic skill named `docx`".

## Files and file names

1. A skill folder holds `SKILL.md`, then:

    - `references/` for documentation that Claude reads when needed

    - `assets/` for templates

    A skill folder has no `README.md`.

2. Files with the same role have the same name in every skill:

    - `references/setup.md`: initial setup

    - `references/coding.md`: code conventions

    - `references/workflow.md`: how to perform a task

    Other files are named for their topic.

3. `SKILL.md` stays under 500 lines. Put details that are rarely needed in a file in `references/`, and say in `SKILL.md` when to read each file. Put template files in `assets/`.

4. A skill name must not clash with another skill, including the Anthropic skills. Prepend the client (for example `<client>-python`) or a short description (for example `extend-docx` extends the Anthropic `docx` skill).

## Descriptions

Claude sees every description in every session and decides from it whether to load the skill, so a description should be short and clear.

1. A description is written in the third person and starts with "Use when ...".

2. The format is: [When to use it] + [What it does] + [Key capabilities].

3. Name the key case first, then every other case that should load the skill: one trigger for each real case, in the words a user would say, with file types where they apply. Give the capabilities as one short clause.

4. A general skill (`data-analysis`, `extend-xlsx`, `project-setup`, `python`, `csv-files`, `readme`) mentions both personal and client work where both apply.

5. A client skill names the client and the kind of project in its description (for example "Use when working in a [client] Nextflow pipeline"), so that it loads next to the general skill. Its body holds only what is specific to that client.

## Parallel structure for related skills

Related skills, such as `python` and `r`, are built to match, so that a reader finds the same thing in the same place.

1. The same role has the same file name (see "Files and file names").

2. Sibling files have the same headings in the same order. When you add a section to one, add the matching section to the other, or say why only one has it.

3. Each section opens the same way and has the same kind of numbered rule list at the same depth. For example, the opening line is: Follow the section "Command-line flags" in the `scripting` skill, and these Python details. Numbered rules come next.

4. Full code examples live in one place: the templates in `references/setup.md`. A section of `coding.md` points to the function in the template (for example "See `parse_arguments()` in the script template in `references/setup.md`"). Keep a short example in `coding.md` only where the template does not show the pattern, such as a plot or reading a table.

5. The same rule has the same wording in each sibling. A rule that is identical in all siblings belongs in the general skill instead.

6. Where a tool differs, say so in the section where it matters. For example, `argparse` exits with status 2 by itself, but `optparse` exits with status 1, so the R skill needs extra code.

7. Sibling templates behave the same: the same sections, the same exit codes, and the same log line format.
