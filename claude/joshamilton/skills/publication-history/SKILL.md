---
name: publication-history
description: Use when the user asks to research the printing or publication history of a book or a series of books. Covers catalogue sources (OpenLibrary, Goodreads) and the stand-alone summary and PDF.
---

# Publication history

Research the print history of a book or series and hand the user a short, stand-alone summary with a PDF copy.

## Hard limits

- The summary covers three things only: print history, ISBNs, and cover designs. Do not add availability, prices, page counts, sizes, typesetting, or other details.

- Stay on the works and the print runs the user names (typically hardback and paperback formats). Research other editions only as far as needed to rule them out, then leave them out of the summary. Film and TV tie-ins, foreign-language editions, large print, and e-books are always out of scope (`references/report.md`, section 1).

- Cite official sources only: catalogues, publishers, and ISBN agencies. Marketplace listings, fan bibliographies, and wikis are leads, never citations (`references/report.md`, section 4).

- Verify every ISBN you report against a catalogue record, and link it to that record.

- Look at every cover image yourself before describing a design. Do not describe a cover from a page's text or from another agent's summary.

- The summary must read on its own. Do not refer to any external files, including spreadsheets, the scratchpad, or the image folder.

## How this skill interacts with the global instructions

This is research and writing, not code, so the global "propose a plan and wait for approval" step does not apply to the research or the summary. 

Start work when the request names the works and the print runs. Ask the user first only in the cases listed under "When to ask" in `references/workflow.md`, then work without waiting.

The global rule to wait for the user's confirmation still applies at the end. The summary is the hand-over, and the task is not finished until the user has reviewed it.

## Reference files

- `references/workflow.md` - read before starting and again before handing over. Covers the working environment (`publication-history`, from `assets/publication-history.yml`), when to ask the user, and the hand-over.

- `references/research.md` - read before starting the research. Covers the terms (edition, print run, printing, cover state), building the edition list from catalogues, telling print runs apart by ISBN block, identifying and dating cover designs, and which web sources work.

- `references/report.md` - read before starting and again before drafting. Covers the fixed scope, the default structure, the stand-alone rule, citations, style, and making and checking the PDF.

## Order of work

1. Read `references/workflow.md` and `references/report.md`.

2. Check that the `publication-history` environment exists. It it does not, create it from `assets/publication-history.yml`. Run all Python in it.

3. Confirm that the request names the works and the print runs. If it does not, ask the user (`references/workflow.md`, section 2).

4. Build the edition list for every volume from the catalogues (`references/research.md`).

5. Group the editions into print runs by publisher, format and ISBN block, and rule out anything that only looks like another run (`references/research.md`).

6. Download and look at the cover images for each run, and check whether any ISBN was printed under more than one design (`references/research.md`).

7. Write the summary, render the PDF, and look at every page (`references/report.md`).

8. Hand over in a short chat message and wait for the user's review (`references/workflow.md`).
