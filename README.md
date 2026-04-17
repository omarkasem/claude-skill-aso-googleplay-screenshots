# ASO Play Store Screenshots

A Claude Code skill that generates high-converting Google Play Store screenshots for your Android app. It analyzes your codebase, identifies core benefits, and creates professional screenshot images using AI.

## What It Does

1. **Benefit Discovery** — Analyzes your app's codebase to identify the 3-5 core benefits that drive downloads
2. **Screenshot Pairing** — Reviews your app screenshots, rates them, and pairs each with the best benefit
3. **Generation** — Creates polished Play Store screenshots using a two-stage process: deterministic scaffolding (compose.py) + AI enhancement (Nano Banana Pro via Gemini MCP)
4. **Showcase** — Generates a preview image with all screenshots side-by-side

## Installation

### 1. Add the skill to Claude Code

```bash
claude install-skill github.com/adamlyttleapps/claude-skill-aso-playstore-screenshots
```

### 2. Install Python dependencies

```bash
pip install Pillow
```

### 3. Font requirement

The skill uses **Montserrat Black** for headline text — the industry-standard font for high-converting app store marketing screenshots. Install it from [Google Fonts](https://fonts.google.com/specimen/Montserrat), or on macOS:

```bash
brew install --cask font-montserrat
```

The skill searches for fonts in this order:

| Priority | Font | Path |
|----------|------|------|
| 1 | **Montserrat Black** | `~/Library/Fonts/Montserrat-Black.ttf` (macOS) |
| 2 | Montserrat Black | `/Library/Fonts/Montserrat-Black.ttf` (macOS system) |
| 3 | Montserrat Black | `/usr/share/fonts/truetype/montserrat/Montserrat-Black.ttf` (Linux) |
| 4 | SF Pro Display Black | `/Library/Fonts/SF-Pro-Display-Black.otf` (fallback) |
| 5 | Inter Black | `/usr/share/fonts/truetype/inter/Inter-Black.ttf` (fallback) |
| 6 | Roboto Black | `/usr/share/fonts/truetype/roboto/Roboto-Black.ttf` (fallback) |

### 4. Set up Gemini MCP (for AI enhancement)

The generation phase requires [@houtini/gemini-mcp](https://www.npmjs.com/package/@houtini/gemini-mcp) to be configured as an MCP server in Claude Code:

```bash
npm install -g @houtini/gemini-mcp
```

Then add it to your Claude Code MCP config (`~/.claude/settings.json` or project `.mcp.json`).

## Usage

From within your app's project directory, run:

```
/aso-playstore-screenshots
```

The skill will guide you through each phase interactively. Progress is saved to Claude Code's memory system, so you can resume across conversations.

## How It Works

### Scaffold → Enhance Pipeline

Rather than generating screenshots from scratch (which produces inconsistent results), the skill uses a two-stage approach:

1. **compose.py** creates a deterministic scaffold with exact text positioning, device frame, and your app screenshot composited inside
2. **Nano Banana Pro** (via Gemini MCP) enhances the scaffold — adding a photorealistic device frame, breakout elements, and visual polish

This ensures consistent layout across all screenshots while letting AI handle the creative enhancement.

### Output

Screenshots are saved to a `screenshots/` directory in your project:

```
screenshots/
  01-benefit-slug/          ← working versions
    scaffold.png            ← deterministic compose.py output
    v1.jpg, v2.jpg, v3.jpg  ← AI-enhanced versions
    v1-resized.jpg, ...     ← resized to Play Store dimensions
  final/                    ← approved screenshots, ready to upload
    01-benefit-slug.jpg
    02-benefit-slug.jpg
  showcase.png              ← preview image with all screenshots
```

The `final/` folder contains Play Store-ready screenshots at Google's recommended dimensions (default: 1080×1920px, portrait 9:16).

## Files

| File | Purpose |
|------|---------|
| `SKILL.md` | The skill prompt — defines the multi-phase workflow |
| `compose.py` | Deterministic scaffold generator (Pillow-based) |
| `generate_frame.py` | Generates the device frame template |
| `showcase.py` | Generates the side-by-side showcase image |
| `assets/device_frame.png` | Pre-rendered Android device frame template |

## License

MIT
