---
name: extend-skill-creator
description: Use when creating, editing, or reviewing a skill in the claude repo, alongside the Anthropic `skill-creator` skill, or when checking a skill before reporting it done. Adds the repo rules for where content belongs, file names, descriptions, and final checks.
---

# Extend skill-creator

This skill extends the guidance in the Anthropic skill named `skill-creator`. Use `skill-creator` for the process of drafting and improving a skill. Use this skill for the rules of this repo. Where the two disagree, this skill wins. It has two reference files:

- `references/structure.md`: read this when deciding what goes into which skill, which files a skill has, how to name and describe it, and how related skills line up. It covers:

    - where content belongs

    - files and file names

    - descriptions

    - parallel structure for related skills

- `references/workflow.md`: read this when creating or revising a skill. It covers:

    - the steps

    - where this repo differs from `skill-creator`

    - the checks to run before reporting a skill done

Both files assume the global standing instructions (`~/.claude/CLAUDE.md`) are already in effect: interaction style and documentation standards live there.
