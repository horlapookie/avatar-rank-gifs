# Avatar Rank GIFs

69 separate five-second animated GIF files for Avatar's season division system: **35 rank badges + 34 adjacent promotions**.

## Preview

| Rookie I | Rookie I → Rookie II | Rookie V → Veteran I |
| --- | --- | --- |
| ![Rookie I](gifs/rookie-I.gif) | ![Rookie I to Rookie II](gifs/rookie-I-to-rookie-II.gif) | ![Rookie V to Veteran I](gifs/rookie-V-to-veteran-I.gif) |

## Divisions

Rookie, Veteran, Elite, Pro, Master, Grandmaster, Legendary — each has divisions **I, II, III, IV, V**. Division I shows **one star**, II two, III three, IV four, V five. Promotion to the next family resets the stars to one.

These match the season divisions verified in Avatar's `data/seasonRank.js`. Emblems: bronze/silver/gold medals, diamond, crossed swords, star and crown. Original motion graphics inspired by competitive game rank-up celebrations; no copied game assets.

## Files

All GIFs are individual files under [`gifs/`](gifs/), not rows or contact sheets.

- Rank: `gifs/rookie-I.gif` through `gifs/legendary-V.gif`.
- Promotion: `gifs/rookie-I-to-rookie-II.gif`, `gifs/rookie-V-to-veteran-I.gif`, and every other adjacent step through `gifs/legendary-IV-to-legendary-V.gif`.
- [`gifs/manifest.json`](gifs/manifest.json) lists every filename, destination rank, source rank, stars and duration.
- Each GIF is **320 × 320**, **50 frames at 10 fps**, **exactly 5 seconds**, looping indefinitely, on a dark background.
- Promotion clips charge the previous badge, flash, reveal the new badge, then display **RANK UP!** and the destination stars.

## Use in Avatar

```js
const rankGif = 'https://raw.githubusercontent.com/horlapookie/avatar-rank-gifs/main/gifs/rookie-I.gif';
const promotionGif = 'https://raw.githubusercontent.com/horlapookie/avatar-rank-gifs/main/gifs/rookie-I-to-rookie-II.gif';
```

## Regenerate

The included generator is reproducible. On Linux with DejaVu Sans installed:

```sh
python -m pip install Pillow==12.1.1
python tools/generate.py
```

It validates all 69 filenames, individual files, dimensions, frame counts, looping and five-second durations. The manually-triggered GitHub Actions workflow generates the same files and saves them to this public repository via the GitHub REST API. No database is used.
