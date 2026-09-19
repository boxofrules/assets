#!/bin/bash
# Publish the package to the bor-assets bucket (cdn.boxofrules.com).
#   tools/publish-cdn.sh v1.2.0     -> /v1.2.0/... (cache a year, immutable) and /latest/... (cache an hour)
#   tools/publish-cdn.sh latest     -> /latest/... only
# products/ is ALSO published at the bucket root every time, so a plugin's pictures live at the stable
#   https://cdn.boxofrules.com/products/plugins/<slug>/<version>/... (immutable) and .../<slug>/latest/... (an hour):
# that is the URL the sites, listings and emails use for plugin imagery.
# Needs CLOUDFLARE_API_TOKEN and CLOUDFLARE_ACCOUNT_ID in the environment; uses wrangler via npx.
set -euo pipefail
cd "$(dirname "$0")/.."
tag="${1:?tag or 'latest'}"
ctype() { case "$1" in *.svg) echo image/svg+xml;; *.png) echo image/png;; *.woff2) echo font/woff2;; *.css) echo text/css;; *.json|*.webmanifest) echo application/json;; *.ico) echo image/x-icon;; *.js|*.mjs) echo text/javascript;; *.md|*.txt|*.html) echo text/plain;; *) echo application/octet-stream;; esac; }
put() { npx --yes wrangler@latest r2 object put "bor-assets/${1:+$1/}$2" --file "$2" --content-type "$(ctype "$2")" --cache-control "$3" --remote >/dev/null; }
files=$(find css fonts marks products web tokens.json manifest.json index.js README.md CHANGELOG.md LICENSE.md -type f | sort)
n=0
for f in $files; do
  [ "$tag" != "latest" ] && put "$tag" "$f" "public, max-age=31536000, immutable"
  put latest "$f" "public, max-age=3600"
  case "$f" in products/*)
    case "$f" in */latest/*) put "" "$f" "public, max-age=3600";; *) put "" "$f" "public, max-age=31536000, immutable";; esac;;
  esac
  n=$((n+1))
done
echo "published $n files to https://cdn.boxofrules.com/$tag/ and /latest/, products/ also at the root"
