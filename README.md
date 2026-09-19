# @boxofrules/assets

Every approved Box Of Rules asset, and the law for using it. Today: the brand kit, marks, fonts, tokens. Next: the plugin imagery (UI shots, gallery renders, og cards, store thumbnails) that people and agents keep getting wrong, so any asset a page or a README needs is confirmed against one manifest rather than picked from a folder. Marks, fonts, tokens, one manifest that says which mark goes where. Every site, service, plugin doc and README takes its brand from here. Nobody draws, recolours or "approximates" a mark; if a surface is not covered by `manifest.json`, ask James.

## The rules

1. **Box Of Rules blue leads every public Box Of Rules visual.** Amber is the accent. `marks/box-of-rules/full-blue.svg` is the default mark; white on ink or coal only when blue fails contrast; black for print.
2. **One sign.** Every product icon carries the Box Of Rules sign, the exact path from `marks/box-of-rules/icon-*.svg`, never a redraw. Products differ by colour and by what sits around the sign: the plugins full logo puts it on the amber waveform in violet; Box Of Synths puts it in a ring of dots in moss green `#5FD08A`, never blue; Synth.Directory and Waveform Analyser have their own icons and use the Box Of Rules full logo in their headers. Check the manifest before picking.
3. **One vocabulary.** `full` = sign + wordmark, `icon` = sign alone, `logotype` = wordmark alone, `card` = the padded 5:3 version for og and social. Same words for every product.
4. **Fonts, the standard for every site:** Syne for headings, Barlow for everything else (body, labels, buttons, tables). Two exceptions: plugins.boxofrules.com headings are Unbounded, and synth.directory stays on Barlow for everything, which is why Unbounded is in `fonts/`; no other site or product uses it. Anton and Oswald are retired. JetBrains Mono is the plugin-UI datasheet face and is not part of this kit. `manifest.json` has a `typography` section stating each product's heading, body and wordmark face. Sites move to the standard on their turns.
5. **Name and tagline:** "Box Of Rules", capital O, always. Tagline "Digitally Analogue". No em dashes in public copy.
6. **Support badges** on public READMEs mirror boxofrules.com/support: Support, PayPal, Patreon, Ko-fi, in that order. The URLs are in `tokens.json`.
7. **Masters live in the vault** (`_vault/08 Assets/logos`, `_vault/08 Assets/fonts`). This package is the distributable copy; a change to a master is a version bump here, never an edit in a site.

## What is in it (1.0.x: the brand kit)

| Path | Contents |
|---|---|
| `marks/box-of-rules/` | full, card, icon and logotype, each in blue, white and black, SVG and PNG |
| `marks/accounts/` | My Box Of, the account hub: full, card, icon and logotype in blue and white, SVG and PNG; the icon IS the Box Of Rules sign |
| `marks/plugins/` | full, card, icon and logotype, SVG and PNG |
| `marks/box-of-synths/` | full, card, icon and logotype in green (the ones to use) and white, SVG and PNG; the blue icon for the record only |
| `marks/synth-directory/` | Synth.Directory: full, card, icon and logotype in a light and a dark theme, SVG and PNG; the fader is the dot |
| `marks/waveform-analyser/` | its icon and full |
| `fonts/` | Syne (variable), Barlow 400 to 700, and Unbounded 700 for plugins headings only, as woff2 with their OFL texts |
| `css/tokens.css` | the colour and type tokens, core plus per-product scopes |
| `css/fonts.css` | the `@font-face` rules |
| `tokens.json` | the same tokens for scripts, og-card builders, plugin docs |
| `manifest.json` | every mark with its product, variant, where to use it and where never to; and each product's typography |
| `web/<product>/` | favicons, app icons, `site.webmanifest` and a `head.html` snippet per product, generated from the product's icon on a white circle; sites copy the folder into `public/` |
| `index.js` | `tokens`, `manifest`, `mark(product, variant)` which throws rather than guess, `--check` |

## Using it

**Favicons and app icons:** copy `web/<product>/` into the site's `public/` root and paste `head.html` into the layout's `<head>`. Regenerate with `npm run web-icons` after an icon changes.

```sh
npm install github:boxofrules/assets#v1.1.1
```

- **Laravel sites:** import `@boxofrules/assets/tokens.css` and `fonts.css` in the site's CSS build, or copy `marks/` and `fonts/` into `public/assets/brand/` at build. `bor/brand` (PHP) becomes a thin wrapper that reads `tokens.json` for the constants it exposes.
- **Cloudflare workers, docs, og-card builders:** `import { tokens, mark } from '@boxofrules/assets'`.
- **Anywhere else:** copy the exact file the manifest names.

Pin the version. Update by bumping the tag, and read `CHANGELOG.md` for what moved.
