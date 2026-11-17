# Report

What the summary contains, how to cite, and how to make and check the PDF.

## 1. Scope

The summary covers three things only: print history, ISBNs, and cover designs, for the works and print runs the user named (the hardcover and paperback formats the user listed).

Out of scope, always:

- Film and TV tie-ins, foreign-language editions, large print, e-books, audio books, and book-club editions.

- Availability, prices, and where copies can be bought.

- Page counts, physical sizes, and typesetting.

- Any other edition or detail the user did not name.

Do not ask whether to include these. Add one only when the user asks for it in this run.

Sources are fixed too: cite official sources only (section 4). Do not ask which kinds of sources to cite.

## 2. Default structure

Numbered sections, in this order, unless the user asks for something else:

1. Print history. One short paragraph per print run: publisher, format, the years the run was issued, how many volumes, and which volumes were never issued in that run. One sentence on the ISBN blocks.

2. ISBNs. One table for all runs (one table per series when the summary covers several series): volume number, title, then one column per run. ISBN-13 with hyphens. Each ISBN is a link to its catalog record (the OpenLibrary edition record, or the Goodreads record when OpenLibrary lacks it). Write "none" where a run has no such volume. One sentence above the table says what the links point to.

3. Cover designs, one section per run. Describe each design in one or two sentences (layout, type, where author and title sit), say when it was used as far as the evidence supports, and show two examples, usually the first and last volume, side by side with short captions.

4. The cover problem, when there is one. Say plainly that one ISBN was printed under more than one design, that catalogs, booksellers and the ISBN do not distinguish them, and what that means for assembling a matched set. Keep it to a few sentences.

5. Sources. Short labeled lists: ISBNs and dates, then cover designs. See section 4.

## 3. The summary stands alone

- The summary must read on its own after it is moved elsewhere and the working files are deleted. Do not refer to the user's spreadsheet, the repo, the scratchpad, or the image folder.

## 4. Citations

- Cite official sources only: library and book catalogs (OpenLibrary edition and work pages, Goodreads book and editions pages, WorldCat, national library catalogs, Internet Archive item pages), the publisher's own pages (book pages, catalogs, announcements of a redesign), and the ISBN agency records.

- Never cite marketplace listings (eBay, AbeBooks, Amazon and similar), fan bibliographies, collector sites, wikis, or forums. They are leads. Confirm each claim in an official source before you report it. If you cannot, leave the claim out and say so in the hand-over.

- For each cover image, cite the official page it came from (a catalog or publisher page). If an image was seen only on a marketplace listing, do not use it as the cited example; find the same design on an official page, or leave it out.

- Check every link before handing over. A catalog record that does not exist is worse than no link.

## 5. Style

- Follow the global writing rules: plain words, short sentences, light markdown, ASCII punctuation, each paragraph and list item on one line, a blank line between list items, numbered sections.

- State each claim at the strength the evidence supports. "Probably" needs a reason the reader can see; if the reason is not in the summary, drop the claim or the "probably".

## 6. Images and the PDF

- Save cover images in a working folder next to the summary, for example `summary-images/`, with descriptive names such as `<run>-<design>-cover-<title>.jpg`. Embed them in the markdown by relative path. Do not name the folder in the text, since the user may delete it once the PDF is final.

- Making the PDF. Run `pandoc` from the folder that holds the markdown and the images, so the relative image paths resolve, in the `publication-history` environment: `mamba run -n publication-history pandoc summary.md --pdf-engine=tectonic -V geometry:margin=1in -V colorlinks=true -o summary.pdf`. The first build downloads LaTeX packages and took about 85 seconds; later builds took about 1 second. It needs network access the first time. `tectonic` prints warnings about absolute paths and `.bb` files; the PDF was still correct.

- For two covers side by side with captions: use a two-column markdown table with the images in the first row and the captions in the second, with the height set on each image. Do not use raw LaTeX; `\input` and relative image paths fail because pandoc builds the PDF in a temporary folder.

    ```
    | ![](summary-images/a.jpg){height=3.4in} | ![](summary-images/b.jpg){height=3.4in} |
    |:---:|:---:|
    | Run A, volume 1 | Run A, volume 9 |
    ```

- Open the PDF with the Read tool and look at every page: the table, the image pairs and captions, the links, and any page left nearly empty. Fix and regenerate before handing over.

- Full-size scans make the PDF a few megabytes. Mention the size if it is over about 5 MB and offer to shrink it by saving smaller copies of the images with Pillow. `pypdf` reports the page count and the file size.
