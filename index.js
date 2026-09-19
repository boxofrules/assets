// @boxofrules/assets: tokens, the mark manifest, and a resolver so nobody guesses a file name.
import { readFileSync, existsSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const here = dirname(fileURLToPath(import.meta.url));
export const tokens = JSON.parse(readFileSync(join(here, 'tokens.json'), 'utf8'));
export const manifest = JSON.parse(readFileSync(join(here, 'manifest.json'), 'utf8'));

/** Absolute path of a mark by product + variant, e.g. mark('box-of-synths', 'mark, moss green #5FD08A'). Throws rather than guess. */
export function mark(product, variantStartsWith) {
  const m = manifest.marks.find(x => x.product === product && x.variant.startsWith(variantStartsWith));
  if (!m) throw new Error(`@boxofrules/assets: no mark for ${product} / ${variantStartsWith}; see manifest.json`);
  return join(here, m.file);
}

/** Absolute path of a plugin image, e.g. product('box-of-bass', 'ui.png') for the current release,
 *  product('box-of-bass', 'og.jpg', '1.2.2') for that release. Throws rather than guess. */
export function product(slug, file, version = 'latest') {
  const p = manifest.products?.plugins?.[slug];
  if (!p) throw new Error(`@boxofrules/assets: no product ${slug}; see manifest.json products`);
  const v = version === 'latest' ? p.current : version;
  const files = p.versions[v]?.files;
  if (!files || !(file in files)) throw new Error(`@boxofrules/assets: ${slug} ${v} has no ${file}; see manifest.json products`);
  return join(here, version === 'latest' ? p.latest : p.versions[v].dir, file);
}

/** Absolute path of a music release's cover, e.g. musicCover('tax-wealth-not-work'). Throws rather than guess. */
export function musicCover(slug) {
  const r = manifest.products?.music?.[slug];
  if (!r) throw new Error(`@boxofrules/assets: no music release ${slug}; see manifest.json products.music`);
  return join(here, r.dir, r.cover);
}

/** Every mark the manifest names, with whether the file exists (the package's own check). */
export function check() {
  const marks = manifest.marks.flatMap(m => [{ file: m.file, ok: existsSync(join(here, m.file)) }, ...(m.png ? [{ file: m.png, ok: existsSync(join(here, m.png)) }] : [])]);
  const products = Object.values(manifest.products?.plugins ?? {}).flatMap(p => Object.values(p.versions).flatMap(v => Object.keys(v.files).flatMap(f => [
    { file: v.dir + f, ok: existsSync(join(here, v.dir, f)) }, { file: p.latest + f, ok: existsSync(join(here, p.latest, f)) }])));
  const music = Object.values(manifest.products?.music ?? {})
    .filter(r => r.cover)
    .map(r => ({ file: r.dir + r.cover, ok: existsSync(join(here, r.dir, r.cover)) }));
  return [...marks, ...products, ...music];
}

if (process.argv.includes('--check')) {
  const rows = check(); const bad = rows.filter(r => !r.ok);
  console.log(`${rows.length - bad.length}/${rows.length} files present (marks + products)`);
  if (bad.length) { bad.forEach(r => console.log('MISSING', r.file)); process.exit(1); }
}
