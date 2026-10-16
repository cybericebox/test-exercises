---
name: "Cyber ICE Box — Training Exercises"
description: "A Ukrainian connection desk for a first web flag and VPN-only SSH practice."
colors:
  paper: "#f4f7f5"
  ink: "#142e3a"
  teal: "#14747a"
  focus-teal: "#247c83"
  brand-teal: "#0d767b"
  diagram-teal: "#276a72"
  lime: "#defa8d"
  lime-hover: "#c9ed73"
  white: "#fff"
  body-muted: "#48616b"
  meta-muted: "#526c72"
  section-muted: "#91a9b0"
  on-dark-muted: "#c2d2d6"
  section-number-muted: "#5c7479"
  code-comment: "#617980"
  divider: "#d5dfdb"
  terminal-border: "#c7d7d6"
  terminal-divider: "#d9e3df"
  terminal-note-divider: "#e4eae8"
  copy-border: "#79979f"
  copy-hover: "#264955"
  diagram-dot: "#c7d9da"
  diagram-route: "#87b9ba"
  diagram-server-line: "#779aa3"
typography:
  display:
    fontFamily: "Manrope, ui-sans-serif, sans-serif"
    fontSize: "clamp(40px, 4.5vw, 64px)"
    fontWeight: 730
    lineHeight: 1.07
    letterSpacing: "-2px"
  headline:
    fontFamily: "Manrope, ui-sans-serif, sans-serif"
    fontSize: "27px"
    fontWeight: 650
    lineHeight: 1.25
    letterSpacing: "-0.5px"
  brand:
    fontFamily: "Manrope, ui-sans-serif, sans-serif"
    fontSize: "21px"
    fontWeight: 750
    letterSpacing: "-0.7px"
  body:
    fontFamily: "ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, \"Segoe UI\", sans-serif"
    fontSize: "16px"
    lineHeight: 1.6
  intro:
    fontFamily: "ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, \"Segoe UI\", sans-serif"
    fontSize: "18px"
    lineHeight: 1.65
  button:
    fontFamily: "ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, \"Segoe UI\", sans-serif"
    fontSize: "14px"
    fontWeight: 700
  label:
    fontFamily: "ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, \"Segoe UI\", sans-serif"
    fontSize: "12px"
  code:
    fontFamily: "ui-monospace, SFMono-Regular, Consolas, monospace"
    fontSize: "13px"
    lineHeight: 1.9
rounded:
  copy: "5px"
  button: "6px"
  terminal: "8px"
  flag-section: "12px"
spacing:
  compact: "12px"
  control: "18px"
  block: "24px"
  hero: "28px"
components:
  button-primary:
    backgroundColor: "{colors.lime}"
    textColor: "{colors.ink}"
    typography: "{typography.button}"
    rounded: "{rounded.button}"
    padding: "10px 18px"
  button-primary-hover:
    backgroundColor: "{colors.lime-hover}"
  button-copy:
    backgroundColor: "transparent"
    textColor: "{colors.white}"
    typography: "{typography.label}"
    rounded: "{rounded.copy}"
    padding: "4px 10px"
  button-copy-hover:
    backgroundColor: "{colors.copy-hover}"
  flag-panel:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.white}"
    rounded: "{rounded.flag-section}"
    padding: "38px 34px 30px"
  terminal:
    backgroundColor: "{colors.white}"
    rounded: "{rounded.terminal}"
  status-dot:
    backgroundColor: "{colors.lime}"
    rounded: "50%"
    width: "7px"
    height: "7px"
---

# Design System: Cyber ICE Box — Training Exercises

## Overview

**Creative North Star: "The Connection Desk"**

A quiet editorial desk makes the first network connection feel approachable. The pale page, navy text and restrained teal diagram establish a calm reading surface; lime marks the action that yields a result.

The local Manrope headings give the page its identity, while familiar system text carries instructions. Spacious sections and a single dark reveal panel guide attention without decorative effects. Commands stay visibly distinct in a secondary terminal.

**Key Characteristics:**
- Large, tightly set two-line display type.
- A pale reading surface with one dark action panel.
- A route diagram that explains browser proxy and VPN access.
- Direct controls, visible keyboard focus and readable command examples.

## Colors

The palette pairs pale paper and deep navy with functional teal and a small, bright lime action accent. The frontmatter records every color currently used by the stylesheet and route illustration; it is the normative source for exact values.

### Primary

- **Action Lime** (`lime`, `lime-hover`): the reveal button, successful feedback, flag output and server status lights.
- **Route Teal** (`teal`, `brand-teal`, `diagram-teal`, `focus-teal`): the highlighted headline, brand arrow, route labels and keyboard focus respectively.

### Neutral

- **Paper** (`paper`) and **Ink** (`ink`): page background, primary text and the dark reveal panel.
- **White** (`white`): terminal surface, browser diagram node and text on the dark panel.
- **Body and metadata tones** (`body-muted`, `meta-muted`, `section-number-muted`, `code-comment`): instructional text, small context and command comments.
- **Dark-surface text** (`section-muted`, `on-dark-muted`): section numbering and supporting instructions inside the reveal panel.
- **Borders** (`divider`, `terminal-border`, `terminal-divider`, `terminal-note-divider`, `copy-border`): lightweight structural separation; `copy-hover` fills the copy control on hover.
- **Illustration-only tones** (`diagram-dot`, `diagram-route`, `diagram-server-line`): the dot field, connecting paths and server slots. Keep these scoped to the diagram.

**The Result Accent Rule.** Lime identifies the flag action and its successful result; it does not become the page background or body-text color.

## Typography

**Display Font:** locally served variable Manrope, with UI sans-serif fallback. The font is loaded from `/fonts/manrope.ttf` with swap behavior and weights (200–800). The font is sourced from Google Fonts (`google/fonts/ofl/manrope`); its SIL Open Font License is included at `dynamic/site/fonts/OFL.txt`.

**Body Font:** system UI sans-serif with platform fallbacks. **Code Font:** UI monospace with SFMono-Regular and Consolas fallbacks.

The display is compact and deliberate; ordinary instructions are open and familiar. Frontmatter roles are the observed desktop styles, not a newly imposed type scale.

- **Display:** the two-line hero title. At the narrow breakpoint it uses (42px) with tracking (-1.5px).
- **Headline:** section titles; narrow screens use (24px).
- **Brand:** an unbroken wordmark; narrow header type becomes (19px), footer type is (16px).
- **Body / Intro:** standard instructions and larger lead copy. Lead copy is capped at (480px); SSH prose at (430px).
- **Button / Label:** action labels and small status/footer text.
- **Code:** SSH commands. Narrow terminal text uses (12px); the revealed flag uses (14px) with line-height (1.7).

**The Familiar Instructions Rule.** Reserve the distinctive heading face for headings and the wordmark; keep prose in system sans and commands in monospace.

## Layout

A centered container has maximum width (1220px), with side padding (48px), reduced to (24px) at viewport widths up to (850px). The desktop masthead is (112px) high. The hero uses columns (1.2fr 1fr), a gap (28px) and vertical padding (76px 0 70px); the route diagram is capped at (440px).

The dark reveal panel uses a section number, the instruction/action column and a status column. At the middle breakpoint the status moves below the instructions. The SSH section uses two equal columns with gap (68px), reduced to (30px) at the middle breakpoint.

At viewport widths up to (600px), the masthead becomes (84px) high, the hero and SSH sections stack, and the diagram is capped at (330px). The reveal action fills its available column, the panel padding becomes (25px 20px), and the footer becomes a vertical stack. Long flag values and terminal commands wrap inside their containers.

The spacing frontmatter lists recurring observed gaps and insets; larger section paddings remain component-specific. Anchor scrolling reserves (24px), uses smooth motion, and becomes immediate when reduced motion is requested.

## Elevation & Depth

The implementation has no shadows. Depth comes from the navy reveal panel, the white terminal, the pale page and thin separators. The route illustration uses strokes and flat fills. Hover changes a control's color or adds an underline; it does not lift surfaces.

## Shapes

Mostly rectangular forms use modest rounded corners. The reveal panel has the largest desktop radius and becomes tighter on mobile. The terminal and illustration nodes share a smaller silhouette, the reveal button is more compact, and the copy control is slightly tighter again. Circular geometry is reserved for small status indicators and illustration dots.

## Components

### Buttons

The primary action is compact, solid lime with dark text, a minimum height (48px) and a directional arrow. On hover-capable devices its fill shifts to `lime-hover`. The copy action is a small transparent control with a light border; hovering fills it with `copy-hover`.

All focusable elements share a teal outline (3px) with offset (5px). There is no transition or transform on these controls. On mobile the reveal button fills its column and distributes label and arrow to opposite ends.

### Brand / Masthead

The masthead pairs the unbroken brand link with a small laboratory label. The arrow is an inline SVG, not an image dependency. A thin bottom divider sets the page boundary; small-screen metadata wraps within a narrow right-aligned block.

### Flag Panel

A dark, numbered action region prioritizes the web flag. The initial reveal control exposes the flag output, sets the expanded state, hides itself and focuses the copy button. A reserved feedback line announces copy success or manual-copy guidance without collapsing the panel's rhythm. Flag text is selectable and can wrap anywhere.

### Status Indicator

A small lime dot accompanies a short pale label. The label stays on one line. Its location follows the reveal panel's responsive grid.

### Terminal

A white bordered container keeps SSH secondary. The small header identifies the protocol and port; wrapped monospace commands sit above a divided explanatory note. Muted comments and teal prompts help scanning without changing the command text. The VPN-only requirement stays in normal body text below the example.

### Route Diagram

A flat inline SVG explains two routes to the lab: browser through proxy, or VPN. A dot field, dashed branches, browser window, shield and dark server establish the diagram vocabulary. It scales proportionally and retains an accessible text description.

## Do's and Don'ts

### Do:
- **Do** keep the full Cyber ICE Box wordmark on one line with non-breaking spaces.
- **Do** use Manrope for headings and the brand, system sans for prose, and monospace for commands and flags.
- **Do** preserve the clear web-first, SSH-second hierarchy and the explicit VPN requirement.
- **Do** keep focus visible and allow long flags and commands to wrap.
- **Do** respect reduced motion and maintain the single-column mobile reading order.

### Don't:
- **Don't** use shadows to replace the existing tonal and border hierarchy.
- **Don't** make the secondary SSH terminal compete with the web-flag action.
- **Don't** turn source snippets into decorative monospace body copy.
- **Don't** add color roles, font families or component variants absent from the implementation.
