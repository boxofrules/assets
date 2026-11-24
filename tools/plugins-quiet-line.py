#!/usr/bin/env python3
"""The plugins marks' quiet line (James, 24 Nov 2026): the amber wave keeps full strength at the sign and drops
to 38 percent where it runs behind PLUGINS, so the violet letters read. Rewrites marks/plugins/full.svg,
logotype.svg and card.svg in place (idempotent) and re-exports their PNGs at 1024 px wide with rsvg-convert;
run `npm run images` afterwards for the .min and .webp siblings. icon.svg has no word and is untouched.

    python3 tools/plugins-quiet-line.py
"""
import pathlib, re, subprocess

ROOT = pathlib.Path(__file__).resolve().parent.parent / "marks" / "plugins"
AMBER, QUIET = "#F2A20C", "0.38"
# file: (x where the sign-side squiggle lands on the centre line, x where the end arrow starts)
MARKS = {"full.svg": (610, 2128), "card.svg": (610, 2128), "logotype.svg": (150, 1668)}

for name, (x0, x1) in MARKS.items():
    f = ROOT / name; s = f.read_text()
    if "plg-fade" not in s:
        wave = re.search(r'<path d="(M\d+ \d+C[^"]*?H\d+C[^"]*?)L%d (\d+)" stroke="%s" stroke-width="20" stroke-linejoin="round"/>' % (x1 + 2, AMBER), s)
        arrow = re.search(r'<path d="M%d [^"]+Z" fill="%s"/>' % (x1, AMBER), s)
        assert wave and arrow, name
        grad = (f'<defs><linearGradient id="plg-fade" gradientUnits="userSpaceOnUse" x1="{x0 - 4}" y1="0" x2="{x0 + 80}" y2="0">'
                f'<stop stop-color="{AMBER}"/><stop offset="1" stop-color="{AMBER}" stop-opacity="{QUIET}"/></linearGradient></defs>')
        # the wave stops where the arrow starts, so the two translucent shapes never overlap
        new_wave = f'<path d="{wave.group(1)}L{x1} {wave.group(2)}" stroke="url(#plg-fade)" stroke-width="20" stroke-linejoin="round"/>'
        new_arrow = arrow.group(0).replace("/>", f' fill-opacity="{QUIET}"/>')
        s = s.replace(wave.group(0), new_wave).replace(arrow.group(0), new_arrow)
        i = s.index(">", s.index("<svg")) + 1
        s = s[:i] + "\n" + grad + s[i:]
        f.write_text(s)
    subprocess.run(["rsvg-convert", "-w", "1024", str(f), "-o", str(f.with_suffix(".png"))], check=True)
    print(name, "ok")
