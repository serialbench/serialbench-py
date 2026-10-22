#!/usr/bin/env bash
# Pushes one format's results.yaml to serialbench/data via the GitHub
# Contents API. Same contract as the ruby harness, with a runtime segment:
# runs/{date}/{platform}-{runtime}-{version}.{format}.yaml
set -euo pipefail

FMT="$1"
RUNTIME_VERSION="$2"
PLATFORM="$3"
RUNTIME="${4:-python}"
RESULTS_FILE="results/${FMT}/results.yaml"
DATA_TOKEN="${DATA_REPO_TOKEN:-}"

if [ -z "$DATA_TOKEN" ]; then
  echo "::warning::DATA_REPO_TOKEN not set — skipping data push"
  exit 0
fi

if [ ! -f "$RESULTS_FILE" ]; then
  echo "::warning::No results at $RESULTS_FILE — skipping"
  exit 0
fi

DATE="${DATA_RUN_DATE:-$(date -u +%Y-%m-%d)}"
TARGET_PATH="runs/${DATE}/${PLATFORM}-${RUNTIME}-${RUNTIME_VERSION}.${FMT}.yaml"
CONTENT=$(base64 < "$RESULTS_FILE" | tr -d '\r\n')

echo "Pushing ${TARGET_PATH} to serialbench/data..."

# Parallel legs race on the branch head: 409 (branch moved) and 422 (file
# exists) are both retried with a fresh sha and backoff.
put_file() {
  # The body goes through a file: passing it as a curl argument hits the
  # ~32KB exec limit on windows/msys once a results.yaml grows ("Argument
  # list too long" -> curl never runs -> the format silently drops).
  local body
  body=$(mktemp /tmp/push-body.XXXXXX)
  if [ -n "${1:-}" ]; then
    printf '{"message": "%s (update)", "content": "%s", "sha": "%s", "branch": "main"}' \
      "${PLATFORM} ${RUNTIME}-${RUNTIME_VERSION} ${FMT}" "$CONTENT" "$1" > "$body"
  else
    printf '{"message": "%s", "content": "%s", "branch": "main"}' \
      "${PLATFORM} ${RUNTIME}-${RUNTIME_VERSION} ${FMT}" "$CONTENT" > "$body"
  fi
  curl -s -o /tmp/data-push-resp.json -w "%{http_code}" -X PUT \
    -H "Authorization: Bearer ${DATA_TOKEN}" \
    -H "Accept: application/vnd.github+json" \
    "https://api.github.com/repos/serialbench/data/contents/${TARGET_PATH}" \
    --data-binary @"$body" || echo 000
  rm -f "$body"
}

# Sha of the existing data file, empty on any failure — guarded so a dead
# pipe (curl -f, grep miss, SIGPIPE under pipefail) cannot kill the leg.
fetch_sha() {
  curl -s -H "Authorization: Bearer ${DATA_TOKEN}" \
    "https://api.github.com/repos/serialbench/data/contents/${TARGET_PATH}" \
    | grep -m1 -oE '"sha": ?"[a-f0-9]{40}"' | grep -oE '[a-f0-9]{40}' || true
}

HTTP_CODE=$(put_file "")
for TRY in 1 2 3 4 5; do
  if [ "$HTTP_CODE" = "200" ] || [ "$HTTP_CODE" = "201" ]; then break; fi
  if [ "$HTTP_CODE" = "409" ] || [ "$HTTP_CODE" = "422" ]; then
    SHA=$(fetch_sha)
    if [ -n "$SHA" ]; then
      echo "attempt $TRY got $HTTP_CODE — refetching sha and retrying"
      sleep $((TRY * 3))
      HTTP_CODE=$(put_file "$SHA")
    else
      # Create-phase 409: the branch moved while creating a NEW file —
      # there is no sha to fetch, so a sha-retry cannot recover. Plain
      # retry; a real 422 (file exists) re-detects on the next pass.
      echo "attempt $TRY got $HTTP_CODE with no existing file — retrying create"
      sleep $((TRY * 3))
      HTTP_CODE=$(put_file "")
    fi
  elif [ "$HTTP_CODE" = "000" ]; then
    # 000 = no HTTP response at all (connection-level blip). Retrying is
    # the only recovery — breaking here silently drops the format.
    echo "attempt $TRY got 000 (no response) — retrying"
    sleep $((TRY * 5))
    HTTP_CODE=$(put_file "")
  else
    break
  fi
done

if [ "$HTTP_CODE" = "200" ] || [ "$HTTP_CODE" = "201" ]; then
  echo "Pushed ${TARGET_PATH}"
else
  echo "::warning::Push failed (${HTTP_CODE}): $(cat /tmp/data-push-resp.json | head -c 200)"
fi

curl -sf -X POST \
  -H "Authorization: Bearer ${DATA_TOKEN}" \
  -H "Accept: application/vnd.github+json" \
  "https://api.github.com/repos/serialbench/serialbench.github.io/dispatches" \
  -d '{"event_type": "data-updated"}' \
  && echo "Site rebuild triggered" \
  || echo "::warning::Failed to trigger site rebuild"
