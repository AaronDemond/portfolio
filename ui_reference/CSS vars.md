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

  /* Intentionally square / enterprise */
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
