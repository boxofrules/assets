#!/usr/bin/env python3
"""Generate every product's favicons, app icons and web manifest from its icon in marks/.

    python3 tools/web-icons.py            (needs resvg_py + fontTools in the environment, and ImageMagick for the .ico)

Output: web/<product>/ with favicon.svg, favicon.ico (16/32/48), favicon-16.png, favicon-32.png,
apple-touch-icon.png (180), icon-192.png, icon-512.png, icon-maskable-512.png, site.webmanifest,
head.html. The icon sits on a white circle (Apple and favicons), or a white square with the
80 percent safe zone for the maskable icon. Sites copy the folder into public/ as is.
"""
import json, re, subprocess, pathlib, io
import resvg_py
from svgelements import SVG

ROOT = pathlib.Path(__file__).resolve().parent.parent
PRODUCTS = {
    "box-of-rules":      dict(icon="marks/box-of-rules/icon-blue.svg",         name="Box Of Rules",          short="Box Of Rules", theme="#69AFBF", bg="#0B0B0C"),
    "accounts":          dict(icon="marks/accounts/icon-blue.svg",             name="My Box Of…",       short="My Box Of",    theme="#69AFBF", bg="#0B0B0C"),
    "plugins":           dict(icon="marks/plugins/icon.svg",                   name="Box Of Rules Plugins",  short="Plugins",      theme="#8E5EB0", bg="#0B0B0C"),
    "box-of-synths":     dict(icon="marks/box-of-synths/icon-green.svg",       name="Box Of Synths",         short="Synths",       theme="#5FD08A", bg="#0B0B0C"),
    "synth-directory":   dict(icon="marks/synth-directory/icon-light.svg",     name="Synth.Directory",       short="Synth.Dir",    theme="#983811", bg="#F3F2F2"),
    "waveform-analyser": dict(icon="marks/waveform-analyser/icon.svg",         name="Waveform Analyser",     short="Analyser",     theme="#23707F", bg="#0B0B0C"),
}

def inner_and_box(svg_path):
    s = (ROOT / svg_path).read_text()
    vb = [float(v) for v in re.search(r'viewBox="([^"]+)"', s).group(1).split()]
    inner = s[s.index('>', s.index('<svg')) + 1 : s.rindex('</svg>')]
    return inner, vb

def compose(svg_path, size, shape, fill_frac):
    """The icon centred inside a white circle (shape='circle') or a full white square (shape='square'),
    scaled so its longer side is fill_frac of the canvas."""
    inner, (x0, y0, w, h) = inner_and_box(svg_path)
    s = size * fill_frac / max(w, h)
    tx = (size - w * s) / 2 - x0 * s; ty = (size - h * s) / 2 - y0 * s
    bg = f'<circle cx="{size/2}" cy="{size/2}" r="{size/2}" fill="#ffffff"/>' if shape == "circle" else f'<rect width="{size}" height="{size}" fill="#ffffff"/>'
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 {size} {size}">{bg}<g transform="translate({tx:.4f},{ty:.4f}) scale({s:.6f})">{inner}</g></svg>'

def png(svg, size):
    return bytes(resvg_py.svg_to_bytes(svg_string=svg, width=size, height=size, skip_system_fonts=True))

for key, p in PRODUCTS.items():
    out = ROOT / "web" / key; out.mkdir(parents=True, exist_ok=True)
    circle = compose(p["icon"], 512, "circle", 0.62)          # the icon inside the circle with air around it
    (out / "favicon.svg").write_text(circle + "\n")
    for n in (16, 32, 48): (out / f"favicon-{n}.png").write_bytes(png(circle, n))
    (out / "apple-touch-icon.png").write_bytes(png(circle, 180))
    (out / "icon-192.png").write_bytes(png(circle, 192))
    (out / "icon-512.png").write_bytes(png(circle, 512))
    (out / "icon-maskable-512.png").write_bytes(png(compose(p["icon"], 512, "square", 0.56), 512))   # inside Android's 80% safe circle
    subprocess.run(["magick", str(out / "favicon-16.png"), str(out / "favicon-32.png"), str(out / "favicon-48.png"), str(out / "favicon.ico")], check=True)
    (out / "favicon-48.png").unlink()
    manifest = {"name": p["name"], "short_name": p["short"], "icons": [
        {"src": "/icon-192.png", "sizes": "192x192", "type": "image/png"},
        {"src": "/icon-512.png", "sizes": "512x512", "type": "image/png"},
        {"src": "/icon-maskable-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"}],
        "theme_color": p["theme"], "background_color": p["bg"], "display": "standalone", "start_url": "/"}
    (out / "site.webmanifest").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")
    (out / "head.html").write_text(
        '<link rel="icon" href="/favicon.ico" sizes="32x32">\n'
        '<link rel="icon" href="/favicon.svg" type="image/svg+xml">\n'
        '<link rel="apple-touch-icon" href="/apple-touch-icon.png">\n'
        '<link rel="manifest" href="/site.webmanifest">\n'
        f'<meta name="theme-color" content="{p["theme"]}">\n')
    print(f"{key}: {len(list(out.iterdir()))} files")
