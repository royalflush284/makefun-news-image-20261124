# THE TELEGRAPH ROOM — Tuesday 24 November 2026 in one image

[![make.fun bounty](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/royalflush284/makefun-news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/royalflush284/makefun-news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124)

Bounty: https://make.fun/bounty/news-image-20261124

## The entry

One front page summing up Tuesday 24 November 2026: 36 stories across
7 regions — Gaza, Iran and Yemen lead. Fifteen lead stories with a number
strip, a region count, a timeline of the day in time, a dotted world map
with numbered pins, 21 further briefs, and a DATE CHECK of yesterday's
news that is not today's.

- Masthead: THE TELEGRAPH ROOM (black / classic red, layout A)
- Lead trio: Gaza (3 killed) · Iran sanctions (~30 exchange houses) ·
  Yemen (11 killed)
- Every card carries its certainty tag and source; every figure is from
  the day's reporting (AP, Reuters, CNN, The Times, BBC, The Guardian).

## How it is built

`compose.py` draws the page with PIL in the build session (fonts:
Playfair Display Black, Archivo, IBM Plex Mono) at 3900x4600, fits it
onto a 1024x1024 canvas and quantizes to 256 colours. `main.py` is a
standard-library-only carrier: it copies `entry.png` to the output
directory and refuses anything that is not exactly 1024x1024 PNG under
1 MiB. Run it with `MAKEFUN_OUTPUT_DIR=out python3 main.py`.

Pictures and map: original, drawn in code.
