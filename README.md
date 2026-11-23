# Artist portfolio

Static site for GitHub Pages. No frameworks — `build.py` scans the content folders and writes
`manifest.json`, which the pages read.

## Adding content

```
site.json                 name, tagline, email, links
about/bio.txt             bio (blank line = new paragraph)
about/portrait.jpg        portrait (any image format)
overview.txt              images for the swipeable home overview, one per line
projects/
  01-night-walks/         one folder per project → its own page
    description.txt       optional project text
    01.jpg                photos (jpg, png, webp, gif, avif)
    01.txt                optional caption for 01.jpg (same name, .txt)
```

- **New photo:** drop it into a project folder. Add `<same-name>.txt` for a caption.
- **New project:** create a new folder in `projects/`. The title comes from the folder name:
  `03-red-room` → "Red Room". The leading number only sets the order.
- **Order** is alphabetical by file / folder name, so prefix with numbers (`01-`, `02-`, …).
- **Overview:** list paths relative to `projects/` in `overview.txt`, e.g. `01-night-walks/03.jpg`.
- **CV:** edit `cv.txt`. `# Heading` starts a section; each entry is `year`, then a tab
  (or two spaces), then the text, e.g. `2019	Solo show, Gallery X, Berlin`. A line with no
  year is fine too. Sections with no entries are hidden until filled in.
- **News:** one `.txt` file per article in `news/`, plus an optional image with the same
  name as the thumbnail (e.g. `news/2014-weisse-rose-mut.txt` + `.jpg`). Start the file name
  with the year so the newest sorts first. File format:
  ```
  date: 2014
  title: Article title
  source: Publication, page
  link: https://link-to-article

  Text shown under the thumbnail (after one blank line).
  ```
  The News section and menu link appear once there is at least one entry.
- Resize photos before uploading (≈2500px on the long side is plenty) to keep the site fast.

Then commit and push — the site rebuilds automatically.

## Publishing on GitHub Pages (one-time)

1. Push this folder to a GitHub repo (branch `main`).
2. Repo **Settings → Pages → Source: GitHub Actions**.
3. Every push runs `.github/workflows/pages.yml`, which runs `build.py` and deploys.

## Local preview

```
python3 build.py && python3 -m http.server
```

Open http://localhost:8000.
