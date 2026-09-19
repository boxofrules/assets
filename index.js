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

/** Every mark the manifest names, with whether the file exists (the package's own check). */
export function check() {
  return manifest.marks.flatMap(m => [{ file: m.file, ok: existsSync(join(here, m.file)) }, ...(m.png ? [{ file: m.png, ok: existsSync(join(here, m.png)) }] : [])]);
}

if (process.argv.includes('--check')) {
  const rows = check(); const bad = rows.filter(r => !r.ok);
  console.log(`${rows.length - bad.length}/${rows.length} files present (svg + png)`);
  if (bad.length) { bad.forEach(r => console.log('MISSING', r.file)); process.exit(1); }
}
