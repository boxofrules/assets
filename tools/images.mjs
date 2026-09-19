// Optimised siblings for every raster in products/ and marks/: <name>.min.<ext> (same format, smaller, no visible
// loss) and <name>.webp. Originals are never touched; link the original when fidelity matters, .min or .webp on
// the web. Run with `npm run images`; idempotent (skips outputs newer than their source).
import sharp from 'sharp';
import { readdirSync, statSync } from 'node:fs';
import { join, extname, basename, dirname } from 'node:path';

const ROOT = new URL('..', import.meta.url).pathname;
const walk = d => readdirSync(d, { withFileTypes: true }).flatMap(e => e.isDirectory() ? walk(join(d, e.name)) : [join(d, e.name)]);
const fresh = (out, src) => { try { return statSync(out).mtimeMs >= statSync(src).mtimeMs; } catch { return false; } };
const kb = n => `${(n / 1024).toFixed(0)}k`;

let made = 0, before = 0, afterMin = 0, afterWebp = 0;
for (const dir of ['products', 'marks']) {
  for (const src of walk(join(ROOT, dir))) {
    const ext = extname(src).toLowerCase();
    if (!['.png', '.jpg', '.jpeg'].includes(ext) || basename(src).includes('.min.')) continue;
    const stem = join(dirname(src), basename(src, ext));
    const min = `${stem}.min${ext}`, webp = `${stem}.webp`;
    if (fresh(min, src) && fresh(webp, src)) continue;
    const img = sharp(src, { animated: false });
    const meta = await img.metadata();
    if (ext === '.png') await img.clone().png({ compressionLevel: 9, effort: 10, palette: false }).toFile(min);   // lossless
    else await img.clone().jpeg({ quality: 90, mozjpeg: true }).toFile(min);                                       // visually identical
    await img.clone().webp({ quality: 90, effort: 6, alphaQuality: 100 }).toFile(webp);
    const s = statSync(src).size, m = statSync(min).size, w = statSync(webp).size;
    before += s; afterMin += m; afterWebp += w; made++;
    console.log(`${src.slice(ROOT.length)}  ${meta.width}x${meta.height}  ${kb(s)} -> min ${kb(m)}, webp ${kb(w)}`);
  }
}
console.log(`${made} images: ${kb(before)} original, ${kb(afterMin)} .min, ${kb(afterWebp)} .webp`);
