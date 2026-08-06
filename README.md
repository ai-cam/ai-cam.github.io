# ai@cam Website

Source repository for [ai.cam.ac.uk](https://www.ai.cam.ac.uk) — the website of **ai@cam**, Cambridge University's flagship mission to develop AI for the benefit of science, citizens, and society.

## About the Site

ai@cam is a University of Cambridge initiative that connects research, policy, and practice around artificial intelligence. The website serves as the public-facing hub for:

- **Reports and policy briefs** — research outputs on topics including AI governance, data access, copyright, and regional AI development
- **Events** — workshops, conferences, and public dialogues
- **Projects** — funded initiatives and collaborations across the university
- **Calls** — open funding calls and collaboration opportunities
- **News and blog posts** — updates on AI@cam activities and commentary
- **People and teams** — profiles of researchers, staff, and affiliated contributors
- **Policies** — institutional positions and statements on AI-related topics

## Technology Stack

The site is built with [Jekyll](https://jekyllrb.com/) and hosted on GitHub Pages / Netlify. Content is managed through [Decap CMS](https://decapcms.org/) (formerly Netlify CMS), which provides a web-based editorial interface backed by Git.

Key components:

| Component | Purpose |
|-----------|---------|
| Jekyll | Static site generator |
| Decap CMS | Web-based content management (`/admin`) |
| Netlify | Hosting and deployment |
| GitHub Actions | CI/CD and automated PR workflows |

## Repository Structure

```
├── _blog_posts/       Blog articles
├── _calls/            Funding and collaboration calls
├── _events/           Events (past and upcoming)
├── _news/             News items
├── _pages/            Static pages (About, Contact, etc.)
├── _people/           Individual researcher and contributor profiles
├── _policies/         Policy statements and positions
├── _projects/         Project pages
├── _reports/          Reports and policy briefs
├── _team_members/     Staff and core team profiles
├── _layouts/          Jekyll layout templates
├── _includes/         Jekyll partials and components
├── _data/             Structured data files
├── assets/            CSS, JavaScript, images
├── admin/             Decap CMS configuration
├── backlog/           Task tracking (VibeSafe)
├── cip/               Code Improvement Plans (VibeSafe)
├── requirements/      Requirements documentation (VibeSafe)
└── tenets/            Project guiding principles (VibeSafe)
```

## Local Development

### Prerequisites

- Ruby 3.x
- Bundler (`gem install bundler`)
- Node.js (for any JS tooling)

### Running the Site Locally

```bash
# Install Ruby dependencies
bundle install

# Serve with live reload
bundle exec jekyll serve --livereload
```

The site will be available at `http://localhost:4000`.

### Running Tests

```bash
# Install Node dependencies (if needed)
npm install

# Run tests
npm test
```

## Adding Content

Most content lives in the collections under `_blog_posts/`, `_events/`, `_reports/`, etc. Each file is a Markdown document with YAML front matter. See existing files in those directories for the expected fields.

The Decap CMS admin interface at `/admin` provides a graphical alternative for editors who prefer not to edit files directly.

For branch protection and CMS workflow details, see [`DECAP_CMS_SETUP.md`](DECAP_CMS_SETUP.md).

## Project Management

This repository uses [VibeSafe](https://github.com/lawrennd/vibesafe) for structured project management. Run the status summary at any time:

```bash
./whats-next
```

This shows the current state of open tasks, CIPs, and recommended next steps.

## Contributing

Content contributions (reports, events, news, etc.) should go through a pull request to `main`. The Decap CMS is configured to push to a `cms-edits` branch, from which automated workflows create PRs for review.

For development changes, open a PR against `main` with a clear description of the change.
