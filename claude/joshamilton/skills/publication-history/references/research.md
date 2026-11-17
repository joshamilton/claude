# Research

How to find every edition of each volume, group them into print runs, and identify the cover designs. Do the steps in order.

## 1. Terms

- Edition: one version of the text from one publisher in one format. A new ISBN usually marks a new edition or format.

- Print run, or set: a publisher's uniform issue of a whole series in one format and one design, usually within a span of years and a recognizable ISBN block. This is what a collector means by a matched set.

- Printing: a later printing of the same edition. It keeps the ISBN.

- Cover state: the cover design a printing carries. Publishers often redesign covers on later printings without changing the ISBN, so one ISBN can carry two or more designs. This is the most common trap in this kind of work: an ISBN identifies a run but not necessarily a cover.

## 2. Build the edition list

- Start from what the user gives you (a list of ISBNs, links, a description of the covers). Treat it as a lead to verify, not as fact.

- OpenLibrary is the best first source. Its API needs no key and works with plain `requests` or `curl`:

    - Search for the work: `https://openlibrary.org/search.json?title=<title>&author=<surname>&fields=key,title,edition_count&limit=5`. Several works can match one title; the one with the largest `edition_count` is usually the right one.

    - List its editions: `https://openlibrary.org/works/<OL...W>/editions.json?limit=300`. Each entry has `publishers`, `publish_date`, `isbn_13`, `isbn_10`, and sometimes `physical_format` and `edition_name`. Filter on publisher. Some responses have no `entries` key, so guard for it.

    - Look up one ISBN: `https://openlibrary.org/isbn/<isbn13>.json` returns the edition record; its `key` gives the page to link, `https://openlibrary.org/books/<OL...M>`. A 404 means OpenLibrary does not have that ISBN.

    - The records are crowd-sourced. Dates are sometimes the original publication year, `physical_format` is often missing, and a record can mix up two printings. Cross-check anything you rely on.

- Goodreads fills the gaps, especially recent ISBNs that OpenLibrary lacks, and it is where cover variants show up (section 4). See section 5 for how to read it.

## 3. Tell the print runs apart

- Sort each publisher's editions by ISBN. A run usually occupies one or a few blocks of consecutive ISBNs issued over a span of years. A publisher can switch registrant prefix partway through one run, so a change of prefix does not by itself mean a new run. Check the design and dates.

- Rule out things that look like another run before you call them one, and leave them out of the summary: film or TV tie-ins, foreign-language editions, large-print editions, book-club editions, audio, and e-book ISBNs. E-book ISBNs often appear in catalogs with no format and with dates years after the print run; if no bookseller lists a paperback under them, treat them as e-books.

- When the user describes several "editions" by their covers, map each one to ISBNs before agreeing. Two of the user's editions may turn out to be two cover designs under the same ISBNs.

- Marketplace listings of "complete sets" are leads, not sources, and are never cited. They are weak evidence: sellers mix runs and covers, and often give no ISBN. Use the photo to see which designs exist, not to define a run.

## 4. Cover designs

- Download the cover images and look at them with the Read tool. Compare designs side by side: frame, type, where the author and title sit, series name, volume number. The same cover art can be used by different publishers, or by one publisher in two different frames, so describe the layout, not only the covert art.

- Goodreads lists cover variants as separate entries. An entry with no ISBN, the same publisher, and an editions-list note such as "Alternate cover" for a known ISBN is a second design under that ISBN. Entries imported from Amazon listings (they show an ASIN but no ISBN) often keep the earlier design of an ISBN that was later reprinted in a new design. Match such an entry to an ISBN by its date, publisher and format, and say in the summary that the match is by those details, not by ISBN.

- A Goodreads record's cover image can belong to a different book than its ISBN. Check each cover against the title before you describe it, and if they differ, say so and leave that ISBN out of the cover section.

- Retailer and bookstore stock images are one per ISBN and can show either design. Do not use them to assign a design to an ISBN; at most, a mix of designs among a run's stock images confirms that both designs circulate.

- Internet Archive scans show the cover of a real copy, not a stock image, so they can assign a design to an ISBN when catalogs show only the current design. Find items with `https://archive.org/advancedsearch.php?q=title:(<words>) AND creator:(<surname>)&fl[]=identifier&fl[]=isbn&fl[]=date&rows=50&output=json`; an item named `isbn_<isbn13>` is filed under that ISBN. The public cover thumbnail (180 px wide) is at `https://archive.org/services/img/<identifier>`, and `https://archive.org/metadata/<identifier>/metadata` gives the catalog data. Page images of lending items are restricted; do not try to fetch them. Cite the item page, `https://archive.org/details/<identifier>`. Keyword and ISBN searches can return nothing for titles that have items; an identifier prefix search such as `identifier:problemofslaver*` found them. An item's ISBN list is often a merged catalog record that holds the hardcover, UK and US ISBNs together, so it does not say which copy was scanned. Identify the copy from what its cover shows, such as the publisher logo or a review quote printed in only one country's edition.

- Dating a redesign: if a volume first published in year Y exists in both designs, the redesign came after Y. Internal differences between two printings under one ISBN (a reset text, a new blurb) can narrow the date further, but they are text details and out of scope (`references/report.md`, section 1). Use them for dating only if the user asks.

- A publisher's announcement of a redesign (on its site or on social media) dates the start of a new run. These turn up in WebSearch results.

## 5. Web sources: what works

- WebFetch hands the page to a small model and returns its summary. That summary can drop table rows or misstate what the page says. For anything you will cite or base a claim on, read the raw page text with a browser (below) and quote it.

- Pages that load without JavaScript work with WebFetch. Many book sites do not, and some block it. Use Playwright with Chromium and a desktop user agent for those:

    ```python
  from playwright.sync_api import sync_playwright
  UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
  with sync_playwright() as p:
      browser = p.chromium.launch(headless=True)
      page = browser.new_context(user_agent=UA).new_page()
      page.goto(url, wait_until="domcontentloaded", timeout=45000)
      page.wait_for_timeout(3000)
      text = page.locator("body").inner_text()
      html = page.content()
      browser.close()
    ```

- Goodreads. WebFetch returns an empty page, and curl gets HTTP 202 (a bot check), so check Goodreads links with Playwright, not curl. Playwright works.

    - `https://www.goodreads.com/book/isbn/<isbn13>` redirects to that edition's book page. This is the reliable way to find a Goodreads record from an ISBN; the site search page did not return usable data.

    - The book page HTML embeds the edition data as JSON. Pull `"isbn13"`, `"publisher"`, `"format"` and `"numPages"` with a regular expression such as `'"isbn13":\s*("?[^,}]*"?)'`. `"publicationTime"` is in milliseconds since 1970 and is often the work's first publication date, not the edition's, so do not trust it.

    - The cover image is the first `img` whose `src` contains `books/` (on `m.media-amazon.com`).

    - The page HTML contains `/work/editions/<id>`. The editions list, `https://www.goodreads.com/work/editions/<id>?per_page=100&filter_by_format=Paperback&sort=year`, shows each edition's date, publisher, format and notes such as "Alternate cover", "Movie Tie-in" or "7th Printing".

    - On the editions list, each edition's ISBN-13 is printed on the line labeled `ISBN:` (the ISBN-10 follows in parentheses), not on an `ISBN13:` line. Match `ISBN:\s*(97[89]\d{10})`. The ISBN lines sit in a collapsed details block that `inner_text` of the page body leaves out, so read the page HTML (`page.content()`), split it on `class="editionData"`, strip the tags in each block, and match there.

- Penguin UK (`penguin.co.uk`, which covers Bantam and other Transworld imprints). Its site search does not work for ISBNs, so find the product URL with WebSearch first (the form is `/books/<id>/<slug>/<isbn13>`). Load it with Playwright and read the page HTML; the visible page text shows no publication date. The HTML embeds the format, the publication date as `"publishDate":"YYYY-MM-DD"`, the imprint, page count, trim size as `"trimSize"`, and the list of formats in print (`"editions":[...]`). This is a publisher source for the A or B format question: a trim of 197 x 129 mm was B format. Only titles in print are listed, so an ISBN missing from `"editions"` is out of print or was never a separate product. Cover images are at `https://cdn.penguin.co.uk/dam-assets/books/<isbn13>/<isbn13>-jacket-large.jpg`. The CDN returned HTTP 403 for out-of-print ISBNs (Allen Lane hardcovers) and served images only for titles in print; take covers of out-of-print editions from Goodreads or Internet Archive.

- Penguin Random House US (`penguinrandomhouse.com`). Find the product URL with WebSearch (the form is `/books/<id>/<slug>/<isbn13>/`). It loads with Playwright, and the page text gives the format and a line such as `Published on Jan 25, 2005 | 656 Pages`. Cover images are at `https://images.penguinrandomhouse.com/cover/<isbn13>`.

- eBay. WebFetch gets HTTP 403, and Playwright on `www.ebay.com` gets an error page. Playwright on `https://m.ebay.com/itm/<id>` works and shows the item specifics. Listing photos are at `https://i.ebayimg.com/images/g/<image id>/s-l1600.jpg`; the image ids appear in the page HTML.

- AbeBooks ISBN pages, `https://www.abebooks.com/<isbn13>/<slug>/plp`, work with WebFetch and give publisher, year and format. After a burst of page loads (about a dozen in a few minutes in one run) AbeBooks answers HTTP 429 "Too Many Requests" and keeps doing so for a while. Pace the loads, and do not cache a 429 page as if it were a result.

- Google Books API, with the key in `private/google-books-api-key.txt` (see `references/workflow.md`, section 1). Send the key in the header `x-goog-api-key`, not in the URL, so it cannot appear in an error message:

    ```python
  from pathlib import Path
  import requests
  key = Path("<this skill's folder>/private/google-books-api-key.txt").read_text().strip()
  params = {"q": "isbn:<isbn13>", "fields": "totalItems,items(id,volumeInfo(title,publisher,publishedDate,industryIdentifiers))"}
  try:
      r = requests.get("https://www.googleapis.com/books/v1/volumes", params=params, headers={"x-goog-api-key": key}, timeout=30)
      print(r.status_code)
  except requests.RequestException as e:
      print("request failed:", type(e).__name__)
    ```

    The record link to cite is `https://books.google.com/books?id=<id>`. Treat it as a catalog record: dates and publishers are sometimes wrong, so cross-check them like the OpenLibrary records. Coverage varies by publisher. Add `imageLinks` to `fields` to get the thumbnail, or download the cover directly from `https://books.google.com/books/content?id=<id>&printsec=frontcover&img=1&zoom=1`. It shows the current design only. For old university-press records, the `imageLinks` image can be a scan of the title page, not the cover. Look at it before treating it as a cover.

- Publisher websites are often built with JavaScript. One large publisher's ISBN pages returned "Page not found" to WebFetch while Playwright loaded only the title. Try Playwright, and do not conclude a book does not exist because its publisher page is empty.

    - Macmillan (US), which covers Henry Holt, Picador, Farrar Straus and Giroux, and St. Martin's. `us.macmillan.com` shows a Cloudflare bot check to Playwright and returns HTTP 403 to WebFetch. Do not try to get past the check. The academic site, `https://academic.macmillan.com/academictrade/<isbn13>/<slug>/`, loads with WebFetch and gives the format, imprint and on-sale date for one ISBN; take the slug from the `us.macmillan.com` URL that WebSearch returns (the form is `/books/<isbn13>/<slug>/`). Without the slug it returns HTTP 404. curl gets HTTP 403 from these pages; that is not a broken link. When the academic site has no page, use the catalogs.

    - Penguin Random House (US), `penguinrandomhouse.com`. Find book pages with the site search, `https://www.penguinrandomhouse.com/search/site?q=<words>`, and read the `/books/<id>/<slug>/` links from the page HTML. On the book page, the `"formatName"` and `"isbn"` fields give the formats the publisher still lists for that title; out-of-print formats are dropped. The format counts on the search page, such as "Paperback (1)", cover the whole results list, not one title; do not read them as evidence that a title exists in that format. A search for an ISBN that is out of print returns no results.

    - Oxford University Press (US). `https://global.oup.com/academic/search?q=<words>&cc=us&lang=en` loads with Playwright and lists every print format with its ISBN and publication date, which makes it a single publisher source for the whole edition list. Product pages are at `https://global.oup.com/academic/product/<slug>-<isbn13>`; some load with an empty body even after retries, so cite the search page instead. Cover images are at `https://global.oup.com/academic/covers/pdp/<isbn13>` and show the current design only. curl gets HTTP 202 from these pages; that is not a broken link. Cover URLs return HTTP 403 to curl. A Playwright request (`context.request.get`) after loading an Oxford page worked for one ISBN, but returned 404 for a 1988 title, so older titles may have no cover there.

- Fan bibliographies and collector sites can hold the most detailed edition tables available. Read them in full with Playwright before citing them, since a summary can invert what they say. Use them as leads only and do not cite them. Confirm each claim in an official source (`references/report.md`, section 4).

- Some sites time out under repeated automated loads. Retry once, add a short delay between pages, and cache what you have fetched to a JSON file in the scratchpad so a long run can resume.

- WorldCat (search.worldcat.org) is the one catalog that records physical size, but Cloudflare rate-limits it after about ten page loads from one address and then returns "Error 1015" for a long time; the ISBN URL redirects to a results list, so each record needs a second load. Budget for it, pace at 10 seconds or more per load, and do it before anything else that day, or do without it. In the second run it was lost twice and no size for the US editions could be found.

- OpenLibrary notes: `https://openlibrary.org/isbn/<isbn13>.json` redirects, so use `curl -L`. OpenLibrary has outages: in the second run it refused TCP connections (curl exit 7, "Connection refused") for more than half an hour late in the session, from this machine and from WebFetch's address alike, so it was the site and not a block on this address. Fetch each record once and cache it, and verify links as you go rather than in one burst at the end; a record key returned by the OpenLibrary API earlier in the session is a real record even if the final check cannot reach it. WebFetch is a useful second vantage point to tell an outage from a block. An edition title such as "Kellanved's Reach EXPORT" is a hint that an extra UK ISBN is an export edition.

- Fandom wikis return HTTP 402 to WebFetch; Playwright works. Read `body` text rather than guessing a content container, which timed out.

- Build cover contact sheets with Pillow: paste the covers into a grid, six 240 px columns wide, and label each with the title, ISBN and source, so the sheet reads well with the Read tool. If the labels are awkward in Pillow, build an HTML grid of `file://` images with captions and screenshot it with Playwright `full_page=True` on a 1500 px viewport. Compute an MD5 per downloaded image first: identical files from one source are a fallback image, not evidence that two ISBNs share a cover.
