---
icon: palette
---

# Design Prompt

### Brand Personality

Minimal, trustworthy, technical, fast, precise, premium, calm.

**Avoid**: playful, cartoonish, futuristic for the sake of futuristic, crypto casino style, loud Web3 aesthetics.

**Do not use**: gradients, neon effects, colorful illustrations, 3D objects, glassmorphism, decorative blobs, cyberpunk lighting, excessive shadows, emoji-style icons, or playful UI elements.

The design should feel **calm, precise, premium, and infrastructure-grade**.

***

### Color System

Monochrome-first. No brand color. Status colors are functional only — never decorative.

| Token            | Value                  | Usage                                |
| ---------------- | ---------------------- | ------------------------------------ |
| Background       | `#FFFFFF` or `#FAFAFA` | Page background                      |
| Primary text     | `#0A0A0A`              | Headlines, body                      |
| Secondary text  | `#525252`              | Metadata, captions                   |
| Border           | `#E5E5E5`              | Hairline dividers, inputs, cards     |
| Muted surface   | `#F5F5F5`              | Quiet backgrounds                    |
| Primary button   | Black bg, white text   | Single primary action per screen     |
| Secondary button | White bg, black text, 1px border | Supporting actions          |

**Status colors** (use sparingly):

* Success — small green indicator only
* Warning / error — minimal amber / red text or icon only

🔑 Usage rules\
• Primary CTA → black\
• Hover → slight elevation / subtle outline (not color)\
• Focus → thin black ring\
• Red → only for irreversible danger\
• No blue anywhere by default\
• Do not use status colors as decoration

***

### Typography

* Font family: **Inter** (all weights, all UI surfaces)
* Fallback stack: `Inter, ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif`
* Load from [Google Fonts](https://fonts.google.com/specimen/Inter) or [rsms.me/inter](https://rsms.me/inter/)
* Clean sans-serif only — avoid decorative fonts
* Headlines confident but not oversized
* Use **font weight** for emphasis instead of color

**Hierarchy**

| Level   | Desktop  | Mobile  |
| ------- | -------- | ------- |
| H1      | 48–64px  | 36–44px |
| H2      | 32–40px  | —       |
| H3      | 20–24px  | —       |
| Body    | 16px     | —       |
| Caption | 12–14px  | —       |

***

### Layout & Spacing

* Generous whitespace
* 12-column grid on desktop
* Max content width **1120–1200px**
* Spacing scale: **4, 8, 12, 16, 24, 32, 48, 64**
* Avoid crowded dashboards
* Every screen has **one clear primary action**

***

### Components

**Buttons** — rectangular with subtle radius, no glow, no gradient.

**Cards** — white or very light gray, 1px border, minimal or no shadow.

**Inputs** — clean border, clear focus state, no heavy background.

**Tables** — simple rows, thin dividers, strong alignment.

**Modals** — centered, white, clear action hierarchy.

**Icons** — outline style, monochrome, 16–20px, functional only.

**Border radius**

* Small components: 6–8px
* Cards: 12–16px
* Avoid overly rounded pill shapes (except for small labels)

***

### CSS Tokens

```css
{
  // Base colors
  background: '#FFFFFF',
  foreground: '#0A0A0A',

  // Surfaces (almost flat)
  card: '#FCFCFC',
  'card-foreground': '#0A0A0A',

  // Primary action (monochrome, confident)
  primary: '#0A0A0A',            // black / near-black button
  'primary-foreground': '#FFFFFF',

  // Secondary (quiet surface)
  secondary: '#F5F5F5',
  'secondary-foreground': '#0A0A0A',

  // Muted / metadata
  muted: '#F5F5F5',
  'muted-foreground': '#525252',

  // Accent (same as primary — no brand color)
  accent: '#0A0A0A',
  'accent-foreground': '#FFFFFF',

  // Success (subtle, not celebratory)
  success: '#15803D',
  'success-foreground': '#FFFFFF',

  // Destructive (only when truly dangerous)
  destructive: '#B91C1C',
  'destructive-foreground': '#FFFFFF',

  // Warning (rare)
  warning: '#A16207',
  'warning-foreground': '#0A0A0A',

  // Borders & focus (hairline, neutral)
  border: '#E5E5E5',
  input: '#E5E5E5',
  ring: '#0A0A0A',
}
```
