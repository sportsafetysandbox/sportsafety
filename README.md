# Sport Safety Portal

An organisation-agnostic portal of guidance, standards and free tools to manage safety in sport in Singapore.

**Published at:** https://sportsafetysandbox.github.io/sportsafety/

Built with [MkDocs Material](https://squidfunk.github.io/mkdocs-material/) and published with GitHub Pages.

## Repository layout

```
sportsafety/
├── docs/                     # all portal content (Markdown)
│   ├── index.md              # Home
│   ├── participants/  organisers/  operators/
│   ├── coaches-exercise-professionals/  organisations/
│   ├── topics/  toolkit/  standards/  learn/  help/
│   ├── emergency/            # When to Call 995 (linked from the alert bar)
│   ├── downloads/            # templates and checklists
│   └── assets/css/portal.css # colours and fonts
├── overrides/main.html       # alert bar and page status banner
├── tools/
│   ├── structure.py          # the site map: single source of truth for pages and nav
│   ├── build_skeleton.py     # generates placeholder pages, Site Map and mkdocs.yml nav
│   └── make_risk_template.py # builds the Risk Assessment Template (Excel)
├── mkdocs.base.yml           # site configuration (edit this, not mkdocs.yml)
├── mkdocs.yml                # GENERATED: base config + nav
├── requirements.txt
└── .github/workflows/deploy.yml
```

## Working locally

```bash
pip install -r requirements.txt
python tools/build_skeleton.py   # after changing tools/structure.py
mkdocs serve                     # preview at http://127.0.0.1:8000/sportsafety/
```

## Adding or changing pages

1. Add or move the page in `tools/structure.py` and run `python tools/build_skeleton.py`. This updates the nav, the Site Map and creates a placeholder if the page is new.
2. Write the content in the page's Markdown file and add `<!-- handwritten -->` near the top so the generator never overwrites it.
3. Set front matter `status: pilot` (or remove `status` once approved) and `last_reviewed`.
4. Follow [CONTRIBUTING.md](CONTRIBUTING.md) for writing and source rules.

## Publishing

Pushing to `main` runs `.github/workflows/deploy.yml`, which builds the site and publishes it to GitHub Pages. In the repository settings, set **Pages → Source** to **GitHub Actions**.

## Licensed material

Do **not** commit copies of Singapore Standards (for example SS 681) or other licensed documents to this repository. Cite them by title and clause, and link to their publisher.
