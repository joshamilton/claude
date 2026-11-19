# Research

Steps 4, 6, and 7 of `SKILL.md`: how to find the credited artist and the recording year for every track. Do the sections in order.

## 1. Inventory first

- List each album's folders and files. Dump every current tag of every FLAC (`metaflac --export-tags-to=- file.flac`) into a CSV in your scratchpad, before `cleanup` runs.

    - Keep `MUSICBRAINZ_ALBUMID`, `CATALOG`, `ISRC`, and `COMMENT` in the dump: they identify the exact release on Discogs or MusicBrainz, and `cleanup` removes them.

    - Expect the existing tags to be wrong.

- Read the rip logs (`.log` next to the files). The table of contents gives exact track lengths, which help match tracks to a booklet.

## 2. Liner notes (`Scans.pdf`, when present)

- Scans may sit in the album folder or in each disc folder. They are images with no text layer, so render them: `pdftoppm` and ImageMagick (`magick`, `montage`) are in the `music-tagger` environment.

- Page sizes vary wildly between PDFs, so render with `pdftoppm -scale-to 3400` rather than a fixed `-r` resolution.

- First build low-resolution contact sheets of all pages to find the track list, the credits or discography pages, and the tray card. Then render only those pages. Put `-label '%f'` before the input files in `montage` so each tile shows its page number.

- Check that every page belongs to this album. A `Scans.pdf` can hold pages of another release, left over from a merged folder. Report it.

- Archival box sets and reissues usually key each track to its source recording: a letter code, a heading per group of tracks, or a date column on the tray card. That gives you the credited artist and the date in one place.

- Some archival box sets give the artist and date per disc but not which tracks belong to each recording. Then:

    - Take the track ranges from the Discogs release `notes` (box sets often list "1-1 to 1-3: Recorded ...").

    - Check that each disc's recordings appear in the same order and that the counts add up to the disc's tracks.

    - Take the artist and date from the booklet. If the booklet and Discogs differ on a day but not the year, the year is safe.

- Some scans contain only cover art. Then the web is your only source.

## 3. The web

- Discogs is the user's usual first stop. Its web pages block WebFetch and curl (HTTP 403), but its public API works without a key. Call it with curl, send a User-Agent header, and save each response to a file in your scratchpad:

    - Search: `https://api.discogs.com/database/search?q=<artist+album>` returns releases and masters with their ids.

    - Release: `https://api.discogs.com/releases/<id>` returns the track list with durations, per-track credits (`extraartists`), and `notes`. On reissues and box sets the notes often give a recording date, place, and matrix number for every track.

    - Also useful: `https://api.discogs.com/masters/<id>/versions` and `https://api.discogs.com/artists/<id>/releases`.

    - Original singles and early releases: search by catalog number, `database/search?catno=<catalog number>&type=release` (add `&q=<artist>` for short numbers). The result title alone often shows the label credit per side; the release's per-track `artists` confirm it. Catalog numbers come from the discography page of a reissue's booklet.

    - Match Discogs tracks to the rip by title, not by position. A release can contain tracks the rip lacks, or split one file into two parts.

    - The API is rate-limited, so fetch only the releases you need.

- Search with WebSearch and read pages with WebFetch. AllMusic and RateYourMusic also block WebFetch (HTTP 403), but their pages often show up in search results, and the result summaries can still help.

- Pages that usually work: Wikipedia album pages (the "Recorded" field in the infobox), MusicBrainz, and label or artist websites. For jazz, jazzdiscography.com session lists and jazzdisco.org label catalogs also work.

- Prefer the release's own liner notes over the web, and a full discography over a single retailer listing. When sources disagree, say which you used and why.

## 4. Plan before writing

- For each album, build a per-track plan CSV in your scratchpad with these columns: disc folder, track number, file name, current ARTIST, current ALBUMARTIST, current DATE, current ALBUM, current DISCNUMBER, current TITLE, source or session, new ARTIST, new ALBUMARTIST, new DATE, new ALBUM, new GENRE, new DISCNUMBER, new TITLE, notes.

- Keep the mapping from tracks to recording sessions or sources in a small script, not typed by hand per row, so a correction to one session fixes every track from that session.

## 5. Tips for sources

- Rock and pop album pages on Wikipedia usually give studios and a release date but no per-track recording years. 

- Do not spend time hunting per-track years for contemporaneous studio albums or greatest-hits compilations; the release-year rule in `references/tag-rules.md` covers them.

- Credits: a single's own label credit on Discogs can differ from Wikipedia's discography table. Use the original release's credit and check it on Discogs (`database/search?q=<artist>+<title>&type=release`) when it matters.

- Guest credits on Discogs sit in two places: the track's own `artists` list (for example "<name> And His <band> With <name>") and the track's `extraartists` with role `Featuring` or `Vocals`. Read both. A leader's backing band often has its own Discogs artist page; `https://api.discogs.com/artists/<id>/releases` lists the band-billed releases, and `database/search?q=<band>&type=artist` finds the id.

- Check unfamiliar guest names from Discogs with a web search. Discogs can credit the wrong person for a name the release prints only in part.

- Before choosing a spelling, query the library catalog for each guest (`select distinct artist from tracks where artist like '%<surname>%'`). It shows house conventions the rules do not spell out, such as initials without periods (`<last name>, AB`).

- The Wikipedia API (`https://en.wikipedia.org/w/api.php?action=parse&prop=wikitext&format=json&page=<title>`) can return empty responses when called many times in a fast loop. Pause a few seconds between calls, or use WebFetch on the article instead.
