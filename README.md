# FRAMEVERSE

An independent anime, comics and collecting culture website. Cinematic original visual concepts, convention listings, collector knowledge and editorial content in a fast, accessible, dependency-free web experience.

## Run locally

```bash
python3 -m http.server 8000
```

Open <http://localhost:8000>.

## Architecture

- `build.py`: deterministic static-site source and content definitions. Generates 24 HTML pages.
- `assets/site.css`: design system, layout, animations and responsive styles.
- `assets/site.js`: progressive enhancements: filtering, sorting, search, gallery lightbox, navigation, hero slider, contact workflow.
- `assets/*.webp`: original generated visual concept photography. All featured figure imagery is illustrative concept art, not manufacturer product photography.
- `assets/search-index.json`: generated site-wide search index.
- `tests/`: browser integration and structural checks.

Rebuild generated HTML and index after content edits with `python3 build.py`. Do not hand-edit generated HTML, because the generator is the source of truth.

## Publishing

Deploy the entire repository root as a static site to Vercel, Netlify or Cloudflare Pages; no build step or runtime service is needed. All pages are standalone `.html` files. Configure a custom domain when available; replace the placeholder sitemap URL in `build.py` before submitting it to search engines.

## Contact workflow

The contact form validates data and opens the visitor's email application with a populated message to the editorial inbox. It **does not claim** to transmit mail from the website. For a direct in-page submission endpoint, a verified mail service and server-side API would be required.

## Data and imagery

- Featured figure designs are original visual concept images and **not products for sale**.
- Convention dates and locations were checked against official organizer pages in November 2026; editorial entries link to sources. Revalidate before future publication.
- The site is not affiliated with LINXAI, event organizers, figure companies, or Japanese/American comics licensors.
- The site draws architectural inspiration from premium technology/product websites without copying their code, assets, trademarks or marketing text.

## Quality goals

- Standalone HTML documents and semantic structure
- Fully functioning client-side filters, responsive nav, lightbox, search and mailto
- Keyboard accessibility, focus styles, reduced-motion support
- Accessible external links with `noopener noreferrer`
- No mandatory client dependencies; no tracker by default

## Development workflow

Feature branches → incremental commits → pull request → checks/review → merge. CI definition in `.github/workflows/checks.yml`. Local Git history is real and should not be backdated to imply fictitious development.

## Notes

This release intentionally uses a static multi-page architecture rather than a larger React/Next.js bundle. The user experience is content-led and does not need server-rendered application state, so no-dependency distribution minimizes bugs, dependency and hosting costs. A CMS, payment service or membership system can be introduced later if business needs justify it.
