# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

A Claude Code skill (`aso-playstore-screenshots`) that guides users through creating high-converting Google Play Store screenshots. It is invoked via the `/aso-playstore-screenshots` slash command from within a user's app project.

## Architecture

Four files + one asset make up the skill:

- **SKILL.md** — The skill prompt. Defines a multi-phase workflow: Benefit Discovery → Screenshot Pairing → Generation. Uses Claude Code's memory system to persist state across conversations so users can resume mid-workflow. Generation first creates a deterministic scaffold via compose.py, then sends it to Nano Banana Pro for AI enhancement.
- **compose.py** — A standalone Python compositing script (Pillow-based) that deterministically renders Play Store screenshots. Takes a background hex colour, action verb, benefit descriptor, and app screenshot path, then produces a pixel-perfect 1080×1920 PNG with headline text, device frame template, and the screenshot composited inside. The verb text auto-sizes to fit the canvas width. Includes a font fallback chain (SF Pro Display → Inter → Roboto → Noto Sans) for cross-platform support.
- **generate_frame.py** — Generates the device frame template PNG (`assets/device_frame.png`). Run once to create or update the template. The template is an 864×1920 RGBA PNG with a dark Android phone body, transparent screen cutout, centered punch-hole camera, and side buttons.
- **showcase.py** — Generates a showcase image showing up to 3 final screenshots side-by-side with an optional GitHub link at the bottom. Used as the final step after all screenshots are approved.
- **assets/device_frame.png** — Pre-rendered Android device frame template used by compose.py. Using a template instead of drawing the frame at compose time ensures pixel-perfect consistency across all generated screenshots.

## Running compose.py

```bash
# Requires: pip install Pillow
# Requires: A heavy/black weight font (SF Pro Display Black, Inter Black, Roboto Black, or Noto Sans Black)

python3 compose.py \
  --bg "#E31837" \
  --verb "TRACK" \
  --desc "TRADING CARD PRICES" \
  --screenshot path/to/app-screenshot.png \
  --output output.png
```

## Key Design Decisions

- **Two-stage generation**: compose.py creates a deterministic scaffold first (text + frame + screenshot), then Nano Banana Pro enhances it. This avoids the inconsistencies of generating from scratch.
- **compose.py outputs exact Google Play Console dimensions** (1080×1920 for phone portrait at 9:16) — minimal post-processing needed since 9:16 matches Nano Banana's native aspect ratio.
- **Device frame is a template image** (`assets/device_frame.png`) — not drawn at compose time. Regenerate with `python3 generate_frame.py` if the frame design needs updating.
- **Verb text auto-sizes** — shrinks from 180px down to 100px to fit multi-word verbs (e.g. "TURN YOURSELF") within the canvas width.
- **SKILL.md always generates 3 versions in parallel** for each benefit so the user can pick the best one.
- **The resize step in SKILL.md is mandatory** after every `generate_image` or `edit_image` call — raw Nano Banana output may not be the exact dimensions for Google Play Console.
- **Memory is central to the workflow** — benefits, screenshot assessments, pairings, brand colour, and generation state are all persisted so users can resume across conversations.
- **Cross-platform font support** — compose.py searches for fonts in a priority order (SF Pro → Inter → Roboto → Noto Sans) so it works on both macOS and Linux.
