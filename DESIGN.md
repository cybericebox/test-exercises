---
name: "Cyber ICE Box — Training Exercises"
description: "A Ukrainian communications archive for introductory flag recovery and VPN access."
colors:
  paper: "#f4f7f5"
  ink: "#142e3a"
  teal: "#14747a"
  focus-teal: "#247c83"
  lime: "#defa8d"
  lime-hover: "#c9ed73"
  white: "#fff"
  body-muted: "#48616b"
  meta-muted: "#526c72"
  on-dark-muted: "#c2d2d6"
  divider: "#d5dfdb"
  record-border: "#c7d7d6"
typography:
  display:
    fontFamily: "Manrope, ui-sans-serif, sans-serif"
    fontSize: "clamp(36px, 4.5vw, 54px)"
    fontWeight: 730
    lineHeight: 1.15
    letterSpacing: "-1.5px"
  headline:
    fontFamily: "Manrope, ui-sans-serif, sans-serif"
    fontSize: "25px"
    fontWeight: 650
    lineHeight: 1.3
    letterSpacing: "-0.5px"
  brand:
    fontFamily: "Manrope, ui-sans-serif, sans-serif"
    fontSize: "21px"
    fontWeight: 750
    letterSpacing: "-0.7px"
  body:
    fontFamily: 'ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif'
    fontSize: "16px"
    lineHeight: 1.65
  intro:
    fontFamily: 'ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif'
    fontSize: "18px"
    lineHeight: 1.65
  button:
    fontFamily: 'ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif'
    fontSize: "15px"
    fontWeight: 700
    lineHeight: 1.65
  metadata:
    fontFamily: 'ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif'
    fontSize: "13px"
    lineHeight: 1.65
  code:
    fontFamily: "ui-monospace, SFMono-Regular, Consolas, monospace"
    fontSize: "14px"
    lineHeight: 1.7
rounded:
  stamp: "4px"
  control: "6px"
  document: "10px"
spacing:
  small: "14px"
  prose: "18px"
  inset: "24px"
  block: "28px"
  columns: "48px"
components:
  button-primary:
    backgroundColor: "{colors.lime}"
    textColor: "{colors.ink}"
    typography: "{typography.button}"
    rounded: "{rounded.control}"
    padding: "10px 20px"
  button-primary-hover:
    backgroundColor: "{colors.lime-hover}"
  archive-record:
    backgroundColor: "{colors.white}"
    padding: "28px 30px"
  incoming-record:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.white}"
    padding: "28px 30px"
  message-document:
    backgroundColor: "{colors.white}"
    rounded: "{rounded.document}"
    padding: "38px 44px"
  command:
    backgroundColor: "{colors.white}"
    textColor: "{colors.ink}"
    typography: "{typography.code}"
    rounded: "{rounded.control}"
    padding: "14px 16px"
---

# Design System: Cyber ICE Box — Training Exercises

## Overview

**Creative North Star: "The Communications Archive"**

A quiet communications archive uses pale paper, navy text and restrained teal to make short records easy to scan. A single dark incoming record and lime action direct the participant to the next document.

Locally served Manrope gives headings and the wordmark their identity; system text carries the Ukrainian instructions. White document surfaces, thin borders and generous spacing keep the archive and its attachment readable.

**Key Characteristics:**
- Pale page with flat, bordered records and documents.
- Manrope headings, system prose and monospace technical text.
- One lime action per primary record or attachment.
- Visible keyboard focus and a single-column mobile reading order.

## Colors

The original paper, navy, teal and lime palette remains intact. Exact source colors are normative in the frontmatter; unused illustration and obsolete control colors are not part of the current system.

### Primary

- **Action Lime** (`lime`, `lime-hover`): the primary navigation/download link and its hover state; also text selection.
- **Archive Teal** (`teal`, `focus-teal`): headline emphasis, text links, active navigation, document stamp and keyboard focus.

### Neutral

- **Paper / Ink** (`paper`, `ink`): page, ordinary text and the dark incoming record.
- **White** (`white`): note, message and command surfaces, plus text on the incoming record.
- **Supporting text** (`body-muted`, `meta-muted`, `on-dark-muted`): prose, record metadata and dark-surface supporting copy.
- **Structural lines** (`divider`, `record-border`): masthead and document separators, record/document outlines and command borders.

**The Action Accent Rule.** Lime identifies the primary next step; teal carries ordinary navigation and document context.

## Typography

Manrope is served locally from `/fonts/manrope.ttf`, with swap behavior and variable weights (200–800); the included SIL Open Font License is at `dynamic/site/fonts/OFL.txt`. System sans carries prose, and UI monospace carries commands, filenames in technical copy and identifiers.

The frontmatter records desktop roles. The incoming record heading uses (30px); the briefing heading uses (22px); the attachment heading uses (20px). The message title uses `clamp(30px, 4vw, 44px)`. Introductory prose is capped at (660px), record prose at (510px), message prose at (650px), and hint prose at (65ch).

At the narrow breakpoint, the journal title uses (38px) with tracking (-1px), the message title (32px), incoming heading (27px), brand (19px), intro (16px), metadata (12px) and code (13px).

**The Familiar Instructions Rule.** Reserve Manrope for headings and the wordmark; keep prose in system sans and technical text in monospace.

## Layout

The masthead and main content share a centered maximum width (1160px) and side padding (40px). The masthead has minimum height (96px), with brand and navigation at opposite sides. Introductory padding is (56px 0 36px).

The archive uses columns `minmax(0, 1.8fr) minmax(0, 1fr)` and gap (48px). Two records share one outlined container; the supporting objective sits alongside. The connection section uses two equal columns with gap (48px), top margin (44px), a top separator and padding (36px 0 52px).

The message page has padding (30px 0 64px). Its white document is capped at (850px), centered with top margin (28px) and inset (38px 44px). Metadata uses (80px 1fr) columns with gap (16px). The attachment aligns descriptive text and action horizontally, separated from prose by fine rules.

At widths up to (760px), side padding becomes (24px), navigation wraps below the brand as needed, the archive and connection become one column, and records/documents use inset (24px). The primary action fills its column. The attachment stacks vertically, and the decorative document stamp is hidden. Commands preserve whitespace while wrapping anywhere. Native anchor scrolling reserves (24px); the site adds no motion or transitions.

## Elevation & Depth

There are no shadows. Depth comes from flat white documents, the dark incoming record, pale page and thin structural borders. Hover changes the primary fill or underlines navigation; surfaces do not lift.

## Shapes

The record group and message document use the document radius. Primary links and command blocks use the control radius. A small outlined document stamp uses the stamp radius and rotates (-5deg) on desktop. Separators remain straight and light.

## Components

### Primary Action

A solid lime anchor advances to the message or downloads its attachment. It has minimum height (48px), centered text and the frontmatter padding. Hover-capable devices use `lime-hover`; narrow layouts make it full width. It retains native link/download semantics.

### Masthead and Navigation

An unbroken wordmark anchors a compact pair of text links. Desktop navigation uses (14px) text and gap (28px); narrow navigation uses (13px) and gap (22px). The current-page link is underlined in teal. Hover underlines links. All focusable elements use a teal outline (3px) with offset (5px).

### Archive Records

A white note and navy incoming transmission share one bordered, clipped container. Each has a metadata row, heading, prose and a link. Metadata is muted; dark-record supporting text uses `on-dark-muted`. The note uses a teal text link; the transmission uses the primary action.

### Message Document and Attachment

The white bordered document contains its heading, a desktop identifier stamp, definition-list metadata and readable prose. The attachment is a separate ruled row with a filename, short descriptor and download action. Its mobile order is text then full-width action.

### Command Block and Hints

The SSH command sits in a simple white bordered `pre` block, followed by credentials and a native expandable hint. The message uses the same `details`/`summary` pattern for its optional hint. Summary text is teal, semibold, with vertical padding (8px); expanded prose has top margin (10px). There is no custom disclosure script.

## Do's and Don'ts

### Do:
- **Do** keep the full Cyber ICE Box wordmark on one line with non-breaking spaces.
- **Do** use Manrope for headings and the brand, system sans for prose, and monospace for commands and identifiers.
- **Do** preserve native links and expandable hints with visible keyboard focus.
- **Do** let commands wrap and stack records, supporting instructions and attachments on narrow screens.

### Don't:
- **Don't** use shadows to replace the existing tonal and border hierarchy.
- **Don't** turn technical snippets into decorative body copy.
- **Don't** add color roles, font families or component variants absent from the implementation.
