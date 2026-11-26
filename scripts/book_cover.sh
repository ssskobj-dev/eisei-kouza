#!/usr/bin/env bash
# 本の表紙を作る。使い方: scripts/book_cover.sh <講座id> <ページ数> [title] [subtitle] [tagline] [lines(|区切り)] [blurb]
# できるもの: custom/<id>-cover.png（Kindle 1600x2560）、custom/<id>-cover-print.pdf（KDP ペーパーバック、表4+背+表1、塗り足し込み）
set -e
cd "$(dirname "$0")/.."
ID="$1"; PAGES="$2"; shift 2
T=$(command -v typst || find /opt/quarto -name typst -type f | head -1)
ARGS=(--font-path /usr/share/fonts)
[ -n "$1" ] && ARGS+=(--input "title=$1")
[ -n "$2" ] && ARGS+=(--input "subtitle=$2")
[ -n "$3" ] && ARGS+=(--input "tagline=$3")
[ -n "$4" ] && ARGS+=(--input "lines=$4")
[ -n "$5" ] && ARGS+=(--input "blurb=$5")
mkdir -p custom
"$T" compile "${ARGS[@]}" --input mode=kindle --format png --ppi 96 design/book/cover.typ "custom/$ID-cover.png"
"$T" compile "${ARGS[@]}" --input mode=print --input "pages=$PAGES" design/book/cover.typ "custom/$ID-cover-print.pdf"
cp "custom/$ID-cover.png" custom/cover.png   # EPUB が読む名前
echo "custom/$ID-cover.png, custom/$ID-cover-print.pdf"
