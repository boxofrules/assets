#!/bin/bash
# Publish the package to the bor-assets bucket (cdn.boxofrules.com) with ONE parallel, checksummed sync per
# target: only changed files move, the whole package takes seconds. Needs rclone and, in the environment,
# R2_ACCESS_KEY_ID + R2_SECRET_ACCESS_KEY (an R2 API token with Object Read and Write on bor-assets).
#
#   tools/publish-cdn.sh v1.2.0   -> /v1.2.0/ (immutable, cached a year) + /latest/ (cached an hour)
#   tools/publish-cdn.sh latest   -> /latest/ only
# Every run also syncs products/ to the bucket root: products/plugins/<slug>/<version>/ immutable,
# products/plugins/<slug>/latest/ cached an hour. That is the stable URL for plugin pictures.
set -euo pipefail
cd "$(dirname "$0")/.."
tag="${1:?tag or 'latest'}"
: "${R2_ACCESS_KEY_ID:?}" "${R2_SECRET_ACCESS_KEY:?}"
export RCLONE_CONFIG_R2_TYPE=s3 RCLONE_CONFIG_R2_PROVIDER=Cloudflare RCLONE_CONFIG_R2_ACL=private \
       RCLONE_CONFIG_R2_ACCESS_KEY_ID="$R2_ACCESS_KEY_ID" RCLONE_CONFIG_R2_SECRET_ACCESS_KEY="$R2_SECRET_ACCESS_KEY" \
       RCLONE_CONFIG_R2_ENDPOINT="https://9fb419b7a206ac59b0b8ae5eb76769da.r2.cloudflarestorage.com" \
       RCLONE_CONFIG_R2_NO_CHECK_BUCKET=true RCLONE_CONFIG_R2_REGION=auto
YEAR="public, max-age=31536000, immutable"; HOUR="public, max-age=3600"
FILTER=(--filter '+ /css/**' --filter '+ /fonts/**' --filter '+ /marks/**' --filter '+ /web/**' --filter '+ /products/**' \
        --filter '+ /tokens.json' --filter '+ /manifest.json' --filter '+ /index.js' --filter '+ /README.md' --filter '+ /CHANGELOG.md' --filter '+ /LICENSE.md' --filter '- **')
sync() { rclone sync . "r2:bor-assets/$1" "${FILTER[@]}" --checksum --transfers 32 --fast-list --header-upload "Cache-Control: $2" -q; }
[ "$tag" != "latest" ] && sync "$tag" "$YEAR"
sync latest "$HOUR"
# products at the root: versions immutable, latest an hour (sync = latest mirrors the repo; copy = versions only ever gain files)
rclone copy products "r2:bor-assets/products" --filter '- /plugins/*/latest/**' --checksum --transfers 32 --header-upload "Cache-Control: $YEAR" -q
rclone sync products "r2:bor-assets/products" --filter '+ /plugins/*/latest/**' --filter '- **' --checksum --transfers 32 --header-upload "Cache-Control: $HOUR" -q
echo "published https://cdn.boxofrules.com/$tag/ and /latest/, products/ at the root"
