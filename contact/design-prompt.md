# Design Prompt

✅ Monochrome-First Color Template

🔑 Usage rules (important)\
• Primary CTA → black\
• Hover → slight elevation / subtle outline (not color)\
• Focus → thin black ring\
• Red → only for irreversible danger\
• No blue anywhere by default

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
  secondary: '#F7F7F8',
  'secondary-foreground': '#0A0A0A',

  // Muted / metadata
  muted: '#F2F2F2',
  'muted-foreground': '#6B7280',

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
