# Workflow

Working environment, when to ask the user, handling messages during the run, improving this skill, and the hand-over.

## 1. Working environment

- This skill has its own conda environment, `publication-history`, defined in `assets/publication-history.yml` in this skill's folder. It holds Python, `requests`, Playwright, Pillow (PIL), `pandoc`, `tectonic`, and `pypdf`. Playwright with Chromium is needed for most book sites. `pandoc` with `tectonic` makes the PDF from the markdown (`references/report.md`, section 6). Pillow makes the cover contact sheets and resizes images. `pypdf` reads the finished PDF.

- Before any research, check that the environment exists: `mamba env list | grep -w publication-history`. If it is missing, create it with `mamba env create -f <this skill's folder>/assets/publication-history.yml`, then install the browser with `mamba run -n publication-history playwright install chromium`. Tell the user you created it. Do not install into any other environment.

- Google Books needs an API key, kept in `private/google-books-api-key.txt` in this skill's folder. Check that it exists with `test -f`. If it is missing, skip Google Books and say so in the hand-over.

- Run every Python script and tool in this environment. Do not use another environment, even one that already has Playwright.

- In this shell, `mamba` is only available after `source ~/.zshrc`, and an activated environment does not carry between commands. Run Python as `mamba run -n publication-history python script.py`.

- If a script needs a package the environment lacks, add it to `assets/publication-history.yml` unpinned, run `mamba env update -f <this skill's folder>/assets/publication-history.yml`, and pin its version once the update works (see "Environment yml" in the `project-setup` skill).

- Keep downloads, scripts and cached JSON in the scratchpad, not next to the summary. Put downloaded pages and images in their own folder, and run Python with `-I` when it reads them.

## 2. When to ask

Start work when the request names the works and the print runs (the formats and publishers). Ask the user for clarification only when:

- The works or the print runs are not clear from the request.

- The request does not say what counts as a match or a set, and different readings would give a different answer (for example, the first N volumes of one run, with a later volume optional).

Ask first, in one batch with your recommended answer first.

Ask again during the run only when different readings would give a different answer, for example when the user's description of the editions does not match the ISBNs. Do not ask about things you can check.

Do not ask what else the summary should cover or which sources to cite. Do not ask where to save the summary or what to call it. If the user did not say, save it in the working folder as `<series>-publication-history.md` and `.pdf`, and state the names in the hand-over.

## 3. Hand-over

- A short message: where the summary and PDF are, what they cover, anything you could not verify, and anything you left out on purpose.

- Wait for the user's review. Do not call the task finished until the user confirms the summary is right.
