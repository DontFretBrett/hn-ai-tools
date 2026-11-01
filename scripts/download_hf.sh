#!/bin/bash
# Download monthly HN parquet files from Hugging Face open-index/hacker-news (ODC-By 1.0).
# Sequential, polite: one file at a time with a short pause. Skips files already complete.
set -u
cd "$(dirname "$0")/../data/raw"
BASE="https://huggingface.co/datasets/open-index/hacker-news/resolve/main/data"
for ym in $(python3 -c "
for y in range(2023,2027):
  for m in range(1,13):
    if (y,m)<=(2026,8): print(f'{y}-{m:02d}')
"); do
  y=${ym%%-*}; f="$ym.parquet"
  if [ -s "$f" ] && [ ! -f "$f.part" ]; then echo "skip $f"; continue; fi
  echo "get $f"; curl -sSL --retry 3 -o "$f.part" "$BASE/$y/$f" && mv "$f.part" "$f" || echo "FAIL $f"
  sleep 2
done
echo DONE
