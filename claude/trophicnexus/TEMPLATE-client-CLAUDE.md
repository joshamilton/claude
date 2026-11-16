# [Client name] — client instructions

This file holds the facts about this client that are cheap to keep: the contact block, the cloud this client uses, and the Nextflow values for this client's projects are Nextflow pipelines (if applicable). Put longer conventions in a client skill.

## Contact block

Use this block in place of `[Contact block: see this client's CLAUDE.md]` wherever a template calls for it:

```
[Fill in: name/contact line this client's deliverables should use]
```

## [Client] cloud reference

Projects for a client can be in any language, and a client usually uses a single cloud. Give one row for each value that fills a placeholder in `aws.md` or `gcp.md` (in the `references/` folder of the `nextflow` skill), with that placeholder in the last column. Write "not recorded" for a value that is not known yet. Add one line saying which cloud the client does not use. Delete this section if the client uses no cloud.

| Field | Value | Placeholder |
| ----- | ----- | ----------- |
| [Fill in] | [Fill in] | |

## [Client] Nextflow reference

Keep this section only if any of this client's projects are Nextflow pipelines. Delete it otherwise. Give the values that fill the placeholders in "Placeholders for Nextflow files" in `references/setup.md` of the `nextflow` skill, with the placeholder in the last column. Write "not recorded" for a value that is not known yet.

| Field | Value | Placeholder |
| ----- | ----- | ----------- |
| `manifest.name` | [Fill in] | `[manifest-name]` |
| `.nf-core.yml` `template.org` | [Fill in] | `[org]` |
| `author` (`pipeline.yml`) | [Fill in] | `[author]` |
| GitHub hosting | [Fill in] | `[github-url]` |

## Client-specific overrides

[Note anything this client needs that differs from the rules in the global `CLAUDE.md` and the global skills. For example a different README copyright format, a specific conda channel policy, or naming conventions unique to this engagement. Delete this section if there are none.]
