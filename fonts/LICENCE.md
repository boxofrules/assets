# Font licences

The faces are under the SIL Open Font License 1.1. The full licence texts are beside this file:

- **Oswald** (`oswald-var.woff2`, variable, weights 200 to 700): Copyright 2016 The Oswald Project Authors, https://github.com/googlefonts/Oswald. `OFL-Oswald.txt`. The heading face on every site.
- **Unbounded** (`unbounded-700.woff2`, weight 700): Copyright 2022 The Unbounded Project Authors, https://github.com/googlefonts/unbounded. `OFL-Unbounded.txt`. Used for plugins.boxofrules.com headings and the PLUGINS wordmark only.
- **Barlow** (`barlow-400/500/600/700.woff2`): Copyright 2017 The Barlow Project Authors, https://github.com/jpt/barlow. `OFL-Barlow.txt`.

`fonts/desktop/` holds the same faces as TrueType, for native apps and audio plugins, which cannot load woff2:

- **Oswald** (`desktop/Oswald-Variable.ttf`, the variable font, named instances ExtraLight to Bold). Google Fonts ships no statics for Oswald.
- **Barlow** (`desktop/Barlow-Regular.ttf`, `desktop/Barlow-Medium.ttf`).

The OFL allows bundling and redistribution with software, as here, and forbids selling the fonts on their own.

Not in this kit, and not used anywhere: **JetBrains Mono**. An earlier version of this file called it "the plugin-UI datasheet face, shipped inside each plugin". That was never true. No Box Of Rules plugin has ever embedded a monospaced font: every one of them calls `juce::Font::getDefaultMonospacedFontName()`, so the face is whatever the operating system returns (Menlo on macOS, Consolas on Windows) and was never a design decision. Corrected 20 Sep 2026.

Also not in this kit: **Archivo**, which exists here only as outlined paths in the Synth.Directory and Waveform Analyser wordmarks, and **Futura**, which BR108 uses for its panel lettering. Futura is proprietary (it ships with macOS under Apple's licence) and CANNOT be redistributed here. See the BR108 entry under `typography.plugins` in `manifest.json` for what that means for Windows builds.
