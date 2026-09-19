# @boxofrules/brand

The Box Of Rules brand kit, and the law for using it. Marks, fonts, tokens, one manifest that says which mark goes where. Every site, service, plugin doc and README takes its brand from here. Nobody draws, recolours or "approximates" a mark; if a surface is not covered by `manifest.json`, ask James.

## The rules

1. **Box Of Rules blue leads every public Box Of Rules visual.** Amber is the accent. `marks/box-of-rules/full-blue.svg` is the default mark; white on ink or coal only when blue fails contrast; black for print.
2. **Products have their own marks and they are not interchangeable.** The plugins store uses the plugins lockup (violet + amber). Box Of Synths uses the moss-green mark, `#5FD08A`, never the blue variant. Synth.Directory and Waveform Analyser have their own. Check the product's own site before picking.
3. **Fonts:** Anton for big uppercase display, Oswald for labels and buttons at 600, Barlow for body. JetBrains Mono is the plugin-UI datasheet face and is not part of this kit.
4. **Name and tagline:** "Box Of Rules", capital O, always. Tagline "Digitally Analogue". No em dashes in public copy.
5. **Support badges** on public READMEs mirror boxofrules.com/support: Support, PayPal, Patreon, Ko-fi, in that order. The URLs are in `tokens.json`.
6. **Masters live in the vault** (`_vault/08 Assets/logos`, `_vault/08 Assets/fonts`). This package is the distributable copy; a change to a master is a version bump here, never an edit in a site.

## What is in it

| Path | Contents |
|---|---|
| `marks/box-of-rules/` | full logo, icon and logotype, each in blue, white and black (SVG; PNG for full and icon) |
| `marks/plugins/` | the plugins lockup and mark |
| `marks/box-of-synths/` | the Synths mark in green (the one to use), white, and blue (record only) |
| `marks/synth-directory/`, `marks/waveform-analyser/` | their marks and lockups |
| `fonts/` | Anton, Oswald, Barlow as woff2, OFL |
| `css/tokens.css` | the colour and type tokens, core plus per-product scopes |
| `css/fonts.css` | the `@font-face` rules |
| `tokens.json` | the same tokens for scripts, og-card builders, plugin docs |
| `manifest.json` | every mark with its product, variant, where to use it and where never to |
| `index.js` | `tokens`, `manifest`, `mark(product, variant)` which throws rather than guess, `--check` |

## Using it

```sh
npm install github:boxofrules/brand#v1.0.0
```

- **Laravel sites:** import `@boxofrules/brand/tokens.css` and `fonts.css` in the site's CSS build, or copy `marks/` and `fonts/` into `public/assets/brand/` at build. `bor/brand` (PHP) becomes a thin wrapper that reads `tokens.json` for the constants it exposes.
- **Cloudflare workers, docs, og-card builders:** `import { tokens, mark } from '@boxofrules/brand'`.
- **Anywhere else:** copy the exact file the manifest names.

Pin the version. Update by bumping the tag, and read `CHANGELOG.md` for what moved.
