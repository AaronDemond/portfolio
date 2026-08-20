# Enterprise Blue CSS Variable System — Implementation Reference

Below is a reference specification you can give directly to another coding agent. It explains not just what each variable contains, but **how the variable system is intended to control the visual language of the portfolio**.

The core design intent is: **compact, professional, enterprise-oriented, content-first, square-edged, restrained, and information-dense**.

# 1. Canonical variable set

This is the authoritative variable set the site should use.

```css
:root {
  /* =========================
     BRAND
     ========================= */

  --color-primary: #0a3d78;
  --color-primary-strong: #072e5e;
  --color-accent: #1e88e5;
  --color-accent-strong: #0a66c2;


  /* =========================
     SURFACES
     ========================= */

  --color-bg: #ffffff;
  --color-surface: #ffffff;
  --color-surface-alt: #f3f6fa;


  /* =========================
     TEXT
     ========================= */

  --color-text: #1f2937;
  --color-text-muted: #6b7280;
  --color-heading: #0f172a;
  --color-link: #1e88e5;


  /* =========================
     NAVIGATION
     ========================= */

  --color-nav-bg: #0f172a;
  --color-nav-text: #e5e7eb;
  --color-nav-active: #1e88e5;


  /* =========================
     BORDERS
     ========================= */

  --color-border: #d1d5db;
  --color-border-strong: #9ca3af;


  /* =========================
     STATUS
     ========================= */

  --color-success: #16a34a;
  --color-warning: #f59e0b;
  --color-error: #dc2626;


  /* =========================
     TYPOGRAPHY
     ========================= */

  --font-family-body:
    -apple-system,
    BlinkMacSystemFont,
    "Segoe UI",
    Roboto,
    Helvetica,
    Arial,
    sans-serif;

  --font-family-mono:
    "JetBrains Mono",
    "Cascadia Code",
    Consolas,
    monospace;

  --font-size-xs: 0.6875rem;   /* 11px */
  --font-size-sm: 0.75rem;     /* 12px */
  --font-size-md: 0.875rem;    /* 14px */
  --font-size-base: 1rem;      /* 16px */
  --font-size-lg: 1.125rem;    /* 18px */
  --font-size-xl: 1.375rem;    /* 22px */
  --font-size-2xl: 1.75rem;    /* 28px */

  --font-weight-normal: 400;
  --font-weight-medium: 500;
  --font-weight-semibold: 600;
  --font-weight-bold: 700;

  --line-height-tight: 1.25;
  --line-height-normal: 1.5;
  --line-height-relaxed: 1.65;


  /* =========================
     SPACING
     ========================= */

  --space-1: 0.25rem;   /* 4px */
  --space-2: 0.5rem;    /* 8px */
  --space-3: 0.75rem;   /* 12px */
  --space-4: 1rem;      /* 16px */
  --space-5: 1.25rem;   /* 20px */
  --space-6: 1.5rem;    /* 24px */
  --space-8: 2rem;      /* 32px */
  --space-10: 2.5rem;   /* 40px */


  /* =========================
     BORDERS / SHAPE
     ========================= */

  --border-width: 1px;
  --border-style: solid;

  --radius-none: 0;
  --radius-sm: 2px;


  /* =========================
     SHADOWS
     ========================= */

  --shadow-none: none;
  --shadow-sm: 0 1px 2px rgb(15 23 42 / 0.08);
  --shadow-md: 0 2px 5px rgb(15 23 42 / 0.10);


  /* =========================
     LAYOUT
     ========================= */

  --page-max-width: 1180px;
  --content-max-width: 860px;
  --sidebar-width: 260px;

  --header-height: 52px;
  --nav-height: 38px;


  /* =========================
     COMPONENTS
     ========================= */

  --button-bg: var(--color-accent);
  --button-bg-hover: var(--color-accent-strong);
  --button-text: #ffffff;

  --card-bg: var(--color-surface);
  --card-border: var(--color-border);

  --input-bg: #ffffff;
  --input-border: var(--color-border);
  --input-focus: var(--color-accent);

  --table-header-bg: #f3f6fa;
  --table-row-hover: #f8fafc;
}
```

# 2. Fundamental rule for the agent

The agent should treat these variables as a **design system**, not simply as aliases for colors.

HTML components should reference semantic variables wherever possible instead of containing arbitrary visual values.

For example, avoid:

```css
.project-card {
    color: #1f2937;
    background: #ffffff;
    border: 1px solid #d1d5db;
    padding: 12px;
}
```

Prefer:

```css
.project-card {
    color: var(--color-text);
    background: var(--card-bg);
    border: var(--border-width) var(--border-style) var(--card-border);
    padding: var(--space-3);
}
```

The second version allows the entire visual system to be changed centrally.

The agent should generally avoid introducing new literal colors, spacing measurements, font sizes, border radii, or shadows unless there is a clear reason that the existing design tokens cannot represent the requirement.

# 3. Color hierarchy

The four blue variables have intentionally different purposes.

| Variable | Purpose |
|---|---|
| `--color-primary` | Main brand blue |
| `--color-primary-strong` | Darker brand blue |
| `--color-accent` | Interactive/action blue |
| `--color-accent-strong` | Hover/pressed version of interactive blue |

## `--color-primary`

```css
--color-primary: #0a3d78;
```

Use for substantial brand-oriented elements.

Appropriate uses include section banners, branded headings, important structural accents, selected larger interface regions, and branded graphical elements.

Example:

```css
.section-banner {
    background: var(--color-primary);
    color: #ffffff;
}
```

Do **not** automatically use it for every link and button.

## `--color-primary-strong`

```css
--color-primary-strong: #072e5e;
```

Use when the primary blue needs additional visual weight.

Typical examples are dark brand strips, primary hover variants where appropriate, or hierarchical contrast within blue elements.

```css
.brand-header {
    background: var(--color-primary-strong);
}
```

## `--color-accent`

```css
--color-accent: #1e88e5;
```

This is the principal **interaction color**.

It should communicate:

- clickable
- active
- selected
- focused
- actionable

Typical usages are links, primary buttons, active navigation indicators, focus borders, selected pagination items, and small interface highlights.

```css
a {
    color: var(--color-link);
}

.nav-link.active {
    border-bottom: 2px solid var(--color-accent);
}

input:focus {
    border-color: var(--color-accent);
}
```

The accent should therefore appear selectively. If everything is blue, its value as an interaction cue is lost.

## `--color-accent-strong`

```css
--color-accent-strong: #0a66c2;
```

Primarily use for interaction state changes.

```css
.button-primary:hover {
    background: var(--color-accent-strong);
}
```

This tells the user that the element reacted to interaction without requiring animation or ornamental effects.

# 4. Surface system

There are three principal background levels.

| Variable | Role |
|---|---|
| `--color-bg` | Overall page background |
| `--color-surface` | Main component/content background |
| `--color-surface-alt` | Secondary or differentiated surface |

## Page background

```css
body {
    background: var(--color-bg);
}
```

The site should remain predominantly white.

This is deliberate. Do not turn the design into a collection of colored panels.

## Standard surface

```css
--color-surface: #ffffff;
```

Use for:

- cards
- forms
- project boxes
- content panels
- article entries
- sidebars when white is appropriate

```css
.card {
    background: var(--color-surface);
}
```

## Alternate surface

```css
--color-surface-alt: #f3f6fa;
```

Use when a subtle distinction is needed without introducing a new color.

Good examples:

```css
.sidebar {
    background: var(--color-surface-alt);
}

.table-header {
    background: var(--color-surface-alt);
}

.project-meta {
    background: var(--color-surface-alt);
}
```

It should primarily establish hierarchy.

Do not alternate every second component merely for decoration.

# 5. Text hierarchy

There are four primary text colors.

| Variable | Intended use |
|---|---|
| `--color-heading` | Titles and strong hierarchy |
| `--color-text` | Normal body content |
| `--color-text-muted` | Secondary information |
| `--color-link` | Clickable textual navigation |

## Heading text

```css
--color-heading: #0f172a;
```

Use for:

```css
h1,
h2,
h3,
.section-title,
.card-title {
    color: var(--color-heading);
}
```

The near-navy heading color provides slightly more structure than ordinary body text.

## Normal text

```css
--color-text: #1f2937;
```

This should be the default readable text color.

```css
body {
    color: var(--color-text);
}
```

Use it for descriptions, project explanations, blog text, technology descriptions, experience entries, form labels, and normal information.

## Muted text

```css
--color-text-muted: #6b7280;
```

Use for information that is useful but subordinate.

Examples:

```html
<p class="meta">
    Updated August 20, 2026 · 7 minute read
</p>
```

```css
.meta {
    color: var(--color-text-muted);
    font-size: var(--font-size-xs);
}
```

Other appropriate content includes dates, repository metadata, secondary descriptions, captions, breadcrumbs, and timestamps.

Muted text should **not** be used for important content.

# 6. Navigation system

The navigation deliberately uses a much darker background than the rest of the site.

```css
--color-nav-bg: #0f172a;
--color-nav-text: #e5e7eb;
--color-nav-active: #1e88e5;
```

Recommended structure:

```css
.navbar {
    min-height: var(--nav-height);
    background: var(--color-nav-bg);
    color: var(--color-nav-text);
}

.navbar a {
    color: var(--color-nav-text);
}

.navbar a:hover {
    color: var(--color-accent);
}

.navbar a.active {
    color: var(--color-nav-active);
    border-bottom: 2px solid var(--color-nav-active);
}
```

The navigation should remain:

- compact
- horizontal on desktop
- visually obvious
- immediately understandable
- free of decorative oversized elements

The agent should not create large floating navigation pills, giant navigation text, glassmorphism, or large rounded menus.

# 7. Border system

Borders are important to this design.

Unlike many modern portfolio designs that rely heavily on whitespace, shadows, and rounded floating cards, this portfolio should use **thin structural borders**.

```css
--color-border: #d1d5db;
--color-border-strong: #9ca3af;
```

## Normal border

Use for most structural divisions.

```css
.card {
    border: 1px solid var(--color-border);
}
```

Appropriate for:

- cards
- tables
- form controls
- project sections
- sidebars
- filters
- article rows
- metadata panels

## Strong border

Use when an element requires clearer separation.

```css
.button-secondary {
    border: 1px solid var(--color-border-strong);
}
```

Do not overuse `--color-border-strong`.

# 8. Shape philosophy

This is particularly important.

```css
--radius-none: 0;
--radius-sm: 2px;
```

The default visual shape is **square**.

The agent should assume:

```css
border-radius: var(--radius-none);
```

unless there is a specific reason for otherwise.

`--radius-sm` exists for tiny interface elements where a completely square shape becomes visually awkward, such as small technology tags.

Example:

```css
.tech-tag {
    border-radius: var(--radius-sm);
}
```

The agent should avoid:

```css
border-radius: 8px;
border-radius: 12px;
border-radius: 16px;
border-radius: 9999px;
```

unless explicitly instructed otherwise.

In particular, avoid pill-shaped buttons and tags.

# 9. Typography philosophy

The portfolio is intentionally more information-dense than a typical contemporary portfolio.

The normal body size should generally be:

```css
font-size: var(--font-size-md);
```

which is approximately **14px**.

## Recommended typography mapping

| Content | Variable |
|---|---|
| Fine metadata | `--font-size-xs` |
| Navigation, tags, compact controls | `--font-size-sm` |
| Normal body content | `--font-size-md` |
| Larger body/control text | `--font-size-base` |
| Section heading / H3 | `--font-size-lg` |
| Major section heading / H2 | `--font-size-xl` |
| Page heading / H1 | `--font-size-2xl` |

A reasonable global implementation is:

```css
body {
    font-family: var(--font-family-body);
    font-size: var(--font-size-md);
    line-height: var(--line-height-normal);
}

h1 {
    font-size: var(--font-size-2xl);
}

h2 {
    font-size: var(--font-size-xl);
}

h3 {
    font-size: var(--font-size-lg);
}

small,
.meta {
    font-size: var(--font-size-xs);
}
```

The agent should resist the common portfolio pattern of making headings 48–80px tall.

The purpose of headings is hierarchy, not visual spectacle.

# 10. Font weights

```css
--font-weight-normal: 400;
--font-weight-medium: 500;
--font-weight-semibold: 600;
--font-weight-bold: 700;
```

Recommended usage:

| Weight | Usage |
|---|---|
| `400` | body text |
| `500` | tags, navigation, labels |
| `600` | buttons, table headers, minor headings |
| `700` | page and section headings |

Avoid using bold text everywhere.

Too much bold text destroys hierarchy.

# 11. Line heights

```css
--line-height-tight: 1.25;
--line-height-normal: 1.5;
--line-height-relaxed: 1.65;
```

Use tight line height primarily for headings:

```css
h1,
h2,
h3 {
    line-height: var(--line-height-tight);
}
```

Normal prose:

```css
p {
    line-height: var(--line-height-normal);
}
```

Long-form blog articles may use:

```css
.blog-content {
    line-height: var(--line-height-relaxed);
}
```

This allows blog text to remain comfortable without making the rest of the portfolio unnecessarily spacious.

# 12. Monospace typography

```css
--font-family-mono:
    "JetBrains Mono",
    "Cascadia Code",
    Consolas,
    monospace;
```

Use for technical material only.

```css
code,
pre,
.command,
.file-path {
    font-family: var(--font-family-mono);
}
```

Appropriate content includes code samples, shell commands, class/function names, filenames, paths, configuration snippets, protocol values, and architecture/debug output.

Do not make ordinary body content monospace merely because this is a developer portfolio.

# 13. Spacing system

Spacing should almost always come from this scale.

| Variable | Size | Typical purpose |
|---|---:|---|
| `--space-1` | 4px | Tiny internal separation |
| `--space-2` | 8px | Compact padding |
| `--space-3` | 12px | Standard compact padding |
| `--space-4` | 16px | Standard component spacing |
| `--space-5` | 20px | Medium section separation |
| `--space-6` | 24px | Larger section separation |
| `--space-8` | 32px | Major structural separation |
| `--space-10` | 40px | Rare large separation |

Example:

```css
.card {
    padding: var(--space-3);
}

.section {
    margin-bottom: var(--space-6);
}

.page {
    padding: var(--space-4);
}
```

The agent should not arbitrarily introduce values like:

```css
padding: 17px;
margin: 27px;
gap: 13px;
```

when an existing spacing token is sufficiently close.

The visual rhythm should remain predictable.

# 14. Shadows

This design should primarily rely on borders.

```css
--shadow-none: none;
--shadow-sm: 0 1px 2px rgb(15 23 42 / 0.08);
--shadow-md: 0 2px 5px rgb(15 23 42 / 0.10);
```

Default cards should usually be:

```css
.card {
    border: 1px solid var(--color-border);
    box-shadow: var(--shadow-none);
}
```

`--shadow-sm` can be used sparingly for elevated interactive elements.

`--shadow-md` should be rare.

Avoid dramatic shadows such as:

```css
box-shadow: 0 20px 60px rgba(...);
```

That would conflict with the intended enterprise appearance.

# 15. Page width

```css
--page-max-width: 1180px;
```

This controls the primary desktop page shell.

```css
.page-container {
    width: 100%;
    max-width: var(--page-max-width);
    margin-inline: auto;
    padding-inline: var(--space-4);
}
```

The site should not stretch indefinitely across wide monitors.

# 16. Content width

```css
--content-max-width: 860px;
```

Use when prose or primary content should be narrower than the entire page.

For example:

```css
.article-content {
    max-width: var(--content-max-width);
}
```

This is especially useful for:

- blog posts
- documentation-style project descriptions
- case studies
- long technical explanations

# 17. Sidebar width

```css
--sidebar-width: 260px;
```

Desktop project pages can use:

```css
.project-layout {
    display: grid;

    grid-template-columns:
        minmax(0, 1fr)
        var(--sidebar-width);

    gap: var(--space-4);
}
```

Possible sidebar information includes:

- technology stack
- repository link
- project status
- dates
- language
- testing information
- architecture metadata
- documentation links

On narrow screens, the sidebar should move below the main content.

```css
@media (max-width: 800px) {
    .project-layout {
        grid-template-columns: 1fr;
    }
}
```

# 18. Header and navigation heights

```css
--header-height: 52px;
--nav-height: 38px;
```

These are intentionally compact.

The site should not have a 100–150px-tall header.

Example:

```css
.site-header {
    min-height: var(--header-height);
}

.navbar {
    min-height: var(--nav-height);
}
```

# 19. Buttons

Component variables:

```css
--button-bg: var(--color-accent);
--button-bg-hover: var(--color-accent-strong);
--button-text: #ffffff;
```

Recommended implementation:

```css
.button-primary {
    display: inline-flex;
    align-items: center;
    justify-content: center;

    background: var(--button-bg);
    color: var(--button-text);

    border: 1px solid var(--button-bg);
    border-radius: var(--radius-none);

    padding: var(--space-2) var(--space-3);

    font-size: var(--font-size-sm);
    font-weight: var(--font-weight-semibold);

    text-decoration: none;
    cursor: pointer;
}

.button-primary:hover {
    background: var(--button-bg-hover);
    border-color: var(--button-bg-hover);
}
```

Buttons should generally be compact.

Avoid giant call-to-action buttons.

# 20. Cards and panels

```css
--card-bg: var(--color-surface);
--card-border: var(--color-border);
```

Standard pattern:

```css
.card {
    background: var(--card-bg);

    border:
        var(--border-width)
        var(--border-style)
        var(--card-border);

    border-radius: var(--radius-none);

    padding: var(--space-3);
}
```

Cards should be used to structure information—not to turn every piece of content into an isolated floating tile.

Good uses include project summaries, technical details, architecture notes, featured projects, contact information, and concise metadata.

# 21. Form controls

```css
--input-bg: #ffffff;
--input-border: var(--color-border);
--input-focus: var(--color-accent);
```

Recommended:

```css
input,
textarea,
select {
    background: var(--input-bg);
    color: var(--color-text);

    border: 1px solid var(--input-border);
    border-radius: var(--radius-none);

    padding: var(--space-2);

    font: inherit;
}

input:focus,
textarea:focus,
select:focus {
    outline: none;
    border-color: var(--input-focus);
}
```

Do not use floating labels, giant fields, heavily animated inputs, or large rounded search bars unless explicitly requested.

# 22. Tables

Tables are an important part of the visual language because they allow high information density.

```css
--table-header-bg: #f3f6fa;
--table-row-hover: #f8fafc;
```

Example:

```css
table {
    width: 100%;
    border-collapse: collapse;
    font-size: var(--font-size-sm);
}

th {
    background: var(--table-header-bg);
    color: var(--color-heading);

    font-weight: var(--font-weight-semibold);

    text-align: left;

    padding: var(--space-2);

    border: 1px solid var(--color-border);
}

td {
    padding: var(--space-2);
    border: 1px solid var(--color-border);
}

tbody tr:hover {
    background: var(--table-row-hover);
}
```

Tables are particularly appropriate for:

- blog indexes
- project metadata
- test results
- experience
- release information
- technology matrices

# 23. Technology tags

Use alternate surfaces and borders rather than colorful pills.

```css
.tech-tag {
    display: inline-block;

    background: var(--color-surface-alt);
    color: var(--color-text);

    border: 1px solid var(--color-border);
    border-radius: var(--radius-sm);

    padding: var(--space-1) var(--space-2);

    font-size: var(--font-size-xs);
    font-weight: var(--font-weight-medium);
}
```

Example:

```html
<span class="tech-tag">C++</span>
<span class="tech-tag">Python</span>
<span class="tech-tag">Linux</span>
<span class="tech-tag">CMake</span>
```

Avoid assigning every language a bright custom color unless there is a functional reason.

# 24. Status colors

```css
--color-success: #16a34a;
--color-warning: #f59e0b;
--color-error: #dc2626;
```

These colors have semantic meaning.

They should not be used decoratively.

For example:

```css
.status-success {
    color: var(--color-success);
}

.status-warning {
    color: var(--color-warning);
}

.status-error {
    color: var(--color-error);
}
```

Potential portfolio uses:

| Status | Example |
|---|---|
| Success | Tests passing |
| Warning | Experimental project |
| Error | Build failure shown in technical article |

Do not use red simply because a card needs visual variety.

# 25. Recommended component mapping

This table should be especially useful to an implementation agent.

| Component | Recommended variables |
|---|---|
| `body` | `--color-bg`, `--color-text`, `--font-family-body`, `--font-size-md` |
| Main page shell | `--page-max-width`, `--space-4` |
| Navigation | `--color-nav-bg`, `--color-nav-text`, `--nav-height` |
| Active navigation | `--color-nav-active` |
| H1 | `--color-heading`, `--font-size-2xl`, `--font-weight-bold` |
| H2 | `--color-heading`, `--font-size-xl`, `--font-weight-bold` |
| H3 | `--color-heading`, `--font-size-lg`, `--font-weight-semibold` |
| Body copy | `--color-text`, `--font-size-md` |
| Metadata | `--color-text-muted`, `--font-size-xs` or `sm` |
| Links | `--color-link` |
| Primary button | `--button-bg`, `--button-bg-hover`, `--button-text` |
| Secondary button | `--color-surface`, `--color-primary`, `--color-border-strong` |
| Card | `--card-bg`, `--card-border`, `--space-3` |
| Sidebar | `--color-surface-alt`, `--sidebar-width` |
| Form field | `--input-bg`, `--input-border`, `--input-focus` |
| Table header | `--table-header-bg` |
| Table hover | `--table-row-hover` |
| Tags | `--color-surface-alt`, `--color-border`, `--font-size-xs` |
| Code | `--font-family-mono` |
| Standard divider | `--color-border` |
| Success state | `--color-success` |
| Warning state | `--color-warning` |
| Error state | `--color-error` |

# 26. Recommended global starting CSS

An agent can use this as the baseline before building individual components.

```css
*,
*::before,
*::after {
    box-sizing: border-box;
}

html {
    font-size: 16px;
}

body {
    margin: 0;

    background: var(--color-bg);
    color: var(--color-text);

    font-family: var(--font-family-body);
    font-size: var(--font-size-md);
    font-weight: var(--font-weight-normal);

    line-height: var(--line-height-normal);
}

img {
    display: block;
    max-width: 100%;
}

a {
    color: var(--color-link);
    text-decoration: none;
}

a:hover {
    text-decoration: underline;
}

h1,
h2,
h3,
h4,
p {
    margin-top: 0;
}

h1,
h2,
h3,
h4 {
    color: var(--color-heading);
    line-height: var(--line-height-tight);
}

h1 {
    font-size: var(--font-size-2xl);
    font-weight: var(--font-weight-bold);
}

h2 {
    font-size: var(--font-size-xl);
    font-weight: var(--font-weight-bold);
}

h3 {
    font-size: var(--font-size-lg);
    font-weight: var(--font-weight-semibold);
}

button,
input,
textarea,
select {
    font: inherit;
}

code,
pre {
    font-family: var(--font-family-mono);
}

.page-container {
    width: 100%;
    max-width: var(--page-max-width);

    margin-inline: auto;

    padding-inline: var(--space-4);
}
```

# 27. Visual rules the agent should preserve

The most important design requirement is not any individual hexadecimal color. It is the **relationship between the variables and the resulting interface**.

The agent should preserve these principles:

1. **Content density is desirable.** Do not artificially expand components to imitate modern marketing websites.
2. **Square edges are the default.** Very small radii may be used sparingly.
3. **Borders define structure.** Shadows are secondary.
4. **Typography remains relatively small.** Normal page text should generally be around 14px.
5. **Whitespace should organize content, not dominate it.**
6. **Blue indicates branding or interaction.** Do not make every component blue.
7. **Most surfaces remain white or very light gray.**
8. **Navigation should be compact and obvious.**
9. **Tables, lists, sidebars, metadata blocks, and structured content are encouraged.**
10. **The website should resemble a well-designed engineering/product portal more than a creative-agency portfolio.**
11. **Avoid oversized hero sections.**
12. **Avoid giant headlines occupying much of the viewport.**
13. **Avoid pill-shaped controls.**
14. **Avoid excessive gradients.**
15. **Avoid glassmorphism, blur-heavy surfaces, floating blobs, and abstract decoration.**
16. **Avoid excessive animation.**
17. **Do not hide useful information merely to make the page visually sparse.**
18. **Interactive states must remain obvious through color, borders, or underlines.**
19. **Responsive design should reorganize content rather than radically simplify it.**
20. **New components should reuse the established variable system before introducing new tokens.**

# 28. Example of how the agent should think

Suppose the agent needs to create a new `"Project Technical Details"` panel.

It should not independently choose:

```css
background: #f5f5f5;
border: 1px solid #ccc;
padding: 15px;
border-radius: 8px;
font-size: 13px;
```

Instead, it should translate the requirement into existing design tokens:

```css
.project-technical-details {
    background: var(--color-surface-alt);

    border:
        var(--border-width)
        var(--border-style)
        var(--color-border);

    border-radius: var(--radius-none);

    padding: var(--space-3);

    font-size: var(--font-size-sm);
}
```

That distinction is central to how this design system should be used.

# 29. When new variables should be added

The agent **may** extend the variable system, but only when a new concept is repeatedly needed.

For example, if several components require the same project screenshot background, adding:

```css
--color-code-bg: #0f172a;
```

may make sense.

Likewise, if every responsive layout uses the same breakpoint, a later design-system layer could define breakpoint conventions.

Do not create variables for one-off values simply for the sake of having variables.

A useful rule is:

> If the same semantic design decision appears in multiple components, it is probably a design token. If it appears once, it probably belongs in the component.

# 30. Final implementation target

The finished HTML/CSS should visually communicate:

**“Software engineering portfolio / technical information system.”**

It should **not** communicate:

**“Creative agency landing page / trendy SaaS template / visual design showcase.”**

A visitor should be able to quickly scan the site and answer:

- Who is this developer?
- What technologies do they use?
- What have they built?
- What did they personally implement?
- How does each project work?
- What engineering decisions were made?
- Where is the source code?
- What technical writing is available?
- How can I contact them?

The variable system exists to make all of those pages feel like parts of the **same compact Enterprise Blue interface**, even when different agents or components are responsible for implementing them.
