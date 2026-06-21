---
icon: swatchbook
description: >-
  ROZO's design system — monochrome, infrastructure-grade, built for stablecoin
  payments. Light theme only; no brand color by design. Design tokens plus the
  rules for using them.
---

# Design System

> **Version:** `alpha`. Tokens may change without notice during alpha. Hex values are sRGB.

## Overview

ROZO is a design system for building consistent, infrastructure-grade interfaces for stablecoin payments. The aesthetic is monochrome, hairline, and quiet: plenty of whitespace, near-black on white, and structure carried by 1px borders rather than shadows. The test for any choice is "would this feel right on a Bloomberg terminal or a switch's admin page?" Prioritize readability, density that breathes, and restraint. Use weight, space, and contrast — not color — to signal importance.

This is the single theme. There is no dark theme and no brand color by design; black (`#0a0a0a`) is the accent. Light-only is a deliberate alpha constraint: financial data needs high-fidelity contrast that is hard to guarantee across a dark palette without a dedicated second token set, so dark mode is deferred to a later version rather than half-done now.

## Colors

ROZO is monochrome-first. There is no blue, no purple, no brand hue — if you reach for a color to make something feel important, that is the wrong choice; use weight, space, or contrast instead.

### Core neutrals

| Token | Value | Usage |
| --- | --- | --- |
| `background` | `#ffffff` | Flat white page background |
| `background-alt` | `#fafafa` | Cooler page chrome behind cards |
| `foreground` | `#0a0a0a` | Primary text, icons, primary action |
| `card` | `#fcfcfc` | Surface that must read as separate from the page |
| `muted` / `secondary` | `#f5f5f5` | Quiet fills, hover tints |
| `muted-foreground` | `#525252` | Secondary text: metadata, captions, column headers |
| `border` | `#e5e5e5` | The 1px hairline that carries structure ~95% of the time |
| `border-strong` | `#d4d4d4` | A firmer edge — hover borders and inputs that need more definition |

### Action & accent

`primary` and `accent` share the value `#0a0a0a` / `#ffffff` **on purpose**, but mean different things: `primary` is the fill of the one primary action on a screen (the black button); `accent` is the near-black used to emphasize a word, a number, or an active state. Keep them as separate tokens so either can evolve without disturbing the other.

`input` (`#e5e5e5`) is intentionally the same value as `border`. It is a distinct token so form-control edges can be tuned independently from structural hairlines later — reference `input` on form elements, `border` on everything structural.

`ring` (`#0a0a0a`) is the focus color (see [Focus](#focus)).

### Neutral scale

The `neutral-*` scale runs light to near-black for tables, dividers, and opaque fills.

| `50` | `100` | `200` | `300` | `400` | `500` | `600` | `700` | `800` | `900` |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `#fafafa` | `#f5f5f5` | `#e5e5e5` | `#d4d4d4` | `#a3a3a3` | `#737373` | `#525252` | `#404040` | `#262626` | `#0a0a0a` |

### Status colors

Status colors are **functional only** and rare: `success` green (`#15803d`) for settled, `warning` amber (`#a16207`) for action required, `destructive` red (`#b91c1c`) for hard failure or destructive confirmation. They appear as a single dot, a thin underline, or a word — **never as a fill behind a card or chip**. No gradients, no glows, no neon, no glass. If a surface must read as separate from the page, give it a `1px solid #e5e5e5` border and a `#fcfcfc` background.

### Contrast

All text/background pairs hold WCAG AA (≥ 4.5:1 for body, ≥ 3:1 for large/UI text) on white.

| Foreground | On | Ratio | Level |
| --- | --- | --- | --- |
| `foreground` `#0a0a0a` | `background` `#ffffff` | 20.1:1 | AAA |
| `muted-foreground` `#525252` | `background` `#ffffff` | 7.6:1 | AAA |
| `muted-foreground` `#525252` | `muted` `#f5f5f5` | 6.9:1 | AA |
| `success` `#15803d` | `background` `#ffffff` | 4.8:1 | AA |
| `warning` `#a16207` | `background` `#ffffff` | 4.8:1 | AA |
| `destructive` `#b91c1c` | `background` `#ffffff` | 5.9:1 | AA |
| `neutral-400` `#a3a3a3` (disabled) | `background` `#ffffff` | 2.5:1 | UI only — never body text |

## Typography

Inter sets the entire UI and prose stack; JetBrains Mono is reserved for code, transaction hashes, addresses, and amount strings on developer surfaces. We never reach for a display font, a serif, or a script. For CJK, fall back to the system CJK stack (`"PingFang SC", "Microsoft YaHei", "Hiragino Sans", sans-serif`) — Inter does not cover Han glyphs.

| Style | Font | Size / line | Weight | Tracking |
| --- | --- | --- | --- | --- |
| `display` | Inter | 64 / 70 | 600 | -1.28px |
| `h1` | Inter | 48 / 53 | 600 | -0.72px |
| `h2` | Inter | 32 / 40 | 600 | -0.48px |
| `h3` | Inter | 24 / 30 | 600 | -0.12px |
| `h4` | Inter | 20 / 25 | 600 | -0.1px |
| `body` | Inter | 16 / 26 | 400 | 0 |
| `small` | Inter | 14 / 20 | 400 | 0 |
| `caption` | Inter | 12 / 16 | 400 | 0 |
| `eyebrow` | Inter | 12 / 16 | 500 | +0.96px, uppercase |
| `mono-14/13/12` | JetBrains Mono | 14·13·12 / 20·20·16 | 400 | 0 |

- **Headings** (`display` 64 → `h4` 20) title pages and sections; tracking tightens as size grows, and headings cap at 64px — confident, not oversized.
- **Body** (16px) and **small** (14px) cover most text. Letter-spacing is `0` below headings.
- **Eyebrow** is the 12px uppercase, `+0.96px`-tracked, medium-weight label used over KPIs and section headers.
- **Mono** pairs JetBrains Mono for hashes, addresses, and amounts; always use tabular figures (`font-variant-numeric: tabular-nums`) where numbers must align — in tables and on dashboards.

Weight does the work of color: a 600-weight word inside a 400-weight paragraph is how we emphasize. Keep to two weights per view (400 body + 600 emphasis); reserve 700/800 for marketing surfaces.

## Layout

Spacing follows a 4px scale: 4, 8, 12, 16, 24, 32, 48, 64px. Keep a three-step rhythm: 8px inside a group, 16px between groups, 32–48px between sections. Do not invent 18, 22, 40. Cards pad 24px (16px compact, 32px hero). Center content in a 12-column grid, 24px gutters, 1120–1200px max. Dashboards breathe — a table row is 56px tall, not 36. Sidebars are 240–280px fixed with a hairline right border; top bars are 56–64px fixed with a hairline bottom border. One primary action per screen; everything else is secondary or tertiary.

**Breakpoints.** `sm 640` · `md 768` · `lg 1024` · `xl 1280` · `2xl 1536`. The fixed sidebar collapses to an off-canvas drawer below `lg`; the 12-column grid drops to 8 columns at `md` and a single column below `sm`. Tables become horizontally scrollable rather than reflowing below `md`.

**Stacking (`z-index`).** Use named layers, never ad-hoc values: `base 0` · `dropdown 1000` · `sticky 1100` · `overlay 1200` · `modal 1300` · `toast 1400` · `tooltip 1500`.

## Elevation & depth

Hierarchy comes from tonal surfaces and 1px borders first, so shadows stay essentially absent. The default elevation of a card is its border.

- Raised cards: `none` (border only)
- Floating menu / popover (ceiling): `0 4px 12px rgba(10,10,10,0.06), 0 0 0 1px rgba(10,10,10,0.04)`
- Hairline lift: `0 1px 0 0 rgba(10,10,10,0.04)`

Never wrap a card in a soft drop shadow; if it needs to separate, use a border.

## Motion

Fast, neutral, almost invisible. `120ms` for hover, `180ms` for state changes, `260ms` for layered transitions like a modal entering. Easing is `cubic-bezier(0.2, 0, 0, 1)`. No bounce, no spring, no overshoot, no parallax, no scroll-jacking, no decorative looping. Loading is a 1px progress bar or a thin spinner — never a shimmer skeleton. Honor `prefers-reduced-motion` by dropping nonessential motion.

## Shapes

Radii stay tight and consistent within a view: `6px` for everyday controls (buttons, inputs, search), `8px` available for secondary surfaces, `12–16px` for cards, `9999px` reserved for small status chips and avatars only. Never wrap a whole card in a pill, and never mix rounded and sharp corners in one view.

| Token | `xs` | `sm` | `md` | `lg` | `xl` | `pill` |
| --- | --- | --- | --- | --- | --- | --- |
| Value | 4px | 6px | 8px | 12px | 16px | 9999px |

## Components

The component tokens give ready-to-use values drawn from this theme.

- **Primary button**: solid `#0a0a0a` fill, white label, 6px radius, 40px tall — the single most important action on a view. Hover darkens to `#262626`.
- **Secondary button**: white fill, `#e5e5e5` border, gains a `#0a0a0a` border on hover.
- **Ghost button**: transparent, tints with `muted` on hover, for low-emphasis actions.
- **Destructive button**: solid `#b91c1c` fill, white text, for hard/destructive actions.
- Sizes are `sm` 32px (12px horizontal padding) and `lg` 48px (20px padding) around the default 40px medium (16px padding). Icon-only buttons are square at each height (32/40/48px).
- **Input**: white fill, `#e5e5e5` border, 6px radius, 40px tall; on focus, the border goes to `#0a0a0a` and the standard focus ring is applied (see [Focus](#focus)).
- **Card**: white / `#fcfcfc`, 1px `#e5e5e5` border, 12–16px radius, no shadow, 24–32px padding. Title top-left, actions top-right, content below. Interactive (clickable) cards shift their background to `background-alt` on hover — no shadow, no scale.
- **Badge / status**: the status is carried by a `6px × 6px` dot with `border-radius: 50%` (a circle — unrelated to the `rounded` scale); the text stays neutral. No fill, no colored border.
- **Table**: header row on `muted` (`#f5f5f5`), 1px `border` row separators, 12–16px cell padding, 56px row height. Numbers and status align right (JetBrains Mono, tabular figures); text and dates align left.

### Focus

There is exactly one focus treatment. Use the `shadows.focus` token everywhere — a thin black ring on a white gap:

```css
:focus-visible {
  outline: none;
  box-shadow: 0 0 0 2px #ffffff, 0 0 0 4px #0a0a0a; /* shadows.focus */
}
```

It is always visible at `:focus-visible` and never removed. (Earlier drafts described a soft `rgba(10,10,10,0.08)` ring on inputs — that is deprecated; the double-ring above is the only focus style.)

Disabled uses a `muted` fill, `neutral-400` text, and a not-allowed cursor.

## Using tokens

These tokens are meant to be copied straight into a project. Two ways to consume them:

### CSS custom properties

Name variables `--rozo-<group>-<name>`:

```css
:root {
  /* color */
  --rozo-color-background: #ffffff;
  --rozo-color-foreground: #0a0a0a;
  --rozo-color-muted: #f5f5f5;
  --rozo-color-muted-foreground: #525252;
  --rozo-color-border: #e5e5e5;
  --rozo-color-success: #15803d;
  --rozo-color-warning: #a16207;
  --rozo-color-destructive: #b91c1c;

  /* radius / spacing / motion */
  --rozo-radius-sm: 6px;
  --rozo-radius-lg: 12px;
  --rozo-space-4: 16px;
  --rozo-ease-standard: cubic-bezier(0.2, 0, 0, 1);
  --rozo-shadow-focus: 0 0 0 2px #ffffff, 0 0 0 4px #0a0a0a;
}
```

### Tailwind config

```js
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        background: "#ffffff",
        foreground: "#0a0a0a",
        muted: { DEFAULT: "#f5f5f5", foreground: "#525252" },
        border: "#e5e5e5",
        success: "#15803d",
        warning: "#a16207",
        destructive: "#b91c1c",
      },
      borderRadius: { sm: "6px", md: "8px", lg: "12px", xl: "16px" },
      fontFamily: {
        sans: ["Inter", "system-ui", "sans-serif"],
        mono: ["JetBrains Mono", "ui-monospace", "monospace"],
      },
      transitionTimingFunction: { standard: "cubic-bezier(0.2,0,0,1)" },
    },
  },
}
```

### Component example

A primary button, built only from tokens:

```html
<button class="h-10 px-4 rounded-[6px] bg-foreground text-white text-sm font-medium
               transition-colors duration-[120ms] hover:bg-neutral-800
               focus-visible:outline-none focus-visible:shadow-[0_0_0_2px_#fff,0_0_0_4px_#0a0a0a]">
  Send payment
</button>
```

## Voice & content

The voice is declarative, technical, and quiet. ROZO does not sell; it states. Copy reads like an SDK reference or a hardware spec sheet, not a Web3 landing page.

- **Sentence case** for everything — buttons, headings, menu items, titles. ("Create invoice," not "Create Invoice.") Product names and acronyms keep canonical case: ROZO, USDC, EVM, SDK, POS. Short status chips may use Title Case ("Settled", "Pending").
- Name actions with a verb and a noun (`Send payment`, `Delete member`), never `Confirm`, `OK`, or a bare verb.
- Write errors as what happened plus where: `Transfer failed. Insufficient gas on Base.`
- Status reads as fact, not celebration: `Settled · $48.20 USDC`, never "🎉 Payment successful!".
- Empty states point to the first action: `Connect a wallet to continue.`
- In-progress states use the present participle with an ellipsis: `Settling…`, `Routing…`.
- Prefer the vocabulary of rails: **settle, route, intent, rail, chain, net, clear**. Avoid **seamless, revolutionary, next-gen, empower, unleash**, and crypto slang (`gm`, `wagmi`, `ape in`).
- Use numerals (`3 chains`), the en dash for ranges (`5–8 sec`), ISO currency codes (USDC, USDT). No `please`, no marketing superlatives.
- **No emoji.** Anywhere. No exclamation points except in destructive confirmations ("This cannot be undone.").

**Formatting.** Amounts: `$48.20 USDC` (two decimals, ISO code after, space before). Addresses: truncate as first-6 + last-4 (`0x49CD…eEe0`). Dates: ISO-like `2026-06-21` or `Jun 21, 2026`; times in 24h with timezone. Percentages: one decimal (`9.8% APY`).

## Do's and don'ts

- Use the gray scale to rank information: `foreground` for primary text, `muted-foreground` for secondary, `neutral-400` for disabled.
- Emphasize with weight (600), not color or highlight.
- Let a 1px border be the default elevation; reserve shadow for floating menus only.
- Hold WCAG AA contrast (4.5:1 for body text).
- Show the focus ring on every interactive element at `:focus-visible`; never remove an outline without a visible replacement.
- Use the typography and spacing tokens instead of hand-setting size, line height, weight, or odd pixel gaps.
- Don't reach for a brand color, a gradient, a glow, or a glass effect — there is no brand color.
- Don't signal status with a fill; the dot, underline, or word carries it.
- Don't mix rounded and sharp corners, or more than two font weights, in one view.
- Don't use decorative icons or emoji; every icon has a job (status, action, or category).
