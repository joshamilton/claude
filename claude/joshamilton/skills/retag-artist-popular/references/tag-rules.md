# Tag rules

Steps 8 and 10 of `SKILL.md`: these rules decide the tag values. Apply them to every track in the artist folder.

## 1. Terms

- Contemporaneous album: new material released while the artist was active, soon after it was recorded.

- Posthumous album: released after the artist died or the band broke up, or drawn from the vaults: recordings released many years after they were made.

- If it is not obvious which one an album is, ask.

- Single-artist album and multi-artist album: see section 2. "Multi-artist" describes the tags only; it is not the `Compilation` grouping folder.

## 2. ALBUMARTIST: single-artist or multi-artist album

- Single-artist album: every track's ARTIST is exactly the artist folder name. Then no track has an ALBUMARTIST; remove it if present.

- Multi-artist album: any track's ARTIST differs from the artist folder name (another band, a guest, a side project, an accompanying group). Then every track on that album gets ALBUMARTIST set to exactly the artist folder name, including the tracks whose ARTIST already matches it.

- Never use "Various Artists".

## 3. ARTIST: whose recording is it

- Credit the artist that made each recording, track by track, as the original release credited it. On a career box set or anthology this may be the band the artist was a member of, not the artist themself.

- On a studio or live album, every track takes the album's billing.

- Guests and accompaniment are split into a semicolon list: featured singers, "with", "w/", "acc. by", "featuring".

    - Example: "Jane Doe acc. by Joe Smith and His Orchestra" becomes `Smith, Joe Orchestra; Doe, Jane` (sorted alphabetically).

    - Example: "Jane Doe with The Maple Street Band" becomes `Doe, Jane; Maple Street Band, The`.

    - A band whose name contains a leader's name stays one name: `Smith, Joe Orchestra`, `Smith, Joe Trio`.

    - When the artist played as a member of a band, the track is credited to the band: a track credited to "<Artist> as member of <Band>" gives `<Band>`.

    - A conductor billed with a featured orchestra is added with the orchestra: "Jane Doe featuring the Maple Street Orchestra, conducted by Joe Smith" becomes `Doe, Jane; Maple Street Orchestra; Smith, Joe`.

- Guests are listed only when they are not members of the artist's band.

    - Featured singers and featured players both count as guests (`Doe, Jane` on a `<band>` track).

    - Band members are never added, even when the release bills them per track: a track billed "with <member>" is just the band.

    - Check membership against the band's Wikipedia page (current and previous members) and ask when you cannot tell.

    - A non-member lead vocalist credited only in the liner notes is added too; backing vocalists are not.

- A second performer named in the track titles or another source (e.g., a duet singer) is added to the list.

- Spoken introductions and concert announcements take the name of the announcer, when known. When the announcer is not known, use the artist.

- When two sources (for example two different reissues of the same session in this folder) credit the same recording under different names, each album keeps the credit its own booklet uses.

- When an album's own booklet gives no billing for a session, or an ambiguous one ("Quintet/Quartet" over five tracks), take each track's credit from the label of its original release (the single or first album), found on Discogs.

## 4. ARTIST: name style

- A real personal name is written `Last, First`: `Doe, Jane`. Suffixes follow the name: `Smith, Joe, Jr`.

- A leader's name inside a band name is inverted the same way. A possessive keeps its apostrophe on the inverted name: `Smith, Joe's All Stars`. With a leading article, the article goes to the end: "The Joe Smith Band" becomes `Smith, Joe Band, The`.

- A leader billed with a backing band ("<name> & The <band>", "<name> and the <band>") is split into two: the artist and the band, semicolon delimited and sorted alphabetically. For example, "Jane Doe and the Maple Street Band" becomes `Doe, Jane; Maple Street Band`.

- A leading article is part of a band's name only when the band's Wikipedia article bolds it and capitalizes it mid-sentence. "<label> changed the name of the band to The Joe Smith Band" keeps the article (`Smith, Joe Band, The`); "Jane Doe and the Maple Street Band" does not (`Maple Street Band`).

- Drop "and His", "and Her", and "and Their" from band names.

    - "Joe Smith and His Orchestra" becomes `Smith, Joe Orchestra`.

    - "Jane Doe and Her Quartet" becomes `Doe, Jane Quartet`.

    - "Smith-Doe and Their Orchestra" becomes `Smith-Doe Orchestra`.

    - Apply this even when the catalog still holds an older "and His" spelling of the same artist, and list those artists in the report.

- Mononyms and stage names with a title stay as written: `<name>`, `Dr. <name>`.

- A stage name built like a personal name is inverted like one: "Joe Smith" becomes `Smith, Joe`.

- A stage name whose first word is an honorific is inverted the same way: "Duke Ellington" becomes `Ellington, Duke`, "Count Basie" becomes `Basie, Count`.

- Initials lose their periods, following the library: `Smith, AB`, `Smith, Joe A`.

- Non-Western names follow the order most English-language sources use for that person. If you are unsure which part is the family name, ask the user.

- A leading article moves to the end: `<band>, The`, `<band>, A`.

- Keep accents and other non-ASCII letters exactly as officially spelled.

- Write words in Title Case. Names on the `titlecase_exceptions` list in `/Users/joshamilton/Documents/repos/music-tagger/config/library-schema.yml` are kept exactly as written.

- A semicolon list uses `; ` between names and is sorted alphabetically: `Maple Street Band; Smith, Joe`.

- One artist gets one spelling across every album in the folder. Before writing, list all distinct proposed ARTIST values and check for near-duplicates (`All Stars` vs `All-Stars`, `&` vs `and`). When sources spell a band name differently over time, ask. An ensemble credited under a different name than an artist already in the library keeps the name this release credits.

## 5. DATE

- DATE is a plain four-digit year.

- Contemporaneous studio albums and greatest-hits compilations: DATE is the year the album was first released (Wikipedia's release year), the same on every track. Do not research per-track years for these. A career retrospective, including a box set such as `<N> Years`, is a greatest-hits compilation.

- Posthumous albums and all live albums: DATE is the year each track was recorded. Tracks on one album can have different years. The rest of this section applies to them.

- Compilations and box sets of archival recordings take each track's recording year from its session, like a live album. If unsure which kind a compilation is, ask.

- A range (e.g., 1954-55) takes its first year.

- The album folder year is the earliest DATE; `standardize` renames the folder to match. The year in the folder name from `organize-artist-popular` is provisional.

## 6. ALBUM

- Every track of an album has the same ALBUM: the title of the original release.

- `:` and `/` are allowed. On disk, `standardize` writes `:` as ` -` and `/` as `_`.

- Write `and`, never `&`.

- Remove disc markers (`- CD 1`, `(Disc 1)`, `CD1`, `(Bonus)`), catalog numbers (`(<catalog number>)`), and `[Bonus Track]`.

- An edition is appended with `: `: `<album>: 1-Disc Edition`, `<album>: 2-Disc Edition`.

- A compilation (greatest hits, best-of, career box set) drops a leading article and the artist's name: "The Best of <N> Years" becomes `Best of <N> Years`, "<title>: The Best of <Artist> <year>-<year>" becomes `<title>: Best of <year>-<year>4`.

- A bonus disc with its own name becomes its own album, with that name as ALBUM (`references/standardize.md`, section 1).

## 7. GENRE

- One GENRE for every track in the artist folder: the value the user gave, from the `genres` list in `config/library-schema.yml`.

## 8. DISCNUMBER

- A multi-disc album is one whose album folder holds `Disc N` folders. Every track gets DISCNUMBER equal to the number in its folder name, as a bare number zero-padded to the width of the highest disc number (`1`, `2`; or `01` to `12` for twelve discs). Replace any existing value (`1/2`, `CD`, `CD 1`).

- A single-disc album has no `Disc N` folder. Remove DISCNUMBER from every track, including a value such as `CD`.

- If a disc folder is not named `Disc N`, do not guess: ask the user.

- `standardize` checks TRACKNUMBER and the file names; do not change TRACKNUMBER.

## 9. TITLE

- Missing or placeholder titles are filled. A placeholder is an empty TITLE or a generic name such as `Track01` or `Track 1`.

    - Take the titles from the release's own back cover or booklet (`Scans.pdf`) first. Use the Discogs release that matches the rip (same edition, same track lengths) only when there are no scans.

    - Keep the cover's wording, including subtitles (`<song> (<subtitle>)`).

    - Match titles to files by position only after the track count and lengths confirm the release.

    - Write the title in library title case with `titlecase_value()` from `/Users/joshamilton/Documents/repos/music-tagger/src/tag_normalize.py`. Do not lower-case the text first: that turns an initialism such as `BB` into `Bb`.

- Artist credits embedded in a title are removed, because ARTIST carries them.

    - Remove parenthetical text that starts with a credit word (the patterns are in `assets/title_keywords.yml`) or that only lists performers: "<song> (feat. <name>)" becomes "<song>", "<song> [with <band>]" becomes "<song>", "<song> [<name 1>, <name 2> & <name 3>]" becomes "<song>".

    - Parenthetical text can nest ("[with <name> (<band>)]", "(with <name> (nee <name>))"), so remove all of the outer piece.

    - Also remove a performer written before or after the title ("<name> / <song>", "<song> - <name>"). Check first that the other part is a performer, not a second song of a medley.

- Before removing a credit, make sure ARTIST has the guest (or that the guest is a band member, who is left out of ARTIST by section 3).

- All accessory information is removed: where the recording came from, which mix, edit, or master it is, live notes, bonus-track notes, alternate-take notes, reprise notes, and notes on how the track is played. `assets/title_fixes.py` proposes these removals from the patterns in `assets/title_keywords.yml`. When it misses one, add a pattern to that file. Two tracks with the same title on one album are fine.

- Keep a subtitle that is part of the song's name: "<song> (<subtitle>)", "<song> [<subtitle>]".

    - Check the song's Wikipedia article or the original release when unsure: "<song> (<subtitle>)" is the song's own name, so "<song> (<subtitle>) (<name> Remix)" becomes "<song> (<subtitle>)".

    - A credit word inside the title itself is not a credit ("<word> <word> with <word>").

    - When unsure whether a note is part of the name, ask.

- A part number becomes `, Part N`: "<song> (Part 1)" becomes "<song>, Part 1".

- A medley joins its songs with ` / `: "<song 1> - <song 2>" becomes "<song 1> / <song 2>".

- A spoken introduction is titled `Introduction to '<song>'`, and its ARTIST is the announcer (see section 3).

- Missing accents and umlauts are restored, spelled as on the release or Discogs: "Uber" becomes "Über", "Cafe" becomes "Café". Change only the letters; leave the capitalization as it is.

- One song gets one spelling across every album in the artist folder: the spelling on the original studio album. Before writing, list all distinct proposed titles and check for near-duplicates ("<song> (<subtitle>)" vs "<song> (<subtitle with one letter changed>)").

- Report typos you cannot settle from a source (`<word>` with one letter changed). `standardize` fixes capitalization.

## 10. Punctuation in ARTIST, ALBUM, and TITLE

- Use straight apostrophes (`'`), never curly ones (`’`, `‘`).

- An ellipsis is three periods with a space on each side: "<word>...<word>" becomes `<word> ... <word>`. This holds at the start or end of a value too: "...<title>" becomes ` ... <title>`, and "<title>..." becomes `<title> ... `. A single ellipsis character (`…`) becomes three periods.
